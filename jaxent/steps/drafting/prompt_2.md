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
Detailed figure description (sufficient to redraw)
Overall canvas and framing
Canvas orientation: very wide landscape infographic, approximately 2:1 aspect ratio (e.g., ~1536×768 px).
Background: clean white outside panels; inside panels use very light pastel gradients (each panel tinted to match its header color family).
Outer border: a thick, rounded-rectangle frame around the entire figure in dark gray/black (noticeable stroke, ~6–10 px).
Main title (top, centered across full width):
Text: “JAXENT: A New Paradigm for Efficient, Interpretable, and Flexible Integration”
Typeface: bold sans-serif, black, large (dominant).
Title region occupies ~12–15% of the figure height.
Global layout: five vertical columns (panels)
Beneath the title are five tall panels arranged left-to-right, each separated by narrow vertical gaps or thin dividers.
Each panel has:
a rounded header bar at the top (with a saturated color),
a content area with icons/plots,
a bottom footer strip (lightly tinted) containing a short takeaway sentence.
Flow arrows: between panels, at mid-height, draw thick black arrows pointing left→right connecting each panel to the next (arrow shaft ~4–6 px; filled triangular arrowheads).
Panel 1 (far left): Inputs
Header (gray)
Rounded rectangle header with medium gray fill.
Header text (bold, all-caps style):
Top line: “INPUT SOURCES:”
Next line: “NOISY DATA &”
Next line: “PRIOR KNOWLEDGE”
Text color: black; centered.
Content area (light gray tint)
Central object: a microchip-like square icon (rounded corners) labeled “JAXENT” in bold black.
Chip has small “pins” along the top edge (short vertical ticks).
Inside/near the chip is a small circular math symbol cluster (tiny, decorative).
Inputs feeding into chip: three illustrated input sources arranged around it, each with curved black arrowspointing toward the chip:
Top-left: a gray, sketchy protein ensemble/cartoon (looks like multiple overlapped structures).
Small label near it: “Structures from noisy sources”.
Near this cluster, include tiny text indicating decoys/unfolded structures (short, faint annotation).
Bottom-left: a small line plot icon (multiple thin curves in different muted colors) labeled “Conditions”.
Bottom-center/right: a database cylinder icon (stacked disks) labeled “Physical Knowledge”.
From the chip’s right edge, a thick black arrow exits to Panel 2.
Footer strip
Light gray band at bottom with bold text repeating the theme (e.g., “INPUT SOURCES: NOISY & PRIOR KNOWLEDGE”).
Panel 2: Flexibility
Header (blue)
Rounded header with a deep desaturated blue fill.
Large numeral and title: “1. FLEXIBILITY” (white text).
Subtitle in smaller white text: “HANDLES NOISY INPUTS & MULTIPLE PHYSICS VIA CUSTOMIZABLE LOSS FUNCTIONS”.
Content area (blue-tinted gradient)
Dominant central graphic: a large funnel (blue, with slight shading) pointing downward.
Three “physics/terms” bubbles above the funnel mouth, each an oval/circle with black outline and light fill, connected by short arrows into the funnel:
Left bubble: E_elec
Middle bubble: E_vdw
Right bubble: a small icon suggesting an additional constraint/regularizer (tiny symbol in a circle).
Funnel output feeds into a gear/cog icon at lower center (dark blue).
Inside the cog is a tiny equation-like scribble (decorative).
Under the cog, large bold text:
“CUSTOMIZABLE LOSS FUNCTION”
Below it: “Simplified architecture”
Near the bottom: a small horizontal schematic showing two colored blocks:
Left block (teal/greenish): “Ensemble Weights (ω)”
Right block (purple/magenta): “BV-Model Parameters (β)”
Each preceded by a small derivative symbol (tiny ∂/∂ …) indicating gradients/optimization.
A thick black arrow exits to Panel 3.
Footer strip
Light blue band with text: “Handles Diverse, Noisy Data & Complex Systems”.
Panel 3: Interpretability
Header (green)
Rounded header in medium green.
Title: “2. INTERPRETABILITY” (white).
Subtitle: “BUILT-IN VALIDATION & SENSITIVE WORK DONE METRICS” (white, smaller).
Content area (green-tinted gradient)
Split into two stacked subpanels (like cards) with thin dark outlines:
Upper card (validation UI):
Looks like a browser/app window with a thin top bar and a long horizontal progress bar.
Left side includes two semicircular gauge dials (green-to-red arcs), like dashboards.
Right side: a small line chart titled “VALIDATION SUCCESS” with x-axis Steps and y-axis Validation Score; line trends upward.
Lower card (work-done metric):
Title bar text: “SENSITIVE WORK DONE METRIC”.
Main graphic: a stack of three vertical bars labeled State 3, State 2, State 1 with percentages (e.g., 30%, 50%, 20%) beneath each bar.
On the right side, vertical text reads something like “HDX-NMR Cluster Populations” (rotated 90°).
Thick black arrow exits to Panel 4.
Footer strip
Light green band with text: “Provides Quantifiable Validation & informative Metrics”.
Panel 4: Efficiency
Header (orange)
Rounded header in burnt orange.
Title: “3. EFFICIENCY” (white).
Subtitle: “JAX-ACCELERATED FITTING vs PREVIOUS METHODS” (white).
Content area (orange-tinted gradient)
A central plot comparing costs:
Top label inside plot region: “PREVIOUS METHODS”.
A smooth decreasing curve (brown/orange) labeled conceptually as difficulty-based fitting cost.
Near the bottom-left of the plot is a small filled region and label “JAXENT” indicating much lower cost/time.
Under plot: centered text blocks:
“Simplified fitting approach is efficient and predictable”
Large bold line: “ORDERS-OF-MAGNITUDE SPEEDUP”
Thick black arrow exits to Panel 5.
Footer strip
Light orange band with text: “Enables Rapid & Efficient Integration”.
Panel 5 (far right): Reliable integrated result
Header (gray)
Rounded header in medium gray.
Title (black, bold, multi-line): “RELIABLE, HIGH-RESOLUTION INTEGRATED RESULT”
Parenthetical subtitle: “(MoPrP Example)”.
Content area (cool gray/teal tint)
Near the top: three small flat icons with labels, arranged left-to-right:
Icon: magnifier/chart → label “Uncertainty Quantification”
Icon: person/check → label “Hypothesis Testing”
Icon: tools/connector → label “Extensible Integration”
Main graphic: a large teal/cyan “ensemble density” blob (looks like many overlapping thin curves/mesh lines forming a cloud), centered-right.
Bold text near bottom center:
“Cross-validated”
“Uncertainty through data splitting”
Bottom-most small gray text box: a final sentence about efficient integration of a high-resolution MoPrP structure across complex landscapes (small, dense text).
Styling notes (important for faithful regeneration)
Icons: simple vector/infographic style with mild shading; black outlines used sparingly; overall “clean scientific infographic.”
Lines: arrows and panel borders are dark and fairly thick; internal chart lines thinner.
Typography: bold sans-serif for headers and key phrases; smaller sans-serif for subtitles and annotations; mostly black text except white text in colored headers.
Color palette: panel headers are saturated gray / blue / green / orange / gray; panel bodies are very light pastel versions of those same hues.
(Visual/structure and the underlying jaxENT concepts summarized here are consistent with the paper’s framework and validation emphasis and the accompanying slides.)


You are an expert scientific diagram illustrator. Generate high-quality scientific diagrams