# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790946053_d40697`
**Total Diagnosed Failures**: 7

### Failure #1: [MISWEIGHTED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.3239, SHAP: -0.6523), but opposing sentiment features ('top' (+0.1732)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.3239, SHAP: -0.6523), but opposing sentiment features ('top' (+0.1732)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #2: [MISWEIGHTED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `True` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.6345, SHAP: -0.8114), but opposing sentiment features ('notch' (-0.1344)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.6345, SHAP: -0.8114), but opposing sentiment features ('notch' (-0.1344)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #3: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (0.99)` → `NEGATIVE (0.80)`
- **Prediction Flipped**: `True` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.5024, SHAP: -0.5550), but opposing sentiment features ('top' (+0.1888)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.5024, SHAP: -0.5550), but opposing sentiment features ('top' (+0.1888)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #4: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.63)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: -0.0026, SHAP: -0.0017 < 0.05).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: -0.0026, SHAP: -0.0017 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #5: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.73)`
- **Prediction Flipped**: `True` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.4424, SHAP: -0.6267), but opposing sentiment features ('great' (-0.2031)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.4424, SHAP: -0.6267), but opposing sentiment features ('great' (-0.2031)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #6: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (0.99)` → `NEGATIVE (0.91)`
- **Prediction Flipped**: `True` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.5316, SHAP: -0.5867), but opposing sentiment features ('top' (+0.1567)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.5316, SHAP: -0.5867), but opposing sentiment features ('top' (+0.1567)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #7: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.42)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: +0.0063 < 0.05).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: +0.0063 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.
