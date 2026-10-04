# Probe-Level Behavioral Evidence: fkf3

**Experiment ID**: `exp_1791007716_dac8cb`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_b1d9` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.99) | NEGATIVE (0.94) | POSITIVE → NEGATIVE | -5.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_97f0` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.69) | POSITIVE → POSITIVE | -30.1 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_0653` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c033` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a0ee` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3eae` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.99) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.7 | YES | `EXPECTED_FLIP` | **None** |
| `prb_37a7` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.6 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_b1d9`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_97f0`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 30.06 percentage points under meaning-preserving perturbation.
- **`prb_0653`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c033`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_a0ee`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3eae`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_37a7`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_b1d9` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.80) | NEGATIVE (0.53) | POSITIVE → NEGATIVE | -27.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_97f0` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.80) | POSITIVE (0.69) | POSITIVE → POSITIVE | -10.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0653` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.80) | POSITIVE (0.80) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c033` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.80) | POSITIVE (0.72) | POSITIVE → POSITIVE | -8.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a0ee` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.80) | POSITIVE (0.79) | POSITIVE → POSITIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3eae` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.80) | NEGATIVE (0.70) | POSITIVE → NEGATIVE | -9.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_37a7` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.80) | POSITIVE (0.98) | POSITIVE → POSITIVE | +18.4 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_b1d9`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_97f0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0653`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c033`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_a0ee`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3eae`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_37a7`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_b1d9` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.76) | NEUTRAL (0.41) | POSITIVE → NEUTRAL | -35.7 | NO | `UNEXPECTED_CHANGE` | **Misweighted** |
| `prb_97f0` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.76) | POSITIVE (0.63) | POSITIVE → POSITIVE | -13.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0653` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.76) | POSITIVE (0.86) | POSITIVE → POSITIVE | +10.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c033` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.76) | POSITIVE (0.67) | POSITIVE → POSITIVE | -9.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a0ee` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.76) | POSITIVE (0.75) | POSITIVE → POSITIVE | -1.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3eae` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.76) | NEGATIVE (0.43) | POSITIVE → NEGATIVE | -33.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_37a7` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.76) | POSITIVE (0.92) | POSITIVE → POSITIVE | +15.8 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_b1d9`** [Misweighted / UNEXPECTED_CHANGE]: Model recognized linguistic operator 'not' (LIME: -0.2990, SHAP: -0.4186), but opposing sentiment features ('good' (+0.2432)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **`prb_97f0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0653`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c033`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_a0ee`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3eae`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_37a7`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_b1d9` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.89) | NEGATIVE (0.91) | POSITIVE → NEGATIVE | +2.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_97f0` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.89) | NEGATIVE (0.79) | POSITIVE → NEGATIVE | -9.8 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_0653` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.89) | POSITIVE (0.97) | POSITIVE → POSITIVE | +8.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c033` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.89) | POSITIVE (0.91) | POSITIVE → POSITIVE | +2.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a0ee` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.89) | POSITIVE (0.91) | POSITIVE → POSITIVE | +1.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3eae` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.89) | NEGATIVE (0.93) | POSITIVE → NEGATIVE | +4.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_37a7` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.89) | POSITIVE (1.00) | POSITIVE → POSITIVE | +11.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_b1d9`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_97f0`** [Misweighted / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_0653`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c033`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_a0ee`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3eae`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_37a7`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_b1d9` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.67) | NEUTRAL (0.50) | POSITIVE → NEUTRAL | -17.4 | NO | `UNEXPECTED_CHANGE` | **Misweighted** |
| `prb_97f0` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.62) | POSITIVE → POSITIVE | -5.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0653` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.71) | POSITIVE → POSITIVE | +4.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c033` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.69) | POSITIVE → POSITIVE | +1.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a0ee` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.64) | POSITIVE → POSITIVE | -3.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3eae` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.67) | NEGATIVE (0.47) | POSITIVE → NEGATIVE | -19.8 | YES | `EXPECTED_FLIP` | **None** |
| `prb_37a7` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.87) | POSITIVE → POSITIVE | +19.6 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_b1d9`** [Misweighted / UNEXPECTED_CHANGE]: Model recognized linguistic operator 'not' (LIME: -0.3005, SHAP: -0.3984), but opposing sentiment features ('good' (+0.2194)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **`prb_97f0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0653`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c033`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_a0ee`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3eae`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_37a7`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.