"""
Compute daily storage integrals and Δt-refinement ratios for the
existing Test 2 experiment matrix.

This reproduces a slimmer version of the run_experiments.py Test 2 to
extract two new diagnostics for the updated §4.3 / §5.2 of the report:

  - storage_ratio = (∫G dt over day 2 for this scheme) / (∫G dt for FTCS dt=15s ref)
                   — confirms the "approximately conserved daily mean" claim
                   in §5.4 with a number rather than asserting it.

  - dt_refine_ratio = RMSE_Ts(dt=600s) / RMSE_Ts(dt=60s)
                     — for BTCS this should be ~10 if the splitting error
                     is first-order in Δt; for CN it should be the same
                     (also first-order) since CN's per-scheme order is
                     subdominant to the splitting error.
"""

import os
import sys
import numpy as np
import pandas as pd
from scipy.linalg import solve_banded

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shap_attribution import (
    make_grid, assign_layered_props, step_alpha,
    SIGMA_SB, C_H, RHO_AIR, CP_AIR,
)

# Substrate-specific constants (these match run_experiments.py exactly)
SUBSTRATES = {
    "asphalt_road": [
        (0.05, 0.75,  2.0e6),
        (0.25, 1.40,  2.4e6),
        (1.00, 0.30,  1.3e6),
        (2.00, 0.50,  1.8e6),
    ],
    "concrete_roof": [
        (0.10, 1.50,  2.1e6),
        (0.20, 0.04,  0.08e6),
        (2.00, 0.15,  1.5e6),
    ],
    "bare_soil": [
        (2.00, 0.30,  1.3e6),
    ],
}

ALBEDO   = {"asphalt_road": 0.10, "concrete_roof": 0.30, "bare_soil": 0.20}
EMIS     = {"asphalt_road": 0.95, "concrete_roof": 0.92, "bare_soil": 0.95}


def S_down(t):
    omega = 2.0 * np.pi / 86400.0
    val = 1000.0 * np.cos(omega * (t - 12 * 3600.0))
    return np.maximum(val, 0.0)


def L_down_func(t):
    omega = 2.0 * np.pi / 86400.0
    return 350.0 + 20.0 * np.cos(omega * (t - 14 * 3600.0))


def T_air(t):
    omega = 2.0 * np.pi / 86400.0
    return 292.5 + 7.5 * np.cos(omega * (t - 14 * 3600.0))


def U_wind(_t):
    return 3.0


def seb_residual(Ts0, T_int, dzc0, lam_h0, t, surface_key):
    Sd = S_down(t); Ld = L_down_func(t); Ta = T_air(t); U = U_wind(t)
    r_a = 1.0 / (C_H * U)
    R_n = (1.0 - ALBEDO[surface_key]) * Sd + EMIS[surface_key] * Ld - EMIS[surface_key] * SIGMA_SB * Ts0**4
    H = RHO_AIR * CP_AIR * (Ts0 - Ta) / r_a
    G = lam_h0 * (Ts0 - T_int) / dzc0
    return R_n - H - G


def seb_dresidual_dT(Ts0, dzc0, lam_h0, surface_key):
    dRn = -4.0 * EMIS[surface_key] * SIGMA_SB * Ts0**3
    U = U_wind(0.0)
    r_a = 1.0 / (C_H * U)
    dH = RHO_AIR * CP_AIR / r_a
    dG = lam_h0 / dzc0
    return dRn - dH - dG


def solve_seb(T_int, dzc0, lam_h0, t, surface_key, Ts0_init, tol=1e-4, max_iter=20):
    Ts0 = Ts0_init
    for _ in range(max_iter):
        f = seb_residual(Ts0, T_int, dzc0, lam_h0, t, surface_key)
        df = seb_dresidual_dT(Ts0, dzc0, lam_h0, surface_key)
        dTs = -f / df
        Ts0 += dTs
        if abs(dTs) < tol:
            return Ts0
    return Ts0


def initial_profile(z, T0, A_amp, omega, kappa_eff):
    d = np.sqrt(2.0 * kappa_eff / omega)
    return T0 + A_amp * np.exp(-z / d) * np.cos(-z / d)


