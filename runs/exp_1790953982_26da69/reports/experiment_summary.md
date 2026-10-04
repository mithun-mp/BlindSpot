# BlindSpot Research Audit Report: FlipKart3FoootBall

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790953982_26da69`
- **Run Plan Created**: `1790953984.4502716`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790953960_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 1626.69s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "Good product good quality all are good. But font play without barefoots.because it is a hardground football"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "Good product good quality all are good. ..." | `LITERAL` | **POSITIVE** | 0.9915 (99.2%) |
| `albert-base-v2-SST-2` | "Good product good quality all are good. ..." | `LITERAL` | **POSITIVE** | 0.7930 (79.3%) |
| `twitter-roberta-base-sentiment-latest` | "Good product good quality all are good. ..." | `LITERAL` | **POSITIVE** | 0.7435 (74.3%) |
| `bert-base-uncased-SST-2` | "Good product good quality all are good. ..." | `LITERAL` | **POSITIVE** | 0.8466 (84.7%) |
| `twitter-roberta-base-sentiment` | "Good product good quality all are good. ..." | `LITERAL` | **POSITIVE** | 0.6672 (66.7%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 2 (28.6%) | 0/2 (28.6%) | 5/5 (100.0%) | 100.0% | 0.0371 | -2.9 pp |
| `albert-base-v2-SST-2` | 7 | 2 (28.6%) | 0/2 (28.6%) | 5/5 (100.0%) | 100.0% | 0.2414 | -3.4 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 1 (14.3%) | 0/2 (28.6%) | 5/5 (100.0%) | 85.7% | 0.3713 | -9.4 pp |
| `bert-base-uncased-SST-2` | 7 | 3 (42.9%) | 0/2 (28.6%) | 4/5 (80.0%) | 85.7% | 0.0789 | +6.5 pp |
| `twitter-roberta-base-sentiment` | 7 | 1 (14.3%) | 0/2 (28.6%) | 5/5 (100.0%) | 100.0% | 0.3661 | -3.3 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 0 | 0 | 0 | 0 | 7 |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 7 |
| `twitter-roberta-base-sentiment-latest` | 0 | 0 | 1 | 0 | 6 |
| `bert-base-uncased-SST-2` | 0 | 0 | 1 | 0 | 6 |
| `twitter-roberta-base-sentiment` | 0 | 0 | 0 | 0 | 7 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 85.71%

### Pairwise Concordance Matrix
| Model | `Twitter-RoBERTa (Base)` | `Twitter-RoBERTa (Latest)` | `DistilBERT SST-2` | `ALBERT SST-2` | `BERT SST-2` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Twitter-RoBERTa (Base)` | 100.0% | 100.0% | 85.7% | 85.7% | 71.4% |
| `Twitter-RoBERTa (Latest)` | 100.0% | 100.0% | 85.7% | 85.7% | 71.4% |
| `DistilBERT SST-2` | 85.7% | 85.7% | 100.0% | 100.0% | 85.7% |
| `ALBERT SST-2` | 85.7% | 85.7% | 100.0% | 100.0% | 85.7% |
| `BERT SST-2` | 71.4% | 71.4% | 85.7% | 85.7% | 100.0% |

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