"""
SHAP Attribution Analysis for the BTCS Coarse-Δt Surface-Temperature Error
==========================================================================

This script implements Section 6 of the CLIM-715 project: an independent
attribution analysis of the BTCS error in the coarse-Δt regime, using a
gradient-boosted regression on synthetic substrate columns.

Pipeline:
  1. Sample N = 200 three-layer substrate columns from a plausible prior
     (lambda, C, layer thicknesses) covering the urban-substrate range.
  2. For each column, run the BTCS solver at dt = 600 s and the FTCS
     reference at dt = 15 s, both for 2 diurnal cycles under the same
     synthetic forcing as Test 2 of the main project.
  3. Compute the day-2 RMSE in surface temperature against the reference
     (the same metric used in Section 4 of the main report).
  4. Compute substrate descriptors:
        - bulk admittance mu_eff = sqrt(lambda_eff * C_eff)
        - top-cell kappa
        - max lambda contrast at any internal interface
        - number of internal interfaces (0, 1, or 2 for a 3-layer column)
        - depth of first internal interface
        - top-cell dz
  5. Fit GradientBoostingRegressor on (descriptors -> RMSE_Ts) and run
     SHAP TreeExplainer to produce feature importance.
  6. Plot Figure 6 (SHAP summary plot + partial dependence on the
     dominant feature).

Output:
  - figs/fig6_shap_attribution.png
  - tables/synthetic_dataset.csv
  - tables/shap_summary.csv

Author: Shammunul Islam
Course: CLIM-715 Numerical Methods for Climate and Weather Modeling
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded
from sklearn.ensemble import GradientBoostingRegressor
import shap

# ---------------------------------------------------------------------------
# 0. Setup
# ---------------------------------------------------------------------------

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TABLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tables")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TABLES, exist_ok=True)

plt.rcParams["figure.dpi"] = 130
plt.rcParams["savefig.dpi"] = 200
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 11
plt.rcParams["axes.labelsize"] = 10
plt.rcParams["legend.fontsize"] = 9
plt.rcParams["axes.facecolor"] = "#fafafa"
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

C_BTCS = "#00B8A9"
C_REF  = "#666666"

# Reproducibility
SEED = 42
rng = np.random.default_rng(SEED)


# ---------------------------------------------------------------------------
# 1. Solver functions (replicated from run_experiments.py to keep this
#    script self-contained; identical numerics as the main project)
# ---------------------------------------------------------------------------

def make_grid(z_top=2.0, n_levels=24, stretch=1.20, dz1=0.005):
    """Stretched grid downward from the surface (same as Test 2 main project)."""
    dzs = dz1 * stretch ** np.arange(n_levels)
    if np.sum(dzs) > z_top:
        cumulative = np.cumsum(dzs)
        n_levels = int(np.searchsorted(cumulative, z_top)) + 1
        dzs = dzs[:n_levels]
    dzs[-1] = z_top - np.sum(dzs[:-1])
    z = np.zeros(n_levels)
    z[0] = dzs[0] / 2.0
    for j in range(1, n_levels):
        z[j] = z[j - 1] + (dzs[j - 1] + dzs[j]) / 2.0
    dzc = np.diff(z)
    return z, dzs, dzc


def assign_layered_props(z, layers):
    """Assign cell-centre lambda, C and harmonic-mean lambda at half-levels.

    layers = list of (z_bottom, lambda, C) tuples ordered from surface down.
    """
    N = len(z)
    lam = np.zeros(N)
    C = np.zeros(N)
    for j in range(N):
        for (zb, lj, cj) in layers:
            if z[j] <= zb:
                lam[j] = lj
                C[j] = cj
                break
        else:
            lam[j] = layers[-1][1]
            C[j] = layers[-1][2]
    lam_half = 2.0 / (1.0 / lam[:-1] + 1.0 / lam[1:])
    return lam, C, lam_half


def build_btcs_matrix(dt, dzs, dzc, lam_half, C, alpha=1.0, lower_bc="neumann"):
    """Build the banded LHS matrix A for the alpha-weighted theta-method.

    Since the matrix depends only on (dt, dzs, dzc, lam_half, C, alpha) and
    not on the current T, it can be built once and reused across all time
    steps. This is a 30x speedup for the BTCS path.

    Returns the (3, N) banded representation suitable for solve_banded.
    Also returns the precomputed coefficients a[j], b[j] for the RHS update.
    """
    N = len(dzs)
    diag_main = np.ones(N)
    diag_upper = np.zeros(N)
    diag_lower = np.zeros(N)
    a_arr = np.zeros(N)
    b_arr = np.zeros(N)

    for j in range(1, N - 1):
        a = dt * lam_half[j - 1] / (C[j] * dzs[j] * dzc[j - 1])
        b = dt * lam_half[j] / (C[j] * dzs[j] * dzc[j])
        a_arr[j] = a
        b_arr[j] = b
        diag_lower[j - 1] = -alpha * a
        diag_main[j] = 1.0 + alpha * (a + b)
        diag_upper[j + 1] = -alpha * b

    diag_main[0] = 1.0
    diag_upper[1] = 0.0

    if lower_bc == "neumann":
        diag_main[N - 1] = 1.0
        diag_lower[N - 2] = -1.0
    else:
        diag_main[N - 1] = 1.0
        diag_lower[N - 2] = 0.0

    ab = np.zeros((3, N))
    ab[0, :] = diag_upper
    ab[1, :] = diag_main
    ab[2, :] = diag_lower
    return ab, a_arr, b_arr


def step_btcs_fast(T, ab, a_arr, b_arr, T_top, lower_bc="neumann"):
    """Fast BTCS step using precomputed banded matrix."""
    N = len(T)
    rhs = T.copy()
    rhs[0] = T_top
    if lower_bc == "neumann":
        rhs[N - 1] = 0.0
    else:
        rhs[N - 1] = T[N - 1]
    return solve_banded((1, 1), ab, rhs)


def step_alpha(T, dt, dzs, dzc, lam_half, C, alpha,
               T_top=None, lower_bc="neumann"):
    """alpha-weighted theta-method step. alpha=0 FTCS, 0.5 CN, 1 BTCS.

    NOTE: this is the slow general-purpose version, retained only for
    reference. The fast path used in the experiment loop is build_btcs_matrix
    + step_btcs_fast above.
    """
    N = len(T)

    if alpha == 0.0:
        T_new = T.copy()
        # vectorized FTCS interior update
        flux_up = lam_half[1:] * (T[2:] - T[1:-1]) / dzc[1:]
        flux_dn = lam_half[:-1] * (T[1:-1] - T[:-2]) / dzc[:-1]
        T_new[1:-1] = T[1:-1] + (dt / (C[1:-1] * dzs[1:-1])) * (flux_up - flux_dn)
        if T_top is not None:
            T_new[0] = T_top
        else:
            T_new[0] = T[0]
        if lower_bc == "neumann":
            T_new[-1] = T_new[-2]
        else:
            T_new[-1] = T[-1]
        return T_new

    ab, a_arr, b_arr = build_btcs_matrix(dt, dzs, dzc, lam_half, C, alpha, lower_bc)
    rhs = T.copy()
    if alpha != 1.0:
        # CN/general theta: RHS includes explicit (1-alpha) part
        rhs[1:-1] = (T[1:-1]
                     + (1 - alpha) * a_arr[1:-1] * (T[:-2] - T[1:-1])
                     + (1 - alpha) * b_arr[1:-1] * (T[2:] - T[1:-1]))
    if T_top is None:
        T_top = T[0]
    rhs[0] = T_top
    if lower_bc == "neumann":
        rhs[N - 1] = 0.0
    else:
        rhs[N - 1] = T[N - 1]
    return solve_banded((1, 1), ab, rhs)


# ---------------------------------------------------------------------------
# 2. SEB / Newton iteration (uniform forcing, generic urban surface)
# ---------------------------------------------------------------------------

SIGMA_SB = 5.670374419e-8
ALBEDO   = 0.15      # generic urban (between asphalt and concrete)
EMIS     = 0.95
C_H      = 5.0e-3
RHO_AIR  = 1.2
CP_AIR   = 1005.0


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


def seb_residual(Ts0, T_int, dzc0, lam_h0, t):
    Sd = S_down(t); Ld = L_down_func(t); Ta = T_air(t); U = U_wind(t)
    r_a = 1.0 / (C_H * U)
    R_n = (1.0 - ALBEDO) * Sd + EMIS * Ld - EMIS * SIGMA_SB * Ts0**4
    H = RHO_AIR * CP_AIR * (Ts0 - Ta) / r_a
    G = lam_h0 * (Ts0 - T_int) / dzc0
    return R_n - H - G


def seb_dresidual_dT(Ts0, dzc0, lam_h0):
    dRn = -4.0 * EMIS * SIGMA_SB * Ts0**3
    U = U_wind(0.0)
    r_a = 1.0 / (C_H * U)
    dH = RHO_AIR * CP_AIR / r_a
    dG = lam_h0 / dzc0
    return dRn - dH - dG


def solve_seb(T_int, dzc0, lam_h0, t, Ts0_init, tol=1e-4, max_iter=20):
    Ts0 = Ts0_init
    for _ in range(max_iter):
        f = seb_residual(Ts0, T_int, dzc0, lam_h0, t)
        df = seb_dresidual_dT(Ts0, dzc0, lam_h0)
        dTs = -f / df
        Ts0 += dTs
        if abs(dTs) < tol:
            return Ts0
    return Ts0


# ---------------------------------------------------------------------------
# 3. Substrate column simulator
# ---------------------------------------------------------------------------

def initial_profile(z, T0, A_amp, omega, kappa_eff):
    d = np.sqrt(2.0 * kappa_eff / omega)
    return T0 + A_amp * np.exp(-z / d) * np.cos(-z / d)


def run_column(layers, alpha, dt, n_days=2):
    """Run one substrate column under the SEB.

    Uses the fast precomputed-matrix path for BTCS (alpha = 1.0).
    """
    z_top = 2.0
    z, dzs, dzc = make_grid(z_top=z_top, n_levels=28, stretch=1.20, dz1=0.005)
    lam, C, lam_half = assign_layered_props(z, layers)

    omega = 2.0 * np.pi / 86400.0
    kappa_top = lam[0] / C[0]
    T_mean = 292.5; A0 = 7.5
    T = initial_profile(z, T_mean, A0, omega, kappa_top)
    Ts0 = solve_seb(T[1], dzc[0], lam_half[0], 0.0, T[0])
    T[0] = Ts0

    t_end = n_days * 86400.0
    n_steps = int(round(t_end / dt))
    dt_use = t_end / n_steps

    times = [0.0]
    Ts0_arr = [T[0]]
    G_arr = [lam_half[0] * (T[0] - T[1]) / dzc[0]]

    # Precompute the banded matrix once (it depends only on dt, grid,
    # lam_half, C, alpha — all fixed across the time loop).
    if alpha == 1.0:
        ab, a_arr, b_arr = build_btcs_matrix(dt_use, dzs, dzc, lam_half, C,
                                              alpha=1.0, lower_bc="neumann")
        N = len(T)
        blew_up = False
        for n in range(1, n_steps + 1):
            t_now = n * dt_use
            # Fast BTCS step
            rhs = T.copy()
            rhs[0] = T[0]   # Dirichlet from previous Ts0
            rhs[N - 1] = 0.0
            T = solve_banded((1, 1), ab, rhs)
            if not np.all(np.isfinite(T)) or np.max(np.abs(T - T_mean)) > 1e5:
                blew_up = True
                break
            Ts0 = solve_seb(T[1], dzc[0], lam_half[0], t_now, T[0])
            T[0] = Ts0
            times.append(t_now); Ts0_arr.append(T[0])
            G_arr.append(lam_half[0] * (T[0] - T[1]) / dzc[0])
    else:
        # General-purpose path (FTCS or CN)
        blew_up = False
        for n in range(1, n_steps + 1):
            t_now = n * dt_use
            T = step_alpha(T, dt_use, dzs, dzc, lam_half, C, alpha,
                           T_top=T[0], lower_bc="neumann")
            if not np.all(np.isfinite(T)) or np.max(np.abs(T - T_mean)) > 1e5:
                blew_up = True
                break
            Ts0 = solve_seb(T[1], dzc[0], lam_half[0], t_now, T[0])
            T[0] = Ts0
            times.append(t_now); Ts0_arr.append(T[0])
            G_arr.append(lam_half[0] * (T[0] - T[1]) / dzc[0])

    return {
        "times": np.array(times),
        "Ts0": np.array(Ts0_arr),
        "G": np.array(G_arr),
        "z": z, "lam": lam, "C": C,
        "blew_up": blew_up,
    }


# ---------------------------------------------------------------------------
# 4. Sample synthetic substrate columns from a plausible prior
# ---------------------------------------------------------------------------

def sample_substrate(rng):
    """Sample one 3-layer substrate column.

    The prior covers a wide range of plausible urban substrate configurations:
    - Top layer: lambda in [0.10, 2.50] W/m/K, C in [0.5e6, 3.0e6] J/m^3/K
                 thickness in [2, 15] cm
    - Middle layer: lambda in [0.05, 2.50] W/m/K, C in [0.1e6, 3.0e6]
                    thickness in [5, 30] cm
    - Bottom layer: lambda in [0.10, 1.00] W/m/K, C in [1.0e6, 2.5e6]
                    extends to z = 200 cm

    The wide middle-layer lambda range deliberately includes the rigid-
    insulation extreme (~0.04) and high-conductivity aggregate (~1.5).

    Returns
    -------
    layers : list of (z_bottom, lambda, C) tuples
    """
    # Top layer thickness (cm)
    h1 = rng.uniform(0.02, 0.15)
    # Middle layer thickness (cm)
    h2 = rng.uniform(0.05, 0.30)
    z2 = h1 + h2
    z3 = 2.0  # always extend to 2 m

    lam1 = rng.uniform(0.10, 2.50)
    lam2 = rng.uniform(0.05, 2.50)
    lam3 = rng.uniform(0.10, 1.00)

    # heat capacity correlates loosely with lambda (denser materials)
    # but with substantial scatter
    C1 = rng.uniform(0.5e6, 3.0e6)
    C2 = rng.uniform(0.1e6, 3.0e6)
    C3 = rng.uniform(1.0e6, 2.5e6)

    return [
        (h1, lam1, C1),
        (z2, lam2, C2),
        (z3, lam3, C3),
    ]


def compute_descriptors(layers, dt_coarse=600.0, dz_top_grid=0.005):
    """Compute substrate-level descriptors used as ML features.

    Parameters
    ----------
    layers : list of (z_bottom, lambda, C) tuples (3-layer column)
    dt_coarse : float
        The coarse Δt used for BTCS in seconds. Used to compute dt_ratio.
    dz_top_grid : float
        The top-cell thickness in metres (matches make_grid's dz1=0.005).
    """
    h1, lam1, C1 = layers[0]
    z2, lam2, C2 = layers[1]
    z3, lam3, C3 = layers[2]

    # layer thicknesses
    dh1 = h1
    dh2 = z2 - h1
    dh3 = z3 - z2

    # Effective top-30cm bulk admittance (depth-weighted)
    weights = []
    lams = []
    Cs = []
    if h1 < 0.30:
        weights.append(min(h1, 0.30))
        lams.append(lam1); Cs.append(C1)
    if z2 < 0.30:
        weights.append(min(z2 - h1, 0.30 - h1))
        lams.append(lam2); Cs.append(C2)
        if 0.30 > z2:
            weights.append(0.30 - z2)
            lams.append(lam3); Cs.append(C3)
    else:
        weights.append(0.30 - h1)
        lams.append(lam2); Cs.append(C2)
    weights = np.array(weights); lams = np.array(lams); Cs = np.array(Cs)
    weights = weights / weights.sum()
    lam_eff = (weights * lams).sum()
    C_eff = (weights * Cs).sum()
    mu_eff = np.sqrt(lam_eff * C_eff)

    # Top-cell kappa (sets FTCS bound)
    kappa_top = lam1 / C1

    # Lambda contrasts at each interface
    contrast_12 = max(lam1 / lam2, lam2 / lam1)
    contrast_23 = max(lam2 / lam3, lam3 / lam2)
    max_contrast = max(contrast_12, contrast_23)

    # Number of "significant" interfaces (contrast > 1.5)
    n_interfaces = int(contrast_12 > 1.5) + int(contrast_23 > 1.5)

    # Depth of first significant interface
    if contrast_12 > 1.5:
        first_iface_depth = h1
    elif contrast_23 > 1.5:
        first_iface_depth = z2
    else:
        first_iface_depth = 2.0  # no significant interface

    # Dimensionless coarse-Δt vs FTCS bound at the top cell.
    # This is THE right physical scaling for the question we are asking.
    dt_crit_top = 0.5 * dz_top_grid ** 2 / kappa_top
    dt_ratio = dt_coarse / dt_crit_top

    return {
        "mu_eff": mu_eff,
        "lam_eff": lam_eff,
        "C_eff": C_eff,
        "kappa_top": kappa_top,
        "lam_top": lam1,
        "C_top": C1,
        "max_contrast": max_contrast,
        "contrast_12": contrast_12,
        "contrast_23": contrast_23,
        "n_interfaces": n_interfaces,
        "first_iface_depth": first_iface_depth,
        "h_top": h1,
        "h_mid": dh2,
        "dt_ratio": dt_ratio,
    }


# ---------------------------------------------------------------------------
# 5. Run the experiment matrix
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("SHAP attribution analysis for the BTCS coarse-Δt error")
    print("=" * 70)

    N = 150
    dt_ref = 15.0       # FTCS reference (small-Δt, all schemes agree)
    dt_coarse = 600.0   # coarse-Δt regime
    rows = []

    print(f"\nSampling N = {N} synthetic substrate columns from the prior...")
    print(f"  reference: FTCS at dt = {dt_ref:.0f} s")
    print(f"  test     : BTCS at dt = {dt_coarse:.0f} s")
    print()

    n_blew_up = 0
    n_ok = 0
    for i in range(N):
        layers = sample_substrate(rng)
        descriptors = compute_descriptors(layers)

        # FTCS reference at small dt — for reference we use BTCS at dt=15 s
        # since FTCS may blow up on stiff layers even at 15 s.
        ref = run_column(layers, alpha=1.0, dt=dt_ref, n_days=2)
        if ref["blew_up"]:
            n_blew_up += 1
            continue

        # BTCS at coarse dt
        coarse = run_column(layers, alpha=1.0, dt=dt_coarse, n_days=2)
        if coarse["blew_up"]:
            n_blew_up += 1
            continue

        # Day-2 RMSE in surface temperature
        # interpolate coarse onto reference grid
        mask_ref = ref["times"] >= 86400.0
        t_ref = ref["times"][mask_ref]
        Ts_ref = ref["Ts0"][mask_ref]
        mask_c = coarse["times"] >= 86400.0
        t_c = coarse["times"][mask_c]
        Ts_c = coarse["Ts0"][mask_c]
        Ts_c_on_ref = np.interp(t_ref, t_c, Ts_c)
        rmse_Ts = float(np.sqrt(np.mean((Ts_c_on_ref - Ts_ref) ** 2)))

        # Day-2 amplitude ratio in G
        G_ref = ref["G"][mask_ref]
        G_c = coarse["G"][mask_c]
        AG_ref = 0.5 * (np.max(G_ref) - np.min(G_ref))
        AG_c = 0.5 * (np.max(G_c) - np.min(G_c))
        amp_ratio = AG_c / AG_ref if AG_ref > 0 else np.nan

        row = dict(descriptors)
        row.update({
            "rmse_Ts": rmse_Ts,
            "amp_ratio": amp_ratio,
            "i": i,
        })
        rows.append(row)
        n_ok += 1
        if (i + 1) % 25 == 0:
            print(f"  [{i+1:3d}/{N}] OK={n_ok} blew_up={n_blew_up} "
                  f"latest RMSE_Ts={rmse_Ts:.3f} K  amp_ratio={amp_ratio:.3f}")

    print(f"\nFinal: {n_ok} valid columns, {n_blew_up} blew up.")
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(TABLES, "synthetic_dataset.csv"), index=False)
    print(f"Saved {os.path.join(TABLES, 'synthetic_dataset.csv')}")
    print()
    print("Dataset summary statistics:")
    print(df[['mu_eff', 'kappa_top', 'max_contrast', 'n_interfaces',
              'first_iface_depth', 'rmse_Ts', 'amp_ratio']].describe().round(3))

    # ---------------------------------------------------------------------
    # 6. Fit gradient-boosted regression and run SHAP
    # ---------------------------------------------------------------------
    feature_cols = [
        "kappa_top",
        "mu_eff",
        "max_contrast",
        "n_interfaces",
        "first_iface_depth",
        "h_top",
    ]
    X = df[feature_cols].values
    y = df["rmse_Ts"].values

    print(f"\nFitting GradientBoostingRegressor on N = {len(df)} samples...")
    model = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=3,
        learning_rate=0.05,
        random_state=SEED,
    )
    model.fit(X, y)
    train_score = model.score(X, y)
    print(f"  in-sample R^2 = {train_score:.4f}")

    from sklearn.model_selection import cross_val_score
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    print(f"  5-fold CV R^2 = {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    print("\nRunning SHAP TreeExplainer...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    importance_df = pd.DataFrame({
        "feature": feature_cols,
        "mean_abs_shap": mean_abs_shap,
        "rank": (-mean_abs_shap).argsort().argsort() + 1,
    }).sort_values("mean_abs_shap", ascending=False)
    importance_df.to_csv(os.path.join(TABLES, "shap_summary.csv"), index=False)
    print(f"\nSHAP feature importance (mean |SHAP| over the {len(df)} samples):")
    print(importance_df.to_string(index=False))

    # ---------------------------------------------------------------------
    # 6b. Conditional analysis: residual after κ_top is regressed out
    # ---------------------------------------------------------------------
    # Fit a 1D regression of rmse_Ts on log(kappa_top) (the dominant
    # feature). Take the residual. Then fit a second regression of the
    # residual on the OTHER features to see what remains.
    print("\nConditional analysis: residual after κ_top is partialled out")
    log_kappa = np.log(df["kappa_top"].values).reshape(-1, 1)
    base_model = GradientBoostingRegressor(
        n_estimators=100, max_depth=3, learning_rate=0.05, random_state=SEED,
    )
    base_model.fit(log_kappa, y)
    y_kappa = base_model.predict(log_kappa)
    residual = y - y_kappa

    other_feats = [f for f in feature_cols if f != "kappa_top"]
    X_other = df[other_feats].values
    resid_model = GradientBoostingRegressor(
        n_estimators=100, max_depth=3, learning_rate=0.05, random_state=SEED,
    )
    resid_model.fit(X_other, residual)
    resid_R2 = resid_model.score(X_other, residual)
    print(f"  Variance in y explained by κ_top alone: "
          f"R^2 = {base_model.score(log_kappa, y):.3f}")
    print(f"  Residual variance explained by other features: "
          f"R^2 = {resid_R2:.3f}")

    resid_explainer = shap.TreeExplainer(resid_model)
    resid_shap = resid_explainer.shap_values(X_other)
    resid_imp = pd.DataFrame({
        "feature": other_feats,
        "mean_abs_shap_residual": np.abs(resid_shap).mean(axis=0),
    }).sort_values("mean_abs_shap_residual", ascending=False)
    print(f"\nFeature importance for the κ_top-residual:")
    print(resid_imp.to_string(index=False))

    # ---------------------------------------------------------------------
    # 7. Plot Figure 6 — four-panel layout
    # ---------------------------------------------------------------------
    fig = plt.figure(figsize=(13, 9))

    feat_pretty = {
        "mu_eff":           r"$\mu_{\rm eff}$ (admittance)",
        "kappa_top":        r"$\kappa_{\rm top}$",
        "max_contrast":     r"max $\lambda$ contrast",
        "n_interfaces":     "# interfaces",
        "first_iface_depth": "1st interface depth",
        "h_top":            r"$h_{\rm top}$",
    }

    # Panel (a): full-feature SHAP importance
    ax1 = fig.add_subplot(2, 2, 1)
    sorted_feats = importance_df["feature"].values
    sorted_imps = importance_df["mean_abs_shap"].values
    colors = []
    for f in sorted_feats:
        if f == "kappa_top":
            colors.append("#D14545")  # dominant
        elif f == "mu_eff":
            colors.append("#5B8BD8")  # admittance
        elif f in ("max_contrast", "n_interfaces", "first_iface_depth"):
            colors.append("#F08A24")  # interface-related
        else:
            colors.append("#999999")
    ax1.barh([feat_pretty[f] for f in sorted_feats][::-1],
             sorted_imps[::-1], color=colors[::-1], edgecolor='white')
    ax1.set_xlabel(r"Mean $|{\rm SHAP}|$ for ${\rm RMSE}_{T_s}$ (K)")
    ax1.set_title(r"(a) Full-feature SHAP importance")
    ax1.grid(True, alpha=0.3, axis='x')

    # Panel (b): SHAP dependence on κ_top
    top_feature = importance_df.iloc[0]["feature"]
    top_idx = feature_cols.index(top_feature)
    ax2 = fig.add_subplot(2, 2, 2)
    sc = ax2.scatter(df[top_feature], shap_values[:, top_idx],
                     c=df["mu_eff"], cmap="viridis", s=24, alpha=0.8,
                     edgecolor='white', linewidth=0.3)
    ax2.set_xlabel(feat_pretty[top_feature] + r" (m$^2$ s$^{-1}$)")
    ax2.set_ylabel(f"SHAP value for {feat_pretty[top_feature]} (K)")
    ax2.set_title(f"(b) SHAP dependence on {feat_pretty[top_feature]}")
    ax2.set_xscale('log')
    ax2.axhline(0, color='black', linewidth=0.5, alpha=0.5)
    ax2.grid(True, alpha=0.3)
    cbar = plt.colorbar(sc, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label(r"$\mu_{\rm eff}$ (J m$^{-2}$ K$^{-1}$ s$^{-1/2}$)")

    # Panel (c): residual SHAP importance after κ_top partialled out
    ax3 = fig.add_subplot(2, 2, 3)
    sorted_resid = resid_imp.values
    feats_r = resid_imp["feature"].values
    imps_r = resid_imp["mean_abs_shap_residual"].values
    colors_r = []
    for f in feats_r:
        if f == "mu_eff":
            colors_r.append("#5B8BD8")
        elif f in ("max_contrast", "n_interfaces", "first_iface_depth"):
            colors_r.append("#F08A24")
        else:
            colors_r.append("#999999")
    ax3.barh([feat_pretty[f] for f in feats_r][::-1],
             imps_r[::-1], color=colors_r[::-1], edgecolor='white')
    ax3.set_xlabel(r"Mean $|{\rm SHAP}|$ on residual (K)")
    ax3.set_title(r"(c) SHAP importance on the $\kappa_{\rm top}$-residual"
                  f"\n(residual $R^2$ = {resid_R2:.2f})")
    ax3.grid(True, alpha=0.3, axis='x')

    # Panel (d): predicted vs observed RMSE_Ts
    y_pred = model.predict(X)
    ax4 = fig.add_subplot(2, 2, 4)
    sc4 = ax4.scatter(y, y_pred, c=df["max_contrast"], cmap="plasma",
                      s=24, alpha=0.8, edgecolor='white', linewidth=0.3,
                      norm=plt.matplotlib.colors.LogNorm())
    lim = [0, max(y.max(), y_pred.max()) * 1.05]
    ax4.plot(lim, lim, 'k--', linewidth=1.0, alpha=0.6, label='1:1')
    ax4.set_xlim(lim); ax4.set_ylim(lim)
    ax4.set_xlabel(r"Observed ${\rm RMSE}_{T_s}$ (K)")
    ax4.set_ylabel(r"Predicted ${\rm RMSE}_{T_s}$ (K)")
    ax4.set_title(f"(d) Model fit\n(in-sample $R^2$ = {train_score:.3f}, "
                  f"5-fold CV $R^2$ = {cv_scores.mean():.2f})")
    cbar2 = plt.colorbar(sc4, ax=ax4, fraction=0.046, pad=0.04)
    cbar2.set_label(r"max $\lambda$ contrast")
    ax4.legend(loc='upper left', frameon=False)
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    out_path = os.path.join(OUT, "fig6_shap_attribution.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=200)
    plt.close()
    print(f"\nSaved {out_path}")

    # Save the residual SHAP table too
    resid_imp.to_csv(os.path.join(TABLES, "shap_residual_summary.csv"), index=False)

    # Summary printout for the report
    print()
    print("=" * 70)
    print("Summary for §6 of the report:")
    print("=" * 70)
    print(f"  N = {len(df)} synthetic 3-layer substrate columns")
    print(f"  GradientBoostingRegressor: in-sample R^2 = {train_score:.3f}, "
          f"5-fold CV R^2 = {cv_scores.mean():.3f}")
    print(f"  Top 3 features by mean |SHAP|:")
    for k in range(min(3, len(importance_df))):
        row = importance_df.iloc[k]
        print(f"    {k+1}. {row['feature']:25s} mean|SHAP| = {row['mean_abs_shap']:.4f} K")

    return df, importance_df, model


if __name__ == "__main__":
    df, imp, model = main()
