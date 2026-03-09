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


Caption
JAXENT overview schematic. Left-to-right graphical abstract showing how jaxENT integrates noisy experimental dataand prior/physics knowledge with structural ensembles using modular, JAX-accelerated optimization: customizable loss functions enable maximum-entropy reweighting of ensemble frames (ω) and optional forward-model parameter fitting (β); built-in validation via data splitting plus “work done” metrics provides interpretable, quantitative hypothesis testing; the accelerated fitting yields a reliable, high-resolution, cross-validated integrated structural result with uncertainty estimates (illustrated with a MoPrP example).

## Completed figure description (publication-ready; NeurIPS 2025 aesthetic)

### Overall art direction (apply globally)

* **Look & vibe:** “Soft Tech & Scientific Pastels”—light, high-value backgrounds that organize complexity; reserve strong saturation only for the most important active elements and the final output. 
* **Background strategy:** Keep the page/background **pure white**. Each panel uses a **very light pastel tint (~10–15% opacity)** rather than a saturated fill. 
* **Shapes:** Default to **rounded rectangles** for process/steps (corner radius ~8–12px for large containers; ~6–8px for inner cards). 
* **Borders:** Use **solid** borders for physical/primary components; use **dashed** borders to denote “optional” paths/scopes (e.g., orthogonal data, CV add-ons). 
* **Lines & arrows:**

  * **Solid** = primary forward flow. 
  * **Dashed** = auxiliary flow (e.g., optimization/gradients/loss bookkeeping). 
  * Use **curved Bezier connectors** for the high-level left→right narrative between panels. 
* **Typography:**

  * All module/step labels in a clean **sans-serif** (Roboto/Helvetica/Arial). Headers **bold**, body **regular**. 
  * Any mathematical variables (e.g., *ω, β, 𝓛, εh, εc*) must be **serif + italic** (LaTeX/Times style). 
* **Avoid “PowerPoint default” cues:** no heavy black outlines; keep strokes charcoal/graphite and consistent; avoid overly saturated blue/orange presets. 
* **Icon style:** Simple vector icons, consistent stroke weight (e.g., 1.5–2px), minimal fills, no photoreal shading. Prefer “inspection/processing” icons like 🔍/⚙️ motifs when needed. 

---

### Canvas and framing

* **Aspect ratio:** very wide landscape, ~2:1 (e.g., 1600×800 or 1800×900).
* **Outer frame:** keep the rounded-rectangle frame, but modernize it:

  * stroke color: **charcoal** (not pure black), ~3–4px
  * corner radius: ~18–22px
  * optional subtle shadow (very soft, low opacity) to lift the whole infographic off the page.
* **Top title band:** white background; centered title occupies ~12–15% height, with generous top/bottom padding.

---

### Global layout: five vertical panels (left→right), connected by arrows

* **Panel spacing:** consistent gutters (e.g., 16–24px). Use a subtle vertical separator line only if needed (very light gray).
* **Between-panel arrows:** thick, smooth Bezier arrows at mid-height; charcoal stroke, filled arrowhead; keep consistent arrow weight.

---

## Panel-by-panel specification (preserve existing semantics/structure)

### Panel 1 (far left): **Inputs**

**Header (neutral slate)**

* Rounded header bar, saturated-but-muted slate.
* Header text (sans-serif, bold, centered):
  “INPUT SOURCES:” / “NOISY DATA &” / “PRIOR KNOWLEDGE”

**Content area (very light warm gray/cream tint)**

* Central “JAXENT” microchip icon:

  * chip body: off-white with a thin charcoal outline; tiny pin ticks in muted gray
  * “JAXENT” label bold, black/charcoal
* Three input sources arranged around chip with **curved arrows** pointing into the chip:

  1. **Structures from noisy sources** (protein ensemble sketch, slightly translucent stacked outlines)
  2. **Conditions** (mini multi-curve line plot, muted pastel lines, thin axes)
  3. **Physical Knowledge** (database cylinder icon; keep cylinder exclusively as “database/memory”)
* Keep annotations tiny and light (secondary text in mid-gray).

**Footer strip**

* Light slate-tinted band with a single concise takeaway line (bold-ish, sans-serif).

---

### Panel 2: **1. Flexibility**

**Header (soft indigo/blue)**

