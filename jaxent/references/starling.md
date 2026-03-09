# Caption
Fig. 1 | STARLING approach and model architecture. a, Deep learning has
revolutionized protein structure prediction, with major advances being
facilitated by large-scale evolutionary information. b, Structure prediction
methods for folded domains are poorly suited for predicting the behaviour of
IDRs. These limitations stem from the absence of a native-state structure and
because evolutionary information is often poorly captured in multiple sequence
alignments (MSAs) of IDRs. c, Generative text-to-image models enable the
creation of many unique and independent images consistent with a single input
prompt. d, IDR ensemble generation shares many similarities with text-to-image
generation; we required many distinct, uncorrelated conformers, all of which
are consistent with an input prompt (an amino acid sequence). e, STARLING
was trained on approximately 50,000 amino acid sequences at 150 mM ionic
strength and approximately 14,000 sequences at 20 mM and 300 mM ionic
strength. The sequences performed at 20 mM and 300 mM ionic strength are a
subset of those simulated at 150 mM ionic strength. For each sequence, hundreds
of distinct conformers were generated using coarse-grained molecular
dynamics simulations, and each conformer was converted into a distance map
(an image). Sequences were split into training, testing and validation sets. The
MARV cartoon was reproduced from ref. 61, Martin Steinegger. f, STARLING
makes use of a VAE to compress distance maps to a latent space, allowing a
denoising diffusion model to work in this latent space (‘latent diffusion’).
g, The overall architecture of the STARLING model combines a latent-space
probabilistic denoising diffusion model with a vision transformer architecture
using both convolutions and transformer blocks. Latent-space maps were
decoded to real space via the VAE decoder. Finally, distance maps can be
reconstructed into 3D coordinates via a parallelized multidimensional scaling
approach.

# STARLING: Methodology Description and Figure 1 Specification

---

## Methodology Description

### Short Description
STARLING is a latent diffusion generative model that rapidly predicts full coarse-grained conformational ensembles of intrinsically disordered proteins (IDRs) directly from amino acid sequence. It combines a variational autoencoder (VAE) for distance map compression with a denoising diffusion probabilistic model (DDPM) conditioned on protein sequence and ionic strength, analogous to how text-to-image models generate diverse images from a single text prompt.

### Inputs
- **Amino acid sequence** of an intrinsically disordered protein (up to 384 residues).
- **Ionic strength** conditioning value (between 20 mM and 300 mM; trained at 20, 150, and 300 mM anchor points).
- During training: approximately 12 million distance maps derived from coarse-grained molecular dynamics (MD) simulations of ~50,000 unique IDR sequences (20,349 natural + 50,214 synthetic disordered sequences) simulated using the Mpipi-GG one-bead-per-residue force field. Each conformation is represented as an n×n distance map (an "image"), where element (i, j) encodes the pairwise distance between residues i and j.

### Process
1. **Training data generation**: Natural and rationally designed (via GOOSE) IDR sequences are simulated with coarse-grained MD (Mpipi-GG force field, one bead per residue) at specified ionic strengths. Each resulting 3D conformation is converted into a 2D distance map. Sequences are split into train (70%), validation (15%), and test (15%) sets using MMseqs2-based sequence clustering to avoid data leakage.
2. **VAE training (Stage 1)**: A variational autoencoder with a ResNet18 architecture compresses full-resolution distance maps (up to 384×384) into a compact latent space (24×24). The encoder maps distance maps to a mean (μ) and standard deviation (σ) parameterizing a latent distribution; a latent vector z is sampled and the decoder reconstructs the distance map. RMSE of reconstruction is 1.16 Å on the held-out test set.
3. **DDPM training (Stage 2)**: A discrete-time denoising diffusion probabilistic model is trained in the compressed latent space ("latent diffusion"). A vision transformer architecture with 12 layers processes patchified 2D Gaussian noise, conditioned on the protein sequence (encoded via a learned sequence encoder) and ionic strength. The model learns to reverse a fixed forward noise-addition process, denoising random latent-space noise into latent-space distance maps conditioned on the input sequence.
4. **Inference (ensemble generation)**: During inference, 2D Gaussian noise is sampled, patchified via convolution, processed through the 12-layer vision transformer (conditioned on the input amino acid sequence and positional information), and output patches are re-convolved into a denoised latent-space representation. The VAE decoder then maps these latent representations back to full-resolution distance maps. Multiple independent inference rounds (default: 400 conformers, 30 denoising steps) run in parallel, each producing a distinct, uncorrelated distance map. Finally, distance maps are reconstructed into 3D coordinates using parallelized multidimensional scaling.

