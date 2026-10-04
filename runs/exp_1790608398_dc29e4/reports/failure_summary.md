# Behavioral Failure Diagnoses: E2E Semantic Ground-Truth Benchmark

**Experiment ID**: `exp_1790608398_dc29e4`
**Total Diagnosed Failures**: 7

### Failure #1: [SPURIOUS] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_e3fc47c979fb` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was not absolutely fantastic and thrilling."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Spurious failures.

### Failure #2: [MISWEIGHTED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_2f02bf775223` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was absolutely fantastic and thrilling, however it did not be reliably."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.80)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 19.99 percentage points under meaning-preserving perturbation.
- **Evidence**: Polarity preserved, but confidence collapsed by 19.99 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Misweighted failures.

### Failure #3: [SPURIOUS] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_e3fc47c979fb` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was not absolutely fantastic and thrilling."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Spurious failures.

### Failure #4: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_e3fc47c979fb` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was not absolutely fantastic and thrilling."
- **Observed Transition**: `POSITIVE (0.99)` → `NEGATIVE (0.83)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Spurious failures.

### Failure #5: [SPURIOUS] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_e3fc47c979fb` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was not absolutely fantastic and thrilling."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Spurious failures.

### Failure #6: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_2f02bf775223` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was absolutely fantastic and thrilling, however it did not be reliably."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.69)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 30.71 percentage points under meaning-preserving perturbation.
- **Evidence**: Polarity preserved, but confidence collapsed by 30.71 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Misweighted failures.

### Failure #7: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_e3fc47c979fb` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was not absolutely fantastic and thrilling."
- **Observed Transition**: `POSITIVE (0.99)` → `NEGATIVE (0.66)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Spurious failures.
