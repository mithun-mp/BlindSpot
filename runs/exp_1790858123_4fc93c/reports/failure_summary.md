# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790858123_4fc93c`
**Total Diagnosed Failures**: 10

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
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

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
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.98)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

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
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.63)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #7: [UNDETERMINED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.73)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #8: [UNDETERMINED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.87)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #9: [UNDETERMINED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (0.99)` → `NEGATIVE (0.91)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.

### Failure #10: [UNDETERMINED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.42)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Undetermined probe expectation contract.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Undetermined. Undetermined probe expectation contract.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.