### Evaluation
- **Against simulations (held-out test set)**: Ensemble-averaged radius of gyration (Rg) and end-to-end distance (Re) compared to Mpipi-GG simulations across ~10,000 unseen sequences. Distribution overlap quantified via Hellinger distance (H) and Kolmogorov–Smirnov (KS) statistic. All pairwise inter-residue distance distributions compared between STARLING and simulation ensembles.
- **Against experimental data**: Average Rg compared against 133 SAXS-characterized IDRs (RMSE = 4.53 Å, R² = 0.90). Back-calculated SAXS scattering curves (via FOXS) compared against raw experimental profiles for 12+ IDRs. End-to-end distances compared against smFRET data for 16 length-matched sequences (RMSE = 6.7 Å).
- **Functional vignettes**: Application to Myc, RNA Pol II CTD, H1.0–ProTα and Nupr1–ProTα complexes, TRPV4 N-terminal IDR, microprotein IDRs, and sequence design tasks.

### Results
- Rg prediction: RMSE = 0.85 Å, R² = 0.996 at 150 mM; RMSE = 0.98 Å and 1.12 Å at 20 mM and 300 mM, respectively.
- Re prediction: RMSE = 3.48 Å, R² = 0.989 at 150 mM.
- Excellent distribution-level agreement (typical Hellinger distance H < 0.1) for both global dimensions and all pairwise inter-residue distances.
- State-of-the-art agreement with experimental SAXS and smFRET data across diverse IDR chemistries and lengths.
- Generation speed: ~400 conformers in ~12 s on GPU, ~20 s on Apple M3 CPU, ~6 min on Intel CPU; runtime largely independent of sequence length.
- Smooth interpolation across ionic strengths not seen during training (Pearson r = 0.98).
- Ensemble-first sequence design in <1 s per candidate (mean absolute error 0.94 Å for a 40-residue target).

---

## Detailed Figure Description (Figure 1: STARLING Approach and Model Architecture)

### Overall Layout
The figure is a multi-panel composite (panels **a** through **g**) arranged on a **pure white background**. The figure is wide (landscape-proportioned, roughly 2:1 aspect ratio). Panels are labeled with bold, black, lowercase letters (**a**, **b**, **c**, **d**, **e**, **f**, **g**) in the top-left corner of each panel, using a large sans-serif font (approximately 14–16 pt bold). The overall visual style is clean, schematic, and scientific — using flat illustrations, simple geometric shapes, muted grey backgrounds on key elements, thin black arrows, and small amounts of accent color. No drop shadows, no gradients on shapes (except for heatmap-style distance maps). Lines and arrows are thin (approximately 1–1.5 pt stroke), solid black unless otherwise noted. Text labels use a small sans-serif font (approximately 8–10 pt), black.

---

### Panel a — Structure prediction on foldable region (top-left)

**Title**: "Structure prediction on foldable region" in small black sans-serif text, centered above the panel.

**Layout**: A horizontal left-to-right pipeline, approximately 50% of the figure width in the top-left.

**Elements (left to right)**:
1. **Multiple sequence alignment (MSA) block**: A small rectangular grid (~60×40 px conceptually) showing rows of colored single-letter amino acid codes on a **bright yellow/gold background**. Each row is a sequence; individual residue letters are colored (red, green, blue, black) to indicate amino acid identity. Rows are tightly packed. Below this block, the label reads "Robust multiple sequence alignment" in small black text, left-aligned.
2. **Right-pointing solid black triangular arrow** (small filled triangle, ~8 px wide) connecting to:
3. **Three sequential grey rectangles** representing neural network processing layers. These are tall, narrow, light grey rectangles (~25×50 px each) arranged in a row, each slightly tilted/staggered to suggest depth (3D perspective effect — like stacked cards receding to the right). Between each pair of grey rectangles is a small right-pointing black triangular arrow.
4. **Right-pointing black triangular arrow** to:
5. **Contact map**: A square black-and-white matrix image (~60×60 px) labeled "Contact map" above it. The matrix shows a prominent dark diagonal line (self-contacts) with scattered dark spots (off-diagonal contacts indicating tertiary structure). The label "Contact map" is in small black sans-serif text.
6. **Right-pointing black triangular arrow** to:
7. **3D folded protein structure**: A cartoon-style ribbon representation of a compact folded protein, rendered in **blue** (alpha helices as spirals, beta sheets as arrows, loops as tubes). This is a small illustration (~50×50 px), representing the successful output of structure prediction.

