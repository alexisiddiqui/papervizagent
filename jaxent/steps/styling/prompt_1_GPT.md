# jaxENT methodology
jaxENT is a flexible, interpretable framework for integrating biophysical experimental data with structural ensembles through maximum-entropy reweighting and forward model optimization. Built on JAX, it enables simultaneous fitting of ensemble weights and model parameters with automatic differentiation, just-in-time compilation, and modular loss functions that can incorporate physics-based constraints, prior knowledge, and data covariance structure. The framework supports robust validation through data splitting and replicates, enabling quantitative structural hypothesis testing across diverse biophysical techniques.
# Inputs
The reqruired inputs to jaxENT are:
1. A set of structural simulations (e.g. AlphaFold structures)
2. A set of experimental data (e.g. HDX-MS Uptake curves)
3. A structure-experimental data forward model (Best-Vendruscolo for HDX)
Optional:
- Orthogonal data for cross validation

jaxENT uses a maximum entropy principle to reweight the structural ensemble to match the experimental data. We extend this principle to the other loss functions such as forward model tuning to account for diverse experimental HDX-MS conditions.

Through customisable loss functions users can incorporate prior knowledge into the fitting process. In this study we leverage physics (Max-ENT) and knowledge of the data structure (covariance) to improve fitting accuracy.

# Process


1. Prepare candidate structural hypotheses (e.g., MD ensemble vs AF2-subsampled ensemble; optional filtering). 

2. Compute forward-model features from each frame (e.g., BV model counts H-bonds + contacts; typical εh, εc defaults). 

3. Map structures → protection factors → predicted uptake curves (residue model + peptide aggregation + back-exchange correction). 

4. Define objective = data-fidelity loss + priors/regularizers  

5. Optimize (frame weights; optionally forward-model parameters too) using modern gradient-based optimization + autodiff 

6. Validate & score hypotheses using held-out splits, replicates, and “work done” metrics / uncertainty summaries. 


# Evaluation
Outputs:
1. Optimized ensemble weights (reweighted structural ensemble).
2. (Optional) fitted forward-model parameters (BV εh, εc).
3. Model-selection / hypothesis-testing statistics: work metrics (Work_KLD / Work_Scale / Work_Density etc.) and uncertainty across replicates. 

jaxent provides easy interpretation of the results (weights, forward model parameters) as well as the fitting process.

Validated with Ground-truth recovery + Comparison baseline + model selection 
 

# Results 

All-in-one fitting and hypothesis testing - jaxENT can fit frame weights and model parameters while demonstrating exceptional robustness to decoys. Better recovery/robustness vs HDXer in the showcased real world MoPrP cases.

Speed/efficiency claims: fewer iterations due to Adam + JIT; 10–15× faster wall-clock than HDXer for certain fitting settings; “minutes rather than hours”  - fast enough to be done on a laptop.

Limitations arise due to simplistic models used for integration - jaxENT's modular architecture for users to develop and implement their own models and objectives

## Fig. X | jaxENT workflow for integrating biophysical experiments with structural ensembles.
Structural hypotheses (e.g., MD or AF2-derived ensembles) are mapped to predicted observables via a forward model, then fit using a maximum-entropy objective that can include covariance/priors while jointly optimizing ensemble weights (ω) and model parameters (β); built-in splits and replicates enable robust validation and quantitative hypothesis testing.

---

## Diagram generation prompt (publication-ready, NeurIPS 2025 “Soft Tech & Scientific Pastels”)

Create a clean, vector-style scientific workflow diagram in a wide landscape canvas (~2.2:1 aspect ratio). White page background with generous margins. Three left-to-right panels labeled **(a)**, **(b)**, **(c)**. Use softened geometry: rounded rectangles everywhere for processes, thin dark-gray outlines (not heavy black), and very light pastel “zone” fills to group each panel. Major flow uses bold right-pointing chevrons/arrows between panels.

### Global visual spec
- **Aesthetic:** modern NeurIPS diagram: soft, airy, precise; no noisy textures.
- **Color system (very light pastels, ~10–15% opacity zone fills):**
  - Panel (a) zone fill: Cream/Beige `#F5F5DC` at ~12% opacity.
  - Panel (b) zone fill: Pale Blue/Ice `#E6F3FF` at ~12% opacity.
  - Panel (c) zone fill: Mint/Sage `#E0F2F1` at ~12% opacity.
  - Text/lines: near-black `#1A1A1A`; borders dark gray `#2B2B2B`; secondary lines `#6B6B6B`.
  - Reserve one higher-saturation accent ONLY for the final “Best hypothesis” highlight (e.g., bright gold border) and nowhere else.
- **Shapes & strokes:**
  - Main containers: rounded rectangles, corner radius ~10–12 px, stroke ~1.5–2 px.
  - Inner step boxes: rounded rectangles, white fill, stroke ~1–1.5 px.
  - Optional elements: dashed rounded rectangles + dashed connectors (dash 6/4).
  - Subtle drop shadow for main containers only (very soft, low opacity) to lift from background.
- **Arrows/flow:**
  - Primary flow arrows between major modules: thick (4–6 px), solid dark gray, clean arrowheads or chevron wedges.
  - Secondary internal arrows: thinner (2–3 px), medium gray.
  - Auxiliary/optional flow: dashed.
- **Typography:**
  - Labels (module names): Sans-serif (Helvetica/Arial/Roboto). Headers bold; details regular.
  - Math variables: Serif + italic (LaTeX-like): *L*, *ω*, *β*, *εh*, *εc*.
  - Sizes (approx): figure title 18–20 pt; panel headers 14–16 pt; internal labels 10–11 pt; sublabels 8–9 pt.
