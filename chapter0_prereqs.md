# 0. Mathematical and Physical Prerequisites

> This chapter is for the reader who has heard of calculus but is not fluent in it, and who knows almost nothing about atmospheric physics. Every notation that appears later in the guide is defined here. Every equation comes with a "what this is saying" paragraph. Several interactive widgets let you change values and see the math respond in real time. If you already know this material, skim and move on; if not, read this chapter slowly and come back to it whenever a symbol later in the guide is unfamiliar.

> **Companion resource — the lecture dashboards.** Alongside this chapter, the course has a set of per-lecture interactive dashboards. The most useful one for the prerequisite material here is the **Lecture 3** dashboard (basic math toolkit — Taylor series, mean-value theorem, derivative, Eulerian vs Lagrangian, hydrostatic balance, potential temperature, Exner function, continuity equation, advection–diffusion). The **Lecture 4** dashboard covers wave families. The **Lecture 5** dashboard has the rigorous CFL and von-Neumann walkthroughs. They are embedded below at the relevant sections so you can keep one tab open and tab between widget and dashboard as you read.

## 0.1 How to read mathematical notation

A **variable** is just a letter that stands for a number — a placeholder. When we write $x = 5$ we are saying "the letter $x$ represents the number five". The whole point of using letters is so that we can write rules that are true for any number, not just five.

**Subscripts and superscripts.** When a letter has a small number written below it (a subscript) or above it (a superscript), the small number is almost always a *label*, not an exponent. Examples:

- $T_j$ — temperature in cell $j$. The $j$ is an index that tells you which cell.
- $T_j^n$ — temperature in cell $j$ at time level $n$. Two labels: a space label and a time label. The $n$ is NOT an exponent — $T_j^n$ is not $T_j$ raised to the power $n$.
- $T_s^0$ — surface temperature at depth zero. The "0" labels the depth, not a power.
- $(T_s^0)^4$ — the surface temperature *raised to the fourth power*. When the exponent really is an exponent, it comes outside parentheses to remove the ambiguity.

**Greek letters** appear everywhere in atmospheric science. Whenever you see one, treat it as just another variable name. A reference table:

| Symbol | Name (pronunciation) | Typical use in this guide |
|---|---|---|
| $\alpha$ | alpha | Implicitness weight in θ-method; albedo (with subscript) |
| $\beta$ | beta | Bowen ratio; coefficient in stability analysis |
| $\gamma$ | gamma | Lapse rate; specific-heat ratio $c_p/c_v$ |
| $\Gamma$ | capital gamma | Dry adiabatic lapse rate |
| $\delta$ | delta (small) | Small change, error term |
| $\Delta$ | capital delta | A finite (not infinitesimal) change. $\Delta t$ = time step, $\Delta x$ = grid spacing |
| $\varepsilon$ | epsilon | Emissivity; small positive parameter |
| $\zeta$ | zeta | Monin–Obukhov dimensionless height $z/L$ |
| $\eta$ | eta | Learning rate; coordinate transform variable |
| $\theta$ | theta | Potential temperature; phase angle; implicitness weight |
| $\kappa$ | kappa | Thermal diffusivity $\lambda/C$ |
| $\lambda$ | lambda | Thermal conductivity; wavelength |
| $\mu$ | mu | Substrate admittance $\sqrt{\lambda C}$; viscosity |
| $\nu$ | nu | Diffusion number $\kappa\Delta t/\Delta z^{2}$; kinematic viscosity |
| $\pi$ | pi | The constant 3.14159…; Exner function |
| $\rho$ | rho | Density |
| $\sigma$ | sigma | Stefan–Boltzmann constant |
| $\tau$ | tau | Time scale; stress |
| $\phi$ | phi (Greek "ph") | Generic scalar field; numerical approximation |
| $\Phi$ | capital phi | Universal stability functions in M-O theory |
| $\psi$ | psi | True solution of a PDE |
| $\omega$ | omega | Angular frequency $2\pi/T$; vertical velocity in pressure coordinates |
| $\Omega$ | capital omega | Earth's rotation rate; vorticity |

Function notation $f(x)$ means "the function $f$ evaluated at the input $x$". So $\sin(2\pi)$ means "evaluate the sine function at $2\pi$", which is $0$. The parentheses around the argument do not mean multiplication.

## 0.2 Functions of one variable

A function is a rule that takes an input and gives back an output. We write it $y = f(x)$ and read it "y equals f of x". The four functions that appear most often in this guide:

**Sine and cosine.** $\sin(x)$ and $\cos(x)$ both produce numbers between $-1$ and $+1$ that oscillate as $x$ increases. Both repeat every $2\pi \approx 6.28$ units. Cosine starts at $1$ when $x = 0$; sine starts at $0$. Their derivatives are tied to each other: $\frac{d}{dx}\sin x = \cos x$ and $\frac{d}{dx}\cos x = -\sin x$. Whenever we write something like "$T(t) = \cos(\omega t)$", we mean "a quantity $T$ that oscillates in time with angular frequency $\omega$".

**The exponential function** $e^x$. $e \approx 2.71828$ is a fixed number — like $\pi$ — that shows up everywhere in nature. Its defining property: the slope of $e^x$ at any point equals the value of $e^x$ at that point. Whenever a process grows or decays at a rate proportional to its current size, $e^x$ shows up. Radioactive decay, compound interest, the damping of a thermal wave with depth — all use $e^{-z/d}$ form.

