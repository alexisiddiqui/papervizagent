# jaxENT Methodology Diagram — Refined Prompt

## Caption
**Fig. X | jaxENT workflow for integrating biophysical experiments with structural ensembles.** Structural hypotheses (e.g., MD or AF2-derived ensembles) are mapped to predicted observables via a forward model, then fit using a maximum-entropy objective that can include covariance/priors while jointly optimising ensemble weights (ω) and model parameters (β); built-in splits and replicates enable robust validation and quantitative hypothesis testing.

---

## Methodology Context

jaxENT is a flexible, interpretable framework for integrating biophysical experimental data with structural ensembles through maximum-entropy reweighting and forward model optimisation. Built on JAX, it enables simultaneous fitting of ensemble weights and model parameters with automatic differentiation, just-in-time compilation, and modular loss functions that can incorporate physics-based constraints, prior knowledge, and data covariance structure. The framework supports robust validation through data splitting and replicates, enabling quantitative structural hypothesis testing across diverse biophysical techniques.

### Inputs
The required inputs to jaxENT are:
1. A set of structural simulations (e.g. AlphaFold structures)
2. A set of experimental data (e.g. HDX-MS Uptake curves)
3. A structure-experimental data forward model (Best-Vendruscolo for HDX - \beta_h, \beta_c - hydrogen bond and heavy contacts)

Optional:
- Orthogonal data for cross validation

jaxENT uses a maximum entropy principle to reweight the structural ensemble to match the experimental data. We extend this principle to the other loss functions such as forward model tuning to account for diverse experimental HDX-MS conditions.

Through customisable loss functions users can incorporate prior knowledge into the fitting process. In this study we leverage physics (Max-ENT) and knowledge of the data structure (covariance) to improve fitting accuracy.

### Process
1. Prepare candidate structural hypotheses (e.g., MD ensemble vs AF2-subsampled ensemble; optional filtering).
2. Compute forward-model features from each frame (e.g., BV model counts H-bonds + contacts; typical \beta_h, \beta_c defaults).
3. Map structures → protection factors → predicted uptake curves (residue model + peptide aggregation + back-exchange correction).
4. Define objective = data-fidelity loss + priors/regularizers.
5. optimise (frame weights; optionally forward-model parameters too) using modern gradient-based optimisation + autodiff.
6. Validate & score hypotheses using held-out splits, replicates, and "work done" metrics / uncertainty summaries.

### Evaluation
Outputs:
1. optimised ensemble weights (reweighted structural ensemble).
2. (Optional) fitted forward-model parameters (BV \beta_h, \beta_c).
3. Model-selection / hypothesis-testing statistics: work metrics (Work_KLD / Work_Scale / Work_Density etc.) and uncertainty across replicates.

jaxENT provides easy interpretation of the results (weights, forward model parameters) as well as the fitting process. Validated with Ground-truth recovery + Comparison baseline + model selection.

### Results
All-in-one fitting and hypothesis testing — jaxENT can fit frame weights and model parameters while demonstrating exceptional robustness to decoys. Better recovery/robustness vs HDXer in the showcased real world MoPrP cases. Speed/efficiency claims: fewer iterations due to Adam + JIT; 10–15× faster wall-clock than HDXer for certain fitting settings; "minutes rather than hours" — fast enough to be done on a laptop. Limitations arise due to simplistic models used for integration — jaxENT's modular architecture for users to develop and implement their own models and objectives.

---

## Detailed Figure Description (Aesthetically Refined)

### Global Style Directives

**Figure title** (top-left, bold, 16 pt, sans-serif Helvetica/Arial, color `#1A1A2E`):
"jaxENT workflow for ensemble–experiment integration and hypothesis testing"

**Overall aesthetic:** "Soft Tech & Scientific Pastels" — clean, modular, with clear left-to-right narrative flow. This is a computational biophysics systems paper, so the vibe is **clean modularity with scientific precision**: approachable but not cartoony, structured but not austere.

**Canvas:** Wide landscape, approximately 2.2:1 aspect ratio. Background: pure white (`#FFFFFF`).