def run_seb_column(surface_key, alpha, dt, n_days=2):
    layers = SUBSTRATES[surface_key]
    z_top = 2.0
    if surface_key == "concrete_roof":
        z, dzs, dzc = make_grid(z_top=z_top, n_levels=30, stretch=1.18, dz1=0.005)
    elif surface_key == "asphalt_road":
        z, dzs, dzc = make_grid(z_top=z_top, n_levels=28, stretch=1.20, dz1=0.005)
    else:
        z, dzs, dzc = make_grid(z_top=z_top, n_levels=24, stretch=1.25, dz1=0.01)

    lam, C, lam_half = assign_layered_props(z, layers)
    omega = 2.0 * np.pi / 86400.0
    kappa_top = lam[0] / C[0]
    T_mean = 292.5; A0 = 7.5
    T = initial_profile(z, T_mean, A0, omega, kappa_top)
    Ts0 = solve_seb(T[1], dzc[0], lam_half[0], 0.0, surface_key, T[0])
    T[0] = Ts0

    t_end = n_days * 86400.0
    n_steps = int(round(t_end / dt))
    dt_use = t_end / n_steps

    times = [0.0]
    Ts0_arr = [T[0]]
    G_arr = [lam_half[0] * (T[0] - T[1]) / dzc[0]]

    blew_up = False
    for n in range(1, n_steps + 1):
        t_now = n * dt_use
        T = step_alpha(T, dt_use, dzs, dzc, lam_half, C, alpha,
                       T_top=T[0], lower_bc="neumann")
        if not np.all(np.isfinite(T)) or np.max(np.abs(T - T_mean)) > 1e5:
            blew_up = True
            break
        Ts0 = solve_seb(T[1], dzc[0], lam_half[0], t_now, surface_key, T[0])
        T[0] = Ts0
        times.append(t_now); Ts0_arr.append(T[0])
        G_arr.append(lam_half[0] * (T[0] - T[1]) / dzc[0])

    return {
        "surface": surface_key, "alpha": alpha, "dt": dt_use,
        "times": np.array(times), "Ts0": np.array(Ts0_arr),
        "G": np.array(G_arr), "blew_up": blew_up,
    }


def main():
    surfaces = ["asphalt_road", "concrete_roof", "bare_soil"]
    schemes = [("FTCS", 0.0), ("BTCS", 1.0), ("CN", 0.5)]
    dts = [15.0, 60.0, 600.0]

    print("Running Test 2 experiment matrix (27 cells)...")
    results = {}
    for surface in surfaces:
        for sname, alpha in schemes:
            for dt in dts:
                key = (surface, sname, dt)
                r = run_seb_column(surface, alpha, dt, n_days=2)
                results[key] = r
                tag = "BLEW UP" if r["blew_up"] else "OK"
                print(f"  {surface:14s} | {sname} | dt={dt:5.0f}s  {tag}")

    # Compute storage integral and amplitude metrics
    rows = []
    for surface in surfaces:
        ref = results[(surface, "FTCS", 15.0)]
        if ref["blew_up"]:
            continue
        mask_ref = ref["times"] >= 86400.0
        t_ref = ref["times"][mask_ref]
        G_ref = ref["G"][mask_ref]
        Ts_ref = ref["Ts0"][mask_ref]
        AG_ref = 0.5 * (np.max(G_ref) - np.min(G_ref))
        S_ref = np.trapezoid(G_ref, t_ref)  # daily storage integral

        for sname, _ in schemes:
            for dt in dts:
                r = results[(surface, sname, dt)]
                if r["blew_up"]:
                    rows.append({
                        "surface": surface, "scheme": sname, "dt": dt,
                        "AG_ratio": np.nan, "rmse_Ts": np.nan,
                        "storage_ratio": np.nan, "blew_up": True,
                    })
                    continue
                mask = r["times"] >= 86400.0
                t = r["times"][mask]; G = r["G"][mask]; Ts = r["Ts0"][mask]
                AG = 0.5 * (np.max(G) - np.min(G))
                S = np.trapezoid(G, t)
                Ts_on_ref = np.interp(t_ref, t, Ts)
                rmse = float(np.sqrt(np.mean((Ts_on_ref - Ts_ref) ** 2)))
                rows.append({
                    "surface": surface, "scheme": sname, "dt": dt,
                    "AG_ratio": AG / AG_ref,
                    "rmse_Ts": rmse,
                    "storage_ratio": S / S_ref if abs(S_ref) > 1.0 else np.nan,
                    "blew_up": False,
                })

    df = pd.DataFrame(rows)
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "tables", "test2_extended_metrics.csv")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"\nSaved {out_path}")
    print()
    print("Extended Test 2 metrics:")
    print(df.to_string(index=False))

    # Print the Δt-refinement ratios for §5.2
    print("\n" + "=" * 70)
    print("Δt-refinement ratios (RMSE_Ts at Δt=600s / RMSE_Ts at Δt=60s):")
    print("First-order in Δt would give ratio ≈ 10.")
    print("=" * 70)
    for surface in surfaces:
        for sname, _ in schemes:
            r600 = df[(df["surface"] == surface) & (df["scheme"] == sname)
                      & (df["dt"] == 600.0)]
            r60 = df[(df["surface"] == surface) & (df["scheme"] == sname)
                     & (df["dt"] == 60.0)]
            if len(r600) and len(r60) and not r600["blew_up"].iloc[0] and not r60["blew_up"].iloc[0]:
                ratio = r600["rmse_Ts"].iloc[0] / r60["rmse_Ts"].iloc[0]
                print(f"  {surface:14s} | {sname:4s} | "
                      f"60s: {r60['rmse_Ts'].iloc[0]:.3f} K  "
                      f"600s: {r600['rmse_Ts'].iloc[0]:.3f} K  "
                      f"ratio: {ratio:5.2f}")
            else:
                print(f"  {surface:14s} | {sname:4s} | one or both BLEW UP")


if __name__ == "__main__":
    main()
