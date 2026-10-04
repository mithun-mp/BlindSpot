# Probe-Level Behavioral Evidence: Multimodel Audit

**Experiment ID**: `exp_1790851320_dd1467`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_6e81` | NEGATION_INSERTION | "The movie was great and t..." → "The movie was not great a..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -1.4 | NO | `MISSING_FLIP` | **Misweighted** |
| `prb_93a8` | DOUBLE_NEGATION | "The movie was great and t..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_063f` | CONTRAST_NEGATIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | -0.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_1fa8` | CONTRAST_POSITIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_6e81`** [Misweighted / MISSING_FLIP]: Model recognized linguistic operator 'not' (LIME: -0.3239, SHAP: -0.6523), but opposing sentiment features ('top' (+0.1732)) outweighed the operator, preventing expected polarity reversal.
- **`prb_93a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_063f`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_1fa8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.