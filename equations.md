# Equations of `modified_full_report_1.docx` — LaTeX form

Reference: every equation appearing in the long report, written in proper KaTeX/MathJax-renderable LaTeX. Section headings follow the report's own structure.

---

## §2.1 The substrate heat equation

**Conductivity-form 1-D heat equation:**

$$
C_s(z)\,\frac{\partial T_s}{\partial t} \;=\; \frac{\partial}{\partial z}\!\left[\,\lambda_s(z)\,\frac{\partial T_s}{\partial z}\,\right]
$$

with $T_s(z,t)$ substrate temperature, $\lambda_s(z)$ thermal conductivity (W m⁻¹ K⁻¹), and $C_s(z)$ volumetric heat capacity (J m⁻³ K⁻¹). $z$ points downward, $z=0$ at the surface.

The diffusivity form (used in §2.5 stability analysis on a uniform $\kappa_s$ grid) absorbs $C_s$ into thermal diffusivity:

$$
\frac{\partial T}{\partial t} \;=\; \nabla\!\cdot\!\left(\kappa\,\nabla T\right), \qquad \kappa_s \;=\; \frac{\lambda_s}{C_s}.
$$

---

## §2.2 Spatial discretization on a stretched grid

**Half-level placement:**

$$
z_{j+1/2} \;=\; \tfrac{1}{2}\bigl(z_j + z_{j+1}\bigr).
$$

**Harmonic-mean conductivity at a half-level** (preserves the heat flux exactly across a $\lambda$ discontinuity):

$$
\lambda_{j+1/2} \;=\; \frac{2\,\lambda_j\,\lambda_{j+1}}{\lambda_j + \lambda_{j+1}}.
$$

**Discrete conductive flux at a half-level** (sign convention $G>0$ = downward, into the ground):

$$
G_{j+1/2} \;=\; \lambda_{j+1/2}\,\frac{T_j - T_{j+1}}{z_{j+1} - z_j}.
$$

**Semi-discrete tendency at cell $j$:**

$$
C_j\,\Delta z_j\,\frac{dT_j}{dt} \;=\; G_{j-1/2} - G_{j+1/2}.
$$

---

## §2.3 The $\alpha$-weighted $\theta$-method

$$
C_j\,\Delta z_j\,\frac{T_j^{\,n+1} - T_j^{\,n}}{\Delta t}
\;=\; \alpha\bigl[\,G_{j-1/2} - G_{j+1/2}\,\bigr]^{\,n+1}
\;+\; (1-\alpha)\bigl[\,G_{j-1/2} - G_{j+1/2}\,\bigr]^{\,n}.
$$

| $\alpha$ | Scheme | Order in $\Delta t$ | Stability |
|---|---|---|---|
| $0$ | FTCS (forward Euler) | first | conditional, $\nu \le \tfrac{1}{2}$ |
| $\tfrac{1}{2}$ | Crank–Nicolson | second | unconditional |
| $1$ | BTCS (backward Euler) | first | unconditional |

---

## §2.4 Boundary conditions

**Lower (Neumann zero-flux at $z = z_\text{top} = 2$ m):**

$$
T_{N-1} \;=\; T_{N-2}.
$$

**Upper (Dirichlet, top cell centre):**

$$
T_0 \;=\; T_s^{0},
$$

where $T_s^{0}$ is prescribed sinusoidally in Test 1 and solved from the SEB by Newton iteration in Test 2.

---

## §2.5 Von Neumann amplification factors

Substituting $T_j^{\,n} = A^{\,n}\exp(i\,k\,j\,\Delta z)$ into each scheme on a uniform grid with constant $\kappa_s = \lambda_s/C_s$ and defining

$$
\boxed{\;\nu \;\equiv\; \frac{\kappa_s\,\Delta t}{\Delta z^{2}}\;}
$$

gives the per-step amplification factors:

$$
A_\mathrm{FTCS}(\nu,\,k\Delta z) \;=\; 1 \;-\; 2\,\nu\,\bigl(1 - \cos k\Delta z\bigr),
$$

$$
A_\mathrm{BTCS}(\nu,\,k\Delta z) \;=\; \frac{1}{1 \;+\; 2\,\nu\,(1 - \cos k\Delta z)},
$$

$$
A_\mathrm{CN}(\nu,\,k\Delta z) \;=\; \frac{1 - \nu\,(1 - \cos k\Delta z)}{1 + \nu\,(1 - \cos k\Delta z)}.
$$

**Worst case at the $2\Delta z$ wave** ($k\Delta z = \pi$):

$$
A_\mathrm{FTCS}(\nu,\,\pi) \;=\; 1 - 4\nu, \qquad
A_\mathrm{BTCS}(\nu,\,\pi) \;=\; \frac{1}{1 + 4\nu}, \qquad
A_\mathrm{CN}(\nu,\,\pi) \;=\; \frac{1 - 2\nu}{1 + 2\nu}.
$$

The FTCS stability bound $|A_\mathrm{FTCS}| \le 1$ at $k\Delta z = \pi$ requires $\nu \le \tfrac{1}{2}$, i.e.

