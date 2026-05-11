# CLIM-715 Numerical Methods Project

## What this project is

A CLIM-715 (Numerical Methods for Climate & Weather Modeling) course project comparing FTCS, BTCS, and Crank–Nicolson schemes for the 1-D heat conduction equation, applied to three urban substrates (asphalt road, concrete roof, bare soil) coupled to a prognostic surface energy balance. The model integrates two days of synthetic diurnal forcing and runs a 27-cell experiment matrix (3 substrates × 3 schemes × 3 Δt values: 15, 60, 600 s).

The deliverables for this course are: a written report (5-page short version + ~12-page long version), an executable Python script that reproduces all results, a Jupyter notebook narrating the analysis, and a presentation that uses interactive HTML visualizations.

## Files in this directory

### Source code and notebooks
- `run_experiments.py` — the canonical solver. Defines the three substrate compositions (`SUBSTRATES` dict), the diurnal forcing functions `S_down(t)` and `T_air(t)`, and the coupled SEB+column update. Do not modify the substrate definitions or forcing constants without flagging this first; results in the report depend on them.
- `CLIM715_Project_Notebook_GroundFlux.ipynb` — Jupyter notebook with the analysis narrative, 8 sections including SHAP attribution.

### Written deliverables (Word documents — read with python-docx if needed)
- `CLIM715_Project_Report_Long.docx` — full ~12-page report with §1 introduction through §6 SHAP attribution.
- `CLIM715_Project_Report_5pages (1).docx` — condensed 5-page version.
- `CLIM715_Project_Tutorial.docx` — how-to-reproduce guide.

### Interactive HTML visualizations (presentation pieces)
- `CLIM715_Substrate_3D_Visualization_clean_ed.html` — Three.js 3D scene of the three substrate columns going below ground level, with diurnal sun cycle and X-ray ground-fade. **The "clean_ed" version is the current canonical one; the "v2" file is older.**
- `CLIM715_Substrate_3D_Visualization_v2.html` — older version, kept for reference only.
- `window_von_neuman.html` — interactive ν-slider for von Neumann amplification factors. Three side-by-side panels for FTCS, BTCS, CN with stable/unstable badges.
- `window_delta_t.html` — interactive Δt-refinement slider. Slider on top, 2×2 grid below: three substrate Ts(t) panels plus an RMSE-vs-Δt log-log plot.

## Hard rules for Claude Code when modifying anything in this folder

1. **No frameworks in the HTML visualizations.** They are vanilla HTML/SVG/JavaScript. No React, Vue, D3, Plotly, jQuery, or any CDN-loaded library other than Three.js (which only the substrate 3D viz uses). The reason: the presentation will run on whatever projector/laptop the panel provides. CDN failures kill demos.

2. **Style: "Clean Educational" palette.** All visualizations use this exact palette:
   - Background: `#eaf0f8` (blue-tinted soft)
   - Cards: white `#ffffff` with soft purple shadow `rgba(107, 92, 181, 0.10–0.12)`
   - Input controls: orange `#ee845b` (slider thumbs, hover states)
   - Output values: teal `#38b2ac` / `#2c8a83` (live readouts, "STABLE" badges)
   - Actions / titles: purple `#6b5cb5`
   - Substrate identity colours (used wherever a substrate appears):
     - Asphalt road = purple `#6b5cb5`
     - Concrete roof = warm orange `#d97757`
     - Bare soil = earth brown `#8b6f3a`
   - Rounded corners (10–12px), minimalist.

3. **Encoding rule (for any plot showing multiple substrates and schemes):** colour names the substrate, line style names the scheme. BTCS = solid line, CN = dashed line. Never reuse a substrate colour to mean a scheme or vice versa.

4. **All visualizations must fit in 100vh with no scrolling.** The presentation runs full-screen. Use `height: 100vh; overflow: hidden` on `body`, flex column layouts for the container, and `flex: 1` on the SVG/canvas elements. Never use fixed pixel heights for the main plotting area; let it expand to fill the viewport.

