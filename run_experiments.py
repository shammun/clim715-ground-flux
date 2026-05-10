"""
CLIM-715 Course Project (revised)

Numerical Damping of the Diurnal Ground Heat Flux over Urban Substrates:
An Explicit, Implicit, and Crank-Nicolson Comparison

This script reproduces all four (five) figures in the report. It is organized as:
  1. Solver: FTCS / BTCS / CN on a non-uniform vertical grid with depth-varying
     thermal conductivity lambda_s(z) and volumetric heat capacity C_s(z).
  2. von Neumann amplification factors (analytical).
  3. Test 1: diurnal damping-depth verification on a uniform sandy-loam column.
  4. Test 2: prognostic surface energy balance with Newton iteration, on three
     urban substrate columns (asphalt road / concrete roof / bare soil),
     three schemes, and three time steps. 27 runs total.
  5. Figures 1-5 saved to ./figs/.
  6. Summary tables saved to ./tables/.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded


# ---------------------------------------------------------------------------
# 0. setup
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

C_FTCS = "#7B61FF"
C_BTCS = "#00B8A9"
C_CN   = "#F08A24"
C_REF  = "#666666"
C_ANA  = "#000000"


# ---------------------------------------------------------------------------
# 1. solver on a non-uniform grid with depth-varying lambda_s, C_s
# ---------------------------------------------------------------------------
#
#   C_s(z) dT/dt = d/dz ( lambda_s(z) dT/dz )
#
# Grid: T at integer levels z_j (j = 0..N-1, z_0 = 0 surface, z increasing
# downward). Conductivity and conductive flux at half-levels z_{j+1/2}.
#
# Discrete flux divergence:
#   dT_j/dt = (1/(C_j dz_j)) * (G_{j+1/2} - G_{j-1/2})
# where
#   G_{j+1/2} = lambda_{j+1/2} * (T_{j+1} - T_j) / (z_{j+1} - z_j)
# and dz_j is the THICKNESS of cell j, defined as (z_{j+1/2,top} - z_{j+1/2,bot}).
#
# For a control-volume staggered layout, dz_j = (z_{j+1} - z_{j-1}) / 2 for
# interior j, with the surface and bottom cells using half-cells. We use the
# simpler interpretation z_j marks the cell centre, dz_j is the cell thickness.
#
# alpha-weighted theta-method:
#   alpha = 0  -> FTCS (forward Euler in time)
#   alpha = 1  -> BTCS
#   alpha = 1/2 -> Crank-Nicolson
#
# At each grid point (interior):
#   C_j (T_j^{n+1} - T_j^n)/dt = alpha * L(T^{n+1})_j + (1-alpha) * L(T^n)_j
# where L(T)_j = (1/dz_j) * [lambda_{j+1/2} (T_{j+1}-T_j)/dzc_{j+1/2}
#                          - lambda_{j-1/2} (T_j-T_{j-1})/dzc_{j-1/2}]
# dzc_{j+1/2} = z_{j+1} - z_j (centre-to-centre spacing).
#
# Boundary conditions:
#   - Upper (j=0): Dirichlet T_s^0 prescribed (set externally by SEB or
#     analytical forcing)
#   - Lower (j=N-1): Neumann (zero flux), enforced by setting the
#     j=N-1 row to T_{N-1} = T_{N-2}, or equivalently by setting
#     lambda_{N-1/2} -> 0 in the divergence stencil.

def make_grid(z_top=2.0, n_levels=20, stretch=1.25, dz1=0.01):
    """Stretched grid downward from the surface.

    Cell centres at z_j with thicknesses dz_j satisfying
        dz_j = dz1 * stretch**j
    and z_j = sum of half-thicknesses below the surface.
    Adjusts the deepest cell so the column reaches exactly z_top.
    """
    dzs = dz1 * stretch ** np.arange(n_levels)
    if np.sum(dzs) > z_top:
        # if the geometric sequence overshoots, truncate
        cumulative = np.cumsum(dzs)
        n_levels = int(np.searchsorted(cumulative, z_top)) + 1
        dzs = dzs[:n_levels]
    # rescale the last layer so total = z_top
    dzs[-1] = z_top - np.sum(dzs[:-1])
    # cell-centre depths
    z = np.zeros(n_levels)
    z[0] = dzs[0] / 2.0
    for j in range(1, n_levels):
        z[j] = z[j - 1] + (dzs[j - 1] + dzs[j]) / 2.0
    # centre-to-centre spacings (length n_levels - 1) at half-levels
    dzc = np.diff(z)
    return z, dzs, dzc


def make_uniform_grid(z_top=2.0, dz=0.01):
    """Uniform grid for the verification test."""
    n_levels = int(round(z_top / dz)) + 1
    z = np.arange(n_levels) * dz
    dzs = np.full(n_levels, dz)
    dzs[0] = dz / 2.0    # half-cell at surface
    dzs[-1] = dz / 2.0   # half-cell at bottom
    dzc = np.full(n_levels - 1, dz)
    return z, dzs, dzc


def assign_layered_props(z, layers):
    """Given a list of (z_bottom, lambda, C) tuples, assign at cell centres
    and half-levels.

    layers is a list ordered from surface downward, each entry
    (z_bottom, lambda_s [W/m/K], C_s [J/m^3/K]) describing a layer that
    extends from the bottom of the previous layer to z_bottom.
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
    # half-level conductivities use harmonic mean across layer interfaces
    # (preserves heat flux exactly when crossing an interface)
    lam_half = 2.0 / (1.0 / lam[:-1] + 1.0 / lam[1:])
    return lam, C, lam_half


