# Probe-Level Behavioral Evidence: FlipKart2

**Experiment ID**: `exp_1790951469_218101`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_e1bc` | NEGATION_REMOVAL | "All things are good but 2..." → "All things are good but 2..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (0.99) | NEGATIVE (0.56) | NEGATIVE → NEGATIVE | -42.6 | NO | `MISSING_FLIP` | **Blind** |
| `prb_571f` | DOUBLE_NEGATION | "All things are good but 2..." → "All things are good but 2..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | -0.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c1d3` | INTENSITY | "All things are good but 2..." → "All things are extremely ..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8e4c` | INTENSITY | "All things are good but 2..." → "All things are somewhat g..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | -0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e518` | SYNONYM_SUBSTITUTION | "All things are good but 2..." → "All things are decent but..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4ac6` | CONTRAST_NEGATIVE_APPEND | "All things are good but 2..." → "All things are good but 2..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9c62` | CONTRAST_POSITIVE_APPEND | "All things are good but 2..." → "All things are good but 2..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (0.99) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +1.0 | YES | `UNEXPECTED_FLIP` | **Misweighted** |

### Probe Rationales & Evidence Notes
- **`prb_e1bc`** [Blind / MISSING_FLIP]: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'no' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **`prb_571f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_c1d3`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_8e4c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_e518`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_4ac6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_9c62`** [Misweighted / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_e1bc` | NEGATION_REMOVAL | "All things are good but 2..." → "All things are good but 2..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (0.99) | NEGATIVE (0.94) | NEGATIVE → NEGATIVE | -5.2 | NO | `MISSING_FLIP` | **Blind** |
| `prb_571f` | DOUBLE_NEGATION | "All things are good but 2..." → "All things are good but 2..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c1d3` | INTENSITY | "All things are good but 2..." → "All things are extremely ..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.97) | NEGATIVE → NEGATIVE | -1.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8e4c` | INTENSITY | "All things are good but 2..." → "All things are somewhat g..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e518` | SYNONYM_SUBSTITUTION | "All things are good but 2..." → "All things are decent but..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4ac6` | CONTRAST_NEGATIVE_APPEND | "All things are good but 2..." → "All things are good but 2..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9c62` | CONTRAST_POSITIVE_APPEND | "All things are good but 2..." → "All things are good but 2..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (0.99) | POSITIVE (0.94) | NEGATIVE → POSITIVE | -4.6 | YES | `UNEXPECTED_FLIP` | **Misweighted** |

### Probe Rationales & Evidence Notes
- **`prb_e1bc`** [Blind / MISSING_FLIP]: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'no' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **`prb_571f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_c1d3`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_8e4c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_e518`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_4ac6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_9c62`** [Misweighted / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_e1bc` | NEGATION_REMOVAL | "All things are good but 2..." → "All things are good but 2..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (0.60) | NEUTRAL (0.47) | NEGATIVE → NEUTRAL | -12.8 | NO | `EXPECTED_FLIP` | **None** |
| `prb_571f` | DOUBLE_NEGATION | "All things are good but 2..." → "All things are good but 2..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.60) | NEUTRAL (0.48) | NEGATIVE → NEUTRAL | -12.2 | NO | `UNEXPECTED_CHANGE` | **Misweighted** |
| `prb_c1d3` | INTENSITY | "All things are good but 2..." → "All things are extremely ..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.60) | NEGATIVE (0.43) | NEGATIVE → NEGATIVE | -17.1 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_8e4c` | INTENSITY | "All things are good but 2..." → "All things are somewhat g..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.60) | NEGATIVE (0.54) | NEGATIVE → NEGATIVE | -6.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e518` | SYNONYM_SUBSTITUTION | "All things are good but 2..." → "All things are decent but..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.60) | NEGATIVE (0.69) | NEGATIVE → NEGATIVE | +8.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4ac6` | CONTRAST_NEGATIVE_APPEND | "All things are good but 2..." → "All things are good but 2..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.60) | NEGATIVE (0.79) | NEGATIVE → NEGATIVE | +19.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9c62` | CONTRAST_POSITIVE_APPEND | "All things are good but 2..." → "All things are good but 2..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (0.60) | POSITIVE (0.77) | NEGATIVE → POSITIVE | +17.2 | YES | `UNEXPECTED_FLIP` | **Blind** |

### Probe Rationales & Evidence Notes
- **`prb_e1bc`** [None / EXPECTED_FLIP]: Model correctly shifted to NEUTRAL (NEGATIVE (NEGATIVE) → NEUTRAL (NEUTRAL)) as expected.
- **`prb_571f`** [Misweighted / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_c1d3`** [Misweighted / EXPECTED_PRESERVE]: Expected polarity strengthening, but confidence dropped by 17.06 percentage points (0.60 → 0.43).
- **`prb_8e4c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_e518`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_4ac6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_9c62`** [Blind / UNEXPECTED_FLIP]: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'and' (LIME: +0.0000, SHAP: +0.0000 < 0.05).

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_e1bc` | NEGATION_REMOVAL | "All things are good but 2..." → "All things are good but 2..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (0.91) | NEGATIVE (0.88) | NEGATIVE → NEGATIVE | -3.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_571f` | DOUBLE_NEGATION | "All things are good but 2..." → "All things are good but 2..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.91) | NEGATIVE (0.91) | NEGATIVE → NEGATIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c1d3` | INTENSITY | "All things are good but 2..." → "All things are extremely ..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.91) | POSITIVE (0.59) | NEGATIVE → POSITIVE | -31.6 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_8e4c` | INTENSITY | "All things are good but 2..." → "All things are somewhat g..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.91) | NEGATIVE (0.88) | NEGATIVE → NEGATIVE | -3.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e518` | SYNONYM_SUBSTITUTION | "All things are good but 2..." → "All things are decent but..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.91) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | +3.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4ac6` | CONTRAST_NEGATIVE_APPEND | "All things are good but 2..." → "All things are good but 2..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.91) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +8.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9c62` | CONTRAST_POSITIVE_APPEND | "All things are good but 2..." → "All things are good but 2..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (0.91) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +8.9 | YES | `UNEXPECTED_FLIP` | **Misweighted** |

### Probe Rationales & Evidence Notes
- **`prb_e1bc`** [Blind / MISSING_FLIP]: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'no' (LIME: +0.0000, SHAP: +0.0000 < 0.05).
- **`prb_571f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_c1d3`** [Misweighted / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_8e4c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_e518`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_4ac6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_9c62`** [Misweighted / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_e1bc` | NEGATION_REMOVAL | "All things are good but 2..." → "All things are good but 2..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEUTRAL (0.47) | NEUTRAL (0.50) | NEUTRAL → NEUTRAL | +2.8 | NO | `EXPECTED_FLIP` | **None** |
| `prb_571f` | DOUBLE_NEGATION | "All things are good but 2..." → "All things are good but 2..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.47) | POSITIVE (0.53) | NEUTRAL → POSITIVE | +5.4 | YES | `UNEXPECTED_CHANGE` | **Misweighted** |
| `prb_c1d3` | INTENSITY | "All things are good but 2..." → "All things are extremely ..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.47) | POSITIVE (0.43) | NEUTRAL → POSITIVE | -4.2 | YES | `UNEXPECTED_CHANGE` | **Misweighted** |
| `prb_8e4c` | INTENSITY | "All things are good but 2..." → "All things are somewhat g..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.47) | NEUTRAL (0.55) | NEUTRAL → NEUTRAL | +8.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e518` | SYNONYM_SUBSTITUTION | "All things are good but 2..." → "All things are decent but..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.47) | NEGATIVE (0.49) | NEUTRAL → NEGATIVE | +2.3 | YES | `UNEXPECTED_CHANGE` | **Misweighted** |
| `prb_4ac6` | CONTRAST_NEGATIVE_APPEND | "All things are good but 2..." → "All things are good but 2..." | `NEGATIVE (PRESERVE_POLARITY)` | NEUTRAL (0.47) | NEGATIVE (0.62) | NEUTRAL → NEGATIVE | +14.7 | YES | `UNEXPECTED_CHANGE` | **Misweighted** |
| `prb_9c62` | CONTRAST_POSITIVE_APPEND | "All things are good but 2..." → "All things are good but 2..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEUTRAL (0.47) | POSITIVE (0.87) | NEUTRAL → POSITIVE | +40.0 | YES | `MISSING_FLIP` | **Blind** |

### Probe Rationales & Evidence Notes
- **`prb_e1bc`** [None / EXPECTED_FLIP]: Model correctly shifted to NEUTRAL (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) as expected.
- **`prb_571f`** [Misweighted / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_c1d3`** [Misweighted / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_8e4c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_e518`** [Misweighted / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_4ac6`** [Misweighted / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_9c62`** [Blind / MISSING_FLIP]: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'and' (LIME: +0.0000, SHAP: +0.0000 < 0.05).