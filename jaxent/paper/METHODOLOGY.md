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