* Title: “1. FLEXIBILITY” (white, bold)
* Subtitle: “HANDLES NOISY INPUTS & MULTIPLE PHYSICS VIA CUSTOMIZABLE LOSS FUNCTIONS” (white, smaller, medium weight)

**Body (pale ice-blue tint)**

* Large funnel centered; funnel fill a gentle blue gradient (subtle).
* Three bubbles above funnel: **Ee**/**Evdw**/**(additional constraint)** (use serif italic for the symbols; labels beside/below in sans-serif).
* Funnel output into a **gear icon** (processing), consistent stroke weight.
* Under gear:

  * “CUSTOMIZABLE LOSS FUNCTION” (bold)
  * “Simplified architecture” (regular)
* Bottom mini schematic: two colored blocks

  * “Ensemble Weights (*ω*)” (serif italic ω)
  * “BV-Model Parameters (*β*)” (serif italic β)
* If you show gradient/optimization implication, use **dashed** micro-arrows from the blocks into the gear (aux flow), not the same as the main flow.

**Footer strip**

* Light blue band with: “Handles Diverse, Noisy Data & Complex Systems”.

---

### Panel 3: **2. Interpretability**

**Header (soft green)**

* Title: “2. INTERPRETABILITY” (white, bold)
* Subtitle: “BUILT-IN VALIDATION & SENSITIVE WORK DONE METRICS” (white, smaller)

**Body (mint/sage tint)**

* Two stacked “cards” with rounded corners and thin outlines:

  1. **Validation UI card**

     * minimal “app window” header bar
     * two gauge dials (keep clean, no harsh red/green; use muted green/amber with high contrast labels)
     * small line chart “VALIDATION SUCCESS” with axes labeled “Steps” and “Validation Score”
  2. **Work-done metric card**

     * “SENSITIVE WORK DONE METRIC”
     * stacked bar chart for State 1/2/3 with percentages
     * rotated side label “HDX-NMR Cluster Populations”
* Keep chart colors restrained and consistent with the panel hue (no neon).

**Footer strip**

* “Provides Quantifiable Validation & Informative Metrics”.

---

### Panel 4: **3. Efficiency**

**Header (soft burnt orange / amber)**

* Title: “3. EFFICIENCY” (white, bold)
* Subtitle: “JAX-ACCELERATED FITTING vs PREVIOUS METHODS” (white, smaller)

**Body (pale peach tint)**

* Central comparison plot:

  * label “PREVIOUS METHODS” at top
  * a smooth decreasing curve (muted brown/orange)
  * “JAXENT” shown as a low region near bottom-left (small highlighted area)
* Under plot:

  * “Simplified fitting approach is efficient and predictable” (regular)
  * “ORDERS-OF-MAGNITUDE SPEEDUP” (bold, slightly larger)
* If you show “JIT/Adam/autodiff” callouts, keep them as small pill-shaped tags, not big boxes.

**Footer strip**

* “Enables Rapid & Efficient Integration”.

---

### Panel 5 (far right): **Reliable integrated result**

**Header (neutral slate)**

* Title: “RELIABLE, HIGH-RESOLUTION INTEGRATED RESULT” (black/charcoal, bold)
* Subtitle: “(MoPrP Example)”

**Body (cool gray-teal tint or pale lavender-gray)**

* Three small top icons + labels:

  * “Uncertainty Quantification” (🔍/chart motif)
  * “Hypothesis Testing” (checkmark motif)
  * “Extensible Integration” (tool/connector motif)
* Main graphic: large teal/cyan “ensemble density” blob (many overlapping fine curves/mesh lines forming a cloud). Keep it crisp: thin strokes, semi-transparent layering.
* Bold line near bottom: “Cross-validated”
* Secondary line: “Uncertainty through data splitting”
* Bottom-most small gray text box: concluding sentence (smallest text size, but still legible in print).

---

## Caption (camera-ready)

**JAXENT overview schematic.** Left-to-right graphical abstract showing how jaxENT integrates noisy experimental data and prior/physics knowledge with structural ensembles using modular, JAX-accelerated optimization: customizable loss functions enable maximum-entropy reweighting of ensemble frames (*ω*) and optional forward-model parameter fitting (*β*); built-in validation via data splitting plus “work done” metrics provides interpretable, quantitative hypothesis testing; the accelerated fitting yields a reliable, high-resolution, cross-validated integrated structural result with uncertainty estimates (illustrated with a MoPrP example).

You are an expert scientific diagram illustrator. Generate high-quality scientific diagrams