**Connecting element**: A long horizontal grey arrow runs beneath the entire pipeline from the MSA to the protein structure, spanning the full width of the panel, reinforcing the left-to-right flow.

---

### Panel b — Structure prediction on disordered region (top-right)

**Title**: "Structure prediction on disordered region" in small black sans-serif text, centered above the panel.

**Layout**: Horizontal left-to-right pipeline, positioned to the right of panel a, approximately the other 50% of the figure width in the top row.

**Elements (left to right)**:
1. **Poor MSA block**: Similar grid to panel a, but the alignment is sparse and fragmented — many gaps (shown as dashes or blank spaces), fewer conserved columns. The background is **light pastel (pink/salmon or light yellow-green)**, and the text is sparser, with colored residue letters but large empty/gapped regions. Below: "Poor multiple sequence alignment" label.
2. **Right-pointing black triangular arrow** to:
3. **Three stacked grey rectangles** (identical style to panel a — light grey, slightly staggered, suggesting neural network layers). Small black arrows between them.
4. **Right-pointing black triangular arrow** to:
5. **Contact map**: A square matrix image, but this time the matrix is almost entirely **white/empty** except for the strong dark diagonal line. Essentially no off-diagonal contacts — representing the failure to identify tertiary contacts for a disordered protein. Labeled "Contact map" above.
6. **Right-pointing black triangular arrow** to:
7. **Unstructured protein**: A thin, wiggly, open line drawing in **dark gold/yellow-brown** color, representing a single extended, unstructured, random-coil-like protein conformation. This is a loose, wandering line with no secondary structure features — contrasting with the compact blue structure in panel a.

**Connecting element**: A long horizontal grey arrow runs beneath the pipeline.

---

### Panel c — Text-to-image analogy (middle-left)

**Layout**: Horizontal pipeline, positioned below panel a, occupying roughly the left 45% of the figure's middle row.

**Elements (left to right)**:
1. **Prompt box**: A small rectangle with a **bright yellow/gold border** (2 pt stroke, no fill or very light yellow fill). Inside, the text reads **'Birds on a branch'** in a small black sans-serif font (with single quotes). Below the box: "Prompt (phrase)" label in small black text.
2. **Right-pointing black triangular arrow** to:
3. **Text-to-image model**: A **dark grey/charcoal rounded rectangle** (~70×50 px) representing the model. Inside or overlaid: a stylized icon suggesting an AI/neural network model (a simple abstract pattern of black-and-white pixels or a small abstract graphic).
4. **Right-pointing black triangular arrow** to:
5. **Four grey placeholder rectangles** arranged in a 2×2 grid, each ~40×40 px, light grey, representing output image slots. To their right (or partially overlapping):
6. **Four distinct bird photographs**: Four small photographic images (~40×40 px each) arranged in a 2×2 grid, each showing a different bird on a branch. The images are naturalistic photographs (different bird species, different backgrounds — e.g., a seagull-like bird on a wooden post, a red bird on a branch, a white bird perched, etc.). These are actual photo-quality images, not illustrations. Below the images: **"Images"** label, and below that: "Four distinct and uncorrelated images" in small black text.

Below the box: "Text-to-image Model" label. Below the prompt: "Prompt (phrase)".

---

### Panel d — STARLING analogy (middle-right)

**Layout**: Horizontal pipeline, positioned to the right of panel c, occupying roughly the right 55% of the middle row.

