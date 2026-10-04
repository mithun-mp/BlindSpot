# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790967650_e306ae`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7c3d` | NEGATION_INSERTION | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_20c5` | DOUBLE_NEGATION | "Excellent shoes at low pr..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5695` | INTENSITY | "Excellent shoes at low pr..." → "extremely Excellent shoes..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1a00` | INTENSITY | "Excellent shoes at low pr..." → "somewhat Excellent shoes ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e03d` | SYNONYM_SUBSTITUTION | "Excellent shoes at low pr..." → "Fantabulous shoes at low ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5675` | CONTRAST_NEGATIVE_APPEND | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.95) | POSITIVE → NEGATIVE | -5.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_d604` | CONTRAST_POSITIVE_APPEND | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_7c3d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_20c5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5695`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_1a00`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_e03d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5675`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_d604`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7c3d` | NEGATION_INSERTION | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.85) | POSITIVE → POSITIVE | -14.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_20c5` | DOUBLE_NEGATION | "Excellent shoes at low pr..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.98) | POSITIVE → POSITIVE | -1.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5695` | INTENSITY | "Excellent shoes at low pr..." → "extremely Excellent shoes..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1a00` | INTENSITY | "Excellent shoes at low pr..." → "somewhat Excellent shoes ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e03d` | SYNONYM_SUBSTITUTION | "Excellent shoes at low pr..." → "Fantabulous shoes at low ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -1.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5675` | CONTRAST_NEGATIVE_APPEND | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.59) | POSITIVE → POSITIVE | -40.5 | NO | `MISSING_FLIP` | **Misweighted** |
| `prb_d604` | CONTRAST_POSITIVE_APPEND | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_7c3d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_20c5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5695`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_1a00`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_e03d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5675`** [Misweighted / MISSING_FLIP]: Model recognized linguistic operator 'however' (LIME: +0.0000, SHAP: -0.0608), but opposing sentiment features ('inferior' (-0.4539)) outweighed the operator, preventing expected polarity reversal. Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity.
- **`prb_d604`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7c3d` | NEGATION_INSERTION | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.96) | POSITIVE → POSITIVE | -1.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_20c5` | DOUBLE_NEGATION | "Excellent shoes at low pr..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.97) | POSITIVE → POSITIVE | -1.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5695` | INTENSITY | "Excellent shoes at low pr..." → "extremely Excellent shoes..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1a00` | INTENSITY | "Excellent shoes at low pr..." → "somewhat Excellent shoes ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e03d` | SYNONYM_SUBSTITUTION | "Excellent shoes at low pr..." → "Fantabulous shoes at low ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5675` | CONTRAST_NEGATIVE_APPEND | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.90) | POSITIVE → POSITIVE | -8.5 | NO | `MISSING_FLIP` | **Blind** |
| `prb_d604` | CONTRAST_POSITIVE_APPEND | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_7c3d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_20c5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5695`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_1a00`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_e03d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5675`** [Blind / MISSING_FLIP]: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: -0.0193 < 0.05).
- **`prb_d604`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7c3d` | NEGATION_INSERTION | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.94) | POSITIVE → POSITIVE | -5.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_20c5` | DOUBLE_NEGATION | "Excellent shoes at low pr..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5695` | INTENSITY | "Excellent shoes at low pr..." → "extremely Excellent shoes..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1a00` | INTENSITY | "Excellent shoes at low pr..." → "somewhat Excellent shoes ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e03d` | SYNONYM_SUBSTITUTION | "Excellent shoes at low pr..." → "Fantabulous shoes at low ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -1.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5675` | CONTRAST_NEGATIVE_APPEND | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.94) | POSITIVE → NEGATIVE | -6.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_d604` | CONTRAST_POSITIVE_APPEND | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_7c3d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_20c5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5695`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_1a00`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_e03d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5675`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_d604`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7c3d` | NEGATION_INSERTION | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.96) | POSITIVE → POSITIVE | -1.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_20c5` | DOUBLE_NEGATION | "Excellent shoes at low pr..." → "It is not impossible that..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5695` | INTENSITY | "Excellent shoes at low pr..." → "extremely Excellent shoes..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | +0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1a00` | INTENSITY | "Excellent shoes at low pr..." → "somewhat Excellent shoes ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e03d` | SYNONYM_SUBSTITUTION | "Excellent shoes at low pr..." → "Fantabulous shoes at low ..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.97) | POSITIVE → POSITIVE | -0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5675` | CONTRAST_NEGATIVE_APPEND | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `NEGATIVE (REVERSE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.85) | POSITIVE → POSITIVE | -12.8 | NO | `MISSING_FLIP` | **Blind** |
| `prb_d604` | CONTRAST_POSITIVE_APPEND | "Excellent shoes at low pr..." → "Excellent shoes at low pr..." | `POSITIVE (PRESERVE_POLARITY)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_7c3d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_20c5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5695`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_1a00`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_e03d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_5675`** [Blind / MISSING_FLIP]: Model failed to produce expected polarity reversal and showed negligible attribution to linguistic operator 'however' (LIME: +0.0000, SHAP: -0.0116 < 0.05).
- **`prb_d604`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.