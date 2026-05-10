# Clarify the Project: A Mastery-Level Walkthrough

*A LaTeX-rendered companion to `modified_full_report_1.docx`. Every concept, every equation, every notation explained from zero, with regular references to the course lecture notes and your six homeworks.*

---

## Part 0. How to use this document

This document is built so that anyone — even with zero prior knowledge of numerical modelling, partial differential equations, or surface-energy-balance physics — can read the long report and defend every choice in it. Every Greek letter, every subscript, every equation is opened up and explained.

**Reading recipe.** Read Parts 1–3 in order: they install the language used in the rest of the document. Then open the long report on one screen and this clarification on the other, and walk through them in parallel — when the report mentions §2.5, jump to Part 6.5 here.

**Conventions.**
- Inline math uses `$...$`: e.g. $\nu = \kappa\,\Delta t / \Delta z^2$.
- Display equations use `$$...$$` and are centred on their own line.
- Course-material references use the form **[Notes #6 §6.1]** to mean "Notes #6, Section 6.1".
- Homework references look like **[HW3, Case 3]** — meaning "your HW3 submission, the case labelled Case 3".

---

## Part 1. Foundational physics: heat, temperature, and the substrate

### 1.1 What does it mean for the ground to conduct heat?

Imagine a paving stone in the sun. The top is hot — say $50\,^{\circ}\mathrm{C}$. Five centimetres down, the stone is much cooler — say $30\,^{\circ}\mathrm{C}$. There is a *temperature gradient* inside the stone. As long as that gradient exists, heat will flow from the hot top to the cool bottom. This flow is conduction. There is no air movement, no fluid mixing — energy is passed from molecule to molecule through the solid.

The amount of heat that flows per square metre per second is the **conductive heat flux**, denoted $G$ in this project. Its units are watts per square metre, $\mathrm{W\,m^{-2}}$. By convention $G > 0$ means flow downward — into the ground.

Three quantities describe how a substrate (the generic word for whatever material is below the surface) responds to heat:

- **Thermal conductivity** $\lambda$ (Greek "lambda"). Units $\mathrm{W\,m^{-1}\,K^{-1}}$. How easily heat flows under a given temperature gradient. Air $\approx 0.025$; rigid foam $\approx 0.03$; dry sandy soil $\approx 0.30$; asphalt $\approx 0.75$; concrete $\approx 1.5$; granite $\approx 3.0$. Bigger $\lambda \Rightarrow$ heat propagates more easily.

- **Volumetric heat capacity** $C$. Units $\mathrm{J\,m^{-3}\,K^{-1}}$. The energy needed to raise one cubic metre of the material by one Kelvin. Water $= 4.18 \times 10^{6}$; concrete $\approx 2.1\times 10^{6}$; dry sandy soil $\approx 1.3\times 10^{6}$.

- **Thermal diffusivity** $\kappa$ (Greek "kappa"). Defined as $\kappa = \lambda / C$. Units $\mathrm{m^{2}\,s^{-1}}$. How quickly a temperature disturbance propagates. For our substrates $\kappa$ is in the range $10^{-7}$ to $10^{-6}\,\mathrm{m^{2}\,s^{-1}}$.

> **Lecture-notes connection.** The heat conduction equation is mentioned in **[Notes #2]** under 2nd-order PDEs (parabolic class, $B^{2} - 4AC = 0$). The conductivity-form-vs-diffusivity-form distinction does not appear explicitly there but is consistent with the general PDE framework taught in Notes #2.

### 1.2 Why distinguish $\lambda$ from $\kappa$?

Conductivity $\lambda$ tells you how much heat flows under a given gradient — it is what shows up in **Fourier's law**: $q = -\lambda\,\partial T/\partial z$. Diffusivity $\kappa$ tells you how fast a temperature pulse spreads — it is what shows up in the time-evolution equation $\partial T/\partial t = \kappa\,\partial^{2} T/\partial z^{2}$. Both rates matter, and they are tied together by the heat capacity. Water has high $\lambda$ but moderate $\kappa$ (large reservoir slows down spreading); foam has low $\lambda$ but moderate $\kappa$ (small reservoir, slow flow per gradient, but tiny capacity speeds up the response). For mastery: $\kappa$ controls *speed of response*; $\lambda$ controls *flux per gradient*.

### 1.3 The diurnal damping depth — the most important length scale in the project

Suppose the surface temperature varies sinusoidally with a period of 24 hours: hot in the afternoon, cold before sunrise. How does that wave penetrate into the soil? Solving the heat equation in a deep, uniform substrate with a sinusoidal temperature at the surface gives an exact answer: the wave travels downward, but its amplitude decays exponentially with depth. The depth at which the amplitude has decayed to $e^{-1} \approx 37\%$ of its surface value is the **diurnal damping depth**:

$$
d \;=\; \sqrt{\frac{2\,\kappa}{\omega}},\qquad \omega = \frac{2\pi}{86\,400\ \mathrm{s}} \approx 7.27\times 10^{-5}\ \mathrm{rad\,s^{-1}}.
$$

The square-root structure says: faster-diffusing materials (larger $\kappa$) feel the surface signal deeper; faster cycles (larger $\omega$) decay closer to the surface.

For the project's substrates:

| Substrate | $\kappa$ ($\mathrm{m^{2}\,s^{-1}}$) | $d$ |
|---|---|---|
| Bare soil | $2.31 \times 10^{-7}$ | $\approx 8\,\mathrm{cm}$ |
| Asphalt (top layer) | $3.75 \times 10^{-7}$ | $\approx 10\,\mathrm{cm}$ |
| Concrete deck | $7.14 \times 10^{-7}$ | $\approx 14\,\mathrm{cm}$ |

So the daily wave penetrates only the top 8–14 cm in any of these. To capture how the wave decays we must place the topmost grid cells at much smaller resolution than $d$ — typically half a centimetre to one centimetre.

### 1.4 Why $d$ matters for picking time steps

Once we resolve $d$ with cells of thickness $\Delta z \sim 0.5\,\mathrm{cm}$, we run into a constraint on $\Delta t$. For the explicit (FTCS) scheme, the maximum stable time step is

$$
\Delta t_{\max} \;=\; \frac{1}{2}\,\frac{\Delta z^{2}}{\kappa}.
$$

For $\Delta z = 5\,\mathrm{mm} = 0.005\,\mathrm{m}$ and the concrete deck's $\kappa = 7.14 \times 10^{-7}\,\mathrm{m^{2}\,s^{-1}}$:

$$
\Delta t_{\max} \;=\; \frac{1}{2}\,\frac{(0.005)^{2}}{7.14\times 10^{-7}} \;\approx\; 17\ \mathrm{s}.
$$

This is the famous "17-second problem". Operational models run at $\Delta t = 60$–$600\,\mathrm{s}$ — many times above this bound. So explicit time stepping is structurally ruled out. The whole project is about what to do instead — and what numerical errors that "instead" introduces.

> **Connecting to your work.** In **[HW1]** you saw the consequence of violating an explicit-stability bound: your FTCS tracer integration *blew up at step 113*, with $\max|q|$ exceeding 10 — the same kind of explosive instability that the project's FTCS at $\Delta t = 600\,\mathrm{s}$ on the asphalt road exhibits in 4–5 steps. The mechanism is identical: $|A| > 1$ at the worst Fourier mode causes geometric growth.

### 1.5 The four-component surface energy balance

Surface temperature $T_{s}^{0}$ is determined not by some external rule but by an energy balance at the surface. Four fluxes meet there:

- $R_{n}$ — net absorbed radiation (sun + sky longwave $-$ surface longwave emission), positive when energy is being deposited.
- $H$ — sensible heat flux to the air, positive when heat leaves the surface upward via warm air rising.
- $LE$ — latent heat flux from evaporation. In this project $LE = 0$ (impervious surfaces).
- $G$ — conductive heat flux into the substrate (positive downward).

Energy conservation requires what arrives equals what leaves:

$$
R_{n} - H - LE - G \;=\; 0.
$$

This is the **surface energy balance** (SEB). Together with the heat equation in the substrate, it determines $T_{s}^{0}$ at every moment.

---

## Part 2. From a continuous PDE to a discrete computer program

### 2.1 What is a partial differential equation?

An ordinary differential equation (ODE) describes how something changes with respect to a single variable — usually time. Newton's law of cooling, $\dfrac{dT}{dt} = -k(T - T_{\infty})$, is an ODE.

A partial differential equation (PDE) involves derivatives with respect to more than one variable. Heat conduction in depth is a PDE because $T$ depends on both $z$ and $t$:

$$
\frac{\partial T}{\partial t} \;=\; \kappa\,\frac{\partial^{2} T}{\partial z^{2}}.
$$

A computer cannot solve a PDE in continuous form — it cannot store an infinite number of $T(z, t)$ values. We must replace continuous derivatives with **finite differences** on a discrete grid: a list of cells at depths $z_{0}, z_{1}, \ldots, z_{N-1}$, advanced through time in discrete steps $\Delta t$.

> **[Notes #2]** classifies PDEs by order, linearity, and (for 2nd-order) the discriminant $B^{2} - 4AC$ — hyperbolic ($> 0$, wave-like), parabolic ($= 0$, diffusion-like), elliptic ($< 0$, steady-state). Our heat equation is **parabolic** — first-order in time, second-order in space.

### 2.2 The two basic finite-difference ideas

To replace a derivative by a finite difference, use Taylor's theorem. For a smooth function $f(x)$:

$$
f(x + \Delta x) \;=\; f(x) \;+\; \Delta x\,f'(x) \;+\; \frac{\Delta x^{2}}{2}\,f''(x) \;+\; O(\Delta x^{3}).
$$

Rearranging gives three estimates of $f'(x)$:

$$
\text{Forward:} \qquad f'(x) \;\approx\; \frac{f(x + \Delta x) - f(x)}{\Delta x} \;+\; O(\Delta x).
$$

$$
\text{Backward:} \qquad f'(x) \;\approx\; \frac{f(x) - f(x - \Delta x)}{\Delta x} \;+\; O(\Delta x).
$$

$$
\text{Centred:} \qquad f'(x) \;\approx\; \frac{f(x + \Delta x) - f(x - \Delta x)}{2\,\Delta x} \;+\; O(\Delta x^{2}).
$$

The centred difference is second-order accurate because the leading $O(\Delta x)$ error term cancels when we subtract the two Taylor expansions.

For a second derivative we use the centred three-point formula:

$$
f''(x) \;\approx\; \frac{f(x + \Delta x) - 2 f(x) + f(x - \Delta x)}{\Delta x^{2}} \;+\; O(\Delta x^{2}).
$$

These small algebraic identities are the only finite-difference formulas you need to read this entire report. Every discretised equation in §2.2 of the report is a combination of these few rules.

> **[Notes #3 §1]** sets out Taylor series and explicitly derives these forward/backward/centred difference formulas. **[HW1]** and **[HW2]** both apply the centred-difference (centred-time, centred-space, "CTCS") scheme to advection — so you are already familiar with the algebra.

### 2.3 What does "stability" mean?

A finite-difference scheme is **stable** if small numerical errors at one time step do not grow unboundedly over many time steps. If errors grow, the solution "blows up" — computed temperatures become $\pm\infty$ or NaN with no physical meaning. Stability is separate from accuracy: a scheme can be stable but inaccurate (just damps everything to a uniform value), or accurate but unstable (good for one step, but blows up after many).

Some schemes are **conditionally stable** — $\Delta t$ must be smaller than some bound for stability. Others are **unconditionally stable** — any $\Delta t$ works. Von Neumann analysis (Part 6.5) finds these bounds.

> **[Notes #6 §10]** introduces von Neumann analysis. **[HW3]** and **[HW4]** both used it: in HW3 you computed amplification factors for Euler / Backward / Trapezoidal / Matsuno applied to the oscillation equation $d\psi/dt = i\omega\psi$, and confirmed Euler is unstable, Backward is always stable but damping, Trapezoidal is neutrally stable. The same logical structure carries over to diffusion in this project.

---

## Part 3. The vocabulary of finite-difference time-stepping schemes

### 3.1 Explicit vs implicit

For an ODE $\dfrac{dT}{dt} = f(T)$, two natural time-step rules:

- **Explicit (forward Euler):** $T^{n+1} = T^{n} + \Delta t\,f(T^{n})$. RHS uses only the known $T^{n}$. No equation to solve. Cheap per step, conditionally stable.
- **Implicit (backward Euler):** $T^{n+1} = T^{n} + \Delta t\,f(T^{n+1})$. RHS uses the unknown $T^{n+1}$. We solve an algebraic equation. Expensive per step, unconditionally stable.

When $f$ is linear in $T$, the implicit scheme is a linear system; when nonlinear, we use Newton iteration.

### 3.2 The trapezoidal rule = Crank–Nicolson

Take the average of explicit and implicit:

$$
T^{n+1} \;=\; T^{n} \;+\; \frac{\Delta t}{2}\bigl[f(T^{n}) + f(T^{n+1})\bigr].
$$

This is the **trapezoidal rule** for ODE integration. Implicit (so unconditionally stable), and second-order accurate in $\Delta t$ because the symmetric average cancels the leading error term.

When applied to the heat equation, the trapezoidal rule is called the **Crank–Nicolson** scheme (Crank & Nicolson, 1947). Implicit, unconditionally stable, second-order in time.

### 3.3 The $\alpha$-weighted $\theta$-method

All three schemes are special cases of one formula:

$$
T^{n+1} \;=\; T^{n} \;+\; \Delta t\,\bigl[\,\alpha\,f(T^{n+1}) + (1 - \alpha)\,f(T^{n})\,\bigr].
$$

| $\alpha$ | Scheme | Order | Stability |
|---|---|---|---|
| $0$ | FTCS / explicit Euler | first | conditional, $\nu \le 1/2$ |
| $1/2$ | Crank–Nicolson | second | unconditional |
| $1$ | BTCS / implicit Euler | first | unconditional |

> **[Notes #6 §6 (Slides 15–17)]** introduces these *three exact schemes by name*: Euler (forward), Backward, Trapezoidal. The lecture-note formulae are
> $$\phi^{n+1} = \phi^{n} + \Delta t\,f^{n} \quad \text{(Euler/forward)}$$
> $$\phi^{n+1} = \phi^{n} + \Delta t\,f^{n+1} \quad \text{(Backward)}$$
> $$\phi^{n+1} = \phi^{n} + \tfrac{1}{2}\Delta t\,(f^{n} + f^{n+1}) \quad \text{(Trapezoidal)}$$
> with truncation errors $O(\Delta t)$, $O(\Delta t)$, $O((\Delta t)^{2})$ respectively. The project's FTCS, BTCS, CN are these same three schemes, applied here to the parabolic diffusion equation rather than to the ODE oscillation equation that the lecture used for illustration.
>
> **[HW3]** is the direct ancestor of this project: you implemented the same three schemes (plus Matsuno) on the oscillation equation $d\psi/dt = i\omega\psi$ and showed exactly the property pattern that carries over here — Euler unstable, Backward always stable but damping, Trapezoidal neutrally stable. The project's diffusion problem is a different PDE class (parabolic, not oscillation), so the *quantitative* stability conclusions are different (Trapezoidal is now strictly stable, not just neutral), but the structural pattern is the same.

---

## Part 4. Walking through the abstract

The abstract is the densest paragraph in the report. We unpack it claim by claim.

**"The ground heat flux is the energy that the surface stores and releases from its substrate over a diurnal cycle, and is the term in the surface energy budget that is most sensitive to numerical treatment."** — $G$ is small in daily mean (small fraction of $R_{n}$), but it controls the day-night temperature swing, and the way $G$ is computed numerically can introduce errors that are large compared to $G$ itself.

**"...explicit forward-time discretization is conditionally stable only when $\nu = \kappa_{s}\Delta t / \Delta z^{2} \le 1/2$ — a constraint that becomes prohibitive for the cm-scale near-surface layers required to resolve the diurnal damping depth in highly conductive urban substrates."** Decoded:

- "parabolic" — the mathematical class of PDEs whose principal time-and-space derivative pattern matches the heat equation. From **[Notes #2 §2nd-Order PDEs]**.
- "explicit forward-time discretization" = FTCS = $\alpha = 0$ in the $\theta$-method.
- "conditionally stable when $\nu \le 1/2$" = the FTCS stability bound from von Neumann analysis (**[Notes #9 §Pure Diffusion]**).
- "cm-scale near-surface layers" — since $d \sim 8$–$14\,\mathrm{cm}$, $\Delta z \ll d$ requires $\Delta z \sim 0.5$–$1\,\mathrm{cm}$.
- "highly conductive urban substrates" — concrete and asphalt have higher $\kappa$ than soil and so push the FTCS bound to even smaller $\Delta t$.

**"three numerical treatments...coupled to a fully prognostic surface energy balance solved by Newton iteration."** The key word is *prognostic*: $T_{s}^{0}$ is computed by the model at every step, not prescribed externally. Compare to Test 1 where $T_{s}^{0}$ is prescribed as a sinusoid — that is verification, not prognostic.

The abstract's principal-findings sentences correspond one-to-one with the §7 conclusion bullets. We unpack each in detail when we reach §7 (Part 11).

---

## Part 5. Walking through §1 Introduction

### 5.1 Why the urban heat island depends on $G$ specifically

The urban heat island (UHI) is the systematic phenomenon that cities are warmer than rural areas, especially at night. Many factors contribute (anthropogenic heat, canyon geometry, reduced evapotranspiration), but the central physical mechanism for the *night-time* component is **heat storage**.

During the day, urban materials — pavements, walls, roofs — absorb shortwave radiation. Their high heat capacity and conductivity (relative to vegetated soil) mean they hold a lot of that energy. After sunset, $R_{n}$ turns negative and the stored heat is released. Rural surfaces store less (their substrates are usually drier and less conductive, with much daytime energy lost to evapotranspiration). At night, the urban surface is still warm while the rural one has cooled — that contrast is the nocturnal UHI.

$G$ is the very quantity that *puts heat into the urban substrate during the day and pulls it back out at night*. If a model gets $G$ wrong, it gets the UHI wrong.

### 5.2 The damping-depth values quoted in the introduction

Paragraph 11 of the report says: "$d$ is approximately $8\,\mathrm{cm}$ in dry soil, $14\,\mathrm{cm}$ in dense concrete, and $10\,\mathrm{cm}$ in asphalt (computed from the substrate parameters used in §3.2)." Plugging the substrate's $\lambda$ and $C$ into $d = \sqrt{2\kappa/\omega}$:

$$
d_{\text{soil}} = \sqrt{\frac{2(2.31\times 10^{-7})}{7.27\times 10^{-5}}} \;\approx\; 0.0797\,\mathrm{m} = 7.97\,\mathrm{cm}.
$$

The same calculation gives concrete $14.0\,\mathrm{cm}$ and asphalt $10.2\,\mathrm{cm}$. These are the physical motivation for the cm-scale grid resolution.

### 5.3 What "wavenumber-dependent damping" means

The end of paragraph 11 says implicit schemes "introduce wavenumber-dependent damping that distorts the high-frequency content of the diurnal cycle". Every numerical scheme can be characterised by how it changes the amplitude of each Fourier component (each wavelength) per time step. For FTCS, BTCS, CN we will derive these *amplification factors* explicitly in Part 6.5. Wavenumber-dependent damping means the amplification factor is not 1 — short waves are damped differently from long waves, and that distortion is what the report quantifies.

> **[HW2]** asked you to verify amplitude conservation on a sine-wave initial condition: the period-tracking and max-amplitude diagnostics there are exactly the kind of test for wavenumber-dependent damping that the project applies to its diffusion solvers.

---

## Part 6. Walking through §2 — Governing equation and numerical discretization

### 6.1 §2.1 — Where the heat conduction equation comes from

The report writes the heat conduction equation in **conductivity form**:

$$
\boxed{\;C_{s}(z)\,\frac{\partial T_{s}}{\partial t} \;=\; \frac{\partial}{\partial z}\!\left[\,\lambda_{s}(z)\,\frac{\partial T_{s}}{\partial z}\,\right]\;}
$$

Read aloud: "volumetric heat capacity times the rate of change of temperature with time equals the spatial divergence of the conductive heat flux." Where does this equation come from?

**Step 1. Fourier's law of heat conduction.** Heat flows from hot to cold, with magnitude proportional to the temperature gradient and the conductivity:

$$
q(z) \;=\; -\lambda_{s}(z)\,\frac{\partial T_{s}}{\partial z}.
$$

If $T$ decreases with depth ($\partial T/\partial z < 0$), then $q > 0$ — flux in the $+z$ direction (downward).

**Step 2. Energy conservation in a thin slab.** Pick a thin horizontal slab from depth $z$ to $z + dz$. Energy stored per unit area: $C_{s}\,T_{s}\,dz$. Rate of change of stored energy = net flux into slab = $q(z) - q(z + dz) = -(\partial q/\partial z)\,dz$:

$$
C_{s}\,\frac{\partial T_{s}}{\partial t}\,dz \;=\; -\frac{\partial q}{\partial z}\,dz.
$$

Substituting $q = -\lambda_{s}\,\partial T_{s}/\partial z$:

$$
C_{s}\,\frac{\partial T_{s}}{\partial t} \;=\; -\frac{\partial}{\partial z}\!\left[\,-\lambda_{s}\,\frac{\partial T_{s}}{\partial z}\,\right] \;=\; \frac{\partial}{\partial z}\!\left[\,\lambda_{s}\,\frac{\partial T_{s}}{\partial z}\,\right].
$$

That is the conductivity-form heat equation. It is just energy conservation written locally, with Fourier's law for the flux.

#### Why "conductivity form" instead of "diffusivity form"?

If $\lambda$ and $C$ are constant, we can pull them out of the derivative and write $\partial T/\partial t = \kappa\,\partial^{2} T/\partial z^{2}$ with $\kappa = \lambda/C$. That is the **diffusivity form**. In our layered substrates, $\lambda$ and $C$ jump by an order of magnitude across material interfaces. The diffusivity form, when discretised, does not exactly conserve heat across those jumps — discrete heat content can drift. The conductivity form, with the harmonic mean (Part 6.2), preserves heat exactly across any $\lambda$ jump. That is why the report keeps $\lambda$ and $C$ inside the derivative.

#### What the symbols mean

- $T_{s}(z, t)$ — substrate temperature at depth $z$, time $t$. Units Kelvin (K). The subscript $s$ distinguishes from air temperature $T_{a}$.
- $z$ — vertical depth, $z = 0$ at the surface, increasing downward. Units m.
- $\lambda_{s}(z)$ — substrate thermal conductivity at depth $z$. Units $\mathrm{W\,m^{-1}\,K^{-1}}$. The $s$ subscript means "substrate" — disambiguates from any other $\lambda$.
- $C_{s}(z)$ — volumetric heat capacity. Units $\mathrm{J\,m^{-3}\,K^{-1}}$.
- $\partial T_{s}/\partial t$ — partial derivative w.r.t. time, holding $z$ fixed.
- $\partial T_{s}/\partial z$ — temperature gradient, the "how $T$ changes per metre going down" rate.
- $\partial/\partial z\,[\lambda_{s}\,\partial T_{s}/\partial z]$ — second-order spatial operator with $\lambda$ inside.

### 6.2 §2.2 — The grid, the half-levels, the harmonic mean

#### Cell centres and the staggered grid

Replace the continuous depth $z$ with cell centres $z_{0}, z_{1}, \ldots, z_{N-1}$. At each cell store *one number*: temperature $T_{j}$ at the centre. Between cells $j$ and $j+1$ lies a face at depth $z_{j+1/2} = (z_{j} + z_{j+1})/2$. Temperatures live at centres; conductive fluxes at faces.

Why? The flux involves $\partial T/\partial z$, and the most accurate centred-difference estimate of that derivative uses $T$ on either side of the point of evaluation. The face between cells $j$ and $j+1$ is exactly halfway between them, so $(T_{j} - T_{j+1})/(z_{j+1} - z_{j})$ is naturally centred there.

This **staggered grid** is the standard finite-volume layout. Its main virtue is automatic conservation: the heat that leaves cell $j$ across face $j+\tfrac{1}{2}$ is the *same* heat that enters cell $j+1$ across the same face, so energy is conserved by construction.

> **[Notes #8]** is dedicated to staggered grids and their advantages for accurate handling of short-wavelength features. **[HW5]** is the direct precursor: you compared an unstaggered grid (where the $2\Delta x$ wave has *zero numerical phase speed*) against a staggered grid (where it propagates correctly). The same advantage applies to the project's flux discretisation: putting $G$ at half-levels allows accurate centred-difference gradients and energy conservation by construction.

#### The discrete flux equation, line by line

The report's equation:

$$
G_{j+1/2} \;=\; \lambda_{j+1/2}\,\frac{T_{j} - T_{j+1}}{z_{j+1} - z_{j}}
$$

is Fourier's law evaluated at the half-level. Decoded:

- $G_{j+1/2}$ — conductive heat flux through the face between cells $j$ and $j+1$. Units $\mathrm{W\,m^{-2}}$. Sign: $G > 0$ = downward.
- $\lambda_{j+1/2}$ — thermal conductivity at the face. Computed from the cell-centre $\lambda_{j}$ and $\lambda_{j+1}$ via the harmonic mean.
- $(T_{j} - T_{j+1})$ — temperature drop from cell $j$ (above) to cell $j+1$ (below). Positive when $j$ is warmer, meaning heat flows down — consistent with $G > 0$.
- $(z_{j+1} - z_{j})$ — centre-to-centre spacing.

So $G_{j+1/2}$ = $\lambda$ × (temperature drop) / (centre-to-centre distance) = $\lambda$ × (gradient evaluated centrally at the face). Fourier's law with a centred difference. The minus sign in $q = -\lambda\,\partial T/\partial z$ has been absorbed into writing $(T_{j} - T_{j+1})$ instead of $(T_{j+1} - T_{j})$, so that $G > 0$ corresponds to downward flow.

#### Why the harmonic mean for $\lambda$ at faces?

Solve the steady-state conduction problem across an interface between two materials. The flux must be the same on both sides (steady state, no storage):

$$
q \;=\; \lambda_{1}\,\frac{\Delta T_{1}}{\Delta z_{1}} \;=\; \lambda_{2}\,\frac{\Delta T_{2}}{\Delta z_{2}}.
$$

Total temperature drop is $\Delta T = \Delta T_{1} + \Delta T_{2}$ over total distance $\Delta z = \Delta z_{1} + \Delta z_{2}$. Algebra gives

$$
q \;=\; \frac{\Delta T}{\Delta z_{1}/\lambda_{1} + \Delta z_{2}/\lambda_{2}} \;=\; \lambda_{\text{eff}}\,\frac{\Delta T}{\Delta z},
$$

where $\lambda_{\text{eff}} = \dfrac{\Delta z_{1} + \Delta z_{2}}{\Delta z_{1}/\lambda_{1} + \Delta z_{2}/\lambda_{2}}$ — a thickness-weighted harmonic mean.

For two cells of equal thickness this collapses to:

$$
\boxed{\;\lambda_{j+1/2} \;=\; \frac{2\,\lambda_{j}\,\lambda_{j+1}}{\lambda_{j} + \lambda_{j+1}}\;}
$$

**Numerical check:** with $\lambda_{\text{concrete}} = 1.5$ and $\lambda_{\text{insulation}} = 0.04$:

- Arithmetic mean: $0.77$ (close to concrete — wrong).
- Harmonic mean: $0.078$ (much closer to insulation — correct).

The harmonic mean correctly captures that a thin insulator dominates the resistance. The arithmetic mean would over-estimate the heat flux across this interface by a factor of $\sim 10$ — meaning the model would wrongly predict that insulation lets heat through nearly as easily as concrete.

#### The semi-discrete tendency

Apply the centred-difference flux at every face:

$$
\boxed{\;C_{j}\,\Delta z_{j}\,\frac{dT_{j}}{dt} \;=\; G_{j-1/2} - G_{j+1/2}\;}
$$

The rate of energy accumulation in cell $j$ (per unit horizontal area) equals the flux entering at the top minus the flux leaving at the bottom. Energy-content rate is $C_{j}\,\Delta z_{j}\,dT_{j}/dt$ because the energy density per unit volume is $C_{j} T_{j}$ and the cell has thickness $\Delta z_{j}$.

This is **semi-discrete**: space is discretised, time is still continuous. The next step discretises time.

### 6.3 §2.3 — Building the $\theta$-method update equation

The semi-discrete equation is $C_{j}\,\Delta z_{j}\,dT_{j}/dt = R_{j}(t)$, where $R_{j} = G_{j-1/2} - G_{j+1/2}$. Integrate from $t^{n}$ to $t^{n+1}$:

$$
C_{j}\,\Delta z_{j}\,(T_{j}^{n+1} - T_{j}^{n}) \;=\; \int_{t^{n}}^{t^{n+1}} R_{j}(t)\,dt.
$$

Three quadrature rules give three schemes:

- Left rectangle: $\int \approx \Delta t\,R_{j}^{n}$. FTCS, $\alpha = 0$.
- Right rectangle: $\int \approx \Delta t\,R_{j}^{n+1}$. BTCS, $\alpha = 1$.
- Trapezoid: $\int \approx (\Delta t/2)[R_{j}^{n} + R_{j}^{n+1}]$. CN, $\alpha = 1/2$.

In one line — the report's $\theta$-method update:

$$
\boxed{\;C_{j}\,\Delta z_{j}\,\frac{T_{j}^{n+1} - T_{j}^{n}}{\Delta t} \;=\; \alpha\,[\,G_{j-1/2} - G_{j+1/2}\,]^{n+1} \;+\; (1 - \alpha)\,[\,G_{j-1/2} - G_{j+1/2}\,]^{n}\;}
$$

Setting $\alpha = 0, 1$, or $1/2$ retrieves FTCS, BTCS, CN respectively. The single-line form is what makes the project's code clean — one update routine handles all three schemes.

#### Why FTCS and BTCS are first-order, CN is second-order in $\Delta t$

Taylor-expand each quadrature rule around the midpoint $t^{n} + \Delta t/2$. Left and right rectangles each carry an $O(\Delta t)$ leading error; trapezoid averages them and the leading error cancels, leaving $O(\Delta t^{2})$.

> **[HW3 Case 3]** confirmed this empirically for the oscillation equation: your trapezoidal scheme was *neutrally stable for all frequencies*, with amplitude staying exactly at 1.0 — the second-order accuracy showing through. Same algebraic mechanism here.

#### Linear systems and tridiagonal solves

When $\alpha > 0$, the RHS involves $T$ values at level $n+1$ — the unknowns. Collecting unknowns on the left and knowns on the right gives a system of $N$ linear equations in $N$ unknowns. The matrix has nonzero entries only on the main diagonal and the two adjacent diagonals (because each cell $j$ couples only to $j \pm 1$ through the two faces). Such a matrix is **tridiagonal**.

Tridiagonal systems can be solved in $O(N)$ operations using the Thomas algorithm — far cheaper than a generic $O(N^{3})$ solver. SciPy provides `scipy.linalg.solve_banded((1,1), A, b)`. The argument $(1, 1)$ means "one band below the diagonal, one band above".

> **[Notes #9 §Practical Considerations]** explicitly notes: "implicit differencing leads to a system of algebraic equations with a tridiagonal matrix structure...tridiagonal solvers are particularly efficient and well suited for vertical mixing in oceanic and atmospheric models, where stability constraints are most restrictive." The project uses exactly this lecture-prescribed approach.

### 6.4 §2.4 — The boundary conditions

A PDE governs how things change *inside* a domain. To get a well-defined problem, we need to specify what happens at the boundaries. Two main types:

- **Dirichlet condition** — prescribes the value of $T$ at the boundary. Example: $T(0, t) = T_{s}^{0}(t)$.
- **Neumann condition** — prescribes the value of the gradient $\partial T/\partial z$ (equivalently the flux $q = -\lambda\,\partial T/\partial z$) at the boundary. Example: $\partial T/\partial z = 0$ (zero gradient = zero flux).

#### Lower boundary: zero-flux Neumann

At $z = z_{\text{top}} = 2\,\mathrm{m}$ we impose $\partial T/\partial z = 0$. Why? At $2\,\mathrm{m}$ we are well below $d \approx 8$–$14\,\mathrm{cm}$ — the daily wave has long since decayed. Below $2\,\mathrm{m}$ the temperature varies only on seasonal timescales, which is much slower than the diurnal cycle of interest. Modelling the deep substrate as adiabatic (zero flux) is the standard choice.

Discretely: $T_{N-1} = T_{N-2}$, i.e., the deepest cell has the same temperature as the cell above it. This forces the centred-difference gradient at the bottom face to be zero, hence zero flux.

#### Upper boundary: Dirichlet on $T_{s}^{0}$

At cell 0 we set $T_{0} = T_{s}^{0}$. In Test 1, $T_{s}^{0}(t) = \bar T + A\cos\omega t$ — a prescribed sinusoid. In Test 2, $T_{s}^{0}$ is the unknown solved by Newton iteration on the SEB.

### 6.5 §2.5 — Von Neumann stability analysis from scratch

This is the most algebraically dense subsection of the report. Take it in stages.

#### Setup: linearise, idealise, then test

Von Neumann analysis works only for linear schemes on uniform grids with constant coefficients. Idealise: assume $\lambda$ and $C$ are constant (so $\kappa = \lambda/C$ is constant), assume $\Delta z$ is uniform, assume periodic boundaries. Then test whether the scheme amplifies any small perturbation.

#### Step 1 — Substitute a Fourier mode

Any small perturbation can be written as a sum of complex-exponential Fourier modes:

$$
T_{j}^{n} \;=\; A^{n}\,e^{i k j\,\Delta z}.
$$

Here $k$ is the wavenumber (radians per metre) and $A$ is the **amplification factor** (one complex number per wavenumber). Reasoning: the equation is linear, so different Fourier modes do not interact; we analyse each independently. The complex form $e^{i\theta} = \cos\theta + i\sin\theta$ is just a clean shorthand for the cos/sin analysis.

#### Step 2 — Plug into the FTCS update

FTCS at $\alpha = 0$ on a uniform grid with constant $\kappa$, in diffusivity form:

$$
T_{j}^{n+1} \;=\; T_{j}^{n} \;+\; \frac{\kappa\,\Delta t}{\Delta z^{2}}\,\bigl[\,T_{j+1}^{n} - 2 T_{j}^{n} + T_{j-1}^{n}\,\bigr].
$$

Define $\nu = \kappa\,\Delta t/\Delta z^{2}$. Substitute the Fourier mode:

$$
A^{n+1}\,e^{i k j\Delta z} \;=\; A^{n}\,e^{i k j\Delta z} \;+\; \nu\,A^{n}\,\bigl[\,e^{i k (j+1)\Delta z} - 2\,e^{i k j\Delta z} + e^{i k (j-1)\Delta z}\,\bigr].
$$

Divide both sides by $A^{n}\,e^{i k j\Delta z}$:

$$
A \;=\; 1 \;+\; \nu\,\bigl[\,e^{i k\Delta z} - 2 + e^{-i k\Delta z}\,\bigr].
$$

Use Euler's identity $e^{i x} + e^{-i x} = 2\cos x$:

$$
\boxed{\;A_{\mathrm{FTCS}}(\nu, k\Delta z) \;=\; 1 - 2\nu\,(1 - \cos k\Delta z)\;}
$$

> **[Notes #9 §Pure Diffusion (Von Neumann Analysis)]** derives this *exact same formula*, using $M$ for diffusivity and $\nu = M\Delta t/(\Delta x)^{2}$. The lecture concludes: "Stability criterion: $0 \le \nu \le 1/2$". The project uses identical algebra and the identical bound.

#### Step 3 — Plug into the BTCS update

BTCS at $\alpha = 1$:

$$
T_{j}^{n+1} \;=\; T_{j}^{n} \;+\; \nu\,\bigl[\,T_{j+1}^{n+1} - 2 T_{j}^{n+1} + T_{j-1}^{n+1}\,\bigr].
$$

Substitute the Fourier mode:

$$
A^{n+1} \;=\; A^{n} \;+\; \nu\,A^{n+1}\,[2\cos k\Delta z - 2].
$$

Divide by $A^{n}$:

$$
A \;=\; 1 \;+\; A\,\nu\,[\,2\cos k\Delta z - 2\,].
$$

Rearrange:

$$
A\,\bigl[\,1 + 2\nu\,(1 - \cos k\Delta z)\,\bigr] \;=\; 1.
$$

$$
\boxed{\;A_{\mathrm{BTCS}}(\nu, k\Delta z) \;=\; \frac{1}{1 + 2\nu\,(1 - \cos k\Delta z)}\;}
$$

#### Step 4 — Plug into the CN update

CN at $\alpha = 1/2$:

$$
T_{j}^{n+1} \;=\; T_{j}^{n} \;+\; \frac{\nu}{2}\,[\,T_{j+1}^{n} - 2T_{j}^{n} + T_{j-1}^{n}\,] \;+\; \frac{\nu}{2}\,[\,T_{j+1}^{n+1} - 2T_{j}^{n+1} + T_{j-1}^{n+1}\,].
$$

Let $h = \nu\,(1 - \cos k\Delta z)$. Substitute and simplify:

$$
A \;=\; 1 - h - h\,A.
$$

$$
A\,(1 + h) \;=\; 1 - h.
$$

$$
\boxed{\;A_{\mathrm{CN}}(\nu, k\Delta z) \;=\; \frac{1 - h}{1 + h} \;=\; \frac{1 - \nu(1 - \cos k\Delta z)}{1 + \nu(1 - \cos k\Delta z)}\;}
$$

> **[Notes #9 §Implicit Diffusion]** derives this same formula and labels it "the Crank–Nicolson method". The lecture concludes: "$|A_{k}| < 1$ — Unconditionally stable". The project's algebra and the project's bound are the lecture's algebra and bound.

#### What $|A| \le 1$ means and why we want it

After one time step, the Fourier mode at wavenumber $k$ has amplitude $A$. After $n$ time steps, amplitude is $A^{n}$. If $|A| > 1$, the mode grows exponentially: $|A|^{n} \to \infty$. That is what "blow-up" is — some Fourier component growing without bound until floating-point overflow.

If $|A| \le 1$, the mode either holds steady or decays. The scheme is **stable in the von Neumann sense** if $|A| \le 1$ for every wavenumber the grid resolves. The grid resolves $k\Delta z \in [0, \pi]$ (because shorter wavelengths than $2\Delta z$ cannot exist on the grid).

#### Why $k\Delta z = \pi$ is the worst case

For all three amplification factors, the dependence on $k\Delta z$ is through the factor $(1 - \cos k\Delta z)$. This factor:

- Equals 0 at $k\Delta z = 0$ (because $\cos 0 = 1$).
- Equals 2 at $k\Delta z = \pi$ (because $\cos \pi = -1$).
- Is monotonically increasing on $[0, \pi]$.

Whichever wavenumber pushes $A$ farthest from 1 in magnitude is the wavenumber where $(1 - \cos k\Delta z)$ is largest — always $k\Delta z = \pi$, the **2-$\Delta z$ wave**. Substituting $1 - \cos\pi = 2$ into each amplification factor:

$$
A_{\mathrm{FTCS}}(\nu, \pi) = 1 - 4\nu, \qquad
A_{\mathrm{BTCS}}(\nu, \pi) = \frac{1}{1 + 4\nu}, \qquad
A_{\mathrm{CN}}(\nu, \pi) = \frac{1 - 2\nu}{1 + 2\nu}.
$$

#### Reading the stability conclusions

**FTCS:** $A = 1 - 4\nu$ at the worst wave. Need $|A| \le 1$, i.e., $-1 \le 1 - 4\nu \le 1$. Upper bound automatic (since $\nu \ge 0$). Lower: $1 - 4\nu \ge -1 \Rightarrow \nu \le 1/2$. So FTCS is **conditionally stable** with bound $\nu \le 1/2$, i.e., $\Delta t \le \tfrac{1}{2}\Delta z^{2}/\kappa$.

**BTCS:** $A = 1/(1 + 4\nu)$. For $\nu > 0$ this is automatically in $(0, 1)$. So $|A| < 1$ always — **unconditionally stable, strictly damping**.

**CN:** $A = (1 - 2\nu)/(1 + 2\nu)$. For $\nu > 0$ the numerator can be negative (when $\nu > 1/2$), but $|1 - 2\nu| \le |1 + 2\nu|$, so $|A| \le 1$ always — **unconditionally stable**. As $\nu \to \infty$, $A \to -1$: the worst wave is preserved in magnitude (|$A$| = 1) but flips sign every step. This is the "ringing" pathology of CN at large $\nu$: 2-$\Delta z$ noise is not suppressed, just made to oscillate. Note: this is a noise issue, not a blow-up. For smooth initial conditions and smooth forcing, harmless.

> **[HW4]** is the direct ancestor: you plotted $|A_{k}|$ against $k\Delta x$ for various CFL numbers $\mu$ for an advection scheme, observed the peak at $k\Delta x = \pi/2$, and concluded which $\mu$ values gave $|A_{k}| \ge 1$. The project applies the *same logical structure* to a parabolic equation, with the worst case at $k\Delta z = \pi$ instead of $\pi/2$ — because the diffusion equation has $\cos k\Delta z$, while your HW4's advection had $\sin k\Delta x$.

### 6.6 Reading Figure 1 panel by panel

Figure 1 has three panels — FTCS, BTCS, CN — each plotting $|A_{k}|$ vs $k\Delta z$ for four values of $\nu$.

**The axes.** The $x$-axis is $k\Delta z$, ranging from 0 to $\pi$. The $y$-axis is $|A_{k}(\nu, k\Delta z)|$, the magnitude of the amplification factor.

- $k\Delta z = 0$ corresponds to infinitely long wavelengths (a constant in space) — these are barely affected by diffusion, so $|A| \approx 1$ for all schemes.
- $k\Delta z = \pi$ corresponds to the shortest wavelength on the grid, the 2-$\Delta z$ wave — the pattern flips sign at every cell.

We plot $|A|$ because actual $A$ can be negative — but stability cares only about magnitude. A horizontal dashed line at $|A| = 1$ marks the stability bound.

**The four $\nu$ values.** $\nu = 0.25, 0.5, 1.0, 5.0$. Each curve shows how that scheme responds to each wavenumber at that $\nu$.

Panel by panel:

#### FTCS panel

- $\nu = 0.25$: stays well below 1 across all $k\Delta z$ — stable, well-resolved.
- $\nu = 0.5$: exactly touches $|A| = 1$ at $k\Delta z = \pi$ — the marginal stability case, $A_{\mathrm{FTCS}}(0.5, \pi) = -1$, $|A| = 1$.
- $\nu = 1.0$: exceeds 1 over a large range of $k\Delta z$ — unstable.
- $\nu = 5.0$: off the chart at $k\Delta z = \pi$, where $A = 1 - 4(5) = -19$, $|A| = 19$ — massive instability. The annotation in the figure calls this out.

#### BTCS panel

All four curves stay well below 1, monotonically decreasing in $k\Delta z$. At $\nu = 5$: $|A_{\mathrm{BTCS}}(5, \pi)| = 1/21 \approx 0.05$ — the 2-$\Delta z$ wave is damped to near-nothing in one step. BTCS is unconditionally stable AND strongly damps short waves at large $\nu$.

#### CN panel

All four curves stay below 1, but the $\nu = 5$ curve has a peculiar shape: it dips toward zero around the middle of the $k\Delta z$ range, then rises back up toward $0.82$ at $k\Delta z = \pi$. At $\nu = 5$: $A_{\mathrm{CN}}(5, \pi) = (1 - 10)/(1 + 10) = -9/11 \approx -0.818$, so $|A| = 0.818$. The 2-$\Delta z$ wave is barely damped — losing only 18% per step, compared to BTCS's 95% loss per step. This is the **weak-damping pathology of CN at large $\nu$**.

> **Why we have CN at all, given this weakness.** Because at the *resolved* scales (small $k\Delta z$, where the physics actually lives), CN is *much more accurate per step* than BTCS — second-order accurate vs first-order. The price is poorer damping of unresolved noise. For smooth problems with smooth initial conditions, CN gives much better daytime/nighttime profile fidelity per step than BTCS. The project quantifies this trade-off: at $\Delta t = 600\,\mathrm{s}$, CN halves BTCS's diurnal-amplitude error.

---

## Part 7. Walking through §3 — Methods

### 7.1 §3.1 — What "parameterised by $\alpha$" means in code

The report says: *All three schemes share a single step routine parameterised by* $\alpha$. In Python this means one function `step_alpha(T, dt, ..., alpha, ...)` that takes $\alpha$ as an argument, with FTCS, BTCS, CN recovered by passing `alpha=0.0, 1.0, 0.5`. The branch logic inside is short: when $\alpha = 0$, direct arithmetic; when $\alpha > 0$, tridiagonal solve. Benefit: any bug in the spatial discretisation affects all three schemes equally and cannot manufacture a fake difference between schemes.

### 7.2 §3.2 — Substrate definitions

**Asphalt road** (4 layers, 2 m total):
- Asphalt 0–5 cm: $\lambda = 0.75$, $C = 2.0\times 10^{6}$.
- Aggregate 5–25 cm: $\lambda = 1.40$, $C = 2.4\times 10^{6}$.
- Dry soil 25–100 cm: $\lambda = 0.30$, $C = 1.3\times 10^{6}$.
- Subsoil 100–200 cm: $\lambda = 0.50$, $C = 1.8\times 10^{6}$.

**Concrete roof** (3 layers, 2 m total):
- Concrete deck 0–10 cm: $\lambda = 1.50$, $C = 2.1\times 10^{6}$.
- Mineral-wool insulation 10–20 cm: $\lambda = 0.04$, $C = 0.08\times 10^{6}$. The $\lambda$ jumps by a factor of 37 going down.
- Drywall/wood interior 20–200 cm: $\lambda = 0.15$, $C = 1.5\times 10^{6}$.

**Bare soil** (uniform): $\lambda = 0.30$, $C = 1.3\times 10^{6}$ throughout.

These three substrates intentionally span very different behaviours: a moderately conductive surface over a heterogeneous subgrade (asphalt); moderately conductive over an extreme insulator (roof); uniform low-conductivity reference (soil).

### 7.3 §3.3 — The surface energy balance and Newton iteration

#### The SEB and what each term does

$$
\boxed{\;R_{n}(T_{s}^{0}) - H(T_{s}^{0}) - LE(T_{s}^{0}) - G(T_{s}^{0}) \;=\; 0\;}
$$

Components:

$$
R_{n} \;=\; (1 - \alpha_{s})\,S{\downarrow} \;+\; \varepsilon_{s}\,L{\downarrow} \;-\; \varepsilon_{s}\,\sigma\,(T_{s}^{0})^{4}
$$

- $\alpha_{s}$ — surface albedo (note: same Greek letter as the $\theta$-method weight, but different role). Fraction of $S{\downarrow}$ reflected.
- $S{\downarrow}$ — incoming shortwave (W/m²).
- $\varepsilon_{s}$ — surface longwave emissivity (= absorptivity by Kirchhoff's law).
- $L{\downarrow}$ — incoming sky longwave.
- $\sigma = 5.67\times 10^{-8}\,\mathrm{W\,m^{-2}\,K^{-4}}$ — Stefan–Boltzmann constant.
- $(T_{s}^{0})^{4}$ — the fourth power that makes the SEB *nonlinear*.

$$
H \;=\; \rho\,c_{p}\,\frac{T_{s}^{0} - T_{a}}{r_{a}},\qquad r_{a} \;=\; \frac{1}{C_{H}\,U}.
$$

- $\rho \approx 1.2$ kg/m³ — air density.
- $c_{p} = 1005$ J/(kg K) — specific heat at constant pressure.
- $T_{a}$ — 2-metre air temperature (K).
- $r_{a}$ — aerodynamic resistance (s/m). Smaller $r_{a}$ means stronger surface-to-air coupling.
- $C_{H} = 5\times 10^{-3}$ — bulk transfer coefficient.
- $U = 3$ m/s — wind speed (constant).

$$
LE \;=\; 0 \quad (\text{strict-impervious assumption}).
$$

$$
G \;=\; \lambda_{1/2}\,\frac{T_{s}^{0} - T_{1}}{z_{1} - z_{0}} \quad (\text{ground heat flux at the top half-level}).
$$

#### Why the SEB is nonlinear

The $(T_{s}^{0})^{4}$ Stefan–Boltzmann term makes the SEB nonlinear in $T_{s}^{0}$. We cannot rearrange to put $T_{s}^{0}$ on one side. We must find the root of $F(T_{s}^{0}) = R_{n} - H - LE - G$ as a function of $T_{s}^{0}$.

#### Newton's method derived from the linear approximation

Start with a guess $T_{s,\mathrm{old}}^{0}$. Approximate $F$ linearly around that point:

$$
F(T) \;\approx\; F(T_{s,\mathrm{old}}^{0}) \;+\; F'(T_{s,\mathrm{old}}^{0})\,(T - T_{s,\mathrm{old}}^{0}).
$$

Set this approximation to zero and solve for $T$:

$$
T_{s,\mathrm{new}}^{0} \;=\; T_{s,\mathrm{old}}^{0} \;-\; \frac{F(T_{s,\mathrm{old}}^{0})}{F'(T_{s,\mathrm{old}}^{0})}.
$$

This is one Newton step. Iterate until $|T_{s,\mathrm{new}}^{0} - T_{s,\mathrm{old}}^{0}| < 10^{-4}\,\mathrm{K}$. Newton has **quadratic convergence near the root** — the number of correct digits roughly doubles per iteration. From a warm start (previous time step's $T_{s}^{0}$), 3–5 iterations suffice.

#### The full analytical Jacobian

$$
\frac{dF}{dT_{s}} \;=\; \frac{dR_{n}}{dT_{s}} \;-\; \frac{dH}{dT_{s}} \;-\; \frac{dG}{dT_{s}}.
$$

Term by term:

$$
\frac{dR_{n}}{dT_{s}} \;=\; -4\,\varepsilon_{s}\,\sigma\,(T_{s}^{0})^{3} \quad (\text{only the Stefan–Boltzmann term depends on }T_{s}^{0}).
$$

$$
\frac{dH}{dT_{s}} \;=\; \frac{\rho\,c_{p}}{r_{a}}.
$$

$$
\frac{dG}{dT_{s}} \;=\; \frac{\lambda_{1/2}}{z_{1} - z_{0}}.
$$

All three are smooth functions of $T_{s}^{0}$. The analytical Jacobian gives full Newton convergence. A finite-difference Jacobian would introduce noise — at small $\delta$, floating-point cancellation; at large $\delta$, linear approximation breaks down near the root.

### 7.4 §3.4 — Synthetic forcing

With $\omega = 2\pi/86\,400\,\mathrm{s}^{-1}$:

$$
S{\downarrow}(t) \;=\; \max\bigl[1000\,\cos(\omega(t - 12\,\mathrm{h})),\; 0\bigr]\ \mathrm{W\,m^{-2}}\quad (\text{peak noon, zero night}),
$$

$$
L{\downarrow}(t) \;=\; 350 + 20\,\cos(\omega(t - 14\,\mathrm{h}))\ \mathrm{W\,m^{-2}}\quad (\text{peak 14:00 LT}),
$$

$$
T_{a}(t) \;=\; 292.5 + 7.5\,\cos(\omega(t - 14\,\mathrm{h}))\ \mathrm{K}\quad (\text{peak 14:00 LT}),
$$

$$
U(t) \;=\; 3\ \mathrm{m\,s^{-1}}\quad (\text{constant}).
$$

Why 14:00 peak for $T_{a}$ and $L{\downarrow}$ but 12:00 for $S{\downarrow}$? In reality, the air takes ~2 hours to respond to peak solar input — the surface heats during the morning, transfers heat to the air via $H$, and the air mass reaches its maximum in early afternoon. The 2-hour lag is a standard simplification.

### 7.5 §3.5 — Initialization

$$
T(z, 0) \;=\; T_{\text{mean}} \;+\; A_{0}\,e^{-z/d_{\text{top}}}\,\cos(-z/d_{\text{top}}),\qquad d_{\text{top}} \;=\; \sqrt{\frac{2\,\kappa_{\text{top}}}{\omega}},
$$

with $T_{\text{mean}} = 292.5\,\mathrm{K}$, $A_{0} = 7.5\,\mathrm{K}$, and $\kappa_{\text{top}} = \lambda_{\text{top}}/C_{\text{top}}$ from the topmost layer. This is the analytical damping-depth solution evaluated at $t = 0$.

There is a 12-hour phase mismatch: this initial profile assumes the surface is at peak temperature at $t = 0$, but the SEB-driven cycle peaks at 14:00 LT. So the column carries a transient that decays during day 1. By the start of day 2 the column has equilibrated; day 2 is what we use for diagnostics.

### 7.6 §3.6 — Test 1 vs Test 2 setups

**Test 1 (verification):** uniform sandy-loam column, 1 cm uniform grid, $T_{s}^{0}(t) = T_{\text{mean}} + A_{0}\cos(\omega t)$ prescribed. Six configurations: FTCS at $\nu = 0.4$ and $\nu = 0.6$ (the latter expected to blow up); BTCS and CN at $\Delta t = 300\,\mathrm{s}$ ($\nu \approx 0.69$) and $\Delta t = 900\,\mathrm{s}$ ($\nu \approx 2.08$). Each runs 5 days; day-5 diagnostics vs analytical solution.

**Test 2 (prognostic SEB):** three substrates × three schemes × three time steps $\Delta t \in \{15, 60, 600\}\,\mathrm{s}$ = 27 cells. $\Delta t = 15\,\mathrm{s}$ is below FTCS bound on all three substrates (high-resolution reference). $\Delta t = 60\,\mathrm{s}$ is a typical mesoscale time step. $\Delta t = 600\,\mathrm{s}$ is a typical regional/climate-model time step.

---

## Part 8. Walking through §4 — Results

### 8.1 §4.1 — Damping-depth verification

#### The analytical solution and the $\pi/4$ phase lead

For a semi-infinite uniform substrate with sinusoidal Dirichlet forcing $T_{s}(0, t) = \bar T + A\cos\omega t$:

$$
\boxed{\;T_{s}(z, t) \;=\; \bar T + A\,e^{-z/d}\,\cos(\omega t - z/d),\qquad d = \sqrt{2\kappa/\omega}\;}
$$

$$
\boxed{\;G(0, t) \;=\; \lambda\,\frac{A}{d}\,\sqrt{2}\,\cos(\omega t + \pi/4)\;}
$$

**Where do these come from?** Try $T(z, t) = \bar T + \mathrm{Re}[A\,e^{i(\omega t - K z)}]$. Substitute into $\partial T/\partial t = \kappa\,\partial^{2}T/\partial z^{2}$:

$$
i\omega \;=\; -\kappa\,K^{2}\quad\Rightarrow\quad K^{2} = -i\omega/\kappa.
$$

Take $K = (1 - i)/d$ with $d = \sqrt{2\kappa/\omega}$. Then $-iKz = -(1+i)z/d \cdot i$... after careful algebra (treating real and imaginary parts) we get the real solution above.

The flux at the surface:

$$
G(0,t) \;=\; -\lambda\,\frac{\partial T}{\partial z}\Big|_{z=0} \;=\; \lambda\,\frac{A}{d}\,(\cos\omega t - \sin\omega t) \;=\; \lambda\,\frac{A}{d}\,\sqrt{2}\,\cos(\omega t + \pi/4),
$$

using $\cos x - \sin x = \sqrt{2}\cos(x + \pi/4)$.

**Physical meaning of $\pi/4$ lead.** $G$ peaks $\pi/4$ in phase before $T_{s}$ peaks. For a 24-hour period, $\pi/4$ of 24 h = 3 hours. So if $T_{s}$ peaks at noon, $G$ peaks at 9 AM — the substrate absorbs heat fastest in mid-morning when the surface is still warming most rapidly (steepest gradient at $z = 0$). At noon, when $T_{s}$ has already reached its peak, $G$ has already declined.

#### Reading Table 1

Six configurations on uniform sandy loam, day-5 errors at $z = 10\,\mathrm{cm}$:

| Configuration | $\Delta t$ (s) | $\nu$ | RMSE T (K) | RMSE G (W/m²) |
|---|---|---|---|---|
| FTCS, $\nu = 0.4$ | 173.4 | 0.40 | 0.007 | 3.15 |
| FTCS, $\nu = 0.6$ (unstable) | 259.9 | 0.60 | BLEW UP at step 53 | — |
| BTCS, $\Delta t = 300$ | 300.0 | 0.69 | 0.024 | 3.31 |
| CN, $\Delta t = 300$ | 300.0 | 0.69 | 0.005 | 3.17 |
| BTCS, $\Delta t = 900$ | 900.0 | 2.08 | 0.062 | 3.61 |
| CN, $\Delta t = 900$ | 900.0 | 2.08 | 0.006 | 3.17 |

- FTCS at $\nu = 0.6$: blew up at step 53. Predicted growth $|A_{\mathrm{FTCS}}(0.6, \pi)| = 1.4$ per step. After 53 steps: $1.4^{53} \approx 5.5\times 10^{7}$.
- BTCS error grows roughly linearly: $0.024$ at 300 s, $0.062$ at 900 s — ratio 2.6 (close to the 3.0 expected for first-order in $\Delta t$).
- CN error stays flat: $0.005$ → $0.006$. Empirical demonstration of CN's *second-order* accuracy.
- $\mathrm{RMSE}_{G} \approx 3$ W/m² regardless of scheme — a *spatial-discretisation residual* (analytical $G$ uses exact $\partial T/\partial z|_{0}$, numerical uses $(T_{0} - T_{1})/\Delta z$). All stable schemes share this residual; mesh refinement would reduce it.

### 8.2 §4.2 — Three-substrate prognostic SEB results

#### Reading Figure 3 (schemes agree at $\Delta t = 15$ s)

Day-2 surface temperature evolution at $\Delta t = 15\,\mathrm{s}$ for all three schemes on each substrate. Three curves overlay to within line thickness on every substrate — the schemes are visually indistinguishable. *When $\Delta t$ is small enough, the choice of scheme does not matter.*

What does differ between substrates is the peak $T_{s}^{0}$:

- Asphalt peaks at $\sim 50\,^{\circ}\mathrm{C}$ around 1 PM.
- Concrete roof at $\sim 45\,^{\circ}\mathrm{C}$ — higher albedo (0.30) reflects more solar.
- Bare soil at $\sim 51\,^{\circ}\mathrm{C}$ — surprisingly the highest, despite moderate albedo (0.20).

**Why bare soil is hottest.** Bare soil has the lowest $\kappa$ ($2.31\times 10^{-7}$). Absorbed energy cannot diffuse downward fast enough — combined with $LE = 0$, energy concentrates at the surface and pushes $T_{s}^{0}$ higher. Asphalt's higher $\kappa$ spreads the heat downward more easily; concrete's high albedo reduces the absorbed energy in the first place.

#### Reading Figure 4 (schemes diverge at $\Delta t = 600$ s)

Day-2 ground heat flux $G(t)$ at $\Delta t = 600\,\mathrm{s}$ vs FTCS reference at $\Delta t = 15\,\mathrm{s}$:

- FTCS at $\Delta t = 600\,\mathrm{s}$ blows up on asphalt and roof (annotated in figure).
- BTCS overshoots the daytime $G$ peak by $\sim 40\%$ on asphalt and roof, $19\%$ on soil.
- CN overshoots by $\sim 21\%$ on asphalt, $26\%$ on roof, $10\%$ on soil — about half of BTCS.

**Why FTCS is stable on bare soil but not paved at $\Delta t = 600$ s.** Soil top cell: $\Delta z = 1\,\mathrm{cm}$, $\kappa = 2.3\times 10^{-7}$, so $\Delta t_{\text{crit}} \approx 217\,\mathrm{s}$. At $\Delta t = 600\,\mathrm{s}$, $\nu \approx 1.4$ — over the bound but only modestly. Why doesn't it blow up? The smooth initial profile and smooth Dirichlet boundary do not strongly excite the worst 2-$\Delta z$ wave; the modest growth rate per step does not compound enough to overflow within 2 days. On asphalt with $\nu \approx 18$, growth rate $|1 - 4(18)| = 71$ per step compounds to $71^{N}$ within a handful of steps.

#### Reading Figure 5 (vertical profiles in the asphalt column)

Three local times on day 2 (06:00, 12:00, 18:00):

- 06:00 (steady cooling): all schemes agree closely.
- 12:00 (peak heating): BTCS and CN slightly warmer than reference near the surface.
- 18:00 (immediately after sunset): largest divergence. BTCS at $\Delta t = 600\,\mathrm{s}$ holds the surface $\sim 2\,\mathrm{K}$ above reference, with deviation concentrated in the top 5 cm — the asphalt layer.

**Why divergence is largest after sunset.** That is when $T_{s}^{0}$ swings most rapidly. The operator-splitting error (Part 9.2) is largest when $T_{s}^{0}$ swings fastest between sub-step A and sub-step B.

### 8.3 §4.3 — Cross-substrate quantitative summary (Table 2)

Each cell of Table 2 reports the triplet $A_{G}/A_{\text{ref}}$ / $\mathrm{RMSE}_{T_{s}}$ / $S/S_{\text{ref}}$, where:

- $A_{G}/A_{\text{ref}}$ — diurnal $G$ amplitude normalised to the FTCS $\Delta t = 15\,\mathrm{s}$ reference. Value 1.000 = perfect; 1.400 = over-amplified by 40%.
- $\mathrm{RMSE}_{T_{s}}$ — root-mean-squared error of $T_{s}^{0}$ across the 24-hour day-2 cycle, in K.
- $S/S_{\text{ref}}$ — daily storage integral $S = \int G\,dt$ over day 2, normalised. If $S/S_{\text{ref}} \approx 1$, the daily mean storage is preserved across schemes.

**Three patterns:**

1. **Substrate ordering at $\Delta t = 600\,\mathrm{s}$.** RMSE is largest for concrete roof (3.69 BTCS, 2.10 CN), middle for asphalt (2.10 BTCS, 1.12 CN), smallest for bare soil (0.53 BTCS, 0.28 CN). The κ_top values: soil $2.31$, asphalt $3.75$, roof $7.14$ (all $\times 10^{-7}$). *Error scales with* $\kappa_{\text{top}}$ — the same parameter that sets the FTCS stability bound.

2. **Scheme ordering.** At fixed substrate and $\Delta t$, CN errors are roughly half of BTCS errors. The factor-of-two improvement.

3. **Storage preservation.** $S/S_{\text{ref}}$ stays within $\pm 5\%$ of unity (largest deviation 0.958, a 4.2% deficit, for concrete roof BTCS at $\Delta t = 600\,\mathrm{s}$). Even when diurnal $G$ amplitude is over-amplified by 40%, the daily mean is preserved. The over-amplification is symmetric in day/night.

---

## Part 9. Walking through §5 — Discussion

### 9.1 §5.1 — Why FTCS stability is set by the most thermally stiff layer

On a stretched-grid layered substrate, the FTCS stability constraint applies cell by cell: $\nu_{j} = \kappa_{j}\Delta t/\Delta z_{j}^{2} \le 1/2$ for every $j$. The cell with the smallest $\Delta z_{j}^{2}/\kappa_{j}$ sets the bound:

| Substrate | Stiffest cell | $\Delta z$ | $\kappa$ | $\Delta t_{\text{crit}}$ |
|---|---|---|---|---|
| Asphalt | top asphalt cell | 0.5 cm | $3.75\times 10^{-7}$ | 33 s |
| Concrete roof | concrete deck top cell | 0.5 cm | $7.14\times 10^{-7}$ | 17 s |
| Bare soil | top sandy-loam cell | 1.0 cm | $2.31\times 10^{-7}$ | 217 s |

*Inverse* of naive intuition: the most diffusive substrate (concrete) is the most restrictive, not the least. The phrase "thermally stiff" means a system whose time-step constraint is set by the fastest-evolving component, even if that component is small. The topmost cm of concrete is the fastest-responding component and sets the stiff bound.

> **[Notes #11, Misconception #1]** says: "Higher resolution will not always lead to more accurate forecasts" — high resolution requires consistent surface fields, realistic physics, and adequate observations. The project's result inverts this: high resolution is not optional once you accept the cm-scale damping depth, and FTCS becomes structurally infeasible. So the lecture's "high resolution does not solve everything" misconception manifests here as: high resolution forces you to give up explicit time stepping.

### 9.2 §5.2 — The operator-splitting error, derived

This is the most subtle physical argument in the report. The amplitude inflation of $G$ at large $\Delta t$ is **not** explained by the von Neumann picture (BTCS damps everything; one would expect under-amplification). The real explanation is **operator splitting**.

#### How the splitting works in the code

Each time step has two sub-steps in sequence:

- **Sub-step A — column update.** Hold $T_{s}^{0}$ fixed at its current value (= start-of-step). Solve the heat conduction equation in the column for one $\Delta t$. New interior temperatures $T_{1}^{n+1}, T_{2}^{n+1}, \ldots$.
- **Sub-step B — SEB update.** With new interior values fixed (especially $T_{1}^{n+1}$), solve the SEB by Newton iteration for new $T_{s}^{0}$.

During sub-step A, the column relaxed to equilibrium with $T_{s}^{0}$ from the *start* of the step. In sub-step B the SEB jerks $T_{s}^{0}$ to its new value — but the column does not re-respond within the same step. The column has *over-relaxed* relative to where it should be at the end of the step.

#### Why this produces over-amplification in BTCS

Consider sunset. $T_{s}^{0}$ drops fast — say from 35 °C to 25 °C in one $\Delta t = 600\,\mathrm{s}$. With column-then-SEB ordering, sub-step A holds $T_{s}^{0}$ at 35 and the column relaxes to that. Sub-step B computes new $T_{s}^{0} = 25$. But the column is still mostly equilibrated to 35 — $T_{1}$ has not updated. The gradient at the top half-level is $(T_{s}^{0} - T_{1})/(z_{1} - z_{0})$ with $T_{s}^{0} = 25$ and $T_{1}$ effectively at 35. Gradient is much steeper than the true coupled solution would have. $G$ is correspondingly larger in magnitude. *That is the over-amplification.*

BTCS evaluates the diffusion operator entirely at the post-swing temperature, so it amplifies this gradient steepening the most. CN evaluates half-old, half-new, so half the swing is cancelled — CN's error is half of BTCS's.

> **[Notes #10 §8 "The Order of the Processes"]** says: *"running an implicit fast process first, without including the other tendencies, drives the system toward an equilibrium with respect to only one process — the wrong equilibrium."* This is exactly the project's column-first-then-SEB pathology. The lecture's prescribed cure: **fully coupled solution** of the strongly interacting processes, or careful coupling. Notes #10 specifically warns that "with more than one implicit process there is no real solution to the ordering problem" — different orderings give different answers.

#### Why both BTCS and CN show first-order scaling

The operator-splitting error is first-order in $\Delta t$ regardless of the per-substep scheme: gradient error scales linearly with how far $T_{s}^{0}$ has swung between updates, which scales linearly with $\Delta t$. So even CN (intrinsically second-order) ends up showing first-order scaling because the splitting error dominates.

#### Reading Table 3

Six rows (3 substrates × 2 schemes; FTCS absent because at $\Delta t = 600\,\mathrm{s}$ on asphalt and roof it blows up):

| Surface | Scheme | RMSE at 60 s | RMSE at 600 s | Ratio |
|---|---|---|---|---|
| Asphalt | BTCS | 0.225 | 2.104 | 9.4 |
| Asphalt | CN | 0.114 | 1.115 | 9.8 |
| Roof | BTCS | 0.450 | 3.686 | 8.2 |
| Roof | CN | 0.229 | 2.102 | 9.2 |
| Soil | BTCS | 0.053 | 0.529 | 9.9 |
| Soil | CN | 0.027 | 0.279 | 10.2 |

All six ratios in $[8.2, 10.2]$ — first-order range. Second-order would give $\sim 100$. The fact that CN shows ratios near 10 not 100 is the empirical confirmation that operator splitting dominates over the per-substep scheme.

### 9.3 §5.3 — Why $\kappa_{\text{top}}$ dominates substrate dependence

If admittance $\mu = \sqrt{\lambda C}$ alone explained the substrate ordering, asphalt:roof error ratio would be $\sim 1\!:\!1.5$ (since $\mu_{\text{asphalt}} \approx 1220$ and $\mu_{\text{roof}} \approx 1770$). Empirical ratio is closer to $1\!:\!1.75$. Bare soil with $\mu \approx 624$ — about half asphalt's — has scheme error one *quarter* of asphalt's, not one half. So admittance alone does not explain it.

§6 SHAP attribution identifies $\kappa_{\text{top}}$ as the dominant predictor: 92% of variance from $\kappa_{\text{top}}$ alone.

### 9.4 §5.4 — Implications, limitations, outlook

#### UHI implication: diurnal range bias, not mean bias

Storage ratios within ±5% confirm symmetric day/night over-amplification. So over-amplified $G$ does not bias the daily-mean nocturnal warm anomaly, but it inflates its diurnal range. For a mesoscale model running at $\Delta t = 60\,\mathrm{s}$ with BTCS: 4–6% nocturnal $G$ inflation on asphalt and concrete, 2% on bare soil. At $\Delta t = 600\,\mathrm{s}$: 40% and 20%.

> **[Notes #11, Misconception #8]** notes that surface conditions in models are not directly forecast but diagnosed from a balance, and errors in any budget component propagate to near-surface temperature. The project gives a quantitative example of this: errors in the *numerical* treatment of $G$ (not in the physics) propagate to the simulated UHI diurnal range.

#### The four numbered limitations

(i) $LE = 0$ — strict-impervious. Realistic for new pavement, underestimates real cities.
(ii) Symmetric synthetic forcing — real cities show asymmetric morning warming, slow evening cooling.
(iii) Independent columns — a real urban canopy is a tile-weighted mix of facets.
(iv) Constant $U = 3\,\mathrm{m/s}$ — under time-varying $U$ the Newton SEB Jacobian would need updating each step.

#### How to remove the splitting error

**Fully-coupled SEB-row solve** — augment the tridiagonal system with one extra row representing the SEB residual at the surface. Newton linearisation lets us assemble the linearised SEB into the column system. The two processes are no longer split. First-order splitting error vanishes; CN with this fix recovers its formal second-order accuracy.

**Strang splitting** — replace the standard column-then-SEB ordering A-B at full $\Delta t$ with a symmetric A($\Delta t/2$)-B($\Delta t$)-A($\Delta t/2$) sandwich. Leading splitting error cancels by symmetry, leaving $O(\Delta t^{2})$. Cheaper than fully-coupled solution.

---

## Part 10. Walking through §6 — Independent SHAP attribution

### 10.1 What problem §6 is solving

The mechanistic argument of §5 ranks $\kappa_{\text{top}}$, admittance $\mu$, and layer-interface descriptors as candidate predictors of BTCS coarse-$\Delta t$ error. The three idealised substrates differ in all three properties simultaneously, so a three-substrate comparison cannot disentangle which is dominant. §6 fixes this by sampling 150 random columns and using machine learning to identify the dominant predictor across a wider parameter space.

### 10.2 §6.1 — The synthetic ensemble

150 three-layer substrate columns sampled from a wide prior:

- Top-layer $\lambda \in [0.10, 2.50]\,\mathrm{W\,m^{-1}\,K^{-1}}$.
- Middle-layer $\lambda \in [0.05, 2.50]$ (covers the rigid-insulation extreme).
- Bottom-layer $\lambda \in [0.10, 1.00]$.
- All $C \in [0.5, 3.0]\times 10^{6}\,\mathrm{J\,m^{-3}\,K^{-1}}$.
- Top thickness 2–15 cm; middle 5–30 cm; bottom to 200 cm.

Each column run at BTCS $\Delta t = 600\,\mathrm{s}$ and BTCS reference at $\Delta t = 15\,\mathrm{s}$ for two diurnal cycles. Day-2 surface-temperature RMSE between the two is the target $y$.

#### Six substrate descriptors (features)

- Bulk admittance $\mu_{\text{eff}} = \sqrt{\lambda_{\text{eff}}\,C_{\text{eff}}}$, depth-weighted over top 30 cm.
- Top-cell diffusivity $\kappa_{\text{top}} = \lambda_{\text{top}}/C_{\text{top}}$.
- Max $\lambda$-contrast across any internal interface.
- Number of significant interfaces (contrast > 1.5).
- Depth of first significant interface.
- Top-layer thickness $h_{\text{top}}$.

### 10.3 §6.2 — Gradient-boosted regression and SHAP

#### What is gradient boosting?

A machine-learning regression method that builds an ensemble of small decision trees, each trying to correct the errors of the previous one:

- Start with constant prediction $\hat y_{0} = \overline{y}$.
- At iteration $m$, fit a small decision tree to the residuals $y - \hat y_{m-1}$. Add the tree's output, scaled by learning rate $\eta$:

$$
\hat y_{m} \;=\; \hat y_{m-1} \;+\; \eta\,\mathrm{tree}_{m}(x).
$$

- Repeat for $M$ iterations. Final: $\hat y_{M} = \hat y_{0} + \sum_{m=1}^{M} \eta\,\mathrm{tree}_{m}(x)$.

Project: $M = 200$, max depth 3, $\eta = 0.05$. Six features → one target. Captures nonlinearity and feature interactions automatically.

#### What is SHAP?

**SHAP — SHapley Additive exPlanations** — a method for assigning each feature a fair contribution to each prediction. From cooperative game theory: in a coalition of players (features), each is paid in proportion to its marginal contribution averaged over all possible orderings. Lloyd Shapley proved (1953) this is the unique fair allocation satisfying four axioms (efficiency, symmetry, dummy, additivity).

For each prediction $\hat y(x)$ and each feature $f$, SHAP computes a value $\phi_{f}(x)$ such that

$$
\hat y(x) \;=\; \text{baseline} \;+\; \sum_{f}\,\phi_{f}(x).
$$

Positive $\phi$ means feature $f$ pushed the prediction up; negative means down. Aggregating: **mean** $|\phi_{f}|$ gives a global feature-importance ranking.

For tree ensembles, SHAP values are computed exactly in polynomial time via TreeExplainer.

#### Model fit metrics

- In-sample $R^{2} = 0.96$ (model fits training data well).
- 5-fold CV $R^{2} = 0.61$ (model generalises moderately; ~40% variance not captured by six descriptors).

The reason both are reported is intellectual honesty: in-sample is too optimistic; CV is realistic. Feature ranking is robust under both; absolute SHAP magnitudes have noise consistent with the gap.

### 10.4 §6.3 — The findings

Figure 6 has four panels:

- **(a)** Mean $|\mathrm{SHAP}|$ for full feature set. $\kappa_{\text{top}}$ tallest at 0.71 K. $\mu_{\text{eff}}$ and max $\lambda$-contrast tied at 0.18–0.20 K. Others smaller.
- **(b)** SHAP dependence on $\kappa_{\text{top}}$, points coloured by $\mu_{\text{eff}}$. Monotone, near-log-linear positive: higher $\kappa_{\text{top}}$ → larger SHAP value. Colour-by-$\mu_{\text{eff}}$ shows interaction.
- **(c)** Residual SHAP after $\kappa_{\text{top}}$ partialled out. $\mu_{\text{eff}}$ dominates the residual.
- **(d)** Predicted vs observed RMSE. Tight 1:1 line.

**Why $\kappa_{\text{top}}$? The mechanistic connection.** Same $\kappa_{\text{top}}$ that sets the FTCS stability bound also sets the prefactor of the BTCS coarse-$\Delta t$ operator-splitting error. Higher $\kappa_{\text{top}}$ → top cell relaxes to $T_{s}^{0}$ faster within sub-step A → larger gradient swing between sub-steps → larger splitting error. The connection is mechanistic, not coincidence.

### 10.5 §6.4 — Limitations of the attribution

- Fixed grid ($\Delta z_{\text{top}} = 0.5\,\mathrm{cm}$) means we cannot separate $\kappa_{\text{top}}$ from the dimensionless ratio $\Delta t\,\kappa_{\text{top}}/\Delta z_{\text{top}}^{2}$.
- $N = 150$ small for ML; CV $R^{2} = 0.61$ reflects this. Feature ranking robust at this $n$; absolute magnitudes have noise.
- Forcing-specific (synthetic SEB, $LE = 0$); transfer to real-forcing runs may not be quantitative but qualitative ranking likely robust.

---

## Part 11. Walking through §7 — Conclusions

The five conclusion bullets recap everything. Each repeats material we have already unpacked.

**(i) FTCS conditional stability.** $\nu \le 1/2$. On a stretched-grid layered substrate the bound is set by the most thermally stiff layer: $\Delta t_{\text{crit}}$ of 33 s on asphalt, 17 s on concrete. Implication: implicit treatment of vertical conduction is structurally required.

**(ii) BTCS and CN unconditionally stable.** At $\Delta t = 600\,\mathrm{s}$, BTCS over-amplifies the diurnal $G$ amplitude by 40% on asphalt, 41% on roof, 19% on soil. CN halves these to 21%, 26%, 10%. RMSE up to 3.7 K on the roof.

**(iii) Operator-splitting error is dominant.** Both BTCS and CN show $\Delta t$-refinement ratios near 10:1 (first-order). Even CN shows first-order scaling because splitting dominates over per-substep scheme order. CN's factor-of-two improvement is a prefactor effect.

**(iv) Daily storage preserved within ±5%.** Bias is in diurnal range of simulated UHI, not in daily mean.

**(v) $\kappa_{\text{top}}$ dominates SHAP attribution.** $R^{2} = 0.92$ from $\kappa_{\text{top}}$ alone over 150 synthetic columns. Mechanism: same parameter that sets the FTCS bound sets the splitting-error prefactor.

**Closing.** Two follow-ups: fully-coupled SEB-row solve (the lecture-prescribed cure for operator-splitting errors), or Strang splitting (cheaper alternative recovering second-order accuracy in the splitting). Longer-term outlook: coupling this diagnostic framework to an offline run of WRF-SLUCM or WRF-TEB for a real city.

---

## Part 12. Mastery cheat-sheet

### 12.1 The single most important sentence

*"The dominant error in BTCS at $\Delta t = 600\,\mathrm{s}$ is not the within-substep truncation error; it is the operator-splitting error between the column update and the SEB update, which is first-order in $\Delta t$ regardless of the per-substep scheme."*

Everything else — the von Neumann analysis, the substrate ordering, the SHAP attribution — is a supporting argument for this sentence.

### 12.2 The three numbers to memorise

1. $\Delta t_{\text{crit}} = 17\,\mathrm{s}$ for the concrete deck top cell ($\Delta z = 5\,\mathrm{mm}$, $\kappa = 7.14\times 10^{-7}$). The "$\Delta t < \tfrac{1}{2}\Delta z^{2}/\kappa$" formula made concrete.
2. BTCS over-amplifies the diurnal $G$ amplitude by **40%** on asphalt at $\Delta t = 600\,\mathrm{s}$. CN halves this to **21%**.
3. $\kappa_{\text{top}}$ alone explains $R^{2} = 0.92$ of the BTCS coarse-$\Delta t$ error variance across 150 synthetic substrates.

### 12.3 The five concepts you must define on demand

- **Diurnal damping depth** $d = \sqrt{2\kappa/\omega}$. Depth at which the daily wave decays to $e^{-1} \approx 37\%$ of surface amplitude.
- **Diffusion number** $\nu = \kappa\Delta t/\Delta z^{2}$. Dimensionless control parameter for FTCS stability — bound $\nu \le 1/2$.
- **Harmonic mean conductivity** $\lambda_{j+1/2} = 2\lambda_{j}\lambda_{j+1}/(\lambda_{j} + \lambda_{j+1})$. Preserves heat flux exactly across a $\lambda$ discontinuity.
- **Operator splitting / wrong-equilibrium pathology.** Sub-step-A relaxes the column to start-of-step $T_{s}^{0}$; sub-step-B updates $T_{s}^{0}$; the column does not see the swing within the same step.
- **SHAP value.** Fair allocation, from cooperative game theory, of feature contribution to a prediction. Mean $|\mathrm{SHAP}|$ over the dataset is a global feature-importance ranking.

### 12.4 Common follow-up questions and the right answers

**Q: Why CN over BTCS?** A: CN is second-order in time intrinsically and cuts the BTCS coarse-$\Delta t$ error in half. Remaining error is operator splitting, which both share. CN gives "BTCS for free" until you fix the splitting.

**Q: Why does FTCS work on bare soil at $\Delta t = 600\,\mathrm{s}$ but not asphalt?** A: $\nu \approx 1.4$ on soil (over the bound, but smooth forcing keeps the unstable mode small) vs $\nu \approx 18$ on asphalt (so far over the bound that the noise compounds within a few steps).

**Q: Why is bare soil error a quarter of asphalt error, not half?** A: The operator-splitting error scales with $\kappa_{\text{top}}$, not admittance. Soil $\kappa_{\text{top}}$ is about 60% of asphalt's — but the splitting error is nonlinear, and SHAP confirms $\kappa_{\text{top}}$ alone accounts for 92% of variance.

**Q: Why don't you just remove operator splitting?** A: That is the recommended follow-up — fully coupled SEB-row solve or Strang splitting (Notes #10 §8). Within this project we wanted to characterise the error, not eliminate it. Knowing splitting is the dominant error tells us removing it would give the largest accuracy gain — much bigger than switching from BTCS to CN.

### 12.5 Lecture-notes index for this project

| Project section | Lecture-note source |
|---|---|
| §2.1 conductivity-form heat equation | [Notes #2] PDE classification |
| §2.2 staggered grid, half-levels | [Notes #8] Staggered Grid |
| §2.3 $\theta$-method (FTCS, BTCS, CN) | [Notes #6 §6 (Slides 15–17)] Single-Stage Two-Level Schemes |
| §2.5 von Neumann analysis | [Notes #6 §10] + [Notes #9 Pure Diffusion / Implicit Diffusion] |
| §3.3 tridiagonal solver | [Notes #9 Practical Considerations] |
| §5.1 stability layer-by-layer | [Notes #11 Misconception #1] |
| §5.2 operator-splitting error | [Notes #10 §8] The Order of the Processes |
| §5.4 UHI diagnostic interpretation | [Notes #11 Misconception #8] |

### 12.6 Homework index for this project

| Project topic | Your HW work |
|---|---|
| FTCS blow-up | [HW1] FTCS blew up at step 113 on tracer advection |
| Amplification factors $\|A_{k}\|$ vs wavenumber | [HW4] $\|A_{k}\|$ vs $k\Delta x$ for various CFL numbers |
| Three-scheme comparison (Euler/Backward/Trapezoidal) | [HW3] Same three on the oscillation equation $d\psi/dt = i\omega\psi$ |
| Staggered grid | [HW5] Numerical phase speed comparison, 2-$\Delta x$ wave |
| Wave amplitude and period diagnostics | [HW2] Sine-wave advection, period & amplitude tracking |

---

*End of document. Companion files: `modified_full_report_1.docx` (the corrected long report), `equations.md` (LaTeX-rendered equation reference), `clarify_project.docx` (the .docx version of this walkthrough).*
