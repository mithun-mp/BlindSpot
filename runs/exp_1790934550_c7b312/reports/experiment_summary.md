# BlindSpot Research Audit Report: movieboring

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790934550_c7b312`
- **Run Plan Created**: `1790934552.1091146`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790934530_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 234.34s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "the movie was very boring but the ending was good"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "the movie was very boring but the ending..." | `LITERAL` | **POSITIVE** | 0.9988 (99.9%) |
| `albert-base-v2-SST-2` | "the movie was very boring but the ending..." | `LITERAL` | **POSITIVE** | 0.8785 (87.8%) |
| `twitter-roberta-base-sentiment-latest` | "the movie was very boring but the ending..." | `LITERAL` | **POSITIVE** | 0.4555 (45.6%) |
| `bert-base-uncased-SST-2` | "the movie was very boring but the ending..." | `LITERAL` | **POSITIVE** | 0.9766 (97.7%) |
| `twitter-roberta-base-sentiment` | "the movie was very boring but the ending..." | `LITERAL` | **POSITIVE** | 0.3553 (35.5%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 1 (14.3%) | 0/1 (14.3%) | 6/6 (100.0%) | 100.0% | 0.0033 | -0.2 pp |
| `albert-base-v2-SST-2` | 7 | 1 (14.3%) | 0/1 (14.3%) | 6/6 (100.0%) | 100.0% | 0.1072 | +1.4 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 2 (28.6%) | 0/1 (14.3%) | 5/6 (83.3%) | 71.4% | 0.3441 | +20.9 pp |
| `bert-base-uncased-SST-2` | 7 | 1 (14.3%) | 0/1 (14.3%) | 6/6 (100.0%) | 100.0% | 0.0170 | +0.6 pp |
| `twitter-roberta-base-sentiment` | 7 | 2 (28.6%) | 0/1 (14.3%) | 5/6 (83.3%) | 71.4% | 0.2152 | +24.3 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 0 | 0 | 0 | 0 | 7 |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 7 |
| `twitter-roberta-base-sentiment-latest` | 0 | 0 | 2 | 0 | 5 |
| `bert-base-uncased-SST-2` | 0 | 0 | 0 | 0 | 7 |
| `twitter-roberta-base-sentiment` | 0 | 0 | 2 | 0 | 5 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 85.71%

### Pairwise Concordance Matrix
| Model | `Twitter-RoBERTa (Base)` | `Twitter-RoBERTa (Latest)` | `DistilBERT SST-2` | `ALBERT SST-2` | `BERT SST-2` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Twitter-RoBERTa (Base)` | 100.0% | 85.7% | 71.4% | 71.4% | 71.4% |
| `Twitter-RoBERTa (Latest)` | 85.7% | 100.0% | 85.7% | 85.7% | 85.7% |
| `DistilBERT SST-2` | 71.4% | 85.7% | 100.0% | 100.0% | 100.0% |
| `ALBERT SST-2` | 71.4% | 85.7% | 100.0% | 100.0% | 100.0% |
| `BERT SST-2` | 71.4% | 85.7% | 100.0% | 100.0% | 100.0% |

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