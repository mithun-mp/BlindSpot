# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790858123_4fc93c`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_6e81` | NEGATION_INSERTION | "The movie was great and t..." → "The movie was not great a..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -1.4 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_93a8` | DOUBLE_NEGATION | "The movie was great and t..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_655b` | INTENSITY | "The movie was great and t..." → "The movie was extremely g..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_ad69` | INTENSITY | "The movie was great and t..." → "The movie was somewhat gr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0bcf` | SYNONYM_SUBSTITUTION | "The movie was great and t..." → "The film was great and th..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_063f` | CONTRAST_NEGATIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | POSITIVE (1.00) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | -0.3 | YES | `UNDETERMINED` | **Undetermined** |
| `prb_1fa8` | CONTRAST_POSITIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_6e81`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_93a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_655b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_ad69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0bcf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_063f`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_1fa8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_6e81` | NEGATION_INSERTION | "The movie was great and t..." → "The movie was not great a..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | POSITIVE (1.00) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.5 | YES | `UNDETERMINED` | **Undetermined** |
| `prb_93a8` | DOUBLE_NEGATION | "The movie was great and t..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.95) | POSITIVE → POSITIVE | -4.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_655b` | INTENSITY | "The movie was great and t..." → "The movie was extremely g..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_ad69` | INTENSITY | "The movie was great and t..." → "The movie was somewhat gr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0bcf` | SYNONYM_SUBSTITUTION | "The movie was great and t..." → "The film was great and th..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_063f` | CONTRAST_NEGATIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | POSITIVE (1.00) | NEGATIVE (0.98) | POSITIVE → NEGATIVE | -1.4 | YES | `UNDETERMINED` | **Undetermined** |
| `prb_1fa8` | CONTRAST_POSITIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_6e81`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_93a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_655b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_ad69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0bcf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_063f`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_1fa8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_6e81` | NEGATION_INSERTION | "The movie was great and t..." → "The movie was not great a..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | POSITIVE (0.99) | NEGATIVE (0.80) | POSITIVE → NEGATIVE | -19.0 | YES | `UNDETERMINED` | **Undetermined** |
| `prb_93a8` | DOUBLE_NEGATION | "The movie was great and t..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.97) | POSITIVE → POSITIVE | -1.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_655b` | INTENSITY | "The movie was great and t..." → "The movie was extremely g..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_ad69` | INTENSITY | "The movie was great and t..." → "The movie was somewhat gr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0bcf` | SYNONYM_SUBSTITUTION | "The movie was great and t..." → "The film was great and th..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_063f` | CONTRAST_NEGATIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | POSITIVE (0.99) | POSITIVE (0.63) | POSITIVE → POSITIVE | -36.1 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_1fa8` | CONTRAST_POSITIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_6e81`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_93a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_655b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_ad69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0bcf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_063f`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_1fa8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_6e81` | NEGATION_INSERTION | "The movie was great and t..." → "The movie was not great a..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | POSITIVE (1.00) | NEGATIVE (0.73) | POSITIVE → NEGATIVE | -27.2 | YES | `UNDETERMINED` | **Undetermined** |
| `prb_93a8` | DOUBLE_NEGATION | "The movie was great and t..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_655b` | INTENSITY | "The movie was great and t..." → "The movie was extremely g..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_ad69` | INTENSITY | "The movie was great and t..." → "The movie was somewhat gr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0bcf` | SYNONYM_SUBSTITUTION | "The movie was great and t..." → "The film was great and th..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_063f` | CONTRAST_NEGATIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | POSITIVE (1.00) | NEGATIVE (0.87) | POSITIVE → NEGATIVE | -12.8 | YES | `UNDETERMINED` | **Undetermined** |
| `prb_1fa8` | CONTRAST_POSITIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_6e81`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_93a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_655b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_ad69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0bcf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_063f`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_1fa8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_6e81` | NEGATION_INSERTION | "The movie was great and t..." → "The movie was not great a..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | POSITIVE (0.99) | NEGATIVE (0.91) | POSITIVE → NEGATIVE | -7.5 | YES | `UNDETERMINED` | **Undetermined** |
| `prb_93a8` | DOUBLE_NEGATION | "The movie was great and t..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.97) | POSITIVE → POSITIVE | -2.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_655b` | INTENSITY | "The movie was great and t..." → "The movie was extremely g..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_ad69` | INTENSITY | "The movie was great and t..." → "The movie was somewhat gr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0bcf` | SYNONYM_SUBSTITUTION | "The movie was great and t..." → "The film was great and th..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_063f` | CONTRAST_NEGATIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | POSITIVE (0.99) | POSITIVE (0.42) | POSITIVE → POSITIVE | -57.1 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_1fa8` | CONTRAST_POSITIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_6e81`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_93a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_655b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_ad69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0bcf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_063f`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_1fa8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.