# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790615553_58ae10`
**Total Diagnosed Failures**: 4

### Failure #1: [SPURIOUS] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_01db79cec89d` (N/A)
- **Original Input**: "The new security system is extremely reliable and protects users from dangerous attacks"
- **Perturbed Input**: "The new security system is extremely reliable and protects users from dangerous attacks, however it is surprisingly worn in comparison."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction ('POSITIVE -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction ('POSITIVE -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Spurious failures.

### Failure #2: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_01db79cec89d` (N/A)
- **Original Input**: "The new security system is extremely reliable and protects users from dangerous attacks"
- **Perturbed Input**: "The new security system is extremely reliable and protects users from dangerous attacks, however it is surprisingly worn in comparison."
- **Observed Transition**: `POSITIVE (0.77)` → `POSITIVE (0.52)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 24.81 percentage points under meaning-preserving perturbation.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Polarity preserved, but confidence collapsed by 24.81 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Misweighted failures.

### Failure #3: [SPURIOUS] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_01db79cec89d` (N/A)
- **Original Input**: "The new security system is extremely reliable and protects users from dangerous attacks"
- **Perturbed Input**: "The new security system is extremely reliable and protects users from dangerous attacks, however it is surprisingly worn in comparison."
- **Observed Transition**: `POSITIVE (1.00)` → `NEGATIVE (0.95)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction ('POSITIVE -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction ('POSITIVE -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Spurious failures.

### Failure #4: [MISWEIGHTED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_01db79cec89d` (N/A)
- **Original Input**: "The new security system is extremely reliable and protects users from dangerous attacks"
- **Perturbed Input**: "The new security system is extremely reliable and protects users from dangerous attacks, however it is surprisingly worn in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.52)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 46.94 percentage points under meaning-preserving perturbation.
- **Evidence**: Under contrast_negative_append, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Polarity preserved, but confidence collapsed by 46.94 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Misweighted failures.
