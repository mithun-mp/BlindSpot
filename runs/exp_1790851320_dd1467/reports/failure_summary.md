# Behavioral Failure Diagnoses: Multimodel Audit

**Experiment ID**: `exp_1790851320_dd1467`
**Total Diagnosed Failures**: 1

### Failure #1: [MISWEIGHTED] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_6e8149c6f61d` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Model recognized linguistic operator 'not' (LIME: -0.3239, SHAP: -0.6523), but opposing sentiment features ('top' (+0.1732)) outweighed the operator, preventing expected polarity reversal.
- **Evidence**: Under negation_insertion, model transition 'POSITIVE -> POSITIVE' was diagnosed as Misweighted. Model recognized linguistic operator 'not' (LIME: -0.3239, SHAP: -0.6523), but opposing sentiment features ('top' (+0.1732)) outweighed the operator, preventing expected polarity reversal.
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Undetermined failures.
