# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790597753_cea438`
**Total Diagnosed Failures**: 14

### Failure #1: [SPURIOUS] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_80889330b7c6` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was not boring and disappointing"
- **Observed Transition**: `NEGATIVE (1.00)` → `POSITIVE (0.98)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Spurious failures.

### Failure #2: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_8883f3615d65` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing, however it was surprisingly inferior in comparison."
- **Observed Transition**: `NEGATIVE (1.00)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [SPURIOUS] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_0896126a5725` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing, and the overall storyline was engaging."
- **Observed Transition**: `NEGATIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #4: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_0b010af6635d` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "It is not impossible that the movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Observed Transition**: `POSITIVE (0.45)` → `NEGATIVE (0.50)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #5: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_d794fddd78d0` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had somewhat excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Observed Transition**: `POSITIVE (0.45)` → `NEGATIVE (0.39)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Downtoner inverted polarity (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: Downtoner inverted polarity (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #6: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_80889330b7c6` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was not boring and disappointing"
- **Observed Transition**: `NEGATIVE (0.63)` → `POSITIVE (0.90)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Spurious failures.

### Failure #7: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_8883f3615d65` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing, however it was surprisingly inferior in comparison."
- **Observed Transition**: `NEGATIVE (0.63)` → `NEGATIVE (0.63)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #8: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_0896126a5725` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing, and the overall storyline was engaging."
- **Observed Transition**: `NEGATIVE (0.63)` → `NEGATIVE (0.48)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 15.01 percentage points under meaning-preserving perturbation.
- **Evidence**: Polarity preserved, but confidence collapsed by 15.01 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Misweighted failures.

### Failure #9: [SPURIOUS] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_80889330b7c6` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was not boring and disappointing"
- **Observed Transition**: `NEGATIVE (0.94)` → `POSITIVE (0.57)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Spurious failures.

### Failure #10: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_8883f3615d65` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing, however it was surprisingly inferior in comparison."
- **Observed Transition**: `NEGATIVE (0.94)` → `NEGATIVE (0.98)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #11: [SPURIOUS] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_0896126a5725` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing, and the overall storyline was engaging."
- **Observed Transition**: `NEGATIVE (0.94)` → `POSITIVE (0.62)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #12: [SPURIOUS] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_80889330b7c6` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was not boring and disappointing"
- **Observed Transition**: `NEGATIVE (0.99)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Spurious failures.

### Failure #13: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_8883f3615d65` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing, however it was surprisingly inferior in comparison."
- **Observed Transition**: `NEGATIVE (0.99)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #14: [SPURIOUS] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_0896126a5725` (N/A)
- **Original Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing"
- **Perturbed Input**: "The movie had excellent acting and beautiful visuals, but the storyline was boring and disappointing, and the overall storyline was engaging."
- **Observed Transition**: `NEGATIVE (0.99)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.
