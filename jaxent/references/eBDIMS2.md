# Caption for eBDIMS2 Figure
Fig. 1 | Overview of the eBDIMS2 path-sampling method for the generation of
conformational intermediates of large protein systems, cross-validation with
Principal Component Analysis (PCA) of experimental ensembles, and appli-
cations upon atomistic reconstruction. The first step is to generate an ensemble
from all available structures in the Protein Data Bank (PDB) obtained from X-ray
crystallography or cryogenic Electron Microscopy (cryoEM) experiments. PCA is
then performed to cluster experimental conformations and assign biological states
to each conformational cluster, e.g., apo/holo, inactive/active. After identification
of relevant end-state conformers, eBDIMS2 uses a combination of coarse-grained
(CG) Elastic Network Modeling (ENM) and Brownian Dynamics (BD) to sample the
conformational transition between the two states. The transition pathway is pro-
jected back onto the experimental PC space and used to explain experimental
intermediates and conformational cycles. The CG intermediates can be atomisti-
cally reconstructed and used for downstream applications, e.g., enhanced sampling
with Molecular Dynamics (MD), drug design targeting the intermediate con-
formation, etc.

## Methodology Description

### Short Description
eBDIMS2 is an optimized coarse-grained path-sampling algorithm that combines Elastic Network Models (ENM) with Brownian Dynamics (BD) and Dynamic IMportance Sampling (DIMS) to efficiently simulate conformational transition pathways between two experimentally determined end-state protein structures, achieving quasi-linear scaling with system size. The method generates intermediate conformations that are validated against experimental intermediates via Principal Component Analysis (PCA) of structural ensembles, and can be atomistically reconstructed for downstream applications such as enhanced MD sampling and drug design.

### Inputs
- An ensemble of large-protein complex structures retrieved from the Protein Data Bank (PDB), obtained via X-ray crystallography or cryogenic Electron Microscopy (cryo-EM) experiments.
- Two end-state conformations (e.g., apo/holo, active/inactive) identified from PCA clustering of the structural ensemble, represented as Cα-only coarse-grained coordinates.

### Process
1. **Ensemble generation and PCA clustering**: All available PDB structures for a given protein are collected, aligned, and subjected to Principal Component Analysis. PC1 and PC2 (typically capturing >70% variance) are used to identify conformational clusters corresponding to distinct biological states (e.g., apo vs. holo). Relevant end-state conformers are selected from these clusters.
2. **Coarse-grained ENM construction**: Each protein is represented as one bead per residue (Cα atom), connected by elastic springs following the MD-parametrized edENM force field. An adaptive cutoff (8 Å) is used to build a neighbor list of interacting residue pairs, dramatically reducing force computation from O(N²) to quasi-linear scaling.
3. **Brownian Dynamics simulation with DIMS biasing**: Starting from one end-state (R₀), the Langevin equation of motion is integrated under implicit solvent conditions (friction coefficient γ and white noise ξ). Every k=10 BD steps, a progress variable Γ (sum of squared differences in pairwise distances between the current and target conformation) is evaluated. If Γ decreases, the current conformation is accepted; otherwise it is rejected. This biases the trajectory toward the target (Rₜ) without relying on RMSD minimization or normal mode analysis.
4. **Pathway projection and intermediate identification**: The resulting CG trajectory is projected back onto the experimental PC space. Intermediates along the pathway are compared to experimentally trapped conformations to assess mechanistic relevance.
5. **Atomistic reconstruction**: Selected CG intermediates are converted to all-atom models using cg2all, followed by short molecular refinement (energy minimization, equilibration, short MD) to resolve clashes and recover near-experimental stereochemical quality.

### Evaluation
- Pathways are projected onto experimental PCA spaces to verify that eBDIMS2 intermediates spontaneously visit known experimental intermediates (RMSD comparisons, typically 3–4 Å from trapped intermediates).
- Stereochemical quality is assessed by computing consecutive Cα–Cα distances (should center around 3.8 Å) and MolProbity scores after atomistic reconstruction.
- Computing times and convergence RMSDs are benchmarked against 10 other path-sampling methods (iMOD, GOdMD, NOLB, MinActionPath2, Climber, etc.).
- Pathway smoothness is evaluated via PC-space projections (smooth vs. zig-zag trajectories).
- Agreement with Targeted MD and enhanced MD (Weighted Ensemble) simulations is assessed via PC-space overlap and pairwise RMSD comparisons.

