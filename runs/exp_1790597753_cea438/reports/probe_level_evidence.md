# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790597753_cea438`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_8088` | NEGATION_INSERTION | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | POSITIVE (0.98) | NEGATIVE → POSITIVE | -2.2 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_0b01` | DOUBLE_NEGATION | "The movie had excellent a..." → "It is not impossible that..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3b1c` | INTENSITY | "The movie had excellent a..." → "The movie had extremely e..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d794` | INTENSITY | "The movie had excellent a..." → "The movie had somewhat ex..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e115` | SYNONYM_SUBSTITUTION | "The movie had excellent a..." → "The film had excellent ac..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8883` | CONTRAST_NEGATIVE_APPEND | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | -0.8 | NO | `MISSING_FLIP` | **Blind** |
| `prb_0896` | CONTRAST_POSITIVE_APPEND | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | POSITIVE (1.00) | NEGATIVE → POSITIVE | -0.1 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_8088`** [Spurious / UNEXPECTED_FLIP]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **`prb_0b01`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_3b1c`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_d794`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_e115`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_8883`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_0896`** [Spurious / UNEXPECTED_FLIP]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_8088` | NEGATION_INSERTION | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | POSITIVE (0.45) | POSITIVE (0.96) | POSITIVE → POSITIVE | +50.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0b01` | DOUBLE_NEGATION | "The movie had excellent a..." → "It is not impossible that..." | `NEGATIVE (PRESERVE_POLARITY)` | POSITIVE (0.45) | NEGATIVE (0.50) | POSITIVE → NEGATIVE | +4.7 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_3b1c` | INTENSITY | "The movie had excellent a..." → "The movie had extremely e..." | `NEGATIVE (PRESERVE_POLARITY)` | POSITIVE (0.45) | POSITIVE (0.60) | POSITIVE → POSITIVE | +14.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d794` | INTENSITY | "The movie had excellent a..." → "The movie had somewhat ex..." | `NEGATIVE (PRESERVE_POLARITY)` | POSITIVE (0.45) | NEGATIVE (0.39) | POSITIVE → NEGATIVE | -6.8 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_e115` | SYNONYM_SUBSTITUTION | "The movie had excellent a..." → "The film had excellent ac..." | `NEGATIVE (PRESERVE_POLARITY)` | POSITIVE (0.45) | POSITIVE (0.46) | POSITIVE → POSITIVE | +0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8883` | CONTRAST_NEGATIVE_APPEND | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | POSITIVE (0.45) | NEGATIVE (0.72) | POSITIVE → NEGATIVE | +26.9 | YES | `EXPECTED_FLIP` | **None** |
| `prb_0896` | CONTRAST_POSITIVE_APPEND | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | POSITIVE (0.45) | POSITIVE (0.48) | POSITIVE → POSITIVE | +3.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_8088`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_0b01`** [Spurious / UNEXPECTED_FLIP]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **`prb_3b1c`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_d794`** [Misweighted / UNEXPECTED_FLIP]: Downtoner inverted polarity (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)).
- **`prb_e115`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_8883`** [None / EXPECTED_FLIP]: Model correctly flipped and reversed polarity (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under polarity-altering probe.
- **`prb_0896`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_8088` | NEGATION_INSERTION | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | POSITIVE (0.90) | NEGATIVE → POSITIVE | +26.8 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_0b01` | DOUBLE_NEGATION | "The movie had excellent a..." → "It is not impossible that..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.61) | NEGATIVE → NEGATIVE | -1.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3b1c` | INTENSITY | "The movie had excellent a..." → "The movie had extremely e..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.52) | NEGATIVE → NEGATIVE | -10.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d794` | INTENSITY | "The movie had excellent a..." → "The movie had somewhat ex..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.63) | NEGATIVE → NEGATIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e115` | SYNONYM_SUBSTITUTION | "The movie had excellent a..." → "The film had excellent ac..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.61) | NEGATIVE → NEGATIVE | -2.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8883` | CONTRAST_NEGATIVE_APPEND | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.63) | NEGATIVE → NEGATIVE | -0.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_0896` | CONTRAST_POSITIVE_APPEND | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.63) | NEGATIVE (0.48) | NEGATIVE → NEGATIVE | -15.0 | NO | `EXPECTED_PRESERVE` | **Misweighted** |

### Probe Rationales & Evidence Notes
- **`prb_8088`** [Spurious / UNEXPECTED_FLIP]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **`prb_0b01`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_3b1c`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_d794`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_e115`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_8883`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_0896`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 15.01 percentage points under meaning-preserving perturbation.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_8088` | NEGATION_INSERTION | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.94) | POSITIVE (0.57) | NEGATIVE → POSITIVE | -36.7 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_0b01` | DOUBLE_NEGATION | "The movie had excellent a..." → "It is not impossible that..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.94) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +6.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3b1c` | INTENSITY | "The movie had excellent a..." → "The movie had extremely e..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.94) | NEGATIVE (0.89) | NEGATIVE → NEGATIVE | -4.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d794` | INTENSITY | "The movie had excellent a..." → "The movie had somewhat ex..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.94) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | +0.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e115` | SYNONYM_SUBSTITUTION | "The movie had excellent a..." → "The film had excellent ac..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.94) | NEGATIVE (0.89) | NEGATIVE → NEGATIVE | -5.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8883` | CONTRAST_NEGATIVE_APPEND | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.94) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | +4.2 | NO | `MISSING_FLIP` | **Blind** |
| `prb_0896` | CONTRAST_POSITIVE_APPEND | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.94) | POSITIVE (0.62) | NEGATIVE → POSITIVE | -31.4 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_8088`** [Spurious / UNEXPECTED_FLIP]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **`prb_0b01`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_3b1c`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_d794`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_e115`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_8883`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_0896`** [Spurious / UNEXPECTED_FLIP]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_8088` | NEGATION_INSERTION | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +0.5 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_0b01` | DOUBLE_NEGATION | "The movie had excellent a..." → "It is not impossible that..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3b1c` | INTENSITY | "The movie had excellent a..." → "The movie had extremely e..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d794` | INTENSITY | "The movie had excellent a..." → "The movie had somewhat ex..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e115` | SYNONYM_SUBSTITUTION | "The movie had excellent a..." → "The film had excellent ac..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8883` | CONTRAST_NEGATIVE_APPEND | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +0.1 | NO | `MISSING_FLIP` | **Blind** |
| `prb_0896` | CONTRAST_POSITIVE_APPEND | "The movie had excellent a..." → "The movie had excellent a..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | POSITIVE (0.99) | NEGATIVE → POSITIVE | -0.2 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_8088`** [Spurious / UNEXPECTED_FLIP]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).
- **`prb_0b01`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_3b1c`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_d794`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_e115`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_8883`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_0896`** [Spurious / UNEXPECTED_FLIP]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)).