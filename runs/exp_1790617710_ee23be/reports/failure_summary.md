# Behavioral Failure Diagnoses: Multimodel health

**Experiment ID**: `exp_1790617710_ee23be`
**Total Diagnosed Failures**: 10

### Failure #1: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_d59487c5df7c` (N/A)
- **Original Input**: "i am healthy but still hospitalized"
- **Perturbed Input**: "i am not healthy but still hospitalized"
- **Observed Transition**: `NEUTRAL (0.49)` → `NEGATIVE (0.94)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction ('NEUTRAL -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Evidence**: Under negation_insertion, model transition 'NEUTRAL -> NEGATIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction ('NEUTRAL -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Spurious failures.

### Failure #2: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_18fb2706a780` (N/A)
- **Original Input**: "i am healthy but still hospitalized"
- **Perturbed Input**: "It is not impossible that i am healthy but still hospitalized"
- **Observed Transition**: `NEUTRAL (0.49)` → `POSITIVE (0.70)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Evidence**: Under double_negation, model transition 'NEUTRAL -> POSITIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #3: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_1faf50373dfb` (N/A)
- **Original Input**: "i am healthy but still hospitalized"
- **Perturbed Input**: "i am extremely healthy but still hospitalized"
- **Observed Transition**: `NEUTRAL (0.49)` → `POSITIVE (0.78)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Evidence**: Under intensity, model transition 'NEUTRAL -> POSITIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Spurious failures.

### Failure #4: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_defcd4d250b4` (N/A)
- **Original Input**: "i am healthy but still hospitalized"
- **Perturbed Input**: "i am somewhat healthy but still hospitalized"
- **Observed Transition**: `NEUTRAL (0.49)` → `POSITIVE (0.56)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Evidence**: Under intensity, model transition 'NEUTRAL -> POSITIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Spurious failures.

### Failure #5: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_7dc6459a9d15` (N/A)
- **Original Input**: "i am healthy but still hospitalized"
- **Perturbed Input**: "i am goodish but still hospitalized"
- **Observed Transition**: `NEUTRAL (0.49)` → `POSITIVE (0.64)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Evidence**: Under synonym_substitution, model transition 'NEUTRAL -> POSITIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Spurious failures.

### Failure #6: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_d59487c5df7c` (N/A)
- **Original Input**: "i am healthy but still hospitalized"
- **Perturbed Input**: "i am not healthy but still hospitalized"
- **Observed Transition**: `NEUTRAL (0.63)` → `NEGATIVE (0.83)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction ('NEUTRAL -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Evidence**: Under negation_insertion, model transition 'NEUTRAL -> NEGATIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction ('NEUTRAL -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Spurious failures.

### Failure #7: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_18fb2706a780` (N/A)
- **Original Input**: "i am healthy but still hospitalized"
- **Perturbed Input**: "It is not impossible that i am healthy but still hospitalized"
- **Observed Transition**: `NEUTRAL (0.63)` → `NEUTRAL (0.46)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 16.95 percentage points under meaning-preserving perturbation.
- **Evidence**: Under double_negation, model transition 'NEUTRAL -> NEUTRAL' was diagnosed as Misweighted. Polarity preserved, but confidence collapsed by 16.95 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Misweighted failures.

### Failure #8: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_1faf50373dfb` (N/A)
- **Original Input**: "i am healthy but still hospitalized"
- **Perturbed Input**: "i am extremely healthy but still hospitalized"
- **Observed Transition**: `NEUTRAL (0.63)` → `POSITIVE (0.59)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Evidence**: Under intensity, model transition 'NEUTRAL -> POSITIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Spurious failures.

### Failure #9: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_f9f881eda7b2` (N/A)
- **Original Input**: "i am healthy but still hospitalized"
- **Perturbed Input**: "i am healthy but still hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEUTRAL (0.63)` → `NEGATIVE (0.66)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction ('NEUTRAL -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Evidence**: Under contrast_negative_append, model transition 'NEUTRAL -> NEGATIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction ('NEUTRAL -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Spurious failures.

### Failure #10: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_f9f881eda7b2` (N/A)
- **Original Input**: "i am healthy but still hospitalized"
- **Perturbed Input**: "i am healthy but still hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.82)` → `NEGATIVE (0.61)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 21.30 percentage points under meaning-preserving perturbation.
- **Evidence**: Under contrast_negative_append, model transition 'NEGATIVE -> NEGATIVE' was diagnosed as Misweighted. Polarity preserved, but confidence collapsed by 21.30 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Misweighted failures.
