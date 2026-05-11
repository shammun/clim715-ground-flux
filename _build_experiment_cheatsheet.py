"""Build CLIM715_Experiment_Cheatsheet.docx - a today-ready handout
explaining exactly how the CLIM-715 ground-flux experiment was set up
and run. For explaining the project to others.
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PURPLE = RGBColor(0x6B, 0x5C, 0xB5)
TEAL = RGBColor(0x2C, 0x8A, 0x83)
ORANGE = RGBColor(0xC2, 0x49, 0x2A)
GREY = RGBColor(0x4A, 0x50, 0x66)
DARK = RGBColor(0x2C, 0x31, 0x42)

doc = Document()

# Page setup
for s in doc.sections:
    s.left_margin = Inches(0.85)
    s.right_margin = Inches(0.85)
    s.top_margin = Inches(0.7)
    s.bottom_margin = Inches(0.7)

# Default style
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

def add_title(text, color=PURPLE, size=22):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return p

def add_subtitle(text, color=GREY, size=11):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return p

def add_h(text, level=1, color=PURPLE):
    sizes = {1: 16, 2: 13, 3: 12}
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(sizes.get(level, 11))
    r.font.color.rgb = color
    return p

def add_para(text, bold_first_phrase=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    if bold_first_phrase:
        r1 = p.add_run(bold_first_phrase + ' ')
        r1.bold = True
        r1.font.color.rgb = DARK
        r2 = p.add_run(text)
    else:
        p.add_run(text)
    return p

def add_bullet(text, bold_lead=None, level=0):
    p = doc.add_paragraph(style='List Bullet' if level == 0 else 'List Bullet 2')
    p.paragraph_format.space_after = Pt(2)
    if bold_lead:
        r1 = p.add_run(bold_lead + ' ')
        r1.bold = True
        r1.font.color.rgb = DARK
        p.add_run(text)
    else:
        p.add_run(text)
    return p

def add_num(text, bold_lead=None):
    p = doc.add_paragraph(style='List Number')
    p.paragraph_format.space_after = Pt(3)
    if bold_lead:
        r1 = p.add_run(bold_lead + ' ')
        r1.bold = True
        r1.font.color.rgb = DARK
        p.add_run(text)
    else:
        p.add_run(text)
    return p

def add_equation_block(text):
    """Centred italic monospaced equation line (poor man's math)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    r.font.name = 'Cambria Math'
    r.font.size = Pt(13)
    r.font.color.rgb = DARK
    return p

def add_code_block(lines):
    """Monospace block, indented, light background-ish via grey colour."""
    for line in lines:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        r = p.add_run(line if line else ' ')
        r.font.name = 'Consolas'
        r.font.size = Pt(10)
        r.font.color.rgb = DARK

def add_callout(text, color=TEAL):
    """Indented, italic, coloured callout."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.right_indent = Inches(0.3)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    r.italic = True
    r.font.color.rgb = color
    return p

def add_table(headers, rows, col_widths=None):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = 'Light Grid Accent 1'
    t.autofit = True

    hdr_cells = t.rows[0].cells
    for i, h in enumerate(headers):
        c = hdr_cells[i]
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(10)
        # purple header background
        tc_pr = c._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:fill'), '6B5CB5')
        tc_pr.append(shd)

    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            c = t.rows[ri + 1].cells[ci]
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(str(val))
            r.font.size = Pt(10)
            r.font.color.rgb = DARK

    if col_widths:
        for i, w in enumerate(col_widths):
            for row in t.rows:
                row.cells[i].width = w
    return t

# =================================================================
# CONTENT BEGINS
# =================================================================

add_title("CLIM-715 Ground Flux Experiment", color=PURPLE, size=22)
add_subtitle("Everything you need to explain the experiment in one sitting.", size=12)
add_subtitle("Source: run_experiments.py + modified_full_report_1.docx. Built 2026-05-11.", size=9)

# -----------------------------------------------------------------
add_h("1. The Big Picture (30-second version)", level=1)
add_para(
    "We simulate one-dimensional heat conduction through three urban substrate columns "
    "(asphalt road, concrete roof, bare soil), each 2 metres deep, driven by a synthetic "
    "diurnal cycle of solar radiation and air temperature. We solve the heat equation using "
    "three different finite-difference schemes (FTCS, BTCS, Crank-Nicolson) at three "
    "different time steps (15 s, 60 s, 600 s). The surface temperature is computed at every "
    "step by solving the surface energy balance with Newton iteration. We then measure how "
    "the schemes' surface ground heat flux deviates from a fine-Δt reference.",
)
add_callout(
    "Headline finding: at Δt = 600 s, BTCS over-amplifies the diurnal G amplitude by 40 % on "
    "asphalt and concrete, 19 % on bare soil; Crank-Nicolson halves these errors. The "
    "dominant error is operator-splitting between the column and SEB updates."
)

# -----------------------------------------------------------------
add_h("2. Sequence of Steps — How the Experiment Runs", level=1)
add_para("The whole project follows this order; everything else is detail.")

add_num("Define three substrates as layered stacks of (depth, λ, C).", bold_lead="Define substrates.")
add_num("Build a stretched vertical grid for each substrate (top cell 0.5 cm for asphalt and concrete, 1 cm for bare soil; geometric stretch 1.18-1.25 down to bottom cell ≈ 30 cm at z = 2 m).", bold_lead="Build the grid.")
add_num("Initialize substrate temperatures from the analytical damping-depth profile.", bold_lead="Initialize.")
add_num("Loop over time steps. For each step:", bold_lead="Time-step loop.")
add_bullet("Sub-step A: advance the column from time n to n+1 using the θ-method, holding Tₛ⁰ fixed.", level=1)
add_bullet("Sub-step B: solve the surface energy balance for new Tₛ⁰ via Newton iteration, holding the column fixed.", level=1)
add_bullet("Apply bottom BC: T[N-1] = T[N-2] (zero-flux Neumann).", level=1)
add_num("Run for 2 diurnal cycles. Use day-2 (after 1-day spin-up) for all diagnostics.", bold_lead="Integration period.")
add_num("Compare each scheme's day-2 surface ground heat flux G(t) and surface temperature Tₛ⁰(t) against the reference run (FTCS at Δt = 15 s).", bold_lead="Compare.")
add_num("Report: RMSE of Tₛ⁰, peak-amplitude ratio of G, daily-storage ratio.", bold_lead="Diagnose.")

# -----------------------------------------------------------------
add_h("3. The Three Substrates", level=1)
add_para("Each substrate is a 2 m deep column of layered material with prescribed albedo at the top.")
add_table(
    ["Substrate", "Layers (depth, λ W/m/K, C ×10⁶ J/m³/K)", "Albedo α_s", "d (cm)"],
    [
        ["Asphalt road (4 layers)", "Asphalt 0-5 cm (0.75, 2.0); aggregate 5-25 cm (1.40, 2.4); dry soil 25-100 cm (0.30, 1.3); subsoil 100-200 cm (0.50, 1.8)", "0.10", "10.2"],
        ["Concrete roof (3 layers)", "Concrete deck 0-10 cm (1.50, 2.1); mineral-wool insulation 10-20 cm (0.04, 0.08); drywall/wood 20-200 cm (0.15, 1.5)", "0.30", "14.0"],
        ["Bare soil (uniform)", "Sandy loam 0-200 cm (0.30, 1.3)", "0.20", "8.0"],
    ],
)
add_callout("d = √(2κ/ω) is the diurnal damping depth, the e-folding depth of the daily wave. Computed from each substrate's top-layer κ = λ/C.")

# -----------------------------------------------------------------
add_h("4. The Governing Equation (the physics)", level=1)
add_para(
    "The heat equation in conductivity form (preserves discrete heat conservation across layer interfaces):",
)
add_equation_block("C_s(z) · ∂T_s/∂t  =  ∂/∂z [ λ_s(z) · ∂T_s/∂z ]")
add_para(
    "In words: the volumetric heat capacity times the rate of temperature change at depth z "
    "equals the spatial divergence of the conductive heat flux. Heat piles up wherever more "
    "flux enters from above than exits below.",
)

# -----------------------------------------------------------------
add_h("5. The Three Schemes — One Equation, Three α Values", level=1)
add_para("All three time-stepping schemes are special cases of a single θ-method update equation:")
add_equation_block("C_j Δz_j (T_j^(n+1) − T_j^n) / Δt = α [−∂G/∂z]^(n+1) + (1−α) [−∂G/∂z]^n")
add_para("where the flux-divergence at cell j is computed from G_{j±1/2} = λ_{j±1/2} (T_j − T_{j±1}) / (centre-to-centre spacing). Choose α; get a scheme:")
add_table(
    ["α", "Scheme", "Stability", "Order in Δt", "Per-step cost"],
    [
        ["0",   "FTCS  (Forward in Time)",  "Conditionally stable: ν ≤ 1/2",   "1st", "Cheap (vectorised arithmetic)"],
        ["1/2", "Crank-Nicolson",           "Unconditionally stable",          "2nd", "Tridiagonal solve, O(N)"],
        ["1",   "BTCS  (Backward in Time)", "Unconditionally stable, damping", "1st", "Tridiagonal solve, O(N)"],
    ],
)
add_callout("ν = κ Δt / Δz² is the dimensionless diffusion number — the diffusion analogue of the Courant-Friedrichs-Lewy number.")

# -----------------------------------------------------------------
add_h("6. Boundary Conditions — What Closes the System", level=1)
add_para(
    "The heat equation is second-order in z, so we need two BCs (one at each end of the column).",
)

add_h("6a. Top BC — Surface Energy Balance (SEB) closure", level=2)
add_para("The top of the column is closed by the requirement that the four surface fluxes balance to zero:")
add_equation_block("R_n − H − LE − G = 0   (solved for T_s⁰)")
add_para("with each flux evaluated at the surface temperature T_s⁰:")
add_bullet("R_n = (1 − α_s) S↓ + ε_s L↓ − ε_s σ (T_s⁰)⁴   (net radiation; σ = 5.67×10⁻⁸ W/m²/K⁴)", bold_lead="Net radiation.")
add_bullet("H = ρ c_p (T_s⁰ − T_a) / r_a    where r_a = 1 / (C_H U) ≈ 67 s/m   (sensible heat flux)", bold_lead="Sensible.")
add_bullet("LE = 0   (strict-impervious assumption — no evaporation)", bold_lead="Latent.")
add_bullet("G = λ_{1/2} (T_s⁰ − T_1) / (z_1 − z_0)   (ground heat flux, from the top half-level)", bold_lead="Ground.")
add_para(
    "The (T_s⁰)⁴ term makes this equation nonlinear in T_s⁰. We solve it by Newton iteration:",
)
add_equation_block("T_s⁰_new = T_s⁰_old − F(T_s⁰_old) / F′(T_s⁰_old)")
add_para("where F = R_n − H − LE − G. Typically converges in 3-4 iterations to |ΔT| < 10⁻⁴ K.")

add_h("6b. Bottom BC — Zero-flux Neumann at z = 2 m", level=2)
add_para("At the deepest face, the temperature gradient is set to zero:")
add_equation_block("∂T_s/∂z |_{z=2m} = 0    ⟺    G|_{z=2m} = 0    ⟺    T_{N-1} = T_{N-2}")
add_para(
    "Discretely, one line of code: the deepest cell mirrors the one above it. Justified "
    "because z = 2 m is 14-25 damping depths down, where the diurnal amplitude is already "
    "negligible (~10⁻⁶ of the surface value).",
)

# -----------------------------------------------------------------
add_h("7. Von Neumann Stability Analysis — How We Used It", level=1)
add_para("We used von Neumann analysis to PREDICT which (scheme, Δt, substrate) combinations would blow up, then VERIFIED the prediction empirically in Test 1 and Test 2.")
add_h("7a. The procedure (four steps)", level=2)
add_num("Substitute a Fourier mode  T_j^n = A^n · e^(ikjΔz)  into each scheme's update equation.")
add_num("Cancel common factors and solve for the per-step amplification factor A as a function of ν and kΔz.")
add_num("Demand |A| ≤ 1 for every resolvable wavenumber, i.e., kΔz ∈ [0, π].")
add_num("Note that the worst case is always at kΔz = π (the 2-Δz wave, where adjacent cells flip sign). Substitute that and solve for the stability bound on ν.")

add_h("7b. Results — the three amplification factors at kΔz = π", level=2)
add_table(
    ["Scheme", "A at worst wave", "|A| over ν > 0", "Stability bound"],
    [
        ["FTCS",            "1 − 4ν",        "> 1 when ν > 1/2",   "Conditional: ν ≤ 1/2"],
        ["BTCS",            "1/(1 + 4ν)",    "Always in (0, 1]",   "Unconditional"],
        ["Crank-Nicolson",  "(1 − 2ν)/(1 + 2ν)", "Always in [−1, 1]", "Unconditional"],
    ],
)

add_h("7c. The 27-cell FTCS prediction (Test 2)", level=2)
add_para("Plugging each substrate's top-cell κ, top-cell Δz, and the three Δt values into ν = κΔt/Δz² gives the FTCS stability picture in advance:")
add_table(
    ["Substrate (top κ, Δz₀)", "ν at Δt=15s", "ν at Δt=60s", "ν at Δt=600s"],
    [
        ["Bare soil  (2.31e-7 m²/s, 1.0 cm)",     "0.035 ✓",       "0.139 ✓",      "1.39 ✗ (mild)"],
        ["Asphalt road (3.75e-7 m²/s, 0.5 cm)",   "0.225 ✓",       "0.900 ✗",      "9.00 ✗ (catastrophic)"],
        ["Concrete roof (7.14e-7 m²/s, 0.5 cm)",  "0.428 ⚠",      "1.71 ✗",       "17.14 ✗ (catastrophic)"],
    ],
)
add_callout("Test 2 then confirmed these predictions: FTCS blew up at Δt=60s on asphalt and concrete, at Δt=600s on all three substrates (mildly on soil). BTCS and CN completed every run.")

# -----------------------------------------------------------------
add_h("8. The Two Experiments — Test 1 and Test 2", level=1)

add_h("Test 1 — Verification (does the solver work?)", level=2)
add_table(
    ["Setting", "Value"],
    [
        ["Substrate",          "Uniform sandy loam (1 material, no layers)"],
        ["Grid",               "Uniform Δz = 1 cm everywhere"],
        ["Surface BC",         "Prescribed: T_s⁰(t) = 292.5 + 7.5·cos(ω t) K"],
        ["Bottom BC",          "Zero-flux Neumann at z = 2 m"],
        ["Reference",          "Closed-form analytical damping-depth solution"],
        ["Integration",        "5 diurnal cycles; day-5 used for diagnostics"],
        ["Configurations",     "6: FTCS at ν=0.4 and ν=0.6; BTCS and CN at Δt=300 s and 900 s"],
        ["Question answered",  "Does the solver reproduce the textbook analytical answer? (Yes.)"],
    ],
)
add_para(
    "FTCS at ν = 0.6 was predicted to blow up. It did, at step 53 — matching the predicted "
    "geometric growth factor |1 − 4·0.6|^53 ≈ 5.5×10⁷ per step. Confirmation of the theory.",
)

add_h("Test 2 — Prognostic SEB (what we actually wanted to know)", level=2)
add_table(
    ["Setting", "Value"],
    [
        ["Substrate",          "Three: asphalt road, concrete roof, bare soil"],
        ["Grid",               "Stretched per-substrate: top 0.5-1 cm, geometric stretch 1.18-1.25, bottom ≈ 30 cm"],
        ["Surface BC",         "Prognostic: T_s⁰ from SEB Newton iteration (top BC §6a above)"],
        ["Bottom BC",          "Zero-flux Neumann at z = 2 m"],
        ["Reference",          "FTCS at Δt = 15 s on the same substrate"],
        ["Integration",        "2 diurnal cycles; day-2 used for diagnostics"],
        ["Configurations",     "27: 3 substrates × 3 schemes (FTCS/BTCS/CN) × 3 Δt (15 / 60 / 600 s)"],
        ["Question answered",  "How do FTCS, BTCS, CN compare at operational time steps on real urban substrates?"],
    ],
)

# -----------------------------------------------------------------
add_h("9. Algorithm — What Runs Inside One Time Step", level=1)
add_para("For each substrate × scheme α × Δt cell of the matrix, the following loop executes:")
add_code_block([
    "for step in range(N_steps):",
    "    # SUB-STEP A: column update (theta-method)",
    "    G_half = harmonic_mean_lambda * (T - T_neighbour) / dz_centre   # half-level fluxes",
    "    if alpha == 0:",
    "        # FTCS — explicit, no linear system",
    "        T_new = T + dt / (C * dz) * (G_half[:-1] - G_half[1:])",
    "    else:",
    "        # BTCS (alpha=1) or CN (alpha=0.5) — implicit, tridiagonal solve",
    "        A_band, b = build_tridiagonal_system(T, alpha, dt, dz, lambda_half, C)",
    "        T_new = scipy.linalg.solve_banded((1, 1), A_band, b)",
    "",
    "    # Apply bottom BC (zero-flux Neumann)",
    "    T_new[N-1] = T_new[N-2]",
    "",
    "    # SUB-STEP B: SEB update (Newton iteration for new T_s^0)",
    "    Ts0 = Ts0_old",
    "    for _ in range(MAX_ITER):",
    "        F  = R_n(Ts0) - H(Ts0) - LE - G(Ts0, T_new[1])",
    "        dF = dR_n/dT - dH/dT - dG/dT",
    "        dTs = -F / dF",
    "        Ts0 = Ts0 + dTs",
    "        if abs(dTs) < 1e-4: break",
    "",
    "    # Update top cell to the new surface temperature",
    "    T_new[0] = Ts0",
    "",
    "    # Advance time",
    "    T = T_new",
    "    t = t + dt",
    "    record(Ts0, G_half[0])",
])
add_callout(
    "Order of operations is the key design choice: column FIRST (holding T_s⁰ fixed), then "
    "SEB SECOND (holding column fixed). This is the operator splitting that produces the "
    "first-order error analysed in §5.2 of the report."
)

# -----------------------------------------------------------------
add_h("10. What the Results Showed (one-page summary)", level=1)

add_h("From Test 1 (verification)", level=2)
add_bullet("FTCS at ν = 0.4: RMSE_T = 0.007 K — essentially exact.")
add_bullet("FTCS at ν = 0.6: BLEW UP at step 53 — exactly as von Neumann predicted.")
add_bullet("BTCS error grows linearly with Δt (first-order). CN error stays flat (second-order behaviour at this regime).")
add_bullet("Conclusion: solver passes verification. Trust it on Test 2.")

add_h("From Test 2 (prognostic SEB)", level=2)
add_bullet("At Δt = 15 s: all three schemes agree to line-thickness on every substrate. Control condition.")
add_bullet("At Δt = 60 s: FTCS blows up on asphalt (ν=0.90) and concrete (ν=1.71). BTCS and CN run to completion.")
add_bullet("At Δt = 600 s: FTCS catastrophically unstable on asphalt and concrete; mildly unstable on soil. BTCS over-amplifies the diurnal G amplitude by 40 % / 41 % / 19 % (asphalt / roof / soil). CN halves these errors to 21 % / 26 % / 10 %.")
add_bullet("Δt-refinement ratios: all six BTCS and CN values cluster in [8.2, 10.2] — first-order in Δt for both schemes, even though CN is intrinsically second-order. This is the smoking-gun signature of operator-splitting error.")
add_bullet("SHAP attribution on a 150-column synthetic ensemble: κ_top is the dominant predictor of BTCS coarse-Δt error, with R² = 0.92 from κ_top alone.")
add_bullet("Daily storage integral preserved within ±5 % across all schemes — so the over-amplification is symmetric (daytime overshoot + nighttime undershoot), preserving the daily mean. Implication: UHI diurnal range is biased, but UHI daily mean is preserved.")

add_h("Why the operator-splitting error dominates", level=2)
add_para(
    "At every step, sub-step A advances the column with the OLD surface temperature, and "
    "sub-step B then updates the surface temperature with the NEW column. The column "
    "therefore equilibrates to the wrong T_s⁰ during sub-step A, and the discrepancy "
    "manifests as a spurious top-cell gradient. This error is first-order in Δt regardless "
    "of the per-substep scheme — which is why CN (intrinsically second-order) shows the same "
    "ratio of 10 as BTCS (first-order) when Δt scales by 10."
)
add_para(
    "Two fixes were sketched in §5.4 of the report but not implemented: a fully coupled SEB "
    "row in the tridiagonal solve, or a Strang-symmetric splitting (A → B → A with half-step "
    "intervals). Either would eliminate the leading first-order splitting error.",
)

# -----------------------------------------------------------------
add_h("Appendix — The atmospheric forcing functions", level=1)
add_para("Synthetic, fully reproducible, sinusoidal:")
add_equation_block("S↓(t) = max[1000 · cos(ω(t − 12 h)), 0]  W/m²")
add_equation_block("L↓(t) = 350 + 20 · cos(ω(t − 14 h))     W/m²")
add_equation_block("T_a(t) = 292.5 + 7.5 · cos(ω(t − 14 h)) K")
add_equation_block("U(t) = 3 m/s   (constant)")
add_para("with ω = 2π / 86400 s ≈ 7.27 × 10⁻⁵ rad/s (one full cycle per day). Solar peaks at noon; air temperature and longwave peak 2 hours later at 14:00 LT, modelling the typical afternoon thermal lag.")

# -----------------------------------------------------------------
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("— End of cheat-sheet —")
r.italic = True
r.font.color.rgb = GREY
r.font.size = Pt(10)

doc.save("CLIM715_Experiment_Cheatsheet.docx")
print("Wrote CLIM715_Experiment_Cheatsheet.docx")
