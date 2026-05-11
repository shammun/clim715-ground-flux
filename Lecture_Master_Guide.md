# CLIM-715 — Master Study Guide

## *Numerical Methods for Weather & Climate Modeling — Plain-English, Mastery-Level Walkthrough*

> **Who this guide is for.** If you know a little calculus (you can take a derivative, you have heard of partial derivatives, you remember what $e^{ix}$ means) and you know nothing else about numerical modeling, this guide is for you. Every symbol is defined the first time it appears. Every equation is unpacked in plain English. Every abstract idea is paired with a concrete weather/climate example. Wherever a homework numerically demonstrates a concept, the result is folded in.
>
> **How to read.** Read top to bottom on a first pass. The chapters build on each other. On a second pass you can jump to any chapter; each one is self-contained and re-defines key symbols.

---

## Table of Contents

1. [Big-Picture Orientation: What Is Weather/Climate Modeling?](#1)
2. [The Story of How We Got Here (Newton → AI)](#2)
3. [Chaos: Why Weather Is Hard but Climate Is Possible](#3)
4. [Partial Differential Equations (PDEs) — The Language of the Atmosphere](#4)
5. [Mathematical Toolkit: Taylor Series, MVT, Eulerian vs Lagrangian](#5)
6. [The Atmospheric Equations and Their Approximations](#6)
7. [Waves Hidden Inside the Equations: Sound, Gravity, Rossby](#7)
8. [Why and How We Filter Sound Waves](#8)
9. [Finite Differences: How a Computer Replaces a Derivative](#9)
10. [Four Properties of a Numerical Scheme: Accuracy, Consistency, Stability, Convergence](#10)
11. [Stability Analysis I — The Energy Method](#11)
12. [Stability Analysis II — Von Neumann (Fourier) Analysis](#12)
13. [The CFL Condition: A Physical View of Stability](#13)
14. [Time-Differencing Schemes and the Oscillation Equation](#14)
15. [Computational Modes and the Leapfrog Story](#15)
16. [Space Differencing — Phase, Group Velocity, Numerical Dispersion](#16)
17. [The Modified Equation, Artificial Dissipation, Higher Order](#17)
18. [Combining Time and Space (Total Error)](#18)
19. [Staggered Grids](#19)
20. [Aliasing and Nonlinear Instability](#20)
21. [Diffusion, the Péclet Number, Implicit Schemes](#21)
22. [Turbulence, the Closure Problem, the Planetary Boundary Layer](#22)
23. [Source/Sink Terms (Parameterizations) — Radiation, Convection, Microphysics](#23)
24. [Common Modeling Misconceptions](#24)
25. [Glossary of Every Symbol](#25)

---

<a id="1"></a>

# 1 Big-Picture Orientation

## 1.1 Weather vs. climate — what we are trying to predict

- **Weather** is "what the sky is doing right now (and tomorrow and next week)." It is the *short-term* state of the atmosphere — temperature, wind, rain, humidity — over minutes to days.
- **Climate** is the *long-term statistical pattern* of weather, typically averaged over **30 years or more**. Climate tells you the *expected* temperature and rainfall and how variable they are. Weather tells you the *exact* condition at a moment.

A useful analogy: **weather is one roll of the dice; climate is the probability distribution of all rolls.** Or said differently: **weather is what you *get*; climate is what you *expect*.**

**The bathtub analogy.** Weather modeling is like predicting the exact pattern of *ripples on the water surface* 5 seconds from now — you need to know every detail of the current ripple pattern. Climate modeling is like predicting the *average water level* over the next year — that depends on how much water comes from the faucet (incoming solar radiation, CO₂ forcing) and how much drains out (outgoing radiation), not on the exact ripples right now.

The 30-year averaging window in climate is the conventional choice for capturing multi-decadal oscillations (like ENSO, NAO, AMO) while filtering out chaotic weather noise. Shorter windows still feel "weatherish"; longer windows risk averaging out genuine climate change.

| Feature | Weather Modeling | Climate Modeling |
|---|---|---|
| Goal | Predict specific events (this Tuesday's storm) | Predict statistical trends (next century's average) |
| Forecast horizon | Hours → ~14 days | Decades → centuries |
| Type of problem | **Initial-value problem** (depends on starting state) | **Boundary-forced problem** (depends on CO₂, sun, ocean, etc.) |
| Resolution | Fine, 1–10 km | Coarse, 25–200 km |
| Time step | Minutes | Hours → days |
| Observations | Heavy real-time assimilation | Long spin-ups, less DA |
| Coupling | Often atmosphere only | Fully coupled Earth system (atm, ocean, ice, land) |
| Main uncertainty | Initial condition errors | Forcing + feedback uncertainties |
| Output | Storms, rain, winds | Trends, variability, extremes |

**Plain-English takeaway.** The same equations are solved in both — but a *weather* run cares about getting *this* day right, while a *climate* run cares about getting the long-term average and variability right. They use different time steps and different resolutions for different reasons.

**The deepest distinction — initial-value vs. boundary-value.**
A *weather* forecast asks: "Given the state of the atmosphere right now, what does it look like at +6 h, +24 h, +5 d?" Tiny errors in "right now" balloon into huge errors a week later. That's why we run **ensembles** (many slightly perturbed starts) and why we invest enormous effort in **data assimilation**.
A *climate* projection asks: "Given the long-term forcings (CO₂, solar, oceans, ice), what equilibrium statistics emerge?" The atmosphere "forgets" its initial state after a few weeks, so you don't need to know the starting day exactly — you need the *boundary forcings* right. Improving CO₂ pathways and ocean–atmosphere coupling matters more than nailing the starting wind field.

**Why the table's resolution and time-step columns are coupled.** Weather models need very fine spatial resolution (1–10 km) to capture thunderstorms, fronts, and squall lines. As you'll see later (§13), the **CFL condition** ties the time step rigidly to the grid spacing — finer grids *force* shorter time steps. So a fine-resolution weather model isn't "fine because we want it" — it's also expensive in time-stepping. Climate models can run at coarser grids partly because their time step is also longer, keeping each multi-decade run computationally feasible.

## 1.2 What goes into a model?

A modern weather/climate model is a "system of systems":

- **Numerical algorithms** that solve the equations of motion (PDEs).
- **Equations** for physical, biological, and chemical behavior.
- **Source/sink terms** (heating, evaporation, etc.).
- **Sub-grid-scale parameterizations** for processes too small for the grid (turbulence, convection, radiation, clouds).
- **Initial conditions (ICs)** — the starting snapshot of the atmosphere.
- **Boundary conditions (BCs)** — what's happening at the edges (top, bottom, sides) of the model domain.
- **Surface datasets** — terrain, land use, soil moisture, sea-surface temperature.
- **Pre-/post-processing** to start the model up and to interpret its output.
- **Improvement techniques** like four-dimensional data assimilation (4DDA) and ensemble forecasting.

A model has to *do* a lot of things at once: ingest observations, integrate physics, run on a supercomputer, and report back.

## 1.3 What can a model do (and why is this powerful)?

- **Predict the future.**
- **Fill in gaps in observations** in a physically consistent way (a model gives you wind at 35,000 ft over the Atlantic where there is no station).
- **Run experiments we cannot do in nature** ("What if CO₂ doubled overnight?").
- **Linearize and simplify** to test theories.
- **Run ensembles** — many slightly different versions of the same forecast — to give probabilities.

## 1.4 What goes wrong (the persistent problems)?

- The atmosphere is **turbulent and variable** — even a perfect equation cannot capture every eddy.
- ICs and BCs are imperfect — we never know the exact starting state.
- Sub-grid processes (a thunderstorm inside a 25 km grid box, a leaf evaporating water) are not resolved and must be **parameterized** (approximated).
- Computing power is finite — there is always a trade-off between resolution and cost.
- A single model run gives one realization. Reality might play out differently — hence ensembles.

---

<a id="2"></a>

# 2 How We Got Here — A 300-Year Tour

## 2.1 Newton (~1687)

Newton's second law $\vec{F} = m\vec{a}$ told us that *acceleration* of a fluid parcel equals *force* divided by *mass*. The laws of fluid motion and mass conservation were known in principle. **But** the thermodynamics — how heating a fluid changes its state — was missing, so there was no way to turn observations into a *forecast*.

## 2.2 The thermodynamics is added (~1858, von Helmholtz)

With Boyle, Charles, Joule, Rumford, Laplace, and finally von Helmholtz's first law of thermodynamics in 1858, the picture was complete: the **number of state variables** (pressure, density, temperature, three wind components) finally matched the **number of independent equations** (momentum × 3, mass conservation, energy conservation, equation of state). The system became *closed* (solvable in principle).

**Why this counting matters.** Imagine you have 7 unknown values you need to find (3 wind components, $T$, $p$, $\rho$, $q$). To solve for 7 unknowns, you need exactly 7 independent equations. Before thermodynamics, scientists had fewer equations than unknowns — the system was *underdetermined* (infinitely many possible solutions). After thermodynamics, the count matched: 7 equations, 7 unknowns. **A solvable system!** This is exactly why von Helmholtz's contribution is *the* foundational moment of modern atmospheric physics.

## 2.3 Bjerknes (1904) — the modern vision

Vilhelm Bjerknes wrote down the first explicit recipe for prediction:

> Future state of atmosphere = $f$(initial conditions, boundary conditions, governing physical laws).

He proposed to do it graphically. He couldn't compute fast enough. He founded the **Bergen School** and the **Polar Front Theory** of midlatitude cyclones.

## 2.4 Richardson (1922) — the first numerical attempt

Lewis Fry Richardson tried to solve the equations *by hand* using **finite differences**. He worked between ambulance shifts during WWI. His 6-hour forecast took **6 weeks** to compute and predicted a pressure change **100× too large**. The error came from the equations admitting fast gravity waves — which his crude scheme couldn't filter, so they corrupted the answer.

**Why Richardson failed — the fast-wave problem.** Richardson was solving the *primitive equations* — the full, unfiltered set of atmospheric equations. These equations support very fast gravity waves and acoustic waves moving at hundreds of m/s. His initial conditions, derived from imperfect station data, were slightly **unbalanced** with respect to these fast waves. His finite-difference scheme then amplified the unbalanced fast-wave signals over the 6-hour forecast, producing wildly unrealistic pressure tendencies. **The bug wasn't his arithmetic; it was his choice of equations.**

This is the deep lesson of Richardson's work: **equation choice matters as much as discretization**. Charney's 1948 success would come precisely from designing a *different* set of equations (filtered to remove fast waves) — not from a better numerical method.

Richardson dreamed of a "**weather factory**" with 64,000 humans computing in parallel — essentially the concept of parallel computing, decades before electronic computers existed. That dream came true 25 years later, only with silicon instead of humans.

## 2.5 The CFL paper (1928)

Courant, Friedrichs, and Lewy proved that the stability of numerical solutions of PDEs depends on the **ratio** of $\Delta t$ to $\Delta x$, not their individual sizes. This is the seed of every modern stability proof.

## 2.6 Charney, von Neumann, ENIAC (1948–1950)

Jule Gregory Charney derived the **quasi-geostrophic potential vorticity equation** — a *filtered* version of the equations that hides sound and gravity waves so they cannot blow up the forecast. On the new ENIAC computer, Charney and von Neumann produced the first skillful **24-hour barotropic forecast** in **April 1950**.

**The genius of Charney's approach.** He didn't just invent better equations — he *filtered out the problematic waves entirely*. The QGPV equation reduces the full equations of motion to a single prognostic equation for the slow geostrophic flow. Critically, the fast sound and gravity waves that destroyed Richardson's forecast **cannot mathematically appear** in Charney's equations — they were eliminated at the level of the equations themselves, not via numerical tricks. **Choose your equations to match what your numerical method can handle.**

## 2.7 The path to today

- 1962: First operational baroclinic QG forecasts.
- 1963: Lorenz discovers chaos.
- 1971: First regional model.
- 1974: First global operational model.
- 1990s–2000s: WRF, MM5, RAMS, OMEGA, fully compressible models, LES, DNS, ensemble forecasting.
- Today: Operational NWP runs at ~10–25 km globally; ~1–3 km regionally. AI/ML emulators, exascale computing, "digital twin of Earth" are the next frontier.

## 2.8 Why this history matters for *you* as a modeler

Each tool in your modern model exists because someone hit a wall:

- **Filtering** (Charney) exists because Richardson's raw equations blew up — fast acoustic and gravity waves overwhelmed the slow weather-relevant signal.
- **The CFL condition** (Courant–Friedrichs–Lewy) exists because numerical schemes don't *know* the speed of physical signals unless you tell them via $\Delta t \leq \Delta x/c$.
- **Ensemble forecasting** exists because Lorenz proved that a single forecast can't be trusted past a chaotic predictability horizon.
- **Data assimilation (4D-Var, EnKF)** exists because Lorenz proved that initial errors matter — so we'd better fix them as best we can each cycle.
- **Sub-grid parameterizations** exist because the grid is finite but the physics isn't.
- **Staggered grids** exist because un-staggered grids can split into non-talking sub-grids and butcher short waves.

When you read about a new model feature, ask: *what wall did this break through?*

---

<a id="3"></a>

# 3 Chaos: Why Weather Is Hard but Climate Is Possible

## 3.1 Lorenz's discovery (1963)

Edward Lorenz built a tiny model — a convection cell, **not even a weather model** — using three coupled nonlinear ODEs:

$$\frac{dx}{dt} = \sigma(y - x)$$
$$\frac{dy}{dt} = x(\rho - z) - y$$
$$\frac{dz}{dt} = xy - \beta z$$

| Symbol | Meaning |
|---|---|
| $x$ | Strength and direction of the overturning circulation |
| $y$ | Horizontal temperature gradient |
| $z$ | Static stability of the fluid |
| $\sigma$ | **Prandtl number** — ratio of momentum diffusivity to thermal diffusivity |
| $\rho$ | **Rayleigh number** — strength of buoyant forcing |
| $\beta$ | A geometric factor |

## 3.2 What he saw

Starting with two *almost identical* initial conditions (differing in the seventh decimal place), the solutions tracked each other for a while, then **diverged completely**. The system never settled. It never repeated. But it stayed inside a butterfly-shaped region in 3-D space — the **Lorenz attractor**.

**The butterfly metaphor.** Tiny perturbations grow exponentially. A 0.0001 °C measurement error today can produce a totally different forecast in a week.

**Why this happens — the role of nonlinearity.** Look at the Lorenz equations: the third term in the second equation is $-xz$, and in the third equation it's $+xy$. These are **products of unknowns** — they are nonlinear. Linear systems amplify errors at most exponentially with a fixed rate; **nonlinear systems can route errors through their own structure** and produce wildly divergent outcomes. This is why a *linear* atmosphere would still be hard to predict but not chaotic, while the real (nonlinear) atmosphere has a hard predictability horizon.

**The three stages of a Lorenz run.** A typical Lorenz integration unfolds in three phases that any modeler will recognize:
1. **Shock phase** — the initial conditions are slightly unbalanced, so the model experiences wild transients while it adjusts.
2. **Spin-up phase** — the oscillations grow as the system settles into its dynamical regime.
3. **Chaotic regime** — the fluid shifts between clockwise and counterclockwise circulation in a *nonperiodic* way, never exactly repeating but never leaving the attractor either.

This three-stage pattern (shock → spin-up → chaos) reappears in real atmospheric model runs as well — which is why operational models are run for a "spin-up period" of hours to days before the forecast is considered trustworthy.

**The marble-bowl analogy.** Think of the atmosphere as a marble rolling around inside a bowl shaped like a butterfly. You can predict where it will be now and a few seconds from now. But beyond a certain time, tiny nudges send it to the other wing of the butterfly. **The shape of the bowl (the set of possible states — the climate) is stable, but the exact path of the marble (the weather) is unpredictable.** And as Lorenz himself put it, with characteristic dryness: *"We certainly hadn't been successful at doing that anyway and now we had an excuse."*

## 3.3 Why this matters

- **Weather is an initial-value problem** → exact prediction has a *finite predictability horizon* (~10–14 days for the atmosphere).
- **Climate is a statistical problem** → the *attractor itself* is stable, even if any single trajectory is not. We can predict the climate's long-term *distribution* even when we cannot predict its individual *trajectories*.
- **Ensembles** are essential: run many slightly perturbed forecasts to estimate the spread of possible outcomes.
- **Data assimilation** is essential: small errors amplify, so getting the IC right matters enormously.

**Plain-English takeaway.** A pinball machine has a "shape" (where the balls tend to settle) — that's climate. Any individual ball's path is unpredictable — that's weather.

---

<a id="4"></a>

# 4 PDEs — The Language of the Atmosphere

## 4.1 Why PDEs?

Atmospheric variables (temperature $T$, pressure $p$, wind $u$, $v$, $w$, density $\rho$, humidity $q$) depend on **multiple independent variables**: time $t$, space $x$, $y$, $z$. So the equations involve **partial derivatives** like $\partial T/\partial t$ (rate of change of $T$ with $t$, holding $x, y, z$ fixed).

## 4.2 Order

- **Order** of a PDE = highest order of any partial derivative in the equation.
- Atmospheric models are usually first-order in time (one $\partial/\partial t$).
- Example, 1st-order PDE: $\dfrac{\partial \psi}{\partial t} + u \dfrac{\partial \psi}{\partial x} = 0$.
- Example, 2nd-order PDE: $\dfrac{\partial^2 \psi}{\partial t^2} + \psi \dfrac{\partial \psi}{\partial x} = 0$.

**Direction-giving analogy.** A 1st-order equation is like saying: *"You're at position X right now. Here's how fast you should be moving."* That's enough — from your current position and your speed, you can figure out where you'll be next. One piece of information (your current position) is all you need. A 2nd-order equation in time is like: *"You're at position X with velocity V. Here's your acceleration."* Now you need *two* initial conditions: position *and* velocity. This is why second-order time PDEs (like the wave equation) require two ICs while first-order ones need only one.

## 4.3 Linear, quasi-linear, nonlinear

- **Linear PDE** — coefficients in front of derivatives depend only on the independent variables ($x$, $t$), not on the unknown $u$ itself. Example: $\dfrac{\partial u}{\partial t} + c\dfrac{\partial u}{\partial x} = 0$ with $c$ a constant.
- **Quasi-linear** — equation is linear *in the highest derivatives*, but coefficients can depend on $u$. Example: $A(x,t,u)\partial u/\partial t + B(x,t,u)\partial u/\partial x = C(x,t,u)$.
- **Nonlinear** — products of $u$ with itself or with its derivatives. Example: **Burgers's equation** $\dfrac{\partial u}{\partial t} + u\dfrac{\partial u}{\partial x} = 0$. The coefficient in front of $\partial u/\partial x$ is *the unknown itself*.

**Plain-English picture.** In a *linear* advection equation the wind speed $c$ is fixed (everything moves at the same speed). In a *nonlinear* equation, taller parts of a wave move faster than shorter parts — so the wave breaks (think of an ocean wave steepening near shore).

**Why linearity matters — superposition.** If $u_1$ is a solution and $u_2$ is a solution of a *linear* PDE, then $u_1 + u_2$ is also a solution. This means you can break a complicated problem into simple pieces, solve each piece separately, and add them together. **Fourier analysis** rests entirely on this: a complicated wave is a sum of pure sinusoids, each evolving independently. Nonlinear PDEs *forbid* this — modes interact, energy moves between them (which is exactly the engine of turbulence and aliasing, §20).

## 4.4 Characteristics — the key idea

**Building the intuition: Eulerian vs. Lagrangian.** Imagine you're standing on a bridge watching leaves float down a river. There are two ways to study the motion:
- **Way 1 (Eulerian):** Stand still on the bridge and watch different leaves pass by your fixed position. You record which leaf is at your spot at each moment.
- **Way 2 (Lagrangian):** Jump onto a leaf and ride it downstream. You experience the journey of *one* parcel.
The method of characteristics is essentially switching from Way 1 to Way 2. Where the Eulerian view sees a complicated PDE in $(x, t)$, the Lagrangian view (riding the characteristic) sees a much simpler ODE.

Consider the general 1st-order quasi-linear PDE:

$$A(x,t,u)\frac{\partial u}{\partial t} + B(x,t,u)\frac{\partial u}{\partial x} = C(x,t,u).$$

There are special curves in the $(x,t)$ plane along which the PDE collapses into an *ordinary* differential equation. These are the **characteristics**. Along them, the solution is "carried" — information about $u$ is transported along these lines.

The characteristic equation is

$$\frac{dx}{dt} = \frac{B}{A}.$$

**Why characteristics matter — they are information highways.** A characteristic curve answers three concrete questions:
1. **Where did the information come from?** Trace backward along the characteristic to the initial time.
2. **What value does $u$ have here?** The same value it had at the origin point (for the case $C = 0$).
3. **Where is this information going?** Follow the characteristic forward.

This is exactly the **Lagrangian frame** of §5.2: instead of standing still and watching the fluid go by (Eulerian), you ride with the fluid.

## 4.5 Three canonical 1st-order PDEs

1. **Constant-wind advection**: $\dfrac{\partial u}{\partial t} + c\dfrac{\partial u}{\partial x} = 0$ with $c$ constant. Characteristics: parallel lines $x - ct = $ const. Solution: $u(x,t) = f(x - ct)$ — the initial profile *translates* without change of shape at speed $c$.

2. **Variable-wind advection**: $\dfrac{\partial u}{\partial t} + c(x)\dfrac{\partial u}{\partial x} = 0$. Characteristics curve. For example, $c(x) = x$ gives characteristic curves $\xi = x e^{-t}$.

3. **Burgers's (nonlinear)**: $\dfrac{\partial u}{\partial t} + u\dfrac{\partial u}{\partial x} = 0$. Characteristics depend on $u$ itself, so they can *cross* — that's what causes a **shock** to form. **HW6** numerically demonstrates exactly this on a periodic domain — the smooth initial wave $1 + \sin(2\pi x)$ steepens and the discrete grid eventually develops large oscillations because of nonlinear instability via *aliasing* (we'll see why in §20).

   **The shock-formation mechanism, visually.** Where the wave is *tall* (large $u$), the characteristic line has a steep slope (fast movement). Where the wave is *short* (small $u$), the characteristic is nearly flat (slow movement). The fast lines from the peak *overtake* the slow lines from the right side. Where they meet, a **shock** forms — a vertical wall where the solution is multi-valued and the smooth assumption breaks down. **This is the mathematical mechanism behind atmospheric fronts**: warm air piles up against cold air, gradients steepen until you have a discontinuity-like front in temperature and humidity.

## 4.6 Initial and boundary conditions

- 1st-order in time → need **one** initial condition $u(x,0) = f(x)$.
- 1st-order in space → need **one** boundary condition (or periodic BCs).

**Plain-English.** "First-order" tells you how many starting/edge values you need to nail down a unique answer.

## 4.7 2nd-order PDE classification

**Why classify PDEs at all?** Before you can solve a PDE you need to know: Does it describe waves bouncing around, heat spreading out, or a static equilibrium? Can I march forward in time, or do I need to solve everything simultaneously? How many initial/boundary conditions do I need? What numerical method will work? The classification of 2nd-order PDEs answers all of these.

**What the second-derivative terms mean physically.** $\partial^2 u/\partial x^2$ measures the *curvature* of $u$ in $x$ (is the function bending up or down?). $\partial^2 u/\partial y^2$ is the curvature in $y$. The mixed term $\partial^2 u/\partial x\partial y$ is how the slope in $x$ changes as you move in $y$. The classification is essentially asking: "Which of these curvatures dominates, and how do they interact?"

For a general 2D linear 2nd-order PDE

$$A u_{xx} + B u_{xy} + C u_{yy} + \cdots = 0,$$

look at the **discriminant** $B^2 - 4AC$.

**Why does the discriminant look like the quadratic formula?** If you've ever used $b^2 - 4ac$ to solve $ax^2 + bx + c = 0$, you've seen this expression. Same role here: the discriminant tells you how many *characteristic directions* the PDE has — two real (hyperbolic), one repeated (parabolic), or none real (elliptic) — exactly analogous to the quadratic having two, one, or no real roots.

| Discriminant | Type | Example | Behavior |
|---|---|---|---|
| $B^2-4AC < 0$ | **Elliptic** | Laplace: $\nabla^2 u = F$ | No real characteristics; equilibrium / boundary problems |
| $B^2-4AC > 0$ | **Hyperbolic** | Wave: $u_{tt} - c^2 u_{xx} = 0$ | Two characteristic families; wave propagation |
| $B^2-4AC = 0$ | **Parabolic** | Diffusion: $u_t = K u_{xx}$ | One family; "forward in time"; spreads but doesn't propagate |

**Plain-English.**
- **Elliptic** — temperature on a metal plate at steady state (no time, just spatial balance).
- **Hyperbolic** — sound, gravity waves: information *propagates*.
- **Parabolic** — heat spreading, ink dispersing in water: amplitude *decays* and information *forgets the past*.

**The hallway analogy that ties all three together.** Imagine three different scenarios with people in a hallway:
- **Hyperbolic (wave):** You shout "fire!" in the middle of the hallway. The message propagates outward at a definite speed — people near you react first, then people further out. Disturbances have a clear "front" — regions ahead of the wave are still undisturbed.
- **Parabolic (diffusion):** You spray perfume in the middle of the hallway. The scent doesn't travel as a sharp front — it slowly diffuses outward, getting weaker as it spreads. Importantly, **once you've sprayed, you can never un-spray**. Information about the original concentration is irreversibly lost.
- **Elliptic (equilibrium):** The hallway has a heater at one end and an air conditioner at the other. The temperature at every point in the hallway *adjusts simultaneously* until a steady-state balance is reached. There's no "propagation" — every point feels every other point at once.

The atmosphere is mostly **hyperbolic + parabolic** (advection + diffusion). The largest class of weather problems is **hyperbolic quasi-linear PDEs**. The wind carries things (hyperbolic) and turbulence smears them (parabolic) — that's the entire game.

**Why the parabolic "irreversibility" matters numerically.** A pure parabolic equation can be integrated *forward* in time but not *backward*. Run it backward and tiny errors blow up exponentially. This is also why long climate simulations are not run as "rewinds" of past climate — they have to be initialized forward.

---

<a id="5"></a>

# 5 Math Toolkit

## 5.1 Taylor series — the workhorse of the whole course

Around a base point $x_0$, any smooth function can be written

$$f(x) = f(x_0) + f'(x_0)(x-x_0) + \frac{f''(x_0)}{2!}(x-x_0)^2 + \frac{f'''(x_0)}{3!}(x-x_0)^3 + \cdots$$

In compact form: $f(x) = \sum_{k=0}^{\infty}\dfrac{f^{(k)}(x_0)}{k!}(x-x_0)^k$.

**Plain-English.** A function is approximately a polynomial near any point. The more terms you keep, the more accurate it is. Each higher-order term is smaller (if the series converges).

**Why we care.** Replace $x$ with time $t$ and $f$ with temperature $T$:

$$T(t_2) \approx T(t_1) + T'(t_1)\,\Delta t.$$

This is exactly *finite differencing in time*: "future = present + tendency × Δt." Truncating Taylor series **is** the basis of finite-difference modeling.

**Mean Value Theorem (MVT).** There exists a point $x^*$ between $x$ and $x_0$ where $f(x) = f(x_0) + f'(x^*)(x - x_0)$ exactly. Equivalently, $f'(x^*) = (f(x) - f(x_0))/(x - x_0)$ — the *definition* of the derivative.

**Why MVT *justifies* finite differences.** The MVT says that *somewhere between any two grid points, there exists a "perfect" point where the simple slope formula gives the exact derivative — not an approximation*. The finite-difference quotient between $f(x_0)$ and $f(x_0+\Delta x)$ is therefore guaranteed to equal $f'$ at *some* interior point. That's the theoretical backbone of why finite differences work at all. The trouble is we don't know exactly *which* interior point — so when we evaluate the difference at $x_0$ (or wherever) we pick up a small error. That error is the truncation error.

**When MVT-style assumptions break.** Sharp atmospheric features — fronts, thunderstorm boundaries, coastlines — have rapidly-changing derivatives. There the "fairly smooth" assumption fails: the finite difference no longer hugs the local slope, and even small $\Delta x$ gives big errors. **This is *why* weather models struggle with frontal precipitation and coastal sea breezes** — exactly where the gradient is biggest.

## 5.2 Eulerian vs Lagrangian

- **Eulerian frame.** Stand still at a fixed point and watch the air go by. You measure $\partial T/\partial t$ — the rate of change *at that fixed point*.
- **Lagrangian frame.** Ride with an air parcel as it moves through space. You measure $dT/dt$ — the rate of change *of that specific parcel*.

The two are linked by the chain rule:

$$\frac{dT}{dt} = \frac{\partial T}{\partial t} + u\frac{\partial T}{\partial x} + v\frac{\partial T}{\partial y} + w\frac{\partial T}{\partial z} = \frac{\partial T}{\partial t} + \vec V \cdot \nabla T.$$

Rewritten:

$$\frac{\partial T}{\partial t} = \underbrace{\frac{dT}{dt}}_{\text{parcel's own change}} - \underbrace{\vec V \cdot \nabla T}_{\text{advection}}.$$

**Plain-English.** Temperature at a fixed weather station can change for two reasons: (1) the *air arriving* is colder/warmer (advection), and (2) the *parcel's own temperature is changing* (e.g., from radiation as it moves) — the Lagrangian piece. A "warm front" is mostly advection. A clear-sky parcel cooling at night is mostly Lagrangian.

**The bridge-and-kayak analogy.** Imagine a river. Standing on a bridge (Eulerian) you watch the water passing under you and record its temperature with a fixed thermometer; the temperature changes because *different parcels* of water arrive. Riding in a kayak (Lagrangian) you carry the thermometer with you; the temperature changes only because *your parcel itself* is heating up or cooling down (radiation, contact with banks, etc.). The chain rule above just relates these two readings.

**A concrete cold-front example.** Suppose at your weather station the wind is from the north at 10 m/s, and the temperature gradient is $-5\,\text{K}$ per 100 km (it gets colder northward). The air arriving has been losing heat radiatively at $\sim 0.5\,\text{K/h}$. Then:
- Advection contribution: $-\vec V\cdot\nabla T \approx -(10\,\text{m/s})(-5\,\text{K}/100\,\text{km}) = +1.8\,\text{K/h}$ → wait, sign matters: northerly wind brings *cold* air, so advection is $\sim -1.8\,\text{K/h}$.
- Lagrangian (radiative) contribution: $\sim -0.5\,\text{K/h}$.
- Eulerian (what your station thermometer reads): $\partial T/\partial t \approx -2.3\,\text{K/h}$.

This is a textbook **cold-front passage** — the station drops a few K per hour, and the dominant term is *cold advection*, not radiation. Eulerian and Lagrangian frames give different (but reconcilable) stories.

## 5.3 The "general prognostic equation"

Almost every model variable $\psi$ obeys

$$\boxed{\frac{\partial \psi}{\partial t} = -\vec V \cdot \nabla \psi + \nabla^2 (K\psi) + S}$$

**Reading this equation.** Left side: the rate at which $\psi$ changes at a fixed point in space. The three right-side terms are the three ways $\psi$ at that point can change: (1) **advection** — the wind blows in fluid from upstream that may have a different value, written $-\vec{V}\cdot\nabla\psi$ (negative because if the wind blows up a gradient, the fixed point sees the value *decrease*); (2) **diffusion** — turbulence smears gradients out, captured by the Laplacian of $K\psi$ exactly as in Chapter 0's heat-equation discussion; (3) **sources and sinks** $S$ — anything not captured by transport: heating, condensation, chemistry. Every prognostic equation in atmospheric science has these same three pieces. Once you have read this equation, every following chapter of the guide is about discretising one or another of these three terms.

where

| Symbol | Meaning |
|---|---|
| $t$ | time |
| $\vec V$ | wind vector (3D) |
| $\nabla$ | gradient operator $\partial/\partial x + \partial/\partial y + \partial/\partial z$ |
| $K$ | eddy diffusivity (units m²/s; how fast turbulence mixes things) |
| $S$ | sources and sinks (heating, evaporation, chemistry, etc.) |
| $\psi$ | any prognostic variable (the thing we're forecasting) |

The three RHS pieces are:

- **Advection** $-\vec V \cdot \nabla \psi$: transport by the wind.
- **Diffusion** $\nabla^2(K\psi)$: smoothing/spreading by turbulence.
- **Sources/sinks** $S$: production or destruction.

This is the equation we will spend most of the course discretizing.

---

<a id="6"></a>

# 6 The Atmospheric Equations and Their Approximations

## 6.1 The "primitive equations" — seven equations, seven unknowns

| Conservation law | Eqs | Unknown |
|---|---|---|
| Momentum (Newton's 2nd law in 3D) | 3 | $u, v, w$ |
| Mass continuity (air) | 1 | $\rho$ |
| Mass continuity (water) | 1 | $q$ (humidity) |
| Energy (1st law of thermodynamics) | 1 | $T$ or $\theta$ |
| Equation of state (ideal gas) | 1 | $p$ |

Seven equations in seven unknowns → solvable in principle.

## 6.2 Hydrostatic balance

The vertical force balance between the *upward* pressure gradient and *downward* gravity:

$$\boxed{\frac{dp}{dz} = -\rho g}$$

**Reading this equation.** The left side is the *vertical pressure gradient* — how rapidly pressure changes as you move up. The right side is *minus density times gravity* — the weight of a unit volume of air, with a minus sign because $z$ points up but weight points down. The equation says: at every altitude, the pressure must drop just fast enough so that the upward pressure-gradient force exactly balances the downward pull of gravity on every chunk of air. Whenever this equation is *not* satisfied — even by a fraction of a percent — the residual force drives a vertical acceleration. *That tiny residual is what powers every cumulus cloud you have ever seen.*

The minus sign is because pressure *decreases* with altitude. A scale analysis shows the vertical pressure gradient is **~10,000× larger** than the horizontal one — yet gravity almost exactly cancels it. The tiny residual is what drives most vertical motion.

**Real-life weather example.** The pressure gradient force on a parcel pointed *upward* is ~976 cm/s² and gravity is ~980 cm/s². **Four decimal places of cancellation.** Even slight changes in air density (a warm bubble of, say, 0.5% lower density) tip the balance, the residual force is upward, and the parcel rises as a thermal. That thermal hits the LCL, condenses water, and a cumulus cloud is born. *Every fair-weather cumulus you've ever seen is a tiny imbalance of two huge forces.*

## 6.3 The Boussinesq approximation

For shallow layers (e.g., the planetary boundary layer):

$$\rho(x,y,z,t) = \rho_0(z) + \rho'(x,y,z,t),\qquad p = p_0(z) + p'(x,y,z,t)$$

A *reference state* ($\rho_0$, $p_0$) varies only with height and is in hydrostatic balance. A *perturbation* ($\rho'$, $p'$) is small and varies in space and time. The approximation says: **use $\rho_0$ everywhere except in the buoyancy term** (the term containing $g$). The buoyancy is then proportional to a *temperature* perturbation, not a density perturbation, via $\rho'/\rho \approx -\theta'/\theta$.

**Why bother.** It dramatically simplifies the equations while still capturing buoyancy. It's appropriate when density changes are small (e.g., a sea breeze at low altitudes), but breaks down for deep, compressible flow.

**The Boussinesq decision rule.** When you write the momentum and continuity equations:
- *Everywhere except the buoyancy term* → replace $\rho$ with $\rho_0$ (the constant reference). The error is ~0.5%, negligible.
- *Inside the buoyancy term* (the $\rho g$ piece in the vertical momentum equation) → keep $\rho'$ — that tiny perturbation is what *drives* the vertical motion. Drop it and you've turned off buoyancy entirely.

The closure relation $\rho'/\rho_0 \approx -\theta'/\theta_0$ tells you that **a parcel warmer than its surroundings is also less dense**, so you can replace density perturbations with temperature perturbations everywhere. That's the computational key.

## 6.4 Potential temperature $\theta$

A real air parcel's temperature changes when it rises (it expands and cools adiabatically). To make a *conserved* quantity for adiabatic motion, define **the temperature the parcel would have if you brought it adiabatically to 1000 mb**:

$$\boxed{\theta = T \left(\frac{p_0}{p}\right)^{R_d/c_{pd}}}$$

with $p_0 = 1000\text{ mb}$, $R_d$ the gas constant for dry air, $c_{pd}$ specific heat at constant pressure for dry air. It is conserved for dry adiabatic motion.

**Plain-English: same adiabat = same air mass.** Two parcels at different altitudes have different $T$ but might have the *same* $\theta$ — meaning they came from the same air mass via adiabatic motion. Meteorologists call lines of constant $\theta$ **dry adiabats**. If $\theta$ *increases* with height (stable atmosphere) a displaced parcel is restored toward its original level — gravity waves. If $\theta$ *decreases* with height (unstable) a displaced parcel keeps going — convection. *The vertical profile of $\theta$ is the single most useful diagnostic for atmospheric stability.*

**Quick mental check.** A parcel at the surface with $T = 300$ K, $p = 1000$ mb has $\theta = 300$ K (same as $T$, by construction). Lifted adiabatically to 500 mb, its $T$ drops to ~246 K, but its $\theta$ stays at 300 K. So the "$\theta = 300$ K surface" snakes through the atmosphere wherever this parcel goes — and you can track it from a satellite or radiosonde sounding.

## 6.5 The Exner function (non-dimensional pressure)

$$\pi = \left(\frac{p}{p_0}\right)^{R_d/c_{pd}},\qquad T = \theta\,\pi.$$

Reworking the hydrostatic equation:

$$\frac{d\pi}{dz} = -\frac{g}{c_{pd}\,\theta_v}, \qquad \theta_v = \theta(1 + 0.61\,q_v).$$

$\theta_v$ = **virtual potential temperature** (corrects for water vapor making air less dense). The Exner formulation simplifies how you handle compressibility numerically — it decouples pressure and density and makes solvers more efficient.

## 6.6 Continuity equation (mass conservation)

Lagrangian form: $\dfrac{d\rho}{dt} + \rho\,\nabla\cdot\vec V = 0$.

**Plain-English.** If the velocity field is *converging* on a parcel (more air arrives than leaves), the parcel is squeezed and its density rises. If the velocity field is *diverging* (more leaves than arrives), the parcel expands and density falls. This is exactly what makes air **compressible**. Think of squeezing a balloon: you compress the air inside and the density rises. The atmosphere does the same locally wherever winds converge.

## 6.7 Anelastic approximation

If we let $\rho$ vary with height but **not change locally** ($\partial\rho/\partial t = 0$), the continuity equation becomes

$$\nabla \cdot (\rho_0 \vec V) = 0.$$

Crucially, **this filters out acoustic (sound) waves**, which are what tripped up Richardson in 1922. We'll come back to this in §8.

**Why this works in plain English.** Sound waves are *compression waves* — they require local oscillation of density ($\partial \rho/\partial t \neq 0$). By forcing $\partial \rho/\partial t = 0$, we remove the very mechanism sound waves need to exist. They simply have nowhere to go. Density can still vary with height (the atmosphere thins with altitude — that's $\rho_0(z)$), but it can't oscillate locally. Best of all, this approximation is **valid for deep circulations** (entire troposphere) — unlike the stricter incompressible assumption $\nabla\cdot\vec V = 0$ which only works for shallow flows.

**Alternative: time splitting.** Modern fully compressible models (WRF) keep the full sound-supporting equations but use a *time-splitting* trick — large time steps for slow weather modes, tiny sub-steps for the fast acoustic modes (with a damping term). More flexible than anelastic but more complex to code. Both approaches solve the same underlying problem: keep sound waves from forcing tiny time steps everywhere.

## 6.8 Scalar transport (advection–diffusion)

For any scalar (concentration $c$, temperature, moisture):

$$\underbrace{\frac{\partial c}{\partial t} + u\frac{\partial c}{\partial x} + v\frac{\partial c}{\partial y} + w\frac{\partial c}{\partial z}}_{\text{advection}} - \underbrace{\frac{\partial}{\partial x_j}\left(\kappa_e\frac{\partial c}{\partial x_j}\right)}_{\text{diffusion}} = S.$$

**Reading this equation.** The underbraced "advection" piece is just the chain-rule expansion of $\vec{V}\cdot\nabla c$ from Chapter 0 — each component of the wind times the gradient of $c$ in that direction. The "diffusion" piece is the flux-divergence form of the Laplacian (also discussed in Chapter 0), using Einstein's summation convention where the repeated subscript $j$ implies a sum over $x, y, z$. So in plain English: a parcel's concentration changes because (1) the wind is bringing in different stuff, (2) turbulence is smoothing gradients, and (3) sources or sinks are creating or destroying material. This is the *same* three-term structure as the general prognostic equation in Section 5.3 — only the variable name has changed.

$\kappa_e$ is the **eddy diffusivity** — turbulence is so much faster than molecular diffusion in the atmosphere that we replace molecular $\kappa$ with a much larger eddy $\kappa_e$.

---

<a id="7"></a>

# 7 The Waves Inside the Equations

The Euler equations support several wave types — to know which ones matter, we **linearize** with a perturbation expansion (mean + small fluctuation).

**The model-builder's mindset (guitar string analogy).** If you want to understand how a guitar string vibrates, you don't start with a full 3D simulation of the wood, the air, the room acoustics, and the musician's fingers. You start with an idealized string under tension. Once you understand that, you add complexity back piece by piece. The Euler equations are exactly that idealization for the atmosphere — a dry, frictionless, non-rotating fluid — chosen so we can isolate the *waves* from everything else.

**Two phenomena, fundamentally different.** Air motion contains two kinds of behavior:
- **Advection** — a leaf carried downstream by a current. Stuff travels *with* the flow, *only downstream*.
- **Waves** — a stone dropped in a pond produces ripples that spread *outward in all directions* regardless of any underlying current. Waves carry information and energy independently of where the bulk fluid is going.
The Euler equations support *both*. The next chapters disentangle the wave part.

## 7.1 The perturbation method

Split each variable into mean + perturbation: $a = \bar a + a'$.

- Linear terms in $a'$ → keep them.
- Products $a' b'$ → if we drop them, we are *linearizing*.
- Time-averaged products $\overline{a'b'}$ are *not* zero — these are **turbulent fluxes** (eddy heat flux $\overline{w'\theta'}$, eddy momentum flux $\overline{u'w'}$, etc.).

**Plain-English.** Wind isn't steady — it has a mean and fluctuations. Add a turbulence-shaped jiggle on top of a mean breeze. The product of two jiggles, averaged, is *not* zero — that's how eddies transport heat upward even when the mean vertical velocity is zero.

## 7.2 The spectral gap

If you Fourier-decompose wind speed at a point, you find peaks at large scales (~days) and small scales (~seconds), with a *gap* at intermediate scales (~tens of minutes). This gap **lets us separate "mean" and "turbulent" cleanly.** Most NWP models choose grid spacing inside this gap: large scales are *resolved*, small scales are *parameterized*.

## 7.3 Sound (acoustic) waves

Picture a horizontal sound wave (propagating in $x$). It's longitudinal — air parcels move parallel to the wave. From the linearized equations, the wave equation for pressure perturbation $p'$ is

$$\left(\frac{\partial p'}{\partial t} + \bar u\frac{\partial p'}{\partial x}\right)^2 - \frac{\gamma\bar p}{\bar\rho}\frac{\partial^2 p'}{\partial x^2} = 0,\qquad \gamma = c_{pd}/c_{vd}.$$

Plug in the wave ansatz $p' = A e^{ik(x - ct)}$ (a plane wave with amplitude $A$, wavenumber $k = 2\pi/L_x$, phase speed $c$). You get the **dispersion relation**

$$\boxed{c = \bar u \pm (\gamma R_d \bar T)^{1/2}}.$$

For $\bar T = 300$ K, $c \approx 350$ m/s. The $\pm$ means sound goes both upstream and downstream. The **Doppler effect** is the extra $\bar u$.

**Plain-English.** Sound waves exist *because* the atmosphere is compressible. When you push air, neighbors don't get out of the way infinitely fast. They compress. Sound waves are **longitudinal**: the air parcels oscillate *parallel* to the wave's direction of travel — exactly like a slinky being pushed.

**Why we don't care, but care a lot.** Sound waves carry essentially no useful weather information — they don't move heat or moisture or do anything meteorologists would notice. But they travel at ~350 m/s, which is **10–30× faster** than typical weather speeds (10–30 m/s). Through the CFL condition (§13), this fastest mode forces *every* time step in the model to be tiny — even though we don't care about sound at all. That's why filtering sound waves (§8) saves enormous computation.

## 7.4 Gravity (buoyancy) waves

**The mass-on-a-spring picture.** Take an air parcel and displace it upward in a stable atmosphere. Step by step:
1. The parcel rises into lower pressure.
2. It expands adiabatically.
3. It cools at the dry-adiabatic lapse rate (~9.8 K/km).
4. The environment at that height is *warmer* than the parcel (because the atmosphere is stably stratified).
5. The parcel is now denser than its surroundings → gravity pulls it back down.
6. It overshoots its original level, gets compressed and warmed, becomes less dense → buoyancy pushes it back up.
7. **It oscillates up and down like a pendulum.**

The natural frequency of this oscillation is the **Brunt–Väisälä frequency** $N$. The atmosphere's stability $d\bar\theta/dz$ acts like the *spring constant* — the more stable, the faster the bobbing.

**Stadium-wave analogy for transverse propagation.** Each parcel oscillates *vertically* (up–down), but the wave pattern propagates *horizontally* across the atmosphere. Think of a stadium wave — each person stands up and sits down (vertical motion), but the wave sweeps sideways around the stadium. Gravity waves are **transverse**: particle motion is *perpendicular* to wave propagation.

**Three regimes of $N^2$.** The sign of $N^2 = g\,d\ln\bar\theta/dz$ tells you the atmospheric regime:
- $N^2 > 0$ (stable, $\bar\theta$ increases with height): displaced parcels oscillate → gravity waves exist.
- $N^2 = 0$ (neutral): no restoring force → parcel sits where you put it.
- $N^2 < 0$ (unstable, $\bar\theta$ decreases with height): the "frequency" is imaginary — small displacements **grow exponentially** → convection, thunderstorms.
*One number, $N^2$, tells you whether you're in a wave-supporting atmosphere or a thunderstorm-spawning one.*

**Real-world example: lenticular ("UFO") clouds.** When stable air flows over a mountain, the parcels are pushed up, oscillate, and hover at the crests of the resulting stationary mountain gravity waves. Moisture condenses at those crests → smooth, stationary, lens-shaped clouds. Pilots and skiers see them all the time. They're the most photogenic possible proof that gravity waves are real.

These are the oscillations of an air parcel pushed up in stable air. They're transverse — air moves vertically, the wave moves horizontally. The linearized incompressible equations give the wave equation

$$\frac{\partial^2}{\partial t^2}\left(w'_{xx} + w'_{zz}\right) + N^2 w'_{xx} = 0,$$

where the **Brunt–Väisälä buoyancy frequency** is

$$\boxed{N \equiv \left(g\frac{d\ln\bar\theta}{dz}\right)^{1/2}}.$$

$N$ measures how strongly stratified (stable) the atmosphere is. A parcel pushed up rises, becomes denser than its surroundings, falls back, overshoots, and oscillates at frequency $N$ if there is no dissipation — like a pendulum.

The **dispersion relation** for plane-wave solutions $w' = A e^{i(kx + mz - \omega t)}$ is

$$\omega = \pm \frac{Nk}{(k^2 + m^2)^{1/2}},\qquad c_x = \bar u \pm \frac{N}{(k^2+m^2)^{1/2}}.$$

For tropospheric values $N \approx 0.01\text{ s}^{-1}$ and $L_x \sim 10$ km, $c_x \sim 15$ m/s.

**Plain-English example.** When stable air flows over a mountain, the pushed-up parcels oscillate — that's why you sometimes see lenticular ("UFO") clouds downwind from mountains: they sit at the crests of stationary mountain gravity waves. Mountain waves are 100–500 km horizontally, can reach the stratosphere, and break (turbulence) when they get high enough.

## 7.5 Rossby waves

**The β-effect mechanism in plain English.** The Coriolis parameter $f$ increases with latitude (it's $2\Omega\sin\phi$). $\beta = df/dy$ is *how fast* it increases. Now imagine an air parcel:
- Pushed *northward* → $f$ increases → conservation of vorticity forces the parcel's relative vorticity to *decrease* → it curves back south.
- Pushed *southward* → $f$ decreases → relative vorticity must *increase* → it curves back north.

The result: meridional oscillations that propagate westward — **Rossby waves**. The β-effect is the spring; the planetary vorticity gradient is the restoring force.

Including the latitudinal variation of the Coriolis parameter $f$ (the **planetary vorticity gradient** $\beta = df/dy$) gives a third wave class — **Rossby waves**, with horizontal scales of 4,000–6,000 km (3–6 wavelengths around the globe). Their phase speed:

$$\boxed{c = \bar u - \frac{\beta}{k^2}}.$$

These are the meandering jet-stream patterns you see on a 500 mb map — troughs and ridges. They're tied to weather (cyclones) and last 1–6 weeks. With $\bar u \sim 15$ m/s and 3 troughs, the wave is roughly stationary; faster $\bar u$ makes it propagate east.

**Real-weather connection.** Every time you see a 500 mb map with troughs and ridges meandering across the country, you're looking at Rossby waves. They're the dominant wave pattern of the large-scale atmosphere — *the* fundamental weather-making waves. When a Rossby trough deepens, mid-latitude cyclones develop on its eastern flank. When two Rossby ridges block, you get heat domes. These waves are why winter doesn't sit forever in one place — they redistribute heat from equator to pole over 1–6-week cycles.

## 7.6 Why this matters for modeling

| Wave | Speed | Why we care |
|---|---|---|
| Sound | ~350 m/s | Fastest mode → forces tiny $\Delta t$ via CFL → must be filtered |
| Gravity | ~15 m/s | Real weather (mountain waves, fronts), *do not* filter |
| Rossby | ~10 m/s | Synoptic patterns, *do not* filter |

**Sound is fast and physically irrelevant for weather → we filter it.** Gravity and Rossby waves carry actual weather and energy → we keep them.

---

<a id="8"></a>

# 8 Filtering Sound Waves

## 8.1 Method 1 — Incompressible

Set $d\rho/dt = 0$. The continuity equation collapses to $\nabla\cdot\vec V = 0$. This kills sound waves entirely.

**Three conditions for incompressibility to be valid**:
1. $u^2 \ll c_s^2$ (flow speed much less than sound speed). Easy: typical winds 10 m/s vs. sound 350 m/s.
2. Time scale ≫ acoustic propagation time across the domain. Easy.
3. $L_z \ll H_z$ (vertical scale ≪ atmospheric scale height ≈ 8 km). **NOT satisfied** for deep flows like sea-breezes, mountain waves, deep convection — these all have $L_z$ comparable to $H_z$.

So incompressibility is too restrictive: it only works for very shallow circulations (e.g., the bottom 100 m of the PBL). For real weather we need the *anelastic* compromise.

**Computational impact, by the numbers.** For a 10 km grid, the CFL bound from sound is $\Delta t \leq \Delta x/c_s = 10\,\text{km}/350\,\text{m/s} \approx 29$ s. From gravity waves it's $\Delta t \leq \Delta x/c_g = 10\,\text{km}/15\,\text{m/s} \approx 670$ s. **A factor of ~23 in time-step length** — meaning 23× more computation if you keep sound waves. Every minute of CPU saved by filtering acoustics translates to faster forecasts.

## 8.2 Method 2 — Anelastic

Allow $\rho$ to vary with height but not with time: $\partial\rho/\partial t = 0$. Continuity becomes

$$\boxed{\nabla\cdot(\rho_0\vec V) = 0.}$$

This kills sound waves *without* requiring shallow flow. Used heavily in modern atmospheric models.

**Why this is an elegant compromise.** Sound waves require *local* compression ($\partial \rho/\partial t \neq 0$). By forcing $\partial \rho/\partial t = 0$, you remove the very mechanism sound needs. But you *keep* the realistic vertical density variation $\rho_0(z)$ — the air thins with altitude, exactly as observed. So you can model deep tropospheric circulations (mountain waves, hurricanes, jet streams) accurately without paying the time-step cost of acoustic CFL. Best of both worlds.

## 8.3 Method 3 — Tricks on the time integration

- **Time splitting.** Integrate sound waves with a different (e.g., implicit) scheme that damps them.
- **Slow them down artificially.** Common; sacrifices physics for stability.
- **Speed them up.** Less common.

In modern fully compressible models (WRF), sound waves are *kept* but treated with a sub-stepped semi-implicit scheme so they don't kill stability.

---

<a id="9"></a>

# 9 Finite Differences — How a Computer Approximates a Derivative

## 9.1 The basic premise

A derivative is

$$\frac{df}{dx}(x_0) = \lim_{\Delta x\to 0}\frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x}.$$

A computer cannot take limits, so it uses *finite* $\Delta x$:

**The broken-speedometer analogy.** Suppose your speedometer is broken. You can still estimate your speed by noting your position at two different times and dividing the position change by the time interval. *That's a finite difference.* You're replacing the *instantaneous* rate of change (derivative) with an *average* rate of change over a small interval. The smaller the interval, the closer you get to your true speed at the start of the interval — but you can never reach it exactly with a finite gap.

**Why centered is inherently better.** The forward and backward differences are *one-sided*: they look in only one direction from $x_0$. The centered difference *straddles* $x_0$ symmetrically — it looks both directions. By symmetry, all the odd-order Taylor errors cancel, leaving only even-order terms. That's why centered is 2nd-order accurate while one-sided is only 1st-order.

| Scheme | Formula | Order of accuracy |
|---|---|---|
| Forward (right) | $\frac{f(x_0+\Delta x) - f(x_0)}{\Delta x}$ | 1st |
| Backward (left) | $\frac{f(x_0) - f(x_0-\Delta x)}{\Delta x}$ | 1st |
| Centered | $\frac{f(x_0+\Delta x) - f(x_0-\Delta x)}{2\Delta x}$ | 2nd |

These are *not equivalent* for finite $\Delta x$. They differ in accuracy and in stability when used in a time-stepping scheme.

## 9.2 The grid

Atmospheric models lay down a 3D grid: $x_i = i\Delta x$, $y_j = j\Delta y$, $z_k = k\Delta z$. We store variables at grid points and compute derivatives by differencing neighbors. The function values between grid points are *unknown* to the computer; the grid is the world.

## 9.3 Pros and cons of grid-point vs. spectral

| Representation | Stored | Pros | Cons |
|---|---|---|---|
| Grid points | Values $f_i$ | Simple, local stencils | Lower accuracy unless very fine |
| Spectral (series) | Coefficients $a_k$ | Very high accuracy for smooth fields | Global; bad with shocks/boundaries |

WRF uses grid points (finite differences); ECMWF historically used spectral (now hybrid).

---

<a id="10"></a>

# 10 The Four Properties of a Numerical Scheme

Every finite-difference scheme should be evaluated on:

1. **Accuracy** — how close is the FD approximation to the derivative for finite $\Delta x$?
2. **Consistency** — as $\Delta x, \Delta t \to 0$, does the scheme reduce to the original PDE?
3. **Stability** — does the numerical solution stay bounded over many steps?
4. **Convergence** — does it actually approach the true answer as $\Delta x, \Delta t \to 0$?

The **Lax Equivalence Theorem** ties them together for linear PDEs:

$$\boxed{\text{Consistency} + \text{Stability} \iff \text{Convergence}}.$$

## 10.1 Accuracy and the order of a scheme

Apply Taylor:

$$f(x_0 + \Delta x) = f(x_0) + \Delta x\,f'(x_0) + \frac{(\Delta x)^2}{2!}f''(x_0) + \cdots$$

So

$$\frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x} = f'(x_0) + \underbrace{\frac{\Delta x}{2}f''(x_0) + \cdots}_{\text{truncation error}}$$

The lowest power of $\Delta x$ in the leftover (here $\Delta x^1$) is the **order of accuracy**. The forward scheme is **first-order**: halving $\Delta x$ halves the error.

A centered difference cancels the $\Delta x$ term and leaves $\Delta x^2$ — **second-order**.

**Bang for your buck.** Halving $\Delta x$ improves accuracy:
- 1st-order scheme → 2× better
- 2nd-order scheme → 4× better
- 3rd-order scheme → 8× better
- 4th-order scheme → 16× better

This is *why* higher-order is worth caring about — the payoff per grid-point investment grows fast. But there's a catch: each higher order needs a wider stencil (more neighboring points), which makes boundary handling and parallelism harder. So the practical sweet spot is usually 2nd–4th order spatial.

## 10.2 Truncation error of an entire scheme — the upstream example

Apply forward time + upstream space to advection $u_t + c u_x = 0$:

$$\frac{u_j^{n+1} - u_j^n}{\Delta t} + c\,\frac{u_j^n - u_{j-1}^n}{\Delta x} = 0.$$

After Taylor-expanding both differences and using the PDE itself to swap second time derivatives for second space derivatives, you find

$$u_t + c u_x = \underbrace{\frac{c\Delta x}{2}\!\left(1 - \frac{c\Delta t}{\Delta x}\right) u_{xx}}_{\text{numerical diffusion}} + O[(\Delta t)^2, (\Delta x)^2].$$

**The leading error is a diffusion term** — the upstream scheme secretly diffuses the solution. That's why upstream wave fronts smear out: it's not a bug in the implementation; it's the scheme. **HW1** numerically demonstrates exactly this on the rotating-cone test: after one revolution the cone peak has dropped from 1.000 to 0.842; after three revolutions, to 0.659. The shape is also slightly broadened — pure numerical diffusion.

## 10.3 Consistency

A scheme is **consistent** if its truncation error vanishes as $\Delta t, \Delta x \to 0$. Almost all reasonable schemes are consistent — but check anyway. (The leapfrog applied to a parabolic equation is *consistent* but not stable, by the way.)

**The recipe-and-oven analogy.** Consistency is like checking that you have the correct recipe for a cake. Stability is like checking that the oven actually cooks the cake without burning it. *Even with a perfect recipe, an unstable oven ruins the cake.* And conversely, a perfectly working oven won't help if your recipe is for a different dish. **Lax says: you need both.**

## 10.4 Convergence

If consistent + stable → converges. We will spend most of the next chapters on **stability**, because that's the hard one.

---

<a id="11"></a>

# 11 Stability I — The Energy Method

## 11.1 What does "stable" mean?

Let $\phi^n_j$ be the numerical solution at time $n\Delta t$ and space $j\Delta x$. We want, for some norm $\|\cdot\|$ and some constant $C_T$ that doesn't depend on $\Delta x$ or $\Delta t$:

$$\boxed{\|\phi^n\| \leq C_T \|\phi^0\|\quad\text{for all } n\Delta t \leq T.}$$

The numerical solution doesn't grow faster than a fixed multiple of the initial data. (The true solution may grow — e.g., an unstable atmosphere — but the *numerical* solution must not grow *faster* than physics allows.)

Two common norms:

- **Maximum (∞) norm**: $\|\phi\|_\infty = \max_j |\phi_j|$.
- **Euclidean ($\ell_2$) norm**: $\|\phi\|_2 = \big(\sum_j |\phi_j|^2 \Delta x\big)^{1/2}$. This is energy-like — when each $\phi_j$ is a velocity, $\|\phi\|_2^2$ is proportional to total kinetic energy.

**Why $\ell_2$ is "energy-like."** When each $\phi_j$ represents a velocity, $\|\phi\|_2^2 = \sum_j \phi_j^2 \Delta x$ is *literally* proportional to the total kinetic energy of the discrete system (mass per cell times velocity squared). That's why this norm is called the **energy method** — you're tracking a quantity that, in the right physical interpretation, *is* energy. If energy can't grow, the scheme can't blow up.

## 11.2 The energy method for the upstream scheme

**The plain-English summary.** The energy method has a one-line recipe: *track the total "energy" $\sum_j \phi_j^2$ from one time step to the next, and prove it never grows.* If you succeed, your scheme is stable; if you fail, you've found an instability.

Define $\mu = c\Delta t/\Delta x$ (the **CFL number / Courant number**). The upstream update is

$$\phi_j^{n+1} = (1-\mu)\phi_j^n + \mu\phi_{j-1}^n.$$

Square both sides, sum over all $j$, and use periodic BCs to swap $\sum_j(\phi_{j-1})^2 = \sum_j(\phi_j)^2$:

$$\sum_j(\phi_j^{n+1})^2 = \sum_j (\phi_j^n)^2 - 2\mu(1-\mu)\sum_j\!\big[(\phi_j^n)^2 - \phi_j^n\phi_{j-1}^n\big].$$

Apply Schwarz's inequality to bound $\sum_j\phi_j^n\phi_{j-1}^n \leq \sum_j(\phi_j^n)^2$. The result:

$$\sum_j(\phi_j^{n+1})^2 \leq \big[(1-\mu)^2 + 2\mu(1-\mu) + \mu^2\big]\sum_j(\phi_j^n)^2 = \sum_j(\phi_j^n)^2,$$

provided **$\mu(1-\mu) \geq 0$**, i.e.,

$$\boxed{0 \leq \frac{c\,\Delta t}{\Delta x} \leq 1.}$$

This is the **CFL stability condition** for upstream. It says: *don't take a time step so large that the wave moves more than one grid box per step.*

## 11.3 What this tells us

- If the scheme is stable, total "energy" $\sum_j\phi_j^2$ decreases or stays the same — never grows.
- The maximum allowed $\Delta t$ scales with $\Delta x/c$ — finer resolution ⇒ smaller time step.
- If you want to halve $\Delta x$ for better accuracy, you must also halve $\Delta t$ — so the cost of the simulation goes up by **4×** (in 1D) or **16×** (in 3D + time).

**HW1** confirms this numerically: with FTCS (forward time + centered space) at $\mu = 0.5$, *the simulation blows up at step 113*. CFL is necessary but not sufficient — FTCS is unconditionally unstable for advection regardless of $\mu$.

**Drawback of the energy method.** Each new problem requires *fresh creativity* to define an appropriate energy and prove a bound on it. There's no universal recipe — you have to spot the right combination of squared variables, manipulate it, and apply Schwarz at the right moment. That creativity-on-demand is exactly why von Neumann's method (next chapter) became the default workhorse: it's *mechanical*. Plug in a Fourier mode, crank, get the answer.

---

<a id="12"></a>

# 12 Stability II — Von Neumann (Fourier) Analysis

## 12.1 The idea

**The musical-chord analogy.** Think of the numerical solution as a musical chord — a superposition of "notes" (Fourier modes) of different frequencies. Each note evolves independently in a *linear* scheme (because of superposition). Von Neumann asks: **does each individual note grow or decay after one time step?** If even one note grows without bound, the chord eventually screams. If all notes are bounded, the chord stays musical (stable).

This is also why von Neumann is *mechanical* compared to the energy method: there's no creativity required, just a plug-and-crank substitution.

Decompose the numerical solution into Fourier modes:

$$\phi_j^n = \sum_k a_k^n e^{ikj\Delta x}.$$

Each mode evolves independently:

$$a_k^{n+1} = A_k\, a_k^n,$$

so

$$a_k^n = (A_k)^n a_k^0.$$

$A_k$ is the **amplification factor** for wavenumber $k$. The solution is bounded iff $|A_k| \leq 1$ for **every** $k$. This is the **von Neumann stability condition**.

**Reading these equations.** The first line says any grid-cell value $\phi_j^n$ is built up as a sum of Fourier modes $e^{ikj\Delta x}$, each carrying a coefficient $a_k^n$ that depends on time. The second line says: in a *linear* scheme, every Fourier mode evolves on its own — multiplied each step by some complex number $A_k$ that depends only on wavenumber. The third line just iterates that fact: after $n$ steps, the coefficient is the initial coefficient times $A_k^n$. So if $|A_k| > 1$ even for one wavenumber $k$, that mode grows exponentially and the whole numerical solution eventually explodes — even if every other mode is well-behaved.

## 12.2 Upstream scheme by von Neumann

Substitute $\phi_j^n = a_k^n e^{ikj\Delta x}$ into the upstream update:

$$A_k = 1 - \mu + \mu e^{-ik\Delta x},$$
$$|A_k|^2 = 1 - 2\mu(1-\mu)(1 - \cos k\Delta x).$$

This requires $\mu(1-\mu) \geq 0$, i.e., $0 \leq \mu \leq 1$ — same as the energy method.

**Reading these equations.** The first line is the amplification factor itself — a complex number that mixes a real piece $1 - \mu$ with a phase-rotated piece $\mu e^{-ik\Delta x}$. The phase-rotation $e^{-ik\Delta x}$ comes from the upstream stencil (the neighbour at $j-1$ is one grid cell behind, hence the negative phase). The second line is just $A_k$ multiplied by its conjugate — a real, non-negative number that measures *per-step amplitude growth*. The factor $(1 - \cos k\Delta x)$ vanishes for very long waves ($k\Delta x \to 0$) and is largest at the worst-case $2\Delta x$ wave ($k\Delta x = \pi$). So the equation says: short waves are always handled most aggressively, and the scheme is stable only when $\mu$ stays inside the unit interval $[0, 1]$ — precisely the CFL bound.

## 12.3 What the modulus tells you

$$|A_k|^2 = 1 - 2\mu(1-\mu)(1 - \cos k\Delta x).$$

- **Worst-case wavelength.** The shortest resolvable wave has $L_x = 2\Delta x$, so $k\Delta x = \pi$, $\cos k\Delta x = -1$, and $|A_k|^2 = 1 - 4\mu(1-\mu)$. Plug $\mu > 1$ → blows up fastest there.
- **At $\mu=1$**: $|A_k|=1$ for all $k$ — no amplitude error (perfect transport, but only for this specific $\mu$).
- **For $\mu < 1$**: $|A_k| < 1$ — solution decays (numerical diffusion).
- **For $\mu > 1$**: every mode amplifies — instability.

**The shortest waves are *always* handled worst.** The lesson: *resolve features by at least 8–10 grid points.*

## 12.4 The combined FTCS scheme — a cautionary tale

Forward time + centered space for advection:

$$\frac{\phi_j^{n+1} - \phi_j^n}{\Delta t} + c\frac{\phi_{j+1}^n - \phi_{j-1}^n}{2\Delta x} = 0.$$

Solving for $\phi_j^{n+1}$:

$$\phi_j^{n+1} = \phi_j^n - \frac{\mu}{2}\big(\phi_{j+1}^n - \phi_{j-1}^n\big),\qquad \mu = c\Delta t/\Delta x.$$

Plug in the Fourier mode $\phi_j^n = a_k^n e^{ikj\Delta x}$. Use $e^{ik\Delta x} - e^{-ik\Delta x} = 2i\sin(k\Delta x)$:

$$A_k = 1 - \frac{\mu}{2}\big(e^{ik\Delta x} - e^{-ik\Delta x}\big) = 1 - i\mu\sin(k\Delta x).$$

So

$$|A_k|^2 = 1 + \mu^2\sin^2(k\Delta x) \geq 1\quad\text{for all } k.$$

**FTCS is unconditionally unstable for pure advection.** No choice of $\Delta t$ saves it. The peak occurs at $k\Delta x = \pi/2$, where $\sin = 1$ and $|A_k|^2 = 1 + \mu^2$:

- $\mu = 0.25$ → peak $|A_k| = \sqrt{1.0625} = 1.031$ (3% growth per step → $\sim 20\times$ in 100 steps).
- $\mu = 0.5$ → peak $|A_k| = \sqrt{1.25} = 1.118$.
- $\mu = 1.0$ → peak $|A_k| = \sqrt{2} = 1.414$.
- $\mu = 2.0$ → peak $|A_k| = \sqrt{5} = 2.236$.

**HW4** plots exactly these curves and confirms every one lies above the dashed $|A_k| = 1$ stability line.

**Why does FTCS fail when its parts each look benign?**
- Forward time alone has $|A| > 1$ for any oscillation (Euler is unconditionally unstable for the oscillation equation, §14).
- Centered space alone has $|A| = 1$ for any wavenumber (no amplitude error, just dispersion).
- Combine "amplifying time × neutral space" → still amplifying.

**HW1** confirms the practical consequence: FTCS on the rotating cone blows up at step 113 with $\mu = 0.5$. The cone is replaced by oscillations of amplitude ~10.

**The deeper lesson.** $\mu = 0.25$ satisfies CFL ($\mu \leq 1$). FTCS still blows up. **CFL is necessary but not sufficient — you must analyze the *combined* scheme with von Neumann.**

## 12.5 The general criterion

For PDEs whose true solution can grow at rate $\gamma$, the criterion relaxes to $|A_k| \leq 1 + \gamma\Delta t$. For all the problems in this course (waves), the true solution is neutral, so we use the strict $|A_k| \leq 1$.

---

<a id="13"></a>

# 13 The CFL Condition — Physical Interpretation

The mathematical CFL condition $|c|\Delta t \leq \Delta x$ has a **physical** meaning that goes beyond Fourier analysis.

**Historical note.** Courant, Friedrichs, and Lewy in 1928 — long before electronic computers — published their stability paper while trying to *prove the existence of solutions to PDEs* using finite differences as a theoretical tool. They had no idea their result would become the operational constraint for every weather model on earth. The CFL condition emerged from pure mathematics decades before it had a practical home.

**CFL as a sampling-rate condition.** Define the sampling rate $s = \Delta x/(c\Delta t) = 1/\mu$:
- $s = 1$: the wave moves *exactly* one grid point per time step (the "magic CFL").
- $s = 2$: the wave moves half a grid point per step — sampled twice per cell.
- $s < 1$ ($\mu > 1$): the wave skips over grid points each step — the scheme literally cannot see where the wave is. Instability.

Just like with audio: if you sample too slowly, you can't reconstruct the signal. The CFL condition is a Nyquist-style requirement in disguise.

**Caveat:** taking $\Delta t$ extremely small does *not* automatically give better answers. Stability depends on the **ratio** $\mu$, not on $\Delta t$ alone. And accuracy doesn't care about $\Delta t$ once it's already much smaller than $\Delta x/c$ — the spatial errors will dominate.

## 13.1 Domain of dependence

For a hyperbolic PDE, the true solution at point $(x, t)$ is determined by initial data along the **characteristic** that passes through $(x, t)$. The characteristic for advection has slope $1/c$ in the $(x, t)$ plane.

A finite-difference scheme has a **numerical stencil** — a set of past grid points it uses to compute the future. The stencil defines a **numerical domain of dependence**.

**CFL says:** *the true characteristic must fall inside the numerical stencil.* Otherwise, the scheme has no information about where the solution is actually coming from, and instability follows.

Geometrically, $c\Delta t \leq \Delta x$: the wave travels less than one grid box per time step.

## 13.2 What CFL does *not* guarantee

- CFL is **necessary** but **not sufficient**. FTCS satisfies CFL for $\mu < 1$ yet is still unconditionally unstable (HW1 / HW4).
- For **higher-order** schemes the stencil is wider — more $\Delta x$ to spare, but also more places for instability to hide.

## 13.3 Practical lesson

When the wind is fast (jet stream, ~100 m/s) and the grid is fine (1 km), the time step must be tiny (~10 s). This is why high-resolution NWP is so expensive.

**Concrete cost numbers.** For a 10 km grid with sound waves (speed 350 m/s), CFL gives $\Delta t \leq 29$ s. Refine to 1 km → $\Delta t \leq 2.9$ s. A factor-of-10 spatial refinement *forces* a factor-of-10 shorter time step. In **3D**, a factor-of-2 spatial refinement multiplies the cost by $2^3$ (more cells) × $2^1$ (more time steps) = **16×** more computation. This is why 1 km global models are pushing the edge of even exascale computers.

---

<a id="14"></a>

# 14 Time-Differencing Schemes and the Oscillation Equation

**Why we need time-differencing schemes at all.** *Computers cannot do calculus.* They cannot compute instantaneous rates of change. They can only do arithmetic. So whenever the true equation says "$d\psi/dt = $ something," we must replace it with an arithmetic recipe — "next value = current value + something × $\Delta t$." Time-differencing schemes are exactly those recipes. Choosing a recipe well (stable, accurate) is the entire game.

## 14.1 Why low-order time differencing?

Two reasons:

1. **For PDEs, total error is dominated by the spatial part.** Improving the time-differencing order from 2 to 4 doesn't help much if your spatial scheme has $O(\Delta x^2)$ errors.
2. **Stability already forces $\Delta t$ to be small** (via CFL), so the time discretization is already very fine — temporal accuracy is rarely the bottleneck.

## 14.2 The test problem — the oscillation equation

To compare schemes, apply each one to

$$\frac{d\psi}{dt} = i\omega\psi.$$

The **true solution** is $\psi(t) = \psi(0) e^{i\omega t}$ — a perfect circle of radius $|\psi(0)|$ in the complex plane, going around at angular frequency $\omega$. **Amplitude is constant; phase advances by $\omega\Delta t$ per step.**

Why this equation? It models any wave-like motion (sound, gravity, Rossby, even Coriolis). If a scheme handles the oscillation equation well, it handles waves in PDEs well.

## 14.3 Single-stage two-level schemes

Generic form: $\phi^{n+1} = \phi^n + \Delta t(\alpha f^n + \beta f^{n+1})$, with $\alpha + \beta = 1$.

**One formula, three schemes.** All three classical schemes are *the same recipe* with different weighting between "now" ($\alpha$) and "future" ($\beta$). When $\alpha > \beta$ (more weight on the present, e.g., Euler) the scheme tends to amplify. When $\beta > \alpha$ (more weight on the future, e.g., Backward) the scheme tends to damp. When they're equal (Trapezoidal) it's perfectly neutral. **The constraint $\alpha + \beta = 1$ is consistency** — anything else and the scheme doesn't converge to the true PDE in the limit.

**Implicit = "looking ahead through the windshield"; explicit = "looking only in the rear-view mirror."** Implicit schemes use information about the *future* state (still unknown) inside the equation — they incorporate where the system is *going*, which is why they are stable for arbitrarily long time steps. Explicit schemes only use the *present* state — like driving by looking only behind you, you can only react to what just happened. The trade-off: implicit schemes require solving a system of equations (cost), explicit schemes don't (cheap but stability-limited).

| Scheme | $(\alpha,\beta)$ | Type | Order |
|---|---|---|---|
| Euler (forward) | $(1, 0)$ | Explicit | 1st |
| Backward | $(0, 1)$ | Implicit | 1st |
| Trapezoidal | $(1/2, 1/2)$ | Implicit | 2nd |

Substitute $\phi^{n+1} = A\phi^n$ with $f = i\omega\phi$ to get

$$A = \frac{1 + i\alpha\mu}{1 - i\beta\mu},\qquad \mu = \omega\Delta t.$$

Multiply by conjugate:

$$|A|^2 = \frac{1 + \alpha^2\mu^2}{1 + \beta^2\mu^2}.$$

**Reading this formula.** $\mu = \omega\Delta t$ is "how many radians of the true oscillation are squeezed into one numerical step." The numerator $1 + \alpha^2\mu^2$ comes from the *explicit* part of the scheme — it always *grows* with $\mu$. The denominator $1 + \beta^2\mu^2$ comes from the *implicit* part — it always *shrinks* the result. So if $\alpha > \beta$ (more explicit than implicit, e.g., Euler with $\alpha=1, \beta=0$) we get $|A| > 1$ — explosive. If $\beta > \alpha$ (more implicit, e.g., Backward with $\alpha=0, \beta=1$) we get $|A| < 1$ — damped. If $\alpha = \beta = 1/2$ (Trapezoidal) the two effects exactly cancel and $|A| = 1$ — perfectly neutral. The single formula captures all three classical schemes.

| Scheme | $|A|$ | Behavior |
|---|---|---|
| **Euler** | $(1+\mu^2)^{1/2}$ | $|A|>1$ — **always unstable** |
| **Backward** | $(1+\mu^2)^{-1/2}$ | $|A|<1$ — **unconditionally stable, damping** |
| **Trapezoidal** | $1$ | $|A|=1$ — **always neutral** |

**HW3 verifies all of this numerically over 30 time steps:**

- **Euler** at $\mu \in \{0.196, 0.393, 0.785, 1.571\}$: amplitude grows; for $\mu = 1.571$ it reaches $\sim 1.26\times 10^8$ in 20 steps. Even tiny $\mu = 0.196$ ends at $|A|=1.019$ → after 30 steps $\sim 1.76$. **No safe $\mu$.**
- **Backward** at the same $\mu$ values: amplitude decays. At $\mu = 1.571$, $|A| = 0.537$ → drops to nearly zero in 8 steps.
- **Trapezoidal**: $|A| = 1$ exactly for all $\mu$. The amplitude line lies on $1.0$ for the entire run.

## 14.4 Multi-stage two-level schemes (predictor–corrector)

These get explicit-style cost with implicit-style accuracy.

| Scheme | Formula | Order | Stability |
|---|---|---|---|
| **Matsuno** (Euler-Backward) | $\phi^* = \phi^n + \Delta t f^n$, then $\phi^{n+1} = \phi^n + \Delta t f^*$ | 1st | $|A|=(1-\mu^2+\mu^4)^{1/2}$ — stable for $\mu \leq 1$, **conditionally stable** |
| **Heun** (RK2) | $\phi^* = \phi^n + \Delta t f^n$, then $\phi^{n+1} = \phi^n + \tfrac12\Delta t(f^n + f^*)$ | 2nd | $|A|=(1+\tfrac14\mu^4)^{1/2}$ — **always slightly unstable**, but instability is $O(\Delta t^4)$ so weak |

**Matsuno's special damping property.** Differentiate $|A|$ with respect to $\mu$ and set zero: minimum at $\mu = 1/\sqrt{2}$. For $0 < \mu < 1/\sqrt{2}$, Matsuno *damps high-frequency noise* — useful for filtering spurious oscillations from imperfect ICs.

**Why this damping is a *feature*, not a bug.** Initial conditions from observations always have small noise — measurement errors, interpolation artifacts, unbalanced fast-wave content. These errors mostly live at *high* frequencies. If you choose your time step so $0 < \mu < 1/\sqrt{2}$ for the highest frequencies you care about, Matsuno preferentially damps those modes — acting like a built-in selective filter that scrubs IC noise without touching the slow weather modes. This is *exactly* the trick that fixed Richardson's fast-wave problem in modern semi-implicit codes.

**Heun's tolerable instability — by the numbers.** Heun's growth is proportional to $\mu^4$ vs. Euler's $\mu^2$. For $\mu = 0.1$:
- Euler: $|A|^2 \approx 1 + 0.01$ → 1% growth per step.
- Heun: $|A|^2 \approx 1 + 2.5\times 10^{-5}$ → 0.0025% growth per step.

Over 1000 steps: Euler grows by factor $1.01^{1000} \approx 21000$ (catastrophic). Heun grows by $1.000025^{1000} \approx 1.025$ (a 2.5% drift — entirely tolerable for short forecasts).

**HW3 verifies Matsuno**: for $\mu = 1/\sqrt{2}$, $|A| = 0.866$ — strongest damping. For $\mu = 1$, $|A| = 1$ (neutral, edge of stability). For $\mu = 1.4$, $|A| = 1.7$ — unstable, blows up.

## 14.5 Three-level schemes

These use *two* past time levels, $\phi^{n-1}$ and $\phi^n$, to compute $\phi^{n+1}$.

| Scheme | Formula | Order |
|---|---|---|
| **Leapfrog** | $\phi^{n+1} = \phi^{n-1} + 2\Delta t\,f^n$ | 2nd |
| **Adams–Bashforth** | $\phi^{n+1} = \phi^n + \Delta t(\tfrac32 f^n - \tfrac12 f^{n-1})$ | 2nd |

These are explicit and second-order — popular. But they have a hidden cost: **computational modes** (next chapter).

---

<a id="15"></a>

# 15 Computational Modes — The Leapfrog Story

## 15.1 The "extra solution" problem

**The guitar-string analogy for computational modes.** Pluck a guitar string and it vibrates at its natural physical frequency (the fundamental). But the string also supports overtones — *parasitic* harmonics that ring simultaneously. In a *two-level* time scheme, there's room for only one harmonic (the physical mode). In a *three-level* scheme, there's room for two — and the second one is the **computational mode**, a parasitic overtone with no physical meaning. **More time levels in your recipe → more parasitic ghosts.** This is a general rule: an $N$-level scheme has $(N-1)$ amplification roots, only one of which is physical; the other $N-2$ are computational modes.

A three-level scheme has *two* roots for the amplification factor — because it is effectively a second-order recurrence. Apply leapfrog to the oscillation equation:

$$\phi^{n+1} = \phi^{n-1} + i\,2\omega\Delta t\,\phi^n.$$

With $\phi^{n+1} = A^2\phi^{n-1}$, you get the quadratic

$$A^2 - 2i\mu A - 1 = 0,$$

with roots

$$A_1 = i\mu + \sqrt{1 - \mu^2},\qquad A_2 = i\mu - \sqrt{1 - \mu^2}.$$

As $\Delta t \to 0$, $A_1 \to 1$ and $A_2 \to -1$.

- $A_1$ corresponds to the **physical mode** — the right answer.
- $A_2$ corresponds to a **computational mode** — a non-physical zig-zag that flips sign every time step. It exists *only because* we used three time levels.

**The zig-zag pattern — the signature of computational modes.** Because $A_2 \approx -1$, the computational mode multiplies by $-1$ every step. So at even time steps ($n = 0, 2, 4, \ldots$) the sign is positive, and at odd time steps ($n = 1, 3, 5, \ldots$) the sign is negative. **The numerical solution oscillates wildly between positive and negative from one time step to the next** — completely unphysical. If you ever see your model output zigzagging like that, you've found a computational mode.

**Why $|A_2| = 1$ is *bad*.** If the computational mode were *damping* ($|A_2| < 1$) it would die away on its own and we wouldn't worry. But $|A_2| = 1$ means it's neutral — once excited, **it persists forever at the same amplitude.** That's why filters or occasional two-level steps are necessary: the bad mode is unkillable on its own.

## 15.2 Three regimes

| Range of $\mu$ | $|A_1|, |A_2|$ | Behavior |
|---|---|---|
| $|\mu| < 1$ | both equal 1 | stable, neutral; computational mode is a $4\Delta t$ zig-zag |
| $|\mu| = 1$ | both equal 1 | neutral but phase error is huge (rotates by $\pi/2$ per step instead of by $\mu$) |
| $|\mu| > 1$ | $|A_1|$ or $|A_2| > 1$ | unstable; growing mode has period $4\Delta t$ |

**HW2 demonstrates this perfectly.** Running CTCS (centered time + centered space, i.e., leapfrog) on $u_t + cu_x = 0$:

- $\mu = 0.5$: stable but with a small phase lag (dispersion).
- $\mu = 1.0$: stable and *exactly* on the exact solution at the snapshot time, but the amplitude oscillates around $1.0$ with peaks ~$1.08$ — that's the computational mode excited by the imperfect Euler first step.
- $\mu = 2.0$: blows up well before $t = 0.5$.

## 15.3 Why the computational mode appears

To start a leapfrog you need *two* initial conditions: $\phi^0$ and $\phi^1$. Physics gives you only $\phi^0$. To get $\phi^1$ you must use a two-level scheme (Euler, Heun) — and **that step always seeds a small computational mode**, no matter how careful you are. Even round-off error keeps it alive.

## 15.4 Controlling the computational mode

Three strategies:

1. **Use a scheme without it** (e.g., RK4, leapfrog with Asselin filter, semi-Lagrangian).
2. **Insert an occasional two-level step** (every ~50 steps, do an Euler step) — this kills the zig-zag.
3. **Apply a filter** — the **Robert–Asselin filter** is a tiny smoothing applied at every step that selectively damps the $4\Delta t$ mode while leaving the physical solution alone.

The Robert–Asselin filter is concretely:

$$\boxed{\phi^n_{\text{filtered}} = \phi^n + \gamma\big(\phi^{n-1} - 2\phi^n + \phi^{n+1}\big),}$$

with $\gamma$ small (typically $\gamma \approx 0.05$–$0.1$). The expression in parentheses is the centered second-difference in time — it is essentially zero for the smooth physical mode (which barely changes from one step to the next on the time scale of $\Delta t$) but maximal for the $\pm 1$ flipping computational mode. So the filter touches the bad mode and leaves the good one alone.

In **HW1, HW2, and HW5**, the very first step is taken with Euler. That single Euler step is what excites the computational mode to begin with — a tiny seeding that the leapfrog then carries forward as a small wobble around the true amplitude. Without a filter you can clearly see this in HW2 Case 1 ($\mu = 0.25$): max amplitude oscillates around 1.0 with peaks of about 1.005 — small but real.

## 15.5 Phase error analysis

Write $A = |A| e^{i\theta}$. The numerical phase advance per step is $\theta$; the true is $\omega\Delta t$. Their ratio:

| Scheme | $\theta/\mu$ | Effect on phase speed |
|---|---|---|
| Euler / Backward | $\arctan(\mu)/\mu$ | Always $<1$ — **decelerating** |
| Matsuno | $\arctan(\mu/(1-\mu^2))/\mu$ | Accelerating for small $\mu$ |
| Trapezoidal | $\arctan(\mu/(1-\mu^2/2 + \mu^2/2))/\mu$ | Close to $1$ |

**Practical note.** Phase errors from time differencing are usually *smaller* than phase errors from space differencing, so we worry less about them. But we should still know which schemes accelerate vs. decelerate.

---

<a id="16"></a>

# 16 Space Differencing — Phase, Group Velocity, Dispersion

The previous chapters mostly held space-derivatives "perfect" and asked: how does *time* differencing fail? Now we flip it: assume time is perfect (tiny $\Delta t$), and ask: what does *space* differencing do to a wave?

**The ocean-wave-on-a-beach picture.** Imagine you're watching ocean waves approach a beach. The water is continuous, but you can only stand at certain *fixed observation posts* spaced $\Delta x$ apart. As the wave moves through, you record the water height at each post. **You've just done a finite-difference approximation in space.** The questions: at what speed do you see the wave move from post to post? Does its shape stay intact, or get distorted? That's exactly the question this chapter answers — and as we'll see, *every* finite-difference scheme in space distorts waves in characteristic ways.

## 16.1 Setup — differential-difference equation

Replace the spatial derivative by a centered difference:

$$\frac{d\phi_j}{dt} + c\frac{\phi_{j+1} - \phi_{j-1}}{2\Delta x} = 0.$$

Plug in the wave $\phi_j(t) = e^{i(kj\Delta x - \omega t)}$:

$$\boxed{\omega_{2c} = c\,\frac{\sin k\Delta x}{\Delta x}}.$$

**Two consequences:**

- $\omega_{2c}$ is *real* → no amplitude error.
- The **numerical phase speed** is

$$c_{2c} = \omega_{2c}/k = c\,\frac{\sin k\Delta x}{k\Delta x}.$$

This depends on $k$ → the scheme is **dispersive**, even though the true equation is non-dispersive.

## 16.2 What this means for waves of different lengths

| Wavelength $L_x$ | $k\Delta x$ | $c_{2c}/c$ | Comment |
|---|---|---|---|
| Long ($L_x \gg \Delta x$) | $\to 0$ | $\to 1$ | well represented |
| $L_x = 4\Delta x$ | $\pi/2$ | $2/\pi \approx 0.64$ | slowed |
| $L_x = 2\Delta x$ | $\pi$ | $0$ | **stationary** — does not propagate |

**Why the $2\Delta x$ wave is stationary — physical intuition.** A $2\Delta x$ wave has values that *alternate* sign at every grid point: $+1, -1, +1, -1, \ldots$. The centered difference looks one step right and one step left: at point $j$ where the value is $+1$, both $j+1$ and $j-1$ have value $-1$. So $\phi_{j+1} - \phi_{j-1} = (-1) - (-1) = 0$. **The scheme literally cannot see a gradient — the apparent slope at $j$ is zero, even though the wave is varying maximally.** Hence its phase speed is zero. This isn't an arithmetic accident; it's the fundamental geometry of the centered stencil.

**Two effects of computational dispersion.**
1. *General slowdown*: every wave moves slower than the truth, so a propagating pattern arrives late.
2. *Pattern distortion*: different wavelengths slow by different amounts, so a multi-wavelength feature (a front, a shear line, a moisture plume) **deforms over time** — its long components race ahead while its short components lag. The original shape blurs and trails.

For long waves, expand $\sin x \approx x - x^3/6$:

$$c_{2c} \approx c\left[1 - \frac{(k\Delta x)^2}{6}\right].$$

This is a **second-order phase-speed error**.

## 16.3 Group velocity is even worse

$$c_g = \frac{\partial\omega_{2c}}{\partial k} = c\cos k\Delta x.$$

For the $2\Delta x$ wave, $\cos\pi = -1$, so $c_g = -c$. **Energy at the shortest wave propagates *backwards*.** This is the source of the famous "dispersive wakes" upstream of fronts and shocks in coarse models.

**Why this is unphysical.** Imagine simulating a thunderstorm front moving east at 20 m/s. The front contains short-wavelength components (the sharp gradient where the temperature drops). On a centered-difference grid, those short components send energy *upstream* (westward!) — *spurious wave noise appears ahead of the storm, where there's nothing physically going on*. This is a real, widely-documented artifact in NWP output. It's also a cue for forecasters: rippling features upstream of a front are often a sign of poor short-wave handling.

## 16.4 Higher-order centered schemes

The standard **4th-order centered** formula uses a 5-point stencil:

$$\frac{\partial \psi}{\partial x}\bigg|_j \approx \frac{-\psi_{j+2} + 8\psi_{j+1} - 8\psi_{j-1} + \psi_{j-2}}{12\Delta x}.$$

| Scheme | $c_{\text{num}} - c$ for long waves | $c_{\text{num}}$ at $2\Delta x$ |
|---|---|---|
| 2nd-order centered | $-c(k\Delta x)^2/6$ | $0$ |
| 4th-order centered | $-c(k\Delta x)^4/30$ | $0$ |

Going from 2nd to 4th order **dramatically** improves long- and medium-wavelength representation. **Concrete numbers** for 10 grid points per wavelength ($k\Delta x = 2\pi/10 \approx 0.63$):

- 2nd order: error $\approx (0.63)^2/6 \approx 7\%$ (wave moves at 93% of true speed).
- 4th order: error $\approx (0.63)^4/30 \approx 0.05\%$.

The $2\Delta x$ wave is *still* stationary at 4th order — no amount of higher-order cleverness fixes it (the centered stencil is symmetric, and a $2\Delta x$ wave is exactly antisymmetric about every grid point, so all symmetric stencils give zero gradient). **Lesson:** never rely on $2\Delta x$ features.

## 16.5 The upstream scheme — dispersion *and* dissipation

For 1st-order upstream:

$$i\omega = \frac{c}{\Delta x}(1 - e^{-ik\Delta x})$$
$$\omega = \frac{c}{\Delta x}\big[\sin k\Delta x + i(\cos k\Delta x - 1)\big].$$

- **Real part** → same dispersion as centered.
- **Imaginary part** → $e^{-i\omega t} = e^{-(1-\cos k\Delta x)\,c/\Delta x \cdot t}$ → **damping**. For $c > 0$, all waves decay; the shortest decay fastest.

**Bottom line.** Upstream is dissipative. Centered is dispersive. Both are bad in different ways.

## 16.6 The dispersion diagram

Plot $\omega$ vs $k$. Superimpose the **true** straight line $\omega = ck$ (slope $c$) and the **numerical** curve. At any wavenumber:

- Slope from origin to point on curve = **phase speed**.
- Slope of tangent at point = **group velocity**.

For 2nd-order centered: the numerical curve coincides with the true line at small $k$, then bends down, hits zero slope at $k\Delta x = \pi/2$, and finally has *negative* slope near $k\Delta x = \pi$ — that's the backward group velocity.

---

<a id="17"></a>

# 17 The Modified Equation — What Are You *Actually* Solving?

## 17.1 The idea

When you discretize a PDE, the equations the computer is *actually integrating* differ from the original. Taylor-expand the FD operator and see what extra terms appear.

For order $p$ centered or upstream finite difference of the spatial derivative,

$$\frac{\partial \psi}{\partial t} + c\frac{\partial \psi}{\partial x} = (\text{leading-order extra term}).$$

| Scheme order | Leading extra term | Type |
|---|---|---|
| 1st | $c\Delta x/2 \cdot u_{xx}$ | **diffusion** (parabolic) |
| 2nd | $-c\Delta x^2/6 \cdot u_{xxx}$ | **dispersion** |
| 3rd | $c\Delta x^3/12 \cdot u_{xxxx}$ | **diffusion** (hyper-) |
| 4th | $-c\Delta x^4/30 \cdot u_{xxxxx}$ | **dispersion** |

**Pattern.** Odd-order schemes have dissipation as leading error; even-order schemes have dispersion as leading error.

**Why even = dispersion, odd = dissipation (Fourier intuition).** When you transform a derivative term into Fourier space, $\partial^n/\partial x^n$ becomes $(ik)^n$. Now look at the powers:
- $(ik)^1 = ik$ → imaginary → phase change → **dispersion**.
- $(ik)^2 = -k^2$ → real (negative) → amplitude change → **dissipation**.
- $(ik)^3 = -ik^3$ → imaginary → dispersion.
- $(ik)^4 = k^4$ → real → dissipation.
- $(ik)^5 = ik^5$ → imaginary → dispersion.

So *odd derivatives* contribute imaginary terms (phase) and *even derivatives* contribute real terms (amplitude). The leading truncation error of an odd-order scheme is an even-derivative correction → real → dissipation. The leading error of an even-order scheme is an odd-derivative correction → imaginary → dispersion. **The pattern follows from the algebra of Fourier modes** — it's not a coincidence.

## 17.2 Practical consequence

- **Pure 2nd order** is undamped, so spurious short-wave noise can propagate upstream and contaminate the field.
- **Adding artificial dissipation** is a standard technique to control this without ruining accuracy.

## 17.3 Artificial / scale-selective dissipation

The simplest extra term:

$$\frac{d\phi_j}{dt} = \gamma_2(\phi_{j+1} - 2\phi_j + \phi_{j-1}).$$

Plug in $\phi_j = A(t) e^{ikj\Delta x}$:

$$\frac{dA}{dt} = -2\gamma_2(1 - \cos k\Delta x)\,A.$$

**Reading these equations.** The first line is just an added diffusion term, applied via the same three-point stencil as the physical diffusion (Section 21.2). The coefficient $\gamma_2$ controls how aggressive the smoothing is. The second line is the Fourier-mode growth rate. The factor $(1 - \cos k\Delta x)$ is zero for long waves ($k\Delta x \to 0$) and largest for the $2\Delta x$ wave ($k\Delta x = \pi$, where $\cos = -1$ and the factor is $2$). So each Fourier mode is damped at a rate that depends entirely on its wavelength: long waves are barely touched, the worst-case grid-scale wave is killed off the fastest. This is what *scale-selective* means.

This damps $2\Delta x$ most strongly (where $1 - \cos k\Delta x = 2$) and barely touches long waves. **Scale-selective:** the property we want from a smoother.

Higher-order smoothers ($\nabla^4$, $\nabla^6$) are even more selective: they leave well-resolved waves nearly untouched while killing grid-scale noise.

## 17.4 When dissipation is necessary

Low-viscosity flows (high Reynolds number) **do not stay smooth**. Energy cascades from large to small scales; once it hits the grid limit ($2\Delta x$), it has nowhere to go physically — but numerically it bounces back via aliasing (next chapter), and the simulation goes haywire. **Adding artificial dissipation gives the energy a sink.**

**The bathtub-with-a-plugged-drain analogy.** Imagine a bathtub where water flows in (energy cascading down from large scales) but the drain is plugged. The water has nowhere to go — it just keeps rising until the tub overflows. That's exactly what happens with grid-scale energy and no dissipation: it accumulates at $k_{\max}$ until the simulation explodes. Adding artificial dissipation is like *unplugging the drain*: energy can finally exit the system at the grid scale, just as molecular viscosity drains it in real life.

**The antibiotic-selectivity analogy for filter order.** Different-order filters trade off between killing the noise and damaging the physics:
- **2nd-order filter** = broad-spectrum antibiotic. Kills the infection (grid-scale noise) but also damages healthy tissue (long waves you want to keep).
- **4th-order filter** = more targeted antibiotic. Hits short waves much harder than long ones; less collateral damage on the resolved part of the solution.
- **6th-order filter** = precision drug. Attacks almost exclusively the offending grid-scale modes while barely touching anything well-resolved.

Higher order means more selective. The cost is wider stencils and harder boundary handling.

---

<a id="18"></a>

# 18 Combining Time and Space — Total Error

When you put a time scheme together with a space scheme, the combined behavior is not always the sum of the parts.

| Time | Space | Combined behavior |
|---|---|---|
| Forward (amplifying) | Centered (neutral) | **Amplifying** (FTCS — unstable, see HW1, HW4) |
| Forward (amplifying) | Upstream (damping) | Possibly stable (FTUS upstream scheme — yes, stable for $\mu \leq 1$) |
| Leapfrog (neutral) | Centered (neutral) | Conditionally stable (CTCS — see HW1) |
| Leapfrog (neutral) | Upstream | **Unstable** (the computational mode runs the wrong way through the upstream stencil) |

The full von Neumann analysis is needed to find exact conditions. But the table is a great heuristic.

## 18.1 The CTCS amplification factor — full derivation

The winning combination for advection in atmospheric models is **CTCS** (Centered-in-Time + Centered-in-Space) — leapfrog time + centered space:

$$\frac{\phi_j^{n+1} - \phi_j^{n-1}}{2\Delta t} + c\,\frac{\phi_{j+1}^n - \phi_{j-1}^n}{2\Delta x} = 0.$$

Rearranging:

$$\phi_j^{n+1} = \phi_j^{n-1} - \mu\big(\phi_{j+1}^n - \phi_{j-1}^n\big).$$

Substitute $\phi_j^n = a_k^n e^{ikj\Delta x}$ with $a_k^{n+1} = A\,a_k^n$ and $a_k^{n+1} = A^2\,a_k^{n-1}$:

$$A^2 + 2i\mu\sin(k\Delta x)\,A - 1 = 0.$$

Solve the quadratic:

$$A = -i\mu\sin(k\Delta x) \pm \sqrt{1 - \mu^2\sin^2(k\Delta x)}.$$

**Reading these equations.** The leapfrog scheme uses *two past time levels* to compute the next, so the amplification per step appears as a *quadratic* in $A$ rather than a linear formula. That quadratic has *two roots* — the $\pm$ in front of the square root — and each root represents a separate "mode" that evolves through the scheme. The $+$ root tracks the true physical wave; the $-$ root is the **computational mode** (a spurious oscillation that flips sign every step). The square root is real when $|\mu\sin(k\Delta x)|\le 1$ — that is the stability range. The discriminant going negative ($\mu\sin(k\Delta x) > 1$) would make $A$ pick up a real exponential growth factor.

Two roots — **two modes** (physical + computational, as for any 3-level scheme, §15). For $|\mu\sin(k\Delta x)| \leq 1$, both roots have $|A|^2 = \mu^2\sin^2 + (1 - \mu^2\sin^2) = 1$. **Both are exactly neutral** — no amplitude error within stability.

Stability requires $|\mu\sin(k\Delta x)| \leq 1$, and since $|\sin(k\Delta x)| \leq 1$ for all $k$, the strongest constraint is $|\mu| \leq 1$. So CTCS is **conditionally stable** with the standard CFL condition, second-order accurate in space and time, and neutral within stability — *the workhorse of atmospheric modeling*. **HW1** demonstrates this directly: CTCS runs cleanly on the rotating cone while FTCS blows up under identical conditions.

The catches you must remember:
1. Leapfrog has a computational mode (the $-$ root) — controlled by Euler first step or a Robert–Asselin filter (§15.4).
2. Centered space is dispersive (§16) — the $2\Delta x$ wave is stationary; cone widens by ~16% per rotation in HW1 even though amplitude *should* be conserved.

## 18.2 Magic CFL — when upstream becomes perfect

A side note on the upstream scheme's modified equation (§17):

$$u_t + cu_x = \frac{c\Delta x}{2}(1 - \mu)\,u_{xx} + \cdots$$

When $\mu \to 1$, the leading numerical-diffusion coefficient $\to 0$ — **the upstream scheme becomes exact**. Physically, the wave moves exactly one grid cell per time step; the new value at $j$ is just the old value from $j-1$ copied over. No artificial diffusion.

This is sometimes called the **"magic CFL"** for upstream and is occasionally exploited deliberately. Of course, in real models $c$ varies in space and time, so you can never sit at $\mu = 1$ everywhere — but this insight explains why upstream is *less* diffusive at higher CFL than at lower CFL.

---

<a id="19"></a>

# 19 Staggered Grids

## 19.1 The problem with un-staggered

In the linear shallow-water system

$$\partial_t h + H\partial_x u = 0,\qquad \partial_t u + g\partial_x h = 0,$$

if you put $u$ and $h$ at the *same* grid points and use centered differences, the derivative skips $\Delta x$ — it uses points $j+1$ and $j-1$, not $j$ itself. **The grid splits into two non-talking sub-grids** (even-index points only see other even points). A perturbation at one even point spreads only to other evens, and the odd points stay zero forever.

**The skip-over problem.** Centered differences ignore the point right in the middle. It's like estimating the slope of a hilly road by measuring elevation at two posts 200 m apart while completely ignoring what happens at the post directly under your feet. If the road has a small bump *exactly* at that middle post, your slope estimate misses it entirely. On a co-located grid this means the derivative formula has *no information* about what's happening at the very point where you're trying to compute it.

**HW5 demonstrates this.** Setting $\phi = 100$ at $j = 50$ (even index) on a 100-point un-staggered grid and integrating for 6 hours: only the *even* indices ever become nonzero. The odd-indexed points remain exactly zero. **The grid has two completely independent solutions.**

## 19.2 The Arakawa C-grid

Solution: place $u$ at "full" points $j$ and $h$ at "half" points $j+1/2$. Now:

$$\delta_x h_j = \frac{h_{j+1/2} - h_{j-1/2}}{\Delta x},\qquad \delta_x u_{j+1/2} = \frac{u_{j+1} - u_j}{\Delta x}.$$

Each derivative now uses *adjacent* points, separated by $\Delta x$ instead of $2\Delta x$. The two sub-grids are gone.

## 19.3 What you gain

- **Better dispersion at short wavelengths.** On the unstaggered grid, $c_u/c = \sin(k\Delta x)/(k\Delta x)$ — zero at $2\Delta x$. On the staggered grid, $c_s/c = 2\sin(k\Delta x/2)/(k\Delta x)$ — at $2\Delta x$ wave, $c_s/c = 2/\pi \approx 0.64$. Big win.
- **Better group velocity.** On the unstaggered grid, $c_g$ goes negative for short waves. On the staggered grid, $c_g = c\cos(k\Delta x/2) \geq 0$ — never negative.
- **Cleaner physics, fewer spurious modes, better energy conservation.**

**HW5 confirms numerically.** For $\Delta x = 100$ km and $c = 300$ m/s:

| $L_x$ (km) | Unstaggered (m/s) | Staggered (m/s) | True (m/s) |
|---|---|---|---|
| $200 = 2\Delta x$ | 0.00 | 195.4 | 300 |
| $800 = 8\Delta x$ | 270.8 | 293.3 | 300 |
| $1200 = 12\Delta x$ | 286.9 | 297.0 | 300 |
| $2000 = 20\Delta x$ | 295.2 | 298.9 | 300 |

The staggered grid is more accurate at *every* wavelength.

## 19.4 What you give up

- **Smaller maximum time step.** The CFL on the staggered grid is $c\Delta t/\Delta x < 1/2$ instead of $< 1$. So you need a time step half as large for the same $\Delta x$.
- **Slightly more bookkeeping** at boundaries and when interpolating between variables.

In **HW5** part (c), the staggered run uses $\Delta t = 3$ min vs. the un-staggered run's $\Delta t = 5$ min for the same problem.

## 19.5 Other staggered grid types

- **Grid A** (un-staggered, MM5).
- **Grid B** (intermediate).
- **Grid C** (Arakawa C, WRF) — what most modern atmospheric models use.

## 19.6 Temporal staggering — forward–backward

Sometimes you stagger in time too. For the shallow-water system you can:

1. Update $u$ forward using the **current** $h$.
2. Update $h$ "backward" using the **just-updated** $u$.

This gives essentially the benefits of an implicit scheme without solving a system. Classic in oceanography.

---

<a id="20"></a>

# 20 Aliasing and Nonlinear Instability

## 20.1 What is aliasing?

A grid with spacing $\Delta x$ can represent waves up to wavenumber $k_{\max} = \pi/\Delta x$, i.e., wavelengths $\geq 2\Delta x$. **Anything shorter cannot be represented honestly.** If a process *creates* a wave with $k > k_{\max}$, the grid sees it as a wave with $k^* = 2k_{\max} - k$ — a *reflection* across $k_{\max}$.

**Audio analogy.** This is exactly the same phenomenon as in audio digital sampling: if you sample a signal too slowly, high-frequency content masquerades as low-frequency content. The CD sampling rate is **44.1 kHz** so it can capture frequencies up to **22.05 kHz** (the Nyquist frequency); anything higher gets aliased into the audible range and sounds wrong. To prevent this, audio engineers run a *low-pass filter* in front of the sampler. Atmospheric models do the same with **scale-selective dissipation** or **spectral filters** — they remove the energy near $k_{\max}$ before nonlinearities can scatter more energy beyond it. Same problem, same fix, different domain.

Mathematically, on a discrete grid:

$$\sin(kj\Delta x) = -\sin\big((2k_{\max} - k)\,j\Delta x\big).$$

So the wavenumbers $k$ and $2k_{\max} - k$ are **indistinguishable** at the grid points. A short, unresolvable wave gets "aliased" into a longer, resolvable one.

## 20.2 Why this is dangerous in nonlinear equations

**Linear vs. nonlinear — the key distinction.** In a *linear* PDE, each Fourier mode evolves on its own — never talks to other modes, never creates new ones. Set up the initial condition with wavenumbers $k_1, k_2, k_3$ and you'll have exactly those wavenumbers forever (just with phase/amplitude changes). In a *nonlinear* PDE, modes *multiply* and create *new* wavenumbers. Two modes at $k_1$ and $k_2$ produce a mode at $k_1 + k_2$ and another at $|k_1 - k_2|$. This is the engine of the energy cascade — and the engine of aliasing.

The linear advection equation $u_t + cu_x = 0$ doesn't generate new wavenumbers — each Fourier mode evolves independently. **Nonlinear** equations *do* generate new ones.

Consider Burgers's equation:

$$u_t + u u_x = 0.$$

If $u(x) = \sin kx$, then $u u_x = k\sin kx \cos kx = \tfrac12 k\sin 2kx$. **A new wave at $2k$ has appeared.**

If $k_{\max}/2 < k < k_{\max}$, the new wave at $2k$ is *outside* the resolvable range. The grid doesn't see a $2k$ wave — it sees its alias at $2k_{\max} - 2k$. **Energy that should be cascading toward the dissipation scale is reflected back to longer wavelengths**, where it accumulates instead of being dissipated.

**Concrete example.** Consider a wave with wavelength $\frac{8}{3}\Delta x$ — resolvable, since it's longer than $2\Delta x$. The nonlinear self-product creates a new wave at half the wavelength: $\frac{4}{3}\Delta x$. **That's shorter than $2\Delta x$ — unresolvable.** The grid mis-sees this short wave as a *longer* wave, specifically at about $4\Delta x$. The energy that should have continued cascading down to viscous scales (and dissipated) instead pops *up* to $4\Delta x$, *longer* than the original wave. **Energy moves the wrong way through the spectrum.**

**Two-wave product.** When two waves with $k_1$ and $k_2$ interact, the nonlinear term creates two new wavenumbers: $k_1 + k_2$ (the dangerous one — moves toward $k_{\max}$ and beyond) and $|k_1 - k_2|$ (longer wave). The "$+$" channel feeds the alias-reflection problem; the "$-$" channel just creates resolvable long waves.

**The killer insight: linear stable ≠ nonlinear stable.** A scheme can be perfectly stable in the linear sense (all $|A_k| \leq 1$ for every individual Fourier mode), and it can satisfy CFL exactly, **and yet still blow up** because of nonlinear aliasing. Linear stability tells you each mode is bounded *if it stays in its own lane*. Nonlinear interactions break that lane — energy is exchanged between modes, reflected back at $k_{\max}$, and accumulates. **No reduction of $\Delta t$ can fix this** — the problem is in $\Delta x$, not $\Delta t$. HW6 is the textbook proof.

**Richardson's verse, on a grid.** "Big whirls have little whirls that feed on their velocity / Little whirls have lesser whirls / and so on — to viscosity." In the real atmosphere, energy cascades down to molecular viscosity and dissipates. On a grid, that cascade hits the *wall* at $k_{\max}$ — there's no viscous sink. So energy reflects back via aliasing, and the cascade closes into a positive-feedback loop. The fix is to *add an artificial sink* — scale-selective dissipation that mimics the missing molecular viscosity, only acting near $k_{\max}$.

In reality (no grid), this energy would cascade further down to viscous scales (Richardson's "big whirls have little whirls...") and dissipate. Numerically, the grid acts like a mirror at $k_{\max}$, bouncing energy back. **The energy spectrum gets distorted, the simulation gets noisy, and eventually instability sets in — even if the linear stability conditions are satisfied.**

## 20.3 HW6 — quantitative demonstration

Solve $u_t + uu_x = 0$ on a 20-point periodic grid with leapfrog + centered space.

| Case | IC | $\Delta t$ | $\max|u|$ at end |
|---|---|---|---|
| (a) | $1 + \sin 2\pi x$ | $\Delta x/10$, 100 steps | grows from 2.00 → 6.84 |
| (b) | same | $\Delta x/100$, 500 steps (same physical $t$ as half of (a)) | 4.70 |
| (c) | $2 + \sin 2\pi x + \sin 4\pi x$ | $\Delta x/10$, 100 steps | 6.88 (faster onset) |
| (d) | $3 + \sin 2\pi x + \sin 4\pi x + \sin 6\pi x$ | $\Delta x/10$, 100 steps | peaks at 11.59 (chaotic) |

**Lessons from HW6.**

1. Reducing $\Delta t$ does **not** save you: the instability is driven by *spatial aliasing*, not by CFL. (Compare (a) at step 50 to (b) at step 500 — same physical time, basically same $\max|u|$.)
2. More waves in the IC → more interaction pairs → faster cascade to short waves → faster instability.

## 20.4 How to control aliasing

- **Add scale-selective artificial dissipation** (the $\gamma_2 \nabla^2$ smoother of §17, or higher orders). Damps energy that piles up near $2\Delta x$.
- **Use schemes with implicit dissipation** (1st- or 3rd-order upstream).
- **Use enough points per wavelength** that nonlinear cascades don't reach $k_{\max}$ in the simulation time.
- **Use spectral filters** (apply a low-pass filter every step).

## 20.5 What numerical diffusion accomplishes

If a model includes appropriate dissipation:

- Spectrum matches truth up to the **effective resolution** ($\sim 6\Delta x$).
- Between $6\Delta x$ and $2\Delta x$, energy is **damped** (where we don't trust it anyway).
- Beyond $2\Delta x$, no energy.

Without dissipation:

- Spectrum matches truth at large scales.
- **Spurious energy** piles up between $6\Delta x$ and $2\Delta x$ from aliasing.
- Solution noisy or unstable.

---

<a id="21"></a>

# 21 Diffusion Term — Implicit Schemes, the Péclet Number

## 21.1 The diffusion equation

$$\frac{\partial \psi}{\partial t} = M\frac{\partial^2 \psi}{\partial x^2}.$$

**Reading this equation.** Left side: how fast $\psi$ changes in time at a fixed location. Right side: $M$ (diffusivity, $\mathrm{m^{2}/s}$) times the spatial curvature of $\psi$. So $\psi$ rises wherever it currently sits in a "valley" (curving upward) and falls wherever it sits on a "peak" (curving downward). The diffusivity $M$ sets the *speed* of this smoothing — large $M$ means rapid spread. Same physics as Section 0.4 of Chapter 0; here we are about to discretise it.

This is **parabolic**: amplitude decays, no wave-like propagation. The total amount under the curve is conserved while the curve spreads.

**Real-life example.** A puff of pollutant released over a city at noon. The total mass stays fixed; the puff spreads out and the peak concentration drops.

**Advection vs. diffusion — what each does to a shape.**
- **Advection** moves a shape *without changing it* — the blob slides sideways, maintaining its form.
- **Diffusion** changes a shape *without moving it* — the blob stays in place but spreads out and flattens.
*A bakery is a fixed source of warm air; the wind (advection) carries the warmth toward you, while diffusion (turbulence) spreads it out as it travels. The two effects compose to give you the smell that arrives at your nose.*

**Why the second derivative?** Imagine three thermometers in a row. If the middle one reads *higher* than both neighbors, that point has *negative curvature* (it's a local peak, like a hilltop). Diffusion will *cool* that point — heat flows away from the hot spot toward the cooler neighbors. Mathematically, $\partial^2 \psi/\partial x^2 < 0$ at a peak, so $\partial \psi/\partial t = M\partial^2\psi/\partial x^2 < 0$ — the peak cools. Conversely, a *valley* (positive curvature) warms up. **Diffusion erases curvature.** The temperature at a fixed point changes only if more heat flows in than flows out — which is exactly what curvature measures (the imbalance of fluxes into and out of the point).

## 21.2 Standard explicit FTCS for diffusion

$$\frac{\phi_j^{n+1} - \phi_j^n}{\Delta t} = M\,\frac{\phi_{j+1}^n - 2\phi_j^n + \phi_{j-1}^n}{(\Delta x)^2}.$$

**Reading this update.** The left side is the discrete time derivative — "value next step minus value now, divided by step size." The right side is the discrete second derivative — the famous **three-point stencil** $(\phi_{j+1} - 2\phi_j + \phi_{j-1})/\Delta x^{2}$, which compares cell $j$ to the *average* of its two neighbours. If $\phi_j$ is below the neighbour average (valley), the stencil is positive and $\phi_j$ rises next step. If above the average (peak), it falls. Solving for $\phi_j^{n+1}$ gives an explicit recipe: each new value is a weighted average of three current values, with weights $\nu$, $1-2\nu$, $\nu$.

Define $\nu = M\Delta t/(\Delta x)^2$. Von Neumann analysis gives

$$A_k = 1 - 2\nu(1 - \cos k\Delta x),$$

which is bounded by 1 in absolute value iff

$$\boxed{0 \leq \nu \leq \tfrac12.}$$

This means $\Delta t \leq (\Delta x)^2/(2M)$ — **time step must shrink as the *square* of $\Delta x$**. If you halve $\Delta x$, you must quarter $\Delta t$. **Punishingly expensive at high resolution.**

## 21.3 Implicit (Crank–Nicolson) diffusion

Use trapezoidal time stepping:

$$\frac{\phi_j^{n+1} - \phi_j^n}{\Delta t} = \frac{M}{2}\big(\delta_x^2 \phi_j^{n+1} + \delta_x^2 \phi_j^n\big).$$

**Reading this update.** Same left side as FTCS — the discrete time derivative. The right side averages the discrete second-derivative stencil *between two time levels*: half from the current step ($\delta_x^2\phi^n$, known) and half from the future step ($\delta_x^2\phi^{n+1}$, still unknown). Because the unknown appears on both sides of the equation, you cannot just update cell-by-cell — you have to solve a coupled system of equations for all $\phi^{n+1}$ values simultaneously. That is the price of unconditional stability.

The amplification factor:

$$A_k = \frac{1 - \nu(1 - \cos k\Delta x)}{1 + \nu(1 - \cos k\Delta x)},$$

with $|A_k| \leq 1$ for **all** $\nu$. **Unconditionally stable.**

The cost: at each time step you must solve a tri-diagonal system (in 1D) — fast and standard. In 2D/3D it gets harder, so implicit diffusion is most often used in the **vertical** (where $\Delta z$ near the ground is tiny and explicit would be lethal).

## 21.4 The Péclet number — a hidden truncation error

Combining 1st-order upwind advection with 2nd-order diffusion:

$$\frac{\partial \psi_j}{\partial t} + c\frac{\psi_j - \psi_{j-1}}{\Delta x} = M\frac{\psi_{j+1} - 2\psi_j + \psi_{j-1}}{(\Delta x)^2}.$$

Hidden truncation analysis shows the *equation actually solved* is

$$\frac{\partial \psi}{\partial t} + c\frac{\partial \psi}{\partial x} = M\left(1 + \frac{\text{Pe}}{2}\right)\frac{\partial^2 \psi}{\partial x^2},$$

where the **grid Péclet number** is

$$\text{Pe} = \frac{c\Delta x}{M}.$$

Pe measures *advection vs diffusion at the grid scale*. If $\text{Pe} \gg 1$, the *numerical* diffusion swamps the physical diffusion — your physics is being overwhelmed by your scheme. To get the true diffusion behavior, you want $\text{Pe} \ll 1$, i.e., $\Delta x \ll M/c$.

The **Reynolds number** $\text{Re} = UL/\nu$ is the same idea for momentum.

**Plain-English.** With coarse grids and fast winds, your "diffusion" is mostly numerical — you can't trust it for anything physical.

**Three Péclet regimes — what each looks like in practice.**
- **Pe ≪ 1**: physical diffusion is strong enough to smooth gradients within each grid cell. Numerical artifacts are negligible. *Ideal regime.*
- **Pe ≈ 1**: numerical and physical diffusion are comparable. Numerical adds ~50% extra smoothing on top of physics. Tolerable.
- **Pe ≫ 1**: numerical diffusion completely overwhelms physical diffusion. Solutions look smeared and unreliable; sharp fronts melt into broad gradients. **Bad.**

**Hidden numerical diffusion connection (§17 callback).** The 1st-order upwind scheme has a leading truncation error term $\frac{c\Delta x}{2}\frac{\partial^2\psi}{\partial x^2}$ — that's exactly a *diffusion* term. So even if your physical $M$ is small, your scheme is silently adding $\sim c\Delta x/2$ on top of it. For typical atmospheric values ($c = 10$ m/s, $\Delta x = 10$ km), that's a numerical diffusion of $5 \times 10^4$ m²/s — *thousands of times* larger than typical eddy diffusivities. Conclusion: in coarse-grid weather models, the simulated diffusion is mostly the scheme, not the physics.

---

<a id="22"></a>

# 22 Turbulence, the Closure Problem, and the PBL

**The three components of atmospheric flow.** At any point and time, the wind is the sum of three pieces:
- **Mean wind** — large-scale, slowly varying. Responsible for **advection** (carrying heat, moisture, pollutants horizontally and vertically). Magnitude 2–10 m/s typically.
- **Waves** — organized oscillatory motion (gravity waves, mountain waves, internal waves), often generated by shear or terrain. Effective at transporting momentum and energy.
- **Turbulence** — chaotic, irregular swirling eddies of all sizes. Responsible for the **diffusion** of heat, moisture, and momentum.

PBL turbulence is what makes the boundary layer *the* boundary layer.

**Why the PBL matters — three big reasons.**
1. About **50% of the atmosphere's kinetic energy** is dissipated in the boundary layer.
2. About **90% of the net radiation absorbed by oceans** drives evaporation; latent heat carried in water vapor accounts for **~80% of the fuel** that drives all atmospheric motions.
3. **Almost all human-relevant weather** lives here: thunderstorms, hurricanes, fog, frost, pollution dispersion, agricultural microclimates, the air you breathe.

The PBL isn't an afterthought — it's the engine room.

**The spectral gap as a natural separator.** When you Fourier-decompose the wind speed at a point, you get peaks at large scales (synoptic, ~days) and at small scales (turbulence, seconds–minutes), with a relatively quiet **gap** between them (~10 minutes to 1 hour). This gap *justifies* the Reynolds-decomposition split into "mean + perturbation": there's a natural cut-off period where the spectrum is empty, so the average over that period meaningfully separates "slow weather" from "fast turbulence." Most NWP models pick grid spacings that fall *inside* the spectral gap — the slow side is resolved explicitly, the fast side is parameterized.

## 22.1 The set-up

The actual atmospheric variables ($U$, $V$, $W$, $\theta$, $q$) are *each* the sum of a mean and a turbulent fluctuation:

$$U = \overline U + u',\quad \theta = \overline\theta + \theta',\quad\text{etc.}$$

Plug into the Navier–Stokes / heat / moisture equations and **average**. The averaging rules are:

- $\overline{a' } = 0$ — fluctuations average to zero by definition.
- $\overline{(\overline a)} = \overline a$ — averaging an average just gives the average back.
- $\overline{a + b} = \overline a + \overline b$, $\overline{c\,a} = c\,\overline a$ for constant $c$ — linearity of averaging.
- $\overline{(\overline a)\,b'} = \overline a \cdot \overline{b'} = 0$ — mean times fluctuation averages to zero.

**Critical: products of fluctuations are NOT zero.**
$$\overline{a'^2} \neq 0,\qquad \overline{a'b'} \neq 0,\qquad \overline{a'^2 b'} \neq 0.$$
**This is *the* exception to the averaging rules** and the source of every difficulty in turbulence modeling. These nonzero correlations are precisely the **turbulent fluxes** — the things that move heat, moisture, and momentum vertically through the PBL even when the *mean* vertical wind is zero.

You get equations for the means, but they contain **new unknowns** — the *turbulent fluxes* $\overline{u'_iu'_j}$, $\overline{u'_j\theta'}$, $\overline{u'_jq'}$. These are second-order moments of the fluctuations.

## 22.2 The closure problem

Each new equation introduces *more* unknowns than it solves:

| Order | What we keep prognostic | New unknowns |
|---|---|---|
| 1st | $\overline U_i$ | $\overline{u'_iu'_j}$ → 6 stresses |
| 2nd | also $\overline{u'_iu'_j}$ | $\overline{u'_iu'_ju'_k}$ → 10 third-moments |
| 3rd | also $\overline{u'_iu'_ju'_k}$ | $\overline{u'_iu'_ju'_ku'_m}$ → 15 fourth-moments |

**Total statistical description of turbulence requires an *infinite* set of equations.** This is the **turbulence closure problem** — first noted by Keller and Friedmann in 1924, still unsolved.

**The cascade in running counts.** Consider the deficit between equations and unknowns:
- *1st-moment equations* (mean wind, $\overline U_i$): 3 equations, 6 unknowns ($\overline{u'_i u'_j}$). **Deficit = 3.**
- *Add 2nd-moment equations*: 3 + 6 = 9 equations, but now 6 + 10 = 16 unknowns (the new $\overline{u'_iu'_ju'_k}$ triple correlations). **Deficit = 7.**
- *Add 3rd-moment equations*: 9 + 10 = 19 equations, 16 + 15 = 31 unknowns. **Deficit = 12.**

The deficit *accelerates* as you climb the hierarchy. There is no finite level at which it closes — that's why we have to *parameterize* somewhere along the way.

## 22.3 Closure approximations — what models actually do

You stop somewhere and *parameterize* the next-order unknown in terms of resolved quantities.

- **Zero-order**: parameterize the mean variables themselves. Crude.
- **Half-order ("bulk")**: assume profile shapes (e.g., logarithmic) and shift them by a bulk forecast.
- **First-order (K-theory)**: parameterize 2nd moments via gradients of 1st moments. The famous *gradient-transport* assumption:

$$\overline{w'\theta'} = -K_H\frac{\partial \overline\theta}{\partial z},\qquad \overline{u'w'} = -K_M\frac{\partial \overline U}{\partial z}.$$

**Reading these equations.** The bar denotes a time-average; the primes denote turbulent fluctuations around that mean. The left sides are *covariances* — the average over many seconds of (vertical-velocity fluctuation × temperature fluctuation), and (vertical-velocity fluctuation × horizontal-wind fluctuation). When warm air rises preferentially (positive $\theta'$ paired with positive $w'$) these covariances are positive — heat is being transported upward. The right sides relate these covariances to the *mean* gradient: K-theory says the eddy flux is proportional to (minus) the mean gradient, with eddy diffusivity $K$ playing the same role that the molecular diffusivity $\kappa$ played in Chapter 0's heat equation. The minus sign means transport is *down-gradient* — from hot to cold, from fast to slow.

$K$ has units of m²/s and is called the **eddy diffusivity** / *eddy viscosity* / *turbulent transfer coefficient*. Magnitude in the PBL: 1–100 m²/s, vs. molecular $\nu \approx 10^{-5}$ m²/s — so turbulence mixes ~10⁷ times faster than molecules.

**Gradient transport (a.k.a. K-theory)** is a "small-eddy" closure. It works when turbulent eddies are smaller than the gradient scale. It **fails** for large eddies (deep convection) where transport is *non-local*.

**Why K-theory fails for deep convection.** In a sunny convective PBL, big thermals span the *entire* layer (1–2 km tall). They pick up warm, moist air at the surface and dump it near the inversion at the top — without ever interacting with the local gradient in between. The transport is *non-local*: heat is carried from where the gradient is strongly upward (hot ground) directly to where it's nearly zero (top of mixed layer), skipping the middle. K-theory, which assumes flux ∝ local gradient, can't represent this; it gives the wrong sign of heat flux in the middle of the mixed layer (counter-gradient transport). This is why modern PBL schemes (e.g., YSU, EDMF) augment K-theory with a *non-local mass-flux* term that explicitly accounts for the big thermals.

- **One-and-a-half order**: parameterize $K$ in terms of the prognostic *turbulent kinetic energy* $\overline e$ (and possibly $\overline{\theta'^2}$). More physically grounded:

$$K_M = l\sqrt{2\overline e}\,S_M,\qquad K_H = l\sqrt{2\overline e}\,S_H.$$

Mellor–Yamada-style schemes work this way.

- **Second- and third-order**: prognose more moments. Best physics, expensive.

## 22.4 The planetary boundary layer (PBL)

The PBL is the lowest part of the troposphere, directly influenced by the Earth's surface (friction, heat, moisture). Structure (top → bottom):

| Layer | Height | Process |
|---|---|---|
| Free atmosphere | above ~1–2 km | Geostrophic, mostly laminar |
| Transition layer | $z_i$ (0.1–3 km) | Top of mixed layer |
| Surface layer | 10–100 m | Constant-flux, log wind profile |
| Viscous sublayer | mm | Molecular processes |
| Ground | $z = 0$ | $\vec V = 0$ ("no-slip") |

The PBL is special:

- **Almost always turbulent.** Free atmosphere is mostly not.
- **Strong drag against the surface.**
- **Logarithmic wind profile** in the surface layer.
- **Diurnal cycle**: in the daytime, surface heating drives buoyant convection (free convection). At night, the air radiatively cools and the PBL becomes shallower and stable, often with a low-level jet aloft.

**Why TKE is "the fuel of the PBL."** The TKE budget tells a story:
- Sun heats the ground.
- Ground heats the air via sensible heat flux.
- Buoyancy production (Term III) creates eddies — buoyant production is the *fuel*.
- Eddies stir heat, moisture, and pollutants up through the layer.
- Wind shear over rough ground (cities, forests, fields) creates more TKE mechanically (Term IV).
- Eventually viscosity dissipates everything to heat (Term VII).
- At night, surface cools, buoyancy production dies (or even turns negative), TKE drops → **calm air, fog, frost** form. The morning of the next day, the cycle restarts.

The whole life cycle of the PBL — its growth in the morning, depth at noon, collapse at sunset — is dictated by TKE.

## 22.5 The log wind profile (neutral PBL)

In a neutral surface layer, far from molecular dissipation but in the constant-flux region:

$$\frac{\partial U}{\partial z} = \frac{u_*}{kz}\quad\Longrightarrow\quad U(z) = \frac{u_*}{k}\ln\frac{z}{z_0}.$$

**Reading this equation.** The shear $\partial U/\partial z$ near the ground is large at small $z$ and decays as $1/z$ — so the wind speeds up *fastest* very close to the surface and changes more slowly higher up. Integrating from the roughness height $z_0$ (where the wind is essentially zero) gives a *logarithmic* wind profile. Plug in $z = 10$ m and you get the wind at the standard observing height in terms of just two numbers — the friction velocity $u_*$ (set by surface stress) and the roughness $z_0$ (set by what the surface is made of). This is why every operational weather model carries lookup tables of $z_0$ for grass, forest, city, ocean.

| Symbol | Meaning |
|---|---|
| $u_*$ | **friction velocity** (~$\sqrt{|\overline{u'w'_s}|}$) — a velocity scale set by surface stress |
| $k$ | von Kármán constant, $\approx 0.4$ |
| $z_0$ | **roughness length** — height at which the log profile gives zero wind. ~$10^{-5}$ m for water, several meters for forests/cities |

This is also called the **law of the wall** in engineering. It works to ~20–200 m above the surface.

## 22.6 Monin–Obukhov similarity (non-neutral)

**Why a logarithmic profile shows up in the surface layer.** Two facts hold:
1. The turbulent momentum flux $\overline{u'w'}$ is *constant with height* in the surface layer (this is the "constant flux layer" — the layer is so thin that nothing has time to change).
2. The natural turbulent length scale grows linearly with height: $\ell = kz$ — the higher you go, the bigger the eddies (since they can finally fit). This is the **mixing length** assumption (Prandtl, 1925).
Combine these with K-theory ($K_M = u_*\ell$) and you derive a $1/z$ shear → integrating gives $\ln z$ → the log profile. **The log profile is just the consequence of constant flux + linearly-growing eddies.**

When buoyancy matters, define the **Obukhov length**:

$$L = -\frac{u_*^3}{k(g/T_0)(H_0/\rho c_p)}.$$

$L$ is the height at which buoyant production of TKE equals shear production. Above $L$, buoyancy dominates; below $L$, shear dominates.

**Reading $L$ in plain English.**
- *Numerator* $u_*^3$: rate of *shear* (mechanical) TKE production.
- *Denominator* $(g/T_0)(H_0/\rho c_p)$: rate of *buoyancy* TKE production/destruction.
- The ratio $L$ = the height at which these two rates would be equal.

Below this height, shear dominates → the surface layer behaves close to the neutral log profile. Above it, buoyancy takes over.

**Sign conventions for $\zeta = z/L$.**

| Surface condition | Heat flux $H_0$ | Sign of $L$ | Sign of $\zeta$ | Meaning |
|---|---|---|---|---|
| **Unstable** (sunny day) | $> 0$ (upward) | $L < 0$ | $\zeta < 0$ | Buoyancy *helps* turbulence; thermals form. |
| **Neutral** (overcast, windy) | $\approx 0$ | $|L| \to \infty$ | $\zeta \to 0$ | No buoyancy effect; pure log profile. |
| **Stable** (clear night) | $< 0$ (downward) | $L > 0$ | $\zeta > 0$ | Buoyancy *suppresses* turbulence; layer becomes shallow and quiet. |

**Reading $|L|$ as a length.** If $|L|$ is large (hundreds of meters), the shear/buoyancy crossover is far above your observation height — you're in the neutral-like regime, log profile approximately valid. If $|L|$ is small (a few meters), buoyancy dominates almost everywhere — strong departure from log profile, full M-O correction needed.

**Where M-O came from.** M-O similarity isn't pure theory — its functional forms ($\Phi_m, \Phi_h$) were determined empirically from the **1968 Kansas Field Experiment**: a 32 m tower in a 1-mile² field of wheat stubble, fast-response cup anemometers, sonic anemometers, thermistors. Both heat and momentum fluxes were confirmed constant with height to within ±15%. That's the experimental backbone every operational surface scheme rests on (Businger et al. 1971).

The non-dimensional gradient functions $\Phi_m(\zeta)$, $\Phi_h(\zeta)$ with $\zeta = z/L$ describe deviations from the log profile:

$$\frac{kz}{u_*}\frac{\partial U}{\partial z} = \Phi_m(\zeta),\qquad \frac{kz}{\theta_*}\frac{\partial\theta}{\partial z} = \Phi_h(\zeta).$$

Determined empirically from the **1968 Kansas Field Experiment** (Businger et al., 1971).

**Plain-English.** M-O theory gives you a recipe for the wind and temperature profiles in the surface layer for any thermal stability — useful for plume dispersion, building loading, surface flux estimation in models.

## 22.7 TKE budget

Turbulent kinetic energy $\overline e = \tfrac12(\overline{u'^2} + \overline{v'^2} + \overline{w'^2})$. Its budget:

$$\frac{\partial\overline e}{\partial t} + \overline U_j\frac{\partial\overline e}{\partial x_j} = \underbrace{\frac{g}{\overline\theta_v}\overline{w'\theta'_v}}_{\text{buoyancy}} - \underbrace{\overline{u'_iu'_j}\frac{\partial \overline U_i}{\partial x_j}}_{\text{shear}} - \underbrace{\frac{\partial \overline{u'_je}}{\partial x_j}}_{\text{turb. transport}} - \underbrace{\frac{1}{\overline\rho}\frac{\partial \overline{u'_ip'}}{\partial x_i}}_{\text{pressure}} - \underbrace{\varepsilon}_{\text{dissipation}}.$$

| Term | Meaning |
|---|---|
| Storage (LHS 1) | TKE building up or running down |
| Advection (LHS 2) | TKE carried by mean wind |
| Buoyancy | Daytime heat → vertical thermals → produces TKE; nighttime cooling → consumes TKE |
| Shear | Wind shear over rough ground → produces TKE |
| Turb. transport | Redistributes TKE within PBL |
| Pressure | Redistribution by pressure perturbations |
| Dissipation | Always negative — turbulence degrades to heat at small scales |

**Plain-English.** TKE is the "fuel" of the PBL. Sun heats the ground → ground heats the air → buoyancy creates eddies → eddies stir heat, moisture, and pollutants up; eventually viscosity dissipates them. Wind shear over a city or forest also creates TKE mechanically. At night, cooling kills buoyant production → TKE dies → calm air, fog, frost.

## 22.8 Free vs. forced convection scaling

**Two regimes, two weather situations.**
- **Free convection**: buoyancy dominates, wind weak. *Clear sunny day with light winds.* Air heats up against warm ground, becomes buoyant, rises in plumes. The PBL grows to 2–3 km by mid-afternoon. Cumulus often forms by noon if moisture is sufficient.
- **Forced convection**: shear dominates, buoyancy weak. *Overcast day with strong winds.* Surface heating is suppressed by clouds; turbulence is generated mechanically by wind shear over rough terrain. The PBL stays shallower (~500 m) and turbulent eddies are more horizontal/elongated.

**Free-convection scales — physical meanings:**
- $w_*$ = convective velocity scale. Taller mixed layer → thermals travel farther → they have to move faster to circulate within $t_*$. That's why $z_i$ appears in $w_*$.
- $t_* = z_i/w_*$ = the time for one thermal to circulate from the surface to the top of the mixed layer and back. Typically **5–15 min**. The diurnal cycle is composed of dozens of these turnovers.
- $\theta_*$ = how much warmer thermals are than their surroundings. Typically **0.01–0.3 K**. *Surprisingly small* — yet enough to drive vigorous convection.
- $q_*$ = how much moister thermals are than their surroundings. Typically **0.01–0.5 g/kg**.

**Skew-T levels meteorologists care about (briefly).** The lecture references several thunderstorm-forecasting levels you may see on a Skew-T diagram:
- **CCL** (Convection Condensation Level): height to which a parcel must rise *via surface heating alone* to saturate. Cumulus base on a sunny convective day.
- **$T_c$** (Convection Temperature): the surface temperature needed to push thermals to the CCL. If $T < T_c$ → no thunderstorms. If $T > T_c$ → thunderstorms possible.
- **LCL** (Lifting Condensation Level): saturation height when a parcel is lifted dry-adiabatically (e.g., over a front or mountain). Always at or below CCL.
- **LFC** (Level of Free Convection): once a parcel is lifted past saturation, the height at which it becomes warmer than the environment and rises freely.
- **EL** (Equilibrium Level): the height at which the rising parcel cools back to environmental temperature — the cap of the cumulonimbus.
- **CAPE** (Convective Available Potential Energy): the area on a Skew-T between the LFC and EL — quantifies storm potential energy.

---

<a id="23"></a>

# 23 Source/Sink Terms — Parameterizations

> **Mastery overview.** Chapters 1–22 dealt with the *dynamical core* — the equations that describe motion (advection, pressure gradient, Coriolis) and how to discretize them numerically. But a real atmosphere also contains processes the dynamical core *cannot resolve*: a single thunderstorm inside a 25 km grid box, a leaf transpiring water, a CO₂ molecule absorbing infrared. These have to be approximated by **parameterizations** — formulas that, given the resolved-scale variables in a grid box, predict what the unresolved processes are doing. This chapter walks through every major parameterization in plain English, explains *why* each one is hard, and tells you how they fit together into a working model.

## 23.0 What "source/sink term" actually means

Throughout this course we've been writing the master prognostic equation as

$$\frac{\partial \psi}{\partial t} = -\vec V\cdot\nabla\psi + \nabla^2(K\psi) + S.$$

The first term on the right is **advection** — wind carrying $\psi$ around. The second is **diffusion** — turbulence smearing $\psi$ out. **The third — $S$, the source/sink term — is everything else.** It's where all the parameterized physics live: radiation heating the air, condensation releasing latent heat, convection redistributing moisture, surface fluxes pumping heat from the ground.

**Plain-English picture.** Imagine you're tracking the temperature of a parcel of air. Advection asks: "Is warmer or cooler air being blown in?" Diffusion asks: "Is the parcel mixing with its neighbors?" The source/sink term asks: **"What's happening to the parcel itself?"** — sun heating it, IR cooling it, latent heat being released as moisture condenses inside it, the ground beneath it warming it, etc. All these "happening to it" processes get bundled into $S$.

## 23.1 The split of the prognostic equation

$$\frac{\partial\psi}{\partial t} = D\psi + P\psi,$$

with

- $D\psi$ = **dynamic tendency** (advection, Coriolis, pressure gradient).
- $P\psi$ = **parameterized tendency** = $R\psi + VD\psi + GWD\psi + C\psi + LSP\psi$:
  - $R$ — **radiation**.
  - $VD$ — **vertical diffusion** (PBL).
  - $GWD$ — **gravity wave drag**.
  - $C$ — **convection** (cumulus parameterization).
  - $LSP$ — **large-scale precipitation**.

**Grid-scale vs. sub-grid-scale processes.** Atmospheric physics splits into two camps based on whether the grid can see the process:

- **Grid-scale (explicit):** Things the grid resolves and treats directly.
  - *Microphysics* — cloud droplet formation, freezing/melting, autoconversion to rain. Even though individual droplets are micrometers across, we apply *bulk* equations on the grid-cell averages.
- **Sub-grid-scale (parameterized):** Things much smaller than $\Delta x$ that nevertheless influence the resolved flow.
  - PBL turbulence, cumulus convection, radiation, gravity-wave drag, vegetation, urban canopy, soil layers, aerosols, chemistry.

**What parameterizations output to the rest of the model:** surface fluxes (sensible, latent, momentum), precipitation (especially convective), cloud cover (fractional cloudiness in each grid box), heating and moistening rates (vertical $T$ and $q$ tendencies), eddy diffusivities for the turbulent mixing scheme.

**Why parameterizations are usually *not* the most numerically polished part of the code.** Sub-grid-scale parameterizations have been a major research field for decades, but the *numerical methods used inside them* historically receive less attention than the dynamical core. Why? Because the parameterizations themselves are often considered too *physically uncertain* to merit highly sophisticated numerics. The dominant concerns are **conservation** (mass, energy must be preserved) and **stability** — not 4th-order accuracy. Pragmatically, *the physics is the bottleneck, not the numerics*. So we use forward time integration if it works, switch to implicit if it must, and don't fuss with high-order schemes.

## 23.2 Why leapfrog doesn't work for $P\psi$

Most parameterized processes are diffusive (parabolic). Leapfrog is **unconditionally unstable** for parabolic equations. So we use forward (or implicit) schemes for the parameterized tendencies, and leapfrog for the dynamic ones.

**Plain-English summary.** The dynamical core happily uses leapfrog because advection is hyperbolic — leapfrog is great for hyperbolic. But almost *every* parameterization (radiation relaxes profiles, turbulence smears them, microphysics relaxes RH to 100%) is *diffusive* in flavor. Apply leapfrog to a diffusive equation and the simulation explodes within a handful of steps. So in practice:
- **Dynamic tendencies** ($D\psi$): use leapfrog.
- **Parameterized tendencies** ($P\psi$): use forward Euler if stable, otherwise switch to implicit.
- The two pieces are added together at each step to update $\psi^{n+1}$.

## 23.3 Radiation

Two parts:

- **Atmospheric radiation** — column-radiative heating from CO₂, water vapor, ozone, aerosols. Computed every 10 min – several hours (it changes slowly).
- **Surface energy budget** — must be every time step:

$$R_N = H + H_L + H_G,$$

where $R_N$ is net radiation (downward), $H$ is sensible heat flux, $H_L$ is latent heat flux, $H_G$ is ground heat flux. **Every term must balance every time step**, otherwise the surface temperature drifts.

**Plain-English: what each term does at the surface.**
- $R_N$ = net radiation hitting the ground (downward solar minus upward thermal IR). This is the *fuel*.
- $H$ = sensible heat flux: the ground heats the air directly via conduction → turbulent transfer. (You feel this on a hot blacktop.)
- $H_L$ = latent heat flux: water evaporates from soil/vegetation/oceans, carrying away energy as it leaves. (Why moist surfaces stay cooler than dry ones.)
- $H_G$ = ground heat flux: energy conducted *into the ground* during the day, *back out* at night.

The four terms must balance instantaneously. If $R_N$ rises (sun comes out) and $H_G + H + H_L$ don't immediately rise to match, the skin temperature *jumps* until they do. That instantaneous balance is exactly why the surface scheme runs every model time step — it's much faster than the atmospheric radiation calculation.

**Why atmospheric radiation can be called less often.** Computing radiative transfer through a column means tracking many absorption bands of CO₂, water vapor, ozone, methane; correlations between gases; many vertical levels; multiple zenith angles for the sun; cloud overlap assumptions; aerosol distributions. *It's expensive.* Fortunately the vertical heating profile evolves slowly — over 30–60 min — so calling radiation once every 10–60 min and *holding the rates fixed* between calls is a sensible compromise. The bias introduced is small and worth the speedup. (But see Misconception #7 in §24 — this *does* introduce real errors.)

**Aerosols add real complications.** Aerosol forcing is uncertain — most likely a *negative* radiative forcing globally (cooling effect), but with large error bars (IPCC, 2007). Aerosols affect radiation in three pathways:
- **Direct effect** — particles scatter and absorb sunlight.
- **Semi-direct effect** — absorbing particles (black carbon) heat the air, evaporating nearby clouds.
- **Indirect effect** — particles act as cloud condensation nuclei, modifying cloud droplet sizes (Twomey effect / 1st indirect), drizzle suppression (Pincus & Baker), increased cloud height/lifetime (Albrecht / 2nd indirect). And for ice clouds, aerosols influence contrails and cirrus formation.

Each pathway is named after the researcher who first described it. Each is a separate set of equations the radiation parameterization has to handle.

## 23.4 Microphysics vs. cumulus parameterization

- **Microphysics** = grid-scale moisture (Lin et al. 1983 6-class scheme: vapor, cloud water, rain, ice, snow, graupel). Resolved (or pseudo-resolved). Every time step.
- **Cumulus parameterization** = sub-grid-scale moist convection. Models *can't* resolve a 5-km thunderstorm in a 50-km grid box. The cumulus scheme's job: **release the instability** (consume CAPE) so the grid-scale doesn't blow up trying to do convection at the grid scale. Output: heating profile, drying profile, and convective precipitation. Called every 10 min – hours.

**Microphysics — the six water species and their pathways.** A bulk microphysics scheme (Lin et al. 1983 is the classical one, used in many WRF runs) tracks six water classes:

| Phase | Species | Description |
|---|---|---|
| Gas | Vapor | Water as gas — invisible. |
| Liquid (suspended) | Cloud droplets | Tiny droplets floating in the air; visible as clouds. |
| Liquid (precipitating) | Rain | Larger droplets falling to the surface. |
| Solid (suspended) | Ice crystals | Tiny ice crystals floating in cold clouds. |
| Solid (precipitating) | Snow | Larger ice particles falling. |
| Solid (large) | Graupel/hail | Dense ice particles formed by aggregation/riming. |

The microphysics scheme is essentially a *bookkeeper* of mass transitions between these six pools. Vapor → cloud droplets is **condensation**; cloud droplets → vapor is **evaporation**. Vapor → ice is **deposition**; ice → vapor is **sublimation**. Cloud droplets → rain is **autoconversion** (small drops merge into bigger ones) plus **collection** (rain catching cloud droplets as it falls). Cloud droplets ↔ ice and rain ↔ snow happen via **freezing** and **melting** at the 0 °C isotherm. Each transition has its own parameterized rate, and each rate is a tendency added to the relevant moisture species.

**Why cumulus parameterization is necessary at coarse $\Delta x$.** A real thunderstorm cell is 1–10 km wide. A typical regional model has $\Delta x = 10$–25 km. So one grid cell may contain *many* unresolved cumulus clouds. The cumulus scheme represents their *aggregate* effect on the grid-cell mean fields:
- Heat is *transported upward* (latent heat release in updrafts → mid-troposphere warming).
- Moisture is *transported upward* (boundary-layer moist air → upper troposphere).
- Convective precipitation falls out.
- Compensating subsidence in the rest of the grid cell (outside updrafts) warms and dries the column.

**Why the *primary purpose* is to release instability — not to predict precipitation.** If you didn't have a cumulus scheme:
1. The grid-scale advection would slowly let the column become more and more unstable (high CAPE).
2. Eventually grid-scale moisture would saturate the entire grid box.
3. Latent heat release would produce a *grid-point storm* — a 25 km wide, slow-developing, surface-low-pressure feature, with delayed precipitation onset and unrealistically heavy rain falling uniformly across the entire grid box.
4. This is *physically wrong*: real thunderstorms are 5 km wide, fast-developing, and dump rain in a small fraction of the grid cell.

The cumulus scheme intervenes *before* the grid scale can saturate, "consuming" the CAPE that has built up. Convective precipitation is a *byproduct* of consuming that instability — but the timing, location, and amount are notoriously hard to get right because they depend on the scheme's trigger criterion and closure assumption.

**The "grey zone."** When $\Delta x$ approaches a few km (3–5 km), the grid is starting to resolve individual storms. The cumulus parameterization, which assumes *many* unresolved storms in each grid box, breaks down. But the grid is still too coarse for fully explicit convection. This is the **convective grey zone** — neither fully resolved nor fully parameterized. Active research area; modern operational regional models (e.g., ECMWF AROME at 1.3 km) attempt to operate below it, where convection is mostly explicit. WRF at 4 km is squarely in the grey zone — many practitioners turn cumulus *off* and let the explicit microphysics handle storms, accepting that small storms may be over-resolved as 4–8 grid-point features.

## 23.5 Large-scale precipitation — saturation adjustment

If a grid box ends up with relative humidity $RH > 100\%$ at the end of a time step, the excess water vapor is condensed *instantaneously*: temperature is adjusted up (latent heat release), $q$ is adjusted down, and the box is set to $RH = 100\%$ exactly. **Conservation of internal energy** is enforced.

**Must be done last**, after every other process, so the output state is physical (not supersaturated).

**Why this is treated instantaneously.** Saturation adjustment is so fast in the real atmosphere (seconds) compared to a model time step (minutes) that there's no point time-stepping it. We just apply the algebraic correction: condense the excess, release latent heat, set $RH = 100\%$. Conservation of internal energy means that the latent heat released is *exactly* enough to warm the parcel by the right amount — so the new (warmer) air can hold its (smaller) remaining $q$ at exactly 100% RH.

**Why "last" is important.** If saturation adjustment is applied in the middle of the parameterization sequence — say, before vertical diffusion — a later process could push the grid box back into supersaturation, and the model would output unphysical $RH > 100\%$ fields. Saturation adjustment must be the *final* step so the output state is always physical.

**Clausius–Clapeyron context.** Saturation vapor pressure roughly *doubles* for every 10 °C increase in temperature. So when latent heat release warms the parcel by, say, 2 °C, the saturation $q$ rises by ~14% — meaning the parcel can hold significantly more vapor at the new (warmer) state. This is why the adjustment is *coupled* (you can't just remove the excess vapor; you have to update both $T$ and $q$ together) and why warm air masses produce so much heavier rainfall than cold ones.

## 23.6 Order of processes within a time step

Different orderings give different answers when implicit schemes are involved (because each implicit solver brings its own variables to *its own* equilibrium, ignoring others). Best practice:

- Slow processes (advection) first, with explicit schemes.
- Fast processes (vertical diffusion) last, with implicit schemes.
- Critical: **couple** strongly interacting processes inside the same implicit solver. E.g., implicit vertical diffusion of momentum should include the Coriolis and pressure-gradient terms.

**Why ordering matters when implicit schemes are involved.** Implicit schemes drive *their own variables* to *their own equilibrium* — but if other processes are influencing those variables on similar time scales, the equilibrium they relax toward is the *wrong* one (it ignores the others). A long-time-step implicit solver assumes its process is the only thing happening, but in reality everything is happening simultaneously.

**Concrete example 1: vertical diffusion of momentum.** Suppose you apply implicit vertical diffusion *first*, then Coriolis and pressure gradient afterward. The diffusion solver relaxes the wind profile toward an equilibrium that *ignores* Coriolis and pressure gradient — biasing the momentum profile in a wrong direction. The fix: include Coriolis and pressure-gradient terms *inside* the implicit diffusion solver, so the equilibrium it relaxes toward is the *full multi-process* equilibrium.

**Concrete example 2: stratocumulus-topped PBL.** Radiation cools the cloud top; vertical diffusion redistributes the cooling through the PBL. If radiation and diffusion are called separately (radiation first, then diffusion), the cooling is dumped in one layer for one time step before diffusion can spread it — the result is noisy profiles. The fix: include the radiative tendencies inside the implicit diffusion solver.

**The general principle.** The time evolution of the actual atmosphere is *much slower* than the evolution that any single physical process would produce in isolation, because processes *partially compensate each other* (radiative cooling balanced by turbulent warming from below, etc.). When you take long time steps, you must ensure that strongly-interacting processes are *balanced within the same step* — otherwise the model drifts into spurious states even when the long-term tendency would be small.

**Ordering strategy.** If you can't fully couple, then order by time scale:
1. **Slow processes first** (advection, large-scale dynamics) — explicit, set the broad tendency.
2. **Fast processes afterward** (vertical diffusion, saturation adjustment) — implicit, adjust to the right local equilibrium given the already-incremented fields.

**The honest caveat.** With more than one implicit process, *no clean ordering exists* — every choice biases the answer in some way. This is why operational models invest huge effort in coupling implicit processes together, and why the same model with different process-ordering choices can give noticeably different forecasts. There is no perfect solution, just careful engineering.

**Final note on update frequency.** Some parameterizations (radiation, cumulus, gravity-wave drag) can be called less frequently than the dynamics — every 10 minutes to hours, rather than every 30-second time step — because they evolve relatively slowly. This is a practical compromise to save computation, justified by the slow evolution of those tendencies compared to the dynamical fields. The trade-off: between calls, the heating profile is "frozen" while the dynamics evolve, which introduces a small error.

---

<a id="24"></a>

# 24 Common Modeling Misconceptions

> **Mastery overview.** This chapter is a tour of ten *plausible-sounding intuitions* about numerical weather and climate models that turn out to be oversimplifications or outright wrong. Each one is a trap forecasters and modelers frequently fall into; understanding them is what separates a careful interpreter of model output from someone who blindly trusts the colored map. **Read this chapter as a checklist** for sanity-checking your own thinking the next time you stare at a forecast.

A quick summary table:

| # | Misconception | Reality |
|---|---|---|
| 1 | **High resolution fixes everything.** | No. You also need high-resolution surface data, realistic physics, and good DA. |
| 2 | **A 10 km grid resolves a 20 km feature.** | No. **Effective resolution is ~8–10 Δx.** |
| 3 | **Surface conditions are accurate.** | No. Vegetation, soil moisture, terrain — all approximate. |
| 4 | **The analysis matches observations.** | No, by design. It blends obs with a first-guess. |
| 5 | **Convective parameterization predicts precipitation.** | Its primary purpose is to *release instability*, not predict rain amounts. |
| 6 | **Good large-scale = good convection.** | No. Convection lives at sub-grid scales. |
| 7 | **Radiation is fine without clouds.** | False — even clear-sky radiation is complex. |
| 8 | **Models directly forecast 2 m T, 10 m wind.** | No — these are *diagnosed*, not forecast. |
| 9 | **MOS auto-improves with model improvements.** | No. MOS is tuned to a specific model version. |
| 10 | **You always need full-resolution output.** | No. Coarsened output is fine for many uses. |

Now, each misconception in mastery-level depth.

## 24.1 Misconception #1 — "High resolution fixes everything"

**The intuition (wrong).** "If we just halve the grid spacing, the model will be much more accurate."

**The reality.** Higher resolution helps *only if* matched by:
- **High-resolution surface data.** A 1 km grid is useless if your land-use, soil, and topography come from a 25 km dataset. The model won't *know* there's a city or a forest there.
- **Realistic physics packages.** At high resolution, deficiencies in convection, microphysics, and PBL schemes get *exposed* rather than hidden by the smoothing of a coarse grid. A bad scheme at 10 km can look reasonable; the same scheme at 1 km looks broken.
- **High-resolution observations and good data assimilation.** The initial conditions must contain the small-scale information the high-resolution model is supposed to evolve. If the analysis is too smooth, the model's "fine grid" is filled with extrapolated detail that has no observational basis.

**Concrete example: Hurricane Floyd.** A 5 km simulation captures storm structure (eye, eyewall, rain bands) but the predicted track still differs from observed by tens of kilometers. A 75 km run barely shows a hurricane and the track is much further off. The 5 km is *better*, but neither is "right." The 5 km improvement comes from a combination of dynamics, physics, *and* data — not just resolution.

**A real-world counterexample.** Sometimes **targeted observations** in the right place do more for forecast quality than a resolution increase. Adaptive observing (drop sondes deployed into the inflow region of a storm) can dramatically improve a track forecast by *fixing the initial conditions* — a 75 km model with great ICs can outperform a 5 km model with poor ICs.

**Inherent limitations of very high-resolution models.**
- Observational data may not exist at the model's resolution → the analysis "fills in the holes" with extrapolated (often wrong) details.
- A correct convective forecast requires very accurate moisture profiles — but moisture is highly variable and notoriously hard to analyze from sparse soundings.
- Boundary-layer and surface variables (soil moisture, vegetation phenology, urban canopy) determine instability and convection, but these are often parameterized loosely.
- Microphysics schemes are unlikely to be perfect; their errors become visible at high resolution.

**Practical takeaway.** *Treat resolution as one knob among many.* If the surface data and physics aren't keeping up, refining the grid just gives you a more detailed wrong answer.

## 24.2 Misconception #2 — "A 10 km grid accurately depicts 20 km features"

**The intuition (wrong).** "My grid spacing is half my feature size, so the feature is 'resolved.'"

**The reality.** *Effective resolution* is roughly **$8\Delta x$ to $10\Delta x$** — much coarser than the nominal $\Delta x$. A 10 km grid resolves features of ~80–100 km comfortably. A 20 km feature on a 10 km grid is just barely "on" the grid; it gets distorted, slowed, and dispersed (recall §16: $4\Delta x$ waves move at ~64% of the true speed; $2\Delta x$ waves don't move at all).

**Concrete demonstration.** Plot a sine wave with wavelength $4\Delta x$ on a 10 km grid alongside the true continuous wave. The "model representation" is a coarse stair-step that grossly oversimplifies. Now plot a sine with wavelength $10\Delta x$ — the model representation hugs the true curve almost perfectly. This is the *visual proof* of why $8\Delta x$–$10\Delta x$ is the rule of thumb.

**To resolve a 20 km feature properly**, you need $\Delta x \leq 2$–3 km. And even then, the feature won't survive the entire forecast — it'll degrade as numerical dispersion deforms it over time.

**Practical takeaway.** When the model brochure says "10 km resolution," translate that to "*meaningful structures of ~80 km and larger.*" Don't trust 20–30 km features in the output, even if they show up clearly in your colormap.

## 24.3 Misconception #3 — "Surface conditions are accurately depicted"

**The intuition (wrong).** "The model knows the surface — it has soil moisture, vegetation, terrain, etc."

**The reality.** Surface fields are *coarse, often outdated, and lossy* by the time they get into the model:
- **Vegetation** maps are typically categorical (one type per grid cell), drawn from year-old satellite climatology.
- **Soil moisture** is hard to measure and varies enormously over short distances.
- **Terrain** is *smoothed* during interpolation onto the model grid — a Sierra Nevada peak at 4,400 m might appear in the model at 3,800 m.
- **Land use** transitions are abrupt categorical jumps in the model versus gradual real-world mosaics.
- **SST** can be days old or come from blended satellite/in-situ products with their own biases.

**Concrete example: pre-harvest vs. post-harvest.** Run a single-column model over a corn field through one diurnal cycle, with two scenarios:
- *Pre-harvest case*: 90% green vegetation cover. Most absorbed solar energy goes into latent heat (transpiration), keeping the surface cool. Peak afternoon $T_{2m} \sim 35$ °C.
- *Post-harvest case*: 20% green cover; rest is bare stubble. More energy goes into sensible heat (the bare soil heats up; less evaporation). Peak afternoon $T_{2m} \sim 40$–41 °C.

**A 5–6 °C swing** in afternoon temperature from a *single* surface-input change. Now imagine the model has the wrong vegetation fraction — *every* downstream variable is biased: PBL height, moisture, instability, convective initiation. **A small surface input error can ripple into a missed thunderstorm forecast.**

**Reality in NWP.** Surface conditions in operational models often:
- Use *climatology* (long-term averages) instead of current observations.
- Don't match the model grid scale (different resolution).
- Don't make it into the current run (data latency).
- Aren't accurately analyzed (poor observational coverage).
- Aren't well-handled within the surface physics scheme.

**Practical takeaway.** When something seems "off" about the model's near-surface temperature, *first suspect the surface fields* (soil moisture, vegetation, SST). They're a more common error source than people realize.

## 24.4 Misconception #4 — "The analysis should match observations"

**The intuition (wrong).** "The initial conditions in the model should equal what's been observed."

**The reality.** The initial analysis is a **complicated blend** of observations and a **first-guess field** (short-range forecast from the previous cycle). The blending accounts for:
- Differing accuracy of observing systems (a satellite-derived temperature ≠ a radiosonde ≠ a surface station).
- *Possibility of incorrect observations* (instrument errors, transmission glitches, miscoded reports).
- The relative importance of the trial field and observations in different regions (more trust in obs where they're dense and reliable; more trust in the first-guess where they're sparse).

The analysis must also be **consistent with the model's own resolution and physics** — there's no point assimilating a 1 km feature into a 25 km model that can't represent it.

For all these reasons, **the analysis will differ somewhat from observations by design.**

**The 4DDA cycle.**
1. The model produces a short-range forecast (the *trial field* or *first guess*).
2. New observations come in.
3. An analysis algorithm blends them, producing the new initial conditions.
4. The model is re-launched.
5. Loop forever.

The *goal* is to extract maximum usable information from observations while *avoiding inconsistent information that could corrupt the analysis*. Bad observations are routinely *rejected* — but in the rare case where they were correct, ignoring them yields a bad forecast.

**Why observations and analysis legitimately differ.**
- Different temporal/spatial resolutions.
- Different vertical structure (an observation at 850 mb vs. the model's level closest to it).
- Conflicting observations from different instruments at the same place.
- Observation errors (which the analysis must "filter out").

**Practical takeaway.** When you compare a forecast to "the obs at $t = 0$," remember that the model didn't start *exactly* at the obs — it started at the analysis, which is a deliberately filtered, dynamically-balanced version of the obs. Some discrepancy is by design, not by error.

## 24.5 Misconception #5 — "Convective precipitation is directly parameterized"

**The intuition (wrong).** "The cumulus parameterization's job is to predict convective rainfall."

**The reality.** The *primary* purpose of cumulus parameterization is to **release atmospheric instability** so the resolved equations *don't* spawn unphysical grid-scale storms. Convective precipitation is a *byproduct* — a notoriously unreliable one.

**The natural convective sequence (real atmosphere).** Start with an unstable sounding. A *narrow* updraft (in only a small portion of the grid column) quickly transports heat and moisture upward. Compensating *subsidence* outside the updraft (still within the same grid column) stabilizes the rest. Rain falls in a *small portion* of the grid area; the rest stays dry. After convection weakens, a stratiform anvil cloud may produce light rain from middle and upper levels. Final state: *stable* post-convective atmosphere.

**The "no-cumulus-parameterization" sequence (model bug).**
1. Begin with the same unstable sounding.
2. The model attempts to build convection at the grid scale, with only the slow grid-scale vertical velocities (cm/s, vs. real updrafts at m/s).
3. The cloud builds slowly → *delayed precipitation*.
4. The grid-scale moisture eventually saturates the *entire grid box*.
5. *Heavy precipitation across the entire grid* — not in a narrow strip.
6. Massive latent heat release in lower/mid troposphere → *spurious surface low pressure* ("grid-point storm").
7. The low draws in more moist inflow → more precipitation → positive feedback.

This pathology is exactly why we need a cumulus scheme — to consume the CAPE *before* the grid scale can produce a fictitious storm.

**Why convective precipitation is unreliable even when the scheme is "working."**
- Different schemes give different soundings → different downstream weather.
- Timing and placement depend on the trigger criterion (e.g., minimum cloud depth in mass-flux schemes).
- The scheme doesn't directly modify the model winds, even though real convection *does* alter winds.
- Convective rainfall amounts have large uncertainty band.

**Practical takeaway.** *Don't* use the model's convective precipitation field as a quantitative forecast of how much rain will fall where. Use it as a *qualitative* indicator: "convection likely in this region" — and check ensemble spread to see how confident the forecast is.

## 24.6 Misconception #6 — "A good large-scale prediction implies a good convective prediction"

**The intuition (wrong).** "If the model has the synoptic pattern right (jet stream, fronts, lows), the convective forecast will follow."

**The reality.** A perfect synoptic forecast does *not* guarantee good convection because convection lives at sub-grid scales. Five separate reasons:
1. The model's IC misses small-scale moisture details that convection is sensitive to.
2. The model works on a grid; nature works at much smaller scales.
3. Cumulus-scheme tuning works for the *typical* case but not all situations.
4. CP schemes can be *over-active* (too much drying and stabilization) or *under-active* (grid-point storm pathology).
5. Different CP schemes give different results on the same case → ensemble spread among schemes can be large.

**Over-active CP scheme symptoms.**
- Precipitation over-forecast in the convective area.
- Precipitation *under*-forecast downstream (the air has been over-dried by aggressive convective drying).
- Soundings too dry and stable in both the convective area and downstream.

**Under-active CP scheme symptoms.**
- Explicit (grid-scale) precipitation takes over → grid-point storm pathology (see Misconception #5).
- Precipitation onset is delayed; eventually heavy rain dumps across the entire grid box.
- Too-moist post-convective columns; spurious surface lows.

**Why this matters operationally.** The convective forecast quality depends as much on the *cumulus scheme* and *PBL scheme* as on the synoptic-scale dynamics. Forecasters who only look at the synoptic charts and trust convective parameters from the model can be badly misled.

**Practical takeaway.** Even if your 500 mb map looks great, double-check the model's convective initiation, sounding evolution, and rainfall accumulation. If different ensemble members or different schemes disagree wildly on convective placement, *treat the convective forecast as low-confidence*.

## 24.7 Misconception #7 — "Radiation is well-handled in the absence of clouds"

**The intuition (wrong).** "Without clouds, radiation is just simple absorption/emission — easy."

**The reality.** Even clear-sky SW and LW radiation is *highly complex*:
- CO₂, water vapor, ozone, methane, etc. each have many absorption bands across the spectrum.
- Water-vapor abundance varies enormously vertically and horizontally.
- Aerosol effects (direct, semi-direct, indirect — see §23.3) complicate everything.
- Stratospheric ozone absorption affects UV penetration to the ground.

**Clouds are a complication on top, not the only complication.** Cloud overlap assumptions (random? maximum? maximum-random?) profoundly affect column radiative transfer. Cloud optical thickness, droplet effective radius, cloud-top height, cloud thickness — all matter. But *clear-sky radiation alone* still has uncertainties of several W/m².

**Practical computational consequence.** Radiation is expensive, so it's called less frequently than dynamics — typically every **60 minutes** when the dynamics step is **90 seconds**. Between calls, the heating profile is held *fixed* even as the dynamics evolve. This lag introduces real error: if a cloud moves into a previously clear region between radiation updates, the column radiative cooling won't update for up to 60 min. The error is bounded but real.

**Practical takeaway.** "Radiation is fine in clear sky" is the *sleep-soundly* version of the truth. Reality: radiation has significant uncertainties even without clouds, and the time-lag between radiation calls injects extra error.

## 24.8 Misconception #8 — "Models directly forecast 2 m temperature, 10 m wind, etc."

**The intuition (wrong).** "When I see '2 m temperature' in the model output, the model is forecasting that variable directly."

**The reality.** The model's *lowest* level is typically at **5–50 m** above ground. The 2 m temperature you see is a **diagnosed** quantity — computed *after* the dynamics + physics finish, by interpolating between the lowest model level and the surface skin temperature, using:
1. Monin–Obukhov similarity theory (giving a logarithmic profile).
2. The surface physics package (skin temperature, fluxes, roughness length).
3. Terrain representation (which is usually *smoothed* compared to real terrain).

**Two interpolation methods, two different answers.** From the *same* model state with $T_{\text{lowest}} = 25$ °C and $T_{\text{skin}} = 30$ °C:
- **GFS curve** (M-O log profile, physically correct in the surface layer): $T_{2m} = 27.6$ °C.
- **Linear interpolation** (a simpler approximation): $T_{2m} = 29.8$ °C.

A **2 °C difference** from the same underlying model state. The model didn't change; only the diagnostic recipe did. **This is a real source of forecast disagreement between models.**

**Terrain smoothing compounds the problem.** The model elevation at a station might be 200 m higher than reality (e.g., in a valley the model can't resolve). The model assumes 200 m of "missing" altitude, gives you a temperature for the wrong elevation, and your forecast at that station is systematically biased *cold* or *warm* depending on how the smoothing went.

**Practical takeaway.** Take 2 m temperature, 10 m wind, and 2 m dew point with a grain of salt — they are *diagnostics*, not forecasts. If two models disagree, much of the disagreement may be in the *diagnosis* rather than the actual atmosphere.

## 24.9 Misconception #9 — "Improving the model improves Model Output Statistics"

**The intuition (wrong).** "If the underlying model gets better, the post-processed MOS forecasts will get better."

**The reality.** **MOS** (Model Output Statistics) is a statistical post-processor that maps model output to *observed* variables (temperature, dew point, precipitation probabilities, etc.) using regression equations *fit to a specific model version's biases*. If you change the model (a physics upgrade, a new dynamical core, a new resolution), you change the biases — and the MOS equations no longer apply.

**The dangerous regime.** If the new model is genuinely better but MOS hasn't been re-derived, the *new model + old MOS* can produce *worse* forecasts than the old model + old MOS. Operational forecasters experienced this firsthand whenever NWS upgraded the GFS — there's typically a transition period before MOS catches up.

**Why MOS even exists.** No model is unbiased everywhere. MOS calibrates: "When this model says $T_{2m} = 25$ °C in central Texas in July at 18 UTC, the *observed* temperature usually runs 2 °C cooler — so we'll subtract 2 °C from the raw output." That's exactly the kind of station-specific bias correction that makes MOS valuable. But the correction is only valid as long as the underlying model behaves the same way it did when the regression was fit.

**Practical takeaway.** When a new model version goes operational, *don't trust its MOS until the MOS has been re-derived from a long enough training period* — typically a year of parallel runs. Operational centers know this and plan accordingly, but downstream users sometimes don't.

## 24.10 Misconception #10 — "Full-resolution model output is always required"

**The intuition (wrong).** "If we don't see the model on its native grid, we lose valuable information."

**The reality.** Native-grid model output is often *much higher resolution than what most users actually need*. Bandwidth and storage constraints dictate that model data are typically interpolated to coarser output grids (and sometimes smoothed). The question is: how much information is actually lost?

**Concrete example.** A 12 km native model output is post-processed onto AWIPS grids of 20 km, 40 km, and 80 km:
- 20 km: shows mesoscale features (vorticity couplets near terrain, fine wind structure).
- 40 km: most mesoscale detail is smoothed out.
- 80 km: nearly featureless field; only synoptic-scale patterns visible.

For forecasting a synoptic-scale system, even the 80 km field has all the practically usable information. For mesoscale work (sea breezes, urban heat-island plumes, terrain-induced flows), the 80 km field is too coarse. **The right resolution depends on the application.**

**The case for coarsening.** A 12 km global field is about **64× as much data** as an 80 km field. Distributing the native-resolution data to thousands of users would consume enormous bandwidth — most of which would be wasted on detail the user can't act on. Coarsening is a sensible compromise.

**Practical takeaway.** Don't assume "more resolution = more usable info." Ask what spatial scale your decision actually depends on. If you're flagging severe-weather risk over a 200 km region, an 80 km grid is fine. If you're routing a flight through a thunderstorm complex, you need much higher.

## 24.11 The unifying lesson

Each misconception comes from imagining the model as a single black box that "predicts the weather." The reality is that **a model is a coupled system of dynamics, physics, surface, data assimilation, and post-processing.** Improving any single component does not automatically improve the forecast — sometimes it makes things worse if other components aren't updated alongside (e.g., MOS).

For a forecaster or model interpreter, the practical advice from these ten misconceptions distills to:
1. *Question every fine-resolution feature* — is it backed by data and physics, or just numerical detail?
2. *Don't trust feature size near the grid scale.* Effective resolution is much coarser than $\Delta x$.
3. *Look at surface fields* when something seems off near the ground.
4. *Don't expect the analysis to match obs.* It's a balanced blend, not a copy.
5. *Don't take convective rainfall numbers literally.* Use them as a "convection likely here" indicator.
6. *Synoptic skill ≠ convective skill.* Check the cumulus scheme behavior independently.
7. *Radiation has uncertainties even in clear sky.* And it's frozen between calls.
8. *2 m temperature and 10 m wind are diagnostics.* Different models compute them differently.
9. *MOS lags model upgrades.* Watch for a transition period.
10. *Match output resolution to your decision scale.* Don't fetishize native grids.

Above all: **understand the model as a system of trade-offs, not a magical predictor.** That mindset is what separates a master from a button-pusher.

---

<a id="25"></a>

# 25 Glossary of Every Symbol

| Symbol | Meaning | Where introduced |
|---|---|---|
| $t$ | time | §5 |
| $x, y, z$ | spatial coordinates | §5 |
| $\Delta t, \Delta x$ | time step, grid spacing | §9 |
| $\rho$ | air density | §6 |
| $p$ | pressure | §6 |
| $T$ | temperature | §6 |
| $\theta$ | potential temperature | §6.4 |
| $\theta_v$ | virtual potential temperature, $\theta(1+0.61q_v)$ | §6.5 |
| $q, q_v$ | specific humidity / water-vapor mixing ratio | §6 |
| $u, v, w$ | wind components in $x, y, z$ | §6 |
| $\vec V$ | wind vector $(u, v, w)$ | §5 |
| $\nabla$ | gradient operator | §5 |
| $\nabla^2$ | Laplacian | §5 |
| $g$ | gravitational acceleration ≈ 9.806 m/s² | §6 |
| $R_d$ | gas constant for dry air | §6 |
| $c_{pd}, c_{vd}$ | specific heats of dry air at constant $p$, $V$ | §6 |
| $\gamma$ | $c_{pd}/c_{vd}$, ratio of specific heats | §7 |
| $\pi$ | Exner function $(p/p_0)^{R_d/c_{pd}}$ | §6.5 |
| $f$ | Coriolis parameter | §7.5 |
| $\beta$ | $df/dy$, planetary vorticity gradient | §7.5 |
| $N$ | Brunt–Väisälä buoyancy frequency | §7.4 |
| $K, K_M, K_H$ | eddy diffusivity (momentum, heat) | §22.3 |
| $M$ | molecular diffusivity | §21 |
| $k$ | wavenumber $2\pi/L_x$ | §7 |
| $\omega$ | angular frequency $2\pi/P$ | §7 |
| $c$ | phase speed | §7 |
| $c_g$ | group velocity $\partial\omega/\partial k$ | §16 |
| $L_x, L_z$ | wavelength in $x$, $z$ | §7 |
| $A_k$ | amplification factor for wavenumber $k$ | §12 |
| $\mu$ | $c\Delta t/\Delta x$ for advection; $\omega\Delta t$ for oscillation | §11, §14 |
| $\nu$ | $M\Delta t/(\Delta x)^2$ for diffusion | §21 |
| Pe | Péclet number $cL/M$ (or $c\Delta x/M$ for grid Péclet) | §21.4 |
| Re | Reynolds number $UL/\nu$ | §21.4 |
| $u_*$ | friction velocity | §22.5 |
| $z_0$ | aerodynamic roughness length | §22.5 |
| $L$ | Obukhov length | §22.6 |
| $\zeta$ | $z/L$, Monin–Obukhov stability parameter | §22.6 |
| $\Phi_m, \Phi_h$ | M-O similarity functions | §22.6 |
| $\overline e$ | turbulent kinetic energy (TKE) | §22.7 |
| $\varepsilon$ | TKE dissipation rate | §22.7 |
| $w_*, \theta_*, q_*$ | convective scaling velocity, temperature, humidity | §22.8 |
| $z_i$ | PBL / mixed-layer depth | §22.8 |
| $\sigma, \rho, \beta$ (Lorenz) | Prandtl, Rayleigh, geometric factor | §3 |
| $H, H_L, H_G, R_N$ | sensible, latent, ground, net radiation flux | §23.3 |
| $a' = a - \overline a$ | turbulent fluctuation | §7 |
| $\overline{u'w'}, \overline{w'\theta'}, \overline{w'q'}$ | turbulent fluxes | §22.1 |

---

# Closing Remarks

If you've read this guide cover to cover, you now know:

- **Why** weather is fundamentally limited and climate is fundamentally predictable.
- **What** PDEs underlie atmospheric motion and what their characteristics carry.
- **How** finite differences turn a continuum equation into a marching algorithm, with concrete formulas for derivatives.
- **The four properties** every numerical scheme must have, and how to test for them.
- **Why CFL** is necessary but not sufficient, and **what amplification factors** tell you.
- **Why short waves are mishandled by every scheme** and how staggered grids and higher orders help.
- **Why nonlinear equations alias energy** and how to control it with artificial dissipation.
- **What the closure problem is** and how K-theory, M-O similarity, and TKE schemes try to fix it.
- **How parameterizations interact** with each other and with dynamics at every time step.
- **What to *not* trust about a model output** — the ten misconceptions are a first-line sanity check.

The recurring theme — and probably the deepest idea of the whole course — is this: **all numerical schemes are approximations**. Each one trades one kind of error (dissipation, dispersion, instability, computational modes) for another. The art is choosing the right trade-off for the problem, knowing how it can fail, and *reading the model output with that knowledge in mind*.

---

# Appendix A — Numerical Experiments Atlas

Each homework in this course is a direct numerical demonstration of a specific lecture concept. Treat this atlas as a "where to look in the homeworks for proof of each claim."

## A.1 HW1 — Rotating Cone (FTCS vs. CTCS)

**Setup.** Solid-body 2D rotational flow advecting an initial cone of height 1 around a 100×100 mesh, $\mu = 0.5 < 1$.

| Scheme | Result | Concept demonstrated |
|---|---|---|
| **FTCS** | Blows up at step 113. Cone replaced by oscillations, values from $-10.3$ to $+10.2$. | FTCS is unconditionally unstable for advection (§12.4, §18). CFL is *necessary but not sufficient*. |
| **CTCS after 1 rotation** | Peak: $1.000 \to 0.842$. Cone visibly broader. Small ripples at base. Negative undershoots ($\min q = -0.10$) at sharp gradient. | Leapfrog is neutral in amplitude (§14, §18.1) — the peak loss comes from *dispersion* (§16). Different wavelengths in the cone propagate at different numerical speeds. |
| **CTCS after 3 rotations** | Peak: $0.659$. Undershoots reach $-0.216$. | Errors *accumulate* with each revolution. Same diffusive-looking pattern but bigger magnitude. This is why long climate runs need high-order or spectral schemes. |

## A.2 HW2 — 1D Linear Advection $u_t + cu_x = 0$ with leapfrog

**Setup.** $u(x,0) = \sin(2\pi x)$ on cyclic $[0,1]$, $c = 1$, $T = 1/c = 1$ for one full period.

### Case 1 — Baseline ($\mu = 0.25$, $N = 16$, $\Delta t = 1/64$)

- Period verified at exactly **64 steps** (one full revolution).
- Amplitude tracked: oscillates around 1.0, peak $\approx 1.005$ — the **computational mode** (§15) excited by the Euler first step.
- Leapfrog itself is neutral within stability, so the wobble persists at constant tiny amplitude rather than damping.

### Case 2 — Vary $\mu$ at fixed $\Delta x = 1/16$

| $\mu$ | $\Delta t$ | Result |
|---|---|---|
| $0.5$ | $1/32$ | Stable; small phase lag (dispersion). |
| $1.0$ | $1/16$ | Stable; minimal phase error (waves move exactly one cell per step → "magic CFL," §18.2). Amplitude oscillation reaches $\sim 1.08$ — bigger Euler-first-step computational mode. |
| $2.0$ | $1/8$ | **Blows up** by $t = 0.5$ — confirms the CFL bound $|\mu| \leq 1$ for leapfrog + centered space. |

### Case 3 — Vary resolution at fixed $\mu = 0.8$

| $N$ | Pts/wavelength | Result |
|---|---|---|
| $32$ | $32$ | Nearly exact; tiny phase error. |
| $16$ | $16$ | Small but visible phase lag. |
| $8$ | $8$ | Clear phase lag; amplitude wobble peaks reach $\sim 1.20$ (Euler first step injects more comp. mode at coarse grid). |

**Lesson.** Resolution matters more than scheme order for advection — coarse grids make the same scheme behave much worse.

### Case 4 — Computational dispersion (sum of two waves)

- IC (i): $\cos(2\pi x) + \cos(4\pi x)$ — both wavelengths well-resolved ($\geq 8$ pts/wl) → minor dispersion, stays close to exact.
- IC (ii): $\cos(2\pi x) + \cos(12\pi x)$ — second has only ~2.67 pts/wl. By $t = 1$, the two components have **separated visibly** because the short component propagates much slower than the long one (it's near the $2\Delta x$ stationary limit).

**Lesson.** Numerical dispersion = different wavelengths travel at different numerical speeds. Effects are mild for well-resolved waves but devastating for poorly-resolved ones.

## A.3 HW3 — Time differencing on the oscillation equation

**Setup.** $d\psi/dt = i\omega\psi$, run for 30 steps with $\mu = \omega\Delta t \in \{0.196, 0.393, 0.785, 1.571\}$ (corresponding to $n = 32, 16, 8, 4$ steps per period).

| Scheme | Result | Concept |
|---|---|---|
| **Euler** | Always grows. $\mu=1.571$: $|A|=1.86$, blows up to $\sim 1.3\times 10^8$ in 30 steps. Even $\mu=0.196$: amplitude $\to 1.76$. | Euler is unconditionally unstable for waves (§14.3). |
| **Backward** | Always decays. $\mu=1.571$: drops to nearly zero in 8 steps. Higher $\mu$ → faster damping. | Implicit, unconditionally stable, intrinsically damping. Useful for damping out high-frequency garbage. |
| **Trapezoidal** | $|A| = 1$ exactly for all 4 $\mu$. Amplitude line stays *exactly* on 1.0. | Crank–Nicolson: 2nd-order, implicit, **always neutral**. |
| **Matsuno** | Stable for $\mu \leq 1$. Maximum damping at $\mu = 1/\sqrt{2} \approx 0.707$ where $|A| = 0.866$. At $\mu = 1.4$: blows up. | Conditionally stable, scale-selective damping (§14.4). |

## A.4 HW4 — von Neumann analysis of FTCS

**Plot.** $|A_k| = \sqrt{1 + \mu^2 \sin^2(k\Delta x)}$ vs. $k\Delta x$ for $\mu \in \{0.25, 0.5, 1.0, 2.0\}$. **Every curve sits above $|A_k| = 1$**, with peak at $k\Delta x = \pi/2$:

- $\mu=0.25$: peak $1.031$
- $\mu=0.5$: peak $1.118$
- $\mu=1.0$: peak $1.414$
- $\mu=2.0$: peak $2.236$

**Lesson.** No choice of $\mu$ saves FTCS. CFL satisfaction (e.g., $\mu = 0.25$) is irrelevant — the scheme grows for *every* $\mu \neq 0$. (See §12.4.)

## A.5 HW5 — Staggered vs. unstaggered grids

**Setup.** Linearized 1D shallow water, $c = 300$ m/s, $\Delta x = 100$ km.

### Part 1 — Numerical phase speeds (true = 300 m/s)

| Wavelength | Unstaggered | Staggered |
|---|---|---|
| $200$ km ($2\Delta x$) | **$0.00$** | $195.4$ |
| $800$ km ($8\Delta x$) | $270.8$ | $293.3$ |
| $1200$ km | $286.9$ | $297.0$ |
| $2000$ km | $295.2$ | $298.9$ |

Staggered wins at every wavelength.

### Part 2 — Sub-grid decoupling

Place a unit point disturbance at $j = 50$ (even index) on each grid; run 6 hours.

- **Unstaggered:** disturbance only ever reaches **even-indexed points**. Odd points stay exactly zero. The grid has split into two non-talking sub-grids.
- **Staggered:** disturbance spreads smoothly to all neighbors.

This is the cleanest possible visual proof of why centered differences on a co-located grid are pathological.

### Part 3 — Sine wave advection

- Unstaggered: visible phase lag, slower than exact.
- Staggered: closely tracks exact solution. Smaller initial-step error too (because of smaller required $\Delta t$).

## A.6 HW6 — Nonlinear instability in Burgers's equation

**Setup.** $u_t + uu_x = 0$ on a 20-point periodic grid with leapfrog + centered space, **no artificial diffusion**.

| Case | IC | $\Delta t$ | Result |
|---|---|---|---|
| (a) | $1 + \sin 2\pi x$ | $\Delta x/10$ | $\max|u|$: $2.00 \to 6.84$ over 100 steps. Wild grid-scale spikes by step 100. |
| (b) | same | $\Delta x/100$ (10× smaller) | $\max|u|$: $2.00 \to 4.70$ over 500 steps. **Same physical time as (a) at step 50, same value.** |
| (c) | $2 + \sin 2\pi x + \sin 4\pi x$ | $\Delta x/10$ | $\max|u|$: $3.76 \to 6.88$ — instability arrives earlier. |
| (d) | $3 + \sin 2\pi x + \sin 4\pi x + \sin 6\pi x$ | $\Delta x/10$ | $\max|u|$ peaks at $11.59$ at step 85 — most chaotic. |

**Lesson** (the most important from the entire course):

1. The instability is driven by **spatial aliasing**, not CFL. Reducing $\Delta t$ stretches the instability over more steps but does not prevent it.
2. The number of **interaction pairs** controls the cascade rate: 1 wave → 1 pair, 2 waves → 4 pairs, 3 waves → 9 pairs. More waves = faster instability.
3. The cure is **scale-selective spatial dissipation** or filters — adding viscosity in the right places, not making time steps smaller.

---

# Appendix B — Master Cheat Sheet

If you remember nothing else from this course, remember this list.

## B.1 Equations to know cold

| Equation | Form | Use |
|---|---|---|
| Material derivative | $\dfrac{d}{dt} = \dfrac{\partial}{\partial t} + \vec V\cdot\nabla$ | Connects Lagrangian ↔ Eulerian |
| Hydrostatic balance | $\dfrac{dp}{dz} = -\rho g$ | Vertical balance for large-scale flow |
| Potential temperature | $\theta = T(p_0/p)^{R_d/c_{pd}}$ | Conserved in dry adiabatic motion |
| Continuity (Lagrangian) | $\dfrac{d\rho}{dt} + \rho\nabla\cdot\vec V = 0$ | Mass conservation |
| Anelastic continuity | $\nabla\cdot(\rho_0\vec V) = 0$ | Filters sound waves |
| Linear advection | $\dfrac{\partial \psi}{\partial t} + c\dfrac{\partial \psi}{\partial x} = 0$ | Workhorse test problem |
| Pure diffusion | $\dfrac{\partial \psi}{\partial t} = M\dfrac{\partial^2 \psi}{\partial x^2}$ | Parabolic, smoothing |
| Oscillation equation | $\dfrac{d\psi}{dt} = i\omega\psi$ | Test problem for time schemes |
| General prognostic | $\dfrac{\partial \psi}{\partial t} = -\vec V\cdot\nabla\psi + \nabla^2(K\psi) + S$ | Master equation |

## B.2 Dimensionless numbers

| Number | Definition | Meaning |
|---|---|---|
| CFL / Courant | $\mu = c\Delta t/\Delta x$ | Advection stability bound |
| Diffusion | $\nu = M\Delta t/\Delta x^2$ | Explicit diffusion stability bound |
| Péclet | $\text{Pe} = cL/M$ | Advection vs. diffusion |
| Reynolds | $\text{Re} = UL/\nu$ | Turbulent vs. viscous |
| Rossby | $\text{Ro} = U/(fL)$ | Inertial vs. Coriolis |
| Brunt–Väisälä | $N = \sqrt{g\,d\ln\bar\theta/dz}$ | Gravity-wave frequency |
| Obukhov | $L = -u_*^3/[k(g/T_0)(H_0/\rho c_p)]$ | Surface-layer stability scale |

## B.3 Stability conditions at a glance

| Scheme | Condition | Notes |
|---|---|---|
| Upstream advection | $0 \leq \mu \leq 1$ | Stable, dissipative |
| Leapfrog + centered (CTCS) | $|\mu| \leq 1$ | Stable, dispersive |
| **FTCS for advection** | **None — always unstable** | Unconditional |
| Forward time + centered diffusion | $\nu \leq 1/2$ | Very restrictive |
| Crank–Nicolson diffusion | None — unconditionally stable | Implicit cost |
| Euler for oscillation | None — always unstable | Never use for waves |
| Backward for oscillation | None — unconditionally stable, damping | |
| Trapezoidal for oscillation | None — unconditionally neutral | |
| Matsuno for oscillation | $|\mu| \leq 1$ | Damps with max at $\mu = 1/\sqrt{2}$ |
| Heun for oscillation | None — weakly unstable | $|A| = 1 + \mu^4/8 + \cdots$ |
| C-grid (staggered) shallow water | $\mu \leq 1/2$ | Half the unstaggered limit |

## B.4 The big theorems

- **Lax Equivalence Theorem** (linear, well-posed IVPs): $\text{Consistency} + \text{Stability} \iff \text{Convergence}$.
- **CFL physical interpretation**: Numerical domain of dependence ⊇ physical domain of dependence.
- **CFL is necessary but not sufficient**: FTCS is the textbook example.

## B.5 Phase and amplitude error rules of thumb

- **Even-order centered space** → dispersive (phase error), no amplitude error.
- **Odd-order upstream space** → dissipative (amplitude error), with dispersion as secondary.
- **2nd-order centered**: $2\Delta x$ wave is *stationary*; long-wave phase error $\sim (k\Delta x)^2/6$.
- **4th-order centered**: long-wave phase error $\sim (k\Delta x)^4/30$.
- **8–10 grid points per wavelength** = "well-resolved."
- **Effective resolution** of a typical model is ~$8\Delta x$, not $2\Delta x$.

## B.6 Computational mode of leapfrog

- 3-level scheme produces TWO solutions: physical mode + computational mode.
- Computational mode flips sign every step (period $4\Delta t$), zig-zag pattern.
- **Cures**: Euler first step (limits seeding), occasional 2-level steps, **Robert–Asselin filter** $\phi^n_{\text{filt}} = \phi^n + \gamma(\phi^{n-1} - 2\phi^n + \phi^{n+1})$ with $\gamma \approx 0.05$–$0.1$.

## B.7 Aliasing and nonlinear instability

- Maximum resolvable wavenumber: $k_{\max} = \pi/\Delta x$ ($\lambda = 2\Delta x$).
- A wave with $k > k_{\max}$ aliases to $k^* = 2k_{\max} - k$ — reflection across $k_{\max}$.
- Nonlinear terms create shorter waves; when they exceed $k_{\max}$ they alias *back* and accumulate.
- **Cures**: artificial diffusion, scale-selective filters, upstream-biased schemes.
- **Reducing $\Delta t$ does NOT cure nonlinear instability** (HW6).

## B.8 Sound-wave filtering

- Sound: $c_s \sim 350$ m/s — fastest mode, weather-irrelevant, forces tiny CFL.
- Anelastic $\nabla\cdot(\rho_0\vec V) = 0$ filters them while preserving deep flow.
- QG / hydrostatic filters more drastic, used at synoptic scales.

## B.9 Staggered grids

- **Arakawa C-grid**: $u$ at integer points, $h$ at half-integer.
- **Pros**: better short-wave dispersion, no sub-grid decoupling, $c_g \geq 0$ always.
- **Cons**: smaller stable $\Delta t$ ($\mu \leq 1/2$), more bookkeeping.

## B.10 PBL & turbulence

- Reynolds averaging: $a = \bar a + a'$, $\overline{a'b'} \neq 0$ (turbulent fluxes).
- **Closure problem**: more unknowns than equations at every order.
- K-theory: $\overline{w'\theta'} = -K_H\partial\bar\theta/\partial z$, etc. Works for small eddies.
- TKE budget: storage = buoyancy + shear + transport + pressure − dissipation.
- Surface log-profile: $U(z) = (u_*/k)\ln(z/z_0)$, $k = 0.4$.
- **Monin–Obukhov**: surface-layer profiles $\Phi_m(z/L), \Phi_h(z/L)$.

## B.11 Parameterization workflow

- Split: $\partial \psi/\partial t = D\psi + P\psi$.
- $P\psi = R + VD + GWD + C + LSP$.
- Leapfrog cannot integrate $P\psi$ (parabolic) — use forward or implicit.
- **Radiation**: SW + LW, called every 10 min – several hours; surface energy balance every step.
- **Microphysics**: grid-scale, every step, 6-class water phase (Lin et al. 1983).
- **Cumulus**: sub-grid, every 10 min – hours, **releases instability** (precipitation is by-product).
- **Large-scale precipitation**: instantaneous saturation adjustment, applied last.
- **Order matters** when implicit schemes are involved — couple interacting processes.

---

# Appendix C — Closing Thoughts: Nine Threads to Tie Together

The threads that should now connect in your head after reading this guide:

1. **The atmosphere is governed by PDEs.** Hyperbolic (advection, waves) and parabolic (diffusion) types dominate; both must be discretized.

2. **Discretization introduces error with structure.** Numerical diffusion (wrong amplitude), numerical dispersion (wrong phase speed), aliasing (energy misplaced in wavenumber space), computational modes (spurious solutions) — each one comes from a specific choice you made about the scheme.

3. **The CFL condition links physical and numerical speeds.** The grid must be able to "see" the wave; otherwise the scheme blows up. But CFL alone is not enough — you must also Von Neumann–analyze the scheme.

4. **Higher-order schemes are not always better.** They give better accuracy on smooth solutions, but they're more expensive, sometimes more dispersive at the grid scale, and require careful filter design to handle nonlinear instability.

5. **Staggered grids are usually worth it.** They handle the worst-resolved waves much better than collocated grids — at the cost of a smaller stable $\Delta t$.

6. **Turbulence is the hardest problem.** It can never be fully resolved, must be parameterized, and the closure is approximate. Modern progress (LES, TKE-based schemes, ML-augmented closures) is incremental.

7. **A real model is a system.** The dynamical core, the physics, the surface, the data assimilation, and the post-processing are all coupled. Improving one without the others rarely improves the forecast — that's the unifying lesson of the ten misconceptions.

8. **Chaos is the fundamental limit on weather forecasting**, but **climate is statistically tractable** because the attractor's shape is robust even when its trajectory is unpredictable.

9. **Every numerical choice is a trade-off**: accuracy vs. cost, stability vs. accuracy, simplicity vs. realism, dispersive vs. dissipative leading errors. **Knowing what trade-off you're making is the difference between blindly running a model and actually understanding it.**

The homeworks give you direct experience with all of this — every theoretical claim in the lecture notes maps to a graph or a numerical experiment in HW1–HW6. When you're stuck, go back to the homework that demonstrated the relevant phenomenon and re-walk through the discussion: it's a much better way to ground the theory than re-reading abstract slides.

Good luck.