def step_alpha(T, dt, dzs, dzc, lam_half, C, alpha,
               T_top=None, lower_bc="neumann"):
    """Advance T by dt using the alpha-weighted scheme.

    alpha = 0  : FTCS (explicit)
    alpha = 1  : BTCS
    alpha = 0.5: Crank-Nicolson

    Top BC: Dirichlet, T[0] = T_top.
    Bottom BC: Neumann zero-flux (default), or 'dirichlet' to hold T[-1].

    Equation per cell j (interior):
        C_j (T_j^{n+1} - T_j^n)/dt
         = alpha [lam_h[j]  (T_{j+1}^{n+1} - T_j^{n+1})/dzc[j]
                 -lam_h[j-1] (T_j^{n+1} - T_{j-1}^{n+1})/dzc[j-1]] / dz_j
         + (1-alpha) [same with n].
    """
    N = len(T)

    # for the FTCS branch, no linear solve needed
    if alpha == 0.0:
        T_new = T.copy()
        for j in range(1, N - 1):
            flux_up = lam_half[j] * (T[j + 1] - T[j]) / dzc[j]
            flux_dn = lam_half[j - 1] * (T[j] - T[j - 1]) / dzc[j - 1]
            T_new[j] = T[j] + (dt / (C[j] * dzs[j])) * (flux_up - flux_dn)
        # boundaries
        if T_top is not None:
            T_new[0] = T_top
        else:
            T_new[0] = T[0]
        if lower_bc == "neumann":
            T_new[-1] = T_new[-2]
        else:
            T_new[-1] = T[-1]
        return T_new

    # build banded system  A T^{n+1} = b  for alpha > 0
    diag_main = np.ones(N)
    diag_upper = np.zeros(N)
    diag_lower = np.zeros(N)
    rhs = T.copy()

    for j in range(1, N - 1):
        a = dt * lam_half[j - 1] / (C[j] * dzs[j] * dzc[j - 1])
        b = dt * lam_half[j] / (C[j] * dzs[j] * dzc[j])
        diag_lower[j - 1] = -alpha * a
        diag_main[j] = 1.0 + alpha * (a + b)
        diag_upper[j + 1] = -alpha * b
        rhs[j] = (T[j]
                  + (1 - alpha) * a * (T[j - 1] - T[j])
                  + (1 - alpha) * b * (T[j + 1] - T[j]))

    # boundary rows
    # top: Dirichlet
    if T_top is None:
        T_top = T[0]
    diag_main[0] = 1.0
    diag_upper[1] = 0.0
    rhs[0] = T_top

    # bottom: zero-flux Neumann -> T[N-1] = T[N-2]
    if lower_bc == "neumann":
        diag_main[N - 1] = 1.0
        diag_lower[N - 2] = -1.0
        rhs[N - 1] = 0.0
    else:
        diag_main[N - 1] = 1.0
        diag_lower[N - 2] = 0.0
        rhs[N - 1] = T[N - 1]

    ab = np.zeros((3, N))
    ab[0, :] = diag_upper
    ab[1, :] = diag_main
    ab[2, :] = diag_lower
    return solve_banded((1, 1), ab, rhs)


# ---------------------------------------------------------------------------
# 2. von Neumann amplification factors
# ---------------------------------------------------------------------------

def amp_ftcs(nu, kdz):
    return 1.0 - 2.0 * nu * (1.0 - np.cos(kdz))

def amp_btcs(nu, kdz):
    return 1.0 / (1.0 + 2.0 * nu * (1.0 - np.cos(kdz)))

def amp_cn(nu, kdz):
    h = nu * (1.0 - np.cos(kdz))
    return (1.0 - h) / (1.0 + h)


# ---------------------------------------------------------------------------
# Figure 1: amplification factor curves
# ---------------------------------------------------------------------------

def figure_1():
    kdz = np.linspace(0, np.pi, 200)
    nu_values = [0.25, 0.5, 1.0, 5.0]
    nu_colors = ["#5B8BD8", "#F08A24", "#7B61FF", "#D14545"]

    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6))
    titles = ["FTCS (explicit)", "BTCS (fully implicit)", "Crank-Nicolson"]
    funcs = [amp_ftcs, amp_btcs, amp_cn]
    ylims = [(0, 4.0), (0, 1.1), (0, 1.1)]

    for ax, title, fn, ylim in zip(axes, titles, funcs, ylims):
        for nu, col in zip(nu_values, nu_colors):
            ax.plot(kdz, np.abs(fn(nu, kdz)), label=fr"$\nu={nu}$",
                    linewidth=1.7, color=col)
        ax.axhline(1.0, color="black", linestyle="--", linewidth=0.9, alpha=0.7)
        ax.set_xlabel(r"$k\,\Delta z$")
        ax.set_ylabel(r"$|A_k|$")
        ax.set_title(title)
        ax.set_xlim(0, np.pi)
        ax.set_xticks([0, np.pi / 2, np.pi])
        ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$"])
        ax.set_ylim(*ylim)
        ax.legend(loc="best", frameon=False)
        ax.grid(True, alpha=0.3)

    axes[0].annotate(r"$\nu=5$ off-scale (max $\approx 19$)",
                     xy=(np.pi*0.95, 3.6),
                     xytext=(np.pi*0.4, 3.6), ha="left", fontsize=8,
                     color="#D14545",
                     arrowprops=dict(arrowstyle="->", color="#D14545", lw=0.8))

    plt.tight_layout()
    out = os.path.join(OUT, "fig1_amplification.png")
    plt.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {out}")

    # numerical table
    rows = []
    for nu in [0.25, 0.5, 1.0, 5.0, 50.0]:
        rows.append((nu, amp_ftcs(nu, np.pi), amp_btcs(nu, np.pi), amp_cn(nu, np.pi)))
    return rows


# ---------------------------------------------------------------------------
# 3. Test 1 - diurnal damping-depth verification
# ---------------------------------------------------------------------------
#
# Single uniform sandy-loam column of depth z_top = 2 m. Sinusoidal Dirichlet
# at the surface:
#   T_s(0, t) = T0 + A * cos(omega t)
# zero-flux Neumann at z = z_top.
# Analytical solution in the semi-infinite limit:
#   T_s(z, t) = T0 + A * exp(-z/d) * cos(omega t - z/d)
# where d = sqrt(2 * kappa_s / omega).
#
# We use kappa_s = lambda_s / C_s = 0.30 / (1.3e6) = 2.31e-7 m^2/s, giving
# d = 7.97 cm.
#
# Run: spin up to diurnal equilibrium, then compare profiles and surface flux
# G(t) at t = 12, 18 h (peak and post-peak) and the L2 error over the column.

