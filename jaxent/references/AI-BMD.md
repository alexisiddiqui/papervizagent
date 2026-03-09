# Caption
Fig. 1 | The overall pipeline of AI 2 BMD. Proteins are divided into protein units
by a fragmentation process. The AI 2 BMD potential is designed on the basis of
ViSNet, and the datasets are generated at the DFT level. It calculates the energy
and atomic forces for the whole protein. The AI 2 BMD simulation system is built
on these components and provides a generalizable solution for simulating the
MD of proteins. It achieves ab initio accuracy in energy and force calculations.
Through comprehensive analysis from both kinetics and thermodynamics
perspectives, AI 2 BMD exhibits good alignment with wet-lab experimental data
and detects different phenomena than MM.

## Methodology Description

### Short Description
AI²BMD is an AI-based ab initio biomolecular dynamics system that fragments proteins into dipeptide units, trains machine learning force fields (ViSNet) on DFT-level data for each unit type, and reassembles energies/forces to simulate full-atom proteins with quantum-chemical accuracy at orders-of-magnitude lower computational cost.

### Inputs
- Full-atom protein structures of arbitrary size and composition (tested on proteins ranging from 175 to 13,728 atoms)
- The 20 standard amino acid types, which define the 21 possible protein unit types (20 dipeptides + Ace-Nme)
- DFT-level quantum chemistry data: ~20.88 million conformations generated via AIMD simulations using the M06-2X functional with the 6-31g* basis set
- Explicit solvent modeled by the AMOEBA polarizable force field

### Process
1. **Fragmentation**: A protein is decomposed into overlapping dipeptide units using a sliding-window approach along the polypeptide chain. Each dipeptide consists of one amino acid capped with acetyl (Ace) and N-methylamino (Nme) groups. Overlapping Ace-Nme fragments connect successive dipeptides. This yields only 21 distinct unit types, ensuring generalizability to any protein.
2. **Dataset Construction / Modelling**: For each of the 21 protein unit types, main-chain dihedral angles (φ, ψ) are systematically scanned, and AIMD simulations at the DFT level are run to generate comprehensive conformational sampling. This produces a dataset of ~20.88 million conformations with DFT-computed energies and forces.
3. **AI²BMD Potential Training (ViSNet)**: ViSNet, a geometric deep learning model, is trained on each protein unit's dataset as an energy-conserving potential. It takes atomic coordinates and types as input and predicts potential energy; forces are derived as negative gradients of energy with respect to coordinates.
4. **Energy and Force Calculation**: At each MD simulation step, the protein is fragmented, ViSNet computes energies/forces for each unit, and results are reassembled by summing dipeptide contributions and subtracting overlapping Ace-Nme contributions. Non-overlapping inter-unit interactions are handled via Coulomb and Lennard-Jones potentials.
5. **Simulation**: The AI²BMD simulation program runs MD in an NVT ensemble with 1-fs time steps. Protein forces come from ViSNet; solvent forces come from the AMOEBA force field. An asynchronous client-server architecture distributes fragment calculations across multiple GPUs.

### Evaluation
- **Energy/force accuracy**: Compared against DFT reference values and classical MM (ff19SB) for 9 proteins (175–13,728 atoms). Metrics: mean absolute error (MAE) for energy and force per atom.
- **Conformational space exploration**: 3J(HN, Hα) coupling constants derived from simulation trajectories compared to NMR experiments (Pearson correlation). Protein folding/unfolding observed for chignolin.
- **Thermodynamic properties**: Melting temperature (Tm), free-energy difference (ΔG), enthalpy change (ΔH), and heat capacity change (ΔCp) estimated for fast-folding and two-state proteins, compared against experimental calorimetry/spectroscopy data.
- **Computational efficiency**: Wall-clock time per simulation step compared to DFT, DPMD, Allegro, AMOEBA, and Amber ff19SB.

### Results
- Energy MAE ~0.045 kcal/mol (vs. MM's 3.198 kcal/mol); force MAE ~0.078 kcal/mol/Å (vs. MM's 8.125 kcal/mol/Å) on protein units.
- Pearson correlation with NMR J-couplings: ρ = 0.924 (AI²BMD) vs. ρ = 0.543 (MM).
- Melting temperatures and thermodynamic quantities closely match experimental values, outperforming MM.
- Computational speedup of >6 orders of magnitude over DFT for the largest protein tested (13,728 atoms).

