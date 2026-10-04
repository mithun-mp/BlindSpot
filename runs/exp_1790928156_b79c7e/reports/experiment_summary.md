# BlindSpot Research Audit Report: sun

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790928156_b79c7e`
- **Run Plan Created**: `1790928157.8178988`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790928142_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 653.54s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "sun rises in the east and sets in the west"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "sun rises in the east and sets in the we..." | `LITERAL` | **POSITIVE** | 0.9987 (99.9%) |
| `albert-base-v2-SST-2` | "sun rises in the east and sets in the we..." | `LITERAL` | **POSITIVE** | 0.9623 (96.2%) |
| `twitter-roberta-base-sentiment-latest` | "sun rises in the east and sets in the we..." | `LITERAL` | **NEUTRAL** | 0.9119 (91.2%) |
| `bert-base-uncased-SST-2` | "sun rises in the east and sets in the we..." | `LITERAL` | **POSITIVE** | 0.9952 (99.5%) |
| `twitter-roberta-base-sentiment` | "sun rises in the east and sets in the we..." | `LITERAL` | **NEUTRAL** | 0.8554 (85.5%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 2 (28.6%) | 0/0 (0.0%) | 5/7 (71.4%) | 0.0% | 0.9951 | -0.4 pp |
| `albert-base-v2-SST-2` | 7 | 2 (28.6%) | 0/0 (0.0%) | 5/7 (71.4%) | 0.0% | 0.9610 | -0.1 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 1 (14.3%) | 0/0 (0.0%) | 6/7 (85.7%) | 42.9% | 0.4656 | -7.5 pp |
| `bert-base-uncased-SST-2` | 7 | 2 (28.6%) | 0/0 (0.0%) | 5/7 (71.4%) | 0.0% | 0.9483 | -4.7 pp |
| `twitter-roberta-base-sentiment` | 7 | 3 (42.9%) | 0/0 (0.0%) | 4/7 (57.1%) | 42.9% | 0.4491 | -7.9 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 0 | 0 | 1 | 6 | 0 |
| `albert-base-v2-SST-2` | 0 | 0 | 1 | 6 | 0 |
| `twitter-roberta-base-sentiment-latest` | 0 | 0 | 2 | 2 | 3 |
| `bert-base-uncased-SST-2` | 0 | 0 | 1 | 6 | 0 |
| `twitter-roberta-base-sentiment` | 0 | 2 | 0 | 2 | 3 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 54.29%

### Pairwise Concordance Matrix
| Model | `Twitter-RoBERTa (Base)` | `Twitter-RoBERTa (Latest)` | `DistilBERT SST-2` | `ALBERT SST-2` | `BERT SST-2` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Twitter-RoBERTa (Base)` | 100.0% | 71.4% | 42.9% | 42.9% | 42.9% |
| `Twitter-RoBERTa (Latest)` | 71.4% | 100.0% | 14.3% | 14.3% | 14.3% |
| `DistilBERT SST-2` | 42.9% | 14.3% | 100.0% | 100.0% | 100.0% |
| `ALBERT SST-2` | 42.9% | 14.3% | 100.0% | 100.0% | 100.0% |
| `BERT SST-2` | 42.9% | 14.3% | 100.0% | 100.0% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |

## 8. Semantic Reference Methodology & Ground-Truth Alignment
1. **Canonical Semantic Label Space**: Ground-truth polarity is strictly confined to `POSITIVE`, `NEGATIVE`, and `NEUTRAL`. Non-canonical sentiment categories (such as `MIXED`, `AMBIGUOUS`, `SARCASTIC`) are rejected.
2. **Google Gemini Role**: Gemini operates exclusively as an external semantic annotator/verification layer for baseline and probe sentences. It is **never** a benchmark model, does not forecast model failures, and is strictly prohibited from generating the failure taxonomy.
3. **Human Verification & Override**: Every semantic reference can be verified and overridden by researchers (`[Accept]` / `[Change]`). Frozen semantic references are strictly immutable during model evaluation.
4. **Binary vs. Multiclass Alignment**: Binary models (e.g. 2-class SST-2) natively output `NEGATIVE` and `POSITIVE`. When semantic reference is `NEUTRAL`, binary models' forced polarity is recorded as `NOT_DIRECTLY_REPRESENTABLE` (`BINARY_FORCED_POLARITY`), preserving empirical truth rather than falsely modifying the reference.
5. **Independence of Model Outputs & Rule-Based Taxonomy**: Model predictions remain 100% empirical forward-pass outputs. The failure taxonomy (`Blind`, `Spurious`, `Misweighted`, `Undetermined`) is derived purely by deterministic rule-based behavioral analysis, completely independent of Gemini.