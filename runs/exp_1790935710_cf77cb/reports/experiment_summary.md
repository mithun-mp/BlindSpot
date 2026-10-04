# BlindSpot Research Audit Report: Multimodel Robustness Audit

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790935710_cf77cb`
- **Run Plan Created**: `1790935712.1947005`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790935704_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 1127.35s
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
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 3 (42.9%) | 0/2 (28.6%) | 4/5 (80.0%) | 85.7% | 0.1275 | -2.4 pp |
| `albert-base-v2-SST-2` | 7 | 2 (28.6%) | 0/2 (28.6%) | 5/5 (100.0%) | 100.0% | 0.0460 | -0.8 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 1 (14.3%) | 0/0 (0.0%) | 6/7 (85.7%) | 57.1% | 0.3411 | -5.7 pp |
| `bert-base-uncased-SST-2` | 7 | 3 (42.9%) | 0/2 (28.6%) | 4/5 (80.0%) | 85.7% | 0.1768 | -6.4 pp |
| `twitter-roberta-base-sentiment` | 7 | 3 (42.9%) | 0/0 (0.0%) | 4/7 (57.1%) | 57.1% | 0.3781 | -6.3 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 0 | 0 | 1 | 0 | 6 |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 7 |
| `twitter-roberta-base-sentiment-latest` | 0 | 0 | 2 | 1 | 4 |
| `bert-base-uncased-SST-2` | 0 | 0 | 1 | 0 | 6 |
| `twitter-roberta-base-sentiment` | 0 | 2 | 0 | 1 | 4 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 51.43%

### Pairwise Concordance Matrix
| Model | `Twitter-RoBERTa (Base)` | `Twitter-RoBERTa (Latest)` | `DistilBERT SST-2` | `ALBERT SST-2` | `BERT SST-2` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Twitter-RoBERTa (Base)` | 100.0% | 71.4% | 42.9% | 42.9% | 42.9% |
| `Twitter-RoBERTa (Latest)` | 71.4% | 100.0% | 14.3% | 14.3% | 14.3% |
| `DistilBERT SST-2` | 42.9% | 14.3% | 100.0% | 85.7% | 100.0% |
| `ALBERT SST-2` | 42.9% | 14.3% | 85.7% | 100.0% | 85.7% |
| `BERT SST-2` | 42.9% | 14.3% | 100.0% | 85.7% | 100.0% |

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