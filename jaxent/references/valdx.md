# Methodology Description

## Short Description
ValDX is a validation framework that integrates HDX-MS experimental data with structural ensembles from molecular simulations, using overlap-aware data splitting, Maximum Entropy reweighting, and novel "Work Done" metrics to quantitatively test whether proposed protein conformational ensembles genuinely represent solution-state dynamics rather than achieving good fits through overfitting.

## Inputs
- **HDX-MS peptide data**: Experimental deuterium uptake curves measured across overlapping peptide fragments at multiple time points (e.g., 0.167, 1.0, 10.0, 120.0 min). Peptides are filtered to remove short peptides (<5 residues), low-information peptides (saturation difference <0.05), and time points with replicate precision (RSD) exceeding 5%.
- **Structural ensembles**: Collections of candidate protein conformations generated via multiple methods — conventional single-start MD (MD-1Start), multi-start MD (MD-10Start), enhanced sampling MD via Topology Frontier Expansion Sampling (MD-TFES), AlphaFold2 MSA-subsampled and geometrically filtered ensembles (AF2-Filtered), and unfiltered AlphaFold2 ensembles (AF2-MSAss). Each ensemble contains ~10,000–12,700 frames representing distinct structural hypotheses about protein conformational dynamics.
- **Protein 3D structure(s)**: Used as reference for spatial splitting and for computing structural features (heavy-atom contacts, hydrogen bonds) needed by the Best-Vendruscolo (BV) forward model that predicts protection factors from coordinates.

## Process
1. **Assemble Data (Step 1)**: Experimental HDX-MS peptide uptake data is paired with simulated structural ensembles. Peptides are organized in two ways: "Peptide-Clustered" (grouped by sequence region overlap) and "Spatial-proximal" (grouped by 3D structural proximity). HDX uptake curves are measured experimentally across time. Independently, molecular simulations generate a conformational landscape of the protein, producing a cloud of diverse 3D structures. From this cloud, structural hypotheses (distinct conformational clusters) are identified via PCA on pairwise Cα distances. The data is then split into training and validation sets using four strategies: Random Split, Sequential Split, Non-Redundant (Redundancy-Aware) Split, and Spatial Split — the latter two specifically designed to prevent information leakage caused by overlapping peptides sharing residues.

2. **Fitting (Step 2)**: The training peptide data is used for ensemble optimization. Structural features (heavy-atom contacts NC and hydrogen bonds NH) are computed for each conformation. The Best-Vendruscolo model converts these features into residue-level protection factors, which are then used to predict peptide-level fractional deuterium uptake. Maximum Entropy Reweighting adjusts the population weights of each conformation (and optionally the BV model parameters βC, βH) to minimize the discrepancy between predicted and experimental uptake on training peptides, balanced against a regularization term (controlled by γHDXer) that penalizes large deviations from the prior uniform ensemble distribution. This creates a tension between two objectives: minimizing prediction error and maintaining conformational diversity (i.e., minimizing Work Done). Validation error is computed on the held-out peptides. Multiple replicates (3–10) of each split type are run. The optimal γHDXer is selected via a "curve-of-the-knee" algorithm on the work-error tradeoff curve.

3. **Inference (Step 3)**: After optimization, a battery of metrics is computed. Standard metrics include training error (MSETraining), validation error (MSEValidation), and validation error change (ΔMSEopt). Critically, three uptake-independent "Work Done" metrics are computed: Workshape (change in relative pattern of protection factors, analogous to enthalpy), Workscale (change in overall magnitude of protection factors), and Workdensity (reorganization of ensemble-average protection factor distribution, analogous to entropy). Statistical significance is assessed via one-way ANOVA and Tukey's HSD post-hoc tests across ensembles and split types. Metrics are compared across split types (Non-Redundant vs. Spatial) to assess global vs. local structural representativeness. A decision matrix is applied: for each ensemble hypothesis, the combination of which Work Done metrics show significant change (Density Change and Scale Change, checked or crossed for each colored ensemble cluster) determines whether the structural hypothesis should be refined, accepted, or rejected. Confidence is quantified via multivariate standard deviation of Workscale and Workdensity across replicates. Agreement between split types is measured by RMSD of median metric values.

