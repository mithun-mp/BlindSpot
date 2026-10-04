# Behavioral Failure Diagnoses: FlipKart3FoootBall

**Experiment ID**: `exp_1790953982_26da69`
**Total Diagnosed Failures**: 2

### Failure #1: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_17870bb01cb0` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without barefoots.because it is a hardground football"
- **Perturbed Input**: "It is not impossible that good product good quality all are good. But font play without barefoots.because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.74)` → `POSITIVE (0.57)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 17.22 percentage points under meaning-preserving perturbation.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Polarity preserved, but confidence collapsed by 17.22 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Misweighted failures.

### Failure #2: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_17870bb01cb0` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without barefoots.because it is a hardground football"
- **Perturbed Input**: "It is not impossible that good product good quality all are good. But font play without barefoots.because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.85)` → `NEGATIVE (0.82)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.