5. **Number values must match the report.** When generating data for a viz, use `run_experiments.py` (or its helpers) as the source of truth. Sanity-check key numbers against the report:
   - Asphalt BTCS Δt=600s RMSE_Ts ≈ 2.10 K; CN ≈ 1.12 K
   - Δt=600/Δt=60 RMSE ratios all between 8.2 and 10.2 (first-order in Δt)
   - FTCS at ν=0.5 gives |A|=1 at the 2Δz wave; at ν=5, |A|=19
   - Storage ratios all within ±5% of unity
   - SHAP: κ_top has mean |SHAP| ≈ 0.71 K with R²=0.92 alone; residual after κ_top is dominated by μ_eff
   If a generated number disagrees with the report by more than ~5%, stop and flag it before continuing.

6. **The model has no ground level, no buildings, and no above/below distinction.** It is three identical 1-D columns, each 2 m of layered material with a radiating top surface. Past iterations of the substrate 3D viz tried to add fictional buildings and ground-level distinctions; do not reintroduce those.

7. **No shadows in 3D visualizations.** `renderer.shadowMap.enabled = false`, all `castShadow`/`receiveShadow` flags = false. Past confusion came from shadowed geometry making depth ambiguous.

## Standard workflow for new visualizations

When asked to build a new interactive piece:

1. Read this CLAUDE.md and the relevant report section first to understand what the viz needs to demonstrate.
2. Create the viz as a standalone HTML file with a descriptive name (`window_<concept>.html` matches the existing convention).
3. Use the Clean Educational style and substrate-colour/line-style encoding from the rules above.
4. Verify slider behaviour with a real DOM simulation (jsdom or equivalent) before declaring it done. Do not assume a slider works just because the syntax is correct — past iterations had silent rendering failures.
5. Check that the viz fits in 100vh by inspecting the layout flex hierarchy.

## Standard workflow for editing the report or notebook

1. Read the current version first; do not re-derive content from memory.
2. The notebook and the long report are the two sources of truth — keep them consistent. If a number changes in one, change it in the other.
3. Citations in the report should reference course materials: lecture notes by section ("Lecture 6 Section 6, Slides 15–17"), Misconception list by number, Notes by number. Avoid inventing or paraphrasing citations.

## Hardware and execution

- The `run_experiments.py` solver runs in ~30 seconds for the full 27-cell matrix on a typical laptop. Re-run when you need fresh CSVs or PNGs.
- The 150-column synthetic ensemble for the SHAP analysis (`shap_attribution.py` in older sessions) takes ~2 minutes.
- All numerical runs are deterministic given fixed seeds; if results don't reproduce, suspect a code change, not a stochastic effect.

## GitHub-hosted live preview (set up 2026-05-09)

The full project lives at https://github.com/shammun/clim715-ground-flux (public, free-tier Pages). Every HTML file in this directory is served live at:

- Final presentation deck: https://shammun.github.io/clim715-ground-flux/CLIM715_Final_Presentation.html
- Qualifier reference deck: https://shammun.github.io/clim715-ground-flux/qualifier_final_presentation_3.html
- Any standalone viz: https://shammun.github.io/clim715-ground-flux/window_<name>.html

The user views these from mobile while changes are made on the desktop. Workflow on every change:

1. Make the change.
2. `git add` the touched files, `git commit` with a clear message, `git push`. Use the gh CLI binary at `C:\Users\sislam27\AppData\Local\Microsoft\WinGet\Packages\GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe\bin\gh.exe` if you need to run anything via gh; the user is already authenticated as `shammun`.
3. Pages redeploys in ~30–60 s. Tell the user the change is live and quote the relevant deck URL so they can refresh on mobile.

**Always include the deck URL in every reply** so the user can tap it from their phone. The canonical URL is `https://shammun.github.io/clim715-ground-flux/CLIM715_Final_Presentation.html`.

**Always include the full live-page link list at the end of every reply that touches any HTML in this repo.** The user has asked, across sessions, to see all live URLs without having to ask. Whenever you modify, create, rebuild, or even just discuss any `.html` file in this directory, end your reply with the link block below. The canonical README.md in this repo carries the full table; the block below is the abbreviated form to drop into chat replies.