## Evaluation
- **Iso-Validation benchmark** (TeaA): Synthetic HDX data with known 40:60 open:closed populations enables direct ground-truth comparison via Open State Recovery%. Demonstrated that training error fails to distinguish correct (ISO-Bimodal) from incorrect (ISO-Trimodal) ensembles, while Work Done metrics robustly correlate with true population recovery.
- **Real experimental systems**: BPTI (58 residues, rigid), HOIP (flexible ubiquitinase), BRD4 (two bromodomains with disordered linkers), MBP, and LXRα — spanning 58–474 residues.
- **Protocol comparison**: Five optimization protocols (BV-only, RW-only, RWafterBV, BVafterRW, MutualBVRW) tested on AF2-Filtered BPTI ensemble. BVafterRW identified as most robust.
- **Clustering sweep**: Ensembles downsampled from 0.001 to 1.0 proportions to assess minimum ensemble size for reliable fitting.
- **Structure poisoning**: Three artifact types (Gaussian noise, coordinate mixing, proton shuffling) added at 0.1–50% levels to test sensitivity to specific failure modes.

## Results
- Conventional training error metrics fail to distinguish structurally representative ensembles from incorrect ones across all tested systems.
- Work Done metrics (especially Workshape and Workdensity) robustly discriminate ensemble quality at both global (Non-Redundant split) and local (Spatial split) structural scales.
- For BPTI, MD-1Start better represents global dynamics while AF2-Filtered better captures local sub-structural flexibility.
- Staged optimization (reweight first, then optimize BV parameters — BVafterRW) produces the most robust ensemble-models.
- Representative ensembles can be clustered to 10–13 structures (proportion 0.001) with minimal quality loss, enabling human-interpretable structural analysis.
- No single synthetic artifact type simultaneously informs on sampling completeness and structural plausibility; multiple complementary metrics are essential.

---

# Detailed Figure Description

The figure is a large, vertically stacked infographic divided into **four horizontal panels**, each enclosed in a **rounded-corner light grey rectangle with a thin (~1.5 pt) medium-grey border**. The panels are stacked top-to-bottom with small gaps (~8–10 px) between them. The overall background is **pure white**. Each panel has a **bold black section number and title** in the upper-left corner in a large sans-serif font (approximately 18–20 pt). The four panels are labeled: "**1. Assemble data**", "**2. Fitting**", "**3. Inference**", and "**4. Applications**". Thick **black arrows** (~3–4 pt stroke) connect elements within and between panels to indicate workflow direction.

---

## Panel 1: "Assemble data"

**Layout**: A wide horizontal panel reading left-to-right with a central bidirectional workflow.