def run_test_1():
    print("\n=== Test 1: diurnal damping-depth verification ===")

    # uniform sandy loam
    lam_s = 0.30          # W/m/K
    C_s = 1.3e6           # J/m^3/K
    kappa = lam_s / C_s   # m^2/s, ~ 2.31e-7

    omega = 2.0 * np.pi / 86400.0  # rad/s
    d = np.sqrt(2.0 * kappa / omega)  # damping depth
    print(f"  damping depth d = {d*100:.2f} cm")

    # surface forcing
    T0 = 290.0   # K
    A_amp = 10.0  # K (large for a clean signal)

    # uniform grid
    dz = 0.01  # 1 cm
    z, dzs, dzc = make_uniform_grid(z_top=2.0, dz=dz)
    N = len(z)
    print(f"  grid: N = {N}, dz = {dz*100:.1f} cm")

    # FTCS critical dt = (1/2) dz^2 / kappa
    dt_crit = 0.5 * dz**2 / kappa
    print(f"  FTCS critical dt = {dt_crit:.1f} s")

    # piecewise-constant arrays
    lam_arr = np.full(N, lam_s)
    C_arr = np.full(N, C_s)
    lam_half = np.full(N - 1, lam_s)

    def analytical(z_arr, t):
        return T0 + A_amp * np.exp(-z_arr / d) * np.cos(omega * t - z_arr / d)

    def G_analytical(t):
        # surface ground heat flux from analytical solution:
        #   G = -lambda * dT/dz|_{z=0}
        #   T(z,t) = T0 + A exp(-z/d) cos(omega t - z/d)
        #   dT/dz|_{z=0} = (A/d) [ -cos(omega t) + sin(omega t) ]
        #   G = lambda * (A/d) * [cos(omega t) - sin(omega t)]
        #     = lambda * (A/d) * sqrt(2) * cos(omega t + pi/4)
        # G leads surface T by pi/4 in time (peaks 3 hours before surface T).
        # +ve G = downward flux into ground.
        return lam_s * (A_amp / d) * np.sqrt(2.0) * np.cos(omega * t + np.pi / 4.0)

    # configurations: scheme, dt
    configs = [
        ("FTCS (nu=0.4)", 0,    0.4 * dt_crit / 0.5),
        ("FTCS (nu=0.6, unstable)", 0, 0.6 * dt_crit / 0.5),
        ("BTCS dt=300s", 1,    300.0),
        ("CN   dt=300s", 0.5,  300.0),
        ("BTCS dt=900s", 1,    900.0),
        ("CN   dt=900s", 0.5,  900.0),
    ]

    # run each config for 5 days (4 days spin-up + 1 day diagnostic)
    n_days = 5
    t_end = n_days * 86400.0
    results = []

    for name, alpha, dt in configs:
        n_steps = int(round(t_end / dt))
        dt = t_end / n_steps
        nu_actual = (lam_s / C_s) * dt / dz**2
        print(f"  running {name:30s}  dt = {dt:7.1f} s  nu = {nu_actual:6.2f}  steps = {n_steps:6d}")

        T = np.full(N, T0)  # cold start
        # storage
        save_every = max(1, n_steps // (24 * n_days))
        ts = [0.0]
        Ts_surface = [T[0]]
        T_at_10cm = [T[10]]   # z = 10 cm (index 10 since dz = 1 cm and z[0]=0)
        T_at_5cm  = [T[5]]    # z = 5 cm
        G_surface = [0.0]
        profiles_day_5 = []
        times_day_5 = []

        blew_up = False
        for n in range(1, n_steps + 1):
            t_now = n * dt
            T_top = T0 + A_amp * np.cos(omega * t_now)
            T = step_alpha(T, dt, dzs, dzc, lam_half, C_arr, alpha,
                           T_top=T_top, lower_bc="neumann")
            if not np.all(np.isfinite(T)) or np.max(np.abs(T - T0)) > 1e6:
                blew_up = True
                print(f"    BLEW UP at step {n}, t = {t_now:.1f} s")
                break
            G_surf = -lam_half[0] * (T[1] - T[0]) / dzc[0]
            if n % save_every == 0:
                ts.append(t_now)
                Ts_surface.append(T[0])
                T_at_10cm.append(T[10])
                T_at_5cm.append(T[5])
                G_surface.append(G_surf)
            # store full profiles every ~hour during day 5
            if t_now >= 4 * 86400 and (n % max(1, int(round(3600 / dt))) == 0):
                profiles_day_5.append(T.copy())
                times_day_5.append(t_now)

        results.append({
            "name": name, "alpha": alpha, "dt": dt, "nu": nu_actual,
            "ts": np.array(ts), "Ts_surface": np.array(Ts_surface),
            "T_at_5cm": np.array(T_at_5cm),
            "T_at_10cm": np.array(T_at_10cm),
            "G_surface": np.array(G_surface),
            "profiles_day_5": profiles_day_5,
            "times_day_5": times_day_5,
            "blew_up": blew_up,
            "T_final": T,
        })

    return results, dict(z=z, dz=dz, lam_s=lam_s, C_s=C_s, omega=omega, d=d,
                        T0=T0, A_amp=A_amp, analytical=analytical,
                        G_analytical=G_analytical, dt_crit=dt_crit)


def figure_2(test1_results, test1_meta):
    """Three-panel: (a) profiles at noon on day 5 vs analytical
                    (b) surface T over day 5 vs analytical
                    (c) surface G over day 5 vs analytical.
    """
    z = test1_meta["z"]
    analytical = test1_meta["analytical"]
    G_analytical = test1_meta["G_analytical"]
    omega = test1_meta["omega"]
    T0 = test1_meta["T0"]

    # we want one analytical reference and traces for stable runs only
    # FTCS unstable case shown separately
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.0))

    # day 5: t in [4*86400, 5*86400]
    t_day5_start = 4 * 86400.0
    t_day5_end = 5 * 86400.0

    # ----- panel a: profile at "noon" of day 5
    # solar noon is when surface forcing is maximum: cos(omega t) = 1 -> omega t = 0, 2pi, ...
    # so t = 4*86400 (start of day 5) is 'noon' here
    t_noon = 4 * 86400.0  # this corresponds to cos = 1 -> max surface T
    z_arr = np.linspace(0, 1.0, 500)  # plot only top 1 m
    ax = axes[0]
    ax.plot(analytical(z_arr, t_noon), z_arr * 100, color=C_ANA,
            linewidth=2.0, label="Analytical")
    for r in test1_results:
        if r["blew_up"]:
            continue
        # find profile closest to t_noon
        if not r["profiles_day_5"]:
            continue
        idx = int(np.argmin(np.abs(np.array(r["times_day_5"]) - t_noon)))
        prof = r["profiles_day_5"][idx]
        if r["alpha"] == 0:
            col, ls = C_FTCS, "-"
        elif r["alpha"] == 1:
            col, ls = C_BTCS, "-"
        else:
            col, ls = C_CN, "-"
        # only plot the dt=900 cases for clarity
        if "900s" in r["name"] or "0.4" in r["name"]:
            ax.plot(prof, z * 100, color=col, linewidth=1.4,
                    linestyle=ls, label=r["name"], alpha=0.85)
    ax.invert_yaxis()
    ax.set_xlabel(r"$T_s$ (K)")
    ax.set_ylabel("Depth (cm)")
    ax.set_title("(a) Profile at $t$ = 24 h (peak surface forcing)")
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(100, 0)

    # ----- panel b: surface T over day 5
    ax = axes[1]
    t_anal = np.linspace(t_day5_start, t_day5_end, 500)
    ax.plot((t_anal - t_day5_start) / 3600.0,
            analytical(0.0, t_anal), color=C_ANA,
            linewidth=2.0, label="Analytical")
    for r in test1_results:
        if r["blew_up"]:
            continue
        mask = (r["ts"] >= t_day5_start) & (r["ts"] <= t_day5_end)
        if r["alpha"] == 0:
            col = C_FTCS
        elif r["alpha"] == 1:
            col = C_BTCS
        else:
            col = C_CN
        if "900s" in r["name"] or "0.4" in r["name"]:
            ax.plot((r["ts"][mask] - t_day5_start) / 3600.0,
                    r["Ts_surface"][mask], color=col,
                    linewidth=1.4, label=r["name"], alpha=0.85)
    ax.set_xlabel("Hours into day 5")
    ax.set_ylabel(r"$T_s(0, t)$ (K)")
    ax.set_title(r"(b) Surface temperature, day 5")
    ax.legend(loc="upper right", frameon=False, fontsize=8)
    ax.grid(True, alpha=0.3)

    # ----- panel c: surface G over day 5
    ax = axes[2]
    ax.plot((t_anal - t_day5_start) / 3600.0,
            G_analytical(t_anal), color=C_ANA,
            linewidth=2.0, label="Analytical")
    for r in test1_results:
        if r["blew_up"]:
            continue
        mask = (r["ts"] >= t_day5_start) & (r["ts"] <= t_day5_end)
        if r["alpha"] == 0:
            col = C_FTCS
        elif r["alpha"] == 1:
            col = C_BTCS
        else:
            col = C_CN
        if "900s" in r["name"] or "0.4" in r["name"]:
            ax.plot((r["ts"][mask] - t_day5_start) / 3600.0,
                    r["G_surface"][mask], color=col,
                    linewidth=1.4, label=r["name"], alpha=0.85)
    ax.set_xlabel("Hours into day 5")
    ax.set_ylabel(r"$G$ at $z = 0$ (W/m$^2$)")
    ax.set_title(r"(c) Surface ground heat flux, day 5")
    ax.legend(loc="upper right", frameon=False, fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    out = os.path.join(OUT, "fig2_damping_depth.png")
    plt.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {out}")


# ---------------------------------------------------------------------------
# 4. Test 2 - prognostic SEB on three urban substrates
# ---------------------------------------------------------------------------

# substrate definitions: list of (z_bottom, lambda [W/m/K], C [J/m^3/K])
SUBSTRATES = {
    "asphalt_road": [
        (0.05, 0.75,  2.0e6),   # asphalt
        (0.25, 1.40,  2.4e6),   # aggregate
        (1.00, 0.30,  1.3e6),   # dry soil
        (2.00, 0.50,  1.8e6),   # subsoil
    ],
    "concrete_roof": [
        (0.10, 1.50,  2.1e6),   # concrete deck
        (0.20, 0.04,  0.08e6),  # rigid insulation (low lambda, low C)
        (2.00, 0.15,  1.5e6),   # interior structure (drywall/wood/etc.)
    ],
    "bare_soil": [
        (2.00, 0.30,  1.3e6),   # uniform sandy loam
    ],
}

SUBSTRATE_NAMES = {
    "asphalt_road":  "Asphalt road",
    "concrete_roof": "Concrete roof",
    "bare_soil":     "Bare soil",
}

# physical / forcing constants
SIGMA_SB = 5.670374419e-8   # Stefan-Boltzmann
ALBEDO   = {"asphalt_road": 0.10, "concrete_roof": 0.30, "bare_soil": 0.20}
EMIS     = {"asphalt_road": 0.95, "concrete_roof": 0.92, "bare_soil": 0.95}

# atmospheric forcing (synthetic, idealised)
def S_down(t):
    """Incoming shortwave (W/m^2). Sinusoidal 0..1000 with positive part only."""
    omega = 2.0 * np.pi / 86400.0
    # peak at solar noon = 12 h after midnight
    val = 1000.0 * np.cos(omega * (t - 12 * 3600.0))
    return np.maximum(val, 0.0)

def L_down_func(t):
    """Incoming longwave (W/m^2). Slow diurnal variation around 350."""
    omega = 2.0 * np.pi / 86400.0
    return 350.0 + 20.0 * np.cos(omega * (t - 14 * 3600.0))

def T_air(t):
    """2-m air temperature (K). Diurnal range 285-300, peak at 14:00 LT."""
    omega = 2.0 * np.pi / 86400.0
    return 292.5 + 7.5 * np.cos(omega * (t - 14 * 3600.0))

def U_wind(_t):
    """Constant moderate wind."""
    return 3.0  # m/s

# bulk-aerodynamic resistance: r_a = 1/(C_H U)   with C_H = 5e-3 typical
C_H = 5.0e-3
RHO_AIR = 1.2
CP_AIR = 1005.0


def seb_residual(Ts0, T_int, dzc0, lam_h0, t, surface_key):
    """SEB residual at the surface. Positive = excess at surface (too warm).

    R_n - H - LE - G = 0
    """
    albedo = ALBEDO[surface_key]
    emis = EMIS[surface_key]
    Sd = S_down(t)
    Ld = L_down_func(t)
    Ta = T_air(t)
    U = U_wind(t)
    r_a = 1.0 / (C_H * U)

    R_n = (1.0 - albedo) * Sd + emis * Ld - emis * SIGMA_SB * Ts0**4
    H = RHO_AIR * CP_AIR * (Ts0 - Ta) / r_a
    LE = 0.0  # strict impervious
    G = lam_h0 * (Ts0 - T_int) / dzc0   # +ve = downward (into ground)
    return R_n - H - LE - G


def seb_dresidual_dT(Ts0, dzc0, lam_h0, surface_key):
    emis = EMIS[surface_key]
    dRn = -4.0 * emis * SIGMA_SB * Ts0**3
    U = U_wind(0.0)
    r_a = 1.0 / (C_H * U)
    dH = RHO_AIR * CP_AIR / r_a
    dG = lam_h0 / dzc0
    return dRn - dH - dG


def solve_surface_energy_balance(T_int, dzc0, lam_h0, t, surface_key,
                                  Ts0_init, tol=1e-4, max_iter=20):
    """Newton iteration for T_s^0 satisfying SEB."""
    Ts0 = Ts0_init
    for _ in range(max_iter):
        f = seb_residual(Ts0, T_int, dzc0, lam_h0, t, surface_key)
        df = seb_dresidual_dT(Ts0, dzc0, lam_h0, surface_key)
        dTs = -f / df
        Ts0 += dTs
        if abs(dTs) < tol:
            return Ts0, True
    return Ts0, False


# ---------------------------------------------------------------------------
# Option B: analytical damping-depth initialization
# ---------------------------------------------------------------------------

def initial_profile(z, T0, A_amp, omega, kappa_eff, t0=0.0):
    """Damping-depth quasi-equilibrium profile for cold-start avoidance.

    Uses an effective kappa_eff = lambda_s_top / C_s_top as an approximation;
    rough but standard for spin-up reduction.
    """
    d = np.sqrt(2.0 * kappa_eff / omega)
    return T0 + A_amp * np.exp(-z / d) * np.cos(omega * t0 - z / d)


# ---------------------------------------------------------------------------
# Run a single column for 24 h
# ---------------------------------------------------------------------------

def run_seb_column(surface_key, alpha, dt, n_days=2, store_every=1):
    """Integrate one substrate column for n_days under synthetic diurnal
    forcing. Returns dict of stored time series and final state.

    Initialization: damping-depth profile at t = midnight using effective
    kappa from the topmost layer.
    """
    layers = SUBSTRATES[surface_key]
    # build grid -- stretched for asphalt and roof, finer for layered cases
    z_top = 2.0
    if surface_key == "concrete_roof":
        # the layered structure needs fine resolution near the top
        z, dzs, dzc = make_grid(z_top=z_top, n_levels=30, stretch=1.18,
                                 dz1=0.005)
    elif surface_key == "asphalt_road":
        z, dzs, dzc = make_grid(z_top=z_top, n_levels=28, stretch=1.20,
                                 dz1=0.005)
    else:
        z, dzs, dzc = make_grid(z_top=z_top, n_levels=24, stretch=1.25,
                                 dz1=0.01)
    N = len(z)

    lam, C, lam_half = assign_layered_props(z, layers)

    # initialize from damping-depth solution
    omega = 2.0 * np.pi / 86400.0
    kappa_top = lam[0] / C[0]
    T_mean = 292.5
    A0 = 7.5
    T = initial_profile(z, T_mean, A0, omega, kappa_top, t0=0.0)
    # surface temperature: solve SEB at t=0 to get a consistent starting point
    Ts0, _ = solve_surface_energy_balance(T[1], dzc[0], lam_half[0], 0.0,
                                          surface_key, T[0])
    T[0] = Ts0

    # storage
    t_end = n_days * 86400.0
    n_steps = int(round(t_end / dt))
    dt_use = t_end / n_steps

    times = [0.0]
    Ts0_arr = [T[0]]
    G_arr = [lam_half[0] * (T[0] - T[1]) / dzc[0]]
    Rn_arr = [(1.0 - ALBEDO[surface_key]) * S_down(0.0)
              + EMIS[surface_key] * L_down_func(0.0)
              - EMIS[surface_key] * SIGMA_SB * T[0]**4]
    H_arr = [RHO_AIR * CP_AIR * (T[0] - T_air(0.0)) * C_H * U_wind(0.0)]
    profiles = [T.copy()]

    blew_up = False
    for n in range(1, n_steps + 1):
        t_now = n * dt_use

        # 1) advance the soil column with current T[0] held as Dirichlet
        T = step_alpha(T, dt_use, dzs, dzc, lam_half, C, alpha,
                       T_top=T[0], lower_bc="neumann")
        if not np.all(np.isfinite(T)) or np.max(np.abs(T - T_mean)) > 1e5:
            blew_up = True
            print(f"    {surface_key} alpha={alpha} dt={dt_use:.1f}s BLEW UP at step {n}")
            break

        # 2) update T[0] from SEB given new interior T[1]
        Ts0_new, conv = solve_surface_energy_balance(
            T[1], dzc[0], lam_half[0], t_now, surface_key, T[0])
        T[0] = Ts0_new

        # store
        if n % store_every == 0 or n == n_steps:
            times.append(t_now)
            Ts0_arr.append(T[0])
            G_arr.append(lam_half[0] * (T[0] - T[1]) / dzc[0])
            Rn_arr.append((1.0 - ALBEDO[surface_key]) * S_down(t_now)
                          + EMIS[surface_key] * L_down_func(t_now)
                          - EMIS[surface_key] * SIGMA_SB * T[0]**4)
            H_arr.append(RHO_AIR * CP_AIR * (T[0] - T_air(t_now))
                         * C_H * U_wind(t_now))
            profiles.append(T.copy())

    return {
        "surface": surface_key,
        "alpha": alpha,
        "dt": dt_use,
        "z": z, "dzs": dzs, "dzc": dzc,
        "lam": lam, "C": C, "lam_half": lam_half,
        "times": np.array(times),
        "Ts0": np.array(Ts0_arr),
        "G": np.array(G_arr),
        "Rn": np.array(Rn_arr),
        "H": np.array(H_arr),
        "profiles": np.array(profiles),
        "blew_up": blew_up,
        "n_steps": n_steps,
    }


def run_test_2():
    print("\n=== Test 2: prognostic SEB on three urban substrates ===")
    surfaces = ["asphalt_road", "concrete_roof", "bare_soil"]
    schemes = [("FTCS", 0.0), ("BTCS", 1.0), ("CN", 0.5)]
    # dt = 15 s : safely below the FTCS stability bound on all three surfaces
    #             (asphalt: dt_crit ~33 s with dz1=0.5 cm; roof: dt_crit ~17 s
    #             with dz1=0.5 cm; soil: dt_crit ~166 s with dz1=1 cm).
    # dt = 60 s : typical mesoscale-model time step, exceeds FTCS bound on
    #             roof (highly stiff), borderline on asphalt.
    # dt = 600 s: typical regional/climate-model time step, well beyond FTCS
    #             on all surfaces.
    dts = [15.0, 60.0, 600.0]

    results = {}
    for surface in surfaces:
        for sname, alpha in schemes:
            for dt in dts:
                key = (surface, sname, dt)
                print(f"  running {surface:14s} | {sname} | dt = {dt:5.1f} s ...")
                r = run_seb_column(surface, alpha, dt, n_days=2,
                                   store_every=max(1, int(round(60.0 / dt))))
                results[key] = r
    return results


def figure_3(test2_results):
    """24-h surface temperature evolution on day 2 for the three substrates,
    all schemes, dt = 15 s. (i.e., the small-dt regime where schemes agree.)
    """
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.0), sharey=True)
    surfaces = ["asphalt_road", "concrete_roof", "bare_soil"]
    schemes = [("FTCS", 0.0, C_FTCS), ("BTCS", 1.0, C_BTCS),
               ("CN",   0.5, C_CN)]

    for ax, surface in zip(axes, surfaces):
        for sname, alpha, col in schemes:
            r = test2_results[(surface, sname, 15.0)]
            if r["blew_up"]:
                continue
            t_day2 = r["times"] >= 86400.0
            t_h = (r["times"][t_day2] - 86400.0) / 3600.0
            ax.plot(t_h, r["Ts0"][t_day2] - 273.15, color=col,
                    linewidth=1.6, label=sname, alpha=0.9)
        ax.plot((np.linspace(0, 24, 200)),
                T_air(86400.0 + np.linspace(0, 86400, 200)) - 273.15,
                color="grey", linewidth=1.0, linestyle=":",
                label=r"$T_a$")
        ax.set_xlabel("Hour of day")
        ax.set_title(SUBSTRATE_NAMES[surface])
        ax.set_xlim(0, 24)
        ax.set_xticks([0, 6, 12, 18, 24])
        ax.legend(loc="upper right", frameon=False, fontsize=8)
        ax.grid(True, alpha=0.3)
    axes[0].set_ylabel(r"$T_s(0, t)$ ($^\circ$C)")

    plt.suptitle(r"Day-2 surface temperature, $\Delta t = 15$ s "
                 r"(schemes agree at small $\Delta t$)", y=1.02)
    plt.tight_layout()
    out = os.path.join(OUT, "fig3_seb_dt15.png")
    plt.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {out}")