### Results
- eBDIMS2 achieves quasi-linear size-time scaling (PCC ~0.9), with median computing time of ~2.5 hours for systems up to ~2 MDa on a standard desktop computer.
- Convergence to target states is routinely below ~1 Å RMSD.
- The method successfully simulates 191 transition pathways across 47 large protein systems (300 kDa to 2.3 MDa), including complex rotary motions of ATP synthases, ~57 Å rearrangements in LRP2, and ~29 Å opening-closing of A2M.
- eBDIMS2 pathways spontaneously approach experimental intermediates in >30% of PC spaces and overlap with microsecond MD and enhanced sampling trajectories at a fraction of computational cost.

---

## Detailed Figure Description

The figure is a vertically stacked three-panel diagram on a **pure white background**, illustrating the eBDIMS2 workflow from top to bottom. Each panel is separated by subtle spacing. The overall layout reads left-to-right within each panel and top-to-bottom across panels, forming a continuous pipeline. All text labels use a clean sans-serif font (similar to Arial or Helvetica). Connecting arrows between major steps are **black, curved or straight arrows** with solid lines and medium thickness (~2 px).

---

### **Panel 1 (Top Row): Ensemble Collection → PCA → End-State Identification**

**Layout**: Three elements arranged horizontally, connected by **thick black rightward-pointing arrows** with angular/chevron style.

**Element 1 (Left)**: A 3D molecular surface rendering of a large protein complex (superposition of many conformers), shown in a **rainbow/multicolor scheme** (orange, teal, green, red, yellow overlapping structures) to represent the structural diversity of the ensemble. A small **PDB logo** (grey circle with "PDB" text and a small ribbon icon) is placed at the bottom-left corner of this image. Below the structure, a **white rounded-rectangle label with thin black border** reads: "Ensemble of large-protein complexes from the PDB (cryoEM, X-ray)".

**Element 2 (Center)**: A **2D scatter plot** on white background with thin black axes. The x-axis is labeled "PC1 (57.12%)" and the y-axis "PC2 (29.97%)". Axis tick marks and numbers are in small black text. The plot contains approximately 10–15 **small black dots** scattered across the space, representing individual experimental conformations. Two dots are highlighted with **large colored circles**: a **solid blue circle** in the upper-left region labeled "6pof (apo)" in black text, and a **solid red circle** in the lower-right region labeled "6hxh (holo)" in black text. A **grey dashed curved line** connects the two highlighted points with the label "Path?" in grey italic text positioned near the middle of the curve. Below the plot, a **white rounded-rectangle label with thin black border** reads: "Principal Component Analysis (PCA) of the structural ensemble".

**Element 3 (Right)**: Two 3D molecular surface renderings of the protein, shown side by side at a slight angle. The **left structure is blue** (labeled "Apo end state" in blue text) and the **right structure is red** (labeled "Holo end state" in red text). A **light blue-to-red gradient dashed arrow** curves between them suggesting directionality. Below, a **white rounded-rectangle label with thin black border** reads: "Identification of relevant end-state conformers".

---

### **Panel 2 (Middle Row): Brownian Dynamics + DIMS Biasing = eBDIMS2**

**Layout**: Two major elements side by side, connected at the bottom by a combined label. A **large curved black arrow** sweeps downward from Panel 1 into Panel 2.

**Element 1 (Left)**: A 3D molecular structure rendered as a **red-tinted elastic network representation** — the protein shown as a transparent reddish surface with visible **spring-like connections** (thin lines between Cα nodes) overlaid. The background around this structure is subtly lighter. Four **text annotations** in black sans-serif surround the structure:
- Upper-left: The **Langevin equation** in LaTeX-style math: $m_i \ddot{r}_i = F_i - \gamma \dot{r}_i + \xi_i(t)$, rendered in black italic/math font
- Left side: "Implicit solvent" in black text
- Right side: "White noise" in black text
- Bottom: "Elastic Network Model" in black text

Below this element, a **white rounded-rectangle label with thin black border** reads: "Brownian Dynamics (BD) simulation from the starting state".

**A bold black "+" symbol** separates Element 1 and Element 2 horizontally.

