# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790834880_9104de`
**Total Diagnosed Failures**: 3

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to flip prediction ('POSITIVE -> POSITIVE') and effectively ignored syntactic operator (negation attribution = 0.49).
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to flip prediction ('POSITIVE -> POSITIVE') and effectively ignored syntactic operator (negation attribution = 0.49).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.63)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to flip prediction ('POSITIVE -> POSITIVE') and effectively ignored syntactic operator (negation attribution = 0.00).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to flip prediction ('POSITIVE -> POSITIVE') and effectively ignored syntactic operator (negation attribution = 0.00).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.42)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to flip prediction ('POSITIVE -> POSITIVE') and effectively ignored syntactic operator (negation attribution = 0.00).
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Blind. Model failed to flip prediction ('POSITIVE -> POSITIVE') and effectively ignored syntactic operator (negation attribution = 0.00).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.
