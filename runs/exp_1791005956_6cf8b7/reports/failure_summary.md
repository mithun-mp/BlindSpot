# Behavioral Failure Diagnoses: flipkartFootball2

**Experiment ID**: `exp_1791005956_6cf8b7`
**Total Diagnosed Failures**: 4

### Failure #1: [SPURIOUS] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_0ac3428fbbd3` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without bare foots ,because it is a hardground football"
- **Perturbed Input**: "It is not impossible that good product good quality all are good. But font play without bare foots,because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.99)` → `NEGATIVE (0.93)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 31.7%, top token: 'is') rather than semantic content.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 31.7%, top token: 'is') rather than semantic content.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #2: [SPURIOUS] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_0ac3428fbbd3` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without bare foots ,because it is a hardground football"
- **Perturbed Input**: "It is not impossible that good product good quality all are good. But font play without bare foots,because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.72)` → `NEGATIVE (0.55)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 37.3%, top token: 'is') rather than semantic content.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Spurious. Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 37.3%, top token: 'is') rather than semantic content.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #3: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_0ac3428fbbd3` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without bare foots ,because it is a hardground football"
- **Perturbed Input**: "It is not impossible that good product good quality all are good. But font play without bare foots,because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.81)` → `NEGATIVE (0.88)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Evidence**: Under double_negation, model transition 'POSITIVE -> NEGATIVE' was diagnosed as Misweighted. Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Undetermined failures.

### Failure #4: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_559004d5d2f7` (N/A)
- **Original Input**: "Good product good quality all are good. But font play without bare foots ,because it is a hardground football"
- **Perturbed Input**: "Good product good quality all are not good. But font play without bare foots,because it is a hardground football"
- **Observed Transition**: `POSITIVE (0.67)` → `NEUTRAL (0.50)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.2451, SHAP: -0.3988), but opposing sentiment features ('good' (+0.1821)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> NEUTRAL' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.2451, SHAP: -0.3988), but opposing sentiment features ('good' (+0.1821)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Misweighted failures.
