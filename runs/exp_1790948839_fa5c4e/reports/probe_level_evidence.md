# Probe-Level Behavioral Evidence: Flipkart1

**Experiment ID**: `exp_1790948839_fa5c4e`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c186` | NEGATION_PREFIX | "It's really a good and co..." → "It is not true that it's ..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.9 | YES | `EXPECTED_FLIP` | **None** |
| `prb_ba2f` | DOUBLE_NEGATION | "It's really a good and co..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0770` | INTENSITY | "It's really a good and co..." → "It's really a extremely g..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3292` | INTENSITY | "It's really a good and co..." → "It's really a somewhat go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7152` | SYNONYM_SUBSTITUTION | "It's really a good and co..." → "It's really a decent and ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_096a` | CONTRAST_NEGATIVE_APPEND | "It's really a good and co..." → "It's really a good and co..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_21e6` | CONTRAST_POSITIVE_APPEND | "It's really a good and co..." → "It's really a good and co..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_c186`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_ba2f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0770`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3292`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_7152`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_096a`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_21e6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c186` | NEGATION_PREFIX | "It's really a good and co..." → "It is not true that it's ..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.98) | POSITIVE → NEGATIVE | -2.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_ba2f` | DOUBLE_NEGATION | "It's really a good and co..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0770` | INTENSITY | "It's really a good and co..." → "It's really a extremely g..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3292` | INTENSITY | "It's really a good and co..." → "It's really a somewhat go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7152` | SYNONYM_SUBSTITUTION | "It's really a good and co..." → "It's really a decent and ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_096a` | CONTRAST_NEGATIVE_APPEND | "It's really a good and co..." → "It's really a good and co..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.58) | POSITIVE → POSITIVE | -41.7 | NO | `MISSING_FLIP` | **Blind** |
| `prb_21e6` | CONTRAST_POSITIVE_APPEND | "It's really a good and co..." → "It's really a good and co..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_c186`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_ba2f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0770`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3292`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_7152`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_096a`** [Blind / MISSING_FLIP]: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: -0.0258, SHAP: +0.0172 < 0.05).
- **`prb_21e6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c186` | NEGATION_PREFIX | "It's really a good and co..." → "It is not true that it's ..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.98) | NEGATIVE (0.64) | POSITIVE → NEGATIVE | -33.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_ba2f` | DOUBLE_NEGATION | "It's really a good and co..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.91) | POSITIVE → POSITIVE | -7.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0770` | INTENSITY | "It's really a good and co..." → "It's really a extremely g..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | +0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3292` | INTENSITY | "It's really a good and co..." → "It's really a somewhat go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.97) | POSITIVE → POSITIVE | -1.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7152` | SYNONYM_SUBSTITUTION | "It's really a good and co..." → "It's really a decent and ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.96) | POSITIVE → POSITIVE | -2.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_096a` | CONTRAST_NEGATIVE_APPEND | "It's really a good and co..." → "It's really a good and co..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.98) | NEGATIVE (0.66) | POSITIVE → NEGATIVE | -31.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_21e6` | CONTRAST_POSITIVE_APPEND | "It's really a good and co..." → "It's really a good and co..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | +0.4 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_c186`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_ba2f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0770`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3292`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_7152`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_096a`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_21e6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c186` | NEGATION_PREFIX | "It's really a good and co..." → "It is not true that it's ..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.78) | POSITIVE → NEGATIVE | -22.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_ba2f` | DOUBLE_NEGATION | "It's really a good and co..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -1.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0770` | INTENSITY | "It's really a good and co..." → "It's really a extremely g..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3292` | INTENSITY | "It's really a good and co..." → "It's really a somewhat go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7152` | SYNONYM_SUBSTITUTION | "It's really a good and co..." → "It's really a decent and ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_096a` | CONTRAST_NEGATIVE_APPEND | "It's really a good and co..." → "It's really a good and co..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.95) | POSITIVE → NEGATIVE | -4.8 | YES | `EXPECTED_FLIP` | **None** |
| `prb_21e6` | CONTRAST_POSITIVE_APPEND | "It's really a good and co..." → "It's really a good and co..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_c186`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_ba2f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0770`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3292`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_7152`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_096a`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_21e6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c186` | NEGATION_PREFIX | "It's really a good and co..." → "It is not true that it's ..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.98) | NEGATIVE (0.47) | POSITIVE → NEGATIVE | -50.9 | YES | `EXPECTED_FLIP` | **None** |
| `prb_ba2f` | DOUBLE_NEGATION | "It's really a good and co..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.94) | POSITIVE → POSITIVE | -4.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0770` | INTENSITY | "It's really a good and co..." → "It's really a extremely g..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3292` | INTENSITY | "It's really a good and co..." → "It's really a somewhat go..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.97) | POSITIVE → POSITIVE | -0.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7152` | SYNONYM_SUBSTITUTION | "It's really a good and co..." → "It's really a decent and ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.96) | POSITIVE → POSITIVE | -1.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_096a` | CONTRAST_NEGATIVE_APPEND | "It's really a good and co..." → "It's really a good and co..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.98) | NEGATIVE (0.45) | POSITIVE → NEGATIVE | -53.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_21e6` | CONTRAST_POSITIVE_APPEND | "It's really a good and co..." → "It's really a good and co..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_c186`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_ba2f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0770`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_3292`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_7152`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_096a`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_21e6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.