# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790977223_6c3ec3`
**Total Diagnosed Failures**: 4

### Failure #1: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_52ce79d7f530` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without barefoots.because it is a hardground football"
- **Perturbed Input**: "Good product good quality all are not good. But font play without barefoots.because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.74)` → `NEUTRAL (0.41)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.2805, SHAP: -0.4140), but opposing sentiment features ('good' (+0.2484)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEUTRAL' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.2805, SHAP: -0.4140), but opposing sentiment features ('good' (+0.2484)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Misweighted failures.

### Failure #2: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_17870bb01cb0` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without barefoots.because it is a hardground football"
- **Perturbed Input**: "It is not impossible that good product good quality all are good. But font play without barefoots.because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.74)` → `POSITIVE (0.57)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 17.22 percentage points under meaning-preserving perturbation.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Polarity preserved, but confidence collapsed by 17.22 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Misweighted failures.

### Failure #3: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_17870bb01cb0` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without barefoots.because it is a hardground football"
- **Perturbed Input**: "It is not impossible that good product good quality all are good. But font play without barefoots.because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.85)` → `NEGATIVE (0.82)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #4: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_52ce79d7f530` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without barefoots.because it is a hardground football"
- **Perturbed Input**: "Good product good quality all are not good. But font play without barefoots.because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.67)` → `NEUTRAL (0.49)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.2929, SHAP: -0.3933), but opposing sentiment features ('good' (+0.2199)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEUTRAL' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.2929, SHAP: -0.3933), but opposing sentiment features ('good' (+0.2199)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Misweighted failures.
