# Behavioral Failure Diagnoses: E2E Semantic Ground-Truth Benchmark

**Experiment ID**: `exp_1790612296_7b62a3`
**Total Diagnosed Failures**: 2

### Failure #1: [MISWEIGHTED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_2f02bf775223` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was absolutely fantastic and thrilling, however it did not be reliably."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.80)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 19.99 percentage points under meaning-preserving perturbation.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Polarity preserved, but confidence collapsed by 19.99 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Misweighted failures.

### Failure #2: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_2f02bf775223` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was absolutely fantastic and thrilling, however it did not be reliably."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.69)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 30.71 percentage points under meaning-preserving perturbation.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Polarity preserved, but confidence collapsed by 30.71 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Misweighted failures.