**Elements (left to right)**:
1. **Protein sequence prompt box**: A small rectangle with a **light yellow/gold border** (matching panel c style). Inside: four rows of amino acid sequence text in monospaced font. Each row is a sequence string (e.g., "GSIGHEAGHSNW", "AGQGHRKPGHAH", "AGSQGHRKKPGH", "GWSMGHHQSQPK"). Certain residues are highlighted in **red** (e.g., G), **green** (e.g., H), and **blue/magenta** (e.g., specific residues) to indicate amino acid properties. Below: "Prompt (protein sequence)" label.
2. **Right-pointing black triangular arrow** to:
3. **STARLING model box**: A **light grey rounded rectangle with a subtle gradient or shadow** (~80×60 px). Inside: the word **"STARLING"** in bold black sans-serif text. A small bird icon (a starling silhouette, grey) is positioned above or beside the text within the box.
4. **Right-pointing black triangular arrow** to:
5. **"Conformers" label box**: A small white rectangle with a thin black border, containing the word **"Conformers"** in black text.
6. Below/beside this: **Four distinct conformer illustrations** arranged in a 2×2 grid. Each conformer is a small (~40×40 px) illustration of a coarse-grained protein conformation rendered as a blue dot-and-line chain (bead-model style), with each bead representing one residue. The four conformers have distinctly different spatial arrangements — some more compact, some more extended — all drawn with **blue/teal dots** connected by thin lines. Below: "Four distinct and uncorrelated conformers" label.

---

### Panel e — Training data generation (middle band, spanning left ~60% of figure)

**Layout**: A complex flowchart with two parallel paths (one red arrow going right for "Sequence clustering", one blue arrow going down-right for "Coarse-grained molecular dynamics simulation") that converge.

**Elements**:
1. **Left block — Natural sequences**: A **medium grey rectangle** containing the text "20,349 Natural disordered sequences" in small black text, stacked on three lines.
2. **Adjacent right block — Synthetic sequences**: A **darker grey/teal-tinted rectangle** (slightly taller) containing "50,214 Synthetic disordered sequences" in small white or light text.
3. **Red horizontal arrow** pointing right from the top of these blocks, labeled **"Sequence clustering"** in **red text** above/beside the arrow.
4. **Blue arrow** pointing down-right from the bottom of these blocks, labeled **"Coarse-grained molecular dynamics simulation"** in **blue text** below the arrow.
5. **MD simulation icon**: A small illustration of a computer/monitor with a coarse-grained bead model displayed on screen (colored beads — pink, green, yellow, blue — connected in a chain). Below: "One bead per residue" label. To the right of this:
6. **Distance maps**: Two or three small square heatmap images (~30×30 px each) representing distance maps. Each heatmap uses a **rainbow/thermal colormap** (dark blue along the diagonal, transitioning through green, yellow, to red/magenta for large distances). Labeled "Distance maps" below.
7. **MMseqs2 icon**: A small cartoon illustration (a colorful bird mascot — the MMseqs2 "MARV" logo, a stylized cartoon bird in an inflatable boat, multicolored). Labeled "MMseqs2" below.
8. **Train/Validation/Test split**: Three small white rectangles stacked vertically to the right, each with a thin black border, containing "Train (70%)", "Validation (15%)", and "Test (15%)" in small black text. Black arrows point from MMseqs2 to each of these three boxes.

The red arrow (sequence clustering) feeds into the MMseqs2 step. The blue arrow (MD simulation) feeds into the distance maps, which also feed into the train/val/test split.

---

### Panel f — Variational autoencoder (right side of middle band, ~35% width)

**Title**: "Variational autoencoder (distance map compression)" in small black text, centered above.

**Layout**: A horizontal left-to-right schematic of the VAE architecture.

**Elements (left to right)**:
1. **Input distance map**: A small square heatmap (rainbow colormap, ~30×30 px) with a vertical label "Distance map" along its left side (rotated 90°).
2. **Right-pointing black arrow** to:
3. **Encoder**: A set of **orange/amber colored rectangles** arranged as a progressively shrinking stack (tall-to-short trapezoid shape, 3–4 rectangles decreasing in height from left to right), representing the encoder compressing information. Labeled "Encoder" below.
4. **Right-pointing arrow** to:
5. **Latent space**: Two small boxes labeled **μ** (mu) and **σ** (sigma) in Greek letters, with lines converging to a single node/circle labeled **z** (the sampled latent vector). This represents the reparameterization trick. The whole subunit is labeled "Latent-space representation" below.
6. **Right-pointing arrow** to:
7. **Decoder**: A set of **orange/amber colored rectangles** arranged as a progressively growing stack (short-to-tall, mirroring the encoder in reverse), representing the decoder expanding information. Labeled "Decoder" below.
8. **Right-pointing black arrow** to:
9. **Output distance map**: A small square heatmap (same rainbow colormap style as input), labeled "Distance map" on the right side.

