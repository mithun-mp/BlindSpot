# Probe-Level Behavioral Evidence: flipkartFootball2

**Experiment ID**: `exp_1791005956_6cf8b7`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_5590` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.99) | NEGATIVE (0.96) | POSITIVE → NEGATIVE | -3.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_0ac3` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | NEGATIVE (0.93) | POSITIVE → NEGATIVE | -6.3 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_3a4e` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4192` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b526` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2e20` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.99) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | +0.0 | YES | `EXPECTED_FLIP` | **None** |
| `prb_14f2` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.8 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_5590`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_0ac3`** [Spurious / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 31.7%, top token: 'is') rather than semantic content.
- **`prb_3a4e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4192`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_b526`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2e20`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_14f2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_5590` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.72) | NEGATIVE (0.55) | POSITIVE → NEGATIVE | -16.9 | YES | `EXPECTED_FLIP` | **None** |
| `prb_0ac3` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.72) | NEGATIVE (0.55) | POSITIVE → NEGATIVE | -16.5 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_3a4e` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.72) | POSITIVE (0.72) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4192` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.72) | POSITIVE (0.62) | POSITIVE → POSITIVE | -9.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b526` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.72) | POSITIVE (0.70) | POSITIVE → POSITIVE | -1.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2e20` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.72) | NEGATIVE (0.78) | POSITIVE → NEGATIVE | +6.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_14f2` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.72) | POSITIVE (0.98) | POSITIVE → POSITIVE | +26.1 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_5590`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_0ac3`** [Spurious / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 37.3%, top token: 'is') rather than semantic content.
- **`prb_3a4e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4192`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_b526`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2e20`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_14f2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_5590` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.69) | NEGATIVE (0.47) | POSITIVE → NEGATIVE | -22.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_0ac3` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.69) | POSITIVE (0.57) | POSITIVE → POSITIVE | -12.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3a4e` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.69) | POSITIVE (0.83) | POSITIVE → POSITIVE | +13.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4192` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.69) | POSITIVE (0.59) | POSITIVE → POSITIVE | -10.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b526` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.69) | POSITIVE (0.68) | POSITIVE → POSITIVE | -1.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2e20` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.69) | NEGATIVE (0.48) | POSITIVE → NEGATIVE | -21.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_14f2` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.69) | POSITIVE (0.91) | POSITIVE → POSITIVE | +22.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_5590`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_0ac3`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3a4e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4192`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_b526`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2e20`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_14f2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_5590` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.81) | NEGATIVE (0.94) | POSITIVE → NEGATIVE | +13.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_0ac3` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.81) | NEGATIVE (0.88) | POSITIVE → NEGATIVE | +6.8 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_3a4e` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.81) | POSITIVE (0.96) | POSITIVE → POSITIVE | +14.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4192` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.81) | POSITIVE (0.88) | POSITIVE → POSITIVE | +6.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b526` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.81) | POSITIVE (0.81) | POSITIVE → POSITIVE | +0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2e20` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.81) | NEGATIVE (0.95) | POSITIVE → NEGATIVE | +14.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_14f2` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.81) | POSITIVE (1.00) | POSITIVE → POSITIVE | +18.9 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_5590`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_0ac3`** [Misweighted / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_3a4e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4192`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_b526`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2e20`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_14f2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_5590` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.67) | NEUTRAL (0.50) | POSITIVE → NEUTRAL | -17.7 | NO | `UNEXPECTED_CHANGE` | **Misweighted** |
| `prb_0ac3` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.61) | POSITIVE → POSITIVE | -6.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3a4e` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.71) | POSITIVE → POSITIVE | +4.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4192` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.68) | POSITIVE → POSITIVE | +1.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b526` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.64) | POSITIVE → POSITIVE | -3.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2e20` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.67) | NEGATIVE (0.48) | POSITIVE → NEGATIVE | -19.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_14f2` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.87) | POSITIVE → POSITIVE | +19.4 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_5590`** [Misweighted / UNEXPECTED_CHANGE]: Model recognized linguistic operator 'not' (LIME: -0.2451, SHAP: -0.3988), but opposing sentiment features ('good' (+0.1821)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **`prb_0ac3`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3a4e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4192`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_b526`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2e20`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_14f2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.