**The logarithm** $\ln(x)$. Inverse of $e^x$. If $e^a = b$, then $\ln(b) = a$. We use it when we want to convert exponential growth or decay into a straight line.

**Power laws** $x^n$. $x^2$ is "x squared", $x^3$ is "x cubed", etc. In numerical analysis we talk about "first-order error" ($\propto \Delta t^1$), "second-order error" ($\propto \Delta t^2$), and so on. A second-order method's error shrinks four times faster than a first-order method's when $\Delta t$ halves.

## 0.3 Derivatives — rate of change

If $y = f(x)$, the **derivative** $\frac{df}{dx}$ (read "d-f-d-x") is the rate at which $y$ changes when $x$ changes — the slope of the curve. Equivalent notations: $f'(x)$, $\dot{f}$ (when $x$ is time), $\frac{dy}{dx}$.

Plain-English reading: "if I bump $x$ up by a small amount, how much does $y$ go up by?" Slope, in other words.

**Why we care.** All physics equations are statements about rates. Newton's $F = ma$ says the rate of change of velocity is proportional to force. Heat conduction says the rate of change of temperature is proportional to the curvature of temperature in space. To write any rate-of-change law down, we need derivatives.

<!--WIDGET:derivative_tangent-->

The interactive widget above lets you slide a point along a curve and watch the tangent-line slope change. The slope of the tangent IS the derivative at that point.

## 0.4 Partial derivatives — when there is more than one variable

If a quantity depends on two variables — say temperature depends on both depth $z$ and time $t$ — we need to say *which* variable we are taking the derivative with respect to. We write $\frac{\partial T}{\partial t}$ (read "partial T over partial t") to mean "the rate of change of $T$ with respect to $t$, holding $z$ fixed". The curly $\partial$ symbol is just a way to remind ourselves that $T$ depends on something else too.

**Reading the heat equation $\frac{\partial T}{\partial t} = \kappa \frac{\partial^{2} T}{\partial z^{2}}$.** Plain English: "at every point in space and at every moment in time, the rate at which the temperature is changing in time equals $\kappa$ times the spatial curvature of $T$." The factor $\kappa$ controls how fast temperature responds; the spatial curvature $\partial^{2} T/\partial z^{2}$ is what drives the change. If $T$ is concave up in $z$ (a valley), it rises in time; if concave down (a hill), it falls.

<!--WIDGET:partial_deriv_slicer-->

The widget above lets you take horizontal and vertical slices through a 2-D temperature field $T(x, t)$. The orange slice (fixed $t$) shows $T$ as a function of $x$; its slope at the cursor is $\partial T/\partial x$. The purple slice (fixed $x$) shows $T$ as a function of $t$; its slope is $\partial T/\partial t$. Both slopes are evaluated *at the same physical point* — they are different numbers because they measure change along different axes.

## 0.5 Integrals — accumulation

If a derivative is a rate, an **integral** is a total accumulation. We write $\int_a^b f(x)\,dx$ and read it "the integral of f of x from a to b". Geometrically, it is the area under the curve $y = f(x)$ between $x = a$ and $x = b$.

**Why we care.** If $G(t)$ is the rate at which heat is flowing into the ground at time $t$, then the **total** heat that has flowed in between time $a$ and time $b$ is $\int_a^b G(t)\,dt$. That is the daily storage integral $S = \int G\,dt$ over 24 hours that appears in the project report.

**The fundamental theorem of calculus** says derivatives and integrals are inverses of each other. If you differentiate $\int_a^x f(s)\,ds$ with respect to $x$, you get back $f(x)$. So the integral is just "anti-derivative".

## 0.6 Complex numbers and Euler's formula

The **imaginary unit** $i$ is defined by $i^2 = -1$. It is not a "real" number — no real number's square is negative — but it turns out to be enormously useful as a bookkeeping device for waves.

A **complex number** is a sum of a real and imaginary part: $z = a + bi$. We can plot it as a point in the plane with $a$ on the horizontal axis (real part) and $b$ on the vertical (imaginary part). Every complex number can also be written in polar form: $z = r\,e^{i\theta}$ where $r$ is the distance from the origin and $\theta$ is the angle from the positive real axis.

**Euler's formula** ties everything together:

$$e^{i\theta} = \cos\theta + i\sin\theta.$$

**Reading this equation.** The left side is a complex exponential — an abstract symbol. The right side is a concrete pair: cosine in the real part, sine in the imaginary part. Together they say: as $\theta$ increases, $e^{i\theta}$ traces a unit circle in the complex plane, with horizontal coordinate $\cos\theta$ and vertical coordinate $\sin\theta$. Why does this matter? Because waves are sums of sines and cosines, and a complex exponential carries both at once — clean and compact.

<!--WIDGET:euler_unit_circle-->

The interactive widget shows a point moving around the unit circle. The horizontal projection (real part) traces $\cos\theta$; the vertical projection (imaginary part) traces $\sin\theta$. As $\theta$ runs from $0$ to $2\pi$, both side panels plot full sinusoids.

## 0.7 Sine waves — amplitude, wavenumber, frequency

A sine wave that depends on both space and time can be written

$$\phi(x, t) = A\,\sin(kx - \omega t).$$

**Reading this equation.**