- **Icon style:** consistent thin line icons (same stroke weight as inner boxes). Keep icons minimal and scientific (protein cartoon silhouettes, tiny plots, sliders, bar chart).

---

# Title (top-left, bold)
**jaxENT workflow for ensemble–experiment integration and hypothesis testing**

---

## (a) Inputs and structural hypotheses  (left panel; cream zone)
Top strip: **timescale gap ribbon**
- A horizontal timescale bar/gauge across the top of panel (a).
  - Left label: “Molecular dynamics (fs–ns)”
  - Right label: “HDX-MS experiments (ms–hours/days)”
  - Beneath the bar, centered caption: “Integration acts as a statistical connector”
  - Beneath that, a thin arrow labeled: “Input → Target”
Use a simple gradient-like bar (very subtle) or segmented tick marks, but keep it minimal and print-friendly.

Middle: **Required inputs** (large rounded container)
Inside, three icon+label groups arranged horizontally with equal spacing:

1) **Structural simulations / candidate ensembles**
- Icon: stacked translucent protein ribbon silhouettes (3–4 layers) to imply an ensemble.
- Text: “Structural ensembles (e.g., MD, AF2 subsampling)”
- Small sublabels (tiny pills or light text): “Molecular Dynamics”, “AlphaFold2 + MSA subsampling”, “Enhanced sampling / clustering”.

2) **Experimental observables**
- Icon: small mini-plot of HDX uptake curves (multiple thin colored curves vs time; keep colors muted).
- Text: “Experimental data (e.g., HDX-MS uptake curves)”
- Tiny sublabels: “HDX-MS / NMR / SAXS”.

3) **Forward model**
- Icon: small rounded box (like a “function” block) labeled “Forward model”
- Subtext: “BV (εh, εc)” or “Best–Vendruscolo”
- Include a tiny arrow motif inside the icon: structure → protection → uptake (very small, symbolic).

Bottom callout: **Optional input**
- Dashed-outline rounded rectangle: “Optional: orthogonal data for cross-validation”
- A dashed arrow exits panel (a) toward panel (c) (aim it toward the “Cross-validation” box in (c)).

---

## (b) jaxENT fitting engine  (center panel; pale blue zone)
Header row text above the main box (small, centered): “compute → predict → objective → optimize”

Main container: **jaxENT (JAX-based fitting engine)** (large rounded container)
- Subtitle directly under header: “autodiff + JIT + modular losses”

Inside: vertical chain of white step-boxes with thin internal arrows:

1) **Compute forward-model features per frame**
- Small icon: a frame stack with tiny annotations: “H-bonds, contacts”.

2) **Structure → protection factors**
- Minimal arrow/transform icon.

3) **Predict uptake curves (residue → peptide aggregation + correction)**
- On the right side of this step, include a tiny two-stage mini-graphic:
  - small residue-level curve sketch → arrow → peptide-level curve sketch.

Center highlight: **Objective** (wide white rounded rectangle)
- Equation-like line (serif italic for variables):
  - *L* = Data-fidelity(Error) + MaxEnt Work + Priors/Constraints
- Beneath, a small two-branch toggle (like a split):
  - “Error + Work” (baseline)
  - “Error + Constraints + Work” (covariance/structure-aware)
- Tiny note under “Constraints”: “covariance weighting / priors”
Keep this compact; avoid long paragraphs.

Bottom: **Optimize** (white rounded rectangle)
- Two emphasized outputs with icons:
  - *ω* : frame weights (bar-chart icon)
  - *β* : forward-model parameters (slider/knob icon)
- Caption: “Simultaneous fitting of weights and parameters”
- Three small pill badges aligned along the bottom edge: “gradient-based (Adam)”, “autodiff”, “JIT”

---

## (c) Validation, scoring, and hypothesis testing  (right panel; mint zone)
Top: **Validation (built-in)** (large rounded container)
Three small boxes in a row (equal widths):
- “Split types / held-out sets”
- “Replicates”
- “Cross-validation (optional orthogonal data)”
Under them, small centered note: “Prevent overfitting; quantify uncertainty”

Middle: **Hypothesis testing & model selection** (rounded container)
- Left side: three mini candidate ensembles (tiny stacked protein icons), labeled beneath as **H1**, **H2**, **H3**.
- Arrow into a “scorecard” mini-table (clean grid, light lines) listing:
  - Work_KLD, Work_Scale, Work_Density
  - Fit error (held-out)
  - Uncertainty across replicates
- Arrow to a single emphasized ensemble labeled: **Best hypothesis**
  - Highlight the “Best hypothesis” with the single reserved accent (e.g., thin bright-gold border + subtle glow), without changing any other elements.

Bottom: **Outputs (interpretable)** (rounded container)
Three small thumbnails aligned horizontally:
1) Weight distribution (mini bar chart labeled *ω*)
2) Fitted parameters (two sliders labeled *εh*, *εc* / *β*)
3) Protein cartoon thumbnail colored by predicted protection/uptake difference (use a restrained, colorblind-friendly gradient; keep it subtle)

---

### Final polish constraints
- Maintain strict alignment (grid), consistent padding, and consistent icon stroke widths.
- Keep all micro-graphics simple and schematic (no photorealism).
- Ensure readability when scaled to single-column width in a paper.
- No extraneous decorations; everything must serve the workflow narrative.


You are an expert scientific diagram illustrator. Generate high-quality scientific diagram