**Left side — Peptide organization (two stacked sub-elements)**:
- **Top sub-element ("Peptide-Clustered")**: A label in small black sans-serif text reading "Peptide-Clustered" sits above a cluster of ~12 filled circles arranged in an irregular packed group. The circles are approximately 12–15 px diameter. They are colored in two main hues: **bright green** (hex ~#4CAF50) and **orange** (hex ~#FF9800), with one or two **grey** circles intermixed, representing different peptide clusters. The arrangement suggests grouping by sequence overlap.
- **Bottom sub-element ("Spatial-proximal")**: A label reading "Spatial-proximal" sits above a similar cluster of circles, but here the arrangement emphasizes spatial adjacency — the same green, orange, and grey circles but organized to show 3D proximity relationships. One **light grey circle** sits at the center/edge to indicate a reference atom or pivot point.
- Between the two sub-elements, a **bold black "+" symbol** (~16 pt) indicates that both peptide organization strategies are combined.

**Center-left — HDX-MS measurement schematic**:
- A cluster of ~5–6 **wavy lines** (representing peptide sequences/fragments) in varied colors: **magenta/pink** (~#E91E63), **cyan/teal** (~#00BCD4), **dark purple** (~#7B1FA2), **red** (~#F44336), and **light blue**. These wavy lines are hand-drawn/organic in style, each roughly 40–60 px long, representing overlapping peptide fragments of different lengths.
- A thick black arrow points rightward from the peptide fragments to a **small plot schematic** labeled "**Measure**" (bold black text below). The plot shows a miniature XY chart with **"HDX Uptake"** on the y-axis (vertical) and **"Time"** on the x-axis (horizontal), with ~4–5 thin curved lines (in matching peptide colors: pink, blue, purple, red) rising from lower-left to upper-right with varying rates, representing deuterium uptake kinetics curves. Axes are thin black lines.

**Center — Protein structure + labeling**:
- A **3D ribbon/cartoon representation** of a protein structure, rendered in a semi-realistic style with **blue alpha-helices**, **teal/cyan sheets**, and **grey/white loops**. The protein is approximately 80–100 px wide. Small colored circles (**orange**, **green**, with "Na" labels in white text inside some circles — representing sodium ions or atom markers) are scattered around the protein surface, indicating specific labeled sites or exchangeable positions. These circles are ~8–10 px diameter with thin dark outlines.
- A thick black arrow points leftward from the protein back toward the uptake plot, and another thick black arrow points rightward from the protein toward the simulation panel, establishing the bidirectional relationship between measurement and simulation.

**Center-right — Simulation**:
- The word "**Simulate**" appears in bold black text below a small icon of a **speedometer/gauge** rendered in grey with a needle, suggesting computational simulation effort.
- A thick black arrow connects from the protein structure rightward to the simulation icon, and then another arrow continues rightward.

**Far right — Conformational landscape**:
- A **large scatter plot** (~120×100 px visual area) showing a UMAP/PCA-style 2D projection of the conformational ensemble. Hundreds of small dots (~2–3 px each) are scattered across the space, colored in a **rainbow/spectral gradient**: **red** (lower-left), **orange**, **yellow**, **green**, **cyan**, **blue**, **purple/violet** (upper regions), creating a visually striking multicolored point cloud. The dots form an irregular L-shaped or crescent distribution. The plot has thin **dark teal/navy blue axes** forming an L-shape (x and y axes only, no tick marks or labels). This represents the sampled conformational landscape from simulation.

**Connecting arrows between Panel 1 and Panel 2**:
- A thick black downward arrow on the far left connects from Panel 1 to Panel 2, labeled "**Split Data**" in black text next to the arrow.
- A thick black arrow from the conformational landscape (far right of Panel 1) curves downward into Panel 2's right side, labeled "**Generate Hypotheses**" in bold black text.

---

## Panel 2: "Fitting"

**Layout**: A horizontal panel with three main elements connected by arrows, reading right-to-left-to-center.

**Left side — Split data / training-validation**:
- A cluster of **wavy peptide lines** similar to Panel 1 but now shown in two distinct color groups: **orange wavy lines** (training set, ~4–5 lines) and **green wavy lines** (validation set, ~3–4 lines), representing the data split. The lines are organic/hand-drawn style.

**Center-left — Error minimization plot**:
- A **scatter plot** labeled "**Minimise error**" (in teal/dark cyan text, ~12 pt, above the plot). The plot has a thin black axis system with "**Target**" on the y-axis and "**Predicted**" on the x-axis (both in small black text). A **dark navy/teal diagonal line** (~2 pt) runs from lower-left to upper-right (the identity line). Scattered around this line are ~15–20 small filled circles (~6–8 px diameter) in **orange** and **dark green/teal** colors, representing training data points. Points close to the line indicate good fit; points far from it indicate poor fit.
- A thick black arrow points from the split data (left) rightward to this plot.

**Center — Balance Objectives / Maximum Entropy**:
- In the center of the panel, text reads "**Balance Objectives**" in bold dark teal/black text (~14 pt), positioned between two opposing thick black arrows (one from the error plot on the left, one from the conformational diversity element on the right), suggesting a tension/tradeoff.
- Below this, an icon of a **gear/cog** in grey (~30 px) represents the optimization engine, with the text "**Maximum Entropy Optimisation**" in bold italic dark teal/black text (~12 pt) beneath it.

**Center-right — Conformational Diversity**:
- The label "**Conformational Diversity**" appears in dark teal text (~12 pt) above a schematic showing a **central open circle** (thin black outline, ~15 px, representing the ensemble center/mean) with **6–7 thin black lines radiating outward** to smaller filled circles at their endpoints. The endpoint circles are in different colors: **dark teal**, **dark purple/maroon**, **blue**, **yellow/gold**, **dark green**, representing different conformational states. This star/spoke diagram represents the diversity of conformations being balanced.

**Far right — Structural hypothesis clusters**:
- A collection of **5–6 protein-shaped blobs** (organic, cloud-like silhouettes, each ~40–50 px) arranged in a loose cluster. Each blob is a different color: **purple/violet** (~#9C27B0), **dark red/maroon** (~#8B0000), **orange** (~#FF9800), **teal/cyan** (~#009688), **gold/yellow** (~#FFC107), and **blue** (~#2196F3). These represent distinct structural hypothesis clusters derived from the conformational landscape. They have soft, organic outlines suggesting protein surface shapes, rendered with slight internal texture/shading to give a 3D molecular surface appearance.
- A thick black arrow points leftward from these clusters toward the conformational diversity element.
- Another thick black arrow points from the conformational landscape in Panel 1 (above) downward to these clusters.

---

## Panel 3: "Inference"

**Layout**: A horizontal panel with three main elements reading left-to-right.

**Left side — Statistical significance bar chart**:
- A **bar chart** with ~7 bars along the x-axis. The x-axis labels (in small black italic text, ~8 pt, rotated ~45°) read: "Training_Error", "Validation_Error", "Error_Change", "KL_Divergence", "Shape_Change", "Density_Change", "Scale_Change". The y-axis is labeled "**p-value**" in small black text, with a horizontal **dashed grey line** at y ≈ 0.25 representing a significance threshold.
- The first three bars (Training_Error, Validation_Error, Error_Change) are **tall light grey bars** extending above the dashed line, each topped with the annotation "**n.s.**" (not significant) in small dark blue/black bold text. These bars have thin black error bars (vertical lines with small horizontal caps).
- The next bar (KL_Divergence) is a **medium-height light blue/steel blue bar** (~#90CAF9) extending below or near the dashed line, annotated "**‡-\***" in small text above.
- The following bars (Shape_Change, Density_Change, Scale_Change) are progressively **shorter light blue bars**, annotated with increasing significance markers: "**‡-\*\*\***", "**†-\***", "**†-\*\***" respectively, in small dark text. These bars are clearly below the dashed line, indicating statistical significance.
- Bars have thin (~1 pt) black outlines with thin black error bars.
- The annotation style uses daggers (†) and double-daggers (‡) combined with asterisks to denote significance levels.
- Between the "n.s." and significant annotations, there's a visual text "**n.s.-\***" above the Error_Change bar, suggesting borderline significance.

**Center — Decision matrix (metric × ensemble grid)**:
- A **grid/table** structure. Along the top, **4–5 protein-shaped blob icons** (same organic molecular surface style as Panel 2) are shown in different colors: **purple**, **orange/gold**, **teal**, **dark red/maroon**, and possibly one more. These represent different ensemble hypotheses.
- Two row labels on the left side read "**Density Change**" and "**Scale Change**" in small black text.
- Inside the grid cells, **checkmarks (✓)** and **crosses (✗)** in bold black (~14 pt) indicate whether each ensemble shows significant density change or scale change. The pattern varies: some ensembles show ✓ for Density Change but ✗ for Scale Change, or vice versa, or both, creating a diagnostic fingerprint for each ensemble.
- A thick black rightward arrow connects from this grid to the next element.

**Right side — Refined structural hypothesis**:
- The text "**Refine Structural Hypothesis**" in bold black text (~12 pt) sits above/beside a single **protein-shaped blob** rendered in **light purple/lavender** (~#CE93D8) with a slightly more detailed surface texture than the earlier blobs, suggesting a refined/improved structural model. The blob is ~50–60 px wide.
- A thick black arrow points from the decision matrix rightward to this refined hypothesis.

---

## Panel 4: "Applications"

**Layout**: A wide horizontal panel with **five evenly spaced application vignettes** arranged left-to-right, each consisting of an icon/illustration above a bold label.

The panel has a slightly darker or more defined grey border compared to the other panels, and the section number "**4.**" and title "**Applications**" are in bold black in the upper-left, slightly larger than other panel titles to emphasize this as the concluding summary.

**Application 1 — "Comparative Hypothesis testing"** (far left):
- **Icon**: A **balance scale** (classic justice/weighing scale) rendered in dark navy/charcoal grey line art (~2 pt strokes). On the left pan sits a **purple protein blob** (~#9C27B0), and on the right pan sits a **blue/teal protein blob** (~#2196F3), representing two competing hypotheses being weighed against each other. The scale beam is slightly tilted, suggesting one hypothesis is favored.
- **Label**: "**Comparative Hypothesis testing**" in bold black text (~10 pt), centered below the icon, potentially spanning two lines.

**Application 2 — "Single Structure Evaluation"**:
- **Icon**: A **single protein blob** in **light blue/periwinkle** (~#7986CB) enclosed in or overlaid with a **circular magnifying lens or gauge** motif. The gauge has a **rainbow-colored arc** (green-yellow-orange-red gradient) along its circumference with a small **green arrow/needle** pointing to a position on the arc, suggesting a quality score assessment. The protein blob sits inside or behind the circular element.
- **Label**: "**Single Structure Evaluation**" in bold black text (~10 pt), centered below.

**Application 3 — "Fitting of parameters and frame-weights"** (center):
- **Icon**: A **large dark grey gear/cog** (~40 px) in the center, with the Greek letters "**ω**" and "**β**" in bold black text (~14 pt) on the left and right sides of the gear respectively, representing the two types of parameters being fit (frame weights ω and BV model parameters β). Below the gear, **5–6 small colored circles** (teal, green, orange, yellow, cyan) are connected by thin lines in a tree/network structure, with small **gauge/meter icons** at the bottom leaves showing different readings (green, yellow, red zones), representing the parameter fitting outcomes for different ensemble members.
- **Label**: "**Fitting of parameters and frame-weights**" in bold black text (~10 pt), centered below.

**Application 4 — "Performance of clustered ensembles"**:
- **Icon**: A **dendrogram/hierarchical tree** structure with thin black lines (~1.5 pt) branching from a single root at the top down to ~5–6 terminal nodes. At each terminal node, a small **protein blob** is shown in different colors (teal, white/grey, light purple, beige, green), representing cluster centroids of different sizes. The tree structure visually conveys hierarchical clustering, with varying branch lengths suggesting different cluster distances.
- **Label**: "**Performance of clustered ensembles**" in bold black text (~10 pt), centered below.

**Application 5 — "Quantification of noise sensitivity"** (far right):
- **Icon**: A **protein blob** in **light grey/white** (~#E0E0E0) surrounded by multiple concentric **translucent grey rings or halos** (3–5 rings, progressively more transparent outward) creating a "noisy cloud" effect. A small **pipette or dropper icon** in dark grey/black is positioned in the upper-right, appearing to "add" noise to the structure. The overall effect suggests perturbation/noise being applied to a structure and measuring its response.
- **Label**: "**Quantification of noise sensitivity**" in bold black text (~10 pt), centered below.

---

## Global Visual Style Notes

- **Background**: Pure white (#FFFFFF) for the overall canvas; panels have very light grey (#F5F5F5 to #FAFAFA) interior fill.
- **Panel borders**: Rounded rectangles with ~8–12 px corner radius, ~1.5 pt medium grey (#BDBDBD) stroke.
- **Arrows**: Thick black (#000000) arrows, ~3–4 pt stroke, with solid triangular arrowheads (~10 px). Arrows are straight or have single clean right-angle bends.
- **Text**: Sans-serif font throughout (resembling Helvetica, Arial, or Calibri). Section numbers and titles are bold, ~18–20 pt. Sub-labels are ~10–12 pt regular or bold. Axis labels are ~8 pt.
- **Color palette**: The figure uses a rich, diverse palette: bright green (#4CAF50), orange (#FF9800), teal/cyan (#009688 / #00BCD4), purple (#9C27B0), dark red/maroon (#8B0000 / #B71C1C), blue (#2196F3), gold (#FFC107), pink/magenta (#E91E63), navy (#1A237E), light blue (#90CAF9), lavender (#CE93D8). Colors are saturated and distinct for clear differentiation.
- **Protein blobs**: Rendered as soft, organic, irregular cloud-like shapes with subtle internal shading to suggest molecular surface topology. Each is a single solid color with slight gradient or texture.
- **Icons**: Mix of schematic line art (scales, gears, gauges, dendrograms) and filled organic shapes (protein blobs, colored circles). Line art uses ~1.5–2 pt dark grey or black strokes.
- **Overall composition**: Clean, professional scientific infographic style. No drop shadows. Minimal decorative elements. Information flows primarily left-to-right within panels and top-to-bottom between panels. The figure is wide-format (landscape aspect ratio approximately 2:1 to 2.5:1).