# BlindSpot Research Audit Report: Multimodel Robustness Audit

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790615553_58ae10`
- **Run Plan Created**: `1790615554.9032447`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `cardiffnlp/twitter-roberta-base-sentiment`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `textattack/bert-base-uncased-SST-2`, `textattack/albert-base-v2-SST-2`
- **Probe Set ID / Version**: `pset_1790615533_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 608.34s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "The new security system is extremely reliable and protects users from dangerous attacks"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "The new security system is extremely rel..." | `LITERAL` | **POSITIVE** | 0.9988 (99.9%) |
| `twitter-roberta-base-sentiment` | "The new security system is extremely rel..." | `LITERAL` | **POSITIVE** | 0.8925 (89.2%) |
| `twitter-roberta-base-sentiment-latest` | "The new security system is extremely rel..." | `LITERAL` | **POSITIVE** | 0.7663 (76.6%) |
| `bert-base-uncased-SST-2` | "The new security system is extremely rel..." | `LITERAL` | **POSITIVE** | 0.9980 (99.8%) |
| `albert-base-v2-SST-2` | "The new security system is extremely rel..." | `LITERAL` | **POSITIVE** | 0.9876 (98.8%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 2 (28.6%) | 0/1 (14.3%) | 5/6 (83.3%) | 85.7% | 0.1380 | -0.4 pp |
| `twitter-roberta-base-sentiment` | 7 | 1 (14.3%) | 0/1 (14.3%) | 6/6 (100.0%) | 100.0% | 0.1270 | -1.9 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 1 (14.3%) | 0/1 (14.3%) | 6/6 (100.0%) | 85.7% | 0.1657 | -4.6 pp |
| `bert-base-uncased-SST-2` | 7 | 2 (28.6%) | 0/1 (14.3%) | 5/6 (83.3%) | 85.7% | 0.1266 | -1.4 pp |
| `albert-base-v2-SST-2` | 7 | 1 (14.3%) | 0/1 (14.3%) | 6/6 (100.0%) | 85.7% | 0.1003 | -8.3 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 0 | 1 | 0 | 0 | 6 |
| `twitter-roberta-base-sentiment` | 0 | 0 | 0 | 0 | 7 |
| `twitter-roberta-base-sentiment-latest` | 0 | 0 | 1 | 0 | 6 |
| `bert-base-uncased-SST-2` | 0 | 1 | 0 | 0 | 6 |
| `albert-base-v2-SST-2` | 0 | 0 | 1 | 0 | 6 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 91.43%

### Pairwise Concordance Matrix
| Model | `Twitter-RoBERTa (Base)` | `Twitter-RoBERTa (Latest)` | `DistilBERT SST-2` | `ALBERT SST-2` | `BERT SST-2` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Twitter-RoBERTa (Base)` | 100.0% | 100.0% | 85.7% | 100.0% | 85.7% |
| `Twitter-RoBERTa (Latest)` | 100.0% | 100.0% | 85.7% | 100.0% | 85.7% |
| `DistilBERT SST-2` | 85.7% | 85.7% | 100.0% | 85.7% | 100.0% |
| `ALBERT SST-2` | 100.0% | 100.0% | 85.7% | 100.0% | 85.7% |
| `BERT SST-2` | 85.7% | 85.7% | 100.0% | 85.7% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |

## 8. Semantic Reference Methodology & Ground-Truth Alignment
1. **Canonical Semantic Label Space**: Ground-truth polarity is strictly confined to `POSITIVE`, `NEGATIVE`, and `NEUTRAL`. Non-canonical sentiment categories (such as `MIXED`, `AMBIGUOUS`, `SARCASTIC`) are rejected.
2. **Google Gemini Role**: Gemini operates exclusively as an external semantic annotator/verification layer for baseline and probe sentences. It is **never** a benchmark model, does not forecast model failures, and is strictly prohibited from generating the failure taxonomy.
3. **Human Verification & Override**: Every semantic reference can be verified and overridden by researchers (`[Accept]` / `[Change]`). Frozen semantic references are strictly immutable during model evaluation.
4. **Binary vs. Multiclass Alignment**: Binary models (e.g. 2-class SST-2) natively output `NEGATIVE` and `POSITIVE`. When semantic reference is `NEUTRAL`, binary models' forced polarity is recorded as `NOT_DIRECTLY_REPRESENTABLE` (`BINARY_FORCED_POLARITY`), preserving empirical truth rather than falsely modifying the reference.
5. **Independence of Model Outputs & Rule-Based Taxonomy**: Model predictions remain 100% empirical forward-pass outputs. The failure taxonomy (`Blind`, `Spurious`, `Misweighted`, `Undetermined`) is derived purely by deterministic rule-based behavioral analysis, completely independent of Gemini.