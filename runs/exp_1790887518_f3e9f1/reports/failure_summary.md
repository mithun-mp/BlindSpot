# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790887518_f3e9f1`
**Total Diagnosed Failures**: 23

### Failure #1: [MISWEIGHTED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.3239, SHAP: -0.6523), but opposing sentiment features ('top' (+0.1732)) outweighed the operator, preventing expected polarity reversal.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.3239, SHAP: -0.6523), but opposing sentiment features ('top' (+0.1732)) outweighed the operator, preventing expected polarity reversal.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #2: [UNDETERMINED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_93a8a314162b` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "It is not impossible that the movie was great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #3: [UNDETERMINED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_655b09534fa8` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was extremely great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Undetermined failures.

### Failure #4: [UNDETERMINED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_ad69074f6902` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was somewhat great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Undetermined failures.

### Failure #5: [UNDETERMINED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_0bcfcb23a772` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The film was great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Undetermined failures.

### Failure #6: [UNDETERMINED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `True`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #7: [UNDETERMINED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_1fa8d2280eef` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, and the overall storyline was engaging."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Undetermined failures.

### Failure #8: [UNDETERMINED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `True` (Expected Flip: `True`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #9: [UNDETERMINED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_93a8a314162b` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "It is not impossible that the movie was great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.95)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #10: [UNDETERMINED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_655b09534fa8` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was extremely great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Undetermined failures.

### Failure #11: [UNDETERMINED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_ad69074f6902` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was somewhat great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Undetermined failures.

### Failure #12: [UNDETERMINED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_0bcfcb23a772` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The film was great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Undetermined failures.

### Failure #13: [UNDETERMINED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.98)`
- **Prediction Flipped**: `True` (Expected Flip: `True`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #14: [UNDETERMINED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_1fa8d2280eef` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, and the overall storyline was engaging."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Undetermined failures.

### Failure #15: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.63)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: -0.0026, SHAP: -0.0017 < 0.05).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: -0.0026, SHAP: -0.0017 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #16: [UNDETERMINED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.73)`
- **Prediction Flipped**: `True` (Expected Flip: `True`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #17: [UNDETERMINED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_93a8a314162b` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "It is not impossible that the movie was great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #18: [UNDETERMINED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_655b09534fa8` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was extremely great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Undetermined failures.

### Failure #19: [UNDETERMINED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_ad69074f6902` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was somewhat great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Undetermined failures.

### Failure #20: [UNDETERMINED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_0bcfcb23a772` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The film was great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Undetermined failures.

### Failure #21: [UNDETERMINED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.87)`
- **Prediction Flipped**: `True` (Expected Flip: `True`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #22: [UNDETERMINED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_1fa8d2280eef` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, and the overall storyline was engaging."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Undetermined failures.

### Failure #23: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.42)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: +0.0063 < 0.05).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: +0.0063 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.
