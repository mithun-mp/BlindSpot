# Behavioral Failure Diagnoses: fkf3

**Experiment ID**: `exp_1791007716_dac8cb`
**Total Diagnosed Failures**: 4

### Failure #1: [MISWEIGHTED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_97f0e64a57c6` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without barefoots ,because it is a hardground football"
- **Perturbed Input**: "It is not impossible that good product good quality all are good. But font play without barefoots,because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.69)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 30.06 percentage points under meaning-preserving perturbation.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Polarity preserved, but confidence collapsed by 30.06 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Misweighted failures.

### Failure #2: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_b1d9ce026ec4` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without barefoots ,because it is a hardground football"
- **Perturbed Input**: "Good product good quality all are not good. But font play without barefoots,because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.76)` → `NEUTRAL (0.41)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.2990, SHAP: -0.4186), but opposing sentiment features ('good' (+0.2432)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEUTRAL' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.2990, SHAP: -0.4186), but opposing sentiment features ('good' (+0.2432)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Misweighted failures.

### Failure #3: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_97f0e64a57c6` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without barefoots ,because it is a hardground football"
- **Perturbed Input**: "It is not impossible that good product good quality all are good. But font play without barefoots,because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.89)` → `NEGATIVE (0.79)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #4: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_b1d9ce026ec4` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without barefoots ,because it is a hardground football"
- **Perturbed Input**: "Good product good quality all are not good. But font play without barefoots,because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.67)` → `NEUTRAL (0.50)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.3005, SHAP: -0.3984), but opposing sentiment features ('good' (+0.2194)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEUTRAL' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.3005, SHAP: -0.3984), but opposing sentiment features ('good' (+0.2194)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Misweighted failures.