def figure_4(test2_results):
    """Diurnal G(t) for three substrates at dt = 600 s. Shows scheme divergence.
    Reference is FTCS at dt=15s (smallest stable dt across all surfaces).
    """
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.0), sharey=True)
    surfaces = ["asphalt_road", "concrete_roof", "bare_soil"]

    for ax, surface in zip(axes, surfaces):
        # reference: FTCS at dt=15s
        r_ref = test2_results[(surface, "FTCS", 15.0)]
        if not r_ref["blew_up"]:
            t_day2 = r_ref["times"] >= 86400.0
            t_h = (r_ref["times"][t_day2] - 86400.0) / 3600.0
            ax.plot(t_h, r_ref["G"][t_day2], color="black", linewidth=1.8,
                    label=r"FTCS reference $\Delta t=15$ s")

        # compare FTCS, BTCS, CN at dt=600s
        for sname, col in [("FTCS", C_FTCS), ("BTCS", C_BTCS), ("CN", C_CN)]:
            r = test2_results[(surface, sname, 600.0)]
            if r["blew_up"]:
                ax.text(0.50, 0.92,
                        f"{sname} $\\Delta t=600$ s: BLEW UP",
                        transform=ax.transAxes, ha="center", va="top",
                        color=col, fontsize=8.5,
                        bbox=dict(boxstyle="round", facecolor="#ffeeee",
                                  edgecolor=col, alpha=0.7))
                continue
            t_day2 = r["times"] >= 86400.0
            t_h = (r["times"][t_day2] - 86400.0) / 3600.0
            ax.plot(t_h, r["G"][t_day2], color=col, linewidth=1.4,
                    label=fr"{sname} $\Delta t=600$ s", alpha=0.85)
        ax.set_xlabel("Hour of day")
        ax.set_title(SUBSTRATE_NAMES[surface])
        ax.set_xlim(0, 24)
        ax.set_xticks([0, 6, 12, 18, 24])
        ax.axhline(0, color="black", linewidth=0.5, alpha=0.5)
        ax.legend(loc="lower right", frameon=False, fontsize=8)
        ax.grid(True, alpha=0.3)
    axes[0].set_ylabel(r"$G$ (W/m$^2$, +ve = into ground)")

    plt.suptitle(r"Day-2 ground heat flux, $\Delta t = 600$ s "
                 r"vs FTCS $\Delta t=15$ s reference", y=1.02)
    plt.tight_layout()
    out = os.path.join(OUT, "fig4_G_dt600.png")
    plt.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {out}")


