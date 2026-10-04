# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790876807_68cc48`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_ab20` | NEGATION_PREFIX | "sun rises in the east and..." → "It is not true that sun r..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.7 | YES | `UNDETERMINED` | **Misweighted** |
| `prb_3dd0` | DOUBLE_NEGATION | "sun rises in the east and..." → "It is not impossible that..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.2 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_3257` | INTENSITY | "sun rises in the east and..." → "sun rises extremely in th..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_8a01` | INTENSITY | "sun rises in the east and..." → "sun rises somewhat in the..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_eb8f` | SYNONYM_SUBSTITUTION | "sun rises in the east and..." → "sunlight rises in the eas..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_56f8` | CONTRAST_NEGATIVE_APPEND | "sun rises in the east and..." → "sun rises in the east and..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (1.00) | NEGATIVE (0.98) | POSITIVE → NEGATIVE | -1.7 | YES | `UNDETERMINED` | **Undetermined** |
| `prb_85c3` | CONTRAST_POSITIVE_APPEND | "sun rises in the east and..." → "sun rises in the east and..." | `POSITIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `UNDETERMINED` | **Undetermined** |

### Probe Rationales & Evidence Notes
- **`prb_ab20`** [Misweighted / UNDETERMINED]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_3dd0`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_3257`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_8a01`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_eb8f`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_56f8`** [Undetermined / UNDETERMINED]: Indeterminate behavioral transition.
- **`prb_85c3`** [Undetermined / UNDETERMINED]: Indeterminate behavioral transition.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_ab20` | NEGATION_PREFIX | "sun rises in the east and..." → "It is not true that sun r..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (0.96) | NEGATIVE (0.90) | POSITIVE → NEGATIVE | -5.8 | YES | `UNDETERMINED` | **Misweighted** |
| `prb_3dd0` | DOUBLE_NEGATION | "sun rises in the east and..." → "It is not impossible that..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (0.96) | POSITIVE (0.95) | POSITIVE → POSITIVE | -0.9 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_3257` | INTENSITY | "sun rises in the east and..." → "sun rises extremely in th..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (0.96) | POSITIVE (0.97) | POSITIVE → POSITIVE | +1.1 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_8a01` | INTENSITY | "sun rises in the east and..." → "sun rises somewhat in the..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (0.96) | POSITIVE (0.95) | POSITIVE → POSITIVE | -1.0 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_eb8f` | SYNONYM_SUBSTITUTION | "sun rises in the east and..." → "sunlight rises in the eas..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (0.96) | POSITIVE (0.97) | POSITIVE → POSITIVE | +0.4 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_56f8` | CONTRAST_NEGATIVE_APPEND | "sun rises in the east and..." → "sun rises in the east and..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (0.96) | NEGATIVE (0.96) | POSITIVE → NEGATIVE | -0.4 | YES | `UNDETERMINED` | **Undetermined** |
| `prb_85c3` | CONTRAST_POSITIVE_APPEND | "sun rises in the east and..." → "sun rises in the east and..." | `POSITIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (0.96) | POSITIVE (1.00) | POSITIVE → POSITIVE | +3.7 | NO | `UNDETERMINED` | **Undetermined** |

### Probe Rationales & Evidence Notes
- **`prb_ab20`** [Misweighted / UNDETERMINED]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_3dd0`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_3257`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_8a01`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_eb8f`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_56f8`** [Undetermined / UNDETERMINED]: Indeterminate behavioral transition.
- **`prb_85c3`** [Undetermined / UNDETERMINED]: Indeterminate behavioral transition.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_ab20` | NEGATION_PREFIX | "sun rises in the east and..." → "It is not true that sun r..." | `NEUTRAL (PRESERVE_POLARITY)` | NEUTRAL (0.91) | NEUTRAL (0.71) | NEUTRAL → NEUTRAL | -20.1 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_3dd0` | DOUBLE_NEGATION | "sun rises in the east and..." → "It is not impossible that..." | `NEUTRAL (PRESERVE_POLARITY)` | NEUTRAL (0.91) | NEUTRAL (0.71) | NEUTRAL → NEUTRAL | -19.8 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_3257` | INTENSITY | "sun rises in the east and..." → "sun rises extremely in th..." | `NEUTRAL (PRESERVE_POLARITY)` | NEUTRAL (0.91) | NEUTRAL (0.92) | NEUTRAL → NEUTRAL | +1.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8a01` | INTENSITY | "sun rises in the east and..." → "sun rises somewhat in the..." | `NEUTRAL (PRESERVE_POLARITY)` | NEUTRAL (0.91) | NEUTRAL (0.90) | NEUTRAL → NEUTRAL | -1.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eb8f` | SYNONYM_SUBSTITUTION | "sun rises in the east and..." → "sunlight rises in the eas..." | `NEUTRAL (PRESERVE_POLARITY)` | NEUTRAL (0.91) | NEUTRAL (0.92) | NEUTRAL → NEUTRAL | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_56f8` | CONTRAST_NEGATIVE_APPEND | "sun rises in the east and..." → "sun rises in the east and..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | NEUTRAL (0.91) | NEUTRAL (0.93) | NEUTRAL → NEUTRAL | +2.3 | NO | `MISSING_FLIP` | **Undetermined** |
| `prb_85c3` | CONTRAST_POSITIVE_APPEND | "sun rises in the east and..." → "sun rises in the east and..." | `POSITIVE (SHIFT_FROM_NEUTRAL)` | NEUTRAL (0.91) | POSITIVE (0.90) | NEUTRAL → POSITIVE | -1.3 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_ab20`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 20.11 percentage points under meaning-preserving perturbation.
- **`prb_3dd0`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 19.76 percentage points under meaning-preserving perturbation.
- **`prb_3257`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_8a01`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_eb8f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_56f8`** [Undetermined / MISSING_FLIP]: Indeterminate behavioral transition.
- **`prb_85c3`** [None / EXPECTED_FLIP]: Model correctly shifted from NEUTRAL to POSITIVE (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_ab20` | NEGATION_PREFIX | "sun rises in the east and..." → "It is not true that sun r..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (1.00) | NEGATIVE (0.72) | POSITIVE → NEGATIVE | -27.1 | YES | `UNDETERMINED` | **Misweighted** |
| `prb_3dd0` | DOUBLE_NEGATION | "sun rises in the east and..." → "It is not impossible that..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.97) | POSITIVE → POSITIVE | -2.1 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_3257` | INTENSITY | "sun rises in the east and..." → "sun rises extremely in th..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.2 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_8a01` | INTENSITY | "sun rises in the east and..." → "sun rises somewhat in the..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (0.98) | POSITIVE → POSITIVE | -1.3 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_eb8f` | SYNONYM_SUBSTITUTION | "sun rises in the east and..." → "sunlight rises in the eas..." | `NEUTRAL (PRESERVE_POLARITY)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.3 | NO | `UNDETERMINED` | **Undetermined** |
| `prb_56f8` | CONTRAST_NEGATIVE_APPEND | "sun rises in the east and..." → "sun rises in the east and..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (1.00) | NEGATIVE (0.96) | POSITIVE → NEGATIVE | -3.3 | YES | `UNDETERMINED` | **Undetermined** |
| `prb_85c3` | CONTRAST_POSITIVE_APPEND | "sun rises in the east and..." → "sun rises in the east and..." | `POSITIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.4 | NO | `UNDETERMINED` | **Undetermined** |