$$
\Delta t \;\le\; \frac{1}{2}\,\frac{\Delta z^{2}}{\kappa_s}.
$$

---

## §3.3 Surface energy balance and Newton iteration

**Surface energy balance (residual form, $F=0$ at solution):**

$$
F(T_s^{0}) \;\equiv\; R_n(T_s^{0}) \;-\; H(T_s^{0}) \;-\; LE(T_s^{0}) \;-\; G(T_s^{0}) \;=\; 0.
$$

**Components:**

$$
R_n \;=\; (1 - \alpha_s)\,S{\downarrow} \;+\; \varepsilon_s\,L{\downarrow} \;-\; \varepsilon_s\,\sigma\,(T_s^{0})^{4},
$$

$$
H \;=\; \rho\,c_p\,\frac{T_s^{0} - T_a}{r_a},
\qquad
r_a \;=\; \frac{1}{C_H\,U},
\qquad
C_H = 5\times10^{-3},\ U = 3\ \text{m s}^{-1},
$$

$$
LE \;=\; 0\quad(\text{strict-impervious assumption}),
$$

$$
G \;=\; \lambda_{1/2}\,\frac{T_s^{0} - T_1}{z_1 - z_0}.
$$

**Newton step** with the analytical Jacobian (terminated at $|\Delta T_s^{0}| < 10^{-4}$ K):

$$
\frac{dF}{dT_s} \;=\; \frac{dR_n}{dT_s} \;-\; \frac{dH}{dT_s} \;-\; \frac{dG}{dT_s},
\qquad
\frac{dR_n}{dT_s} \;=\; -4\,\varepsilon_s\,\sigma\,(T_s^{0})^{3}.
$$

The other Jacobian terms are $dH/dT_s = \rho c_p / r_a$ and $dG/dT_s = \lambda_{1/2}/(z_1-z_0)$. Because $U$ is held constant in this study, the Newton step evaluates $U$ in $r_a$ at $t=0$ without loss of accuracy.

---

## §3.4 Synthetic forcing

With $\omega = 2\pi/86400\ \text{s}^{-1}$:

$$
S{\downarrow}(t) \;=\; \max\!\Bigl[1000\,\cos\!\bigl(\omega(t-12\,\mathrm{h})\bigr),\;0\Bigr]\ \text{W m}^{-2},
$$

$$
L{\downarrow}(t) \;=\; 350 \;+\; 20\,\cos\!\bigl(\omega(t-14\,\mathrm{h})\bigr)\ \text{W m}^{-2},
$$

$$
T_a(t) \;=\; 292.5 \;+\; 7.5\,\cos\!\bigl(\omega(t-14\,\mathrm{h})\bigr)\ \text{K},
$$

$$
U(t) \;=\; 3\ \text{m s}^{-1}\quad(\text{constant}).
$$

---

## §3.5 Damping-depth initialization

**Initial profile at $t=0$ (midnight)** with effective top-cell diffusivity $\kappa_\text{top}=\lambda_\text{top}/C_\text{top}$:

$$
T_s(z,\,0) \;=\; T_\text{mean} \;+\; A_0\,\exp\!\bigl(-z/d_\text{top}\bigr)\,\cos\!\bigl(-z/d_\text{top}\bigr),
\qquad
d_\text{top} \;=\; \sqrt{\frac{2\,\kappa_\text{top}}{\omega}},
$$

with $T_\text{mean} = 292.5$ K and $A_0 = 7.5$ K. (The 12-hour phase mismatch between this profile and the SEB-driven cycle is absorbed during day 1; diagnostics are taken on day 2.)

---

## §4.1 Damping-depth analytical solution

For a semi-infinite medium with sinusoidal Dirichlet forcing $T_s(0,t) = \bar T + A\cos(\omega t)$ (Carslaw & Jaeger, 1959 §2.6; Hillel, 2003):

**Temperature wave (exponential damping + linear phase lag with depth):**

$$
T_s(z,\,t) \;=\; \bar T \;+\; A\,\exp\!\bigl(-z/d\bigr)\,\cos\!\bigl(\omega t - z/d\bigr),
\qquad
d \;=\; \sqrt{\frac{2\,\kappa}{\omega}}.
$$

**Surface ground heat flux (leads $T_s$ by $\pi/4$ = 3 hours):**

$$
G(0,\,t) \;=\; \lambda\,\frac{A}{d}\,\sqrt{2}\;\cos\!\bigl(\omega t + \tfrac{\pi}{4}\bigr).
$$

The flux leads the surface temperature because $\partial T_s/\partial z\big|_{z=0}$ peaks before $T_s(0,t)$ does.

---

## §5.1 FTCS critical time step on a layered substrate

The critical $\Delta t$ for the most thermally stiff layer:

$$
\Delta t_\text{crit} \;=\; \frac{1}{2}\,\frac{\Delta z^{2}}{\kappa},
\qquad \kappa \;=\; \frac{\lambda}{C}.
$$

For the substrates simulated:

| Substrate | top $\lambda$ (W m⁻¹ K⁻¹) | top $C$ (J m⁻³ K⁻¹) | $\kappa$ (m² s⁻¹) | $\Delta z$ | $\Delta t_\text{crit}$ |
|---|---|---|---|---|---|
| Asphalt road | $0.75$ | $2.0\times10^{6}$ | $3.75\times10^{-7}$ | 0.5 cm | $\approx 33$ s |
| Concrete roof (deck) | $1.50$ | $2.1\times10^{6}$ | $7.14\times10^{-7}$ | 0.5 cm | $\approx 17$ s |
| Bare soil | $0.30$ | $1.3\times10^{6}$ | $2.31\times10^{-7}$ | 1 cm | $\approx 217$ s |

---

## §5.3 Substrate descriptors used in the SHAP attribution

**Bulk admittance** (depth-weighted over the top 30 cm):

$$
\mu_\text{eff} \;=\; \sqrt{\,\lambda_\text{eff}\,C_\text{eff}\,},
$$

with values for the three idealized substrates (top layer):

$$
\mu_\text{asphalt}\approx 1225,\quad
\mu_\text{roof}\approx 1775,\quad
\mu_\text{soil}\approx 624
\qquad (\text{J m}^{-2}\,\text{K}^{-1}\,\text{s}^{-1/2}).
$$

**Top-cell thermal diffusivity** (the parameter that sets the FTCS stability bound and dominates the SHAP ranking):

$$
\kappa_\text{top} \;=\; \frac{\lambda_\text{top}}{C_\text{top}}.
$$

Values: $\kappa_\text{soil} = 2.31\times10^{-7}$, $\kappa_\text{asphalt} = 3.75\times10^{-7}$, $\kappa_\text{roof} = 7.14\times10^{-7}$ m² s⁻¹.

**Layer-interface descriptor** (max ratio across any internal interface):

$$
\text{max}\,\lambda\text{-contrast} \;=\; \max_{j\in\text{interfaces}}\,\max\!\Bigl(\frac{\lambda_j}{\lambda_{j+1}},\,\frac{\lambda_{j+1}}{\lambda_j}\Bigr).
$$

---

## §5.2 Empirical $\Delta t$-refinement ratio

For a first-order error in $\Delta t$ between $\Delta t = 60$ s and $\Delta t = 600$ s, the expected ratio is

$$
\frac{\mathrm{RMSE}_{T_s}\!\bigl(\Delta t = 600\,\text{s}\bigr)}{\mathrm{RMSE}_{T_s}\!\bigl(\Delta t = 60\,\text{s}\bigr)}
\;\approx\; \frac{600}{60} \;=\; 10.
$$

Observed ratios (from $\textit{test2\_extended\_metrics.csv}$): asphalt BTCS 9.4, asphalt CN 9.8; roof BTCS 8.2, roof CN 9.2; soil BTCS 9.9, soil CN 10.2 — all in $[8.2,\,10.2]$, identifying the operator-splitting error between the column and SEB updates as the dominant first-order term.

---

## §6 Diagnostic for the SHAP target variable

For each of the $N=150$ synthetic substrate columns, the BTCS coarse-$\Delta t$ surface-temperature error is

$$
\mathrm{RMSE}_{T_s} \;=\; \sqrt{\,\frac{1}{N_\text{day2}}\sum_{t\in\text{day 2}}\!\Bigl[\,T_s^\text{BTCS,\,600\,s}(t) \;-\; T_s^\text{ref,\,15\,s}(t)\,\Bigr]^{\,2}\,}.
$$

Six features are used: $\kappa_\text{top}$, $\mu_\text{eff}$, max $\lambda$-contrast, number of significant ($>1.5\times$) interfaces, depth of the first significant interface, and $h_\text{top}$.

Result: $\kappa_\text{top}$ alone explains $R^{2} = 0.92$ of the variance, with mean $|\mathrm{SHAP}|_{\,\kappa_\text{top}} = 0.71$ K.

---

## Constants used throughout

| Symbol | Value | Description |
|---|---|---|
| $\sigma$ | $5.670374419\times10^{-8}$ W m⁻² K⁻⁴ | Stefan–Boltzmann |
| $\rho$ | $1.2$ kg m⁻³ | air density |
| $c_p$ | $1005$ J kg⁻¹ K⁻¹ | specific heat of air |
| $C_H$ | $5\times10^{-3}$ | bulk transfer coefficient |
| $U$ | $3$ m s⁻¹ | wind speed (constant) |
| $\omega$ | $2\pi/86400 = 7.2722\times10^{-5}$ s⁻¹ | diurnal angular frequency |
| $\alpha_s$ | 0.10 / 0.30 / 0.20 | albedo (asphalt / roof / soil) |
| $\varepsilon_s$ | 0.95 / 0.92 / 0.95 | emissivity (asphalt / roof / soil) |

---

*Equations extracted from `modified_full_report_1.docx`, cross-checked against `run_experiments.py` and `shap_attribution.py`. All formulas are verified to agree with the code implementation and with the published numerical results in `test2_extended_metrics.csv`, `shap_summary.csv`, and `shap_residual_summary.csv`.*
