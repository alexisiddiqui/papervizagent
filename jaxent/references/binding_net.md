
Detailed Figure Description for "Figure 2: The BindingNet architecture and integration"
Caption: 
Fig. 2 | The BindingNet architecture and integration. a Illustration of the three granularities of vector frame bases utilized by BindingNet for geometric representation. b Overview of BindingNet’s three core components and their integration into the NeuralMD pipeline for molecular dynamics simulation.

# Methodology Description and Figure Specification

### Short Description
NeuralMD is a machine learning framework for accelerating molecular dynamics (MD) simulations of protein-ligand binding. It combines BindingNet — a multi-grained, SE(3)-equivariant geometric neural network that models protein-ligand interactions at three granularity levels (atom, backbone, residue) using vector frame bases — with a second-order neural differential equation solver (ODE or SDE) that integrates forces into trajectories following Newtonian or Langevin mechanics.

### Inputs
- **Ligand data:** Atomic numbers f^(l) and 3D Euclidean coordinates x^(l) for each atom in the small-molecule ligand, plus initial velocity v^(l)_0.
- **Protein data (backbone level):** Residue type f^(p) and coordinates of the three backbone atoms per residue: x^(p)_N (nitrogen), x^(p)_Cα (alpha carbon), x^(p)_C (carbonyl carbon).
- **Protein data (residue level):** Residue type f^(p) and Cα coordinate x^(p) ≜ x^(p)_Cα taken as the coarse-grained residue-level position.
- **Problem setting:** Semi-flexible binding — the protein structure is rigid, and only the ligand moves. The task is to predict the ligand trajectory {x^(l)_1, ..., x^(l)_T} given initial conditions.

### Process
The NeuralMD framework has two main components executed sequentially:

**Component 1 — BindingNet (multi-grained SE(3)-equivariant force prediction):**

BindingNet is composed of three sub-modules that operate at different granularity levels, each using its own vector frame basis for SE(3)-equivariance:

1. **BindingNet-Ligand (atom-level):**
   - Constructs an atom-level vector frame F_ligand from pairs of ligand atom positions using Gram-Schmidt orthogonalization.
   - Takes as input the atomic features f^(l) and coordinates x^(l).
   - Generates atom embeddings z^(l) via one-hot encoding.
   - Aggregates neighbor information to get equivariant atom representations: h^(l)_i = Agg(x^(l)_i − x^(l)_j) · z^(l)_i.
   - Performs scalarization by projecting concatenated representations onto the ligand vector frame: h^(l)_ij = (h^(l)_i ⊕ h^(l)_j) · F_ligand.
   - Passes through equivariant message-passing neural network (MPNN) layers to produce atom-level hidden representations h^(l) and equivariant vector representations vec^(l).

2. **BindingNet-Protein (backbone-level):**
   - Constructs a backbone-level vector frame F_protein from the N−Cα−C backbone structure of each residue.
   - Takes as input the residue type f^(p) and backbone atom coordinates x^(p)_Cα, x^(p)_N, x^(p)_C.
   - Generates atom embeddings z̃^(p) via type encoding, and atom-level embeddings z^(p) via neighbor aggregation.
   - Computes equivariant representations: h^(p)_i = Agg(x^(p)_i − x^(p)_j) · z^(p)_i.
   - Scalarizes via the protein backbone frame: h^(p)_ij = (h^(p)_i ⊕ h^(p)_j) · F_residue.
   - Passes through MPNN layers to produce residue-level representations h^(p).

3. **BindingNet-Complex (residue-level):**
   - Constructs a residue-level vector frame F_complex from sequential Cα positions of pocket residues.
   - Takes as input: vec^(l) and x^(l) and h^(l) from the ligand module, and h^(p) and x^(p) from the protein module.
   - Computes equivariant interaction edge features: h_ij = (h^(l)_i + h^(p)_j) · (x^(l)_i − x^(p)_j).
   - Scalarizes via the complex frame: h_ij = h_ij · F_complex.
   - Applies equivariant MPNN to produce per-atom force predictions F^(l) that combine internal ligand forces and external protein-ligand interaction forces.

**Component 2 — NeuralMD Dynamics Solver (trajectory integration):**