```
Live pages (https://shammun.github.io/clim715-ground-flux/):
• Final Presentation: …/CLIM715_Final_Presentation.html
• Study Guide:        …/Lecture_Master_Guide.html
• Project Walkthrough:…/clarify_project.html
• Speaker Notes:      …/CLIM715_speaker_notes.html
• Q&A Guide:          …/CLIM715_QA_guide.html
• Substrate 3D (v3):  …/CLIM715_Substrate_3D_Visualization_v3.html
• Von Neumann widget: …/window_von_neuman.html
• Δt widget:          …/window_delta_t.html
• Lecture 3 dash:     …/lecture3_dashboard_Claude_Code.html
• Lecture 4 dash:     …/lecture4_dashboard_Claude_Code.html
• Lecture 5 dash:     …/lecture5_dashboard_Claude_Code.html
• Lecture 6 dash:     …/lecture6_dashboard_Claude_Code.html
• Qualifier deck:     …/qualifier_final_presentation_3.html
• Full list:          README.md on GitHub
```

When the user's most-recent request was specifically about *one* page (e.g., "fix slide 8 of the deck"), bold or callout the relevant URL at the top of that block so it is the first thing they see; still include the rest so they have one-touch access to everything.

**Auto-push is the default** — do not ask the user for permission to commit or push. Every user-requested change ends in `git commit` + `git push`. Don't push speculative WIP; push after each change has landed and is internally consistent (i.e., what would be a clean commit). Don't commit `.claude/settings.local.json`; it's already in `.gitignore`.

## Multi-pass verification when the user asks "verify slide N"

When the user asks to verify a slide against the long report or Python code, do **not** trust the first pass — values can be self-consistent within the slide but use the wrong source-of-truth. The pattern that has caught real bugs:

1. **Read the slide content fully** — title, subtitle, headline, table cells, chart code, sub-labels, peak callouts.
2. **Extract the matching source-of-truth** in parallel:
   - Long report `.docx`: read with `python-docx`, including `d.tables` (Table 1 has the verification numbers; Table 2 has Test 2 metrics). The text often paraphrases a value but the table holds the canonical version.
   - Python code: `run_experiments.py`, `extend_test2_metrics.py`, `shap_attribution.py`. Especially substrate parameters, κ values, Δz, atmospheric forcing constants, SEB coefficients.
   - Generated CSVs: `test2_extended_metrics.csv`, `shap_summary.csv`, `shap_residual_summary.csv`, `synthetic_dataset.csv`.
   - The embedded JSON inside `window_delta_t.html` (`<script id="dt-data">`) — extract with regex + `json.loads`.
3. **Cell-by-cell comparison**, ideally in a small Python snippet that prints the long-report value, the slide value, and a checkmark. Don't eyeball — actually compute.
4. **Cross-check internal consistency** — e.g., for any (Δt, ν) pair claim, verify ν = κΔt/Δz² with the slide's stated κ. A real bug we hit: the slide displayed κ = 2.31×10⁻⁷ in caption but every ν in the table was computed with κ = 2.31×10⁻⁸.
5. **Cross-check across slides** — values quoted on slide N should match those on adjacent slides. Slide 8's Tₛ(t) curves and slide 9's reference dataset should be from the same data; slide 10's λ/C should match slide 3's substrate definitions; slide 11's RMSE values should match `test2_extended_metrics.csv` exactly; slide 12's SHAP values should match `shap_summary.csv`.
6. **Re-verify after fixing** — after the first round of edits, re-extract the source-of-truth and compare again. The first fix often catches the obvious errors but misses subtle ones (e.g., a row reordering, a column-header mismatch, a fabricated extra row that needs removal). Plan on at least two verification passes.
7. **Report findings as a table** in the reply: bug list, source-of-truth value, slide value, fix. The user wants to see the diff, not just "fixed it".

Things to watch for that have actually broken slides in this deck:
- ν values computed with the wrong κ (factor of 10 off).
- Δt values 10× larger or smaller than they should be for the stated ν.
- Hand-drawn SVG paths that don't match the actual data (curve peaks at wrong hour, or curves with implausible amplitude).
- Column headers that label values differently than the source-of-truth ("RMSE Tₛ" when the data is actually "RMSE T@10 cm").
- Two SVG coordinate systems in the same chart (one for gridlines, another for data points). The "slope = 1" reference line on a log-log plot should be a true 45°.
- Sub-labels that paraphrase the long report's physical reasoning incorrectly (e.g., "high admittance → hot" when the report attributes the peak to low albedo).
- Fabricated extra rows in tables that don't appear in the long report's Table 1 / Table 2.
- Use of dev jargon ("faithful port of run_experiments.py", "per long report §5.2") in a slide subtitle that should be presentation prose.

After fixing, push the commit (auto-push), give the user the Pages URL, and report the diff in a verification table.