- $\phi(x, t)$ — some quantity (could be air pressure, surface elevation, temperature anomaly) at position $x$ and time $t$.
- $A$ — the **amplitude**, the peak height of the wave.
- $k$ — the **wavenumber** (rad/m). It controls how tightly packed the wave is in space.
- $\omega$ — the **angular frequency** (rad/s). It controls how fast the wave oscillates in time.
- The combination $(kx - \omega t)$ is the **phase**. As $t$ increases, points of constant phase satisfy $x = (\omega/k)\,t$, so the wave moves to the right at speed $c = \omega/k$.

The **wavelength** is $\lambda = 2\pi/k$ — the distance over which the wave completes one full cycle. The **period** is $T = 2\pi/\omega$ — the time for one full cycle at a fixed point.

<!--WIDGET:sine_explorer-->

Drag the amplitude, wavenumber, and angular frequency sliders and watch the wave respond. Notice that increasing $k$ packs more cycles into the same space (shorter wavelength), and increasing $\omega$ runs the wave faster.

## 0.8 What $k\Delta z$ means — the dimensionless wavenumber on a grid

When we discretise space into cells of size $\Delta z$, only some wavelengths "fit" on the grid. A wavelength $\lambda = 2\pi/k$ takes about $\lambda/\Delta z = 2\pi/(k\Delta z)$ grid cells to complete one cycle. The dimensionless number $k\Delta z$ tells us *how many radians of the wave fall in one grid cell*.

- $k\Delta z = 0$ means $\lambda \to \infty$ — a constant in space (no variation).
- $k\Delta z = \pi/2$ means $\lambda = 4\Delta z$ — four cells per cycle.
- $k\Delta z = \pi$ means $\lambda = 2\Delta z$ — the shortest pattern the grid can hold: temperature flips sign at every cell. This is called the "$2\Delta z$ wave" and it is the worst case for stability analysis.

Wavenumbers above $k\Delta z = \pi$ cannot be represented on the grid — they get **aliased** into longer-wavelength patterns (Lecture 8 explains this in detail). So all of stability analysis happens in the range $k\Delta z \in [0, \pi]$.

<!--WIDGET:kdz_grid-->

Drag the $k\Delta z$ slider to see how the wave looks on a grid of fixed $\Delta z$. At $k\Delta z = \pi$, adjacent cells take opposite signs — the worst-case pattern that von Neumann analysis tests.

## 0.9 Time steps and discretisation

In a continuous mathematical model, time $t$ varies smoothly. In a computer model, we cannot store infinitely many time levels, so we sample time at discrete points $t_0 = 0$, $t_1 = \Delta t$, $t_2 = 2\Delta t$, …, $t_n = n\Delta t$. The integer $n$ is the **time-level index**; $\Delta t$ is the **time step**.

We write $\phi^n$ to mean "the numerical approximation to $\phi$ at time $t_n = n\Delta t$". The superscript is a label (not an exponent). Whenever you see $\phi^{n+1}$, read it as "$\phi$ one time step later".

**Discrete derivatives.** With this notation, the continuous time derivative $\frac{d\phi}{dt}$ becomes the **forward difference**

$$\frac{d\phi}{dt} \approx \frac{\phi^{n+1} - \phi^{n}}{\Delta t}.$$

This is the simplest finite-difference approximation. It introduces an error of order $\Delta t$ (first-order accuracy), which we call **truncation error**.

<!--WIDGET:time_step-->

The widget shows a continuous time axis sampled at $n = 0, 1, 2, \ldots$, with $\Delta t$ as the spacing. Drag $\Delta t$ to see how the discrete samples spread out or compress.

**Forward, backward, centred differences.** Three different ways to approximate the *same* derivative from grid values:

- **Forward**: $(\phi^{n+1}-\phi^{n})/\Delta t$ — uses information from the future. First-order accurate ($O(\Delta t)$).
- **Backward**: $(\phi^{n}-\phi^{n-1})/\Delta t$ — uses past information. Also $O(\Delta t)$.
- **Centred**: $(\phi^{n+1}-\phi^{n-1})/(2\Delta t)$ — symmetric, much more accurate: $O(\Delta t^{2})$.

Centred differences are nominally "better" but introduce a famous problem — the leapfrog **computational mode** — which Chapter 15 of this guide explains in detail. For now, the takeaway: how you discretise time matters as much as the time-step size itself.

For an interactive walkthrough of finite differences and their order-of-accuracy properties, the Lecture 6 dashboard has tabs for forward/backward/centred difference operators, their truncation errors, and a side-by-side comparison:

<iframe src="lecture6_dashboard_Claude_Code.html" style="width:100%;height:820px;border:1px solid #cbd5e1;border-radius:8px;background:#fff" loading="lazy" title="Lecture 6 dashboard — finite differences"></iframe>

## 0.10 Fourier basics — every function as a sum of sines

A remarkable mathematical fact: any reasonable function defined on an interval can be written as an infinite sum of sines and cosines:

$$f(x) = \sum_{k} \bigl[a_k\,\cos(kx) + b_k\,\sin(kx)\bigr].$$

The coefficients $a_k$ and $b_k$ are the **Fourier coefficients** — they tell us how much of each wavelength is in $f$. The full set $\{a_k, b_k\}$ as a function of $k$ is the **Fourier spectrum** of $f$.

**Why we care.** Numerical schemes are linear, so they act on each Fourier component independently. To check whether a scheme is stable, we only have to check whether any *single* Fourier component grows — this is what von Neumann analysis does (Section 0.13 and Lecture 5).

<!--WIDGET:fourier_square-->