def figure_5(test2_results):
    """Vertical T profiles at three local times (06, 12, 18) for the asphalt
    road column at dt=600s, all schemes vs FTCS reference at dt=60s.
    """
    surface = "asphalt_road"
    target_hours = [6, 12, 18]   # local time in hours of day 2
    target_t = [86400.0 + h * 3600.0 for h in target_hours]

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.5), sharey=True)

    r_ref = test2_results[(surface, "FTCS", 15.0)]
    z = r_ref["z"]

    for ax, h, t_target in zip(axes, target_hours, target_t):
        # ref
        idx_ref = int(np.argmin(np.abs(r_ref["times"] - t_target)))
        ax.plot(r_ref["profiles"][idx_ref] - 273.15, z * 100,
                color="black", linewidth=2.0, label=r"FTCS ref $\Delta t=15$s")

        for sname, col in [("FTCS", C_FTCS), ("BTCS", C_BTCS), ("CN", C_CN)]:
            r = test2_results[(surface, sname, 600.0)]
            if r["blew_up"]:
                continue
            idx = int(np.argmin(np.abs(r["times"] - t_target)))
            ax.plot(r["profiles"][idx] - 273.15, r["z"] * 100,
                    color=col, linewidth=1.4,
                    label=f"{sname} $\\Delta t=600$s", alpha=0.85)

        ax.invert_yaxis()
        ax.set_xlabel(r"$T_s$ ($^\circ$C)")
        ax.set_title(f"{h:02d}:00 LT")
        ax.set_ylim(50, 0)
        ax.legend(loc="lower right", frameon=False, fontsize=8)
        ax.grid(True, alpha=0.3)
    axes[0].set_ylabel("Depth (cm)")

    plt.suptitle("Vertical profile, asphalt road column, day 2 — top 50 cm",
                 y=1.02)
    plt.tight_layout()
    out = os.path.join(OUT, "fig5_profiles_asphalt.png")
    plt.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {out}")