**Layout structure:** Three main left-to-right columns (panels) with bold panel labels **(a)**, **(b)**, **(c)** in the upper-left of each section. Panel labels: 14 pt bold sans-serif, dark navy (`#1A1A2E`). There is a dashed line that crosses from (a.2) Optional Input, routes beneath panel (b) along the bottom of the canvas, and connects to the 'orthogonal/reference distribution' thumbnail in (c.3) Interpretable Outputs

---

### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **Panel (a) zone fill** | Pale Blue / Ice | `#E6F3FF` at ~12% opacity | Light wash behind entire panel (a) container |
| **Panel (b) zone fill** | Pale Lavender | `#F3E5F5` at ~12% opacity | Light wash behind entire panel (b) container |
| **Panel (c) zone fill** | Mint / Sage | `#E0F2F1` at ~12% opacity | Light wash behind entire panel (c) container |
| **Active / trainable elements** | Warm Coral | `#E8735A` | optimisation block border, ω/β icons, "optimise" header accent |
| **Core process modules** | Medium Teal | `#4CA6A8` | Forward-model steps, prediction boxes, feature computation |
| **Objective / loss highlight** | Soft Gold | `#D4A94B` | "Objective" block header underline, "MaxEnt Work" highlight |
| **Frozen / static inputs** | Cool Slate Grey | `#8E99A4` | Input data icons, structural ensemble outlines |
| **Best hypothesis / final output** | Bright Gold | `#D4A017` | "Best hypothesis" label and highlight border only |
| **Internal step boxes** | White | `#FFFFFF` | All interior step-boxes within modules |
| **Text — primary** | Dark Navy | `#1A1A2E` | All headers, labels |
| **Text — secondary** | Medium Grey | `#5A6270` | Subtitles, captions, annotations |
| **Borders — modules** | Charcoal | `#3A3A4A` | Thin (1–1.5 pt) borders on all rounded rectangles |
| **Borders — optional/dashed** | Medium Grey | `#8E99A4` | Dashed borders for optional elements |

---

### Visual Language (Global Rules)

**Shapes:**
- **All process nodes and modules:** Rounded rectangles, corner radius 8 px, thin charcoal border (1.5 pt `#3A3A4A`).
- **Data elements** (structural ensembles, uptake curves): Flat representations within rounded containers — no 3D cuboids unless explicitly showing tensor dimensionality.
- **Grouping containers** (the three panel zones): Very large rounded rectangles with the pastel zone fills above, thin (1 pt) charcoal solid border.
- **Optional elements:** Dashed border (`#8E99A4`, dash pattern 6-4), no fill or very faint cream fill (`#FBF9F4`).

