# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790926809_946e6d`
**Total Diagnosed Failures**: 5

### Failure #1: [MISWEIGHTED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.3239, SHAP: -0.6523), but opposing sentiment features ('top' (+0.1732)) outweighed the operator, preventing expected polarity reversal.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.3239, SHAP: -0.6523), but opposing sentiment features ('top' (+0.1732)) outweighed the operator, preventing expected polarity reversal.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #2: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (0.99)` → `NEGATIVE (0.80)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #3: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.63)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: -0.0026, SHAP: -0.0017 < 0.05).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: -0.0026, SHAP: -0.0017 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #4: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (0.99)` → `NEGATIVE (0.91)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #5: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.42)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: +0.0063 < 0.05).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: +0.0063 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.
