# Probe-Level Behavioral Evidence: movieboring

**Experiment ID**: `exp_1790934550_c7b312`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_0917` | NEGATION_INSERTION | "the movie was very boring..." → "the movie was not very bo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5d81` | DOUBLE_NEGATION | "the movie was very boring..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5a73` | INTENSITY | "the movie was very boring..." → "the movie was very extrem..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b2a2` | INTENSITY | "the movie was very boring..." → "the movie was very somewh..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3f66` | SYNONYM_SUBSTITUTION | "the movie was very boring..." → "the film was very boring ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7309` | CONTRAST_NEGATIVE_APPEND | "the movie was very boring..." → "the movie was very boring..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.98) | POSITIVE → NEGATIVE | -1.7 | YES | `EXPECTED_FLIP` | **None** |
| `prb_dde1` | CONTRAST_POSITIVE_APPEND | "the movie was very boring..." → "the movie was very boring..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_0917`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5d81`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5a73`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_b2a2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3f66`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_7309`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_dde1`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_0917` | NEGATION_INSERTION | "the movie was very boring..." → "the movie was not very bo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.88) | POSITIVE (0.97) | POSITIVE → POSITIVE | +9.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5d81` | DOUBLE_NEGATION | "the movie was very boring..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.88) | POSITIVE (0.97) | POSITIVE → POSITIVE | +8.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5a73` | INTENSITY | "the movie was very boring..." → "the movie was very extrem..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.88) | POSITIVE (0.84) | POSITIVE → POSITIVE | -3.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b2a2` | INTENSITY | "the movie was very boring..." → "the movie was very somewh..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.88) | POSITIVE (0.87) | POSITIVE → POSITIVE | -1.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3f66` | SYNONYM_SUBSTITUTION | "the movie was very boring..." → "the film was very boring ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.88) | POSITIVE (0.88) | POSITIVE → POSITIVE | +0.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7309` | CONTRAST_NEGATIVE_APPEND | "the movie was very boring..." → "the movie was very boring..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.88) | NEGATIVE (0.75) | POSITIVE → NEGATIVE | -12.7 | YES | `EXPECTED_FLIP` | **None** |
| `prb_dde1` | CONTRAST_POSITIVE_APPEND | "the movie was very boring..." → "the movie was very boring..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.88) | POSITIVE (0.97) | POSITIVE → POSITIVE | +9.3 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_0917`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5d81`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5a73`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_b2a2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3f66`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_7309`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_dde1`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_0917` | NEGATION_INSERTION | "the movie was very boring..." → "the movie was not very bo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.46) | POSITIVE (0.95) | POSITIVE → POSITIVE | +49.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5d81` | DOUBLE_NEGATION | "the movie was very boring..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.46) | POSITIVE (0.44) | POSITIVE → POSITIVE | -1.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5a73` | INTENSITY | "the movie was very boring..." → "the movie was very extrem..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.46) | NEGATIVE (0.69) | POSITIVE → NEGATIVE | +23.3 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_b2a2` | INTENSITY | "the movie was very boring..." → "the movie was very somewh..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.46) | POSITIVE (0.68) | POSITIVE → POSITIVE | +22.0 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_3f66` | SYNONYM_SUBSTITUTION | "the movie was very boring..." → "the film was very boring ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.46) | POSITIVE (0.36) | POSITIVE → POSITIVE | -9.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7309` | CONTRAST_NEGATIVE_APPEND | "the movie was very boring..." → "the movie was very boring..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.46) | NEGATIVE (0.67) | POSITIVE → NEGATIVE | +21.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_dde1` | CONTRAST_POSITIVE_APPEND | "the movie was very boring..." → "the movie was very boring..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.46) | POSITIVE (0.87) | POSITIVE → POSITIVE | +41.7 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_0917`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5d81`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5a73`** [Misweighted / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_b2a2`** [Misweighted / EXPECTED_PRESERVE]: Expected polarity downtoning, but confidence increased by 21.99 percentage points (0.46 → 0.68).
- **`prb_3f66`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_7309`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_dde1`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_0917` | NEGATION_INSERTION | "the movie was very boring..." → "the movie was not very bo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (1.00) | POSITIVE → POSITIVE | +2.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5d81` | DOUBLE_NEGATION | "the movie was very boring..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (1.00) | POSITIVE → POSITIVE | +1.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5a73` | INTENSITY | "the movie was very boring..." → "the movie was very extrem..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.94) | POSITIVE → POSITIVE | -3.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b2a2` | INTENSITY | "the movie was very boring..." → "the movie was very somewh..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | +0.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3f66` | SYNONYM_SUBSTITUTION | "the movie was very boring..." → "the film was very boring ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7309` | CONTRAST_NEGATIVE_APPEND | "the movie was very boring..." → "the movie was very boring..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.98) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | +0.9 | YES | `EXPECTED_FLIP` | **None** |
| `prb_dde1` | CONTRAST_POSITIVE_APPEND | "the movie was very boring..." → "the movie was very boring..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (1.00) | POSITIVE → POSITIVE | +2.2 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_0917`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5d81`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5a73`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_b2a2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3f66`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_7309`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_dde1`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_0917` | NEGATION_INSERTION | "the movie was very boring..." → "the movie was not very bo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.36) | POSITIVE (0.96) | POSITIVE → POSITIVE | +60.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5d81` | DOUBLE_NEGATION | "the movie was very boring..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.36) | POSITIVE (0.64) | POSITIVE → POSITIVE | +28.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5a73` | INTENSITY | "the movie was very boring..." → "the movie was very extrem..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.36) | NEGATIVE (0.48) | POSITIVE → NEGATIVE | +12.6 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_b2a2` | INTENSITY | "the movie was very boring..." → "the movie was very somewh..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.36) | POSITIVE (0.47) | POSITIVE → POSITIVE | +11.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3f66` | SYNONYM_SUBSTITUTION | "the movie was very boring..." → "the film was very boring ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.36) | NEUTRAL (0.35) | POSITIVE → NEUTRAL | -0.9 | NO | `UNEXPECTED_CHANGE` | **Misweighted** |
| `prb_7309` | CONTRAST_NEGATIVE_APPEND | "the movie was very boring..." → "the movie was very boring..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.36) | NEGATIVE (0.65) | POSITIVE → NEGATIVE | +29.0 | YES | `EXPECTED_FLIP` | **None** |
| `prb_dde1` | CONTRAST_POSITIVE_APPEND | "the movie was very boring..." → "the movie was very boring..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.36) | POSITIVE (0.64) | POSITIVE → POSITIVE | +28.8 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_0917`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5d81`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5a73`** [Misweighted / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_b2a2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3f66`** [Misweighted / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_7309`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_dde1`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.