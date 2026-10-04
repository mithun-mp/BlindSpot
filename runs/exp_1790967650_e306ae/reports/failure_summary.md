# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790967650_e306ae`
**Total Diagnosed Failures**: 3

### Failure #1: [MISWEIGHTED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_5675b2bfff4a` (N/A)
- **Original Input**: "Excellent shoes at low price light weight and comfortable, this is my second purchase from Asian shoes. Thank you Flipkart and dealer"
- **Perturbed Input**: "Excellent shoes at low price light weight and comfortable, this is my second purchase from Asian shoes. Thank you Flipkart and dealer, however it is surprisingly inferior in comparison."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.59)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'however' (LIME: +0.0000, SHAP: -0.0608), but opposing sentiment features ('inferior' (-0.4539)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Model recognized linguistic operator 'however' (LIME: +0.0000, SHAP: -0.0608), but opposing sentiment features ('inferior' (-0.4539)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #2: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_5675b2bfff4a` (N/A)
- **Original Input**: "Excellent shoes at low price light weight and comfortable, this is my second purchase from Asian shoes. Thank you Flipkart and dealer"
- **Perturbed Input**: "Excellent shoes at low price light weight and comfortable, this is my second purchase from Asian shoes. Thank you Flipkart and dealer, however it is surprisingly inferior in comparison."
- **Observed Transition**: `POSITIVE (0.98)` → `POSITIVE (0.90)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: -0.0193 < 0.05).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: -0.0193 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #3: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_5675b2bfff4a` (N/A)
- **Original Input**: "Excellent shoes at low price light weight and comfortable, this is my second purchase from Asian shoes. Thank you Flipkart and dealer"
- **Perturbed Input**: "Excellent shoes at low price light weight and comfortable, this is my second purchase from Asian shoes. Thank you Flipkart and dealer, however it is surprisingly inferior in comparison."
- **Observed Transition**: `POSITIVE (0.98)` → `POSITIVE (0.85)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: -0.0116 < 0.05).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: -0.0116 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.
