# Behavioral Failure Diagnoses: FlipKart2

**Experiment ID**: `exp_1790951469_218101`
**Total Diagnosed Failures**: 15

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_e1bc1b0bcfac` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are good but 2/3 months after use color was fade It's original jockey t-shirt"
- **Observed Transition**: `NEGATIVE (0.99)` → `NEGATIVE (0.56)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'no' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **Evidence**: Under negation_removal, model transition 'NEGATIVE -> NEGATIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'no' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_removal perturbations to fix Undetermined failures.

### Failure #2: [MISWEIGHTED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_9c627a7c6f46` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt, but it delivered good results in practice."
- **Observed Transition**: `NEGATIVE (0.99)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under contrast_positive_append, model transition 'NEGATIVE -> POSITIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Undetermined failures.

### Failure #3: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_e1bc1b0bcfac` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are good but 2/3 months after use color was fade It's original jockey t-shirt"
- **Observed Transition**: `NEGATIVE (0.99)` → `NEGATIVE (0.94)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'no' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **Evidence**: Under negation_removal, model transition 'NEGATIVE -> NEGATIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'no' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_removal perturbations to fix Undetermined failures.

### Failure #4: [MISWEIGHTED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_9c627a7c6f46` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt, but it delivered good results in practice."
- **Observed Transition**: `NEGATIVE (0.99)` → `POSITIVE (0.94)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under contrast_positive_append, model transition 'NEGATIVE -> POSITIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Undetermined failures.

### Failure #5: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_571f2f88377e` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are good but 2/3 months after use color was fade It's not entirely non-original jockey t-shirt"
- **Observed Transition**: `NEGATIVE (0.60)` → `NEUTRAL (0.48)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under double_negation, model transition 'NEGATIVE -> NEUTRAL' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #6: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_c1d3675b76af` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are extremely good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Observed Transition**: `NEGATIVE (0.60)` → `NEGATIVE (0.43)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Expected polarity strengthening, but confidence dropped by 17.06 percentage points (0.60 → 0.43).
- **Evidence**: Under intensity, model transition 'NEGATIVE -> NEGATIVE' was diagnosed as Misweighted. Expected polarity strengthening, but confidence dropped by 17.06 percentage points (0.60 → 0.43).
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #7: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_9c627a7c6f46` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt, but it delivered good results in practice."
- **Observed Transition**: `NEGATIVE (0.60)` → `POSITIVE (0.77)`
- **Prediction Flipped**: `True` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'and' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **Evidence**: Under contrast_positive_append, model transition 'NEGATIVE -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'and' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Undetermined failures.

### Failure #8: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_e1bc1b0bcfac` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are good but 2/3 months after use color was fade It's original jockey t-shirt"
- **Observed Transition**: `NEGATIVE (0.91)` → `NEGATIVE (0.88)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'no' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **Evidence**: Under negation_removal, model transition 'NEGATIVE -> NEGATIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'no' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_removal perturbations to fix Undetermined failures.

### Failure #9: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_c1d3675b76af` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are extremely good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Observed Transition**: `NEGATIVE (0.91)` → `POSITIVE (0.59)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under intensity, model transition 'NEGATIVE -> POSITIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Undetermined failures.

### Failure #10: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_9c627a7c6f46` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt, but it delivered good results in practice."
- **Observed Transition**: `NEGATIVE (0.91)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under contrast_positive_append, model transition 'NEGATIVE -> POSITIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Undetermined failures.

### Failure #11: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_571f2f88377e` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are good but 2/3 months after use color was fade It's not entirely non-original jockey t-shirt"
- **Observed Transition**: `NEUTRAL (0.47)` → `POSITIVE (0.53)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under double_negation, model transition 'NEUTRAL -> POSITIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #12: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_c1d3675b76af` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are extremely good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Observed Transition**: `NEUTRAL (0.47)` → `POSITIVE (0.43)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under intensity, model transition 'NEUTRAL -> POSITIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Undetermined failures.

### Failure #13: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_e5186710a324` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are decent but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Observed Transition**: `NEUTRAL (0.47)` → `NEGATIVE (0.49)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under synonym_substitution, model transition 'NEUTRAL -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Undetermined failures.

### Failure #14: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_4ac621fcebbb` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt, however they were surprisingly bad in comparison."
- **Observed Transition**: `NEUTRAL (0.47)` → `NEGATIVE (0.62)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under contrast_negative_append, model transition 'NEUTRAL -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Undetermined failures.

### Failure #15: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_9c627a7c6f46` (N/A)
- **Original Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt"
- **Perturbed Input**: "All things are good but 2/3 months after use color was fade It's not original jockey t-shirt, but it delivered good results in practice."
- **Observed Transition**: `NEUTRAL (0.47)` → `POSITIVE (0.87)`
- **Prediction Flipped**: `True` (Expected Flip: `True`)
- **Diagnostic Reason**: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'and' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **Evidence**: Under contrast_positive_append, model transition 'NEUTRAL -> POSITIVE' was diagnosed as Blind. Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'and' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Undetermined failures.
