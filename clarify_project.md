# Clarify the Project: A Mastery-Level Walkthrough

*A LaTeX-rendered companion to `modified_full_report_1.docx`. Every concept, every equation, every notation explained from zero, with regular references to the course lecture notes (`Lecture_1_2_3_4_5_6_7_8_9_10_11_Notes.md`) and your six homeworks (HW1–HW6).*

---

## Part 0. How to use this document

This document is built so that anyone — even with zero prior knowledge of numerical modelling, partial differential equations, or surface-energy-balance physics — can read the long report and defend every choice in it. Every Greek letter, every subscript, every equation is opened up and explained.

**Reading recipe.** Read Parts 1–3 in order: they install the language used in the rest of the document. Then open the long report on one screen and this clarification on the other, and walk through them in parallel — when the report mentions §2.5, jump to Part 6.5 here.

**Conventions.**
- Inline math uses `$...$`: e.g. $\nu = \kappa\,\Delta t / \Delta z^2$.
- Display equations use `$$...$$` and are centred on their own line.
- Course-material references use the form **[Notes #6 §6.1]** to mean "Notes #6, Section 6.1".
- Homework references look like **[HW3, Case 3]** — meaning "your HW3 submission, the case labelled Case 3".
- Worked numerical examples are highlighted with the symbol $\boxed{\,\text{example}\,}$.

**The 14 parts.**
- Parts 0–3: foundations.
- Parts 4–11: section-by-section walk through the long report.
- Part 12: mastery cheat-sheet.
- Part 13: glossary of every symbol.
- Part 14: common confusions and how to clear them up.

---

## Part 1. Foundational physics: heat, temperature, and the substrate

### 1.1 What does it mean for the ground to conduct heat?

Imagine a paving stone in the sun. The top is hot — say $50\,^{\circ}\mathrm{C}$. Five centimetres down, the stone is much cooler — say $30\,^{\circ}\mathrm{C}$. There is a *temperature gradient* inside the stone. As long as that gradient exists, heat will flow from the hot top to the cool bottom. This flow is conduction. There is no air movement, no fluid mixing — energy is passed from molecule to molecule through the solid.

The amount of heat that flows per square metre per second is the **conductive heat flux**, denoted $G$ in this project. Its units are watts per square metre, $\mathrm{W\,m^{-2}}$. By convention $G > 0$ means flow downward — into the ground.

To make this less abstract: a typical mid-afternoon $G$ on a sun-warmed asphalt road is about $200\,\mathrm{W\,m^{-2}}$ (positive, into the ground). At night the same surface emits at perhaps $-50\,\mathrm{W\,m^{-2}}$ (negative, out of the ground). Both numbers fit on a small portion of a $1000\,\mathrm{W\,m^{-2}}$ peak insolation, which is why $G$ is "small in the daily mean" but "large in the diurnal range" — the daily-mean value of $G$ is near zero, but the day-to-night swing is hundreds of W/m².

### 1.2 The four key material properties

Every substrate (the generic word for whatever material is below the surface) is described by two material numbers, from which a third (the thermal diffusivity) is derived. The fourth quantity (the diurnal damping depth) is a length scale derived from the diffusivity.

- **Thermal conductivity** $\lambda$ (Greek "lambda"). Units $\mathrm{W\,m^{-1}\,K^{-1}}$. How easily heat flows under a given temperature gradient. Air $\approx 0.025$; rigid foam $\approx 0.03$; dry sandy soil $\approx 0.30$; asphalt $\approx 0.75$; concrete $\approx 1.5$; granite $\approx 3.0$. Bigger $\lambda \Rightarrow$ heat propagates more easily. Read the unit aloud as "watts per metre per Kelvin": for each metre of thickness you traverse, each Kelvin of temperature drop produces $\lambda$ watts of flux per square metre.

- **Volumetric heat capacity** $C$. Units $\mathrm{J\,m^{-3}\,K^{-1}}$. The energy needed to raise one cubic metre of the material by one Kelvin. Water $= 4.18 \times 10^{6}$; concrete $\approx 2.1\times 10^{6}$; dry sandy soil $\approx 1.3\times 10^{6}$. Note water is the universe's record-holder for $C$ — that is why coastal climates are so much milder than inland ones. The factor of $\sim 10^{6}$ in the units is just SI bookkeeping: a cubic metre is $10^{6}\,\mathrm{cm^{3}}$, so the per-cubic-centimetre heat capacity (in $\mathrm{J\,cm^{-3}\,K^{-1}}$) is in the range 1–4, which is more intuitive: it takes roughly 2 joules to warm a cubic centimetre of concrete by a Kelvin.

- **Thermal diffusivity** $\kappa$ (Greek "kappa"). Defined as $\kappa = \lambda / C$. Units $\mathrm{m^{2}\,s^{-1}}$. How quickly a temperature disturbance propagates. For our substrates $\kappa$ is in the range $10^{-7}$ to $10^{-6}\,\mathrm{m^{2}\,s^{-1}}$. The unit is *the same* as the kinematic viscosity of a fluid — both describe how fast something diffuses (heat in one case, momentum in the other). For a length scale $L$ and a time scale $\tau$, $\kappa$ relates them as $L^{2} \sim \kappa\,\tau$. So with $\kappa = 10^{-6}\,\mathrm{m^{2}/s}$ and $\tau = 1\,\mathrm{day} = 86\,400\,\mathrm{s}$, $L \sim \sqrt{86\,400 \times 10^{-6}} \approx 0.3\,\mathrm{m}$ — heat diffuses about 30 cm per day in a high-$\kappa$ substrate. That order-of-magnitude estimate is *exactly* the diurnal damping depth (up to a factor of $\sqrt{4\pi}$).

- **Diurnal damping depth** $d = \sqrt{2\kappa/\omega}$ — units metres. Discussed in Section 1.3 below.

> **Lecture-notes connection.** [Notes #2 — 2nd-Order PDEs] classifies the heat equation explicitly as **parabolic** ($B^{2} - 4AC = 0$) and notes: *"Amplitude decreases; the initial 'pile' of material does not propagate but spreads horizontally, conserving the total quantity under the curve."* That is the physical picture our $\kappa$ controls: $\kappa$ sets the rate of spreading.

### 1.3 The diurnal damping depth — the most important length scale in the project

Suppose the surface temperature varies sinusoidally with a period of 24 hours: hot in the afternoon, cold before sunrise. How does that wave penetrate into the soil? Solving the heat equation in a deep, uniform substrate with a sinusoidal temperature at the surface gives an exact answer (we derive it in Part 8.1): the wave travels downward, but its amplitude decays exponentially with depth. The depth at which the amplitude has decayed to $e^{-1} \approx 37\%$ of its surface value is the **diurnal damping depth**:

$$
\boxed{\;d \;=\; \sqrt{\frac{2\,\kappa}{\omega}},\qquad \omega = \frac{2\pi}{86\,400\ \mathrm{s}} \approx 7.27\times 10^{-5}\ \mathrm{rad\,s^{-1}}\;}
$$

The square-root structure says: faster-diffusing materials (larger $\kappa$) feel the surface signal deeper; faster cycles (larger $\omega$) decay closer to the surface.

For the project's substrates, plug in:

$$\boxed{\,\text{Worked example — bare soil damping depth.}\,}$$

Sandy loam: $\lambda = 0.30\,\mathrm{W\,m^{-1}\,K^{-1}}$, $C = 1.3\times 10^{6}\,\mathrm{J\,m^{-3}\,K^{-1}}$.

$$
\kappa \;=\; \frac{\lambda}{C} \;=\; \frac{0.30}{1.3\times 10^{6}} \;=\; 2.31\times 10^{-7}\ \mathrm{m^{2}\,s^{-1}}.
$$

$$
d \;=\; \sqrt{\frac{2 \times 2.31\times 10^{-7}}{7.27\times 10^{-5}}} \;=\; \sqrt{6.35\times 10^{-3}} \;=\; 0.0797\ \mathrm{m} \;=\; 7.97\,\mathrm{cm}.
$$

Same calculation for the other two substrates:

| Substrate | $\lambda$ | $C$ | $\kappa = \lambda/C$ | $d$ |
|---|---|---|---|---|
| Bare soil | 0.30 | $1.3\times 10^{6}$ | $2.31\times 10^{-7}$ | 7.97 cm |
| Asphalt (top) | 0.75 | $2.0\times 10^{6}$ | $3.75\times 10^{-7}$ | 10.16 cm |
| Concrete deck | 1.50 | $2.1\times 10^{6}$ | $7.14\times 10^{-7}$ | 14.02 cm |

So the daily wave penetrates only the top 8–14 cm in any of these materials. **To capture how the wave decays, our topmost grid cells must be much smaller than $d$ — typically half a centimetre to one centimetre.** This is *why* the project uses a stretched grid with $\Delta z_{0} \approx 0.5\,\mathrm{cm}$ at the surface.

### 1.4 Why $d$ matters for picking time steps

Once we resolve $d$ with cells of thickness $\Delta z \sim 0.5\,\mathrm{cm}$, we run into a constraint on $\Delta t$. For the explicit (FTCS) scheme, the maximum stable time step is

$$
\Delta t_{\max} \;=\; \frac{1}{2}\,\frac{\Delta z^{2}}{\kappa}.
$$

For $\Delta z = 5\,\mathrm{mm} = 0.005\,\mathrm{m}$ and the concrete deck's $\kappa = 7.14 \times 10^{-7}\,\mathrm{m^{2}\,s^{-1}}$:

$$\boxed{\,\text{Worked example — the 17-second problem.}\,}$$

$$
\Delta t_{\max} \;=\; \frac{1}{2}\,\frac{(0.005)^{2}}{7.14\times 10^{-7}} \;=\; \frac{1}{2}\,\frac{2.5\times 10^{-5}}{7.14\times 10^{-7}} \;\approx\; \frac{1}{2}\,\times\,35 \;\approx\; 17\ \mathrm{s}.
$$

Operational mesoscale models run with $\Delta t = 60$–$600\,\mathrm{s}$. At $\Delta t = 60\,\mathrm{s}$ on the concrete deck, FTCS exceeds the bound by a factor of $\sim 4$; at $\Delta t = 600\,\mathrm{s}$ by a factor of $\sim 35$. Explicit time stepping is structurally ruled out.

> **Connecting to your work.** In **[HW1]** you saw the consequence of violating an explicit-stability bound: your FTCS tracer integration *blew up at step 113*, with $\max|q|$ exceeding 10 — the same kind of explosive instability that the project's FTCS at $\Delta t = 600\,\mathrm{s}$ on the asphalt road exhibits in 4–5 steps. The mechanism is identical: $|A| > 1$ at the worst Fourier mode causes geometric growth.

### 1.5 The four-component surface energy balance

Surface temperature $T_{s}^{0}$ is determined not by some external rule but by an energy balance at the surface. Four fluxes meet there:

- $R_{n}$ — net absorbed radiation (sun + sky longwave $-$ surface longwave emission), positive when energy is being deposited.
- $H$ — sensible heat flux to the air, positive when heat leaves the surface upward via warm air rising.
- $LE$ — latent heat flux from evaporation. In this project $LE = 0$ (impervious surfaces).
- $G$ — conductive heat flux into the substrate (positive downward).

Energy conservation requires what arrives equals what leaves:

$$
\boxed{\;R_{n} \;-\; H \;-\; LE \;-\; G \;=\; 0\;}
$$

This is the **surface energy balance** (SEB). Together with the heat equation in the substrate, it determines $T_{s}^{0}$ at every moment. Because $R_{n}$ depends on $T_{s}^{0}$ (through the Stefan–Boltzmann $T^{4}$ outgoing longwave), $H$ depends on $T_{s}^{0}$ (through $T_{s} - T_{a}$), and $G$ depends on $T_{s}^{0}$ (through the gradient at the surface), the SEB is a *single nonlinear equation in one unknown* — perfect for Newton iteration (Part 7.3).

### 1.6 Units and dimensional analysis sanity check

Every equation in the report is dimensionally consistent. As a sanity check:

- $C\,\partial T/\partial t$ has units $\mathrm{(J\,m^{-3}\,K^{-1})(K\,s^{-1})} = \mathrm{J\,m^{-3}\,s^{-1}} = \mathrm{W\,m^{-3}}$ — energy per cubic metre per second (a power density).
- $\partial/\partial z\,[\lambda\,\partial T/\partial z]$ has units $\mathrm{m^{-1}\,(W\,m^{-1}\,K^{-1})\,K\,m^{-1}} = \mathrm{W\,m^{-3}}$. Same units. ✓
- The amplification factor $A$ is dimensionless. ✓
- $\nu = \kappa\,\Delta t/\Delta z^{2}$ has units $\mathrm{(m^{2}\,s^{-1})(s)/(m^{2})} = $ dimensionless. ✓
- $r_{a} = 1/(C_{H}\,U)$ has units $\mathrm{1/(m\,s^{-1})} = \mathrm{s\,m^{-1}}$. ✓
- $H = \rho\,c_{p}\,(T_{s} - T_{a})/r_{a}$: $\mathrm{(kg\,m^{-3})(J\,kg^{-1}\,K^{-1})(K)/(s\,m^{-1})} = \mathrm{W\,m^{-2}}$. ✓

> **[Notes #3 §1 Taylor Series]** is the algebraic foundation of the finite differences we use. **[Notes #3 §3 Definition of the Derivative]** opens with the limit definition $f'(x) = \lim_{h\to 0}[f(x+h) - f(x)]/h$ — exactly what we are approximating with finite differences when we set $h = \Delta x$ and stop taking the limit.

---

## Part 2. From a continuous PDE to a discrete computer program

### 2.1 What is a partial differential equation?

An ordinary differential equation (ODE) describes how something changes with respect to a single variable — usually time. Newton's law of cooling, $\dfrac{dT}{dt} = -k(T - T_{\infty})$, is an ODE.

A partial differential equation (PDE) involves derivatives with respect to more than one variable. Heat conduction in depth is a PDE because $T$ depends on both $z$ and $t$:

$$
\frac{\partial T}{\partial t} \;=\; \kappa\,\frac{\partial^{2} T}{\partial z^{2}}.
$$

A computer cannot solve a PDE in continuous form — it cannot store an infinite number of $T(z, t)$ values. We must replace continuous derivatives with **finite differences** on a discrete grid: a list of cells at depths $z_{0}, z_{1}, \ldots, z_{N-1}$, advanced through time in discrete steps $\Delta t$.

### 2.2 The PDE classification — why heat is parabolic

[Notes #2] classifies linear second-order PDEs by the discriminant $B^{2} - 4AC$ of the general form

$$
A\,u_{xx} \;+\; B\,u_{xy} \;+\; C\,u_{yy} \;+\; \text{lower-order terms} \;=\; 0.
$$

- **Elliptic** ($B^{2} - 4AC < 0$). Example: Laplace's equation $\nabla^{2} u = 0$. Steady-state, no time direction. The atmosphere's pressure field at a given instant satisfies an elliptic-like balance equation.
- **Hyperbolic** ($B^{2} - 4AC > 0$). Example: the wave equation $u_{tt} - c^{2} u_{xx} = 0$, or the advection equation $u_{t} + c\,u_{x} = 0$. Information travels along characteristic curves at finite speed. The atmosphere's gravity waves and acoustic waves are hyperbolic.
- **Parabolic** ($B^{2} - 4AC = 0$). Example: the diffusion equation $u_{t} = \kappa\,u_{xx}$. Has the concept of "forward time" — initial conditions are *forgotten* over time as the diffusion smears them out. Cannot be integrated stably backward in time.

Our heat conduction equation, written as $u_{t} - \kappa\,u_{xx} = 0$, has $A = -\kappa$, $B = 0$, $C = 0$: discriminant $0 - 4(-\kappa)(0) = 0$, parabolic. (To match the [Notes #2] form, identify $u_{xx} = u_{zz}$ and treat $t$ as the second variable.)

> **[Notes #2 — Summary]** — *"The PDEs that we encounter in weather/climate modeling are largely hyperbolic and parabolic"*. The advection problems you handled in HW1 and HW2 are hyperbolic (information travels along characteristics at speed $c$); the project is parabolic (information spreads out by diffusion, no characteristic propagation).

### 2.3 The two basic finite-difference ideas

To replace a derivative by a finite difference, use Taylor's theorem [Notes #3 §1]. For a smooth function $f(x)$:

$$
f(x + \Delta x) \;=\; f(x) \;+\; \Delta x\,f'(x) \;+\; \frac{\Delta x^{2}}{2}\,f''(x) \;+\; \frac{\Delta x^{3}}{6}\,f'''(x) \;+\; O(\Delta x^{4}).
$$

Rearranging gives three estimates of $f'(x)$:

$$
\text{Forward:} \qquad f'(x) \;\approx\; \frac{f(x + \Delta x) - f(x)}{\Delta x}.
$$

The leading error is $\Delta x\,f''(x)/2$, so this is **first-order accurate**: error is $O(\Delta x)$.

$$
\text{Backward:} \qquad f'(x) \;\approx\; \frac{f(x) - f(x - \Delta x)}{\Delta x}.
$$

Also first-order, error $-\Delta x\,f''(x)/2 + O(\Delta x^{2})$.

$$
\text{Centred:} \qquad f'(x) \;\approx\; \frac{f(x + \Delta x) - f(x - \Delta x)}{2\,\Delta x}.
$$

This is **second-order accurate**: error is $O(\Delta x^{2})$, because the leading $O(\Delta x)$ error term cancels when we subtract the two Taylor expansions. Concretely: the $f''$ terms have opposite signs in the forward and backward expansions, so subtracting kills them; the surviving terms start at $f'''$, scaled by $\Delta x^{2}/6$.

For a second derivative we use the centred three-point formula:

$$
f''(x) \;\approx\; \frac{f(x + \Delta x) - 2 f(x) + f(x - \Delta x)}{\Delta x^{2}} \;+\; O(\Delta x^{2}).
$$

These small algebraic identities are the only finite-difference formulas you need to read this entire report. Every discretised equation in §2.2 of the report is a combination of these few rules.

> **[Notes #3 §1]** sets out Taylor series and explicitly derives these forward/backward/centred difference formulas. **[HW1]** and **[HW2]** both apply the centred-time, centred-space ("CTCS") scheme to advection — so you are already familiar with the centred-difference algebra. The project applies the *same* centred difference for the spatial derivative, but pairs it with backward time (BTCS) or trapezoidal time (CN) instead of centred time, because diffusion is parabolic and centred time does not work for it.

### 2.4 What does "stability" mean?

A finite-difference scheme is **stable** if small numerical errors at one time step do not grow unboundedly over many time steps. If errors grow, the solution "blows up" — computed temperatures become $\pm\infty$ or NaN with no physical meaning. Stability is separate from accuracy: a scheme can be stable but inaccurate (just damps everything to a uniform value), or accurate but unstable (good for one step, but blows up after many).

Some schemes are **conditionally stable** — $\Delta t$ must be smaller than some bound for stability. Others are **unconditionally stable** — any $\Delta t$ works. Von Neumann analysis (Part 6.5) finds these bounds.

There is also a related concept, **convergence**: as $\Delta t \to 0$ and $\Delta z \to 0$, the numerical solution should approach the true solution. The Lax equivalence theorem says that for a *consistent* scheme (one whose truncation error $\to 0$ as $\Delta t, \Delta z \to 0$), stability is necessary and sufficient for convergence. So in practice, "is my scheme stable?" is the question worth asking.

> **[Notes #6 §10 (Slides 29–31)]** introduces von Neumann analysis. **[HW3]** and **[HW4]** both used it: in HW3 you computed amplification factors for Euler / Backward / Trapezoidal / Matsuno applied to the oscillation equation $d\psi/dt = i\omega\psi$, and confirmed Euler is unstable, Backward is always stable but damping, Trapezoidal is neutrally stable. The same logical structure carries over to diffusion in this project.

---

## Part 3. The vocabulary of finite-difference time-stepping schemes

### 3.1 The general framework

[Notes #6 §3] introduces the notation: let $\psi$ denote the true solution, $\phi_{j}^{n}$ the numerical approximation at $t = n\Delta t$ and (if needed) $x = j\Delta x$. For the ODE form $d\psi/dt = f(\psi, t)$, the goal is to construct schemes for advancing $\phi^{n} \to \phi^{n+1}$ that approximate the exact integral

$$
\psi^{n+1} \;=\; \psi^{n} \;+\; \int_{n\Delta t}^{(n+1)\Delta t}\,f(\psi, t)\,dt.
$$

[Notes #6 §4] classifies schemes by how many time levels they connect:

- **Two-level**: relate $\phi^{n+1}$ to $\phi^{n}$ only.
- **Three-level (or multi-level)**: relate $\phi^{n+1}$ to $\phi^{n}$ AND $\phi^{n-1}$ (and possibly earlier).

Two-level schemes can start from a single initial condition; multi-level schemes need a special start-up.

### 3.2 Explicit vs implicit (Notes #6 §5, Slides 13–14)

For an ODE $\dfrac{dT}{dt} = f(T)$, two natural time-step rules:

- **Explicit (forward Euler):** $T^{n+1} = T^{n} + \Delta t\,f(T^{n})$. RHS uses only the known $T^{n}$. No equation to solve. Cheap per step, conditionally stable.
- **Implicit (backward Euler):** $T^{n+1} = T^{n} + \Delta t\,f(T^{n+1})$. RHS uses the unknown $T^{n+1}$. We solve an algebraic equation. Expensive per step, unconditionally stable.

When $f$ is linear in $T$, the implicit scheme is a linear system; when nonlinear (as in the SEB with $T^{4}$), we use Newton iteration.

> **[Notes #6 §5]** also defines the **semi-implicit** scheme:
> $$\phi^{n+1} \;=\; \phi^{n} \;+\; a\,\Delta t\,\phi^{n} \;+\; b\,\Delta t\,\phi^{n+1}.$$
> The trapezoidal rule we use for Crank–Nicolson is one specific case of this: $a = b = 1/2$.

### 3.3 The trapezoidal rule = Crank–Nicolson

Take the average of explicit and implicit:

$$
T^{n+1} \;=\; T^{n} \;+\; \frac{\Delta t}{2}\bigl[\,f(T^{n}) + f(T^{n+1})\,\bigr].
$$

This is the **trapezoidal rule** for ODE integration. Implicit (so unconditionally stable), and second-order accurate in $\Delta t$ because the symmetric average cancels the leading error term.

When applied to the heat equation, the trapezoidal rule is called the **Crank–Nicolson** scheme (Crank & Nicolson, 1947). Implicit, unconditionally stable, second-order in time.

### 3.4 The full $\theta$-method family

All three schemes are special cases of one formula:

$$
\boxed{\;T^{n+1} \;=\; T^{n} \;+\; \Delta t\,\bigl[\,\alpha\,f(T^{n+1}) + (1 - \alpha)\,f(T^{n})\,\bigr]\;}
$$

| $\alpha$ | Scheme | Order in $\Delta t$ | Stability |
|---|---|---|---|
| $0$ | FTCS / Forward Euler / Explicit | first | conditional, $\nu \le 1/2$ |
| $1/2$ | Crank–Nicolson / Trapezoidal | second | unconditional |
| $1$ | BTCS / Backward Euler / Implicit | first | unconditional |

> **[Notes #6 §6 (Slides 15–17)]** introduces these *three exact schemes by name*: Euler (forward), Backward, Trapezoidal. The lecture-note formulae are
>
> $$\phi^{n+1} = \phi^{n} + \Delta t\,f^{n} \quad \text{(Euler/forward)}$$
>
> $$\phi^{n+1} = \phi^{n} + \Delta t\,f^{n+1} \quad \text{(Backward)}$$
>
> $$\phi^{n+1} = \phi^{n} + \tfrac{1}{2}\,\Delta t\,(f^{n} + f^{n+1}) \quad \text{(Trapezoidal)}$$
>
> with truncation errors $O(\Delta t)$, $O(\Delta t)$, $O((\Delta t)^{2})$ respectively. The project's FTCS, BTCS, CN are these same three schemes, applied here to the parabolic diffusion equation rather than to the ODE oscillation equation that the lecture used for illustration.

### 3.5 Other schemes you have seen — how the project's three relate

[Notes #6] discusses several more schemes besides Euler / Backward / Trapezoidal. Although the project uses only those three, knowing the surrounding family clarifies *why* the choice was made.

- **Matsuno scheme** (predictor-corrector): one Euler step as predictor, then re-evaluate $f$ at the predicted value. First-order, but explicit.
  $$\phi^{*\,n+1} = \phi^{n} + \Delta t\,f^{n}, \qquad \phi^{n+1} = \phi^{n} + \Delta t\,f(\phi^{*\,n+1}).$$
- **Heun scheme** (2nd-order Runge–Kutta): use the trapezoidal average of $f$ at the predicted endpoint. Explicit, second-order.
- **Leapfrog**: $\phi^{n+1} = \phi^{n-1} + 2\Delta t\,f^{n}$. Three-level, explicit, second-order. Widely used for atmospheric dynamics — but **unconditionally unstable for diffusive problems** (which is why we cannot use it here).

> **[HW3]** is the direct ancestor of this project. You implemented Euler, Backward, Trapezoidal, AND Matsuno on the oscillation equation $d\psi/dt = i\omega\psi$. Your figures showed:
>
> - **[HW3 Case 1 — Euler]**: amplitude grows above 1 for all four values of $n$ — Euler is unstable on the oscillation equation.
> - **[HW3 Case 2 — Backward]**: amplitude decays below 1 in every panel — Backward is always stable but damping.
> - **[HW3 Case 3 — Trapezoidal]**: amplitude stays exactly at 1 in every panel — Trapezoidal is neutrally stable for the oscillation equation.
> - **[HW3 Case 4 — Matsuno]**: amplitude decays slightly — Matsuno-Euler iterative correction stabilises the explicit Euler step.
>
> This is the structural pattern that carries over to the project's diffusion problem. The diffusion equation is parabolic, not oscillatory, so the *quantitative* stability conclusions are different (Trapezoidal is now strictly stable, not just neutral; Backward damps the worst wave aggressively rather than mildly), but the *ranking* — Euler unstable past a bound, Backward unconditionally stable but first-order, Trapezoidal unconditionally stable AND second-order — is identical.

### 3.6 Why the project uses the $\theta$-method specifically

Implementing all three schemes via one $\alpha$-parameterised routine has three benefits:

1. Single source of truth for the spatial discretisation — bugs there affect all three schemes equally and cannot bias the comparison.
2. Three numbers ($\alpha = 0, 1/2, 1$) replace three separately implemented routines — fewer opportunities for bugs.
3. The same banded-tridiagonal solver handles BTCS and CN, only the right-hand-side construction differs.

[Notes #6 §6.3] notes that the trapezoidal scheme is implicit but second-order, suggesting the comparison the project makes: pay the implicit cost (tridiagonal solve), gain unconditional stability AND second-order accuracy.

---

## Part 4. Walking through the abstract

The abstract is the densest paragraph in the report. We unpack it claim by claim.

**"The ground heat flux is the energy that the surface stores and releases from its substrate over a diurnal cycle, and is the term in the surface energy budget that is most sensitive to numerical treatment."**

$G$ is small in daily mean (small fraction of $R_{n}$), but it controls the day-night temperature swing, and the way $G$ is computed numerically can introduce errors that are large compared to $G$ itself. The other three SEB terms — $R_{n}$, $H$, $LE$ — are also computed by the model, but they are local in time: they depend on the current $T_{s}^{0}$ and the current atmospheric forcing, with no time-history dependence. $G$ is the term that involves the full *history* of the substrate (a buried heat reservoir built up over hours), and that history dependence is exactly what numerical errors accumulate in.

**"The governing one-dimensional heat conduction equation in the substrate is parabolic, and its explicit forward-time discretization is conditionally stable only when $\nu = \kappa_{s}\Delta t / \Delta z^{2} \le 1/2$ — a constraint that becomes prohibitive for the cm-scale near-surface layers required to resolve the diurnal damping depth in highly conductive urban substrates."**

Decoded:

- "parabolic" — the mathematical class of PDEs whose principal time-and-space derivative pattern matches the heat equation. From [Notes #2 §2nd-Order PDEs]. Discriminant $B^{2} - 4AC = 0$.
- "explicit forward-time discretization" = FTCS = $\alpha = 0$ in the $\theta$-method.
- "conditionally stable when $\nu \le 1/2$" = the FTCS stability bound from von Neumann analysis ([Notes #9 §Pure Diffusion]).
- "cm-scale near-surface layers" — since $d \sim 8$–$14\,\mathrm{cm}$, $\Delta z \ll d$ requires $\Delta z \sim 0.5$–$1\,\mathrm{cm}$.
- "highly conductive urban substrates" — concrete and asphalt have higher $\kappa$ than soil and so push the FTCS bound to even smaller $\Delta t$.

**"This project compares three numerical treatments of the soil heat equation — FTCS, BTCS, and Crank–Nicolson — coupled to a fully prognostic surface energy balance solved by Newton iteration."**

The key word is *prognostic*: $T_{s}^{0}$ is computed by the model at every step, not prescribed externally. Compare to Test 1 where $T_{s}^{0}$ is prescribed as a sinusoid — that is verification, not prognostic. The distinction matters because the operator-splitting error (the project's main finding) only appears when $T_{s}^{0}$ is itself a model variable that interacts with the column.

**"The von Neumann amplification factor is derived for each scheme; a damping-depth verification test confirms second-order CN error against first-order BTCS error; and the prognostic surface-energy-balance integration over the three substrates exposes the substrate-dependence of the scheme errors."**

Three lines of evidence: (1) analytical (von Neumann), (2) verified vs analytical solution (Test 1 / damping depth), (3) prognostic numerical experiment (Test 2). Each is independent of the others; the three converge on the same conclusions.

**"FTCS blows up at $\Delta t = 60\,\mathrm{s}$ on the concrete roof and at $\Delta t = 600\,\mathrm{s}$ on the asphalt road and concrete roof"** — this was originally written as "on all substrates" before the audit fix; bare soil at $\Delta t = 600\,\mathrm{s}$ is over the bound but completes (with substantial error). The corrected version is what is in `modified_full_report_1.docx`.

**"BTCS at $\Delta t = 600\,\mathrm{s}$ over-amplifies the diurnal G amplitude by 40% on asphalt and concrete and by 20% on bare soil, with surface temperature RMSE up to 3.7 K on the roof; CN at the same $\Delta t$ halves these errors."**

These are the headline numbers. Memorise them: 40% on the paved substrates, 20% on soil, factor-of-two reduction by CN.

**"The empirical $\Delta t$-refinement ratios for BTCS and CN are both close to 10:1 between $\Delta t = 60\,\mathrm{s}$ and $\Delta t = 600\,\mathrm{s}$ — first-order in $\Delta t$ for both schemes — which identifies the dominant error as a first-order operator-splitting error from the column-then-SEB ordering, not the schemes' own temporal accuracy orders."**

This is the project's intellectual core. The $\Delta t$-refinement ratio $\mathrm{RMSE}(600\,\mathrm{s})/\mathrm{RMSE}(60\,\mathrm{s})$ would be 10 if the dominant error is first-order, 100 if second-order. Empirically it is around 10 for both BTCS and CN. CN is intrinsically second-order, so a ratio of 10 (not 100) tells us the dominant error is *not* the per-substep CN truncation; it is the operator splitting between sub-steps. Discussed in detail in Part 9.2.

**"The daily storage integral $\int G\,dt$ is preserved across schemes to within 5%, so the diurnal G inflation is symmetric in day/night and translates into an inflation of the diurnal range of the simulated nocturnal urban heat island rather than a bias in its mean."**

This is the bridge to physical/UHI relevance. The over-amplification is *symmetric*: the daytime peak is too high, but the night-time trough is also too low (more negative), so the daily mean is preserved. The implication is that the simulated nocturnal UHI is unbiased on average but its diurnal range is exaggerated.

**"An independent attribution analysis using a gradient-boosted regression with SHAP feature importance on $N = 150$ synthetic substrate columns identifies top-cell thermal diffusivity $\kappa_{\text{top}}$ — the parameter that sets the FTCS stability bound — as the dominant predictor of BTCS coarse-$\Delta t$ error ($R^{2} = 0.92$ from $\kappa_{\text{top}}$ alone), with bulk admittance second and layer-interface descriptors a small but non-zero residual contribution."**

This is the §6 finding. Three things to take from it: (1) the dominant predictor of error is $\kappa_{\text{top}}$, the same parameter that sets the FTCS bound; (2) it explains 92% of the variance on its own; (3) admittance is a secondary, layer interfaces tertiary. The mechanistic connection — why $\kappa_{\text{top}}$ — is in Part 10.

---

## Part 5. Walking through §1 Introduction

### 5.1 Why the urban heat island depends on $G$ specifically

The urban heat island (UHI) is the systematic phenomenon that cities are warmer than rural areas, especially at night. Many factors contribute (anthropogenic heat, canyon geometry, reduced evapotranspiration), but the central physical mechanism for the *night-time* component is **heat storage**.

During the day, urban materials — pavements, walls, roofs — absorb shortwave radiation. Their high heat capacity and conductivity (relative to vegetated soil) mean they hold a lot of that energy. After sunset, $R_{n}$ turns negative and the stored heat is released. Rural surfaces store less (their substrates are usually drier and less conductive, with much daytime energy lost to evapotranspiration). At night, the urban surface is still warm while the rural one has cooled — that contrast is the nocturnal UHI.

$G$ is the very quantity that *puts heat into the urban substrate during the day and pulls it back out at night*. If a model gets $G$ wrong, it gets the UHI wrong. This is the project's policy-relevant motivation.

> **[Notes #11 Misconception #3]** ("Surface conditions are accurately depicted") emphasises that **surface conditions in models may be based on climatology rather than current observations, may not match the model grid scale, and may not be well-handled within the model integration**. The project addresses one specific way the surface conditions can be mis-handled: the numerical treatment of $G$ at the column-SEB interface.

### 5.2 The damping-depth values quoted in the introduction

Paragraph 11 of the report says: *"$d$ is approximately $8\,\mathrm{cm}$ in dry soil, $14\,\mathrm{cm}$ in dense concrete, and $10\,\mathrm{cm}$ in asphalt (computed from the substrate parameters used in §3.2)."* These are computed by plugging the substrate's $\lambda$ and $C$ into $d = \sqrt{2\kappa/\omega}$. We did the calculation in Part 1.3.

The report concludes: "small enough that operational urban canopy schemes such as TEB (Masson, 2000) and SLUCM (Kusaka et al., 2001) use cm-scale near-surface layers." The two cited schemes are real operational urban canopy parameterisations. TEB (Town Energy Balance) is used in Météo-France's mesoscale model; SLUCM (Single-Layer Urban Canopy Model) is used in WRF. Both indeed use cm-scale top layers.

### 5.3 What "wavenumber-dependent damping" means

The end of paragraph 11 says implicit schemes "introduce wavenumber-dependent damping that distorts the high-frequency content of the diurnal cycle, particularly at the rapid sunrise and sunset transitions and at sharp material interfaces in layered urban substrates."

Every numerical scheme can be characterised by how it changes the amplitude of each Fourier component (each wavelength) per time step. For FTCS, BTCS, CN we will derive these *amplification factors* explicitly in Part 6.5. Wavenumber-dependent damping means the amplification factor is not 1 — short waves are damped differently from long waves, and that distortion is what the report quantifies.

> **[HW2]** asked you to verify amplitude conservation on a sine-wave initial condition: the period-tracking and max-amplitude diagnostics there are exactly the kind of test for wavenumber-dependent damping that the project applies to its diffusion solvers. **[HW4]** plotted $|A_{k}|$ vs $k\Delta x$ for a specific advection scheme — the *same kind of plot* that Figure 1 of the project shows, with $k\Delta z$ on the x-axis instead.

### 5.4 What the §1 closing paragraph promises

Paragraph 12 of the report says: *"This project investigates the trade-off between numerical stability and accuracy for ground heat conduction in three idealized urban substrates."* This is the framing. Stability-vs-accuracy is the central tension in any numerical scheme: explicit schemes are accurate per step but conditionally stable; implicit schemes are unconditionally stable but expensive per step. The report goes further than the binary stability question: among unconditionally stable schemes, *what kind of error remains*? The answer (operator splitting) becomes the project's main finding.

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

If $T$ decreases with depth ($\partial T/\partial z < 0$), then $q > 0$ — flux in the $+z$ direction (downward). The minus sign encodes the second law of thermodynamics: heat flows from hot to cold, never the reverse.

**Step 2. Energy conservation in a thin slab.** Pick a thin horizontal slab from depth $z$ to $z + dz$. Energy stored per unit area: $C_{s}\,T_{s}\,dz$. Rate of change of stored energy = net flux into slab = $q(z) - q(z + dz)$:

$$
\frac{\partial}{\partial t}\bigl[\,C_{s}\,T_{s}\,dz\,\bigr] \;=\; q(z) - q(z + dz).
$$

If we assume $C_{s}$ is time-independent (the substrate doesn't change phase or composition) and Taylor-expand $q(z + dz) \approx q(z) + (\partial q/\partial z)\,dz$:

$$
C_{s}\,\frac{\partial T_{s}}{\partial t}\,dz \;=\; -\frac{\partial q}{\partial z}\,dz.
$$

Substituting $q = -\lambda_{s}\,\partial T_{s}/\partial z$:

$$
C_{s}\,\frac{\partial T_{s}}{\partial t} \;=\; -\frac{\partial}{\partial z}\!\left[\,-\lambda_{s}\,\frac{\partial T_{s}}{\partial z}\,\right] \;=\; \frac{\partial}{\partial z}\!\left[\,\lambda_{s}\,\frac{\partial T_{s}}{\partial z}\,\right].
$$

That is the conductivity-form heat equation. It is just energy conservation written locally, with Fourier's law for the flux.

**Step 3. Why "conductivity form" instead of "diffusivity form"?** If $\lambda$ and $C$ are constant, we can pull them out of the derivative and write $\partial T/\partial t = \kappa\,\partial^{2} T/\partial z^{2}$ with $\kappa = \lambda/C$. That is the **diffusivity form**.

In our layered substrates, $\lambda$ and $C$ jump by an order of magnitude across material interfaces. The diffusivity form, when discretised, does **not** exactly conserve heat across those jumps — the discrete heat content can drift. Why? Because $\kappa = \lambda/C$ depends on *both* $\lambda$ and $C$, and the form $\partial T/\partial t = \kappa\,\partial^{2}T/\partial z^{2}$ does not isolate the flux as a derivative of a *single* spatial quantity. The conductivity form, by contrast, has the structure $\partial(\text{stored})/\partial t = \partial(\text{flux})/\partial z$, so the discrete update directly conserves the integral $\int C_{s}\,T_{s}\,dz$ when fluxes match across faces. That conservation holds regardless of whether $\lambda$ or $C$ jumps.

**The symbols, definitively.**

- $T_{s}(z, t)$ — substrate temperature at depth $z$, time $t$. Units Kelvin. The subscript $s$ distinguishes from air temperature $T_{a}$.
- $z$ — vertical depth, $z = 0$ at surface, increasing downward. Units m.
- $t$ — time. Units s.
- $\lambda_{s}(z)$ — substrate thermal conductivity at depth $z$. Units $\mathrm{W\,m^{-1}\,K^{-1}}$. The $s$ subscript means "substrate" — disambiguates from any other $\lambda$ in the project.
- $C_{s}(z)$ — volumetric heat capacity. Units $\mathrm{J\,m^{-3}\,K^{-1}}$.
- $\partial T_{s}/\partial t$ — partial derivative w.r.t. time, holding $z$ fixed. The "how $T$ changes per second at this depth" rate.
- $\partial T_{s}/\partial z$ — partial w.r.t. depth, holding $t$ fixed. The temperature gradient.
- $\partial/\partial z\,[\lambda_{s}\,\partial T_{s}/\partial z]$ — second-order spatial operator with $\lambda$ inside.

### 6.2 §2.2 — The grid, the half-levels, the harmonic mean

#### Cell centres and the staggered grid

Replace continuous depth $z$ with cell centres $z_{0}, z_{1}, \ldots, z_{N-1}$. At each cell store *one number*: temperature $T_{j}$ at the centre. Between cells $j$ and $j+1$ lies a face at depth $z_{j+1/2} = (z_{j} + z_{j+1})/2$. **Temperatures live at centres; conductive fluxes at faces.**

Why? The flux involves $\partial T/\partial z$, and the most accurate centred-difference estimate of that derivative uses $T$ on either side of the point of evaluation. The face between cells $j$ and $j+1$ is exactly halfway between them, so $(T_{j} - T_{j+1})/(z_{j+1} - z_{j})$ is naturally centred there.

This **staggered grid** is the standard finite-volume layout. Its main virtue is automatic conservation: heat that leaves cell $j$ across face $j+\tfrac{1}{2}$ is the *same* heat that enters cell $j+1$ across the same face, so energy is conserved by construction. No special bookkeeping required.

> **[Notes #8]** is dedicated to staggered grids and their advantages. Specifically [Notes #8] emphasises that an unstaggered grid suffers from the **2-$\Delta x$ aliasing problem**: a wavelength-2$\Delta x$ pattern has zero numerical phase speed on an unstaggered grid (the centred difference $\dfrac{u_{j+1} - u_{j-1}}{2\Delta x}$ "skips over" the alternating wave), while a staggered grid evaluates the derivative at a face *between* two cells, capturing the alternating pattern correctly.
>
> **[HW5]** is the direct precursor where you proved this empirically. You showed that on the unstaggered grid, a single point disturbance ($\phi = 100$ at one grid point) only spread to *every other* grid point, creating sub-grid decoupling — odd-indexed cells stayed at zero forever. On the staggered grid, the disturbance spread smoothly to all neighbours, as expected physically. The same advantage applies to the project's flux discretisation: putting $G$ at half-levels allows accurate centred-difference gradients with no aliasing pathology.

#### The discrete flux equation, line by line

The report's equation:

$$
\boxed{\;G_{j+1/2} \;=\; \lambda_{j+1/2}\,\frac{T_{j} - T_{j+1}}{z_{j+1} - z_{j}}\;}
$$

is Fourier's law evaluated at the half-level. Decoded:

- $G_{j+1/2}$ — conductive heat flux through the face between cells $j$ and $j+1$. Units $\mathrm{W\,m^{-2}}$. Sign: $G > 0$ means downward.
- $\lambda_{j+1/2}$ — thermal conductivity at the face. Computed from the cell-centre $\lambda_{j}$ and $\lambda_{j+1}$ via the harmonic mean.
- $(T_{j} - T_{j+1})$ — temperature drop from cell $j$ (above) to cell $j+1$ (below). Positive when $j$ is warmer, meaning heat flows downward — consistent with $G > 0$ = downward.
- $(z_{j+1} - z_{j})$ — centre-to-centre spacing.

So $G_{j+1/2}$ = $\lambda$ × (temperature drop) / (centre-to-centre distance) = $\lambda$ × (gradient at the face). Fourier's law $q = -\lambda\,\partial T/\partial z$, with the centred difference for the gradient. The minus sign in Fourier's law has been absorbed into writing $(T_{j} - T_{j+1})$ instead of $(T_{j+1} - T_{j})$, so that $G > 0$ corresponds to downward flow.

#### Why the harmonic mean for $\lambda$ at faces?

Solve the steady-state conduction problem across an interface between two materials in series. The flux must be the same on both sides (steady state, no storage):

$$
q \;=\; \lambda_{1}\,\frac{\Delta T_{1}}{\Delta z_{1}} \;=\; \lambda_{2}\,\frac{\Delta T_{2}}{\Delta z_{2}}.
$$

Total temperature drop is $\Delta T = \Delta T_{1} + \Delta T_{2}$ over total distance $\Delta z = \Delta z_{1} + \Delta z_{2}$. From the two single-material relations: $\Delta T_{1} = q\,\Delta z_{1}/\lambda_{1}$ and $\Delta T_{2} = q\,\Delta z_{2}/\lambda_{2}$. Adding:

$$
\Delta T \;=\; q\,\left(\frac{\Delta z_{1}}{\lambda_{1}} + \frac{\Delta z_{2}}{\lambda_{2}}\right) \;=\; q\,\frac{\Delta z}{\lambda_{\text{eff}}},
$$

where $\lambda_{\text{eff}} = \dfrac{\Delta z_{1} + \Delta z_{2}}{\Delta z_{1}/\lambda_{1} + \Delta z_{2}/\lambda_{2}}$ — a **thickness-weighted harmonic mean**.

For two cells of equal thickness this collapses to:

$$
\boxed{\;\lambda_{j+1/2} \;=\; \frac{2\,\lambda_{j}\,\lambda_{j+1}}{\lambda_{j} + \lambda_{j+1}}\;}
$$

$$\boxed{\,\text{Worked example — concrete-roof interface.}\,}$$

At the concrete-deck-to-insulation interface: $\lambda_{1} = \lambda_{\text{concrete}} = 1.5$, $\lambda_{2} = \lambda_{\text{insulation}} = 0.04$.

- **Arithmetic mean:** $\dfrac{1.5 + 0.04}{2} = 0.77$. Close to concrete's value — wrong.
- **Harmonic mean:** $\dfrac{2 \times 1.5 \times 0.04}{1.5 + 0.04} = \dfrac{0.12}{1.54} = 0.078$. Much closer to insulation's value — correct.

The ratio: arithmetic / harmonic = $0.77/0.078 \approx 9.9$. So the arithmetic mean over-estimates the heat flux across this interface by a factor of $\sim 10$ — meaning the model would wrongly predict that the insulation lets heat through nearly as easily as concrete.

This matches the intuition from electrical resistors in series: total resistance is the sum of individual resistances, and the *smaller* conductivity dominates. Heat conduction across an interface is exactly analogous to current flowing through resistors in series, with $\lambda$ playing the role of conductance and $\Delta z/\lambda$ the role of resistance.

#### The semi-discrete tendency

Apply the centred-difference flux at every face. The rate of energy accumulation in cell $j$ (per unit horizontal area) equals the flux entering at the top minus the flux leaving at the bottom:

$$
\boxed{\;C_{j}\,\Delta z_{j}\,\frac{dT_{j}}{dt} \;=\; G_{j-1/2} - G_{j+1/2}\;}
$$

Energy-content rate is $C_{j}\,\Delta z_{j}\,dT_{j}/dt$ because energy density per unit volume is $C_{j}\,T_{j}$ and the cell has thickness $\Delta z_{j}$.

This is **semi-discrete**: space is discretised, time is still continuous. The next step discretises time.

### 6.3 §2.3 — Building the $\theta$-method update equation

The semi-discrete equation is $C_{j}\,\Delta z_{j}\,dT_{j}/dt = R_{j}(t)$, where $R_{j} = G_{j-1/2} - G_{j+1/2}$. Integrate from $t^{n}$ to $t^{n+1}$:

$$
C_{j}\,\Delta z_{j}\,(T_{j}^{n+1} - T_{j}^{n}) \;=\; \int_{t^{n}}^{t^{n+1}} R_{j}(t)\,dt.
$$

The integral has to be approximated. Three natural quadrature rules give us three schemes:

- **Left rectangle**: $\int \approx \Delta t\,R_{j}^{n}$. Use only the value at the start of the interval. Gives FTCS, $\alpha = 0$.
- **Right rectangle**: $\int \approx \Delta t\,R_{j}^{n+1}$. Use only the value at the end. Gives BTCS, $\alpha = 1$.
- **Trapezoid**: $\int \approx (\Delta t/2)[R_{j}^{n} + R_{j}^{n+1}]$. Average start and end. Gives CN, $\alpha = 1/2$.

In one line — the report's $\theta$-method update:

$$
\boxed{\;C_{j}\,\Delta z_{j}\,\frac{T_{j}^{n+1} - T_{j}^{n}}{\Delta t} \;=\; \alpha\,[\,G_{j-1/2} - G_{j+1/2}\,]^{n+1} \;+\; (1 - \alpha)\,[\,G_{j-1/2} - G_{j+1/2}\,]^{n}\;}
$$

Setting $\alpha = 0, 1, 1/2$ retrieves FTCS, BTCS, CN. The single-line form is what makes the project's code clean — one update routine handles all three schemes.

#### Why FTCS and BTCS are first-order, CN is second-order in $\Delta t$

Plug the exact integral into a Taylor expansion around the midpoint $t^{n} + \Delta t/2$ and compare with each quadrature rule. Let $R_{m} = R(t^{n} + \Delta t/2)$ denote the midpoint value, and Taylor-expand:

$$
R(t^{n}) \;=\; R_{m} - \tfrac{\Delta t}{2}\,R'_{m} + \tfrac{(\Delta t)^{2}}{8}\,R''_{m} - \cdots
$$

$$
R(t^{n+1}) \;=\; R_{m} + \tfrac{\Delta t}{2}\,R'_{m} + \tfrac{(\Delta t)^{2}}{8}\,R''_{m} + \cdots
$$

Average these two:

$$
\tfrac{1}{2}\,[R(t^{n}) + R(t^{n+1})] \;=\; R_{m} + \tfrac{(\Delta t)^{2}}{8}\,R''_{m} + O(\Delta t^{4}).
$$

The $\Delta t/2 \cdot R'_{m}$ terms have opposite signs and cancel exactly when averaged. This means the trapezoid (CN) approximates the integral as $\Delta t\,R_{m} + O((\Delta t)^{3})$ — with leading error $O(\Delta t^{3})$ in the integral, hence $O(\Delta t^{2})$ in the time-derivative. **Second-order.** The single-rectangle rules (FTCS and BTCS) keep the $\Delta t/2 \cdot R'_{m}$ term, so their leading error is $O(\Delta t^{2})$ in the integral, hence $O(\Delta t)$ in the time-derivative. **First-order.**

> **[HW3 Case 3]** confirmed this empirically for the oscillation equation: your trapezoidal scheme was *neutrally stable for all frequencies*, with amplitude staying exactly at 1.0 — a special case of the second-order accuracy showing through. The same algebraic mechanism here.

#### Linear systems and tridiagonal solves

When $\alpha > 0$, the RHS involves $T$ values at level $n+1$ — the unknowns. Collecting unknowns on the left and knowns on the right gives a system of $N$ linear equations in $N$ unknowns. The matrix has nonzero entries only on the main diagonal and the two adjacent diagonals (because each cell $j$ couples only to $j \pm 1$ through the two faces). Such a matrix is **tridiagonal**:

$$
\begin{pmatrix}
b_{0} & c_{0} & 0 & \cdots & 0 \\
a_{1} & b_{1} & c_{1} & \cdots & 0 \\
0 & a_{2} & b_{2} & \ddots & \vdots \\
\vdots & \vdots & \ddots & \ddots & c_{N-2} \\
0 & 0 & \cdots & a_{N-1} & b_{N-1}
\end{pmatrix}
\begin{pmatrix}
T_{0}^{n+1} \\ T_{1}^{n+1} \\ T_{2}^{n+1} \\ \vdots \\ T_{N-1}^{n+1}
\end{pmatrix}
\;=\;
\begin{pmatrix}
d_{0} \\ d_{1} \\ d_{2} \\ \vdots \\ d_{N-1}
\end{pmatrix}.
$$

Tridiagonal systems can be solved in $O(N)$ operations using the **Thomas algorithm** (a specialised Gaussian elimination) — far cheaper than a generic $O(N^{3})$ solver. SciPy provides `scipy.linalg.solve_banded((1,1), A, b)`. The argument $(1, 1)$ means "one band below the diagonal, one band above".

> **[Notes #9 §Practical Considerations]** explicitly says: *"Implicit differencing leads to a system of algebraic equations with a tridiagonal matrix structure...Tridiagonal solvers are particularly efficient and well suited for vertical mixing in oceanic and atmospheric models, where stability constraints are most restrictive."* The project uses exactly this lecture-prescribed approach.

### 6.4 §2.4 — The boundary conditions

A PDE governs how things change *inside* a domain. To get a well-defined problem, we need to specify what happens at the boundaries. Two main types:

- **Dirichlet condition** — prescribes the value of $T$ at the boundary. Example: $T(0, t) = T_{s}^{0}(t)$.
- **Neumann condition** — prescribes the value of the gradient $\partial T/\partial z$ (equivalently the flux $q = -\lambda\,\partial T/\partial z$) at the boundary. Example: $\partial T/\partial z = 0$ (zero gradient = zero flux).

(There is also a **Robin condition**, which prescribes a linear combination of value and gradient, like $a\,T + b\,\partial T/\partial z = c$ — but we don't use it here.)

#### Lower boundary: zero-flux Neumann

At $z = z_{\text{top}} = 2\,\mathrm{m}$ we impose $\partial T/\partial z = 0$. Why? At $2\,\mathrm{m}$ we are well below the diurnal damping depth $d \approx 8$–$14\,\mathrm{cm}$ — the daily wave has long since decayed. Below $2\,\mathrm{m}$ the temperature varies only on seasonal timescales, which is much slower than the diurnal cycle of interest. Modelling the deep substrate as adiabatic (zero flux) is the standard choice for diurnal-scale studies. It is sometimes called a **deep adiabatic floor**.

Discretely: $T_{N-1} = T_{N-2}$, i.e., the deepest cell has the same temperature as the cell above it. This forces the centred-difference gradient at the bottom face to be zero, hence the flux is zero.

A more conservative choice would be a *fixed-temperature* Dirichlet condition at the bottom, anchoring the deep substrate to the annual mean. For a 2-day integration with the deep substrate already at quasi-equilibrium (thanks to the damping-depth initialisation), the two choices give numerically indistinguishable answers, so the simpler Neumann condition is used.

#### Upper boundary: Dirichlet on $T_{s}^{0}$

At cell 0 we set $T_{0} = T_{s}^{0}$. In Test 1, $T_{s}^{0}(t) = \bar T + A\cos\omega t$ — a prescribed sinusoid. In Test 2, $T_{s}^{0}$ is the unknown solved by Newton iteration on the SEB.

Note the Dirichlet condition imposes a **value** on $T_{s}^{0}$, not on $T_{0}$ as a separate quantity. The cell-centre $T_{0}$ is held identically equal to the surface temperature $T_{s}^{0}$ — there is no half-cell at $z = 0$ in this convention.

### 6.5 §2.5 — Von Neumann stability analysis from scratch

This is the most algebraically dense subsection of the report. Take it in stages.

#### Setup: linearise, idealise, then test

Von Neumann analysis works only for linear schemes on uniform grids with constant coefficients. So we idealise: assume $\lambda$ and $C$ are constant (so $\kappa = \lambda/C$ is constant), assume $\Delta z$ is uniform, assume periodic boundaries (no top, no bottom — the substrate extends infinitely in $z$). Then we test whether the scheme amplifies any small perturbation away from a smooth state.

The result will technically apply only to the idealised problem. But when we apply the same scheme to the real (non-uniform, layered, finite-domain) problem, the local stability properties are still controlled by the *cell-by-cell* values of $\nu_{j} = \kappa_{j}\,\Delta t/\Delta z_{j}^{2}$. The cell with the most restrictive $\nu_{j}$ sets the bound. This is the substance of §5.1 of the report.

#### Step 1 — Substitute a Fourier mode

Any small perturbation can be written as a sum of complex-exponential Fourier modes:

$$
T_{j}^{n} \;=\; A^{n}\,e^{i\,k\,j\,\Delta z}.
$$

Here $k$ is the wavenumber (radians per metre), $A$ is the amplification factor (one complex number per wavenumber). Why complex exponentials? Because $e^{i\theta} = \cos\theta + i\sin\theta$ (Euler's formula) and so a complex exponential is just the simultaneous bookkeeping of cosine and sine. The equation is linear, so different Fourier modes do not interact; we analyse each independently. Linearity also means that if a real initial condition has only cosine components, the imaginary parts of the solution stay zero — they are along for the ride algebraically but contribute nothing physically.

The grid resolves wavenumbers $k$ from 0 (a constant in space) up to $k = \pi/\Delta z$ (the 2-$\Delta z$ wave — alternating sign at every grid point). So we need $|A(\nu, k\Delta z)| \le 1$ for every $k\Delta z$ in $[0, \pi]$ for stability.

#### Step 2 — Plug into the FTCS update

FTCS at $\alpha = 0$ on a uniform grid with constant $\kappa$, in diffusivity form:

$$
T_{j}^{n+1} \;=\; T_{j}^{n} \;+\; \frac{\kappa\,\Delta t}{\Delta z^{2}}\,\bigl[\,T_{j+1}^{n} - 2\,T_{j}^{n} + T_{j-1}^{n}\,\bigr].
$$

(Why is this the right discrete form? We are using the conductivity-form heat equation with constant $\lambda$ and $C$, so $\partial T/\partial t = \kappa\,\partial^{2}T/\partial z^{2}$, and the centred three-point formula for the second derivative gives us the bracket.)

Define $\nu = \kappa\,\Delta t/\Delta z^{2}$. Substitute the Fourier mode $T_{j}^{n} = A^{n}\,e^{i\,k\,j\,\Delta z}$:

$$
A^{n+1}\,e^{i\,k\,j\,\Delta z} \;=\; A^{n}\,e^{i\,k\,j\,\Delta z} \;+\; \nu\,A^{n}\,\bigl[\,e^{i\,k\,(j+1)\,\Delta z} - 2\,e^{i\,k\,j\,\Delta z} + e^{i\,k\,(j-1)\,\Delta z}\,\bigr].
$$

Divide both sides by $A^{n}\,e^{i\,k\,j\,\Delta z}$ — every term has this common factor:

$$
A \;=\; 1 \;+\; \nu\,\bigl[\,e^{i\,k\,\Delta z} - 2 + e^{-i\,k\,\Delta z}\,\bigr].
$$

Use Euler's identity $e^{ix} + e^{-ix} = 2\cos x$:

$$
\boxed{\;A_{\mathrm{FTCS}}(\nu, k\Delta z) \;=\; 1 \;-\; 2\,\nu\,(1 - \cos k\Delta z)\;}
$$

> **[Notes #9 §Pure Diffusion (Von Neumann Analysis)]** derives this **exact same formula**, using $M$ for diffusivity and $\nu = M\Delta t/(\Delta x)^{2}$. The lecture concludes: *"Stability criterion: $0 \le \nu \le 1/2$"*. The project uses identical algebra and the identical bound.

#### Step 3 — Plug into the BTCS update

BTCS at $\alpha = 1$ on a uniform grid:

$$
T_{j}^{n+1} \;=\; T_{j}^{n} \;+\; \nu\,\bigl[\,T_{j+1}^{n+1} - 2\,T_{j}^{n+1} + T_{j-1}^{n+1}\,\bigr].
$$

Substitute the Fourier mode (note the right-hand side now involves $T$ at level $n+1$):

$$
A^{n+1} \;=\; A^{n} \;+\; \nu\,A^{n+1}\,[2\cos k\Delta z - 2].
$$

Divide by $A^{n}$:

$$
A \;=\; 1 \;+\; A\,\nu\,[2\cos k\Delta z - 2] \;=\; 1 \;-\; 2\,A\,\nu\,(1 - \cos k\Delta z).
$$

Solve for $A$:

$$
A\,\bigl[\,1 + 2\,\nu\,(1 - \cos k\Delta z)\,\bigr] \;=\; 1.
$$

$$
\boxed{\;A_{\mathrm{BTCS}}(\nu, k\Delta z) \;=\; \frac{1}{1 + 2\,\nu\,(1 - \cos k\Delta z)}\;}
$$

#### Step 4 — Plug into the CN update

CN at $\alpha = 1/2$:

$$
T_{j}^{n+1} \;=\; T_{j}^{n} \;+\; \frac{\nu}{2}\,[\,T_{j+1}^{n} - 2 T_{j}^{n} + T_{j-1}^{n}\,] \;+\; \frac{\nu}{2}\,[\,T_{j+1}^{n+1} - 2 T_{j}^{n+1} + T_{j-1}^{n+1}\,].
$$

Substitute the Fourier mode and let $h = \nu\,(1 - \cos k\Delta z)$ for brevity. The two bracketed groups become $-2 A^{n}\,h$ and $-2 A^{n+1}\,h$ respectively. So:

$$
A^{n+1} \;=\; A^{n} \;-\; A^{n}\,h \;-\; A^{n+1}\,h.
$$

Divide by $A^{n}$:

$$
A \;=\; 1 - h - h\,A.
$$

$$
A\,(1 + h) \;=\; 1 - h.
$$

$$
\boxed{\;A_{\mathrm{CN}}(\nu, k\Delta z) \;=\; \frac{1 - h}{1 + h} \;=\; \frac{1 - \nu\,(1 - \cos k\Delta z)}{1 + \nu\,(1 - \cos k\Delta z)}\;}
$$

> **[Notes #9 §Implicit Diffusion]** derives this same formula and labels it "the Crank–Nicolson method". The lecture concludes: *"$|A_{k}| < 1$ — Unconditionally stable"*. The project's algebra and bound exactly match the lecture's.

#### What $|A| \le 1$ means and why we want it

After one time step, the Fourier mode at wavenumber $k$ has amplitude $A$. After $n$ time steps, amplitude is $A^{n}$. If $|A| > 1$, the mode grows exponentially: $|A|^{n} \to \infty$ as $n$ grows. That is what "blow-up" is — some Fourier component growing without bound until floating-point overflow.

If $|A| \le 1$, the mode either holds steady or decays. The scheme is **stable in the von Neumann sense** if $|A| \le 1$ for every wavenumber the grid resolves.

#### Why $k\Delta z = \pi$ is the worst case

For all three amplification factors, the dependence on $k\Delta z$ is through the factor $(1 - \cos k\Delta z)$. This factor:

- Equals 0 at $k\Delta z = 0$ (because $\cos 0 = 1$).
- Equals 2 at $k\Delta z = \pi$ (because $\cos \pi = -1$).
- Is monotonically increasing on $[0, \pi]$.

So whichever wavenumber pushes $A$ farthest from 1 in magnitude is the wavenumber where $(1 - \cos k\Delta z)$ is largest — always $k\Delta z = \pi$, the **2-$\Delta z$ wave**.

Substituting $1 - \cos\pi = 2$ into each amplification factor:

$$
A_{\mathrm{FTCS}}(\nu, \pi) = 1 - 4\nu, \qquad
A_{\mathrm{BTCS}}(\nu, \pi) = \frac{1}{1 + 4\nu}, \qquad
A_{\mathrm{CN}}(\nu, \pi) = \frac{1 - 2\nu}{1 + 2\nu}.
$$

#### Reading the stability conclusions

**FTCS** at the worst wave: $A = 1 - 4\nu$. For $|A| \le 1$ we need $-1 \le 1 - 4\nu \le 1$. Upper bound is automatic ($1 - 4\nu \le 1$ since $\nu \ge 0$). Lower bound: $1 - 4\nu \ge -1$ requires $4\nu \le 2$, i.e., $\nu \le 1/2$. So **FTCS is conditionally stable** with bound

$$
\boxed{\;\nu \le 1/2\quad \text{i.e.,}\quad \Delta t \;\le\; \frac{1}{2}\,\frac{\Delta z^{2}}{\kappa}\;}
$$

**BTCS** at the worst wave: $A = 1/(1 + 4\nu)$. For $\nu > 0$ this is automatically between 0 and 1. So $|A| < 1$ always — **BTCS is unconditionally stable**, and moreover *strictly damping* (the worst wave decays each step).

**CN** at the worst wave: $A = (1 - 2\nu)/(1 + 2\nu)$. For $\nu > 0$ the numerator can be negative (when $\nu > 1/2$), but $|1 - 2\nu| \le |1 + 2\nu|$ always, so $|A| \le 1$ always — **CN is unconditionally stable**. But notice what happens as $\nu \to \infty$: $A \to -1$. So at very large $\nu$, the worst wave is preserved in magnitude (|$A$| stays at 1) but flips sign every step. This is the *over-damping pathology of CN at large $\nu$* that the report mentions: 2-$\Delta z$ noise is not suppressed, just made to oscillate.

Note that CN's behaviour $A \to -1$ is a **numerical-noise issue, not a blow-up**. Any 2-$\Delta z$ pattern that exists at the start stays in the solution as a flipping pattern of the same amplitude. For smooth initial conditions and forcing, this is harmless — no 2-$\Delta z$ pattern is excited in the first place. For sharp transitions or noisy initial states, CN can ring at the 2-$\Delta z$ frequency without ever decaying.

> **[HW4]** is the direct ancestor: you plotted $|A_{k}|$ against $k\Delta x$ for various CFL numbers $\mu$ for an advection scheme, observed the peak at $k\Delta x = \pi/2$, and concluded which $\mu$ values gave $|A_{k}| \ge 1$. The project applies the *same logical structure* to a parabolic equation, with the worst case at $k\Delta z = \pi$ instead of $\pi/2$. The reason for the difference: HW4's advection had $\sin k\Delta x$ in its amplification factor; the project's diffusion has $\cos k\Delta z$, and these two trigonometric functions peak at different $k\Delta x$ values.

### 6.6 Reading Figure 1 panel by panel

Figure 1 has three panels — FTCS, BTCS, CN — each plotting $|A_{k}|$ vs $k\Delta z$ for four values of $\nu$.

#### The axes

- The $x$-axis is $k\Delta z$, ranging from 0 to $\pi$. This is the *dimensionless* wavenumber: $k\Delta z = 0$ corresponds to infinitely long wavelengths (a constant in space); $k\Delta z = \pi$ corresponds to the shortest wavelength on the grid, the 2-$\Delta z$ wave, where the pattern flips sign at every cell. We use $k\Delta z$ rather than just $k$ because $\Delta z$ sets the grid scale — a physically resolvable wavenumber depends on the grid spacing, not on the wavenumber alone.
- The $y$-axis is $|A_{k}(\nu, k\Delta z)|$, the magnitude of the amplification factor. We plot $|A|$ because the actual $A$ can be negative — but stability cares only about magnitude. A horizontal dashed line at $|A| = 1$ marks the stability bound: above it, the mode grows; at or below it, the mode is held or damped.

#### The four $\nu$ values

$\nu = 0.25, 0.5, 1.0, 5.0$. Each curve shows how that scheme responds to each wavenumber at that $\nu$.

#### FTCS panel

$$\boxed{\,\text{Worked example — FTCS at four $\nu$ values, evaluated at $k\Delta z = \pi$.}\,}$$

- $\nu = 0.25$: $A = 1 - 4(0.25) = 0$, so $|A| = 0$. Stable, well-resolved.
- $\nu = 0.5$: $A = 1 - 4(0.5) = -1$, so $|A| = 1$. Marginal stability — exactly on the bound at the 2-$\Delta z$ wave.
- $\nu = 1.0$: $A = 1 - 4(1) = -3$, so $|A| = 3$. **Unstable** — amplifies the worst wave by 3 per step.
- $\nu = 5.0$: $A = 1 - 4(5) = -19$, so $|A| = 19$. Massively unstable. After 4 time steps the worst wave grows by $19^{4} \approx 130\,000$.

The $\nu = 5$ curve is off the chart at $k\Delta z = \pi$ — the figure annotates this with "$\nu = 5$ off-scale (max $\approx 19$)". For lower $k\Delta z$ values (longer wavelengths) the curve is bounded but the high-$\nu$ behaviour at the worst wave is the catastrophic part.

#### BTCS panel

$$\boxed{\,\text{Worked example — BTCS at the same four $\nu$ values, at $k\Delta z = \pi$.}\,}$$

- $\nu = 0.25$: $A = 1/(1 + 1) = 0.5$. Worst wave decays to half each step.
- $\nu = 0.5$: $A = 1/(1 + 2) = 0.333$.
- $\nu = 1.0$: $A = 1/(1 + 4) = 0.2$.
- $\nu = 5.0$: $A = 1/(1 + 20) = 0.0476$. Worst wave is damped to near-nothing in a single step.

All four values are well below 1, monotonically decreasing in $\nu$. **BTCS is unconditionally stable AND strongly damps short waves at large $\nu$**. The figure shows monotonically decreasing curves for each $\nu$; at $k\Delta z = 0$ all curves equal 1 (no damping of constant fields), at $k\Delta z = \pi$ they reach the values above.

#### CN panel

$$\boxed{\,\text{Worked example — CN at the same four $\nu$ values, at $k\Delta z = \pi$.}\,}$$

- $\nu = 0.25$: $A = (1 - 0.5)/(1 + 0.5) = 0.5/1.5 = 1/3$. Worst wave decays to one-third per step.
- $\nu = 0.5$: $A = (1 - 1)/(1 + 1) = 0$. **The worst wave is exactly killed in one step at $\nu = 1/2$** — a special property of CN.
- $\nu = 1.0$: $A = (1 - 2)/(1 + 2) = -1/3$. $|A| = 1/3$.
- $\nu = 5.0$: $A = (1 - 10)/(1 + 10) = -9/11 \approx -0.818$. $|A| \approx 0.818$.

The $\nu = 5$ curve is below 1 but only barely at $k\Delta z = \pi$. The 2-$\Delta z$ wave loses only 18% per step at $\nu = 5$, compared to BTCS's 95% loss. This is the **weak-damping pathology of CN at large $\nu$**: short waves persist much longer than they should.

#### Why we have CN at all, given this weakness

Because at the *resolved* scales (small $k\Delta z$, where the physics actually lives), CN is *much more accurate per step* than BTCS — second-order vs first-order. The price is poorer damping of unresolved noise. For smooth problems with smooth initial conditions, CN gives much better daytime/nighttime profile fidelity per step. The project quantifies this trade-off: at $\Delta t = 600\,\mathrm{s}$, CN halves BTCS's diurnal-amplitude error.

The full curves of Figure 1 also show that CN curves *peak* somewhere in the middle of $k\Delta z$ for large $\nu$ — they dip toward zero around $k\Delta z = \pi/2$ and then rise back up. The dip is where CN damps best; the rise toward $|A| = 1$ at $k\Delta z = \pi$ is the pathology.

---

## Part 7. Walking through §3 — Methods

### 7.1 §3.1 — What "parameterised by $\alpha$" means in code

The report says: *All three schemes share a single step routine parameterised by* $\alpha$. In Python this means one function `step_alpha(T, dt, ..., alpha, ...)` that takes $\alpha$ as an argument, with FTCS, BTCS, CN recovered by passing `alpha=0.0, 1.0, 0.5`. The branch logic inside is short:

- When $\alpha = 0$: vectorised arithmetic update — no linear solve needed.
- When $\alpha > 0$: build the tridiagonal matrix and right-hand side, solve via `scipy.linalg.solve_banded((1,1), ab, rhs)`.

Benefit: any bug in the spatial discretisation affects all three schemes equally and cannot manufacture a fake difference between schemes in the comparison.

### 7.2 §3.2 — Substrate definitions, layer by layer

Three substrate columns, each 2 m deep:

**Asphalt road** (4 layers):
- Asphalt 0–5 cm: $\lambda = 0.75\,\mathrm{W\,m^{-1}\,K^{-1}}$, $C = 2.0\times 10^{6}\,\mathrm{J\,m^{-3}\,K^{-1}}$. The actual asphalt-and-aggregate paving layer.
- Aggregate 5–25 cm: $\lambda = 1.40$, $C = 2.4\times 10^{6}$. The high-conductivity sub-base.
- Dry soil 25–100 cm: $\lambda = 0.30$, $C = 1.3\times 10^{6}$. Native soil below the road bed.
- Subsoil 100–200 cm: $\lambda = 0.50$, $C = 1.8\times 10^{6}$. Slightly moist deep substrate.

**Concrete roof with insulation** (3 layers):
- Concrete deck 0–10 cm: $\lambda = 1.50$, $C = 2.1\times 10^{6}$. The slab itself — high $\lambda$ and high $C$, a strong storage layer.
- Mineral-wool / fibreglass-batt insulation 10–20 cm: $\lambda = 0.04$, $C = 0.08\times 10^{6}$. Extreme insulator: $\lambda$ jumps by a factor of 37 going down, $C$ by a factor of 26. This is the layer that stops summer heat reaching the room below.
- Drywall / wood interior 20–200 cm: $\lambda = 0.15$, $C = 1.5\times 10^{6}$. A composite of room-side materials.

**Bare soil reference**:
- Sandy loam 0–200 cm: $\lambda = 0.30$, $C = 1.3\times 10^{6}$ (uniform throughout). $\kappa = 2.31\times 10^{-7}$ — the lowest of the three substrates.

Why these three? They are intentionally chosen to span very different behaviours:

- Asphalt: moderately conductive surface over a heterogeneous subgrade. The sequence $\kappa$ from top down is $3.75 \to 5.83 \to 2.31 \to 2.78 \times 10^{-7}$ (jumps in both directions).
- Concrete roof: moderately conductive surface over an extreme insulator. $\kappa$ from top: $7.14 \to 5.0 \to 1.0 \times 10^{-7}$ (drops by 7×).
- Bare soil: uniform with low conductivity. $\kappa = 2.31\times 10^{-7}$ throughout.

Differences in scheme errors across these three substrates can therefore be traced to differences in their thermal structure — which is exactly what §5.3 of the report does.

### 7.3 §3.3 — The surface energy balance and Newton iteration

#### The SEB and what each term does

$$
\boxed{\;R_{n}(T_{s}^{0}) - H(T_{s}^{0}) - LE(T_{s}^{0}) - G(T_{s}^{0}) \;=\; 0\;}
$$

Components, with every symbol explained:

$$
R_{n} \;=\; (1 - \alpha_{s})\,S{\downarrow} \;+\; \varepsilon_{s}\,L{\downarrow} \;-\; \varepsilon_{s}\,\sigma\,(T_{s}^{0})^{4}
$$

- $\alpha_{s}$ — surface shortwave albedo, dimensionless, between 0 and 1. The fraction of incoming sunlight that is reflected. Asphalt = 0.10 (dark, absorbs almost all sunlight); concrete = 0.30; soil = 0.20. Note: same Greek letter $\alpha$ as the $\theta$-method weight, but different role and different value.
- $S{\downarrow}$ — incoming shortwave radiation at the surface (W/m²). Peaks $\approx 1000\,\mathrm{W/m^{2}}$ at solar noon for clear-sky conditions, zero at night.
- $\varepsilon_{s}$ — surface longwave emissivity, dimensionless, typically 0.9–0.98. The fraction of incident longwave that is absorbed (= fraction emitted by Kirchhoff's law). Asphalt = 0.95, concrete = 0.92, soil = 0.95.
- $L{\downarrow}$ — incoming longwave from the atmosphere (W/m²). Sky thermal emission. $\approx 350\,\mathrm{W/m^{2}}$ in the project's forcing.
- $\sigma = 5.67\times 10^{-8}\,\mathrm{W\,m^{-2}\,K^{-4}}$ — Stefan–Boltzmann constant.
- $(T_{s}^{0})^{4}$ — the fourth power of the surface temperature in Kelvin. The Stefan–Boltzmann emission law for a black body at temperature $T$. The factor of 4 in $(T_{s}^{0})^{4}$ is what makes the SEB nonlinear.

$$
H \;=\; \rho\,c_{p}\,\frac{T_{s}^{0} - T_{a}}{r_{a}},\qquad r_{a} \;=\; \frac{1}{C_{H}\,U}.
$$

- $\rho \approx 1.2\,\mathrm{kg/m^{3}}$ — air density.
- $c_{p} = 1005\,\mathrm{J\,kg^{-1}\,K^{-1}}$ — specific heat of air at constant pressure.
- $T_{a}$ — 2-metre air temperature in Kelvin.
- $r_{a}$ — aerodynamic resistance (s/m). Smaller $r_{a}$ means stronger surface-to-air coupling.
- $C_{H} = 5\times 10^{-3}$ — bulk transfer coefficient (a turbulence-derived factor).
- $U = 3\,\mathrm{m/s}$ — wind speed (constant in this project).

$$
LE \;=\; 0 \quad (\text{strict-impervious assumption}).
$$

$$
G \;=\; \lambda_{1/2}\,\frac{T_{s}^{0} - T_{1}}{z_{1} - z_{0}} \quad (\text{ground heat flux at the top half-level}).
$$

#### Why the SEB is nonlinear

The $(T_{s}^{0})^{4}$ Stefan–Boltzmann term makes the SEB nonlinear in $T_{s}^{0}$. We cannot rearrange to put $T_{s}^{0}$ on one side. We must find the root of $F(T_{s}^{0}) = R_{n} - H - LE - G$ as a function of $T_{s}^{0}$.

#### Newton's method derived from the linear approximation

Start with a guess $T_{s,\mathrm{old}}^{0}$. Approximate $F$ linearly around that point using a Taylor expansion truncated at first order:

$$
F(T) \;\approx\; F(T_{s,\mathrm{old}}^{0}) \;+\; F'(T_{s,\mathrm{old}}^{0})\,(T - T_{s,\mathrm{old}}^{0}).
$$

Set this approximation to zero (we want the root $F = 0$) and solve for $T$:

$$
0 \;\approx\; F(T_{s,\mathrm{old}}^{0}) \;+\; F'(T_{s,\mathrm{old}}^{0})\,(T_{s,\mathrm{new}}^{0} - T_{s,\mathrm{old}}^{0})
$$

$$
\boxed{\;T_{s,\mathrm{new}}^{0} \;=\; T_{s,\mathrm{old}}^{0} \;-\; \frac{F(T_{s,\mathrm{old}}^{0})}{F'(T_{s,\mathrm{old}}^{0})}\;}
$$

This is **one Newton step**. Iterate until $|T_{s,\mathrm{new}}^{0} - T_{s,\mathrm{old}}^{0}| < 10^{-4}\,\mathrm{K}$.

Newton's method has **quadratic convergence near the root**: the number of correct digits roughly doubles per iteration. From a warm start (we use the previous time step's $T_{s}^{0}$ as the initial guess), 3–5 iterations suffice for tolerance $10^{-4}\,\mathrm{K}$.

#### Why analytical Jacobian rather than finite-difference?

The full Jacobian:

$$
\frac{dF}{dT_{s}} \;=\; \frac{dR_{n}}{dT_{s}} \;-\; \frac{dH}{dT_{s}} \;-\; \frac{dG}{dT_{s}}.
$$

Computed term by term:

$$
\frac{dR_{n}}{dT_{s}} \;=\; -4\,\varepsilon_{s}\,\sigma\,(T_{s}^{0})^{3} \quad (\text{only Stefan–Boltzmann depends on }T_{s}^{0}).
$$

$$
\frac{dH}{dT_{s}} \;=\; \frac{\rho\,c_{p}}{r_{a}} \quad (\text{linear in }T_{s}^{0}, \text{coefficient is constant}).
$$

$$
\frac{dG}{dT_{s}} \;=\; \frac{\lambda_{1/2}}{z_{1} - z_{0}} \quad (\text{linear, constant coefficient}).
$$

Newton's method has quadratic convergence near the root **only if the Jacobian is exact**. With a finite-difference Jacobian, we either use a perturbation that is too small — so floating-point cancellation contaminates the derivative — or too large — so the linear approximation is no longer accurate near the root. Either way, we lose the quadratic convergence and pick up noise.

For our SEB residual, the analytical Jacobian is straightforward, with all three terms smooth functions of $T_{s}^{0}$. With this Jacobian and a warm start, Newton converges in 3–5 iterations to a tolerance of $10^{-4}\,\mathrm{K}$ — essentially free.

$$\boxed{\,\text{Worked example — one Newton step.}\,}$$

Suppose at $t = 0$, $T_{a} = 290\,\mathrm{K}$, $T_{1} = 290\,\mathrm{K}$, $S{\downarrow} = 0$ (midnight), $L{\downarrow} = 350\,\mathrm{W/m^{2}}$, and we guess $T_{s,\mathrm{old}}^{0} = 290\,\mathrm{K}$. Use the asphalt road's parameters: $\alpha_{s} = 0.10$, $\varepsilon_{s} = 0.95$, $\lambda_{1/2} = 0.75$, $z_{1} - z_{0} = 0.005\,\mathrm{m}$.

$F$ at the guess:

- $R_{n} = (0.9)(0) + (0.95)(350) - (0.95)(5.67\times 10^{-8})(290)^{4}$
- $= 0 + 332.5 - (5.39\times 10^{-8})(7.07\times 10^{9})$
- $= 332.5 - 381.0 = -48.5\,\mathrm{W/m^{2}}$.
- $H = (1.2)(1005)(290 - 290)/r_{a} = 0$.
- $G = (0.75)(290 - 290)/0.005 = 0$.
- $F = R_{n} - H - 0 - G = -48.5\,\mathrm{W/m^{2}}$. (Surface is losing more longwave than it gets — too warm.)

$F'$ at the guess:

- $dR_{n}/dT = -4(0.95)(5.67\times 10^{-8})(290)^{3} = -2.16\times 10^{-7}(2.44\times 10^{7}) = -5.27\,\mathrm{W/m^{2}/K}$.
- $dH/dT = (1.2)(1005)/r_{a}$. With $r_{a} = 1/(0.005)(3) = 66.7\,\mathrm{s/m}$: $dH/dT = 1206/66.7 = 18.1\,\mathrm{W/m^{2}/K}$.
- $dG/dT = 0.75/0.005 = 150\,\mathrm{W/m^{2}/K}$.
- $F' = -5.27 - 18.1 - 150 = -173.4\,\mathrm{W/m^{2}/K}$.

Newton update:

$$
T_{s,\mathrm{new}}^{0} = 290 - \frac{-48.5}{-173.4} = 290 - 0.28 = 289.72\,\mathrm{K}.
$$

The surface cools by 0.28 K in one Newton step. Subsequent steps would refine this further, with Newton's quadratic convergence reducing the residual by orders of magnitude per iteration.

### 7.4 §3.4 — The synthetic forcing

With $\omega = 2\pi/86\,400\,\mathrm{s}^{-1}$:

$$
S{\downarrow}(t) \;=\; \max\bigl[1000\,\cos(\omega(t - 12\,\mathrm{h})),\;0\bigr]\ \mathrm{W\,m^{-2}}\quad (\text{peak noon, zero night}),
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

Why 14:00 peak for $T_{a}$ and $L{\downarrow}$ but 12:00 for $S{\downarrow}$? In reality, the air takes about 2 hours to respond to peak solar input — the surface heats during the morning, transfers heat to the air via $H$, and the air mass reaches its maximum in early afternoon. The 2-hour lag is a standard simplification. The same lag is applied to $L{\downarrow}$ because $L{\downarrow}$ scales roughly with sky temperature, which tracks air temperature.

Why the $\max[\,\cdot\,, 0]$ in $S{\downarrow}$? Because solar radiation cannot be negative. At night, the sun is below the horizon; the cosine would go negative (no longer physical), so we clip at zero.

Why constant $U$? Methodological cleanness — holding $U$ constant isolates scheme errors from wind variations. It also makes the SEB Jacobian simpler (the wind-dependent $r_{a}$ is constant). Acknowledged as a simplification in §5.4 (iv) of the report.

### 7.5 §3.5 — Initialization

$$
T(z, 0) \;=\; T_{\text{mean}} \;+\; A_{0}\,\exp(-z/d_{\text{top}})\,\cos(-z/d_{\text{top}}),\qquad d_{\text{top}} \;=\; \sqrt{\frac{2\,\kappa_{\text{top}}}{\omega}},
$$

with $T_{\text{mean}} = 292.5\,\mathrm{K}$, $A_{0} = 7.5\,\mathrm{K}$, and $\kappa_{\text{top}} = \lambda_{\text{top}}/C_{\text{top}}$ from the topmost layer. This is the analytical damping-depth solution evaluated at $t = 0$ (when $\cos(\omega t - z/d) = \cos(-z/d) = \cos(z/d)$ since cosine is even).

There is a 12-hour phase mismatch: this initial profile assumes the surface is at peak temperature at $t = 0$, but the SEB-driven cycle peaks at 14:00 LT. So the column carries a transient that decays during day 1. By the start of day 2 the column has equilibrated, and day 2 is what we use for diagnostics.

### 7.6 §3.6 — Test 1 vs Test 2 setups

**Test 1 (verification):** uniform sandy-loam column, 1 cm uniform grid, $T_{s}^{0}(t) = T_{\text{mean}} + A_{0}\cos(\omega t)$ prescribed. Six configurations: FTCS at $\nu = 0.4$ and $\nu = 0.6$ (the latter expected to blow up); BTCS and CN at $\Delta t = 300\,\mathrm{s}$ ($\nu \approx 0.69$) and $\Delta t = 900\,\mathrm{s}$ ($\nu \approx 2.08$). Each runs 5 days; day-5 diagnostics vs analytical solution.

**Test 2 (prognostic SEB):** three substrates × three schemes × three time steps $\Delta t \in \{15, 60, 600\}\,\mathrm{s}$ = 27 cells. $\Delta t = 15\,\mathrm{s}$ is below FTCS bound on all three substrates (high-resolution reference). $\Delta t = 60\,\mathrm{s}$ is a typical mesoscale time step. $\Delta t = 600\,\mathrm{s}$ is a typical regional/climate-model time step.

---

## Part 8. Walking through §4 — Results

### 8.1 §4.1 — The damping-depth verification

#### The analytical solution and the $\pi/4$ phase lead — derived

For a semi-infinite uniform substrate with sinusoidal Dirichlet forcing $T_{s}(0, t) = \bar T + A\cos\omega t$, we want to solve

$$
\frac{\partial T}{\partial t} \;=\; \kappa\,\frac{\partial^{2} T}{\partial z^{2}}, \qquad T(0, t) = \bar T + A\cos\omega t, \qquad T \to \bar T \text{ as }z \to \infty.
$$

**Ansatz**: try $T(z, t) = \bar T + \mathrm{Re}[\,A\,e^{i(\omega t - K z)}\,]$ where $K$ is a complex wavenumber to be determined. Substitute:

$$
i\omega\,A\,e^{i(\omega t - K z)} \;=\; \kappa\,(-K^{2})\,A\,e^{i(\omega t - K z)}.
$$

Cancel the exponential and $A$:

$$
i\omega \;=\; -\kappa\,K^{2}\quad\Rightarrow\quad K^{2} \;=\; -i\omega/\kappa.
$$

Take the square root. Recall $\sqrt{-i} = (1 - i)/\sqrt{2}$. So:

$$
K \;=\; \pm\,\frac{1 - i}{\sqrt{2}}\,\sqrt{\omega/\kappa}.
$$

Take the root with positive real part (so the wave decays as $z \to \infty$, not grows):

$$
K \;=\; \frac{1 - i}{\sqrt{2}}\,\sqrt{\omega/\kappa} \;=\; \frac{1 - i}{d},\qquad d = \sqrt{2\kappa/\omega}.
$$

Now compute $-i K z$:

$$
-i K z \;=\; -i\,(1 - i)\,z/d \;=\; (-i + i^{2})\,z/d \;=\; (-i - 1)\,z/d \;=\; -z/d - i\,z/d.
$$

So $e^{i(\omega t - K z)} = e^{i\omega t}\,e^{-i K z} = e^{i\omega t}\,e^{-z/d - i z/d} = e^{-z/d}\,e^{i(\omega t - z/d)}$.

Take the real part:

$$
\boxed{\;T_{s}(z, t) \;=\; \bar T \;+\; A\,e^{-z/d}\,\cos(\omega t - z/d),\qquad d \;=\; \sqrt{2\kappa/\omega}\;}
$$

The temperature wave has two effects with depth: amplitude decays exponentially with characteristic length $d$; phase lags linearly with depth, with $z/d$ radians of lag per unit damping depth.

**Surface flux**. $G(0, t) = -\lambda\,\partial T/\partial z|_{z=0}$:

$$
\frac{\partial T}{\partial z} \;=\; A\,e^{-z/d}\,\left[-\frac{1}{d}\,\cos(\omega t - z/d) + \frac{1}{d}\,\sin(\omega t - z/d)\right].
$$

At $z = 0$:

$$
\frac{\partial T}{\partial z}\bigg|_{z=0} \;=\; \frac{A}{d}\,[\,-\cos\omega t + \sin\omega t\,].
$$

So:

$$
G(0, t) \;=\; -\lambda\,\frac{A}{d}\,[\,-\cos\omega t + \sin\omega t\,] \;=\; \lambda\,\frac{A}{d}\,[\,\cos\omega t - \sin\omega t\,].
$$

Use the trigonometric identity $\cos x - \sin x = \sqrt{2}\,\cos(x + \pi/4)$:

$$
\boxed{\;G(0, t) \;=\; \lambda\,\frac{A}{d}\,\sqrt{2}\,\cos(\omega t + \pi/4)\;}
$$

**Physical meaning of the $\pi/4$ lead**. $G$ peaks $\pi/4$ in phase before $T_{s}$ peaks. For a 24-hour period, $\pi/4$ of 24 h = 3 hours. So if $T_{s}$ peaks at noon, $G$ peaks at 9 AM — the substrate is absorbing heat fastest in mid-morning, when the surface is still warming most rapidly (steepest gradient at $z = 0$). At noon, $T_{s}$ is at its peak but no longer rising fast, so $G$ has already started to decline.

#### Reading Table 1

Six configurations on uniform sandy loam ($\kappa = 2.31\times 10^{-7}$, $\Delta z = 1\,\mathrm{cm}$), day-5 errors at $z = 10\,\mathrm{cm}$:

| Configuration | $\Delta t$ (s) | $\nu$ | RMSE $T$ (K) | RMSE $G$ (W/m²) |
|---|---|---|---|---|
| FTCS, $\nu = 0.4$ | 173.4 | 0.40 | 0.007 | 3.15 |
| FTCS, $\nu = 0.6$ (unstable) | 259.9 | 0.60 | BLEW UP at step 53 | — |
| BTCS, $\Delta t = 300$ | 300.0 | 0.69 | 0.024 | 3.31 |
| CN, $\Delta t = 300$ | 300.0 | 0.69 | 0.005 | 3.17 |
| BTCS, $\Delta t = 900$ | 900.0 | 2.08 | 0.062 | 3.61 |
| CN, $\Delta t = 900$ | 900.0 | 2.08 | 0.006 | 3.17 |

- FTCS at $\nu = 0.6$: blew up at step 53. Predicted growth $|A_{\mathrm{FTCS}}(0.6, \pi)| = |1 - 4(0.6)| = |-1.4| = 1.4$ per step. After 53 steps: $1.4^{53} \approx 5.5\times 10^{7}$ — overflow.
- BTCS error grows roughly linearly with $\Delta t$: $0.024$ at 300 s, $0.062$ at 900 s — ratio 2.6. First-order would predict ratio 3 (since $900/300 = 3$). Close enough.
- CN error stays flat: $0.005 \to 0.006$. **Empirical demonstration of CN's second-order accuracy** — doubling $\Delta t$ should quadruple the error if second-order, but we see almost no change. The reason: at this $\Delta t$ range, the time-stepping error has dropped below the spatial-discretisation error, which is independent of $\Delta t$.
- $\mathrm{RMSE}_{G} \approx 3$ W/m² for all stable schemes. This is a **spatial-discretisation residual**: the analytical $G$ uses the exact derivative $\partial T/\partial z|_{0}$, while the numerical version uses $(T_{0} - T_{1})/\Delta z$, which has $O(\Delta z^{2})$ truncation error. All stable schemes share this same residual; mesh refinement (smaller $\Delta z$) would reduce it.

### 8.2 §4.2 — Three-substrate prognostic SEB results

#### Reading Figure 3 — schemes agree at $\Delta t = 15\,\mathrm{s}$

Day-2 surface temperature evolution at $\Delta t = 15\,\mathrm{s}$ for all three schemes on each substrate. The three curves overlay to within line thickness on every substrate — **the schemes are visually indistinguishable**.

The peak surface temperatures:

| Substrate | Peak $T_{s}^{0}$ | Time of peak |
|---|---|---|
| Asphalt road | 50 °C | $\sim$13:00 |
| Concrete roof | 45 °C | $\sim$13:45 |
| Bare soil | 51 °C | $\sim$12:45 |

**Why bare soil is hottest.** Bare soil has the lowest $\kappa$ ($2.31 \times 10^{-7}$) — heat cannot diffuse downward fast enough. Combined with $LE = 0$, absorbed energy concentrates at the surface and pushes $T_{s}^{0}$ higher. Asphalt's higher $\kappa$ spreads heat downward more easily; concrete's higher albedo (0.30) reflects more shortwave in the first place. The bare-soil result is counter-intuitive at first — most people guess asphalt would be hottest because it is darkest — but the combination of low $\kappa$ and $LE = 0$ wins.

Note the time-of-peak ordering: bare soil peaks earliest (12:45), concrete roof latest (13:45). This too is a $\kappa$ story: low-$\kappa$ substrates respond quickly at the surface (the heat does not spread away), so they lock onto the peak forcing time; high-$\kappa$ substrates lag because they have to fill a deeper reservoir before the surface itself gets hot.

#### Reading Figure 4 — schemes diverge at $\Delta t = 600\,\mathrm{s}$

Day-2 $G(t)$ at $\Delta t = 600\,\mathrm{s}$ vs FTCS reference at $\Delta t = 15\,\mathrm{s}$. Key patterns:

- FTCS at $\Delta t = 600\,\mathrm{s}$ blows up on asphalt and concrete roof (figure annotations confirm this).
- BTCS at $\Delta t = 600\,\mathrm{s}$ overshoots the daytime $G$ peak by $\sim 40\%$ on asphalt and roof, $\sim 19\%$ on bare soil.
- CN at $\Delta t = 600\,\mathrm{s}$ overshoots by $\sim 21\%$ on asphalt, $\sim 26\%$ on roof, $\sim 10\%$ on soil — about half of BTCS.

**Why FTCS is stable on bare soil but not paved at $\Delta t = 600\,\mathrm{s}$**. Soil top cell has $\Delta z = 1\,\mathrm{cm}$ (not 0.5 cm — soil uses a coarser grid since its $d$ is smaller and resolving it does not require as fine a top cell), and $\kappa = 2.31\times 10^{-7}$. So $\Delta t_{\text{crit}} = 0.5(0.01)^{2}/(2.31\times 10^{-7}) \approx 217\,\mathrm{s}$. At $\Delta t = 600\,\mathrm{s}$, $\nu \approx 1.4$ — over the bound, but only modestly. The amplification factor at the worst wave is $|1 - 4(1.4)| = 4.6$ per step. For 2 days at $\Delta t = 600\,\mathrm{s}$ that is $\sim 290$ steps; if the worst wave were strongly excited, we would get $4.6^{290}$ growth. But the smooth initial profile and smooth Dirichlet boundary do not strongly excite the worst 2-$\Delta z$ wave; the actual growth is much less than the worst-case bound, and the integration completes (with substantial error in the diurnal cycle, as the AG_ratio of 1.017 reports). On asphalt with $\nu \approx 18$, growth rate $|1 - 4(18)| = 71$ per step, and the noise compounds to overflow within a handful of steps.

#### Reading Figure 5 — vertical profiles in the asphalt column

Vertical $T$ profiles in the asphalt column at three local times on day 2 (06:00, 12:00, 18:00), top 50 cm only. Reference is FTCS at $\Delta t = 15\,\mathrm{s}$; comparison is BTCS and CN at $\Delta t = 600\,\mathrm{s}$.

- 06:00 (steady cooling phase): all schemes agree closely. The column is in slow change, so the splitting error has little effect.
- 12:00 (peak heating phase): BTCS and CN are slightly warmer than reference near the surface — schemes are starting to diverge.
- 18:00 (immediately after sunset): largest divergence. BTCS at $\Delta t = 600\,\mathrm{s}$ holds the surface $\sim 2\,\mathrm{K}$ above the reference, with the largest deviation concentrated in the top 5 cm — the asphalt layer. CN is intermediate.

**Why the divergence appears after sunset rather than at the peak heating time.** Because that is when the surface is cooling most rapidly — $T_{s}^{0}$ is dropping fastest, and the operator-splitting error (Part 9.2) is largest when $T_{s}^{0}$ swings fastest between the column update and the SEB update. At 18:00 the column has been heated all day and has stored a lot of energy; the rapid evening cooling exposes the splitting error most clearly.

### 8.3 §4.3 — The cross-substrate quantitative summary (Table 2)

Table 2 has nine rows (3 substrates × 3 schemes), each with three columns reporting the day-2 metrics at $\Delta t \in \{15, 60, 600\}\,\mathrm{s}$. Each cell triple is $A_{G}/A_{\text{ref}}$ / $\mathrm{RMSE}_{T_{s}}$ / $S/S_{\text{ref}}$:

- $A_{G}/A_{\text{ref}}$ — diurnal $G$ amplitude normalised to the FTCS $\Delta t = 15\,\mathrm{s}$ reference. Value 1.000 = perfect; 1.400 = over-amplified by 40%.
- $\mathrm{RMSE}_{T_{s}}$ — root-mean-squared error of $T_{s}^{0}$ across the 24-hour day-2 cycle, in K.
- $S/S_{\text{ref}}$ — daily storage integral $S = \int G\,dt$ over day 2, normalised. If $S/S_{\text{ref}} \approx 1$, the daily mean storage is preserved across schemes.

Three patterns:

1. **Substrate ordering at $\Delta t = 600\,\mathrm{s}$**. RMSE is largest for concrete roof (3.69 K BTCS, 2.10 K CN), middle for asphalt (2.10 K BTCS, 1.12 K CN), smallest for bare soil (0.53 K BTCS, 0.28 K CN). The $\kappa_{\text{top}}$ values: soil 2.31, asphalt 3.75, roof 7.14 (all $\times 10^{-7}$). **Error scales with $\kappa_{\text{top}}$** — the same parameter that sets the FTCS stability bound.

2. **Scheme ordering**. At fixed substrate and $\Delta t$, CN errors are roughly half of BTCS errors. The factor-of-two improvement.

3. **Storage preservation**. $S/S_{\text{ref}}$ stays within $\pm 5\%$ of unity (largest deviation: 0.958, a 4.2% deficit, for concrete roof BTCS at $\Delta t = 600\,\mathrm{s}$). So even when the diurnal $G$ amplitude is over-amplified by 40%, the daily mean is preserved. The over-amplification is symmetric in day/night.

---

## Part 9. Walking through §5 — Discussion

### 9.1 §5.1 — Why FTCS stability is set by the most thermally stiff layer

On a stretched-grid layered substrate, the FTCS stability constraint applies cell by cell: $\nu_{j} = \kappa_{j}\,\Delta t/\Delta z_{j}^{2} \le 1/2$ for every cell $j$. The cell with the smallest $\Delta z_{j}^{2}/\kappa_{j}$ sets the bound:

| Substrate | Stiffest cell | $\Delta z$ | $\kappa$ | $\Delta t_{\text{crit}}$ |
|---|---|---|---|---|
| Asphalt road | top asphalt cell | 0.5 cm | $3.75\times 10^{-7}$ | 33 s |
| Concrete roof | concrete deck top cell | 0.5 cm | $7.14\times 10^{-7}$ | 17 s |
| Bare soil | top sandy-loam cell | 1.0 cm | $2.31\times 10^{-7}$ | 217 s |

Notice the order: the most diffusive substrate (concrete) is the most restrictive, not the least. This is the inverse of what naive intuition might suggest. The phrase "thermally stiff" describes the property: a stiff equation is one where the time-step constraint is set by the *fastest-evolving component*, even if that component is small. In our problem, the topmost cm of concrete is the fastest-responding component, and it sets the stiff time-step bound for the whole column.

The conclusion drawn from this is that FTCS is structurally ruled out for any model that resolves the cm-scale near-surface layers needed to capture the diurnal damping depth in highly conductive urban materials. **Implicit treatment of vertical conduction is not optional — it is required.**

> **[Notes #11 Misconception #1]** says: *"High Resolution Fixes Everything — Reality: Not so!"* The misconception is that running models at higher resolution will automatically lead to more accurate forecasts. The lecture explains that high resolution depends on consistent surface fields, realistic physics, and high-quality observations.
>
> The project's result is a different angle on the same misconception: high resolution is not free — once you commit to resolving the cm-scale damping depth, you also commit to giving up explicit time stepping. The "high resolution does not solve everything" lesson manifests here as: high resolution forces you to absorb the cost of implicit schemes, and then the implicit-scheme errors (which §5.2 documents) become the new performance ceiling.

### 9.2 §5.2 — The operator-splitting error, derived

This is the most subtle physical argument in the report. The amplitude inflation of $G$ at large $\Delta t$ is **not** explained by the von Neumann picture (BTCS damps everything; one would expect under-amplification). The real explanation is **operator splitting** between the column update and the SEB update.

#### How the splitting works in the code

Each time step has two sub-steps in sequence:

- **Sub-step A — column update.** Hold $T_{s}^{0}$ fixed at its current value (which is $T_{s}^{0}$ from the start of the time step). Solve the heat conduction equation in the column for one $\Delta t$. New interior temperatures $T_{1}^{n+1}, T_{2}^{n+1}, \ldots, T_{N-1}^{n+1}$.
- **Sub-step B — SEB update.** With the new interior values fixed (especially $T_{1}^{n+1}$), solve the SEB by Newton iteration for the new $T_{s}^{0}$.

Notice: during sub-step A the column relaxed toward equilibrium with $T_{s}^{0}$ from the **start** of the step. In sub-step B the SEB then jerks $T_{s}^{0}$ to its new value — but the column does not re-respond to that change within the same step. So the column has "over-relaxed" relative to where it should be at the end of the step.

#### Why this produces over-amplification in BTCS

Consider sunset. $T_{s}^{0}$ is dropping fast — say from 35 °C to 25 °C in one $\Delta t = 600\,\mathrm{s}$. With the column-then-SEB ordering:

- **Sub-step A** holds $T_{s}^{0}$ at 35 and the column relaxes to that. After sub-step A, $T_{1}$ is mostly equilibrated to 35.
- **Sub-step B** computes the new $T_{s}^{0} = 25$. But the column is still equilibrated to 35 — $T_{1}$ has not updated.

The gradient at the top half-level is $(T_{s}^{0} - T_{1})/(z_{1} - z_{0})$ with $T_{s}^{0} = 25$ and $T_{1}$ still effectively at 35. Gradient is much steeper than the true coupled solution would have. $G$ is correspondingly larger in magnitude. **That is the over-amplification.**

BTCS evaluates the diffusion operator entirely at the post-swing temperature, so it amplifies this gradient steepening the most. CN evaluates half-old, half-new, so half the swing is cancelled — CN's error is half of BTCS's.

> **[Notes #10 §8 — The Order of the Processes in Time Integration]** says (verbatim): *"Implicit scheme brings the local profiles into equilibrium, but without accounting for the other tendencies it can be the wrong equilibrium — equilibrium with respect to only one process is not the same as equilibrium with respect to all interacting processes."*
>
> And: *"Without including the dynamic tendencies in the implicit computation of the diffusion, the diffusion scheme will relax toward the wrong equilibrium for long time steps."*
>
> This is exactly the project's column-first-then-SEB pathology. The report's §5.2 cites this lecture verbatim. The lecture's prescribed cure: **fully coupled solution** of the strongly interacting processes (column AND SEB inside the same implicit solve), or **carefully designed ordering** in which strongly interacting processes are solved together.
>
> The lecture also warns: *"With more than one implicit process there is no real solution to the ordering problem — different orderings give different answers, and no single sequential ordering is fully correct."* That is why the project measures the splitting error (it is unavoidable in the column-then-SEB ordering), then proposes the fully coupled solve as the cure.

#### Why both BTCS and CN show first-order scaling

If the dominant error were the within-substep CN truncation error, CN would be second-order: doubling $\Delta t$ would quadruple the error. But the **operator-splitting error is first-order in $\Delta t$ regardless of the per-substep scheme**: the gradient error scales linearly with how far $T_{s}^{0}$ has swung between updates, which scales linearly with $\Delta t$. So both BTCS (intrinsically first-order) and CN (intrinsically second-order) end up showing the same first-order scaling, because that is the dominant error.

Empirically, the report reports $\Delta t$-refinement ratios in $[8.2, 10.2]$ for both BTCS and CN across all three substrates. The expected first-order ratio is $600/60 = 10$. The empirical numbers cluster around 10. **This is the smoking-gun evidence** that the dominant error is operator splitting, not the per-substep scheme.

#### Reading Table 3

Six rows (three substrates × two schemes — FTCS does not appear because at $\Delta t = 600\,\mathrm{s}$ on asphalt and roof it blows up):

| Surface | Scheme | RMSE at 60 s | RMSE at 600 s | Ratio |
|---|---|---|---|---|
| Asphalt | BTCS | 0.225 | 2.104 | 9.4 |
| Asphalt | CN | 0.114 | 1.115 | 9.8 |
| Roof | BTCS | 0.450 | 3.686 | 8.2 |
| Roof | CN | 0.229 | 2.102 | 9.2 |
| Soil | BTCS | 0.053 | 0.529 | 9.9 |
| Soil | CN | 0.027 | 0.279 | 10.2 |

All six ratios are in $[8.2, 10.2]$ — first-order range. A second-order scheme would show ratios near 100. The fact that CN shows ratios near 10, not 100, is the empirical confirmation that the operator-splitting error dominates.

### 9.3 §5.3 — Why $\kappa_{\text{top}}$ dominates substrate dependence

If admittance $\mu = \sqrt{\lambda C}$ alone explained the substrate ordering, asphalt:roof error ratio would be $\sim 1\!:\!1.5$ (since $\mu_{\text{asphalt}} \approx 1220$ and $\mu_{\text{roof}} \approx 1770$). Empirical ratio is closer to $1\!:\!1.75$. Bare soil with $\mu \approx 624$ — about half of asphalt — has scheme error one *quarter* of asphalt's, not one half. So admittance alone does not explain the substrate dependence.

§6 SHAP attribution identifies $\kappa_{\text{top}}$ as the dominant predictor: 92% of the variance from $\kappa_{\text{top}}$ alone. Bulk admittance $\mu_{\text{eff}}$ is the strongest residual predictor; max $\lambda$ contrast across internal interfaces is small and inconsistent.

Why $\kappa_{\text{top}}$ wins over $\mu$? Because the operator-splitting error is governed by **how fast the top cell responds** to a change in $T_{s}^{0}$, not by **how much heat the column can store**. $\kappa_{\text{top}}$ measures the former (the response rate); $\mu$ measures the latter (the storage capacity). The mechanism is fundamentally about **rate of relaxation**, so $\kappa_{\text{top}}$ is the right scaling parameter.

### 9.4 §5.4 — Implications, limitations, outlook

#### UHI implication: diurnal range bias, not mean bias

The §4.3 result that storage ratios stay within ±5% across all schemes and $\Delta t$ underwrites the UHI interpretation. Over a full day, total heat in equals total heat out. So the over-amplified diurnal $G$ cycle that BTCS produces at $\Delta t = 600\,\mathrm{s}$ is symmetric: more heat goes in during the day, more comes out at night, daily mean preserved.

What is biased is the diurnal range. Simulated nocturnal warming is larger than reality (more stored heat being released), and simulated dawn-time cooling is sharper. For a mesoscale model running at $\Delta t = 60\,\mathrm{s}$ with BTCS: 4–6% nocturnal $G$ inflation on asphalt and concrete, 2% on bare soil; at $\Delta t = 600\,\mathrm{s}$: 40% and 20% respectively.

> **[Notes #11 Misconception #8]** is the home concept: surface conditions in models are not directly forecast but diagnosed from a balance, and errors in any of the surface-budget components — including the numerical treatment of $G$ — propagate directly into the simulated near-surface temperature.

#### The four numbered limitations

(i) **$LE = 0$** strict-impervious. Realistic for new pavement, underestimates real cities.

(ii) **Symmetric synthetic forcing**. Real cities show asymmetric morning warming and slow evening cooling.

(iii) **Independent columns**. A real urban canopy is a tile-weighted mix of facets.

(iv) **Constant $U = 3\,\mathrm{m/s}$**. Under time-varying $U$ the Newton SEB Jacobian would need updating each step.

#### How to remove the splitting error structurally

**Option A: Fully coupled SEB-row solve.** Augment the tridiagonal column system with one extra row and one extra column representing the SEB residual at the surface. The Newton iteration linearises $F(T_{s}^{0})$ at each step; that linearised SEB equation can be assembled into the column system, with the result that the two processes are no longer split. The first-order splitting error vanishes, leaving only the per-substep CN truncation error (which is second-order for CN). This is the lecture-prescribed cure in [Notes #10 §8].

**Option B: Strang splitting.** A symmetric reorganisation. Replace the standard column-then-SEB ordering A–B at full $\Delta t$ with the symmetric sandwich:

$$
\text{A}(\Delta t/2) \;\to\; \text{B}(\Delta t) \;\to\; \text{A}(\Delta t/2).
$$

Why this works: let $A$ be the operator that advances the column and $B$ the operator that advances the SEB. The standard split approximates $e^{(A+B)\Delta t} \approx e^{B\Delta t}\,e^{A\Delta t}$, with leading error proportional to the commutator $[A, B]\,\Delta t^{2}/2$ — first-order in $\Delta t$. The symmetric Strang form approximates $e^{(A+B)\Delta t} \approx e^{A\Delta t/2}\,e^{B\Delta t}\,e^{A\Delta t/2}$, with the symmetry cancelling the leading commutator term and leaving the next-order $O(\Delta t^{3})$ — that is, second-order in $\Delta t$ for the splitting itself.

Cost: Strang takes two A-steps per $\Delta t$ (each at half-$\Delta t$), plus one B-step. Roughly 50% more expensive than the standard split. But the splitting error drops by an order of magnitude at fixed $\Delta t$. Strang splitting is the natural intermediate step before going all the way to a fully-coupled solve.

The full project outlook: couple this diagnostic framework to an offline run of an operational urban canopy scheme (WRF-SLUCM or WRF-TEB) for a real city's substrate composition with flux-tower-derived forcing. That moves the analysis from idealised columns to operational relevance.

---

## Part 10. Walking through §6 — Independent SHAP attribution

### 10.1 What problem §6 is solving

The mechanistic argument of §5 ranks $\kappa_{\text{top}}$, admittance $\mu$, and layer-interface descriptors as candidate predictors of BTCS coarse-$\Delta t$ error. The three idealised substrates differ in *all three* properties simultaneously, so a three-substrate comparison cannot disentangle which is dominant. §6 fixes this by sampling a synthetic ensemble of 150 three-layer columns with random property values, running BTCS at coarse $\Delta t$ against a reference, and using machine learning to identify the dominant predictor across the wider parameter space.

The aim is **not** to build a predictive ML model — the experiment is too small for that — but to use SHAP feature importance as a *measurement instrument* for the relative contributions of substrate descriptors to BTCS coarse-$\Delta t$ error.

### 10.2 §6.1 — The synthetic ensemble

150 three-layer substrate columns sampled from a wide prior:

- Top-layer $\lambda \in [0.10, 2.50]\,\mathrm{W\,m^{-1}\,K^{-1}}$ (covers everything from foam to dense aggregate).
- Middle-layer $\lambda \in [0.05, 2.50]$ (covers the rigid-insulation extreme $\lambda \approx 0.04$ and the high-conductivity aggregate extreme).
- Bottom-layer $\lambda \in [0.10, 1.00]$.
- All $C \in [0.5, 3.0]\times 10^{6}\,\mathrm{J\,m^{-3}\,K^{-1}}$.
- Top-layer thickness 2–15 cm; middle 5–30 cm; bottom extends to 200 cm.

Each column is run at BTCS $\Delta t = 600\,\mathrm{s}$ and at a BTCS reference at $\Delta t = 15\,\mathrm{s}$ for two diurnal cycles under the §3.4 synthetic forcing. Day-2 surface-temperature RMSE between the two is the target $y$.

Six substrate descriptors are used as features:

- Bulk admittance $\mu_{\text{eff}} = \sqrt{\lambda_{\text{eff}}\,C_{\text{eff}}}$, depth-weighted over the top 30 cm.
- Top-cell thermal diffusivity $\kappa_{\text{top}} = \lambda_{\text{top}}/C_{\text{top}}$.
- Maximum $\lambda$ contrast across any internal interface: $\max(\lambda_{\text{above}}/\lambda_{\text{below}}, \lambda_{\text{below}}/\lambda_{\text{above}})$.
- Number of "significant" internal interfaces (contrast $> 1.5$).
- Depth of the first significant interface.
- Top-layer thickness $h_{\text{top}}$.

### 10.3 §6.2 — Gradient-boosted regression and SHAP

#### What is gradient boosting?

A machine-learning regression method that builds an ensemble of small decision trees, each trying to correct the errors of the previous one. Concretely:

- Start with a constant prediction $\hat y_{0} = \overline{y}$ (the mean target value).
- At iteration $m$, fit a small decision tree to the residuals $y - \hat y_{m-1}$. Add the tree's output, scaled by a learning rate $\eta$:

$$
\hat y_{m}(x) \;=\; \hat y_{m-1}(x) \;+\; \eta\,\mathrm{tree}_{m}(x).
$$

- Repeat for $M$ iterations. The final prediction is

$$
\hat y_{M}(x) \;=\; \hat y_{0} \;+\; \sum_{m=1}^{M} \eta\,\mathrm{tree}_{m}(x).
$$

For our project: $M = 200$, max depth 3, learning rate $\eta = 0.05$. Six features → one target. The model captures nonlinear relationships and feature interactions automatically.

A "decision tree" is a small flowchart-like model: at each node, ask a question about one feature ("is $\kappa_{\text{top}} > 5\times 10^{-7}$?"); follow the yes/no branch to the next node; eventually arrive at a leaf node with a predicted value. Max depth 3 means at most 3 questions before reaching a leaf.

#### What is SHAP?

**SHAP** stands for **SHapley Additive exPlanations**. It is a method, based on cooperative game theory, for assigning each feature in a machine-learning model a fair contribution to each prediction.

The math comes from Lloyd Shapley (1953), who proved a uniqueness theorem: there is exactly one allocation rule that satisfies four reasonable axioms simultaneously, and that rule averages each player's marginal contribution over all possible orderings of the coalition. The four axioms:

1. **Efficiency**: the sum of each feature's contribution equals the difference between the prediction and the baseline.
2. **Symmetry**: if two features are interchangeable (always have the same effect when swapped), they get the same contribution.
3. **Dummy / Null player**: a feature that contributes nothing to any subset gets contribution zero.
4. **Additivity**: contributions from a sum of two models are the sum of contributions to each.

For each prediction $\hat y(x)$ and each feature $f$, SHAP computes a value $\phi_{f}(x)$ such that

$$
\hat y(x) \;=\; \text{baseline} \;+\; \sum_{f}\,\phi_{f}(x).
$$

The $\phi_{f}$ are signed: positive means $f$ pushed the prediction up, negative means down. Aggregating across the dataset, the **mean absolute SHAP** $\overline{|\phi_{f}|}$ gives a global feature-importance ranking.

For tree ensembles like gradient boosting, SHAP values can be computed exactly in polynomial time via the **TreeExplainer** algorithm (Lundberg & Lee, 2017) — much faster than the exhaustive cooperative-game-theory definition would suggest.

#### Model fit metrics

- **In-sample $R^{2} = 0.96$**. The model fits the training data well.
- **5-fold cross-validated $R^{2} = 0.61$**. The model generalises moderately. About 40% of variance is not captured by the six features — consistent with the small sample size and the fact that the full $\lambda(z), C(z)$ functional form is not fully captured by six scalar descriptors.

The reason both numbers are reported is intellectual honesty: in-sample is too optimistic (the model has memorised some of the noise); CV is the realistic estimate of out-of-sample performance. The feature ranking is robust under both metrics, but absolute SHAP magnitudes have noise consistent with the CV gap.

In **k-fold cross-validation**, the dataset is split into $k$ groups (here $k = 5$). The model is trained on $k-1$ groups and evaluated on the held-out group; this is repeated $k$ times so each group serves as the held-out test set once. The reported CV $R^{2}$ is the average across the 5 folds. This is a standard ML practice for estimating how well a model will perform on new data it has not seen.

### 10.4 §6.3 — The findings

Figure 6 has four panels:

**Panel (a)** — Mean $|\mathrm{SHAP}|$ values for the full feature set. $\kappa_{\text{top}}$ is the tallest bar at 0.71 K. $\mu_{\text{eff}}$ and max $\lambda$-contrast are tied at 0.18–0.20 K. $h_{\text{top}}$, first-interface-depth, and $n_{\text{interfaces}}$ are smaller.

**Panel (b)** — SHAP dependence on $\kappa_{\text{top}}$, points coloured by $\mu_{\text{eff}}$. Shows the SHAP value for $\kappa_{\text{top}}$ as a function of $\kappa_{\text{top}}$ across the 150 samples. Monotone, near-log-linear positive dependence: higher $\kappa_{\text{top}}$ → larger SHAP value (i.e., $\kappa_{\text{top}}$ pushed the predicted RMSE up by more). The colour-by-$\mu_{\text{eff}}$ reveals an interaction: at fixed $\kappa_{\text{top}}$, larger $\mu_{\text{eff}}$ also increases the SHAP value, consistent with admittance as a secondary predictor.

**Panel (c)** — Residual SHAP importance after $\kappa_{\text{top}}$ is partialled out. Concretely: fit a small GBR on $\log(\kappa_{\text{top}})$ only, predict, compute residuals, then fit a second GBR on the residuals using the other five features, and compute SHAP for that second model. $\mu_{\text{eff}}$ dominates the residual; layer-interface descriptors contribute small amounts. Confirms admittance is the dominant secondary predictor.

**Panel (d)** — Predicted vs observed RMSE on the in-sample fit, points coloured by max $\lambda$-contrast on a log scale. Tight clustering along the 1:1 line confirms in-sample $R^{2} \approx 0.96$.

#### Why $\kappa_{\text{top}}$? The mechanistic connection

The same $\kappa_{\text{top}}$ that sets the FTCS stability bound also sets the prefactor of the BTCS coarse-$\Delta t$ operator-splitting error. Higher $\kappa_{\text{top}}$ means the top cell relaxes to $T_{s}^{0}$ faster within sub-step A, which means the gradient at the top half-level swings more between sub-step A and sub-step B. The splitting error scales linearly with that swing magnitude, hence linearly with $\kappa_{\text{top}}$. The SHAP attribution recovers this connection empirically: the strongest predictor of BTCS coarse-$\Delta t$ error is the same parameter that sets the FTCS stability bound. The connection is mechanistic, not a coincidence.

Reconciling with the three-substrate result of §4.3: the three substrates differ in $\kappa_{\text{top}}$ by ratios $1.0:1.62:3.09$ for soil:asphalt:roof. The error ratios should follow approximately the $\kappa_{\text{top}}$ ratios (with admittance and interface effects giving second-order corrections). The three-substrate pattern is consistent with the SHAP finding.

### 10.5 §6.4 — Limitations of the attribution

- **Fixed grid.** $\Delta z_{\text{top}} = 0.5\,\mathrm{cm}$ is the same in every synthetic column. The dimensionless ratio $\Delta t \times \kappa_{\text{top}}/\Delta z_{\text{top}}^{2}$ is what really matters for stability and the splitting error, but the ensemble varies $\kappa_{\text{top}}$ while holding $\Delta z_{\text{top}}$ fixed. Follow-up: vary $\Delta z_{\text{top}}$ and regress against the dimensionless group directly.
- **Sample size.** 150 columns is small for ML. The 5-fold CV $R^{2}$ of 0.61 reflects this. Feature ordering is robust at this $n$; absolute SHAP magnitudes have a few percent of noise.
- **Forcing-specific.** Same synthetic SEB and $LE = 0$ assumption as §3. Conclusions transfer directly to that setting; may not generalise to runs with non-zero latent flux or asymmetric forcing.

---

## Part 11. Walking through §7 — Conclusions

The conclusions section is a five-bullet recap of everything that came before, with bullets matching §7 (i)–(v) numbering.

**(i) FTCS conditional stability**, $\nu \le 1/2$. On a stretched-grid layered substrate the bound is set by the most thermally stiff layer. For asphalt and concrete the critical $\Delta t$ is 33 s and 17 s respectively — well below operational mesoscale time steps. **Implication: implicit treatment of vertical conduction is structurally required.**

**(ii) BTCS and CN unconditionally stable.** At $\Delta t = 600\,\mathrm{s}$, BTCS over-amplifies the diurnal $G$ amplitude by 40% on asphalt, 41% on roof, 19% on soil. CN halves these to 21%, 26%, 10%. Surface temperature RMSE up to 3.7 K on the roof.

**(iii) The empirical $\Delta t$-refinement ratios for both BTCS and CN are close to 10:1 between $\Delta t = 60$ s and $\Delta t = 600$ s — first-order in $\Delta t$.** This identifies the dominant error as a first-order operator-splitting error in the column-then-SEB ordering, not the schemes' own per-substep temporal accuracy. The factor-of-two reduction in CN error compared to BTCS at fixed $\Delta t$ is a prefactor effect: CN's $\alpha = 1/2$ splitting partially cancels the post-swing operator evaluation that BTCS's $\alpha = 1$ retains. Consistent with the wrong-equilibrium warning of [Notes #10 §8].

**(iv) The daily storage integral $\int G\,dt$ is preserved across schemes within ±5%.** So the diurnal $G$ amplitude inflation translates into an inflation of the diurnal range of the simulated nocturnal urban heat island, not a bias in its mean.

**(v) Dominant predictor of BTCS coarse-$\Delta t$ error is $\kappa_{\text{top}}$**, identified by SHAP attribution on a gradient-boosted regression. $\kappa_{\text{top}}$ alone explains 92% of the variance in $\mathrm{RMSE}_{T_{s}}$. Bulk admittance is secondary; layer-interface descriptors smaller. Reconcilable with the §5.3 three-substrate finding because the three substrates differ in $\kappa_{\text{top}}$ AND admittance AND layer structure jointly.

**Closing.** Two follow-ups: fully coupled SEB-row solve (the [Notes #10 §8] cure), or Strang splitting (cheaper alternative). Longer-term outlook: couple this diagnostic to an offline WRF-SLUCM or WRF-TEB run for a real city with flux-tower forcing.

---

## Part 12. Mastery cheat-sheet

### 12.1 The single most important sentence

> **"The dominant error in BTCS at $\Delta t = 600\,\mathrm{s}$ is not the within-substep truncation error; it is the operator-splitting error between the column update and the SEB update, which is first-order in $\Delta t$ regardless of the per-substep scheme."**

Everything else in the project — the von Neumann analysis, the substrate ordering, the SHAP attribution — is a supporting argument for this sentence.

### 12.2 The three numbers to memorise

1. **$\Delta t_{\text{crit}} = 17\,\mathrm{s}$** for the concrete deck top cell ($\Delta z = 5\,\mathrm{mm}$, $\kappa = 7.14\times 10^{-7}$). The "$\Delta t < \tfrac{1}{2}\Delta z^{2}/\kappa$" formula made concrete.
2. **BTCS over-amplifies the diurnal $G$ amplitude by 40% on asphalt** at $\Delta t = 600\,\mathrm{s}$. CN halves this to 21%.
3. **$\kappa_{\text{top}}$ alone explains $R^{2} = 0.92$** of the BTCS coarse-$\Delta t$ error variance across 150 synthetic substrate columns.

### 12.3 The five concepts you must define on demand

- **Diurnal damping depth** $d = \sqrt{2\kappa/\omega}$. Depth at which the daily wave decays to $e^{-1} \approx 37\%$ of surface amplitude.
- **Diffusion number** $\nu = \kappa\Delta t/\Delta z^{2}$. Dimensionless control parameter for FTCS stability — bound $\nu \le 1/2$.
- **Harmonic mean conductivity** $\lambda_{j+1/2} = 2\lambda_{j}\lambda_{j+1}/(\lambda_{j}+\lambda_{j+1})$. Preserves heat flux exactly across a $\lambda$ discontinuity.
- **Operator splitting / wrong-equilibrium pathology**. Sub-step A relaxes the column to start-of-step $T_{s}^{0}$; sub-step B updates $T_{s}^{0}$; the column does not see the swing within the same step.
- **SHAP value**. Fair allocation, from cooperative game theory, of feature contribution to a prediction. Mean $|\mathrm{SHAP}|$ over the dataset is a global feature-importance ranking.

### 12.4 Common follow-up questions and the right answers

**Q: Why CN over BTCS?** A: CN is second-order in time intrinsically and cuts the BTCS coarse-$\Delta t$ error in half at fixed $\Delta t$. The remaining error is operator splitting, which both schemes share. CN gives "BTCS for free" until you fix the splitting.

**Q: Why does FTCS work on bare soil at $\Delta t = 600\,\mathrm{s}$ but not on asphalt?** A: $\nu \approx 1.4$ on soil (over the bound, but smooth forcing keeps the unstable mode small) versus $\nu \approx 18$ on asphalt (so far over the bound that the noise compounds within a few steps).

**Q: Why is bare soil error a quarter of asphalt error, not half?** A: Operator-splitting error scales with $\kappa_{\text{top}}$, not with admittance. Soil $\kappa_{\text{top}}$ is about 60% of asphalt's, but error scales nonlinearly through the splitting mechanism — and SHAP confirms $\kappa_{\text{top}}$ alone accounts for 92% of variance.

**Q: Why don't you just remove operator splitting?** A: That is the recommended follow-up — fully coupled SEB-row solve or Strang splitting. Within this project, we wanted to *characterise* the error, not eliminate it. Knowing splitting is the dominant error tells us removing it would give the largest accuracy gain — much bigger than switching from BTCS to CN.

### 12.5 Lecture-notes index for this project

| Project section | Lecture-note source |
|---|---|
| §1 motivation, UHI | [Notes #11 Misconception #3] surface conditions |
| §2.1 conductivity-form heat equation | [Notes #2 Parabolic class] |
| §2.2 staggered grid, half-levels | [Notes #8] Staggered Grid |
| §2.3 $\theta$-method (FTCS, BTCS, CN) | [Notes #6 §6 Slides 15–17] Single-Stage Two-Level Schemes |
| §2.5 von Neumann analysis | [Notes #6 §10] + [Notes #9 Pure Diffusion / Implicit Diffusion] |
| §3.3 tridiagonal solver | [Notes #9 Practical Considerations] |
| §5.1 stability vs resolution | [Notes #11 Misconception #1] |
| §5.2 operator-splitting error | [Notes #10 §8] Order of the Processes |
| §5.4 UHI diagnostic interpretation | [Notes #11 Misconception #8] |

### 12.6 Homework index for this project

| Project topic | Your HW work |
|---|---|
| FTCS blow-up | **HW1** FTCS blew up at step 113 on tracer advection (max\|q\| > 10) |
| Amplification factors $\|A_{k}\|$ vs wavenumber | **HW4** $\|A_{k}\|$ vs $k\Delta x$ for various CFL numbers, peak at $k\Delta x = \pi/2$ |
| Three-scheme comparison (Euler/Backward/Trapezoidal) | **HW3** Euler unstable, Backward damping, Trapezoidal neutral on $d\psi/dt = i\omega\psi$ |
| Staggered grid | **HW5** Numerical phase speed comparison, 2-$\Delta x$ wave decoupling on unstaggered grid |
| Wave amplitude and period diagnostics | **HW2** Sine-wave advection, period & amplitude tracking |
| Matsuno predictor-corrector | **HW3 Case 4** — first-order but explicit, predicts then corrects |

---

## Part 13. Glossary of every symbol used in the project

This is the mastery glossary — every Greek letter, every subscript, every notation that appears in the long report.

**Symbols used as scheme parameters**

- $\alpha$ — In the $\theta$-method context: the implicitness weight. $\alpha = 0$ FTCS, $\alpha = 1/2$ CN, $\alpha = 1$ BTCS.
- $\alpha_{s}$ — Surface shortwave albedo (dimensionless, 0–1). Note: same Greek letter $\alpha$ but different role and different value.

**Symbols used in the heat conduction equation**

- $T_{s}(z, t)$ — Substrate temperature at depth $z$ and time $t$. Units K.
- $T_{s}^{0}$ — Surface temperature, $T_{s}$ at $z = 0$. Units K.
- $T_{a}$ — 2-metre air temperature. Units K.
- $z$ — Vertical depth, $z = 0$ at the surface, increasing downward. Units m.
- $z_{\text{top}}$ — Bottom of the column. $z_{\text{top}} = 2\,\mathrm{m}$ in the project.
- $z_{j}$ — Depth of cell-centre $j$.
- $z_{j+1/2}$ — Depth of half-level (face) between cells $j$ and $j+1$.
- $\Delta z_{j}$ — Thickness of cell $j$. Range 0.5 cm at surface to ~30 cm at depth.
- $t$ — Time. Units s.
- $\Delta t$ — Time step. Project uses 15, 60, 300, 600, 900 s in different runs.
- $n$ — Time-level index ($t = n\Delta t$).
- $\lambda_{s}$ — Substrate thermal conductivity. Units W m⁻¹ K⁻¹.
- $\lambda_{j+1/2}$ — Half-level conductivity, computed via harmonic mean.
- $C_{s}$ — Volumetric heat capacity. Units J m⁻³ K⁻¹.
- $\kappa = \lambda / C$ — Thermal diffusivity. Units m² s⁻¹.
- $\kappa_{\text{top}}$ — Top-cell diffusivity. Sets FTCS bound and dominates SHAP attribution.

**Heat flux and conservation**

- $G(z, t)$ — Conductive heat flux. Units W m⁻². Sign: $G > 0$ means downward.
- $G_{j+1/2}$ — Discrete flux at face between cells $j$ and $j+1$.
- $q$ — Same as $G$ but written without the project-specific sign convention; $q = -\lambda\,\partial T/\partial z$ as in standard Fourier's law.
- $S = \int G\,dt$ — Daily storage integral. Units J/m².

**SEB components**

- $R_{n}$ — Net radiation. Units W m⁻². $R_{n} = (1-\alpha_{s})S{\downarrow} + \varepsilon_{s}L{\downarrow} - \varepsilon_{s}\sigma T_{s}^{4}$.
- $H$ — Sensible heat flux. Units W m⁻². $H = \rho c_{p}(T_{s} - T_{a})/r_{a}$.
- $LE$ — Latent heat flux. Set to 0 in this project.
- $S{\downarrow}$ — Incoming shortwave radiation. Peaks at 1000 W/m² at noon.
- $L{\downarrow}$ — Incoming longwave from atmosphere. ~350 W/m².
- $\varepsilon_{s}$ — Surface longwave emissivity. 0.92–0.95 in the project.
- $\sigma = 5.67 \times 10^{-8}\,\mathrm{W\,m^{-2}\,K^{-4}}$ — Stefan–Boltzmann constant.
- $\rho \approx 1.2\,\mathrm{kg/m^{3}}$ — Air density.
- $c_{p} = 1005\,\mathrm{J\,kg^{-1}\,K^{-1}}$ — Specific heat of air.
- $C_{H} = 5\times 10^{-3}$ — Bulk transfer coefficient for sensible heat.
- $U = 3\,\mathrm{m/s}$ — Wind speed (constant in this project).
- $r_{a} = 1/(C_{H} U)$ — Aerodynamic resistance. Units s/m.
- $F(T_{s}^{0})$ — SEB residual. $F = R_{n} - H - LE - G$. Newton iteration finds the root $F = 0$.

**Wave and stability analysis**

- $\omega = 2\pi/86\,400\,\mathrm{s}^{-1}$ — Diurnal angular frequency.
- $d = \sqrt{2\kappa/\omega}$ — Diurnal damping depth.
- $A$ — Surface temperature amplitude in the analytical damping-depth solution. $A_{0} = 7.5\,\mathrm{K}$ in the project's initialisation.
- $\bar{T}$, $T_{\text{mean}}$ — Mean surface temperature in the analytical solution. 292.5 K.
- $k$ — Spatial wavenumber. Units rad/m.
- $k\Delta z$ — Dimensionless wavenumber, range $[0, \pi]$ on the grid.
- $A_{k}(\nu, k\Delta z)$ — Per-step amplification factor for wavenumber $k$ at diffusion number $\nu$.
- $|A_{k}|$ — Magnitude of the amplification factor. Stability requires $|A_{k}| \le 1$ for all $k$.
- $\nu = \kappa\,\Delta t/\Delta z^{2}$ — Diffusion number. FTCS bound: $\nu \le 1/2$.

**Test 2 metrics**

- $A_{G}$ — Half-amplitude of the diurnal $G$ cycle, $(\max G - \min G)/2$.
- $A_{G}/A_{\text{ref}}$ — Diurnal $G$ amplitude normalised to FTCS $\Delta t = 15$ s reference.
- $\mathrm{RMSE}_{T_{s}}$ — Root-mean-squared error of $T_{s}^{0}$ across day-2 cycle. Units K.
- $S/S_{\text{ref}}$ — Daily storage integral ratio. ~1.0 means daily mean preserved.

**SHAP analysis**

- $N$ — Sample size in the synthetic ensemble. $N = 150$.
- $\mu_{\text{eff}} = \sqrt{\lambda_{\text{eff}} C_{\text{eff}}}$ — Bulk substrate admittance. Units J m⁻² K⁻¹ s⁻¹/².
- $h_{\text{top}}$ — Top-layer thickness in the synthetic ensemble.
- $\phi_{f}(x)$ — SHAP value for feature $f$ on data point $x$.
- $|\mathrm{SHAP}|$ or $\overline{|\phi_{f}|}$ — Mean absolute SHAP value of feature $f$. Global importance.
- $R^{2}$ — Coefficient of determination. Fraction of target variance explained by the model.

---

## Part 14. Common confusions and how to clear them up

These are the points where readers most often get stuck. Each one is a one-paragraph clarification.

### 14.1 "Why is $\alpha$ used for two different things?"

In the $\theta$-method context, $\alpha$ is the implicitness weight (0, 1/2, or 1). In the SEB context, $\alpha_{s}$ is the surface shortwave albedo (a number between 0 and 1 specific to each substrate). Same Greek letter, different role. The subscript $s$ on $\alpha_{s}$ is the disambiguator. When the report writes "α = 0 gives FTCS", it means the implicitness weight; when it writes "α_s = 0.10 for asphalt", it means the albedo.

### 14.2 "Why $\kappa$ instead of $\lambda$ in the diffusivity form?"

Because the heat equation can be written equivalently in two forms:

$$
C\,\partial T/\partial t \;=\; \partial/\partial z\,(\lambda\,\partial T/\partial z) \quad \text{(conductivity form)}
$$

$$
\partial T/\partial t \;=\; \kappa\,\partial^{2}T/\partial z^{2} \quad \text{(diffusivity form, when $\lambda, C$ constant)}.
$$

The two forms are equivalent only when $\lambda$ and $C$ are constant. In our layered substrates they are not constant — they jump across material interfaces — so we must use the conductivity form. The von Neumann analysis (which assumes constant coefficients) uses the diffusivity form because it is mathematically simpler and the stability conclusions transfer back.

### 14.3 "Why does $\nu$ matter and not $\Delta t$ alone?"

Because stability is a *dimensionless* property. The same $\Delta t$ on a finer grid is more stable than on a coarser grid (if everything else is held constant), because finer $\Delta z$ gives a tighter resolution of the spatial derivative. The dimensionless combination $\nu = \kappa\,\Delta t/\Delta z^{2}$ captures the right trade-off: doubling $\Delta z$ at fixed $\kappa$ allows $\Delta t$ to grow by a factor of 4 while keeping $\nu$ fixed.

### 14.4 "Why does $k\Delta z$ go up to $\pi$, not $2\pi$?"

Because the finest wavelength resolvable on the grid is $\lambda_{\min} = 2\Delta z$ (the alternating-sign pattern between adjacent cells). Wavenumber relates to wavelength as $k = 2\pi/\lambda$, so $k_{\max} = 2\pi/(2\Delta z) = \pi/\Delta z$, hence $k\Delta z_{\max} = \pi$. Wavenumbers above this are aliased — they appear on the grid as longer-wavelength patterns and cannot be distinguished from them.

### 14.5 "Why is FTCS first-order but the centred-space part is second-order?"

The "FTCS" name combines "Forward in Time, Centred in Space". The forward-time part (forward Euler) is first-order in $\Delta t$. The centred-space part is second-order in $\Delta z$. Overall accuracy is the worse of the two, so FTCS is first-order in time, second-order in space — usually summarised as just "first-order". BTCS is the same temporally (backward Euler is first-order in $\Delta t$). CN is second-order in both time and space.

### 14.6 "Why did the abstract say FTCS blows up on all substrates, but the original report's §4.2 says soil completes?"

This was an inconsistency in the original report that was corrected in `modified_full_report_1.docx`. The corrected abstract reads: "FTCS blows up at $\Delta t = 60\,\mathrm{s}$ on the concrete roof and at $\Delta t = 600\,\mathrm{s}$ on the asphalt road and concrete roof" — soil at $\Delta t = 600\,\mathrm{s}$ is over the bound but completes (with substantial error). See the audit trail in `clarify_project.docx` Part 4.

### 14.7 "Why is bare soil hottest if asphalt has the lowest albedo?"

Because two factors compete: (a) absorption rate at the surface, controlled by $1 - \alpha_{s}$; (b) downward heat conduction rate, controlled by $\kappa$. Asphalt absorbs more (lower albedo), but its higher $\kappa$ also spreads the absorbed heat downward more efficiently. Bare soil has moderate absorption but very low $\kappa$, so absorbed heat concentrates at the surface. Combined with $LE = 0$ (no evaporative cooling), bare soil ends up with the hottest surface in this idealised setup.

### 14.8 "Why is the operator-splitting error first-order even though CN is second-order?"

The splitting error and the per-substep CN truncation error are two different error sources. CN's second-order accuracy applies to the per-substep integration of one process (the column or the SEB) — but only if the "right" tendencies are inside the implicit operator. In our column-then-SEB ordering, sub-step A solves the column with a *fixed* $T_{s}^{0}$; the SEB tendency on $T_{s}^{0}$ within sub-step A is omitted, so the sub-step does not reach the correct multi-process equilibrium. The mismatch between sub-step-A's single-process equilibrium and the true coupled equilibrium scales linearly with $\Delta t$ (because $T_{s}^{0}$ swings linearly with $\Delta t$). That linear-in-$\Delta t$ mismatch is the splitting error. It is independent of which scheme (BTCS or CN) is used inside sub-step A.

### 14.9 "Why is $\kappa_{\text{top}}$ the dominant SHAP feature when admittance is what governs daily heat storage?"

Admittance $\mu = \sqrt{\lambda C}$ governs how much heat the column can store over a half-cycle, but the *operator-splitting error* depends on how much $T_{s}^{0}$ swings between sub-step A and sub-step B — which is governed by how fast the *top cell* responds to a change in $T_{s}^{0}$. The top-cell response speed is set by $\kappa_{\text{top}} = \lambda_{\text{top}}/C_{\text{top}}$, not by $\mu$. So the SHAP attribution is identifying the right physical scaling: error rate, not error magnitude.

### 14.10 "What would I gain by using a fully-coupled solver instead?"

You would eliminate the first-order operator-splitting error. The remaining error would be the per-substep CN truncation error, which is second-order. Quantitatively: at $\Delta t = 600\,\mathrm{s}$ the splitting error is the dominant contribution to the 1.1 K BTCS error on asphalt; eliminating it could in principle reduce the error to the second-order CN truncation level, perhaps 0.1–0.2 K. Strang splitting recovers second-order accuracy at lower implementation cost. Both options are listed in the report's outlook.

---

*End of document. Companion files in this repository:*

- `modified_full_report_1.docx` — the corrected long report
- `equations.md` — LaTeX-rendered equation reference
- `clarify_project.docx` — the .docx version of this walkthrough
- `clarify_project.md` — this file (LaTeX-rendered, with lecture-notes and HW references)
- `Lecture_1_2_3_4_5_6_7_8_9_10_11_Notes.md` — your professor's lecture notes
- `HW1_Solution.docx` ... `HW6_Submission.pdf` — your six homeworks