---

## Figure Description (Figure 1: The Overall Pipeline of AI²BMD)

### Overall Layout
The figure is a wide, horizontally oriented schematic on a **pure white background**. It flows left-to-right through four major stages, with a secondary results/output column on the far right. The layout has two horizontal tiers: an **upper tier** showing the high-level data flow (protein → neural network → trajectories → analysis), and a **lower tier** showing the corresponding detailed substeps (protein units → DFT datasets → energy/force outputs → simulation snapshots).

### Stage Labels
Beneath the upper and lower tiers, there is a row of four **rounded-rectangle stage labels** connected by **thin gray horizontal arrows** pointing left-to-right. Each label box has a **light gray border** (approximately 1px), **white fill**, and contains centered text in **black, medium-weight sans-serif font**. The labels read, from left to right: **"Fragmentation"**, **"Modelling"**, **"Calculation"**, **"Simulation"**.

### Stage 1: Fragmentation (Left Column)
- **Upper tier**: Two 3D-rendered protein structures (ribbon diagrams) are shown, one slightly above and to the left of the other. The ribbons use the standard rainbow coloring convention: **blue at one terminus grading through cyan, green, yellow, orange to red** at the other terminus. These are photorealistic molecular visualization renderings (as from PyMOL or VMD), approximately 100×100 px each.
- **Below the proteins**, the label **"Proteins"** appears in **black sans-serif text, ~11pt**.
- A **thin gray downward arrow** connects to the lower tier.
- **Lower tier**: Several small ball-and-stick molecular models of dipeptide fragments are shown, arranged in a loose cluster. Atoms are colored with standard CPK conventions: **carbon = gray/dark gray, oxygen = red, nitrogen = blue, hydrogen = white, sulfur = yellow**. These are 3D-rendered small molecules (~40–60 px each), showing 4–5 distinct dipeptide units.
- Below, the label **"Protein units"** appears in **black sans-serif text**.

### Stage 2: Modelling (Second Column)
- **Upper tier**: A schematic of the ViSNet neural network architecture is depicted. It shows a series of **5–6 rectangular slabs** arranged in perspective (like stacked layers receding into depth), colored in a gradient sequence: the first two slabs are **warm red/coral**, the middle two are **orange/amber**, and the last two are **light yellow/cream**. Each slab has thin black outlines. A small **circle with a "⊕" symbol** (white circle, black plus sign) sits between the first group and the rest, suggesting a summation/combination operation. Above the neural network slabs, there are **2–3 small ball-and-stick molecular icons** (~20 px) representing input fragments, and a **rightward-pointing thin black arrow** exits the right side of the network stack.
- The label **"AI²BMD potential"** appears above or near this network diagram in **black sans-serif bold text, ~11pt**. The superscript "2" in AI²BMD is rendered as a proper superscript.
- A **thin gray downward arrow** connects to the lower tier.
- **Lower tier**: A single large circular/radial arrangement of ball-and-stick dipeptide models is shown—approximately 15–20 small molecular structures arranged in a ring/fan pattern radiating outward from a center point, representing the comprehensive dataset. The molecules use **CPK coloring**. Inside or near the ring, there is a small **white rectangular box with a thin black border** containing the text **"DFT"** in **black bold sans-serif**.
- Below, the label **"Datasets"** appears in **black sans-serif text**.

### Stage 3: Calculation (Third Column)
- This stage is visually represented in the **lower tier** primarily.
- **Lower tier**: Several 3D-rendered protein ribbon structures are shown (3–4 small structures, ~60–80 px each), displayed in various folded/partially unfolded conformations. These use **rainbow ribbon coloring** similar to Stage 1 but showing different conformational states (some more extended, some compact). These represent the calculated energy and force outputs being applied to different protein conformations.
- Below, the label **"Energy and atomic forces"** appears in **black sans-serif text**.

