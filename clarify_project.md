# Clarify the Project: A Mastery-Level Walkthrough

A LaTeX-rendered companion to `modified_full_report_1.docx`. Every concept, every equation, every notation explained from zero, with regular references to the course lecture notes (`Lecture_1_2_3_4_5_6_7_8_9_10_11_Notes.md`) and your six homeworks (HW1–HW6).

For every major equation, this document indicates whether it is **[Established theoretical formula]**, **[Derived in the document]**, or **[Definition]**, so you know at a glance whether to memorise it as physics or accept it as a project-specific choice.

---

## Part 0. How to use this document

This document is built so that anyone — even with zero prior knowledge of numerical modelling, partial differential equations, or surface-energy-balance physics — can read the long report and defend every choice in it.

**Reading recipe.** Read Parts 1–3 in order: they install the language used in the rest of the document. Then open the long report on one screen and this clarification on the other, and walk through them in parallel — when the report mentions §2.5, jump to Part 6.5 here.

**Conventions.**
- Inline math uses single dollars: e.g. $\nu = \kappa \Delta t / \Delta z^2$.
- Display equations use double dollars and stand on their own line.
- Course-material references use the form **[Notes #6 §6.1]** to mean "Notes #6, Section 6.1".
- Homework references look like **[HW3, Case 3]** — meaning "your HW3 submission, the case labelled Case 3".
- Every major equation carries a status label:
  - **[Established]** — fundamental physical law or established textbook result that pre-dates the project.
  - **[Derived]** — derived in this document (or in the long report) from established formulas, with the derivation visible.
  - **[Definition]** — a definition or a project-specific discretization choice; nothing to "prove".

---

## Part 1. Foundational physics: heat, temperature, and the substrate

### 1.1 What does it mean for the ground to conduct heat?

Imagine a paving stone in the sun. The top is hot — say $50 ^\circ\mathrm{C}$. Five centimetres down, the stone is much cooler — say $30 ^\circ\mathrm{C}$. There is a temperature gradient inside the stone. As long as that gradient exists, heat will flow from the hot top to the cool bottom. This flow is conduction. There is no air movement, no fluid mixing — energy is passed from molecule to molecule through the solid.

The amount of heat that flows per square metre per second is the **conductive heat flux**, denoted $G$ in this project. Its units are watts per square metre, $\mathrm{W/m^{2}}$. By convention $G > 0$ means flow downward — into the ground.

To make this less abstract: a typical mid-afternoon $G$ on a sun-warmed asphalt road is about $200$ W/m² (positive, into the ground). At night the same surface emits at perhaps $-50$ W/m² (negative, out of the ground). Both numbers fit on a small portion of a $1000$ W/m² peak insolation, which is why $G$ is "small in the daily mean" but "large in the diurnal range".

### 1.2 The four key material properties

Every substrate is described by two material numbers, from which a third (the thermal diffusivity) is derived. The fourth quantity (the diurnal damping depth) is a length scale derived from the diffusivity.

**Thermal conductivity** $\lambda$ (Greek "lambda"). Units W/m/K. How easily heat flows under a given temperature gradient. Air $\approx 0.025$; rigid foam $\approx 0.03$; dry sandy soil $\approx 0.30$; asphalt $\approx 0.75$; concrete $\approx 1.5$; granite $\approx 3.0$. Bigger $\lambda$ means heat propagates more easily.

**Volumetric heat capacity** $C$. Units J/m³/K. The energy needed to raise one cubic metre of the material by one Kelvin. Water $= 4.18 \times 10^{6}$; concrete $\approx 2.1\times 10^{6}$; dry sandy soil $\approx 1.3\times 10^{6}$. Note water is the universe's record-holder for $C$ — that is why coastal climates are so much milder than inland ones.

**Thermal diffusivity** $\kappa$ (Greek "kappa"). Defined as

$$\kappa = \frac{\lambda}{C}.$$

> **Status: [Definition].** $\kappa$ is just a name for the ratio $\lambda/C$.

Units m²/s. How quickly a temperature disturbance propagates. For our substrates $\kappa$ is in the range $10^{-7}$ to $10^{-6}$ m²/s.

**Diurnal damping depth** $d$:

$$d = \sqrt{\frac{2\kappa}{\omega}}, \qquad \omega = \frac{2\pi}{86400\ \text{s}} \approx 7.27 \times 10^{-5}\ \text{rad/s}.$$

> **Status: [Established theoretical formula]**, derived from solving the heat equation in a semi-infinite medium with sinusoidal Dirichlet forcing (Carslaw & Jaeger 1959 §2.6; Hillel 2003). We re-derive it from scratch in Part 8.1 of this document.

> **Lecture-notes connection.** [Notes #2 — 2nd-Order PDEs] classifies the heat equation explicitly as **parabolic** ($B^2 - 4AC = 0$) and notes: "Amplitude decreases; the initial 'pile' of material does not propagate but spreads horizontally, conserving the total quantity under the curve." That is the physical picture our $\kappa$ controls.

### 1.3 The diurnal damping depth — the most important length scale

Plugging the project's substrate values into $d = \sqrt{2\kappa/\omega}$:

**Worked example — bare soil damping depth.**

Sandy loam: $\lambda = 0.30$ W/m/K, $C = 1.3\times 10^6$ J/m³/K.

$$\kappa = \frac{\lambda}{C} = \frac{0.30}{1.3\times 10^6} = 2.31\times 10^{-7}\ \text{m}^2/\text{s}.$$

$$d = \sqrt{\frac{2 \times 2.31\times 10^{-7}}{7.27\times 10^{-5}}} = \sqrt{6.35\times 10^{-3}} = 0.0797\ \text{m} = 7.97\ \text{cm}.$$

Same calculation for the other two substrates:

| Substrate | $\lambda$ | $C$ | $\kappa = \lambda/C$ | $d$ |
|---|---|---|---|---|
| Bare soil | 0.30 | $1.3\times 10^{6}$ | $2.31\times 10^{-7}$ | 7.97 cm |
| Asphalt (top) | 0.75 | $2.0\times 10^{6}$ | $3.75\times 10^{-7}$ | 10.16 cm |
| Concrete deck | 1.50 | $2.1\times 10^{6}$ | $7.14\times 10^{-7}$ | 14.02 cm |

So the daily wave penetrates only the top 8–14 cm in any of these materials. To capture how the wave decays, our topmost grid cells must be much smaller than $d$ — typically half a centimetre to one centimetre.

### 1.4 Why $d$ matters for picking time steps

Once we resolve $d$ with cells of thickness $\Delta z \sim 0.5$ cm, we run into a constraint on $\Delta t$. For the explicit (FTCS) scheme, the maximum stable time step is

$$\Delta t_{\max} = \frac{1}{2}\frac{\Delta z^2}{\kappa}.$$

> **Status: [Derived]** — this comes from von Neumann stability analysis (Part 6.5 below). Standard result for parabolic equations [Notes #9 §Pure Diffusion].

For $\Delta z = 5$ mm $= 0.005$ m and the concrete deck's $\kappa = 7.14\times 10^{-7}$ m²/s:

**Worked example — the 17-second problem.**

$$\Delta t_{\max} = \frac{1}{2}\frac{(0.005)^2}{7.14\times 10^{-7}} = \frac{1}{2}\frac{2.5\times 10^{-5}}{7.14\times 10^{-7}} \approx 17\ \text{s}.$$

Operational mesoscale models run with $\Delta t = 60$–$600$ s. At $\Delta t = 60$ s on the concrete deck, FTCS exceeds the bound by a factor of about 4; at $\Delta t = 600$ s by a factor of about 35. Explicit time stepping is structurally ruled out.

> **Connecting to your work.** In **[HW1]** you saw the consequence of violating an explicit-stability bound: your FTCS tracer integration *blew up at step 113*, with $\max |q|$ exceeding 10. Same kind of explosive instability that the project's FTCS at $\Delta t = 600$ s on the asphalt road exhibits in 4–5 steps. The mechanism is identical: $|A| > 1$ at the worst Fourier mode causes geometric growth.

### 1.5 The four-component surface energy balance

Surface temperature $T_s^0$ is determined not by some external rule but by an energy balance at the surface. Four fluxes meet there:

- $R_n$ — net absorbed radiation (sun + sky longwave minus surface longwave emission), positive when energy is being deposited.
- $H$ — sensible heat flux to the air, positive when heat leaves the surface upward.
- $LE$ — latent heat flux from evaporation. In this project $LE = 0$ (impervious surfaces).
- $G$ — conductive heat flux into the substrate (positive downward).

Energy conservation requires what arrives equals what leaves:

$$R_n - H - LE - G = 0.$$

> **Status: [Established]** — first law of thermodynamics applied at the surface.

This is the **surface energy balance** (SEB). Together with the heat equation in the substrate, it determines $T_s^0$ at every moment.

### 1.6 Units and dimensional analysis sanity check

- $C \partial T/\partial t$ has units (J/m³/K)(K/s) = W/m³ — energy per cubic metre per second.
- $\partial/\partial z[\lambda \partial T/\partial z]$ has units m⁻¹·(W/m/K)·K·m⁻¹ = W/m³. Same units. ✓
- The amplification factor $A$ is dimensionless. ✓
- $\nu = \kappa \Delta t/\Delta z^2$ has units (m²/s)(s)/m² = dimensionless. ✓
- $r_a = 1/(C_H U)$ has units 1/(m/s) = s/m. ✓
- $H = \rho c_p (T_s - T_a)/r_a$ : (kg/m³)(J/kg/K)(K)/(s/m) = W/m². ✓

> **[Notes #3 §1 Taylor Series]** is the algebraic foundation of the finite differences we use. **[Notes #3 §3 Definition of the Derivative]** opens with the limit definition $f'(x) = \lim_{h\to 0}[f(x+h) - f(x)]/h$ — exactly what we approximate when we set $h = \Delta x$ and stop taking the limit.

---

## Part 2. From a continuous PDE to a discrete computer program

### 2.1 What is a partial differential equation?

An ordinary differential equation (ODE) describes how something changes with respect to a single variable. Newton's law of cooling, $dT/dt = -k(T - T_\infty)$, is an ODE.

A partial differential equation (PDE) involves derivatives with respect to more than one variable. Heat conduction in depth is a PDE because $T$ depends on both $z$ and $t$:

$$\frac{\partial T}{\partial t} = \kappa \frac{\partial^2 T}{\partial z^2}.$$

> **Status: [Established]** — the diffusion equation, derived from Fourier's law plus energy conservation. We derive it in Part 6.1 below.

A computer cannot solve a PDE in continuous form. We replace continuous derivatives with **finite differences** on a discrete grid: cells at depths $z_0, z_1, \ldots, z_{N-1}$, advanced through time in steps $\Delta t$.

### 2.2 The PDE classification — why heat is parabolic

[Notes #2] classifies linear second-order PDEs by the discriminant $B^2 - 4AC$ of the general form

$$A u_{xx} + B u_{xy} + C u_{yy} + \text{lower-order terms} = 0.$$

> **Status: [Established]** — standard PDE classification.

- **Elliptic** ($B^2 - 4AC < 0$). Example: Laplace's equation $\nabla^2 u = 0$.
- **Hyperbolic** ($B^2 - 4AC > 0$). Example: the wave equation $u_{tt} - c^2 u_{xx} = 0$.
- **Parabolic** ($B^2 - 4AC = 0$). Example: the diffusion equation $u_t = \kappa u_{xx}$.

Our heat conduction equation, written as $u_t - \kappa u_{zz} = 0$, has $A = -\kappa$, $B = 0$, $C = 0$: discriminant is $0 - 4(-\kappa)(0) = 0$, parabolic.

> **[Notes #2 — Summary]**: *"The PDEs that we encounter in weather/climate modeling are largely hyperbolic and parabolic"*. The advection problems you handled in HW1 and HW2 are hyperbolic; the project is parabolic.

### 2.3 The two basic finite-difference ideas

To replace a derivative by a finite difference, use Taylor's theorem [Notes #3 §1]. For a smooth function $f(x)$:

$$f(x + \Delta x) = f(x) + \Delta x f'(x) + \frac{\Delta x^2}{2} f''(x) + \frac{\Delta x^3}{6} f'''(x) + O(\Delta x^4).$$

> **Status: [Established]** — Taylor's theorem.

Rearranging gives three estimates of $f'(x)$:

**Forward difference**:

$$f'(x) \approx \frac{f(x + \Delta x) - f(x)}{\Delta x}.$$

> **Status: [Established]** — direct from Taylor's theorem. First-order accurate, error $O(\Delta x)$.

**Backward difference**:

$$f'(x) \approx \frac{f(x) - f(x - \Delta x)}{\Delta x}.$$

> **Status: [Established]** — first-order accurate.

**Centred difference**:

$$f'(x) \approx \frac{f(x + \Delta x) - f(x - \Delta x)}{2 \Delta x}.$$

> **Status: [Established]** — second-order accurate, $O(\Delta x^2)$, because the leading $O(\Delta x)$ error term cancels when we subtract the two Taylor expansions.

For a second derivative we use the centred three-point formula:

$$f''(x) \approx \frac{f(x + \Delta x) - 2f(x) + f(x - \Delta x)}{\Delta x^2} + O(\Delta x^2).$$

> **Status: [Established]** — second-order accurate. Used throughout the project for $\partial^2 T/\partial z^2$.

> **[HW1]** and **[HW2]** both apply the centred-time, centred-space ("CTCS") scheme to advection — so you are already familiar with the centred-difference algebra. The project applies the same centred difference for the spatial derivative, but pairs it with backward time (BTCS) or trapezoidal time (CN) instead of centred time.

### 2.4 What does "stability" mean?

A finite-difference scheme is **stable** if small numerical errors at one time step do not grow unboundedly over many time steps. If errors grow, the solution "blows up" — computed temperatures become infinite or NaN. Stability is separate from accuracy.

Some schemes are **conditionally stable** — $\Delta t$ must be smaller than some bound. Others are **unconditionally stable**. Von Neumann analysis (Part 6.5) finds these bounds.

There is also a related concept, **convergence**: as $\Delta t \to 0$ and $\Delta z \to 0$, the numerical solution should approach the true solution. The Lax equivalence theorem states that for a *consistent* scheme, stability is necessary and sufficient for convergence.

> **Status of the Lax equivalence theorem: [Established]** (Lax 1956). Standard result in numerical PDE theory.

> **[Notes #6 §10 (Slides 29–31)]** introduces von Neumann analysis. **[HW3]** and **[HW4]** both used it.

---

## Part 3. The vocabulary of finite-difference time-stepping schemes

### 3.1 The general framework

[Notes #6 §3] introduces the notation: let $\psi$ denote the true solution, $\phi_j^n$ the numerical approximation at $t = n \Delta t$. For the ODE form $d\psi/dt = f(\psi, t)$, the goal is to construct schemes for advancing $\phi^n \to \phi^{n+1}$ that approximate the exact integral

$$\psi^{n+1} = \psi^n + \int_{n\Delta t}^{(n+1)\Delta t} f(\psi, t) dt.$$

> **Status: [Established]** — this is the fundamental theorem of calculus applied to the ODE.

### 3.2 Explicit vs implicit (Notes #6 §5)

**Explicit (forward Euler):** $T^{n+1} = T^n + \Delta t f(T^n)$. Cheap per step, conditionally stable.

**Implicit (backward Euler):** $T^{n+1} = T^n + \Delta t f(T^{n+1})$. Expensive per step, unconditionally stable.

> **Status: [Established]** schemes — both date from Euler's work in the 18th century.

### 3.3 The trapezoidal rule = Crank–Nicolson

Take the average of explicit and implicit:

$$T^{n+1} = T^n + \frac{\Delta t}{2}[f(T^n) + f(T^{n+1})].$$

> **Status: [Established]** — trapezoidal rule for ODE integration. When applied to the heat equation specifically, it is named the **Crank–Nicolson** scheme (Crank & Nicolson 1947).

### 3.4 The full $\theta$-method family

All three schemes are special cases of one formula:

$$T^{n+1} = T^n + \Delta t[\alpha f(T^{n+1}) + (1-\alpha) f(T^n)].$$

> **Status: [Established]** — the $\theta$-method (sometimes called the $\alpha$-method). Standard textbook formulation.

| $\alpha$ | Scheme | Order in $\Delta t$ | Stability |
|---|---|---|---|
| $0$ | FTCS / Forward Euler | first | conditional, $\nu \le 1/2$ |
| $1/2$ | Crank–Nicolson | second | unconditional |
| $1$ | BTCS / Backward Euler | first | unconditional |

> **[Notes #6 §6 (Slides 15–17)]** introduces these three exact schemes. The lecture-note formulae are
>
> $$\phi^{n+1} = \phi^n + \Delta t f^n \quad \text{(Euler/forward)}$$
>
> $$\phi^{n+1} = \phi^n + \Delta t f^{n+1} \quad \text{(Backward)}$$
>
> $$\phi^{n+1} = \phi^n + \tfrac{1}{2}\Delta t (f^n + f^{n+1}) \quad \text{(Trapezoidal)}$$
>
> The project's FTCS, BTCS, CN are these same three schemes, applied to the parabolic diffusion equation rather than to the ODE oscillation equation that the lecture used for illustration.

### 3.5 Other schemes you have seen

[Notes #6] discusses several more schemes besides Euler, Backward, Trapezoidal.

**Matsuno scheme** (predictor-corrector):

$$\phi^{* n+1} = \phi^n + \Delta t f^n, \qquad \phi^{n+1} = \phi^n + \Delta t f(\phi^{* n+1}).$$

> **Status: [Established]** (Matsuno 1966). First-order, but explicit.

**Heun scheme** (2nd-order Runge–Kutta): explicit, second-order. **Status: [Established]**.

**Leapfrog**: $\phi^{n+1} = \phi^{n-1} + 2\Delta t f^n$. Three-level, explicit, second-order. **Status: [Established]** but **unconditionally unstable for diffusive problems** — which is why we cannot use it here.

> **[HW3]** is the direct ancestor of this project. You implemented Euler, Backward, Trapezoidal, AND Matsuno on the oscillation equation $d\psi/dt = i\omega\psi$. Your figures showed:
>
> - **[HW3 Case 1 — Euler]**: amplitude grows above 1 for all four values of $n$. Euler is unstable on the oscillation equation.
> - **[HW3 Case 2 — Backward]**: amplitude decays below 1. Backward is always stable but damping.
> - **[HW3 Case 3 — Trapezoidal]**: amplitude stays exactly at 1. Trapezoidal is neutrally stable for the oscillation equation.
> - **[HW3 Case 4 — Matsuno]**: amplitude decays slightly. Matsuno-Euler iterative correction stabilises the explicit Euler step.
>
> The diffusion equation is parabolic, not oscillatory, so the *quantitative* conclusions are different (Trapezoidal is now strictly stable, not just neutral; Backward damps the worst wave aggressively rather than mildly), but the *ranking* — Euler unstable past a bound, Backward unconditionally stable but first-order, Trapezoidal unconditionally stable AND second-order — is identical.

### 3.6 Why the project uses the $\theta$-method specifically

Implementing all three schemes via one $\alpha$-parameterised routine has three benefits:

1. Single source of truth for the spatial discretisation — bugs there affect all three schemes equally and cannot bias the comparison.
2. Three numbers ($\alpha = 0, 1/2, 1$) replace three separately implemented routines.
3. The same banded-tridiagonal solver handles BTCS and CN.

---

## Part 4. Walking through the abstract

The abstract is the densest paragraph in the report. We unpack it claim by claim.

**"The ground heat flux is the energy that the surface stores and releases from its substrate over a diurnal cycle, and is the term in the surface energy budget that is most sensitive to numerical treatment."**

$G$ is small in daily mean (small fraction of $R_n$), but it controls the day-night temperature swing. The other three SEB terms are local in time: they depend on the current $T_s^0$ and current atmospheric forcing. $G$ is the term that involves the full *history* of the substrate — and that history dependence is exactly what numerical errors accumulate in.

**"The governing one-dimensional heat conduction equation in the substrate is parabolic, and its explicit forward-time discretization is conditionally stable only when $\nu = \kappa_s\Delta t/\Delta z^2 \le 1/2$."**

- "parabolic" — discriminant $B^2 - 4AC = 0$.
- "explicit forward-time discretization" = FTCS = $\alpha = 0$ in the $\theta$-method.
- "conditionally stable when $\nu \le 1/2$" — derived in Part 6.5 below from von Neumann analysis. **Status: [Derived]**.

**"a constraint that becomes prohibitive for the cm-scale near-surface layers required to resolve the diurnal damping depth in highly conductive urban substrates."**

Since $d \sim 8$–$14$ cm, $\Delta z \ll d$ requires $\Delta z \sim 0.5$–$1$ cm. Concrete and asphalt have higher $\kappa$ than soil and so push the FTCS bound to even smaller $\Delta t$.

**"This project compares three numerical treatments of the soil heat equation — FTCS, BTCS, and Crank–Nicolson — coupled to a fully prognostic surface energy balance solved by Newton iteration."**

The key word is *prognostic*: $T_s^0$ is computed by the model at every step, not prescribed externally.

**"FTCS blows up at $\Delta t = 60$ s on the concrete roof and at $\Delta t = 600$ s on the asphalt road and concrete roof"**

(The original report said "on all substrates"; the audit fix in `modified_full_report_1.docx` corrected this — bare soil at $\Delta t = 600$ s is over the bound but completes with substantial error.)

**"BTCS at $\Delta t = 600$ s over-amplifies the diurnal G amplitude by 40% on asphalt and concrete and by 20% on bare soil; CN at the same $\Delta t$ halves these errors."**

These are the headline numbers.

**"The empirical $\Delta t$-refinement ratios for BTCS and CN are both close to 10:1 between $\Delta t = 60$ s and $\Delta t = 600$ s — first-order in $\Delta t$ for both schemes — which identifies the dominant error as a first-order operator-splitting error."**

This is the project's intellectual core. CN is intrinsically second-order, so a ratio of 10 (not 100) tells us the dominant error is *not* the per-substep CN truncation; it is the operator splitting between sub-steps.

**"$\kappa_{\text{top}}$ is the dominant predictor of BTCS coarse-$\Delta t$ error ($R^2 = 0.92$ from $\kappa_{\text{top}}$ alone)."**

The same parameter that sets the FTCS stability bound is also the dominant predictor of BTCS coarse-$\Delta t$ error.

---

## Part 5. Walking through §1 Introduction

### 5.1 Why the urban heat island depends on $G$ specifically

The urban heat island (UHI) is the systematic phenomenon that cities are warmer than rural areas, especially at night. Many factors contribute (anthropogenic heat, canyon geometry, reduced evapotranspiration), but the central mechanism for the *night-time* component is **heat storage**.

During the day, urban materials — pavements, walls, roofs — absorb shortwave radiation. After sunset, $R_n$ turns negative and the stored heat is released. Rural surfaces store less. At night the urban surface is still warm while the rural one has cooled — that contrast is the nocturnal UHI.

$G$ is the very quantity that puts heat into the urban substrate during the day and pulls it back out at night. If a model gets $G$ wrong, it gets the UHI wrong.

> **[Notes #11 Misconception #3]** ("Surface conditions are accurately depicted") emphasises that surface conditions in models may be based on climatology rather than current observations and may not be well-handled within the model integration. The project addresses one specific way the surface conditions can be mis-handled: the numerical treatment of $G$ at the column-SEB interface.

### 5.2 The damping-depth values quoted in the introduction

Paragraph 11 of the report says: "$d$ is approximately 8 cm in dry soil, 14 cm in dense concrete, and 10 cm in asphalt (computed from the substrate parameters used in §3.2)." We did the calculation in Part 1.3 above.

### 5.3 What "wavenumber-dependent damping" means

Every numerical scheme can be characterised by how it changes the amplitude of each Fourier component (each wavelength) per time step. For FTCS, BTCS, CN we will derive these *amplification factors* explicitly in Part 6.5.

> **[HW2]** asked you to verify amplitude conservation on a sine-wave initial condition. **[HW4]** plotted $|A_k|$ vs $k\Delta x$ — the same kind of plot Figure 1 of the project shows, with $k\Delta z$ instead.

---

## Part 6. Walking through §2 — Governing equation and numerical discretization

### 6.1 §2.1 — Where the heat conduction equation comes from

The report writes the heat conduction equation in **conductivity form**:

$$C_s(z) \frac{\partial T_s}{\partial t} = \frac{\partial}{\partial z}\left[\lambda_s(z) \frac{\partial T_s}{\partial z}\right].$$

> **Status: [Derived]** below from Fourier's law plus energy conservation. The result is a standard textbook PDE (Bonan 2019; Hillel 2003).

Read aloud: "volumetric heat capacity times the rate of change of temperature with time equals the spatial divergence of the conductive heat flux."

**Step 1. Fourier's law of heat conduction.**

$$q(z) = -\lambda_s(z) \frac{\partial T_s}{\partial z}.$$

> **Status: [Established]** — Fourier's law (Joseph Fourier, *Théorie analytique de la chaleur*, 1822). Fundamental physical law of heat conduction.

If $T$ decreases with depth ($\partial T/\partial z < 0$), then $q > 0$ — flux in the $+z$ direction (downward). The minus sign encodes the second law of thermodynamics: heat flows from hot to cold, never the reverse.

**Step 2. Energy conservation in a thin slab.** Pick a thin horizontal slab from depth $z$ to $z + dz$. Energy stored per unit area is $C_s T_s dz$. Rate of change of stored energy = net flux into slab = $q(z) - q(z + dz)$:

$$\frac{\partial}{\partial t}(C_s T_s dz) = q(z) - q(z + dz).$$

> **Status: [Established]** — first law of thermodynamics, applied to a thin slab.

If $C_s$ is time-independent and we Taylor-expand $q(z + dz) \approx q(z) + (\partial q/\partial z) dz$:

$$C_s \frac{\partial T_s}{\partial t} dz = -\frac{\partial q}{\partial z} dz.$$

Substituting Fourier's law $q = -\lambda_s \partial T_s/\partial z$:

$$C_s \frac{\partial T_s}{\partial t} = -\frac{\partial}{\partial z}\left(-\lambda_s \frac{\partial T_s}{\partial z}\right) = \frac{\partial}{\partial z}\left(\lambda_s \frac{\partial T_s}{\partial z}\right).$$

That is the conductivity-form heat equation. It is just energy conservation written locally, with Fourier's law for the flux. **Status: [Derived]** from two established laws.

**Step 3. Why "conductivity form" instead of "diffusivity form"?** If $\lambda$ and $C$ are constant, we can pull them out of the derivative and write $\partial T/\partial t = \kappa \partial^2 T/\partial z^2$ with $\kappa = \lambda/C$. That is the diffusivity form. In our layered substrates, $\lambda$ and $C$ jump by an order of magnitude across material interfaces, so we must use the conductivity form to preserve discrete heat conservation.

**The symbols, definitively.**

- $T_s(z, t)$ — substrate temperature at depth $z$, time $t$. Units K.
- $z$ — vertical depth, $z = 0$ at surface, increasing downward. Units m.
- $t$ — time. Units s.
- $\lambda_s(z)$ — substrate thermal conductivity. Units W/m/K.
- $C_s(z)$ — volumetric heat capacity. Units J/m³/K.

### 6.2 §2.2 — The grid, the half-levels, the harmonic mean

#### Cell centres and the staggered grid

Replace continuous depth $z$ with cell centres $z_0, z_1, \ldots, z_{N-1}$. At each cell store one number: temperature $T_j$ at the centre. Between cells $j$ and $j+1$ lies a face at depth $z_{j+1/2} = (z_j + z_{j+1})/2$. **Temperatures live at centres; conductive fluxes at faces.**

This **staggered grid** is the standard finite-volume layout. Heat that leaves cell $j$ across face $j+1/2$ is the same heat that enters cell $j+1$ across the same face, so energy is conserved by construction.

> **[Notes #8]** is dedicated to staggered grids. **[HW5]** is the direct precursor: you showed empirically that on the unstaggered grid, a single point disturbance only spread to *every other* grid point, creating sub-grid decoupling. On the staggered grid, the disturbance spread smoothly to all neighbours.

#### The discrete flux equation

$$G_{j+1/2} = \lambda_{j+1/2} \frac{T_j - T_{j+1}}{z_{j+1} - z_j}.$$

> **Status: [Definition]** — this is the project's discretization of Fourier's law $q = -\lambda \partial T/\partial z$ at the half-level, using a centred difference for $\partial T/\partial z$. The minus sign in Fourier's law has been absorbed into writing $(T_j - T_{j+1})$ instead of $(T_{j+1} - T_j)$, so that $G > 0$ corresponds to downward flow.

Decoded:
- $G_{j+1/2}$ — conductive heat flux through the face between cells $j$ and $j+1$. Units W/m². Sign: $G > 0$ means downward.
- $\lambda_{j+1/2}$ — thermal conductivity at the face. Computed from the cell-centre $\lambda_j$ and $\lambda_{j+1}$ via the harmonic mean (next).
- $(T_j - T_{j+1})$ — temperature drop from cell $j$ (above) to cell $j+1$ (below).
- $(z_{j+1} - z_j)$ — centre-to-centre spacing.

#### Why the harmonic mean for $\lambda$ at faces?

Solve the steady-state conduction problem across an interface between two materials in series. The flux must be the same on both sides:

$$q = \lambda_1 \frac{\Delta T_1}{\Delta z_1} = \lambda_2 \frac{\Delta T_2}{\Delta z_2}.$$

Total drop is $\Delta T = \Delta T_1 + \Delta T_2$ over distance $\Delta z = \Delta z_1 + \Delta z_2$. From the two single-material relations: $\Delta T_1 = q \Delta z_1/\lambda_1$ and $\Delta T_2 = q \Delta z_2/\lambda_2$. Adding:

$$\Delta T = q\left(\frac{\Delta z_1}{\lambda_1} + \frac{\Delta z_2}{\lambda_2}\right) = q \frac{\Delta z}{\lambda_{\text{eff}}},$$

where the effective conductivity is

$$\lambda_{\text{eff}} = \frac{\Delta z_1 + \Delta z_2}{\Delta z_1/\lambda_1 + \Delta z_2/\lambda_2}.$$

For two cells of equal thickness this collapses to:

$$\lambda_{j+1/2} = \frac{2 \lambda_j \lambda_{j+1}}{\lambda_j + \lambda_{j+1}}.$$

> **Status: [Derived]** above from the steady-state heat-flux continuity condition. Standard convention in finite-volume codes (Patankar 1980, *Numerical Heat Transfer and Fluid Flow*).

**Worked example — concrete-roof interface.** $\lambda_1 = 1.5$ (concrete deck), $\lambda_2 = 0.04$ (insulation).

- Arithmetic mean: $(1.5 + 0.04)/2 = 0.77$. Wrong (close to concrete).
- Harmonic mean: $2 \times 1.5 \times 0.04 / (1.5 + 0.04) = 0.12 / 1.54 = 0.078$. Correct (close to insulation).

The arithmetic mean over-estimates the heat flux across this interface by a factor of about 10.

#### The semi-discrete tendency

$$C_j \Delta z_j \frac{dT_j}{dt} = G_{j-1/2} - G_{j+1/2}.$$

> **Status: [Derived]** — discretizing the conductivity-form heat equation by integrating over cell $j$. This is a direct consequence of energy conservation in the discrete cell.

The rate of energy accumulation in cell $j$ (per unit horizontal area) equals the flux entering at the top minus the flux leaving at the bottom. **Semi-discrete**: space is discretised, time is still continuous.

### 6.3 §2.3 — Building the $\theta$-method update equation

The semi-discrete equation is $C_j \Delta z_j dT_j/dt = R_j(t)$, where $R_j = G_{j-1/2} - G_{j+1/2}$. Integrate from $t^n$ to $t^{n+1}$:

$$C_j \Delta z_j (T_j^{n+1} - T_j^n) = \int_{t^n}^{t^{n+1}} R_j(t) dt.$$

Three quadrature rules give three schemes:

- **Left rectangle**: integral $\approx \Delta t R_j^n$. Gives FTCS, $\alpha = 0$.
- **Right rectangle**: integral $\approx \Delta t R_j^{n+1}$. Gives BTCS, $\alpha = 1$.
- **Trapezoid**: integral $\approx (\Delta t/2)[R_j^n + R_j^{n+1}]$. Gives CN, $\alpha = 1/2$.

In one line — the report's $\theta$-method update:

$$C_j \Delta z_j \frac{T_j^{n+1} - T_j^n}{\Delta t} = \alpha [G_{j-1/2} - G_{j+1/2}]^{n+1} + (1-\alpha) [G_{j-1/2} - G_{j+1/2}]^n.$$

> **Status: [Definition]** — the project's discretisation of the heat equation, generalising three established schemes (FTCS, BTCS, CN) into one parameterised form.

#### Why FTCS and BTCS are first-order, CN is second-order in $\Delta t$

Plug the exact integral into a Taylor expansion around the midpoint $t^n + \Delta t/2$. Let $R_m = R(t^n + \Delta t/2)$:

$$R(t^n) = R_m - \frac{\Delta t}{2} R'_m + \frac{\Delta t^2}{8} R''_m - \cdots$$

$$R(t^{n+1}) = R_m + \frac{\Delta t}{2} R'_m + \frac{\Delta t^2}{8} R''_m + \cdots$$

Average:

$$\frac{1}{2}[R(t^n) + R(t^{n+1})] = R_m + \frac{\Delta t^2}{8} R''_m + O(\Delta t^4).$$

> **Status: [Derived]** — direct from Taylor's theorem.

The $\Delta t/2 \cdot R'_m$ terms have opposite signs and cancel exactly when averaged. So the trapezoid (CN) approximates the integral as $\Delta t R_m + O(\Delta t^3)$ — leading error $O(\Delta t^3)$ in the integral, hence $O(\Delta t^2)$ in the time-derivative. **Second-order.** The single-rectangle rules keep the $\Delta t/2 \cdot R'_m$ term, so first-order.

#### Linear systems and tridiagonal solves

When $\alpha > 0$, the RHS involves $T$ values at level $n+1$. Each cell $j$ couples only to $j \pm 1$. The matrix is **tridiagonal**.

Tridiagonal systems can be solved in $O(N)$ operations using the **Thomas algorithm** — far cheaper than a generic $O(N^3)$ solver. SciPy provides `scipy.linalg.solve_banded((1,1), A, b)`.

> **Status: [Established algorithm]** (Thomas 1949). Standard workhorse for 1-D implicit diffusion.

> **[Notes #9 §Practical Considerations]** explicitly says: *"Implicit differencing leads to a system of algebraic equations with a tridiagonal matrix structure...Tridiagonal solvers are particularly efficient and well suited for vertical mixing in oceanic and atmospheric models."*

### 6.4 §2.4 — The boundary conditions

Two main types of boundary conditions:

- **Dirichlet condition** — prescribes the value of $T$ at the boundary.
- **Neumann condition** — prescribes the value of the gradient $\partial T/\partial z$ at the boundary.

> **Status: [Established]** — standard PDE boundary-condition classification (named after Dirichlet 1850s and Neumann 1880s).

#### Lower boundary: zero-flux Neumann

At $z = z_{\text{top}} = 2$ m we impose $\partial T/\partial z = 0$. At 2 m we are well below $d \approx 8$–$14$ cm — the daily wave has decayed. Discretely: $T_{N-1} = T_{N-2}$.

#### Upper boundary: Dirichlet on $T_s^0$

At cell 0 we set $T_0 = T_s^0$. In Test 1, $T_s^0(t) = \bar{T} + A\cos\omega t$ — a prescribed sinusoid. In Test 2, $T_s^0$ is the unknown solved by Newton iteration on the SEB.

### 6.5 §2.5 — Von Neumann stability analysis from scratch

#### Setup: linearise, idealise, then test

Von Neumann analysis works only for linear schemes on uniform grids with constant coefficients. Idealise: assume $\lambda$ and $C$ are constant (so $\kappa = \lambda/C$ is constant), assume $\Delta z$ is uniform, assume periodic boundaries.

#### Step 1 — Substitute a Fourier mode

Any small perturbation can be written as a sum of complex-exponential Fourier modes:

$$T_j^n = A^n e^{ikj\Delta z}.$$

> **Status: [Established technique]** — von Neumann (1947) developed this analysis at Los Alamos. Standard tool in numerical PDE theory.

The grid resolves wavenumbers $k$ from 0 (a constant in space) up to $k = \pi/\Delta z$ (the 2-$\Delta z$ wave). So we need $|A(\nu, k\Delta z)| \le 1$ for every $k\Delta z$ in $[0, \pi]$ for stability.

#### Step 2 — Plug into the FTCS update

FTCS at $\alpha = 0$ on a uniform grid with constant $\kappa$, in diffusivity form:

$$T_j^{n+1} = T_j^n + \frac{\kappa \Delta t}{\Delta z^2}[T_{j+1}^n - 2T_j^n + T_{j-1}^n].$$

Define $\nu = \kappa \Delta t/\Delta z^2$. Substitute $T_j^n = A^n e^{ikj\Delta z}$:

$$A^{n+1} e^{ikj\Delta z} = A^n e^{ikj\Delta z} + \nu A^n[e^{ik(j+1)\Delta z} - 2 e^{ikj\Delta z} + e^{ik(j-1)\Delta z}].$$

Divide both sides by $A^n e^{ikj\Delta z}$:

$$A = 1 + \nu[e^{ik\Delta z} - 2 + e^{-ik\Delta z}].$$

Use Euler's identity $e^{ix} + e^{-ix} = 2\cos x$:

$$A_{\text{FTCS}}(\nu, k\Delta z) = 1 - 2\nu(1 - \cos k\Delta z).$$

> **Status: [Derived]** above from the FTCS update by direct substitution. **Established result** [Notes #9 §Pure Diffusion]: the lecture derives this exact formula using $M$ for diffusivity, with the same $\nu = M\Delta t/\Delta x^2$ definition.

#### Step 3 — Plug into the BTCS update

BTCS at $\alpha = 1$:

$$T_j^{n+1} = T_j^n + \nu[T_{j+1}^{n+1} - 2T_j^{n+1} + T_{j-1}^{n+1}].$$

Substitute the Fourier mode:

$$A^{n+1} = A^n + \nu A^{n+1}[2\cos k\Delta z - 2].$$

Divide by $A^n$:

$$A = 1 + A\nu[2\cos k\Delta z - 2] = 1 - 2A\nu(1 - \cos k\Delta z).$$

Solve for $A$:

$$A[1 + 2\nu(1 - \cos k\Delta z)] = 1.$$

$$A_{\text{BTCS}}(\nu, k\Delta z) = \frac{1}{1 + 2\nu(1 - \cos k\Delta z)}.$$

> **Status: [Derived]** above. **Established result.**

#### Step 4 — Plug into the CN update

CN at $\alpha = 1/2$:

$$T_j^{n+1} = T_j^n + \frac{\nu}{2}[T_{j+1}^n - 2T_j^n + T_{j-1}^n] + \frac{\nu}{2}[T_{j+1}^{n+1} - 2T_j^{n+1} + T_{j-1}^{n+1}].$$

Substitute. Let $h = \nu(1 - \cos k\Delta z)$. The two bracketed groups become $-2A^n h$ and $-2A^{n+1} h$ respectively:

$$A^{n+1} = A^n - A^n h - A^{n+1} h.$$

Divide by $A^n$:

$$A = 1 - h - hA.$$

$$A(1 + h) = 1 - h.$$

$$A_{\text{CN}}(\nu, k\Delta z) = \frac{1 - h}{1 + h} = \frac{1 - \nu(1 - \cos k\Delta z)}{1 + \nu(1 - \cos k\Delta z)}.$$

> **Status: [Derived]** above. **Established result** [Notes #9 §Implicit Diffusion]: the lecture derives this same formula and labels it "the Crank–Nicolson method".

#### What $|A| \le 1$ means

After one time step, the Fourier mode at wavenumber $k$ has amplitude $A$. After $n$ time steps, amplitude is $A^n$. If $|A| > 1$, the mode grows exponentially. If $|A| \le 1$, the mode either holds steady or decays.

#### Why $k\Delta z = \pi$ is the worst case

For all three amplification factors, the dependence on $k\Delta z$ is through the factor $(1 - \cos k\Delta z)$:
- Equals 0 at $k\Delta z = 0$ (since $\cos 0 = 1$).
- Equals 2 at $k\Delta z = \pi$ (since $\cos\pi = -1$).
- Is monotonically increasing on $[0, \pi]$.

So whichever wavenumber pushes $A$ farthest from 1 in magnitude is at $k\Delta z = \pi$, the **2-$\Delta z$ wave**. Substituting:

$$A_{\text{FTCS}}(\nu, \pi) = 1 - 4\nu.$$

$$A_{\text{BTCS}}(\nu, \pi) = \frac{1}{1 + 4\nu}.$$

$$A_{\text{CN}}(\nu, \pi) = \frac{1 - 2\nu}{1 + 2\nu}.$$

> **Status: [Derived]** by setting $k\Delta z = \pi$ in the three preceding equations.

#### Reading the stability conclusions

**FTCS** at the worst wave: $A = 1 - 4\nu$. For $|A| \le 1$ we need $-1 \le 1 - 4\nu \le 1$. Upper bound automatic (since $\nu \ge 0$). Lower: $1 - 4\nu \ge -1$ requires $\nu \le 1/2$. So **FTCS is conditionally stable** with bound

$$\nu \le \frac{1}{2}, \quad \text{i.e.} \quad \Delta t \le \frac{1}{2}\frac{\Delta z^2}{\kappa}.$$

> **Status: [Derived]** — well-known FTCS stability bound for the diffusion equation.

**BTCS** at the worst wave: $A = 1/(1 + 4\nu)$. For $\nu > 0$ this is automatically between 0 and 1. So $|A| < 1$ always — **BTCS is unconditionally stable**, and *strictly damping*. **Status: [Derived]**.

**CN** at the worst wave: $A = (1 - 2\nu)/(1 + 2\nu)$. $|1 - 2\nu| \le |1 + 2\nu|$ always, so $|A| \le 1$ always — **CN is unconditionally stable**. As $\nu \to \infty$, $A \to -1$. So at very large $\nu$, the worst wave is preserved in magnitude but flips sign every step (the *over-damping pathology of CN at large $\nu$*). **Status: [Derived]**.

> **[HW4]** is the direct ancestor: you plotted $|A_k|$ against $k\Delta x$ for various CFL numbers $\mu$ for an advection scheme. The project applies the same logical structure to a parabolic equation, with the worst case at $k\Delta z = \pi$ instead of $\pi/2$.

### 6.6 Reading Figure 1 panel by panel

Figure 1 has three panels — FTCS, BTCS, CN — each plotting $|A_k|$ vs $k\Delta z$ for four values of $\nu$.

#### The axes

- The $x$-axis is $k\Delta z$, ranging from 0 to $\pi$. This is the dimensionless wavenumber.
- The $y$-axis is $|A_k(\nu, k\Delta z)|$, the magnitude of the amplification factor. We plot $|A|$ because the actual $A$ can be negative, but stability cares only about magnitude. A horizontal dashed line at $|A| = 1$ marks the stability bound.

#### The four $\nu$ values

$\nu = 0.25, 0.5, 1.0, 5.0$.

#### FTCS panel

**Worked example — FTCS at the four $\nu$ values, evaluated at $k\Delta z = \pi$.**

- $\nu = 0.25$: $A = 1 - 4(0.25) = 0$, so $|A| = 0$. Stable.
- $\nu = 0.5$: $A = 1 - 4(0.5) = -1$, so $|A| = 1$. Marginal stability — exactly on the bound at the 2-$\Delta z$ wave.
- $\nu = 1.0$: $A = 1 - 4(1) = -3$, so $|A| = 3$. **Unstable** — amplifies the worst wave by 3 per step.
- $\nu = 5.0$: $A = 1 - 4(5) = -19$, so $|A| = 19$. Massively unstable.

#### BTCS panel

**Worked example — BTCS at the same four $\nu$ values, at $k\Delta z = \pi$.**

- $\nu = 0.25$: $A = 1/(1 + 1) = 0.5$.
- $\nu = 0.5$: $A = 1/(1 + 2) = 0.333$.
- $\nu = 1.0$: $A = 1/(1 + 4) = 0.2$.
- $\nu = 5.0$: $A = 1/(1 + 20) = 0.0476$. Worst wave damped to near-nothing in a single step.

All four values are well below 1.

#### CN panel

**Worked example — CN at the same four $\nu$ values, at $k\Delta z = \pi$.**

- $\nu = 0.25$: $A = (1 - 0.5)/(1 + 0.5) = 1/3$.
- $\nu = 0.5$: $A = (1 - 1)/(1 + 1) = 0$. **The worst wave is exactly killed in one step at $\nu = 1/2$**.
- $\nu = 1.0$: $A = (1 - 2)/(1 + 2) = -1/3$. $|A| = 1/3$.
- $\nu = 5.0$: $A = (1 - 10)/(1 + 10) = -9/11 \approx -0.818$. $|A| \approx 0.818$.

The $\nu = 5$ curve is below 1 but only barely at $k\Delta z = \pi$.

#### Why we have CN at all, given the weak-damping pathology

At the resolved scales (small $k\Delta z$), CN is *much more accurate per step* than BTCS — second-order vs first-order. The price is poorer damping of unresolved noise.

---

## Part 7. Walking through §3 — Methods

### 7.1 §3.1 — What "parameterised by $\alpha$" means in code

One Python function `step_alpha(T, dt, ..., alpha, ...)` takes $\alpha$ as an argument. When $\alpha = 0$: vectorised arithmetic update. When $\alpha > 0$: tridiagonal solve. Any bug in the spatial discretisation affects all three schemes equally.

### 7.2 §3.2 — Substrate definitions

Three substrate columns, each 2 m deep:

**Asphalt road** (4 layers):
- Asphalt 0–5 cm: $\lambda = 0.75$, $C = 2.0\times 10^6$.
- Aggregate 5–25 cm: $\lambda = 1.40$, $C = 2.4\times 10^6$.
- Dry soil 25–100 cm: $\lambda = 0.30$, $C = 1.3\times 10^6$.
- Subsoil 100–200 cm: $\lambda = 0.50$, $C = 1.8\times 10^6$.

**Concrete roof** (3 layers):
- Concrete deck 0–10 cm: $\lambda = 1.50$, $C = 2.1\times 10^6$.
- Mineral-wool insulation 10–20 cm: $\lambda = 0.04$, $C = 0.08\times 10^6$.
- Drywall/wood interior 20–200 cm: $\lambda = 0.15$, $C = 1.5\times 10^6$.

**Bare soil** (uniform): $\lambda = 0.30$, $C = 1.3\times 10^6$ throughout.

> **Status: [Project-specific definitions]** — these layer specifications are choices made by the author to span a wide range of substrate behaviours. Material values are drawn from textbook references (Oke 1987 Table A2; ASHRAE handbook).

### 7.3 §3.3 — The surface energy balance and Newton iteration

#### The SEB

$$R_n(T_s^0) - H(T_s^0) - LE(T_s^0) - G(T_s^0) = 0.$$

> **Status: [Established]** — first law of thermodynamics applied at the surface.

Components:

$$R_n = (1 - \alpha_s) S_\downarrow + \varepsilon_s L_\downarrow - \varepsilon_s \sigma (T_s^0)^4.$$

> **Status: [Established]** — net radiation as the sum of three established terms:
> - $(1 - \alpha_s) S_\downarrow$ — absorbed shortwave (Lambert–Beer reflection law).
> - $\varepsilon_s L_\downarrow$ — absorbed longwave (Kirchhoff's law: emissivity = absorptivity).
> - $-\varepsilon_s \sigma (T_s^0)^4$ — Stefan–Boltzmann emission (Stefan 1879, Boltzmann 1884).

The $(T_s^0)^4$ Stefan–Boltzmann term is what makes the SEB nonlinear in $T_s^0$.

$$H = \rho c_p \frac{T_s^0 - T_a}{r_a}, \qquad r_a = \frac{1}{C_H U}.$$

> **Status: [Established]** — bulk-aerodynamic formula for sensible heat (standard surface-layer parameterization, Garratt 1992 §3.3). $r_a$ is the aerodynamic resistance, defined as $1/(C_H U)$. **Status of $r_a$: [Definition]**.

- $\rho \approx 1.2$ kg/m³ — air density.
- $c_p = 1005$ J/kg/K — specific heat of air at constant pressure.
- $T_a$ — 2-metre air temperature (K).
- $C_H = 5\times 10^{-3}$ — bulk transfer coefficient.
- $U = 3$ m/s — wind speed.

$$LE = 0 \quad (\text{strict-impervious assumption}).$$

> **Status: [Project-specific assumption]** — chosen for methodological cleanness. Real cities have $LE > 0$.

$$G = \lambda_{1/2} \frac{T_s^0 - T_1}{z_1 - z_0} \quad (\text{ground heat flux at the top half-level}).$$

> **Status: [Definition]** — same discrete flux formula as in §6.2, evaluated at the top half-level with $T_0 = T_s^0$.

#### Newton's method derived from the linear approximation

Start with a guess $T_{s,\text{old}}^0$. Approximate $F$ linearly around that point:

$$F(T) \approx F(T_{s,\text{old}}^0) + F'(T_{s,\text{old}}^0) (T - T_{s,\text{old}}^0).$$

> **Status: [Derived]** — first-order Taylor expansion.

Set this approximation to zero and solve for $T$:

$$T_{s,\text{new}}^0 = T_{s,\text{old}}^0 - \frac{F(T_{s,\text{old}}^0)}{F'(T_{s,\text{old}}^0)}.$$

> **Status: [Established]** — Newton's method (Newton 1669, Raphson 1690). Iterate until $|T_{s,\text{new}}^0 - T_{s,\text{old}}^0| < 10^{-4}$ K.

Newton's method has **quadratic convergence near the root**: digits roughly double per iteration. From a warm start (previous time step's $T_s^0$), 3–5 iterations suffice.

#### The full analytical Jacobian

$$\frac{dF}{dT_s} = \frac{dR_n}{dT_s} - \frac{dH}{dT_s} - \frac{dG}{dT_s}.$$

Term by term:

$$\frac{dR_n}{dT_s} = -4 \varepsilon_s \sigma (T_s^0)^3.$$

> **Status: [Derived]** by differentiating the Stefan–Boltzmann term. The factor 4 comes from the chain rule on $T^4$.

$$\frac{dH}{dT_s} = \frac{\rho c_p}{r_a}.$$

> **Status: [Derived]** by differentiating $H$ with respect to $T_s^0$.

$$\frac{dG}{dT_s} = \frac{\lambda_{1/2}}{z_1 - z_0}.$$

> **Status: [Derived]** by differentiating the discrete $G$ formula.

All three are smooth functions of $T_s^0$. The analytical Jacobian gives full Newton convergence; a finite-difference Jacobian would introduce noise.

### 7.4 §3.4 — The synthetic forcing

With $\omega = 2\pi/86400$ rad/s:

$$S_\downarrow(t) = \max[1000 \cos(\omega(t - 12 \mathrm{h})), 0]\ \text{W/m}^2.$$

(Peak at noon, zero at night.)

$$L_\downarrow(t) = 350 + 20\cos(\omega(t - 14 \mathrm{h}))\ \text{W/m}^2.$$

(Peak at 14:00 LT.)

$$T_a(t) = 292.5 + 7.5\cos(\omega(t - 14 \mathrm{h}))\ \text{K}.$$

(Peak at 14:00 LT.)

$$U(t) = 3\ \text{m/s} \quad (\text{constant}).$$

> **Status: [Project-specific definitions]** — synthetic forcing chosen to be smooth and reproducible, with realistic amplitudes and a 2-hour lag for $T_a$ and $L_\downarrow$ (real urban surface-layer behaviour).

### 7.5 §3.5 — Initialization

$$T(z, 0) = T_{\text{mean}} + A_0 e^{-z/d_{\text{top}}} \cos(-z/d_{\text{top}}), \qquad d_{\text{top}} = \sqrt{\frac{2 \kappa_{\text{top}}}{\omega}}.$$

> **Status: [Established theoretical formula]** — analytical damping-depth solution from Carslaw & Jaeger 1959 §2.6, evaluated at $t = 0$. Re-derived in Part 8.1 below.

With $T_{\text{mean}} = 292.5$ K, $A_0 = 7.5$ K, $\kappa_{\text{top}} = \lambda_{\text{top}}/C_{\text{top}}$ from the topmost layer.

There is a 12-hour phase mismatch: this initial profile assumes the surface is at peak temperature at $t = 0$, but the SEB-driven cycle peaks at 14:00 LT. So the column carries a transient that decays during day 1.

### 7.6 §3.6 — Test 1 vs Test 2 setups

**Test 1 (verification):** uniform sandy-loam column, 1 cm grid, $T_s^0(t) = T_{\text{mean}} + A_0\cos(\omega t)$ prescribed. Six configurations.

**Test 2 (prognostic SEB):** three substrates × three schemes × three time steps $\Delta t \in \{15, 60, 600\}$ s = 27 cells.

---

## Part 8. Walking through §4 — Results

### 8.1 §4.1 — The damping-depth verification

#### The analytical solution and the $\pi/4$ phase lead — derived

For a semi-infinite uniform substrate with sinusoidal Dirichlet forcing $T_s(0, t) = \bar{T} + A\cos\omega t$, we want to solve

$$\frac{\partial T}{\partial t} = \kappa \frac{\partial^2 T}{\partial z^2}, \qquad T(0, t) = \bar{T} + A\cos\omega t, \qquad T \to \bar{T} \text{ as } z \to \infty.$$

> **Status: [Established theoretical problem]** — the canonical "buried sinusoid" problem in conduction theory. Solution is in Carslaw & Jaeger 1959 §2.6.

**Ansatz.** Try the complex form

$$T(z, t) = \bar{T} + \mathrm{Re}[A e^{i(\omega t - Kz)}],$$

where $K$ is a complex wavenumber to be determined. Substituting into the PDE:

$$i\omega A e^{i(\omega t - Kz)} = \kappa (-K^2) A e^{i(\omega t - Kz)}.$$

Cancel the common factor:

$$i\omega = -\kappa K^2 \quad \Rightarrow \quad K^2 = -\frac{i\omega}{\kappa}.$$

> **Status: [Derived]** — direct substitution.

Take the square root. Recall $\sqrt{-i} = (1 - i)/\sqrt{2}$. So

$$K = \pm\frac{1 - i}{\sqrt{2}}\sqrt{\omega/\kappa}.$$

We take the root that gives decay as $z \to \infty$. With $K = (1-i)/\sqrt{2} \cdot \sqrt{\omega/\kappa}$, the imaginary part of $K$ is negative, so $e^{-iKz} = e^{-i \mathrm{Re}(K) z} e^{\mathrm{Im}(K) z}$ decays. So

$$K = \frac{1 - i}{\sqrt{2}}\sqrt{\omega/\kappa} = \frac{1 - i}{d}, \qquad d = \sqrt{\frac{2\kappa}{\omega}}.$$

Now compute $-iKz$:

$$-iKz = -i (1-i) \frac{z}{d}.$$

Use $-i(1 - i) = -i + i^2 = -i - 1 = -(1 + i)$:

$$-iKz = -\frac{(1 + i) z}{d} = -\frac{z}{d} - i\frac{z}{d}.$$

So

$$e^{i(\omega t - Kz)} = e^{i\omega t} e^{-iKz} = e^{i\omega t} e^{-z/d} e^{-iz/d} = e^{-z/d} e^{i(\omega t - z/d)}.$$

Take the real part:

$$T_s(z, t) = \bar{T} + A e^{-z/d} \cos(\omega t - z/d), \qquad d = \sqrt{2\kappa/\omega}.$$

> **Status: [Derived]** above by complex-exponential ansatz. **Established result** (Carslaw & Jaeger 1959 §2.6).

The temperature wave has two effects with depth: amplitude decays exponentially with characteristic length $d$; phase lags linearly with depth, with $z/d$ radians of lag per unit damping depth.

**Surface flux.** $G(0, t) = -\lambda \partial T/\partial z$ evaluated at $z = 0$. Compute the derivative:

$$\frac{\partial T}{\partial z} = A e^{-z/d}\left[-\frac{1}{d}\cos(\omega t - z/d) + \frac{1}{d}\sin(\omega t - z/d)\right].$$

> **Status: [Derived]** — chain-rule differentiation of $T_s(z,t)$.

At $z = 0$, $e^{-z/d} = 1$:

$$\left.\frac{\partial T}{\partial z}\right|_{z=0} = \frac{A}{d}[-\cos\omega t + \sin\omega t].$$

Therefore

$$G(0, t) = -\lambda \frac{A}{d}[-\cos\omega t + \sin\omega t] = \lambda \frac{A}{d}[\cos\omega t - \sin\omega t].$$

Use the trigonometric identity $\cos x - \sin x = \sqrt{2}\cos(x + \pi/4)$ (verify: $\sqrt{2}\cos(x + \pi/4) = \sqrt{2}[\cos x \cos(\pi/4) - \sin x \sin(\pi/4)] = \cos x - \sin x$ since $\cos(\pi/4) = \sin(\pi/4) = 1/\sqrt{2}$). So

$$G(0, t) = \lambda \frac{A}{d} \sqrt{2} \cos(\omega t + \pi/4).$$

> **Status: [Derived]** above. **Established result.**

**Physical meaning of the $\pi/4$ lead.** $G$ peaks $\pi/4$ in phase before $T_s$ peaks. For a 24-hour period, $\pi/4$ of 24 h = 3 hours. So if $T_s$ peaks at noon, $G$ peaks at 9 AM — the substrate is absorbing heat fastest in mid-morning, when the surface is still warming most rapidly.

#### Reading Table 1

Six configurations on uniform sandy loam ($\kappa = 2.31\times 10^{-7}$, $\Delta z = 1$ cm), day-5 errors at $z = 10$ cm:

| Configuration | $\Delta t$ (s) | $\nu$ | RMSE $T$ (K) | RMSE $G$ (W/m²) |
|---|---|---|---|---|
| FTCS, $\nu = 0.4$ | 173.4 | 0.40 | 0.007 | 3.15 |
| FTCS, $\nu = 0.6$ (unstable) | 259.9 | 0.60 | BLEW UP at step 53 | — |
| BTCS, $\Delta t = 300$ | 300.0 | 0.69 | 0.024 | 3.31 |
| CN, $\Delta t = 300$ | 300.0 | 0.69 | 0.005 | 3.17 |
| BTCS, $\Delta t = 900$ | 900.0 | 2.08 | 0.062 | 3.61 |
| CN, $\Delta t = 900$ | 900.0 | 2.08 | 0.006 | 3.17 |

- FTCS at $\nu = 0.6$: blew up at step 53. Predicted growth $|A_{\text{FTCS}}(0.6, \pi)| = |1 - 4(0.6)| = 1.4$ per step. After 53 steps: $1.4^{53} \approx 5.5\times 10^7$ — overflow.
- BTCS error grows roughly linearly with $\Delta t$. First-order behaviour as expected.
- CN error stays flat. **Empirical demonstration of CN's second-order accuracy**.
- RMSE of $G$ is about 3 W/m² for all stable schemes — a **spatial-discretisation residual**: the analytical $G$ uses the exact derivative $\partial T/\partial z|_0$, while the numerical version uses $(T_0 - T_1)/\Delta z$.

### 8.2 §4.2 — Three-substrate prognostic SEB results

#### Reading Figure 3 — schemes agree at $\Delta t = 15$ s

Day-2 surface temperature evolution at $\Delta t = 15$ s for all three schemes on each substrate. The three curves overlay to within line thickness on every substrate.

The peak surface temperatures:

| Substrate | Peak $T_s^0$ | Time of peak |
|---|---|---|
| Asphalt road | 50 °C | 13:00 |
| Concrete roof | 45 °C | 13:45 |
| Bare soil | 51 °C | 12:45 |

**Why bare soil is hottest.** Bare soil has the lowest $\kappa$ ($2.31\times 10^{-7}$) — heat cannot diffuse downward fast enough. Combined with $LE = 0$, absorbed energy concentrates at the surface and pushes $T_s^0$ higher.

#### Reading Figure 4 — schemes diverge at $\Delta t = 600$ s

- FTCS at $\Delta t = 600$ s blows up on asphalt and concrete roof.
- BTCS at $\Delta t = 600$ s overshoots the daytime $G$ peak by about 40% on asphalt and roof, 19% on bare soil.
- CN at $\Delta t = 600$ s overshoots by about 21% on asphalt, 26% on roof, 10% on soil.

**Why FTCS is stable on bare soil but not paved at $\Delta t = 600$ s.** Soil top cell has $\Delta z = 1$ cm and $\kappa = 2.31\times 10^{-7}$, so $\Delta t_{\text{crit}} \approx 217$ s. At $\Delta t = 600$ s, $\nu \approx 1.4$ — over the bound, but only modestly. The smooth initial profile and smooth Dirichlet boundary do not strongly excite the worst 2-$\Delta z$ wave, so the actual growth is much less than the worst-case bound.

#### Reading Figure 5 — vertical profiles in the asphalt column

- 06:00 (steady cooling phase): all schemes agree closely.
- 12:00 (peak heating phase): BTCS and CN are slightly warmer than reference near the surface.
- 18:00 (immediately after sunset): largest divergence. BTCS at $\Delta t = 600$ s holds the surface about 2 K above the reference.

### 8.3 §4.3 — The cross-substrate quantitative summary (Table 2)

Table 2 has nine rows (3 substrates × 3 schemes), each cell triple is $A_G/A_{\text{ref}}$ / RMSE of $T_s$ / $S/S_{\text{ref}}$.

Three patterns:
1. **Substrate ordering at $\Delta t = 600$ s.** RMSE largest for concrete roof (3.69 K BTCS), middle for asphalt (2.10 K BTCS), smallest for bare soil (0.53 K BTCS). Error scales with $\kappa_{\text{top}}$.
2. **Scheme ordering.** CN errors are roughly half of BTCS errors at fixed $\Delta t$.
3. **Storage preservation.** $S/S_{\text{ref}}$ stays within 5% of unity. Over-amplification is symmetric in day/night.

---

## Part 9. Walking through §5 — Discussion

### 9.1 §5.1 — Why FTCS stability is set by the most thermally stiff layer

| Substrate | Stiffest cell | $\Delta z$ | $\kappa$ | $\Delta t_{\text{crit}}$ |
|---|---|---|---|---|
| Asphalt road | top asphalt cell | 0.5 cm | $3.75\times 10^{-7}$ | 33 s |
| Concrete roof | concrete deck top cell | 0.5 cm | $7.14\times 10^{-7}$ | 17 s |
| Bare soil | top sandy-loam cell | 1.0 cm | $2.31\times 10^{-7}$ | 217 s |

Notice: the most diffusive substrate (concrete) is the most restrictive, not the least. The phrase "thermally stiff" describes the property: a stiff equation is one where the time-step constraint is set by the *fastest-evolving component*.

> **[Notes #11 Misconception #1]** says: *"High Resolution Fixes Everything — Reality: Not so!"*. The project's result: high resolution forces you to give up explicit time stepping.

### 9.2 §5.2 — The operator-splitting error, derived

The amplitude inflation of $G$ at large $\Delta t$ is **not** explained by the von Neumann picture. The real explanation is **operator splitting** between the column update and the SEB update.

#### How the splitting works

Each time step has two sub-steps:
- **Sub-step A — column update.** Hold $T_s^0$ fixed. Solve the heat conduction equation in the column for one $\Delta t$. New interior temperatures.
- **Sub-step B — SEB update.** With new interior values fixed, solve the SEB by Newton iteration for the new $T_s^0$.

During sub-step A the column relaxed to equilibrium with start-of-step $T_s^0$. In sub-step B the SEB jerks $T_s^0$ to its new value — but the column does not re-respond within the same step.

#### Why this produces over-amplification

Consider sunset. $T_s^0$ drops fast — say from 35 °C to 25 °C in $\Delta t = 600$ s. Sub-step A holds $T_s^0$ at 35 and the column relaxes to that. Sub-step B computes new $T_s^0 = 25$. But the column is still equilibrated to 35. The gradient at the top half-level is steeper than the true coupled solution would have. $G$ is correspondingly larger.

BTCS evaluates the diffusion operator entirely at the post-swing temperature. CN evaluates half-old, half-new, so half the swing is cancelled.

> **[Notes #10 §8 — The Order of the Processes]** says: *"Implicit scheme brings the local profiles into equilibrium, but without accounting for the other tendencies it can be the wrong equilibrium."* And: *"Without including the dynamic tendencies in the implicit computation of the diffusion, the diffusion scheme will relax toward the wrong equilibrium for long time steps."* This is exactly the project's column-first-then-SEB pathology.

#### Why both BTCS and CN show first-order scaling

The operator-splitting error is first-order in $\Delta t$ regardless of the per-substep scheme: gradient error scales linearly with how far $T_s^0$ has swung between updates. The expected first-order ratio between $\Delta t = 60$ s and $\Delta t = 600$ s is $600/60 = 10$. Empirical ratios cluster around 10.

#### Reading Table 3

| Surface | Scheme | RMSE at 60 s | RMSE at 600 s | Ratio |
|---|---|---|---|---|
| Asphalt | BTCS | 0.225 | 2.104 | 9.4 |
| Asphalt | CN | 0.114 | 1.115 | 9.8 |
| Roof | BTCS | 0.450 | 3.686 | 8.2 |
| Roof | CN | 0.229 | 2.102 | 9.2 |
| Soil | BTCS | 0.053 | 0.529 | 9.9 |
| Soil | CN | 0.027 | 0.279 | 10.2 |

All ratios in $[8.2, 10.2]$ — first-order. Smoking-gun evidence that operator splitting dominates.

### 9.3 §5.3 — Why $\kappa_{\text{top}}$ dominates substrate dependence

If admittance $\mu = \sqrt{\lambda C}$ alone explained the substrate ordering, asphalt:roof error ratio would be about $1:1.5$. Empirically it is $1:1.75$. Bare soil with $\mu \approx 624$ — about half of asphalt — has scheme error one *quarter* of asphalt's. So admittance alone does not explain it.

§6 SHAP attribution identifies $\kappa_{\text{top}}$ as the dominant predictor: 92% of variance from $\kappa_{\text{top}}$ alone.

### 9.4 §5.4 — Implications, limitations, outlook

#### UHI implication: diurnal range bias, not mean bias

Storage ratios within 5% confirm symmetric over-amplification. The simulated nocturnal warming is larger than reality, and the simulated dawn-time cooling is sharper.

#### The four numbered limitations

1. $LE = 0$ — strict-impervious.
2. Symmetric synthetic forcing.
3. Independent columns.
4. Constant $U = 3$ m/s.

#### Strang splitting — derivation

**Option A: Fully coupled SEB-row solve.** Augment the tridiagonal column system with one extra row representing the SEB residual. **Status: [Established technique]** — standard approach in stiff ODE solvers.

**Option B: Strang splitting.** A symmetric reorganisation. Replace the standard column-then-SEB ordering A–B at full $\Delta t$ with the symmetric sandwich

$$\mathrm{A}(\Delta t/2) \to \mathrm{B}(\Delta t) \to \mathrm{A}(\Delta t/2).$$

> **Status: [Established technique]** — Strang (1968). Standard symmetric operator splitting.

Why this works: let $\mathrm{A}$ be the operator that advances the column and $\mathrm{B}$ the operator that advances the SEB. The standard split approximates

$$e^{(\mathrm{A}+\mathrm{B})\Delta t} \approx e^{\mathrm{B}\Delta t} e^{\mathrm{A}\Delta t},$$

with leading error proportional to the commutator $[\mathrm{A}, \mathrm{B}]\Delta t^2/2$ — first-order in $\Delta t$. The symmetric Strang form approximates

$$e^{(\mathrm{A}+\mathrm{B})\Delta t} \approx e^{\mathrm{A}\Delta t/2} e^{\mathrm{B}\Delta t} e^{\mathrm{A}\Delta t/2},$$

with the symmetry cancelling the leading commutator term and leaving the next-order $O(\Delta t^3)$ error — second-order in $\Delta t$ for the splitting itself.

> **Status: [Derived]** above using the Baker–Campbell–Hausdorff formula. The cancellation of the leading commutator is exactly the same trick that makes the trapezoidal rule second-order vs forward Euler first-order.

---

## Part 10. Walking through §6 — Independent SHAP attribution

### 10.1 What problem §6 is solving

The mechanistic argument of §5 ranks $\kappa_{\text{top}}$, admittance $\mu$, and layer-interface descriptors as candidate predictors of BTCS coarse-$\Delta t$ error. The three idealised substrates differ in *all three* properties simultaneously, so they cannot disentangle which is dominant. §6 fixes this by sampling 150 random columns and using machine learning to identify the dominant predictor.

### 10.2 §6.1 — The synthetic ensemble

150 three-layer substrate columns sampled from a wide prior on $\lambda$, $C$, and layer thicknesses. Each column run at BTCS $\Delta t = 600$ s and at a BTCS reference at $\Delta t = 15$ s. Day-2 surface-temperature RMSE is the target $y$.

Six substrate descriptors are used as features:
- Bulk admittance $\mu_{\text{eff}} = \sqrt{\lambda_{\text{eff}} C_{\text{eff}}}$, depth-weighted over the top 30 cm.
- Top-cell thermal diffusivity $\kappa_{\text{top}} = \lambda_{\text{top}}/C_{\text{top}}$.
- Maximum $\lambda$ contrast across any internal interface.
- Number of significant internal interfaces.
- Depth of the first significant interface.
- Top-layer thickness $h_{\text{top}}$.

> **Status: [Project-specific definitions]** — these features are chosen by the author to characterise candidate physical mechanisms.

### 10.3 §6.2 — Gradient-boosted regression and SHAP

#### Gradient boosting

A machine-learning regression method that builds an ensemble of small decision trees, each correcting the residuals of the previous one:

$$\hat{y}_m(x) = \hat{y}_{m-1}(x) + \eta \mathrm{tree}_m(x).$$

Final prediction:

$$\hat{y}_M(x) = \hat{y}_0 + \sum_{m=1}^{M} \eta \mathrm{tree}_m(x).$$

> **Status: [Established algorithm]** — Friedman (2001). Project uses $M = 200$, max depth 3, $\eta = 0.05$.

#### SHAP

**SHAP** (SHapley Additive exPlanations) is a method for assigning each feature a fair contribution to each prediction, based on cooperative game theory.

> **Status: [Established]** — Shapley (1953) for the cooperative-game-theoretic foundation; Lundberg & Lee (2017) for the ML application.

The math comes from Shapley's uniqueness theorem: there is exactly one allocation rule satisfying four reasonable axioms simultaneously. The four axioms:

1. **Efficiency**: the sum of each feature's contribution equals the difference between the prediction and the baseline.
2. **Symmetry**: if two features are interchangeable, they get the same contribution.
3. **Dummy / Null player**: a feature that contributes nothing gets contribution zero.
4. **Additivity**: contributions from a sum of two models are the sum of contributions to each.

For each prediction $\hat{y}(x)$ and each feature $f$, SHAP computes a value $\phi_f(x)$ such that

$$\hat{y}(x) = \text{baseline} + \sum_{f} \phi_f(x).$$

Mean absolute SHAP $\overline{|\phi_f|}$ gives a global feature-importance ranking.

#### Model fit metrics

- In-sample $R^2 = 0.96$.
- 5-fold cross-validated $R^2 = 0.61$.

In **k-fold cross-validation**, the dataset is split into $k$ groups (here $k = 5$). The model is trained on $k-1$ groups and evaluated on the held-out group; this is repeated $k$ times. **Status: [Established]** — standard ML practice.

### 10.4 §6.3 — The findings

Figure 6 has four panels. **Panel (a)**: Mean $|\mathrm{SHAP}|$ values. $\kappa_{\text{top}}$ tallest at 0.71 K. $\mu_{\text{eff}}$ and max $\lambda$-contrast tied at 0.18–0.20 K. **Panel (b)**: SHAP dependence on $\kappa_{\text{top}}$, monotone positive. **Panel (c)**: residual SHAP after $\kappa_{\text{top}}$ partialled out — $\mu_{\text{eff}}$ dominates. **Panel (d)**: predicted vs observed RMSE, tight 1:1.

#### Why $\kappa_{\text{top}}$? The mechanistic connection

The same $\kappa_{\text{top}}$ that sets the FTCS stability bound also sets the prefactor of the BTCS coarse-$\Delta t$ operator-splitting error. Higher $\kappa_{\text{top}}$ → top cell relaxes to $T_s^0$ faster within sub-step A → larger gradient swing between sub-steps → larger splitting error.

### 10.5 §6.4 — Limitations of the attribution

- Fixed grid ($\Delta z_{\text{top}} = 0.5$ cm).
- Sample size 150 — small for ML; CV $R^2 = 0.61$.
- Forcing-specific (synthetic SEB, $LE = 0$).

---

## Part 11. Walking through §7 — Conclusions

The conclusions section is a five-bullet recap.

**(i) FTCS conditional stability**, $\nu \le 1/2$. On a stretched-grid layered substrate the bound is set by the most thermally stiff layer.

**(ii) BTCS and CN unconditionally stable.** At $\Delta t = 600$ s, BTCS over-amplifies by 40% on asphalt, 41% on roof, 19% on soil. CN halves these.

**(iii) Empirical $\Delta t$-refinement ratios for both BTCS and CN are close to 10:1** — first-order in $\Delta t$. Identifies the dominant error as operator splitting.

**(iv) The daily storage integral $\int G dt$ is preserved across schemes within 5%.**

**(v) Dominant predictor of BTCS coarse-$\Delta t$ error is $\kappa_{\text{top}}$**, identified by SHAP attribution. $\kappa_{\text{top}}$ alone explains 92% of the variance.

**Closing.** Two follow-ups: fully coupled SEB-row solve, or Strang splitting. Outlook: WRF-SLUCM or WRF-TEB on a real city.

---

## Part 12. Mastery cheat-sheet

### 12.1 The single most important sentence

*"The dominant error in BTCS at $\Delta t = 600$ s is not the within-substep truncation error; it is the operator-splitting error between the column update and the SEB update, which is first-order in $\Delta t$ regardless of the per-substep scheme."*

### 12.2 The three numbers to memorise

1. $\Delta t_{\text{crit}} = 17$ s for the concrete deck top cell.
2. BTCS over-amplifies the diurnal $G$ amplitude by 40% on asphalt at $\Delta t = 600$ s.
3. $\kappa_{\text{top}}$ alone explains $R^2 = 0.92$ of the BTCS coarse-$\Delta t$ error variance.

### 12.3 The five concepts you must define on demand

- **Diurnal damping depth** $d = \sqrt{2\kappa/\omega}$. **[Established]**.
- **Diffusion number** $\nu = \kappa \Delta t/\Delta z^2$. **[Definition]**. FTCS bound $\nu \le 1/2$ is **[Derived]** from von Neumann analysis.
- **Harmonic mean conductivity** $\lambda_{j+1/2} = 2\lambda_j\lambda_{j+1}/(\lambda_j+\lambda_{j+1})$. **[Derived]** from steady-state interface analysis.
- **Operator splitting / wrong-equilibrium pathology**. **[Established concept]** [Notes #10 §8].
- **SHAP value**. **[Established]** (Shapley 1953; Lundberg & Lee 2017).

### 12.4 Common follow-up questions and the right answers

**Q: Why CN over BTCS?** A: CN is second-order in time intrinsically and cuts the BTCS coarse-$\Delta t$ error in half. The remaining error is operator splitting, which both share.

**Q: Why does FTCS work on bare soil at $\Delta t = 600$ s but not on asphalt?** A: $\nu \approx 1.4$ on soil (over the bound, but smooth forcing keeps the unstable mode small) versus $\nu \approx 18$ on asphalt.

**Q: Why is bare soil error a quarter of asphalt error, not half?** A: Operator-splitting error scales with $\kappa_{\text{top}}$, not admittance.

**Q: Why don't you just remove operator splitting?** A: Fully coupled SEB-row solve or Strang splitting. Within the project we wanted to *characterise* the error, not eliminate it.

### 12.5 Lecture-notes index

| Project section | Lecture-note source |
|---|---|
| §1 motivation, UHI | [Notes #11 Misconception #3] |
| §2.1 conductivity-form heat equation | [Notes #2 Parabolic class] |
| §2.2 staggered grid, half-levels | [Notes #8] Staggered Grid |
| §2.3 $\theta$-method (FTCS, BTCS, CN) | [Notes #6 §6 Slides 15–17] |
| §2.5 von Neumann analysis | [Notes #6 §10] + [Notes #9 Pure Diffusion / Implicit Diffusion] |
| §3.3 tridiagonal solver | [Notes #9 Practical Considerations] |
| §5.1 stability vs resolution | [Notes #11 Misconception #1] |
| §5.2 operator-splitting error | [Notes #10 §8] |
| §5.4 UHI diagnostic interpretation | [Notes #11 Misconception #8] |

### 12.6 Homework index

| Project topic | Your HW work |
|---|---|
| FTCS blow-up | HW1: FTCS blew up at step 113 on tracer advection |
| Amplification factors | HW4: $|A_k|$ vs $k\Delta x$ for various CFL numbers |
| Three-scheme comparison | HW3: Euler unstable, Backward damping, Trapezoidal neutral |
| Staggered grid | HW5: 2-$\Delta x$ wave decoupling on unstaggered grid |
| Wave amplitude diagnostics | HW2: Sine-wave advection, period and amplitude tracking |
| Matsuno predictor-corrector | HW3 Case 4: explicit but stable through correction |

---

## Part 13. Glossary of every symbol used in the project

### Symbols used as scheme parameters

- $\alpha$ — In the $\theta$-method context: the implicitness weight. $\alpha = 0$ FTCS, $\alpha = 1/2$ CN, $\alpha = 1$ BTCS.
- $\alpha_s$ — Surface shortwave albedo (dimensionless, 0–1). Same Greek letter as $\theta$-method weight, different role.

### Symbols in the heat conduction equation

- $T_s(z, t)$ — Substrate temperature at depth $z$ and time $t$. Units K.
- $T_s^0$ — Surface temperature, $T_s$ at $z = 0$. Units K.
- $T_a$ — 2-metre air temperature. Units K.
- $z$ — Vertical depth, $z = 0$ at surface, increasing downward. Units m.
- $z_{\text{top}}$ — Bottom of column ($z_{\text{top}} = 2$ m).
- $z_j$ — Depth of cell-centre $j$.
- $z_{j+1/2}$ — Depth of half-level (face) between cells $j$ and $j+1$.
- $\Delta z_j$ — Thickness of cell $j$.
- $t$ — Time. Units s.
- $\Delta t$ — Time step.
- $n$ — Time-level index ($t = n\Delta t$).
- $\lambda_s$ — Substrate thermal conductivity. Units W/m/K.
- $\lambda_{j+1/2}$ — Half-level conductivity, harmonic mean.
- $C_s$ — Volumetric heat capacity. Units J/m³/K.
- $\kappa = \lambda/C$ — Thermal diffusivity. Units m²/s.
- $\kappa_{\text{top}}$ — Top-cell diffusivity.

### Heat flux and conservation

- $G(z, t)$ — Conductive heat flux. Units W/m². $G > 0$ means downward.
- $G_{j+1/2}$ — Discrete flux at face between cells $j$ and $j+1$.
- $q$ — Same as $G$ but with standard physics sign convention.
- $S = \int G dt$ — Daily storage integral. Units J/m².

### SEB components

- $R_n$ — Net radiation. $R_n = (1-\alpha_s)S_\downarrow + \varepsilon_s L_\downarrow - \varepsilon_s\sigma T_s^4$.
- $H$ — Sensible heat flux. $H = \rho c_p(T_s - T_a)/r_a$.
- $LE$ — Latent heat flux. Set to 0.
- $S_\downarrow$ — Incoming shortwave.
- $L_\downarrow$ — Incoming longwave.
- $\varepsilon_s$ — Surface longwave emissivity.
- $\sigma = 5.67\times 10^{-8}$ W/m²/K⁴ — Stefan–Boltzmann constant.
- $\rho \approx 1.2$ kg/m³ — Air density.
- $c_p = 1005$ J/kg/K — Specific heat of air.
- $C_H = 5\times 10^{-3}$ — Bulk transfer coefficient.
- $U = 3$ m/s — Wind speed (constant).
- $r_a = 1/(C_H U)$ — Aerodynamic resistance.
- $F(T_s^0)$ — SEB residual.

### Wave and stability analysis

- $\omega = 2\pi/86400$ rad/s — Diurnal angular frequency.
- $d = \sqrt{2\kappa/\omega}$ — Diurnal damping depth.
- $A$ — Surface temperature amplitude.
- $\bar{T}$, $T_{\text{mean}}$ — Mean surface temperature.
- $k$ — Spatial wavenumber.
- $k\Delta z$ — Dimensionless wavenumber.
- $A_k(\nu, k\Delta z)$ — Per-step amplification factor.
- $\nu = \kappa\Delta t/\Delta z^2$ — Diffusion number.

### Test 2 metrics

- $A_G$ — Half-amplitude of the diurnal $G$ cycle.
- $A_G/A_{\text{ref}}$ — Diurnal $G$ amplitude normalised.
- RMSE of $T_s$ — Root-mean-squared error.
- $S/S_{\text{ref}}$ — Daily storage integral ratio.

### SHAP analysis

- $N$ — Sample size ($N = 150$).
- $\mu_{\text{eff}} = \sqrt{\lambda_{\text{eff}} C_{\text{eff}}}$ — Bulk substrate admittance.
- $h_{\text{top}}$ — Top-layer thickness.
- $\phi_f(x)$ — SHAP value for feature $f$.
- $R^2$ — Coefficient of determination.

---

## Part 14. Common confusions and how to clear them up

### 14.1 Why is $\alpha$ used for two different things?

In the $\theta$-method, $\alpha$ is the implicitness weight. In the SEB, $\alpha_s$ is the surface shortwave albedo. The subscript $s$ disambiguates.

### 14.2 Why $\kappa$ instead of $\lambda$ in the diffusivity form?

The conductivity form $C \partial T/\partial t = \partial/\partial z(\lambda \partial T/\partial z)$ is always valid; the diffusivity form $\partial T/\partial t = \kappa \partial^2 T/\partial z^2$ requires constant $\lambda$ and $C$. In our layered substrates we use the conductivity form. Von Neumann analysis uses the diffusivity form because it assumes constant coefficients.

### 14.3 Why does $\nu$ matter and not $\Delta t$ alone?

Stability is a *dimensionless* property. The same $\Delta t$ on a finer grid is more stable. The dimensionless combination $\nu = \kappa\Delta t/\Delta z^2$ captures the right trade-off.

### 14.4 Why does $k\Delta z$ go up to $\pi$, not $2\pi$?

The finest wavelength on the grid is $\lambda_{\min} = 2\Delta z$, so $k_{\max} = 2\pi/(2\Delta z) = \pi/\Delta z$, hence $k\Delta z_{\max} = \pi$.

### 14.5 Why is FTCS first-order but the centred-space part is second-order?

FTCS = "Forward in Time, Centred in Space". Forward Euler is first-order in $\Delta t$. Centred space is second-order in $\Delta z$. Overall accuracy is the worse of the two.

### 14.6 Why did the abstract say FTCS blows up on all substrates?

This was a corrected inconsistency. The corrected version says "on the asphalt road and concrete roof" — soil at $\Delta t = 600$ s is over the bound but completes.

### 14.7 Why is bare soil hottest if asphalt has the lowest albedo?

Two factors compete: absorption rate ($1 - \alpha_s$) and downward conduction rate ($\kappa$). Bare soil has moderate absorption but very low $\kappa$, so absorbed heat concentrates at the surface.

### 14.8 Why is the operator-splitting error first-order even though CN is second-order?

CN's second-order accuracy applies to the per-substep integration of one process. The splitting error between sub-steps is a separate error source, first-order in $\Delta t$.

### 14.9 Why is $\kappa_{\text{top}}$ the dominant SHAP feature when admittance governs daily storage?

Admittance governs how much heat the column can store; $\kappa_{\text{top}}$ governs how fast the top cell responds. The splitting error is about response *rate*, not storage *capacity*.

### 14.10 What would I gain by using a fully-coupled solver?

You would eliminate the first-order operator-splitting error, leaving only the second-order CN truncation error. The 1.1 K BTCS error on asphalt could drop to 0.1–0.2 K.

---

*End of document.*