**Element 2 (Right)**: A 3D molecular surface rendering of the same protein, colored with a **blue-white-red gradient** representing the degree of conformational change or DIMS biasing (blue = regions close to target, red = regions far from target, white = intermediate). To the upper-right of this structure, the **DIMS progress variable equation** is displayed in black math font: $\Gamma_s = \sum_{i=1}^{N-1} \sum_{j=i+1}^{N} (d_{ij}^s - d_{ij}^t)^2$. The label "eBDIMS2" appears in **bold black text** near the structure.

Below this element, a **white rounded-rectangle label with thin black border** reads: "Dynamic IMportance Sampling (DIMS) to bias the BD to the target".

---

### **Panel 3 (Bottom Row): Pathway Analysis → Reconstruction → Applications**

**Layout**: Four elements arranged horizontally, connected by **solid black rightward-pointing arrows** (medium thickness). A **large curved black arrow** sweeps from Panel 2 down into Panel 3.

**Element 1 (Far Left)**: A **2D scatter plot** similar to the one in Panel 1 but now including the eBDIMS2 pathway. Same axes: "PC1 (57.12%)" and "PC2 (29.97%)" with black tick marks. The **blue circle** ("6pof (apo)") is in the upper-left, the **red circle** ("6hxh (holo)") is in the lower-right. A **green continuous line with small circular markers** traces the transition pathway from the blue to the red circle, passing through a region where a **light grey circle** marks the location of "Experimental intermediates" (labeled in black text with an arrow). Black dots represent other ensemble members. The pathway line is labeled "Transition pathway" in green text. Below, a **white rounded-rectangle label with thin black border** reads: "Projection of the pathway on PC space and identification of experimental intermediates".

**Element 2 (Center-Left)**: A 3D molecular structure shown in **semi-transparent red/pink surface** representation, labeled "eBDIMS2 CG intermediate" in black text below.

**A black rightward arrow** connects to:

**Element 3 (Center-Right)**: The same structure now shown as a **detailed all-atom ribbon/cartoon representation** in red/blue coloring (more opaque, higher detail), labeled "eBDIMS2 all-atom intermediate" in black text below. Above the arrow between Elements 2 and 3, the text "cg2all" appears in **bold black monospace-style font**, indicating the reconstruction tool used.

Below Elements 2 and 3 together, a **white rounded-rectangle label with thin black border** reads: "Coarse-grained (CG) eBDIMS2 intermediate and all-atom reconstruction".

**Element 4 (Far Right)**: Two sub-panels stacked vertically:
- **Top sub-panel**: A **2D free energy landscape (FEL) heatmap** plotted on the same PC1/PC2 axes. The heatmap uses a **yellow-to-dark-blue color gradient** (yellow = high free energy, dark blue = low energy basins). A few contour-like regions are visible. The label "Free-energy landscape (FEL) enhanced sampling" appears above in black text. A small **blue arrow/circle** on the FEL indicates the intermediate conformation's location.
- **Bottom sub-panel**: A small 3D molecular surface rendering of a protein (in **orange/gold**) with a small molecule docked nearby (small colorful stick representation), with a "+" sign and text "New drug?" in black. The label "Intermediate-targeted drug discovery" appears above in black text.

Below Element 4, a **white rounded-rectangle label with thin black border** reads: "Applications: enhanced Molecular Dynamics, ligand interactions, etc."

---

### **Overall Figure Caption Area**
At the very bottom, below all three panels, there is a **bold black caption** beginning with "Fig. 1 | Overview of the eBDIMS2 path-sampling method..." followed by descriptive text in regular weight black font, arranged in two columns of justified text spanning the full figure width.

### **Global Style Notes**
- Background: pure white throughout
- All label boxes: white fill, thin (~1 px) black or dark grey rounded-rectangle borders
- All arrows between workflow steps: solid black, ~2–3 px, with pointed arrowheads
- Molecular renderings: high-quality 3D surface or ribbon representations with soft ambient lighting and slight shadows
- Color palette: blue (apo/start state), red (holo/target state), green (pathway), black (text/arrows), with blue-white-red gradient for DIMS visualization
- Mathematical equations rendered in standard LaTeX-style italic math font, black color
- Font sizes: labels ~10–12 pt, axis labels ~8–9 pt, equation text ~11 pt