# BlindSpot Research Audit Report: M001

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790587930_42925e`
- **Run Plan Created**: `1790587931.285006`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`, `textattack/bert-base-uncased-SST-2`, `textattack/albert-base-v2-SST-2`
- **Probe Set ID / Version**: `pset_1790587791_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 8
- **Execution Runtime**: 364.19s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "The movie was great and the acting was top notch."

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "The movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9999 (100.0%) |
| `twitter-roberta-base-sentiment-latest` | "The movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9870 (98.7%) |
| `twitter-roberta-base-sentiment` | "The movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9862 (98.6%) |
| `bert-base-uncased-SST-2` | "The movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9996 (100.0%) |
| `albert-base-v2-SST-2` | "The movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9957 (99.6%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 8 | 1 (12.5%) | 0/2 (25.0%) | 6/6 (100.0%) | 100.0% | 0.0028 | -0.3 pp |
| `twitter-roberta-base-sentiment-latest` | 8 | 1 (12.5%) | 0/2 (25.0%) | 6/6 (100.0%) | 87.5% | 0.1170 | -7.3 pp |
| `twitter-roberta-base-sentiment` | 8 | 1 (12.5%) | 0/2 (25.0%) | 6/6 (100.0%) | 87.5% | 0.0796 | -8.7 pp |
| `bert-base-uncased-SST-2` | 8 | 2 (25.0%) | 0/2 (25.0%) | 6/6 (100.0%) | 100.0% | 0.0504 | -5.0 pp |
| `albert-base-v2-SST-2` | 8 | 2 (25.0%) | 0/2 (25.0%) | 6/6 (100.0%) | 100.0% | 0.0118 | -0.8 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 0 | 0 | 0 | 0 | 8 |
| `twitter-roberta-base-sentiment-latest` | 1 | 0 | 0 | 0 | 7 |
| `twitter-roberta-base-sentiment` | 1 | 0 | 0 | 0 | 7 |
| `bert-base-uncased-SST-2` | 0 | 0 | 0 | 0 | 8 |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 8 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 87.50%

### Pairwise Concordance Matrix
| Model | `Twitter-RoBERTa (Base)` | `Twitter-RoBERTa (Latest)` | `DistilBERT SST-2` | `ALBERT SST-2` | `BERT SST-2` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Twitter-RoBERTa (Base)` | 100.0% | 100.0% | 75.0% | 87.5% | 87.5% |
| `Twitter-RoBERTa (Latest)` | 100.0% | 100.0% | 75.0% | 87.5% | 87.5% |
| `DistilBERT SST-2` | 75.0% | 75.0% | 100.0% | 87.5% | 87.5% |
| `ALBERT SST-2` | 87.5% | 87.5% | 87.5% | 100.0% | 100.0% |
| `BERT SST-2` | 87.5% | 87.5% | 87.5% | 100.0% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 8 | 8 | 8 | 8 | 8 | 8 | 8 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 8 | 8 | 8 | 8 | 8 | 8 | 8 | **PASS** |
| `twitter-roberta-base-sentiment` | 8 | 8 | 8 | 8 | 8 | 8 | 8 | **PASS** |
| `bert-base-uncased-SST-2` | 8 | 8 | 8 | 8 | 8 | 8 | 8 | **PASS** |
| `albert-base-v2-SST-2` | 8 | 8 | 8 | 8 | 8 | 8 | 8 | **PASS** |

## 8. Semantic Reference Methodology & Ground-Truth Alignment
1. **Canonical Semantic Label Space**: Ground-truth polarity is strictly confined to `POSITIVE`, `NEGATIVE`, and `NEUTRAL`. Non-canonical sentiment categories (such as `MIXED`, `AMBIGUOUS`, `SARCASTIC`) are rejected.
2. **Google Gemini Role**: Gemini operates exclusively as an external semantic annotator/verification layer for baseline and probe sentences. It is **never** a benchmark model, does not forecast model failures, and is strictly prohibited from generating the failure taxonomy.
3. **Human Verification & Override**: Every semantic reference can be verified and overridden by researchers (`[Accept]` / `[Change]`). Frozen semantic references are strictly immutable during model evaluation.
4. **Binary vs. Multiclass Alignment**: Binary models (e.g. 2-class SST-2) natively output `NEGATIVE` and `POSITIVE`. When semantic reference is `NEUTRAL`, binary models' forced polarity is recorded as `NOT_DIRECTLY_REPRESENTABLE` (`BINARY_FORCED_POLARITY`), preserving empirical truth rather than falsely modifying the reference.
5. **Independence of Model Outputs & Rule-Based Taxonomy**: Model predictions remain 100% empirical forward-pass outputs. The failure taxonomy (`Blind`, `Spurious`, `Misweighted`, `Undetermined`) is derived purely by deterministic rule-based behavioral analysis, completely independent of Gemini.