### Probe Rationales & Evidence Notes
- **`prb_ab20`** [Misweighted / UNDETERMINED]: Model unexpectedly flipped prediction under meaning-preserving perturbation due to disproportionate feature weight shift on semantic tokens.
- **`prb_3dd0`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_3257`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_8a01`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_eb8f`** [Undetermined / UNDETERMINED]: Undetermined probe expectation contract.
- **`prb_56f8`** [Undetermined / UNDETERMINED]: Indeterminate behavioral transition.
- **`prb_85c3`** [Undetermined / UNDETERMINED]: Indeterminate behavioral transition.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_ab20` | NEGATION_PREFIX | "sun rises in the east and..." → "It is not true that sun r..." | `NEUTRAL (PRESERVE_POLARITY)` | NEUTRAL (0.86) | NEGATIVE (0.55) | NEUTRAL → NEGATIVE | -30.3 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_3dd0` | DOUBLE_NEGATION | "sun rises in the east and..." → "It is not impossible that..." | `NEUTRAL (PRESERVE_POLARITY)` | NEUTRAL (0.86) | POSITIVE (0.76) | NEUTRAL → POSITIVE | -9.4 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_3257` | INTENSITY | "sun rises in the east and..." → "sun rises extremely in th..." | `NEUTRAL (PRESERVE_POLARITY)` | NEUTRAL (0.86) | NEUTRAL (0.85) | NEUTRAL → NEUTRAL | -0.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8a01` | INTENSITY | "sun rises in the east and..." → "sun rises somewhat in the..." | `NEUTRAL (PRESERVE_POLARITY)` | NEUTRAL (0.86) | NEUTRAL (0.88) | NEUTRAL → NEUTRAL | +2.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eb8f` | SYNONYM_SUBSTITUTION | "sun rises in the east and..." → "sunlight rises in the eas..." | `NEUTRAL (PRESERVE_POLARITY)` | NEUTRAL (0.86) | NEUTRAL (0.84) | NEUTRAL → NEUTRAL | -1.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_56f8` | CONTRAST_NEGATIVE_APPEND | "sun rises in the east and..." → "sun rises in the east and..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | NEUTRAL (0.86) | NEUTRAL (0.78) | NEUTRAL → NEUTRAL | -7.4 | NO | `MISSING_FLIP` | **Undetermined** |
| `prb_85c3` | CONTRAST_POSITIVE_APPEND | "sun rises in the east and..." → "sun rises in the east and..." | `POSITIVE (SHIFT_FROM_NEUTRAL)` | NEUTRAL (0.86) | POSITIVE (0.92) | NEUTRAL → POSITIVE | +6.9 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_ab20`** [Spurious / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 44.2%, top token: 'true') rather than semantic content.
- **`prb_3dd0`** [Spurious / UNEXPECTED_CHANGE]: Model unexpectedly flipped prediction under meaning-preserving perturbation, driven primarily by irrelevant/background features (background attribution ratio: 42.0%, top token: 'impossible') rather than semantic content.
- **`prb_3257`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_8a01`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_eb8f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_56f8`** [Undetermined / MISSING_FLIP]: Indeterminate behavioral transition.
- **`prb_85c3`** [None / EXPECTED_FLIP]: Model correctly shifted from NEUTRAL to POSITIVE (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).