The widget builds up a square wave from its Fourier components. Slide the "number of harmonics" to add more terms. With just a few terms you get a wavy approximation; with many terms it converges to a sharp square. (The little overshoots that never go away are called the Gibbs phenomenon.)

## 0.11 Vector calculus — gradient, divergence, curl, Laplacian

So far we have talked about scalar fields (single number at every point, like temperature). Many quantities in fluid mechanics are **vector fields** — three numbers at every point. The wind vector $\vec{V} = (u, v, w)$ has horizontal components $u, v$ and vertical component $w$.

The **del operator** $\nabla$ (read "del" or "nabla") is a shorthand for "take partial derivatives in all three spatial directions and assemble them as a vector":

$$\nabla \;=\; \biggl(\frac{\partial}{\partial x},\, \frac{\partial}{\partial y},\, \frac{\partial}{\partial z}\biggr).$$

By itself $\nabla$ is not a number — it is an operator waiting for something to act on. Four common uses:

### Gradient: $\nabla f$ (operator acting on a scalar)

If $f(x, y, z)$ is a scalar field (one number at every point), then

$$\nabla f \;=\; \biggl(\frac{\partial f}{\partial x},\, \frac{\partial f}{\partial y},\, \frac{\partial f}{\partial z}\biggr).$$

**Reading this.** $\nabla f$ is a vector at every point that points in the direction of steepest increase of $f$. Its magnitude $|\nabla f|$ is the steepness — how fast $f$ rises in that direction. On a topographic map, the gradient of altitude points uphill, and its size measures the slope.

**In atmospheric physics**, the pressure-gradient force is $-\frac{1}{\rho}\nabla p$ — air accelerates from high pressure toward low pressure, with force proportional to how steeply pressure drops.

<!--WIDGET:gradient_field-->

The widget above shows a Gaussian "hill" $f(x, y)$ (light = low, blue = high). At each grid node an orange arrow points in the direction of $\nabla f$ — uphill — and its length shows the steepness $|\nabla f|$. Notice that near the peak the arrows are short (locally flat); on the slopes they are long. The arrows always point *away from* low values and *into* high values. Drag the peak position and watch the whole gradient field reorganise.

### Divergence: $\nabla \cdot \vec{V}$ (operator acting on a vector, dot product)

If $\vec{V} = (u, v, w)$ is a vector field,

$$\nabla \cdot \vec{V} \;=\; \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} + \frac{\partial w}{\partial z}.$$

**Reading this.** $\nabla \cdot \vec{V}$ is a scalar at every point. Where it is **positive**, the vector field is *expanding* outward — think a "source" or air flowing away from a high-pressure point. Where it is **negative**, the field is *converging* inward — think a "sink" or air flowing toward low pressure. Where it is **zero**, mass is conserved at that point.

**In atmospheric physics**, the continuity equation $\frac{\partial \rho}{\partial t} + \nabla\cdot(\rho \vec{V}) = 0$ says density changes at a point only if more mass flows in than out. For the (approximately) incompressible atmosphere, $\nabla \cdot \vec{V} \approx 0$ — the wind field has no net divergence.

<!--WIDGET:divergence_field-->

### Curl: $\nabla \times \vec{V}$ (operator acting on a vector, cross product)

If $\vec{V} = (u, v, w)$,

$$\nabla \times \vec{V} \;=\; \biggl(\frac{\partial w}{\partial y} - \frac{\partial v}{\partial z},\; \frac{\partial u}{\partial z} - \frac{\partial w}{\partial x},\; \frac{\partial v}{\partial x} - \frac{\partial u}{\partial y}\biggr).$$

**Reading this.** $\nabla \times \vec{V}$ is a vector at every point that measures the *rotation* of the field. A small paddle wheel placed in the flow would spin around the axis of the curl, at a rate proportional to the curl's magnitude. If $\nabla \times \vec{V} = 0$ everywhere, the field is "irrotational" — no swirling.

**In atmospheric physics**, the vertical component $\zeta = \partial v/\partial x - \partial u/\partial y$ of the curl is called **vorticity**. Cyclones have positive vorticity in the Northern Hemisphere (counter-clockwise rotation), anticyclones have negative.

<!--WIDGET:curl_field-->

### Laplacian: $\nabla^{2} f = \nabla \cdot (\nabla f)$ (second-order operator on a scalar)

$$\nabla^{2} f \;=\; \frac{\partial^{2} f}{\partial x^{2}} + \frac{\partial^{2} f}{\partial y^{2}} + \frac{\partial^{2} f}{\partial z^{2}}.$$

**Reading this.** $\nabla^{2} f$ measures how much $f$ at a point differs from the average of its neighbours. Positive Laplacian means the point is a local minimum (a valley); negative Laplacian means a local maximum (a hill); zero means it equals the neighbourhood average.

**In atmospheric physics**, the diffusion term in the heat equation is $\kappa \nabla^{2} T$ — heat flows from hot peaks to cold valleys at a rate proportional to the curvature. The Laplacian is the multi-dimensional version of the second derivative $\partial^{2}/\partial z^{2}$ we already met in Section 0.4.

### The dot product and cross product as standalone operations