- Defines a differential function "func" that takes velocity v^(l), position x^(l), time t, and a condition (the protein), calls BindingNet to get force F^(l), computes acceleration a^(l) = F^(l)/m, and returns [a^(l), v^(l)].
- Formulates binding MD as a second-order ODE (Newtonian dynamics) or SDE (Langevin dynamics with learned stochastic noise).
- Uses an augmented derivative space: dx/dt = v, dv/dt = F/m, enabling simultaneous integration of positions and velocities.
- Integrates the initial conditions [v^(l)_0, x^(l)_0] over T timesteps to produce the predicted trajectory x̂^(l)_1, ..., x̂^(l)_T.

### Evaluation
- **Reconstruction metrics:** Mean Absolute Error (MAE, in Å) and Root Mean Squared Error (RMSE) between predicted and ground-truth coordinates over all test snapshots.
- **Validity metrics:** (a) Matching — MSE between atom pairwise distances in predicted vs. ground-truth conformations; (b) Stability (%) — fraction of atom pairs where |true distance − predicted distance| ≤ 0.5 Å.
- **Qualitative analysis:** RMSF-Ligand (root mean square fluctuation) curves computed over sliding windows of 5 snapshots, comparing oscillation patterns against ground truth.
- **Efficiency:** Frames per second (FPS) on a single Nvidia V100 GPU.
- **Experimental settings:** 10 single-trajectory tasks (80/20 temporal split) and 3 multi-trajectory tasks (100, 1000, and full MISATO dataset with 80%/10%/10% train/val/test split). All experiments repeated with 3 random seeds.

### Results
- NeuralMD achieves up to 15× lower reconstruction error and 70% higher stability compared to VerletMD baseline.
- NeuralMD outperforms GNN-MD and DenoisingLD across nearly all datasets and metrics, with the validity metrics (Matching, Stability) being the most distinguishing factors.
- RMSF-Ligand oscillation curves from NeuralMD align most closely with ground truth across the majority of test complexes.
- NeuralMD delivers approximately 420 FPS on average, and is estimated to be at least 1,000× faster than numerical MD methods (conservatively; up to ~25,000× under optimal conditions).

---

# Detailed Figure Description

### Overall Layout and Composition

The figure is divided into two main vertically-stacked panels, labeled **(a)** and **(b)**, on a **pure white background**. The overall figure is wide (landscape aspect ratio, approximately 2.5:1 width-to-height). A thin light-gray rounded-corner border (approximately 1px) encloses each major panel.

---

### Panel (a): "Three granularities of vector frame basis in BindingNet"

**Title:** Bold black text, large font (~16pt), positioned at the top-left of the panel: "(a) Three granularities of vector frame basis in BindingNet".