---

### Panel g — Full STARLING architecture (bottom row, spanning full figure width)

**Title**: Implied by context; no separate title — this is the most detailed architectural diagram.

**Layout**: A wide horizontal left-to-right pipeline spanning the entire bottom of the figure.

**Elements (left to right)**:

1. **2D Gaussian noise**: A small square image (~40×40 px) showing colorful random noise — a pixelated pattern with rainbow/multicolor noise (reds, blues, greens, yellows — resembling a noisy heatmap). Labeled "2D Gaussian noise" above in small black text.

2. **Downward arrow** into:

3. **Convolution block**: A small **purple/lavender rounded rectangle** labeled "Convolution" in small text below. This block takes the noise and produces patches.

4. **Label "Patches"** above the output: small square grid icons (~20×20 px) showing the noise image subdivided into a regular grid of small square patches (visible grid lines over a miniature version of the noise). An arrow points right.

5. **Positional information**: Below the patches, a downward-pointing curly arrow leads to a label "Positional information" in black text, indicating that positional embeddings are added.

6. **Vision transformer block**: A large **purple/lavender rounded rectangle** (~120×60 px), the central and largest element in panel g. Inside: "Vision transformer" in black text. Above the box: a label **"×12 layers"** with a thin bracket/line spanning the top, indicating the transformer has 12 layers. An arrow enters from the left (patches + positional info). An arrow enters from the bottom:

7. **Sequence conditioning input** (entering the Vision Transformer from below):
   - A vertical arrow labeled "Sequence conditioning" in black text points upward into the transformer block.
   - Below this arrow: a small schematic showing the sequence encoding process — several small horizontal bar icons (representing per-residue learned embeddings) in **grey and teal/dark cyan colors**, arranged vertically, feeding into a yellow rectangle containing amino acid sequence text in colored monospaced font: "GSIGHEAG" on one line, "..." in the middle, and "GWSMGHHQ" on the bottom line, with certain residues highlighted in **red** and **green**. Labeled "Prompt (protein sequence)" to the right.

8. **Output from Vision Transformer**: Arrow points right to another set of **"Patches"** — small grid icons similar to the input patches but now showing a more structured/denoised pattern (less noisy, more organized colors).

9. **Second Convolution block**: Another small **purple/lavender rounded rectangle** labeled "Convolution" below. This reassembles patches.

10. **Denoised latent space**: A small square image (~40×40 px) showing a partially structured heatmap pattern (organized colorful patterns, less noisy than input). Labeled "Denoised latent space" above.

11. **"Decoder" label and arrow**: A right-pointing arrow labeled "Decoder" above leads to:

12. **Four distance maps in a 2×2 grid**: Four small square heatmap images (~35×35 px each), each labeled "Distance map 1", "Distance map 2", "Distance map 3", "Distance map 4". Each uses a **rainbow/thermal colormap** (dark blue/purple along the diagonal, transitioning through green/yellow to warm colors off-diagonal). Each map is slightly different, representing four distinct conformers decoded from four independent denoising runs.

13. **Right-pointing solid black triangular arrow** (large, filled) to:

14. **"Structure reconstruction" label** above, and **four 3D conformer illustrations** in a 2×2 grid. Each conformer is drawn as a small **blue dot-and-line bead model** (~30×30 px), showing a coarse-grained protein chain with beads (residues) connected by thin lines. The four conformers have distinctly different spatial arrangements. Labeled "Conformer 1", "Conformer 2", "Conformer 3", "Conformer 4" below each.

---

### Color Palette Summary