Beyond their use with $\nabla$, the dot product $\vec{A} \cdot \vec{B} = A_x B_x + A_y B_y + A_z B_z$ produces a scalar; geometrically it is $|\vec{A}||\vec{B}|\cos\theta$ where $\theta$ is the angle between the vectors. So a dot product of two perpendicular vectors is zero. The cross product $\vec{A} \times \vec{B}$ produces a vector perpendicular to both inputs, with magnitude $|\vec{A}||\vec{B}|\sin\theta$. In atmospheric dynamics, the Coriolis force is written $-2\vec{\Omega} \times \vec{V}$, where $\vec{\Omega}$ is the Earth's rotation vector and $\vec{V}$ is the wind. The cross product is what makes the Coriolis force always perpendicular to the wind.

<!--WIDGET:cross_product-->

The widget above shows two vectors $\vec{A}$ (orange) and $\vec{B}$ (purple) in the page, separated by angle $\theta$. The shaded parallelogram is the geometric object whose area equals $|\vec{A}\times\vec{B}|$. The result vector itself is perpendicular to the page — drawn with a cross symbol because it points into the screen for $\theta > 0$ in this configuration. Drag $\theta$ to $0$ (parallel vectors) and the cross product vanishes; drag to $90°$ and the magnitude is maximum at $|\vec{A}||\vec{B}|$. This is exactly what produces the Coriolis turning of the wind: $-2\vec{\Omega}\times\vec{V}$ is largest when wind and rotation axis are perpendicular (mid-latitudes) and vanishes at the poles where they are parallel.

### Composite operators — the Laplacian inside a flux divergence

The diffusion term you will see repeatedly in this guide is sometimes written as $\nabla\cdot(\kappa\nabla T)$ instead of $\kappa\nabla^{2}T$. When $\kappa$ is constant the two are identical: $\nabla\cdot(\kappa\nabla T) = \kappa\nabla\cdot\nabla T = \kappa\nabla^{2}T$. When $\kappa$ varies in space (different materials in stacked layers, for example), the flux-divergence form $\nabla\cdot(\kappa\nabla T)$ is correct and the simpler $\kappa\nabla^{2}T$ is not — that distinction matters for the layered-substrate version of the project's heat equation.

### Material derivative — $D/Dt$ as gradient + time

The **material derivative** combines the time derivative and the gradient into one operator that "rides along with the flow":

$$\frac{D}{Dt} \;=\; \frac{\partial}{\partial t} + \vec{V}\cdot\nabla.$$

**Reading this.** $\partial/\partial t$ measures change at a fixed point. $\vec{V}\cdot\nabla$ measures change due to the flow carrying the parcel through a spatially varying field. Adding them gives the total rate of change experienced by an air parcel as it moves. Chapter 5 of this guide uses this constantly to switch between Eulerian and Lagrangian views.

## 0.12 Ordinary and partial differential equations

A **differential equation** is an equation that contains derivatives. We classify them by which derivatives appear:

- **Ordinary differential equation (ODE)**: only one independent variable, usually $t$. Example: Newton's law of cooling $\frac{dT}{dt} = -k(T - T_\infty)$. The unknown $T$ is a function of $t$ alone. Given an **initial condition** $T(0) = T_0$, the future $T(t)$ is determined.

- **Partial differential equation (PDE)**: more than one independent variable. Example: the heat equation $\frac{\partial T}{\partial t} = \kappa \frac{\partial^{2} T}{\partial z^{2}}$. The unknown $T$ is a function of both $z$ and $t$. We need both an **initial condition** $T(z, 0)$ for every $z$ AND **boundary conditions** at the ends of the $z$ domain to pin down the solution.

PDEs split into three families by the shape of their characteristics — **elliptic** (steady-state, no time), **parabolic** (diffusion-like, smooths features), **hyperbolic** (wave-like, propagates features at finite speed). The heat equation is parabolic; the wave equation $\partial^{2} u/\partial t^{2} = c^{2} \partial^{2} u/\partial x^{2}$ is hyperbolic. Most atmospheric equations are a mix.

## 0.13 The CFL condition — intuition

The **Courant–Friedrichs–Lewy (CFL) condition** is the most important stability bound in numerical PDE theory. It says: information cannot propagate further in one numerical time step than it would in the real physical system in the same time.

For a wave equation with wave speed $c$, on a grid with spacing $\Delta x$ and time step $\Delta t$, the CFL number is

$$\mu \;=\; \frac{c\,\Delta t}{\Delta x}.$$

The most basic schemes (forward Euler for the advection equation) require $\mu \le 1$ for stability. If $\mu > 1$, the physical wave moves more than one grid cell per time step, but the discrete scheme only "knows about" neighbouring cells — so it cannot keep up, and errors grow geometrically.

**For the diffusion equation**, the analogous bound is on $\nu = \kappa\Delta t/\Delta z^{2}$. The diffusion of temperature with diffusivity $\kappa$ has no fixed wave speed (heat spreads at all speeds simultaneously), so the bound takes the form $\nu \le 1/2$ rather than $\mu \le 1$.

<!--WIDGET:cfl_advection-->

The widget above is the simplest live demonstration of CFL stability. A Gaussian pulse is advected by the upstream finite-difference scheme

$$u_j^{n+1} \;=\; u_j^{n} - \mu\bigl(u_j^{n} - u_{j-1}^{n}\bigr), \qquad \mu = \frac{c\,\Delta t}{\Delta x}.$$

