# CLIM-715 Ground Flux Project — Live Pages

All HTML files in this repository are served live via GitHub Pages at
`https://shammun.github.io/clim715-ground-flux/<filename>`.

## Primary deliverables

| Page | URL |
|---|---|
| **Final Presentation (13-slide deck)** | https://shammun.github.io/clim715-ground-flux/CLIM715_Final_Presentation.html |
| **Study Guide** (Chapter 0 prerequisites + Chapters 1–25 + 16 interactive widgets) | https://shammun.github.io/clim715-ground-flux/Lecture_Master_Guide.html |
| **Project Walkthrough** (mastery-level "clarify_project") | https://shammun.github.io/clim715-ground-flux/clarify_project.html |
| **Speaker Notes** (BroadcastChannel-synced for the deck) | https://shammun.github.io/clim715-ground-flux/CLIM715_speaker_notes.html |
| **Q&A Guide** (20 anticipated questions) | https://shammun.github.io/clim715-ground-flux/CLIM715_QA_guide.html |

## Standalone interactive visualisations

| Widget | URL |
|---|---|
| Substrate 3D scene (v3 — current) | https://shammun.github.io/clim715-ground-flux/CLIM715_Substrate_3D_Visualization_v3.html |
| Substrate 3D scene (clean_ed) | https://shammun.github.io/clim715-ground-flux/CLIM715_Substrate_3D_Visualization_clean_ed.html |
| Von Neumann amplification (FTCS/BTCS/CN slider) | https://shammun.github.io/clim715-ground-flux/window_von_neuman.html |
| Δt refinement (2×2 panel with RMSE log-log) | https://shammun.github.io/clim715-ground-flux/window_delta_t.html |
| 17-second problem widget | https://shammun.github.io/clim715-ground-flux/widget_17sec.html |
| Curvature widget | https://shammun.github.io/clim715-ground-flux/widget_curvature.html |
| θ-method physics slide | https://shammun.github.io/clim715-ground-flux/slide_physics_thetamethod.html |
| Δt-ratios slide | https://shammun.github.io/clim715-ground-flux/slide_dt_ratios.html |
| SHAP attribution slide | https://shammun.github.io/clim715-ground-flux/slide_shap_attribution.html |
| Conclusions slide | https://shammun.github.io/clim715-ground-flux/slide_conclusions.html |

## Per-lecture interactive dashboards

| Dashboard | URL |
|---|---|
| Lecture 3 — basic mathematical & physical tools | https://shammun.github.io/clim715-ground-flux/lecture3_dashboard_Claude_Code.html |
| Lecture 4 — Euler equations and waves | https://shammun.github.io/clim715-ground-flux/lecture4_dashboard_Claude_Code.html |
| Lecture 5 — finite differences, stability, CFL | https://shammun.github.io/clim715-ground-flux/lecture5_dashboard_Claude_Code.html |
| Lecture 6 — finite differences (forward / backward / centred) | https://shammun.github.io/clim715-ground-flux/lecture6_dashboard_Claude_Code.html |

## Qualifier-exam companion

| Page | URL |
|---|---|
| Qualifier final presentation | https://shammun.github.io/clim715-ground-flux/qualifier_final_presentation_3.html |

## Reproducing the numerical results

The full 27-cell experiment matrix (3 substrates × 3 schemes × 3 Δt values) is run by
`run_experiments.py`. The SHAP attribution lives in `shap_attribution.py`. See `CLAUDE.md`
for full project conventions.
