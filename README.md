# CLIM-715 — Numerical Damping of the Diurnal Ground Heat Flux over Urban Substrates

Final project for CLIM-715 (Numerical Methods for Climate & Weather Modeling),
George Mason University. Compares FTCS, BTCS, and Crank–Nicolson schemes for
the 1-D heat equation, applied to three urban substrates (asphalt road,
concrete roof, bare soil) coupled to a prognostic surface energy balance.

**Presentation:** https://shammun.github.io/clim715-ground-flux/CLIM715_Final_Presentation.html

## Reproducing the numerical results

`run_experiments.py` runs the full 27-cell experiment matrix
(3 substrates × 3 schemes × 3 Δt values). The SHAP attribution lives in
`shap_attribution.py`. See `CLAUDE.md` for full project conventions.