| Element | Color | Hex (approximate) |
|---------|-------|--------------------|
| Background | Pure white | #FFFFFF |
| Panel labels (a–g) | Black, bold | #000000 |
| Body text / labels | Black | #000000 |
| MSA highlight (panel a) | Bright yellow/gold background | #FFD700 / #FFC107 |
| Folded protein ribbon | Medium blue | #3366CC |
| Disordered protein line | Dark gold / yellow-brown | #C8A000 / #B8860B |
| Prompt boxes border | Gold / yellow | #DAA520 |
| Grey model boxes | Light grey | #C0C0C0 / #D3D3D3 |
| STARLING box | Light grey with subtle border | #E0E0E0 |
| Neural network layer rectangles | Light grey | #CCCCCC |
| VAE encoder/decoder bars | Orange / amber | #E8943A / #F0A040 |
| Latent z node | White with black outline | — |
| Vision transformer block | Lavender / light purple | #B8A9D0 / #C4B0D8 |
| Convolution blocks | Lavender / light purple | #B8A9D0 |
| Distance map heatmaps | Rainbow colormap: dark blue → cyan → green → yellow → red/magenta | Sequential thermal |
| Conformer bead models | Blue / teal | #4488CC / #5599BB |
| Sequence clustering arrow/text | Red | #CC0000 / #E00000 |
| MD simulation arrow/text | Blue | #0000CC / #2255BB |
| Residue highlights (in sequences) | Red, green, blue/magenta for different amino acids | #CC0000, #228B22, #0000CC |
| Train/Val/Test boxes | White with thin black border | #FFFFFF |
| Arrows (flow) | Black, thin (1–1.5 pt) solid, with filled triangular arrowheads | #000000 |
| Long spanning arrows (panels a, b) | Medium grey, thin | #999999 |

### Typography
- **Panel labels**: Bold, sans-serif (e.g., Helvetica/Arial), ~14–16 pt, black.
- **Titles above panels**: Regular weight, sans-serif, ~9–10 pt, black.
- **In-figure labels**: Regular weight, sans-serif, ~7–9 pt, black.
- **Sequence text**: Monospaced font (e.g., Courier), ~7–8 pt, with individual residue coloring.
- **Greek letters** (μ, σ): Italic serif or sans-serif, ~9 pt.

### Arrow Styles
- **Inter-element flow arrows**: Thin (1–1.5 pt) solid black lines with small filled black triangular arrowheads (~6–8 px wide).
- **Long pipeline arrows** (panels a, b): Medium grey (#999999), thin (1 pt), spanning the full width of the panel with a triangular arrowhead at the right end.
- **Colored annotation arrows** (panel e): Red arrow (sequence clustering path, ~1.5 pt, with arrowhead) and blue arrow (MD simulation path, ~1.5 pt, with arrowhead).
- **Curly/curved arrow** (panel g, positional information): A curved black line with arrowhead, swooping downward.

### Icon / Illustration Styles
- **Protein structures**: Cartoon ribbon style (folded, panel a) or bead-and-stick coarse-grained representations (conformers, panels d, g) in blue.
- **Heatmaps/distance maps**: Small squares with smooth rainbow/thermal gradient colormaps; strong diagonal feature (dark blue) with off-diagonal variation.
- **Computer/monitor icon** (panel e): Simple line-drawing style, showing a desktop monitor with a bead model on screen.
- **Bird photos** (panel c): Actual photographic thumbnails of different bird species, square-cropped.
- **MMseqs2 mascot** (panel e): A colorful cartoon bird in a small inflatable raft (the official MARV mascot).
- **STARLING bird icon** (panel d): A small grey silhouette of a starling bird.

### Spatial Arrangement (approximate)
```
 ┌──────────── a ────────────┐ ┌──────────── b ────────────┐
 │  MSA → NN → ContactMap →  │ │  MSA → NN → ContactMap →  │
 │  FoldedProtein             │ │  DisorderedProtein         │
 └────────────────────────────┘ └────────────────────────────┘

 ┌──────── c ────────┐  ┌────────────── d ──────────────┐
 │ Prompt → T2I →    │  │ SeqPrompt → STARLING →        │
 │ 4 bird images     │  │ 4 conformers                   │
 └────────────────────┘  └────────────────────────────────┘

 ┌──────────────── e ─────────────────┐ ┌────── f ──────┐
 │ Sequences → MD → DistMaps →       │ │ VAE:          │
 │ MMseqs2 → Train/Val/Test          │ │ DM→Enc→z→Dec→DM│
 └────────────────────────────────────┘ └───────────────┘

 ┌──────────────────────────── g ─────────────────────────────────────┐
 │ Noise → Conv → Patches → ViT(×12, seq cond.) → Patches → Conv → │
 │ Denoised latent → Decoder → 4 DistMaps → 4 Conformers            │
 └────────────────────────────────────────────────────────────────────┘
```