**Reading this update.** At each grid cell, the new value $u_j^{n+1}$ equals the old value $u_j^n$ minus $\mu$ times the difference between cell $j$ and its upwind neighbour $j-1$. So information flows from left to right (upstream). If $\mu = 1$, the new value at $j$ is exactly the old value at $j-1$ — the pulse moves one cell per step *with no distortion*. If $\mu < 1$, the pulse moves slower than one cell per step (some artificial diffusion appears). If $\mu > 1$, the scheme tries to extrapolate beyond the upstream neighbour — and any wiggle in the initial data is amplified by a factor greater than 1 every step, so the solution explodes within tens of steps. Try it: set $\mu$ to 1.5 and click Play; the pulse becomes a numerical avalanche.

Lecture 5 derives both bounds rigorously and Section 1.4 of this guide shows how they collapse to the "17-second problem" in the project. The lecture-5 dashboard, embedded below, has a live CFL widget.

<iframe src="lecture5_dashboard_Claude_Code.html" style="width:100%;height:760px;border:1px solid #cbd5e1;border-radius:8px;background:#fff" loading="lazy" title="Lecture 5 dashboard — finite differences, stability, CFL"></iframe>

Click the "CFL Condition" tab in the dashboard to access the live CFL animation; the "Von Neumann" and "Stability & Energy Method" tabs walk you through the two main stability-analysis techniques in detail.

## 0.14 Diffusion vs wave propagation — two different physics

The PDE classification matters because **diffusion and wave propagation look completely different**:

- **Diffusion (parabolic)**: a hot spike spreads outward smoothly, getting wider and lower over time. The total area under the curve is preserved (energy conservation), but the peak shrinks. Information is *lost* — you cannot recover the initial spike from the smeared-out final state.

- **Wave propagation (hyperbolic)**: a hot spike (or any disturbance) keeps its shape and moves at a fixed speed $c$. The peak stays the same height; only its location changes. Information is *preserved* — running the equation backward gives back the initial spike.

The atmosphere has *both* kinds of physics happening simultaneously: turbulent eddies diffuse pollutants horizontally (parabolic), and gravity waves propagate from a storm to a hundred kilometres away (hyperbolic). A good model has to handle both well.

<!--WIDGET:diffusion_vs_wave-->

The widget above starts both equations from the same initial Gaussian bump. Press Play. The purple curve is the diffusion equation's solution — it spreads out and flattens; the integral under it is conserved (energy preserved) but the peak shrinks. The orange dashed curve is the wave equation's solution — it splits into a left-moving copy and a right-moving copy of the original bump, each preserving its shape. This visual difference is *the* difference between parabolic and hyperbolic PDEs.

### A live amplification factor for the three classic diffusion schemes

The whole point of stability analysis is to compute, for each Fourier mode, a *per-step growth factor* $|A|$ that tells you how fast that mode amplifies in one time step. For the diffusion equation $\partial T/\partial t = \kappa\partial^{2}T/\partial z^{2}$ the three classic schemes give the following formulas (derived in detail in Chapter 12 of this guide and Chapter 21):

- **FTCS** (forward time, centred space): $A = 1 - 4\nu\sin^{2}\!\bigl(\tfrac{k\Delta z}{2}\bigr)$
- **BTCS** (backward time): $A = 1/\bigl[1 + 4\nu\sin^{2}\!\bigl(\tfrac{k\Delta z}{2}\bigr)\bigr]$
- **Crank–Nicolson**: $A = \bigl[1 - 2\nu\sin^{2}\!\bigl(\tfrac{k\Delta z}{2}\bigr)\bigr] \,/\, \bigl[1 + 2\nu\sin^{2}\!\bigl(\tfrac{k\Delta z}{2}\bigr)\bigr]$

**Reading these formulas.** All three have the same building block $\sin^{2}(k\Delta z/2)$ — this is the Fourier representation of "$1$ minus average of two neighbours", i.e. the discrete Laplacian's eigenvalue for a Fourier mode. The number $\nu = \kappa\Delta t/\Delta z^{2}$ is the dimensionless diffusion number: how many grid cells the heat would diffuse in one time step. The worst wavelength is always the $2\Delta z$ wave ($k\Delta z = \pi$), where $\sin^{2}(\pi/2) = 1$.

- **FTCS at $k\Delta z = \pi$**: $A = 1 - 4\nu$. So $|A| \le 1$ requires $\nu \le 1/2$.
- **BTCS at $k\Delta z = \pi$**: $A = 1/(1 + 4\nu)$, always positive and $\le 1$. *Unconditionally stable.*
- **CN at $k\Delta z = \pi$**: $A = (1 - 2\nu)/(1 + 2\nu)$, always between $-1$ and $1$. *Unconditionally stable.*

<!--WIDGET:amplification_factor-->

In the widget, the dashed lines at $|A| = \pm 1$ are the stability boundary. As $\nu$ grows, the FTCS curve (orange) dives below $-1$ — that is the unstable regime. The BTCS and CN curves stay safely within $[-1, 1]$ for any $\nu$. Slide $\nu$ up and watch FTCS lose stability.

## 0.15 Basic atmospheric thermodynamics

A few key concepts that the lecture material assumes you know:

### Ideal gas law

$$p = \rho R T,$$

where $p$ is pressure (Pa), $\rho$ is density (kg/m³), $R$ is the gas constant for dry air ($\approx 287$ J/kg/K), and $T$ is temperature (K). This is the equation of state for the atmosphere. If you know any two of $p, \rho, T$ you can find the third.

### Hydrostatic balance

For a fluid in static equilibrium, pressure increases with depth at a rate equal to weight per unit volume:

$$\frac{\partial p}{\partial z} = -\rho g.$$