**Layout:** A single horizontal row of three sub-panels of approximately equal width, separated by thin vertical dividers. Each sub-panel has a **light gray background** (approximately #F0F0F0 or #E8E8E8). The entire row is enclosed in a thin rounded-corner light-gray border.

#### Sub-panel (a.1): Ligand Frame
- **Label:** Centered below the illustration: "(a.1) Ligand Frame" in regular black text (~11pt).
- **Content:** A small molecular graph (approximately 6–8 atoms) shown on the left side of the sub-panel, representing a ligand. Each atom is drawn as a **dark gray/charcoal filled circle** (~12px diameter) with a single-letter label inside in white (e.g., "C"). Bonds between atoms are **dark gray lines** (~2px thick).
- From the molecular graph, **three orthogonal colored arrows** emanate from one atom, forming a local coordinate frame. The arrows are drawn with:
  - One arrow in **dark teal/green** pointing roughly up-left.
  - One arrow in **dark teal/green** pointing roughly right.
  - One arrow in **dark teal/green** pointing roughly down.
- These arrows are thin (~1.5px) with small arrowheads, representing the atom-level vector frame F_ligand constructed via Gram-Schmidt from atom pair positions.

#### Sub-panel (a.2): Protein Frame
- **Label:** Centered below: "(a.2) Protein Frame".
- **Content:** Three residue backbone structures are shown, labeled **i−1**, **i**, and **i+1** in small rounded gray-bordered boxes above or beside each residue.
- Each residue backbone is drawn as three atoms connected in a bent chain (N−Cα−C):
  - **N atom:** A **cyan/turquoise filled circle** (~14px), labeled "N" in white or dark text.
  - **Cα atom:** A **pink/magenta filled circle** (~14px), labeled "Cα" in white.
  - **C atom:** A **gray filled circle** (~14px), labeled "C" in dark text.
- Atoms within each residue are connected by **dark red/maroon lines** (~2px).
- From the Cα atom of each residue, **three orthogonal red arrows** form the backbone vector frame F_protein. The arrows are **dark red/crimson** (~1.5px thick), with small arrowheads.
- A gray shaded irregular background blob (like a translucent protein surface) sits behind the residues to suggest the protein context.

#### Sub-panel (a.3): Complex Frame
- **Label:** Centered below: "(a.3) Complex Frame".
- **Content:** This sub-panel combines elements from both the ligand and the protein:
  - A **ligand molecule** (same style as a.1: dark charcoal circles with bonds) appears on the **left side**.
  - **Protein residues** (Cα nodes as dark circles labeled "C", arranged in two rows inside a **pale yellow/cream ellipse** outline) appear on the **right side**. The ellipse has a thin border (~1px) in gold/amber.
  - Between the ligand and the protein residues, **dashed purple/violet curved lines** (~1.5px, dashed pattern ~4px dash, 3px gap) connect ligand atoms to protein Cα atoms, representing the residue-level cross-interactions.
  - From the connection region, **three orthogonal purple arrows** form the complex-level vector frame F_complex. These arrows are **dark purple/violet** (~1.5px thick).
- **Legend** (positioned at the far right of panel a): A small vertical legend box with two entries:
  - A small orange/amber filled rectangle labeled "Ligand"
  - A small gray filled rectangle labeled "Protein"

---

### Panel (b): "Pipeline of NeuralMD"

**Title:** Bold black text, large font (~16pt), at top-left of the panel: "(b) Pipeline of NeuralMD".

**Layout:** A horizontal arrangement of four distinct column-blocks from left to right, each representing a module. Each column-block has a distinct **pastel background color** and a thin border (1px, slightly darker than the fill). Within each block, processing steps are shown as **white rounded-rectangle boxes** with thin black borders (~1px), connected by **black downward arrows** (~1.5px thick). Mathematical equations are written in black text (italic for variables, using standard mathematical notation with superscripts/subscripts) inside each white box.

#### Column 1 (far left): NeuralMD overview
- **Background color:** Very light lavender/lilac (#EDE4F0 approximately), with a thin light-purple border.
- **Header:** "NeuralMD:" in bold black text at the top of the block.
- **Content (top section):** A white box containing pseudocode-style text in a monospaced or serif font:
  ```
  func(v^(l), x^(l), t, condition):
      F^(l) = BindingNet(v^(l), x^(l), condition)    [BindingNet is underlined/boxed]
      a^(l) = F^(l) / m
      return [a^(l), v^(l)]

  x̂^(l)_1, ..., x̂^(l)_T = NeuralMD(func, [v^(l)_0, x^(l)_0], T, C)
  ```
- **Content (bottom section):** Below, labeled "BindingNet:" in bold, a **dataflow diagram** shows:
  - Two input arrows at the top: "f^(l), x^(l)" on the left and "f^(p), x^(p)_N, x^(p)_Cα, x_C" on the right.
  - Two side-by-side colored boxes:
    - Left box: **Light green background** (#D5E8D4), text "BindingNet-Ligand", thin dark-green border.
    - Right box: **Light blue background** (#DAE8FC), text "BindingNet-Protein", thin dark-blue border.
  - Both boxes have downward arrows merging into a single box below:
    - **Light pink/mauve background** (#E6D0DE), text "BindingNet-Complex", thin dark-pink border.
  - A downward arrow from BindingNet-Complex leads to the output: "F^(l)" with a downward arrow symbol.

#### Column 2: BindingNet-Ligand
- **Background color:** Light yellow/cream (#FFF8E1 or #FEF3CD), thin golden border.
- **Header:** "BindingNet-Ligand:" in bold black text.
- **Inputs at top:** Two downward arrows labeled "f^(l)" and "x^(l)" in italic black text.
- **Processing steps (top to bottom, each in a white rounded-rectangle box with thin black border):**
  1. Box: "z^(l) = Embedding"
  2. Box: "h^(l)_i = Agg(x^(l)_i − x^(l)_j) · z^(l)_i"
  3. Box: "h^(l)_ij = (h^(l)_i ⊕ h^(l)_j) · F_ligand"
     - To the right of this box, a **small vertical label** in a colored sidebar reads "F_ligand" rotated 90° (text running vertically), on a **light green background strip** (#C8E6C9), indicating the scalarization step uses the ligand vector frame.
  4. Box: "h^(l)_i, vec^(l)_i = MPNN(h^(l)_ij, x^(l)_i − x^(l)_j, z^(l)_i, z^(l)_j)"
- **Outputs at bottom:** Two downward arrows labeled "h^(l), vec^(l)".
- **Connections:** Black downward arrows (~1.5px) connect each box to the next sequentially.

#### Column 3: BindingNet-Protein
- **Background color:** Light blue (#E3F2FD or #DCEEFB), thin blue border.
- **Header:** "BindingNet-Protein:" in bold black text.
- **Inputs at top:** Three downward arrows labeled "f^(p)" and "x^(p)_Cα, x^(p)_N, x^(p)_C".
- **Processing steps (top to bottom):**
  1. Two side-by-side small boxes: "z̃^(p) = Embedding" and "z^(p) = Embedding"
  2. Box: "h^(p)_i = Agg(x^(p)_i − x^(p)_j) · z^(p)_i"
  3. Box: "h^(p)_ij = (h^(p)_i ⊕ h^(p)_j) · F_residue"
     - To the right, a **vertical sidebar label** "F_protein" on a **light blue strip** (#BBDEFB), rotated 90°.
  4. Box: "h^(p)_i = MPNN(z̃^(p), h^(p)_i,j)"
- **Output at bottom:** One downward arrow labeled "h^(p)".

#### Column 4: BindingNet-Complex
- **Background color:** Light orange/peach (#FFF3E0 or #FFE8CC), thin orange border.
- **Header:** "BindingNet-Complex:" in bold black text.
- **Inputs at top:** Four downward arrows labeled "vec^(l)", "x^(l), h^(l)", "h^(p), x^(p)" — these come from the outputs of the Ligand and Protein modules.
- **Processing steps (top to bottom):**
  1. Box: "h_ij = (h^(l)_i + h^(p)_j) · (x^(l)_i − x^(p)_j)"
  2. Box: "h_ij = h_ij · F_complex"
     - To the right, a **vertical sidebar label** "F_complex" on a **light orange strip** (#FFE0B2), rotated 90°.
  3. Box: "F^(l)_i = MPNN(vec^(l)_i, h_ij, x^(l)_i − x^(p)_j)"
- **Output at bottom-right:** "F^(l)" with a downward arrow, in bold.

---

### Connections Between Columns in Panel (b)
- Dashed or solid **horizontal arrows** (black, ~1px) connect outputs of Column 2 (h^(l), vec^(l)) and Column 3 (h^(p)) to the inputs of Column 4 (BindingNet-Complex). These arrows curve or run horizontally at the bottom of Columns 2 and 3 and into the top of Column 4.
- Within the NeuralMD overview (Column 1), the BindingNet-Ligand box feeds into BindingNet-Complex, and BindingNet-Protein feeds into BindingNet-Complex, with converging arrows.

---

### Typography and Style Summary
| Element | Specification |
|---------|--------------|
| Overall background | Pure white (#FFFFFF) |
| Panel borders | Thin (~1px), light gray (#D0D0D0), rounded corners (~4px radius) |
| Section titles | Bold, black, ~16pt, sans-serif (e.g., Helvetica/Arial) |
| Module headers | Bold, black, ~12pt |
| Math text inside boxes | Black, italic variables, ~10-11pt, serif or standard math font |
| Processing step boxes | White fill (#FFFFFF), thin black border (~1px), rounded corners (~3px), ~6px internal padding |
| Arrow style | Solid black, ~1.5px thickness, filled triangular arrowheads (~6px) |
| Atom circles (panel a) | ~12-14px diameter, filled solid |
| Ligand atom color | Dark charcoal (#3C3C3C) |
| N atom color | Cyan/turquoise (#00BCD4) |
| Cα atom color | Pink/magenta (#E91E63) |
| C backbone atom color | Gray (#757575) |
| Ligand frame arrows | Dark teal (#009688), ~1.5px |
| Protein frame arrows | Dark red/crimson (#B71C1C), ~1.5px |
| Complex frame arrows/dashes | Dark purple (#7B1FA2), dashed (~1.5px) |
| Column backgrounds | Yellow (#FFF8E1), Blue (#E3F2FD), Orange (#FFF3E0), Lavender (#EDE4F0) |
| Vector frame sidebars | Slightly darker shade of column color, ~20px wide vertical strip |
| Sidebar text | Rotated 90° counter-clockwise, ~9pt, matching the frame name (F_ligand, F_protein, F_complex) |

---

### Figure Caption
**"Fig. 2 | The BindingNet architecture and integration."** **(a)** Illustration of the three granularities of vector frame bases utilized by BindingNet for geometric representation. **(b)** Overview of BindingNet's three core components and their integration into the NeuralMD pipeline for molecular dynamics simulation.