# ---------------------------------------------------------------------------
# 5. Quantitative metrics for cross-substrate comparison
# ---------------------------------------------------------------------------

def diurnal_metrics(test2_results):
    """For each (surface, scheme, dt), compute on day 2:
       - amplitude A_G = (max - min)/2
       - lag (vs FTCS dt=15s reference, in minutes)
       - daily heat storage Delta_S (J/m^2)
       - RMS error in T_s^0 vs reference (K)
    """
    surfaces = ["asphalt_road", "concrete_roof", "bare_soil"]
    schemes = ["FTCS", "BTCS", "CN"]
    dts = [15.0, 60.0, 600.0]

    rows = []
    for surface in surfaces:
        ref = test2_results[(surface, "FTCS", 15.0)]
        if ref["blew_up"]:
            continue
        mask_ref = ref["times"] >= 86400.0
        t_ref = ref["times"][mask_ref]
        G_ref = ref["G"][mask_ref]
        Ts_ref = ref["Ts0"][mask_ref]
        AG_ref = 0.5 * (np.max(G_ref) - np.min(G_ref))
        S_ref = np.trapezoid(G_ref, t_ref)

        for scheme in schemes:
            for dt in dts:
                r = test2_results[(surface, scheme, dt)]
                if r["blew_up"]:
                    rows.append({
                        "surface": surface, "scheme": scheme, "dt": dt,
                        "amp_G": np.nan, "amp_ratio": np.nan,
                        "lag_min": np.nan,
                        "store_kJ": np.nan, "rmse_Ts": np.nan,
                        "blew_up": True
                    })
                    continue
                mask = r["times"] >= 86400.0
                t = r["times"][mask]
                G = r["G"][mask]
                Ts = r["Ts0"][mask]
                AG = 0.5 * (np.max(G) - np.min(G))
                S = np.trapezoid(G, t)
                Ts_on_ref = np.interp(t_ref, t, Ts)
                rmse = float(np.sqrt(np.mean((Ts_on_ref - Ts_ref)**2)))
                G_on_ref = np.interp(t_ref, t, G)
                lag = compute_lag(G_on_ref, G_ref, t_ref)
                rows.append({
                    "surface": surface, "scheme": scheme, "dt": dt,
                    "amp_G": AG,
                    "amp_ratio": AG / AG_ref if AG_ref > 0 else np.nan,
                    "lag_min": lag,
                    "store_kJ": S / 1e3,
                    "rmse_Ts": rmse,
                    "blew_up": False
                })
    return rows


