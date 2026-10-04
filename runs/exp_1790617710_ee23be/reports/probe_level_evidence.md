# Probe-Level Behavioral Evidence: Multimodel health

**Experiment ID**: `exp_1790617710_ee23be`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d594` | NEGATION_INSERTION | "i am healthy but still ho..." → "i am not healthy but stil..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.86) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +14.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_18fb` | DOUBLE_NEGATION | "i am healthy but still ho..." → "It is not impossible that..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.86) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +13.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1faf` | INTENSITY | "i am healthy but still ho..." → "i am extremely healthy bu..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.86) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | +9.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_defc` | INTENSITY | "i am healthy but still ho..." → "i am somewhat healthy but..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.86) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | +9.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7dc6` | SYNONYM_SUBSTITUTION | "i am healthy but still ho..." → "i am goodish but still ho..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.86) | NEGATIVE (0.97) | NEGATIVE → NEGATIVE | +11.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f9f8` | CONTRAST_NEGATIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.86) | NEGATIVE (0.71) | NEGATIVE → NEGATIVE | -14.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d57d` | CONTRAST_POSITIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (0.86) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +14.2 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d594`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_18fb`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_1faf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_defc`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_7dc6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_f9f8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_d57d`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d594` | NEGATION_INSERTION | "i am healthy but still ho..." → "i am not healthy but stil..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.49) | NEGATIVE (0.94) | NEUTRAL → NEGATIVE | +45.5 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_18fb` | DOUBLE_NEGATION | "i am healthy but still ho..." → "It is not impossible that..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.49) | POSITIVE (0.70) | NEUTRAL → POSITIVE | +21.5 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_1faf` | INTENSITY | "i am healthy but still ho..." → "i am extremely healthy bu..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.49) | POSITIVE (0.78) | NEUTRAL → POSITIVE | +29.0 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_defc` | INTENSITY | "i am healthy but still ho..." → "i am somewhat healthy but..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.49) | POSITIVE (0.56) | NEUTRAL → POSITIVE | +7.6 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_7dc6` | SYNONYM_SUBSTITUTION | "i am healthy but still ho..." → "i am goodish but still ho..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.49) | POSITIVE (0.64) | NEUTRAL → POSITIVE | +15.4 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_f9f8` | CONTRAST_NEGATIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.49) | NEUTRAL (0.51) | NEUTRAL → NEUTRAL | +2.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d57d` | CONTRAST_POSITIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | `POSITIVE (REVERSE_POLARITY)` | NEUTRAL (0.49) | POSITIVE (0.92) | NEUTRAL → POSITIVE | +43.4 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d594`** [Spurious / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction ('NEUTRAL -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **`prb_18fb`** [Spurious / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **`prb_1faf`** [Spurious / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **`prb_defc`** [Spurious / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **`prb_7dc6`** [Spurious / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **`prb_f9f8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_d57d`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d594` | NEGATION_INSERTION | "i am healthy but still ho..." → "i am not healthy but stil..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.63) | NEGATIVE (0.83) | NEUTRAL → NEGATIVE | +19.4 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_18fb` | DOUBLE_NEGATION | "i am healthy but still ho..." → "It is not impossible that..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.63) | NEUTRAL (0.46) | NEUTRAL → NEUTRAL | -16.9 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_1faf` | INTENSITY | "i am healthy but still ho..." → "i am extremely healthy bu..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.63) | POSITIVE (0.59) | NEUTRAL → POSITIVE | -4.3 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_defc` | INTENSITY | "i am healthy but still ho..." → "i am somewhat healthy but..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.63) | NEUTRAL (0.70) | NEUTRAL → NEUTRAL | +6.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7dc6` | SYNONYM_SUBSTITUTION | "i am healthy but still ho..." → "i am goodish but still ho..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.63) | NEUTRAL (0.57) | NEUTRAL → NEUTRAL | -6.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f9f8` | CONTRAST_NEGATIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.63) | NEGATIVE (0.66) | NEUTRAL → NEGATIVE | +2.3 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_d57d` | CONTRAST_POSITIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | `POSITIVE (REVERSE_POLARITY)` | NEUTRAL (0.63) | POSITIVE (0.93) | NEUTRAL → POSITIVE | +29.1 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d594`** [Spurious / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction ('NEUTRAL -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **`prb_18fb`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 16.95 percentage points under meaning-preserving perturbation.
- **`prb_1faf`** [Spurious / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction ('NEUTRAL -> POSITIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **`prb_defc`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_7dc6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_f9f8`** [Spurious / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction ('NEUTRAL -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **`prb_d57d`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d594` | NEGATION_INSERTION | "i am healthy but still ho..." → "i am not healthy but stil..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.82) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +17.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_18fb` | DOUBLE_NEGATION | "i am healthy but still ho..." → "It is not impossible that..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.82) | NEGATIVE (0.94) | NEGATIVE → NEGATIVE | +11.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1faf` | INTENSITY | "i am healthy but still ho..." → "i am extremely healthy bu..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.82) | NEGATIVE (0.77) | NEGATIVE → NEGATIVE | -4.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_defc` | INTENSITY | "i am healthy but still ho..." → "i am somewhat healthy but..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.82) | NEGATIVE (0.87) | NEGATIVE → NEGATIVE | +5.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7dc6` | SYNONYM_SUBSTITUTION | "i am healthy but still ho..." → "i am goodish but still ho..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.82) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | +13.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f9f8` | CONTRAST_NEGATIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.82) | NEGATIVE (0.61) | NEGATIVE → NEGATIVE | -21.3 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_d57d` | CONTRAST_POSITIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (0.82) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +18.1 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d594`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_18fb`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_1faf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_defc`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_7dc6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_f9f8`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 21.30 percentage points under meaning-preserving perturbation.
- **`prb_d57d`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d594` | NEGATION_INSERTION | "i am healthy but still ho..." → "i am not healthy but stil..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +35.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_18fb` | DOUBLE_NEGATION | "i am healthy but still ho..." → "It is not impossible that..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.86) | NEGATIVE → NEGATIVE | +22.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1faf` | INTENSITY | "i am healthy but still ho..." → "i am extremely healthy bu..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.60) | NEGATIVE → NEGATIVE | -3.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_defc` | INTENSITY | "i am healthy but still ho..." → "i am somewhat healthy but..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.68) | NEGATIVE → NEGATIVE | +4.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7dc6` | SYNONYM_SUBSTITUTION | "i am healthy but still ho..." → "i am goodish but still ho..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.52) | NEGATIVE → NEGATIVE | -11.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f9f8` | CONTRAST_NEGATIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.56) | NEGATIVE → NEGATIVE | -7.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d57d` | CONTRAST_POSITIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (0.63) | POSITIVE (0.99) | NEGATIVE → POSITIVE | +35.7 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d594`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_18fb`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_1faf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_defc`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_7dc6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_f9f8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_d57d`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.