**Reading this equation.** The minus sign says pressure *decreases* as $z$ increases (because $z$ points up and pressure is higher below). $g \approx 9.81$ m/s² is gravity. Combined with the ideal gas law, this gives the exponential decrease of pressure with altitude — at 5.5 km, atmospheric pressure is half its sea-level value. Hydrostatic balance is the reason planes pressurise their cabins.

### Potential temperature

The temperature an air parcel *would have* if compressed adiabatically to a reference pressure $p_0 = 1000$ hPa:

$$\theta = T\biggl(\frac{p_0}{p}\biggr)^{R/c_p}.$$

**Why care.** As air rises, its temperature drops (because pressure drops). Two parcels at different altitudes might have very different $T$ but identical $\theta$ — they are the "same air" thermodynamically. Potential temperature is conserved for adiabatic motion, so it is much more useful than $T$ as a tracer of air masses.

### Adiabatic process

No heat exchange with surroundings. For an ideal gas, $T\,p^{(1-\gamma)/\gamma} = \mathrm{const}$, where $\gamma = c_p/c_v \approx 1.4$ for air. The defining property: as the parcel changes pressure (going up or down), its temperature changes too — but $\theta$ stays the same. Section 0.15 ↔ Section 0.16 connects this to wave physics.

### Latent heat

When water vapour condenses to liquid, it releases $\approx 2.5 \times 10^{6}$ J per kg of water — this is the **latent heat of vaporisation**. This is enormous compared to the specific heat of air ($c_p = 1005$ J/kg/K), so a small amount of phase change releases massive amounts of energy. That is what powers hurricanes, thunderstorms, and the rapid daytime heating over moist surfaces.

### Coriolis effect

Earth rotates once every $\approx 86164$ s (a sidereal day). On a rotating Earth, freely moving objects appear to curve when viewed from the rotating frame — to the right in the Northern Hemisphere, to the left in the Southern. The fictitious force responsible is the **Coriolis force** $-2\vec{\Omega} \times \vec{V}$, where $\vec{\Omega}$ is the rotation vector and $\vec{V}$ is the velocity. Its magnitude is $f|\vec{V}|$ where $f = 2|\vec{\Omega}|\sin(\text{latitude})$. The Coriolis effect is what makes large-scale atmospheric flow curve into the familiar cyclone/anticyclone patterns on weather maps.

<!--WIDGET:coriolis-->

The widget above launches a puck eastward from the centre. Without rotation it would continue in the dashed straight line. With Coriolis turned on (drag the latitude slider away from zero), the puck curves to the right in the Northern Hemisphere and to the left in the Southern. At the equator, Coriolis vanishes because the rotation axis is parallel to the surface — the cross-product $\vec{\Omega}\times\vec{V}$ has no vertical component to deflect horizontal motion.

### Geostrophic balance

For large-scale, slowly-varying flow, the pressure-gradient force and the Coriolis force approximately balance:

$$f\vec{V} \;=\; -\frac{1}{\rho}\hat{k} \times \nabla p,$$

where $\hat{k}$ is the unit vector pointing up. **Reading this.** Wind flows along (not across) pressure contours, with low pressure on the left in the Northern Hemisphere. This is why high-pressure systems on a weather map have clockwise circulation in the NH — the wind is geostrophic, parallel to the contours.

The lecture-3 dashboard has working widgets for the ideal gas law, hydrostatic balance, potential temperature, and several others. Embed it here and click through:

<iframe src="lecture3_dashboard_Claude_Code.html" style="width:100%;height:820px;border:1px solid #cbd5e1;border-radius:8px;background:#fff" loading="lazy" title="Lecture 3 dashboard — basic mathematical and physical tools"></iframe>

The first three tabs (Taylor Series, Mean Value Theorem, Derivative) give you Lecture 3's foundational maths interactively. Later tabs explore Eulerian vs Lagrangian viewpoints, hydrostatic balance, the Boussinesq approximation, potential temperature, the Exner function, the continuity equation (and divergence), the anelastic approximation, and the scalar advection-diffusion equation.

## 0.16 Three families of atmospheric waves

The atmosphere supports many different kinds of wave motion. The three most important:

**Sound waves**. Restoring force: compressibility. Speed: $\approx 340$ m/s in the lower atmosphere. These are the fastest waves and the most numerically annoying — they require time steps much smaller than the meteorologically-interesting motions. Atmospheric models usually "filter" sound waves out by making simplifying approximations (anelastic, Boussinesq) that eliminate them from the equations.

**Internal gravity waves**. Restoring force: buoyancy. Speed: $\approx 10-100$ m/s. These propagate when stably stratified air is displaced vertically — the air oscillates up and down, sending waves outward. They transport energy and momentum from convection or mountain ranges to remote regions.

**Rossby waves**. Restoring force: the latitudinal variation of the Coriolis parameter $f$. Speed: $\approx 1-10$ m/s. These are the slow, large-scale meanders of the jet stream — the eastward-travelling troughs and ridges that make up weather patterns at mid-latitudes.

A model that wants to resolve weather (Rossby waves) but has to take time steps small enough to keep sound-wave-related numerics stable would be enormously wasteful. That is why filtering matters.

Lecture 4 walks through how sound waves arise from the basic equations and how they are filtered. The embedded dashboard:

<iframe src="lecture4_dashboard_Claude_Code.html" style="width:100%;height:820px;border:1px solid #cbd5e1;border-radius:8px;background:#fff" loading="lazy" title="Lecture 4 dashboard — Euler equations and waves"></iframe>

