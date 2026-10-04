# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790977223_6c3ec3`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_52ce` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.99) | NEGATIVE (0.93) | POSITIVE → NEGATIVE | -6.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_1787` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.85) | POSITIVE → POSITIVE | -14.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0e0c` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c3fa` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eb25` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_29ea` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.99) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_f9e4` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.8 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_52ce`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_1787`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0e0c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c3fa`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_eb25`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_29ea`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_f9e4`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_52ce` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.79) | NEGATIVE (0.55) | POSITIVE → NEGATIVE | -24.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_1787` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.79) | POSITIVE (0.73) | POSITIVE → POSITIVE | -6.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0e0c` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.79) | POSITIVE (0.79) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c3fa` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.79) | POSITIVE (0.70) | POSITIVE → POSITIVE | -9.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eb25` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.79) | POSITIVE (0.74) | POSITIVE → POSITIVE | -4.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_29ea` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.79) | NEGATIVE (0.82) | POSITIVE → NEGATIVE | +2.8 | YES | `EXPECTED_FLIP` | **None** |
| `prb_f9e4` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.79) | POSITIVE (0.98) | POSITIVE → POSITIVE | +18.6 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_52ce`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_1787`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0e0c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c3fa`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_eb25`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_29ea`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_f9e4`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_52ce` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.74) | NEUTRAL (0.41) | POSITIVE → NEUTRAL | -33.7 | NO | `UNEXPECTED_CHANGE` | **Misweighted** |
| `prb_1787` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.74) | POSITIVE (0.57) | POSITIVE → POSITIVE | -17.2 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_0e0c` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.74) | POSITIVE (0.87) | POSITIVE → POSITIVE | +12.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c3fa` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.74) | POSITIVE (0.63) | POSITIVE → POSITIVE | -11.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eb25` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.74) | POSITIVE (0.73) | POSITIVE → POSITIVE | -1.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_29ea` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.74) | NEGATIVE (0.41) | POSITIVE → NEGATIVE | -33.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_f9e4` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.74) | POSITIVE (0.92) | POSITIVE → POSITIVE | +17.8 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_52ce`** [Misweighted / UNEXPECTED_CHANGE]: Model recognized linguistic operator 'not' (LIME: -0.2805, SHAP: -0.4140), but opposing sentiment features ('good' (+0.2484)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **`prb_1787`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 17.22 percentage points under meaning-preserving perturbation.
- **`prb_0e0c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c3fa`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_eb25`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_29ea`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_f9e4`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_52ce` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.85) | NEGATIVE (0.88) | POSITIVE → NEGATIVE | +3.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_1787` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.85) | NEGATIVE (0.82) | POSITIVE → NEGATIVE | -2.4 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_0e0c` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.85) | POSITIVE (0.96) | POSITIVE → POSITIVE | +11.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c3fa` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.85) | POSITIVE (0.90) | POSITIVE → POSITIVE | +4.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eb25` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.85) | POSITIVE (0.87) | POSITIVE → POSITIVE | +2.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_29ea` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.85) | NEGATIVE (0.95) | POSITIVE → NEGATIVE | +10.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_f9e4` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.85) | POSITIVE (1.00) | POSITIVE → POSITIVE | +15.3 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_52ce`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_1787`** [Misweighted / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_0e0c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c3fa`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_eb25`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_29ea`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_f9e4`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_52ce` | NEGATION_INSERTION | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.67) | NEUTRAL (0.49) | POSITIVE → NEUTRAL | -18.1 | NO | `UNEXPECTED_CHANGE` | **Misweighted** |
| `prb_1787` | DOUBLE_NEGATION | "Good product good quality..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.61) | POSITIVE → POSITIVE | -6.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0e0c` | INTENSITY | "Good product good quality..." → "extremely Good product go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.71) | POSITIVE → POSITIVE | +4.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c3fa` | INTENSITY | "Good product good quality..." → "somewhat Good product goo..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.68) | POSITIVE → POSITIVE | +0.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eb25` | SYNONYM_SUBSTITUTION | "Good product good quality..." → "Decent product good quali..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.62) | POSITIVE → POSITIVE | -4.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_29ea` | CONTRAST_NEGATIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.67) | NEGATIVE (0.47) | POSITIVE → NEGATIVE | -19.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_f9e4` | CONTRAST_POSITIVE_APPEND | "Good product good quality..." → "Good product good quality..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.67) | POSITIVE (0.86) | POSITIVE → POSITIVE | +19.2 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_52ce`** [Misweighted / UNEXPECTED_CHANGE]: Model recognized linguistic operator 'not' (LIME: -0.2929, SHAP: -0.3933), but opposing sentiment features ('good' (+0.2199)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **`prb_1787`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0e0c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c3fa`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_eb25`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_29ea`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_f9e4`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.