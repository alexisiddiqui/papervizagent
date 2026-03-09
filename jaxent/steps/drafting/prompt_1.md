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


Short caption (for the figure)
Fig. X | jaxENT workflow for integrating biophysical experiments with structural ensembles. Structural hypotheses (e.g., MD or AF2-derived ensembles) are mapped to predicted observables via a forward model, then fit using a maximum-entropy objective that can include covariance/priors while jointly optimizing ensemble weights (ω) and model parameters (β); built-in splits and replicates enable robust validation and quantitative hypothesis testing.


Detailed figure description for generation (jaxENT methodology)
Figure title (top-left, bold): “jaxENT workflow for ensemble–experiment integration and hypothesis testing”
Overall style should match the slide aesthetics: clean white background, thin black outlines, rounded rectangles, and thick black arrows/chevrons for major flow (as in the “Assemble data → Fitting → Inference” schematic).
Overall layout
Canvas: wide landscape (≈2.2:1 aspect ratio), white background.
Structure: three main left-to-right columns (or panels) with bold panel labels (a), (b), (c) in the upper-left of each section.
Visual language:
Major modules shown as large rounded rectangles with very light pastel fills.
Internal steps shown as smaller white rounded boxes with thin black borders.
Primary flow arrows: thick black arrows pointing right.
Secondary arrows: thinner black/gray arrows inside modules.
Typography: sans-serif (Helvetica/Arial-like). Titles ~14–16 pt bold; internal labels ~9–10 pt.
(a) Inputs and structural hypotheses (left column)
This panel communicates the “data + hypotheses” setup and the motivation: bridging simulation and experiment timescales.

(a.1) Timescale gap ribbon (top strip within panel a)
A horizontal timescale bar/gauge (visual cue similar to the slide) with labels:
Left: “Molecular dynamics (fs–ns)”
Right: “HDX-MS experiments (ms–hours/days)”
Center caption beneath: “Integration acts as a statistical connector”
A thin arrow beneath the bar labeled Input → Target (mirrors slide language).
(a.2) Required inputs block (middle)
A large rounded rectangle labeled “Required inputs” containing three icon+label groups arranged in a row:

Structural simulations / candidate ensembles
Icon: stacked translucent protein cartoons (or multiple ribbons) to indicate an ensemble.
Text under icon: “Structural ensembles (e.g., MD, AF2 subsampling)”
Optional small sublabels beside/under it referencing common sources shown in slides: “Molecular Dynamics”, “AlphaFold2 + MSA subsampling”, “Enhanced sampling / clustering”.
Experimental observables
Icon: a small plot of HDX uptake curves (multiple colored curves vs time) to match slide motifs; optional small labels “HDX-MS / NMR / SAXS” as in the slide list.
Text: “Experimental data (e.g., HDX-MS uptake curves)”
Forward model
Icon: small rounded box labeled “Forward model” with subtext “BV (εh, εc)” (or “Best–Vendruscolo”) to indicate mapping structure→protection→uptake.
(a.3) Optional input (bottom callout)
A dashed-outline rounded rectangle labeled “Optional: orthogonal data for cross-validation” feeding (via dashed arrow) toward panel (c).
(b) jaxENT fitting engine (center column)
This is the core “compute → predict → objective → optimize” pipeline, visually analogous to the slide’s “Fitting / Maximum Entropy Optimisation” stage.

(b.1) Feature computation and prediction stack (top-to-bottom inside a large module box)
Large rounded rectangle titled “jaxENT (JAX-based fitting engine)” with a small subheading “autodiff + JIT + modular losses” (matches the innovation bullets).
Inside it, a vertical chain of white step-boxes:

“Compute forward-model features per frame”
Small icon: frame stack + tiny annotations “H-bonds, contacts”.
“Structure → protection factors”
“Predict uptake curves (residue → peptide aggregation + correction)”
A small mini-graphic on the right: residue-level curve aggregated into peptide-level curve.
(b.2) Objective function block (center highlight)
A wide white rounded rectangle with bold header “Objective” showing a compact equation-like line:

L = Data-fidelity(Error) + MaxEnt Work + Priors/Constraints
Present “Work” explicitly as the MaxEnt regularizer (visual tie-in to slide’s Balance accuracy with plausibility framing).
Include a small toggle/branch beneath:
“Error + Work” (baseline)
“Error + Constraints + Work” (covariance/structure-aware)
Optional tiny note under “Constraints”: “covariance weighting / priors” (kept short).
(b.3) Optimization block (bottom)
A white rounded rectangle with:

Title: “Optimize”
Two outputs emphasized with icons:
ω : frame weights (bar-chart icon)
β : forward-model parameters (slider/knob icon)
A small caption: “Simultaneous fitting of weights and parameters”
Add small badges: “gradient-based (Adam)”, “autodiff”, “JIT” to visually encode speed/efficiency without adding clutter.
(c) Validation, scoring, and hypothesis testing (right column)
This panel communicates robustness: splits/replicates, held-out evaluation, and quantitative hypothesis comparison (as highlighted across the slides).

(c.1) Validation pipeline (top)
A large rounded rectangle titled “Validation (built-in)” with three small boxes in a row:

“Split types / held-out sets”
“Replicates”
“Cross-validation (optional orthogonal data)”
Add a small note beneath: “Prevent overfitting; quantify uncertainty” (consistent with the “prevent overfitting” and “split replicates” messaging).

(c.2) Scoring and model selection (middle)
A box titled “Hypothesis testing & model selection” with:

A small icon row showing multiple candidate ensembles (three mini protein stacks labeled e.g. H1, H2, H3).
An arrow into a scorecard mini-table listing example outputs:
Work_KLD, Work_Scale, Work_Density (as named “work done” metrics)
Fit error (held-out)
Uncertainty across replicates
A final arrow to a single highlighted “Best hypothesis” ensemble.
This aligns with the “Comparative hypothesis testing” framing and the “fitting of parameters and frame-weights” emphasis.

(c.3) Interpretable outputs (bottom)
A final box titled “Outputs (interpretable)” showing three tiny representative visuals:

Weight distribution (bar chart labeled ω)
Fitted parameters (two sliders labeled εh, εc / β)
Structural mapping (protein cartoon colored by predicted protection / uptake difference)
Keep these as small thumbnails—enough to signal interpretability without turning the figure into a results panel.



You are an expert scientific diagram illustrator. Generate high-quality scientific diagram