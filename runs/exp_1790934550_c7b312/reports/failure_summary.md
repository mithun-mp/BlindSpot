# Behavioral Failure Diagnoses: movieboring

**Experiment ID**: `exp_1790934550_c7b312`
**Total Diagnosed Failures**: 4

### Failure #1: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_5a73af4c864a` (N/A)
- **Original Input**: "the movie was very boring but the ending was good"
- **Perturbed Input**: "the movie was very extremely boring but the ending was good"
- **Observed Transition**: `POSITIVE (0.46)` → `NEGATIVE (0.69)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under intensity, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Undetermined failures.

### Failure #2: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_b2a231404863` (N/A)
- **Original Input**: "the movie was very boring but the ending was good"
- **Perturbed Input**: "the movie was very somewhat boring but the ending was good"
- **Observed Transition**: `POSITIVE (0.46)` → `POSITIVE (0.68)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Expected polarity downtoning, but confidence increased by 21.99 percentage points (0.46 → 0.68).
- **Evidence**: Expected polarity downtoning, but confidence increased by 21.99 percentage points (0.46 → 0.68).
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #3: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_5a73af4c864a` (N/A)
- **Original Input**: "the movie was very boring but the ending was good"
- **Perturbed Input**: "the movie was very extremely boring but the ending was good"
- **Observed Transition**: `POSITIVE (0.36)` → `NEGATIVE (0.48)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under intensity, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Undetermined failures.

### Failure #4: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_3f66bcd63292` (N/A)
- **Original Input**: "the movie was very boring but the ending was good"
- **Perturbed Input**: "the film was very boring but the ending was good"
- **Observed Transition**: `POSITIVE (0.36)` → `NEUTRAL (0.35)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under synonym_substitution, model transition 'POSITIVE -> NEUTRAL' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Undetermined failures.
