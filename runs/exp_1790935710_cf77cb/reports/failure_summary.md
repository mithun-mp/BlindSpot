# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790935710_cf77cb`
**Total Diagnosed Failures**: 8

### Failure #1: [MISWEIGHTED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_1f856e73cf96` (N/A)
- **Original Input**: "sun rises in the east and sets in the west"
- **Perturbed Input**: "insolate rises in the east and sets in the west"
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.86)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under synonym_substitution, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Undetermined failures.

### Failure #2: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_ab206b3a976b` (N/A)
- **Original Input**: "sun rises in the east and sets in the west"
- **Perturbed Input**: "It is not true that sun rises in the east and sets in the west"
- **Observed Transition**: `NEUTRAL (0.91)` → `NEUTRAL (0.71)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 20.11 percentage points under meaning-preserving perturbation.
- **Evidence**: Under negation_prefix, model transition 'NEUTRAL -> NEUTRAL' was diagnosed as Misweighted. Polarity preserved, but confidence collapsed by 20.11 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_prefix perturbations to fix Misweighted failures.

### Failure #3: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_3dd07af8ccc8` (N/A)
- **Original Input**: "sun rises in the east and sets in the west"
- **Perturbed Input**: "It is not impossible that sun rises in the east and sets in the west"
- **Observed Transition**: `NEUTRAL (0.91)` → `NEUTRAL (0.71)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 19.76 percentage points under meaning-preserving perturbation.
- **Evidence**: Under double_negation, model transition 'NEUTRAL -> NEUTRAL' was diagnosed as Misweighted. Polarity preserved, but confidence collapsed by 19.76 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Misweighted failures.

### Failure #4: [UNDETERMINED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_56f81359d889` (N/A)
- **Original Input**: "sun rises in the east and sets in the west"
- **Perturbed Input**: "sun rises in the east and sets in the west, however it does not rise reliably."
- **Observed Transition**: `NEUTRAL (0.91)` → `NEUTRAL (0.93)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Indeterminate behavioral transition.
- **Evidence**: Under contrast_negative_append, model transition 'NEUTRAL -> NEUTRAL' was diagnosed as Undetermined. Indeterminate behavioral transition.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #5: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_1f856e73cf96` (N/A)
- **Original Input**: "sun rises in the east and sets in the west"
- **Perturbed Input**: "insolate rises in the east and sets in the west"
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.88)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under synonym_substitution, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Undetermined failures.

### Failure #6: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_ab206b3a976b` (N/A)
- **Original Input**: "sun rises in the east and sets in the west"
- **Perturbed Input**: "It is not true that sun rises in the east and sets in the west"
- **Observed Transition**: `NEUTRAL (0.86)` → `NEGATIVE (0.55)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 44.2%, top token: 'true') rather than semantic content.
- **Evidence**: Under negation_prefix, model transition 'NEUTRAL -> NEGATIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 44.2%, top token: 'true') rather than semantic content.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_prefix perturbations to fix Undetermined failures.

### Failure #7: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_3dd07af8ccc8` (N/A)
- **Original Input**: "sun rises in the east and sets in the west"
- **Perturbed Input**: "It is not impossible that sun rises in the east and sets in the west"
- **Observed Transition**: `NEUTRAL (0.86)` → `POSITIVE (0.76)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 42.0%, top token: 'impossible') rather than semantic content.
- **Evidence**: Under double_negation, model transition 'NEUTRAL -> POSITIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 42.0%, top token: 'impossible') rather than semantic content.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #8: [UNDETERMINED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_56f81359d889` (N/A)
- **Original Input**: "sun rises in the east and sets in the west"
- **Perturbed Input**: "sun rises in the east and sets in the west, however it does not rise reliably."
- **Observed Transition**: `NEUTRAL (0.86)` → `NEUTRAL (0.78)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Indeterminate behavioral transition.
- **Evidence**: Under contrast_negative_append, model transition 'NEUTRAL -> NEUTRAL' was diagnosed as Undetermined. Indeterminate behavioral transition.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.
