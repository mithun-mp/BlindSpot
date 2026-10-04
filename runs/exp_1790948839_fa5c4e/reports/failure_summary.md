# Behavioral Failure Diagnoses: Flipkart1

**Experiment ID**: `exp_1790948839_fa5c4e`
**Total Diagnosed Failures**: 1

### Failure #1: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_096a9aebe53b` (N/A)
- **Original Input**: "It's really a good and comfortable product"
- **Perturbed Input**: "It's really a good and comfortable product, however it is surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.58)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: -0.0258, SHAP: +0.0172 < 0.05).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: -0.0258, SHAP: +0.0172 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.