def compute_lag(signal, reference, times):
    """Cross-correlation lag in minutes. Positive = signal lags reference."""
    s = signal - np.mean(signal)
    r = reference - np.mean(reference)
    n = len(s)
    if n < 4:
        return np.nan
    # pad
    corr = np.correlate(s, r, mode="full")
    lags = np.arange(-n + 1, n)
    dt_s = times[1] - times[0]
    # restrict to physical lags: -3 h .. +3 h
    max_lag = int(round(3 * 3600.0 / dt_s))
    centre = n - 1
    sl = corr[centre - max_lag: centre + max_lag + 1]
    sl_lags = lags[centre - max_lag: centre + max_lag + 1]
    best = sl_lags[int(np.argmax(sl))]
    return best * dt_s / 60.0


def write_metrics_table(metrics_rows):
    out = os.path.join(TABLES, "metrics_summary.txt")
    with open(out, "w") as f:
        f.write("Cross-substrate comparison metrics (day 2 of 2-day integration)\n")
        f.write("=" * 90 + "\n")
        f.write(f"{'Surface':14s} {'Scheme':5s} {'dt(s)':>6} "
                f"{'A_G(W/m2)':>10} {'A/A_ref':>8} {'lag(min)':>9} "
                f"{'Store(kJ)':>10} {'RMSE_T(K)':>10}\n")
        f.write("-" * 90 + "\n")
        for r in metrics_rows:
            if r["blew_up"]:
                f.write(f"{r['surface']:14s} {r['scheme']:5s} {r['dt']:>6.0f} "
                        f"{'BLEW UP':>52s}\n")
                continue
            f.write(f"{r['surface']:14s} {r['scheme']:5s} {r['dt']:>6.0f} "
                    f"{r['amp_G']:>10.2f} {r['amp_ratio']:>8.4f} "
                    f"{r['lag_min']:>9.1f} {r['store_kJ']:>10.2f} "
                    f"{r['rmse_Ts']:>10.4f}\n")
    print(f"  saved {out}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("CLIM-715 project: ground heat flux numerical comparison")
    print("=" * 70)

    print("\n--- Figure 1: amplification factors ---")
    amp_rows = figure_1()
    with open(os.path.join(TABLES, "table_amp.txt"), "w") as f:
        f.write("Amplification factor at k*dz = pi (worst-case 2-dz wave)\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'nu':>8} {'A_FTCS':>12} {'A_BTCS':>12} {'A_CN':>12}\n")
        for nu, aF, aB, aC in amp_rows:
            f.write(f"{nu:>8.2f} {aF:>+12.4f} {aB:>+12.4f} {aC:>+12.4f}\n")

    print("\n--- Test 1 ---")
    t1, t1m = run_test_1()
    figure_2(t1, t1m)

    # Test-1 quantitative summary at end of day 5
    print("\nTest 1 quantitative summary (day 5, against analytical):")
    with open(os.path.join(TABLES, "table_test1.txt"), "w") as f:
        f.write("Test 1 -- Damping-depth verification (day 5)\n")
        f.write("=" * 95 + "\n")
        f.write("Surface T is enforced as Dirichlet, so the surface error is structurally\n")
        f.write("zero. The diagnostics below are at depth z = 10 cm (where amplitude and\n")
        f.write("phase encode the scheme's damping/dispersion behavior) and the surface\n")
        f.write("ground heat flux G = -lambda dT/dz|_0 (which involves the discretized\n")
        f.write("first derivative and is the most scheme-sensitive diagnostic).\n")
        f.write("-" * 95 + "\n")
        f.write(f"{'config':30s} {'dt(s)':>8} {'nu':>7} "
                f"{'RMSE_T@10cm(K)':>14} {'RMSE_G(W/m2)':>13} {'lag_G(min)':>11}\n")
        analytical_func = t1m["analytical"]
        G_anal_func = t1m["G_analytical"]
        z_grid = t1m["z"]
        for r in t1:
            if r["blew_up"]:
                f.write(f"{r['name']:30s} {r['dt']:>8.1f} {r['nu']:>7.2f}   BLEW UP\n")
                print(f"  {r['name']:30s}  BLEW UP")
                continue
            mask = (r["ts"] >= 4 * 86400.0) & (r["ts"] <= 5 * 86400.0)
            t_arr = r["ts"][mask]
            T10 = r["T_at_10cm"][mask]
            G = r["G_surface"][mask]
            T10_anal = analytical_func(z_grid[10], t_arr)
            G_anal = G_anal_func(t_arr)
            rmse_T = float(np.sqrt(np.mean((T10 - T10_anal)**2)))
            rmse_G = float(np.sqrt(np.mean((G - G_anal)**2)))
            lag = compute_lag(G, G_anal, t_arr)
            f.write(f"{r['name']:30s} {r['dt']:>8.1f} {r['nu']:>7.2f} "
                    f"{rmse_T:>14.4f} {rmse_G:>13.3f} {lag:>11.1f}\n")
            print(f"  {r['name']:30s}  RMSE_T(10cm) = {rmse_T:.4f} K  "
                  f"RMSE_G = {rmse_G:.2f} W/m^2  lag = {lag:+.1f} min")

    print("\n--- Test 2 ---")
    t2 = run_test_2()
    figure_3(t2)
    figure_4(t2)
    figure_5(t2)

    print("\n--- Cross-substrate metrics ---")
    metrics = diurnal_metrics(t2)
    write_metrics_table(metrics)
    for m in metrics:
        if m["blew_up"]:
            print(f"  {m['surface']:14s} {m['scheme']:5s} dt={m['dt']:5.0f}  BLEW UP")
        else:
            print(f"  {m['surface']:14s} {m['scheme']:5s} dt={m['dt']:5.0f}  "
                  f"A_G={m['amp_G']:6.1f}  ratio={m['amp_ratio']:.3f}  "
                  f"lag={m['lag_min']:+5.1f} min  RMSE={m['rmse_Ts']:.3f} K")

    print("\nDone.")


if __name__ == "__main__":
    main()
