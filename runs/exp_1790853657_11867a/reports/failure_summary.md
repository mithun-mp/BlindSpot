# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790853657_11867a`
**Total Diagnosed Failures**: 12

### Failure #1: [UNDETERMINED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> POSITIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #2: [UNDETERMINED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_93a8a314162b` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "It is not impossible that the movie was great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> POSITIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #3: [UNDETERMINED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #4: [UNDETERMINED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_93a8a314162b` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "It is not impossible that the movie was great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.95)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> POSITIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #5: [UNDETERMINED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (0.99)` → `NEGATIVE (0.80)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #6: [UNDETERMINED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_93a8a314162b` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "It is not impossible that the movie was great and the acting was top notch."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.97)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> POSITIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #7: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.63)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0377, SHAP: -0.0017 < 0.05).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0377, SHAP: -0.0017 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #8: [UNDETERMINED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.73)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #9: [UNDETERMINED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_93a8a314162b` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "It is not impossible that the movie was great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> POSITIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #10: [UNDETERMINED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (0.99)` → `NEGATIVE (0.91)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #11: [UNDETERMINED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_93a8a314162b` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "It is not impossible that the movie was great and the acting was top notch."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.97)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> POSITIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #12: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.42)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0115, SHAP: +0.0063 < 0.05).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0115, SHAP: +0.0063 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.