### Stage 4: Simulation (Fourth Column)
- **Upper tier**: A series of 4–5 overlapping/sequential 3D protein ribbon structures are shown, arranged to suggest a time-series or trajectory. They overlap slightly and are each in a slightly different conformation, colored with the **rainbow ribbon scheme**. This conveys the idea of conformational evolution over time. Above or near this cluster, the text **"Trajectories:"** appears, followed by the mathematical expression **"t + Δt → … → t + nΔt"** in **black italic serif/math font**.
- A **rightward-pointing thin black arrow** connects from the calculation stage to this trajectory visualization.

### Results Column (Far Right)
On the far right side of the figure, three small panels are stacked vertically, each representing a different type of analysis output. They are connected to the simulation stage by **thin blue right-angle connector lines** (L-shaped or stepped lines, medium blue color ~#3B82F6, ~1.5px thickness):

1. **Top panel — "Ab initio accuracy"**:
   - Title text **"Ab initio accuracy"** in **black sans-serif bold, ~10pt**, positioned above.
   - A small time-series plot (~100×60 px) with a **white background** and thin **black axes**. The y-axis is labeled **"RMSD"** with "High" at top and "Low" at bottom; the x-axis is labeled **"Time"**. Two overlapping noisy signal lines are shown: one in **black/dark gray** and one in **red/coral**, representing AI²BMD vs. reference, both fluctuating in a band.
   - To the right of or above this plot, a small **3D protein ribbon structure** (~40 px) is shown, colored in a **space-filling or ribbon style with rainbow colors**.

2. **Middle panel — "Kinetics"**:
   - Title text **"Kinetics"** in **black sans-serif bold, ~10pt**.
   - A small illustration (~80×60 px) showing a **3D protein structure** in a partially unfolded or dynamic state, rendered in a **space-filling representation** with atoms colored in CPK convention (lots of **red, blue, gray, white** spheres), suggesting molecular dynamics in action.

3. **Bottom panel — "Thermodynamics"**:
   - Title text **"Thermodynamics"** in **black sans-serif bold, ~10pt**.
   - A small plot (~100×60 px) with **white background** and thin **black axes**. The y-axis is labeled **"Dissociation fraction"**, the x-axis labeled from **"Low"** to **"High"**. The plot shows **2–3 sigmoidal curves** (S-shaped), in **black and red**, each shifted along the x-axis, representing melting curves at different conditions.
   - Below the x-axis, the label **"T_m"** (melting temperature) is shown with a small downward-pointing indicator.
   - Below the plot, the text **"Wet-lab experiment alignment"** appears in **black sans-serif, ~9pt**.
   - A small **3D protein ribbon** (~30 px) is shown near this panel.

### Connecting Arrows and Flow
- **Horizontal flow**: Thin **gray arrows** (~1px, solid) connect the four stage labels left-to-right.
- **Vertical flow**: Thin **gray arrows** connect upper-tier elements to lower-tier elements within each stage.
- **Right-side connectors**: Thin **blue stepped/right-angle lines** (~1.5px) connect from the simulation trajectory cluster to each of the three right-side analysis panels.

### Typography
- All text uses a **clean sans-serif font** (similar to Helvetica or Arial).
- Stage labels: ~11pt, regular weight, black.
- Sub-labels (Proteins, Protein units, Datasets, etc.): ~10pt, regular weight, black.
- Analysis panel titles: ~10pt, bold, black.
- Axis labels on small plots: ~8pt, regular weight, black.
- The figure caption below reads: **"Fig. 1 | The overall pipeline of AI²BMD."** in bold, followed by descriptive text in regular weight, all in black ~9pt serif font (Nature style).

### Color Palette Summary
- Background: **pure white (#FFFFFF)**
- Protein ribbons: **rainbow spectrum** (blue → cyan → green → yellow → orange → red)
- Neural network slabs: **red (#E74C3C)** → **orange (#F39C12)** → **yellow/cream (#F9E79F)**
- Molecular models: **CPK coloring** (C=gray, N=blue, O=red, H=white, S=yellow)
- Plot lines: **black** and **red (#E74C3C)**
- Connector lines to right panels: **medium blue (#3B82F6)**
- All borders and arrows: **black or dark gray (#333333)**, thin (~1px)