**Arrows:**
- **Primary flow arrows** (between panels a→b→c): Thick (3 pt) dark charcoal (`#3A3A4A`) solid arrows with clean triangular arrowheads — rendered as large chevron-style connectors (like the existing design's `▶` chevrons, but refined with slight rounding).
- **Internal flow arrows** (within panels): Thinner (1.5 pt) charcoal solid arrows with small arrowheads. Use **orthogonal / elbow connectors** for the vertical chain inside panel (b) to convey precision.
- **Auxiliary / optional arrows** (dashed): 1.5 pt dashed grey (`#8E99A4`) for the cross-validation feed from panel (a) to panel (c).

**Typography:**
- **Panel headers** (e.g., "Inputs and structural hypotheses"): 14 pt bold sans-serif (Helvetica/Arial), dark navy `#1A1A2E`.
- **Module titles** (e.g., "jaxENT (JAX-based fitting engine)"): 12 pt bold sans-serif, dark navy.
- **Internal step labels** (e.g., "Compute forward-model features per frame"): 9–10 pt regular sans-serif, dark navy.
- **Sub-annotations and captions** (e.g., "Prevent overfitting; quantify uncertainty"): 8–9 pt italic sans-serif, medium grey `#5A6270`.
- **Mathematical variables** ($\omega$, $\beta$, $\varepsilon_h$, $\varepsilon_c$, $\mathcal{L}$): Serif font (Times New Roman / LaTeX default), italicized. This is critical — all Greek letters and mathematical symbols must be serif and italic, distinct from sans-serif labels.
- **Equation text** (the objective line): Serif italic for variables, sans-serif regular for function names like "Data-fidelity."

**Badges / Tags** (e.g., "gradient-based (Adam)", "autodiff", "JIT"):
- Small rounded pill shapes (corner radius 10 px), fill: light teal (`#E0F2F1`), border: medium teal (`#4CA6A8`) at 1 pt, text: 7–8 pt regular sans-serif in teal (`#4CA6A8`).

---

### Panel (a): Inputs and Structural Hypotheses (Left Column)
**Zone fill:** Pale Blue / Ice (`#E6F3FF` at ~12% opacity), large rounded rectangle.

#### (a.1) Required Inputs Block (main content area)
A large rounded rectangle (corner radius 8 px, white fill, thin charcoal border) labeled **"Required inputs"** (12 pt bold sans-serif, dark navy).

**Internal layout:** Three columns arranged left-to-right: **Structural ensembles** (left) → **Forward model** (center, acting as the connector) → **Experimental data** (right). This arrangement visually encodes the candidate→target mapping.

**Timescale gap annotation (integrated):** A small horizontal gradient bar spans the top of the Required Inputs box, from teal (`#4CA6A8`, left) to coral (`#E8735A`, right). Above the left end: "Candidate (fs–ns)" in 8 pt sans-serif; above the right end: "Target (ms–hours/days)" in 8 pt sans-serif. Centered above the bar in italic: "*timescale gap*" (8 pt italic, medium grey). Below the bar, centered: "Integration acts as a statistical connector" (7 pt italic, medium grey). This ribbon is compact — a thin decorative strip, not a full sub-panel.

**The three input groups (left → center → right):**

1. **Structural simulations / candidate ensembles** (LEFT — "Candidate")
   - A small label above or beside the icon: **"Candidate"** (9 pt bold sans-serif, teal `#4CA6A8`) to link to the timescale bar's left end.
   - Icon: stacked translucent protein ribbon cartoons (multiple overlaid structures rendered in cool slate grey with slight transparency to imply ensemble). Keep as 2D flat illustration style, not 3D isometric.
   - Text below icon: "Structural ensembles" (10 pt bold sans-serif), "(e.g., MD, AF2 subsampling)" (8 pt regular, medium grey).
   - Small sublabels beneath in a vertical list (8 pt regular, medium grey): "Molecular Dynamics", "AlphaFold2 + MSA subsampling", "Enhanced sampling / clustering".

2. **Forward model** (CENTER — the connector between candidate and target)
   - Positioned centrally between the structural ensembles and experimental data, visually bridging the two. A thin arrow enters from the left (from ensembles) and a thin arrow exits to the right (toward experimental data), making the forward model the explicit mapping step.
   - Icon: small rounded box (corner radius 6 px) with thin teal border (`#4CA6A8`), light teal fill (`#E0F2F1`), labeled "Forward model" (9 pt bold sans-serif) with subtext "BV (\beta_h, \beta_c, ω)" in 8 pt serif italic for the variables, sans-serif for "BV".
   - Beneath: "(Best–Vendruscolo)" in 7 pt sans-serif, medium grey.
   - This central placement emphasises that the forward model is the statistical connector bridging the timescale gap.

3. **Experimental observables** (RIGHT — "Target")
   - A small label above or beside the icon: **"Target"** (9 pt bold sans-serif, coral `#E8735A`) to link to the timescale bar's right end.
   - Icon: a small line plot of HDX uptake curves — multiple thin colored curves (use a sequence: teal, coral, gold, soft purple — `#4CA6A8`, `#E8735A`, `#D4A94B`, `#9B8EC4`) plotted against time. Axes labeled "HDX uptake" (y) and "time" (x) in 7 pt sans-serif.
   - Text: "Experimental data" (10 pt bold), "(e.g., HDX-MS uptake curves)" (8 pt regular, medium grey).
   - Below: "or NMR Protection Factors" (8 pt regular, medium grey).

#### (a.2) Optional Input (bottom subsection connected to middle)
A **dashed-outline** rounded rectangle (corner radius 8 px, dash pattern 6-4, border `#8E99A4`, very faint cream fill `#FBF9F4`) labeled "Optional: orthogonal data for cross-validation" (9 pt regular sans-serif, medium grey). A dashed arrow (1.5 pt `#8E99A4`) exits rightward and routes **beneath panel (b)** — running along the very bottom of the canvas as a long horizontal dashed line, passing under/behind the jaxENT fitting engine, then turning upward on the right side to terminate at the "orthogonal/reference distribution" thumbnail in (c.3) Outputs. This arrow must not overlap or intersect any of panel (b)'s internal step-boxes; it should travel clearly below them in its own visual lane.

---

### Panel (b): jaxENT Fitting Engine (Center Column)
**Zone fill:** Pale Lavender (`#F3E5F5` at ~12% opacity), large rounded rectangle.

**Panel subtitle** (below panel header): "compute → predict → objective → optimise" in 9 pt regular sans-serif, medium grey `#5A6270`.

#### (b.1) Feature Computation and Prediction Stack
subheading "autodiff + JIT + modular losses" (9 pt regular sans-serif, medium grey).

Inside, a **vertical chain** of white step-boxes connected by **orthogonal elbow arrows** (1.5 pt charcoal, downward):

**Step 1:** Rounded rectangle (white fill, thin teal border `#4CA6A8`, corner radius 8 px):
- Label: "Compute forward-model features per frame" (9 pt sans-serif).
- Small annotation right of the text (light teal fill): Matrix/heatmap showing "Residues,frames (x H-bonds, contacts)" (7 pt sans-serif).
- Below within the same box or as a connected sub-step: "Structure → protection factors" (9 pt sans-serif). The arrow (→) rendered as a small inline glyph.

**Step 2:** Rounded rectangle (white fill, thin teal border, corner radius 8 px):
- Label: "Predict uptake curves" (9 pt bold), "(residue → peptide aggregation + correction)" (9 pt regular).
- Small mini-graphic on the right side: two tiny line-plots side by side — left labeled "residue" (single smooth curve in teal), right labeled "peptide" (aggregated stepped/smoothed curve in coral), connected by a small curved arrow to indicate aggregation.

#### (b.2) Objective Function Block (center highlight)
A wide rounded rectangle with **soft gold accent**: thin gold border (`#D4A94B`, 2 pt) or a gold top-stripe / header underline to distinguish it from other boxes. White fill. Corner radius 8 px.

- **Header:** "Define Objective" (12 pt bold sans-serif, dark navy), with a thin gold underline beneath.
- **Graphic:** right of the text/equations, outside of the header:
Symbols for error, work, constraints are being fed into a funnel pointed down into a gear/cog icon (dark blue)  
- **Equation line** (centered, 10 pt):
  *L* = Target Reconstruction (Error) + MaxEnt (Work) + Priors/Constraints
  - *L* in serif italic (gold-highlighted or gold-colored to draw the eye).
  - "MaxEnt (Work)" with a subtle gold background highlight pill behind it (very light gold `#FDF4E3`, rounded, inline) and a tiny annotation below: "Regularisation" in 7 pt italic serif, medium grey.
  - "Data-fidelity" and "Priors/Constraints" in sans-serif regular.
- **Branch row** beneath (two side-by-side small boxes):
  - Left: "Error + Work" with label "(baseline)" in 7 pt grey below.
  - Right: "Error + Constraints + Work" with label "(physics/knowledge)" in 7 pt grey below.
  - Both boxes: white fill, thin charcoal border, corner radius 6 px. The right box could have a very subtle teal left-border accent (2 pt teal stripe on left edge) to visually suggest the "enhanced" variant.



#### (b.3) optimisation Block (bottom)
A rounded rectangle with **warm coral accent**: thin coral border (`#E8735A`, 2 pt) or a coral top-stripe. White fill. Corner radius 8 px. Ensure there is space for the arrow from 'orthogonal data for cross validation'

- **Header:** "optimise" (12 pt bold sans-serif, dark navy).
- **Two output items** with small icons:
  - **ω** (serif italic, coral-colored): "frame weights" — icon: tiny bar-chart pictogram in coral tones.
  - **β** (serif italic, coral-colored): "forward-model parameters" — icon: tiny slider/knob pictogram in coral tones.
- Caption: "Simultaneous fitting of weights and parameters" (8 pt italic sans-serif, medium grey).
- **Three pill badges** in a horizontal row below:
  - "autodiff" — pill with light teal fill, teal border/text.
  - "JIT" — same pill style.
  - "Extensible" — same pill style.

---

### Panel (c): Validation, Scoring, and Hypothesis Testing (Right Column)
**Zone fill:** Mint / Sage (`#E0F2F1` at ~12% opacity), large rounded rectangle.

**Panel subtitle:** "quantifying robustness" in 9 pt regular sans-serif, medium grey.

#### (c.1) Validation Pipeline (top)
A large rounded rectangle (white fill, charcoal border, corner radius 8 px) titled **"Validation (built-in)"** (11 pt bold sans-serif, dark navy) containing three small boxes in a horizontal row:

- "Split types / Replicates" — white fill, thin charcoal border, 9 pt sans-serif.
- "Robust success metrics" — white fill, thin charcoal border, 9 pt sans-serif.
- "Cross-validation (orthogonal data)" — white fill, **dashed border** (`#8E99A4`) to visually match the optional input from panel (a), 9 pt sans-serif.

Below the row: "Prevent overfitting; quantify uncertainty" (8 pt italic sans-serif, medium grey `#5A6270`).

#### (c.2) Scoring and Model Selection (middle)
A box titled **"Hypothesis testing & model selection"** (11 pt bold sans-serif, dark navy). White fill, charcoal border, corner radius 8 px.

- **Left side:** Three mini protein-stack icons (flat 2D overlaid ribbon illustrations, each tinted a different pastel — teal, coral, lavender) labeled H₁ (0%), H₂ (85%), H₃ (15%) beneath in 8 pt sans-serif. Label below group: "Candidate ensembles" (8 pt regular, medium grey).
- **Center:** An arrow (1.5 pt charcoal) pointing into a **scorecard mini-table** rendered as a small clean table:
  - Header row: "scorecard" (8 pt bold sans-serif).
  - Rows (8 pt regular sans-serif):
    - Work_KLD, Work_Scale... (subscripts in serif italic)
    - held-out error
    - Replicate Uncertainty
  - Table border: thin charcoal lines, alternating row fill: white / very faint lavender (`#F9F5FC`).
- **Right side:** Arrow to a single highlighted **"Best hypothesis"** ensemble icon with a bright gold border (`#D4A017`, 2 pt) and label "Best hypothesis" in 10 pt bold sans-serif, bright gold.

#### (c.3) Interpretable Outputs (bottom)
A final rounded rectangle titled **"Outputs (interpretable)"** (11 pt bold sans-serif, dark navy). White fill, charcoal border, corner radius 8 px.

Three small thumbnail-sized representative visuals in a horizontal row:

1. **Weight distribution** — tiny bar chart icon in teal tones, labeled *ω* (serif italic) above and "weight distribution" (7 pt sans-serif, grey) below. An 'orthogonal/reference distribution' is drawn behind the bars as a continuous distribution curve. This thumbnail is the explicit termination point of the dashed arrow from (a.2) 'Orthogonal data for cross-validation' — the arrowhead should visibly connect to this element.
2. **Fitted parameters** — two tiny slider icons in coral tones, labeled \beta, *ω* (serif italic) above and "fitted parameters" (7 pt sans-serif, grey) below.
3. **Structural mapping** — small protein cartoon colored by a white-to-black diverging colormap (implying predicted protection / uptake difference), labeled "residue-level Work done" (7 pt sans-serif, grey) below.

Keep these as small thumbnails — enough to signal interpretability without turning the figure into a results panel.

---

### Summary of Style Choices and Rationale

| Style Decision | Rationale (per NeurIPS 2025 Guide) |
|---|---|
| Soft pastel zone fills per panel | "Zone strategy" for grouping stages; avoids saturated backgrounds |
| Teal/Coral/Gold functional palette | Teal = process (cool), Coral = trainable/optimised (warm), Gold = objective/highlight — status-based coloring |
| Rounded rectangles (8 px radius) everywhere | "Softened Geometry" — dominant shape for processes |
| Dashed borders for optional elements only | Dashed = "Optional Paths" or "Scopes" |
| Orthogonal elbow connectors inside panel (b) | Precision-oriented internal flow |
| Thick chevron arrows between panels | Narrative left-to-right flow connectors |
| Sans-serif labels, serif italic math | Strict "Labeling vs Math" separation |
| Pill badges for tech features | Modern, clean way to encode speed/efficiency without clutter |
| No heavy black outlines, no 3D/2D mixing | Avoids "PowerPoint Default" and "Inconsistent Dimension" pitfalls |

---

*You are an expert scientific diagram illustrator. Generate a high-quality, publication-ready scientific diagram following the description above.*