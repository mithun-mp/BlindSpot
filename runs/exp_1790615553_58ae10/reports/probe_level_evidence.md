# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790615553_58ae10`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_b97b` | NEGATION_INSERTION | "The new security system i..." → "The new security system i..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | +0.0 | YES | `EXPECTED_FLIP` | **None** |
| `prb_19d2` | DOUBLE_NEGATION | "The new security system i..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -1.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_32ac` | INTENSITY | "The new security system i..." → "The new extremely securit..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f64d` | INTENSITY | "The new security system i..." → "The new somewhat security..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_6e32` | SYNONYM_SUBSTITUTION | "The new security system i..." → "The newfangled security s..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_01db` | CONTRAST_NEGATIVE_APPEND | "The new security system i..." → "The new security system i..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -1.2 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_b912` | CONTRAST_POSITIVE_APPEND | "The new security system i..." → "The new security system i..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_b97b`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_19d2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_32ac`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_f64d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_6e32`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_01db`** [Spurious / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction ('POSITIVE -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **`prb_b912`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_b97b` | NEGATION_INSERTION | "The new security system i..." → "The new security system i..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.89) | NEGATIVE (0.91) | POSITIVE → NEGATIVE | +2.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_19d2` | DOUBLE_NEGATION | "The new security system i..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.89) | POSITIVE (0.86) | POSITIVE → POSITIVE | -3.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_32ac` | INTENSITY | "The new security system i..." → "The new extremely securit..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.89) | POSITIVE (0.89) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f64d` | INTENSITY | "The new security system i..." → "The new somewhat security..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.89) | POSITIVE (0.86) | POSITIVE → POSITIVE | -3.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_6e32` | SYNONYM_SUBSTITUTION | "The new security system i..." → "The newfangled security s..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.89) | POSITIVE (0.89) | POSITIVE → POSITIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_01db` | CONTRAST_NEGATIVE_APPEND | "The new security system i..." → "The new security system i..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.89) | POSITIVE (0.78) | POSITIVE → POSITIVE | -10.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b912` | CONTRAST_POSITIVE_APPEND | "The new security system i..." → "The new security system i..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.89) | POSITIVE (0.91) | POSITIVE → POSITIVE | +2.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_b97b`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_19d2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_32ac`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_f64d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_6e32`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_01db`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_b912`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_b97b` | NEGATION_INSERTION | "The new security system i..." → "The new security system i..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.77) | NEGATIVE (0.89) | POSITIVE → NEGATIVE | +12.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_19d2` | DOUBLE_NEGATION | "The new security system i..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.77) | POSITIVE (0.70) | POSITIVE → POSITIVE | -7.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_32ac` | INTENSITY | "The new security system i..." → "The new extremely securit..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.77) | POSITIVE (0.77) | POSITIVE → POSITIVE | +0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f64d` | INTENSITY | "The new security system i..." → "The new somewhat security..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.77) | POSITIVE (0.58) | POSITIVE → POSITIVE | -18.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_6e32` | SYNONYM_SUBSTITUTION | "The new security system i..." → "The newfangled security s..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.77) | POSITIVE (0.77) | POSITIVE → POSITIVE | +0.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_01db` | CONTRAST_NEGATIVE_APPEND | "The new security system i..." → "The new security system i..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.77) | POSITIVE (0.52) | POSITIVE → POSITIVE | -24.8 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_b912` | CONTRAST_POSITIVE_APPEND | "The new security system i..." → "The new security system i..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.77) | POSITIVE (0.81) | POSITIVE → POSITIVE | +4.2 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_b97b`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_19d2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_32ac`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_f64d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_6e32`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_01db`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 24.81 percentage points under meaning-preserving perturbation.
- **`prb_b912`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_b97b` | NEGATION_INSERTION | "The new security system i..." → "The new security system i..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | -0.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_19d2` | DOUBLE_NEGATION | "The new security system i..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.94) | POSITIVE → POSITIVE | -5.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_32ac` | INTENSITY | "The new security system i..." → "The new extremely securit..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f64d` | INTENSITY | "The new security system i..." → "The new somewhat security..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_6e32` | SYNONYM_SUBSTITUTION | "The new security system i..." → "The newfangled security s..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_01db` | CONTRAST_NEGATIVE_APPEND | "The new security system i..." → "The new security system i..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.95) | POSITIVE → NEGATIVE | -4.4 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_b912` | CONTRAST_POSITIVE_APPEND | "The new security system i..." → "The new security system i..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_b97b`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_19d2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_32ac`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_f64d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_6e32`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_01db`** [Spurious / UNEXPECTED_FLIP]: Model unexpectedly flipped prediction ('POSITIVE -> NEGATIVE') under meaning-preserving perturbation, indicating spurious sensitivity.
- **`prb_b912`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_b97b` | NEGATION_INSERTION | "The new security system i..." → "The new security system i..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.99) | NEGATIVE (0.89) | POSITIVE → NEGATIVE | -9.7 | YES | `EXPECTED_FLIP` | **None** |
| `prb_19d2` | DOUBLE_NEGATION | "The new security system i..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.96) | POSITIVE → POSITIVE | -2.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_32ac` | INTENSITY | "The new security system i..." → "The new extremely securit..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f64d` | INTENSITY | "The new security system i..." → "The new somewhat security..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_6e32` | SYNONYM_SUBSTITUTION | "The new security system i..." → "The newfangled security s..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_01db` | CONTRAST_NEGATIVE_APPEND | "The new security system i..." → "The new security system i..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (0.52) | POSITIVE → POSITIVE | -46.9 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_b912` | CONTRAST_POSITIVE_APPEND | "The new security system i..." → "The new security system i..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +1.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_b97b`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_19d2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_32ac`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_f64d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_6e32`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_01db`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 46.94 percentage points under meaning-preserving perturbation.
- **`prb_b912`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.