## 0.17 Stability vs accuracy vs consistency — three different properties of a numerical scheme

When we discretise a PDE, we want our scheme to be three things:

**Consistent** — as $\Delta t, \Delta x \to 0$, the truncation error goes to zero. The discrete equation reduces to the continuous one in the limit. Most reasonable schemes are consistent.

**Stable** — small numerical errors do not amplify unboundedly over many time steps. Forward Euler applied to the diffusion equation is stable only if $\nu \le 1/2$; backward Euler is unconditionally stable.

**Accurate** — the order of the truncation error. A first-order method has error $\propto \Delta t$; a second-order method has error $\propto \Delta t^{2}$.

The **Lax equivalence theorem** says: for a *consistent* linear scheme applied to a linear PDE, stability is necessary and sufficient for convergence (the numerical solution approaching the true solution as $\Delta t, \Delta x \to 0$). So in practice we usually just ask "is the scheme stable?" — that is the question that decides whether the scheme can be used at all.

Lecture 5's dashboard (already embedded in Section 0.13) walks through all three properties with worked examples; the "Stability & Energy Method" tab in particular shows you what a stability proof looks like in practice.

## 0.18 Notation summary you will see throughout the rest of the guide

A quick reference list of the most common notation conventions:

| Symbol | Meaning |
|---|---|
| $T_j^n$ | numerical approximation to $T$ in cell $j$ at time level $n$ |
| $T_{j \pm 1/2}^n$ | quantity evaluated at the half-level (face) between cells |
| $\Delta t$, $\Delta x$, $\Delta z$ | discrete time step and grid spacings |
| $\partial / \partial t$, $\partial / \partial z$ | partial derivatives |
| $\nabla$ | the del operator (gradient, divergence, curl, Laplacian) |
| $\bar{T}$ | a mean or background value |
| $T'$ | a perturbation away from the mean |
| $\hat{T}$ | a Fourier coefficient or a unit vector (context-dependent) |
| $|A|$ | absolute value of a real number; magnitude of a complex number |
| $\propto$ | "proportional to" |
| $\ll$ | "much less than" |
| $\sim$ | "of the same order as" or "approximately" |
| $\langle \cdot \rangle$ | ensemble or volume average |

With this vocabulary in place, the rest of the guide should read smoothly. If you ever hit a symbol that has not been defined, search this chapter — it is here.

## 0.19 The damping-depth solution — tying the prerequisites together

Everything in this chapter — sinusoidal forcing, complex exponentials, partial derivatives, the heat equation, the dimensionless number $\nu$ — comes together in the most important closed-form solution for this course. Apply a sinusoidal surface temperature $T(0, t) = T_{0} + A\sin(\omega t)$ to a semi-infinite, homogeneous ground with diffusivity $\kappa$. The heat equation $\partial T/\partial t = \kappa\,\partial^{2}T/\partial z^{2}$ has the exact solution

$$T(z, t) \;=\; T_{0} + A\,e^{-z/d}\,\sin\!\Bigl(\omega t - \tfrac{z}{d}\Bigr),\qquad d \;=\; \sqrt{\tfrac{2\kappa}{\omega}}.$$

**Reading this solution.** Two things happen as you go deeper into the ground:

1. **Amplitude damping.** The factor $e^{-z/d}$ shrinks the oscillation amplitude exponentially with depth. At $z = d$, the amplitude is $1/e \approx 37\%$ of the surface value; at $z = 3d$ it is below $5\%$ — essentially constant temperature.
2. **Phase lag.** The argument of the sine is $\omega t - z/d$, so peak temperature at depth $z$ arrives a time $z/(\omega d) = z/\sqrt{2\kappa\omega}$ later than at the surface. For a daily forcing ($\omega = 2\pi/86400\,\mathrm{s}^{-1}$) and a typical soil ($\kappa\sim 10^{-6}\,\mathrm{m^{2}/s}$), $d\sim 0.12\,\mathrm{m}$ and the phase lag at depth $d$ is about 4 hours — that is why the soil at 12 cm is coldest *not* at sunrise but in the late morning.

The single parameter $d = \sqrt{2\kappa/\omega}$ is the **damping depth**. Faster forcing (larger $\omega$) means smaller $d$ — the diurnal wave penetrates 10 cm, the annual wave penetrates 1–2 m, geological-time forcing penetrates many metres. Bigger diffusivity $\kappa$ (e.g. wet soil vs. dry) means larger $d$ — wet soil transmits the diurnal wave deeper.

<!--WIDGET:damping_depth-->

In the widget above, drag $\kappa$ to see $d$ change; drag the hour-of-day cursor (or press Play) to scan a 24-hour cycle. The orange envelope is the exponential decay $\pm A\,e^{-z/d}$; the purple curve is the instantaneous $T(z, t)$ profile. Notice how the purple curve always stays within the envelope and how the peak depth lags behind the surface peak. This single picture is the analytical "answer key" against which all the numerical schemes in Chapters 21 and 22 of this guide are tested.

### One last reading-tip

When a section of this guide writes something like "$T_{j}^{n+1}$", "$\kappa\Delta t/\Delta z^{2}$", "$e^{-z/d}$", or "$\nabla\cdot(\kappa\nabla T)$", recognise that you have already seen every symbol here in Chapter 0. The rest of the guide is just composing these blocks into longer arguments about how to discretise PDEs, how to keep schemes stable, and how to assess accuracy.

---
