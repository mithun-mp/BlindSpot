# BlindSpot Research Audit Report: Multimodel health

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790617710_ee23be`
- **Run Plan Created**: `1790617711.997399`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `cardiffnlp/twitter-roberta-base-sentiment`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `textattack/bert-base-uncased-SST-2`, `textattack/albert-base-v2-SST-2`
- **Probe Set ID / Version**: `pset_1790617685_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 314.91s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "i am healthy but still hospitalized"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "i am healthy but still hospitalized..." | `LITERAL` | **NEGATIVE** | 0.8577 (85.8%) |
| `twitter-roberta-base-sentiment` | "i am healthy but still hospitalized..." | `LITERAL` | **NEUTRAL** | 0.4850 (48.5%) |
| `twitter-roberta-base-sentiment-latest` | "i am healthy but still hospitalized..." | `LITERAL` | **NEUTRAL** | 0.6338 (63.4%) |
| `bert-base-uncased-SST-2` | "i am healthy but still hospitalized..." | `LITERAL` | **NEGATIVE** | 0.8187 (81.9%) |
| `albert-base-v2-SST-2` | "i am healthy but still hospitalized..." | `LITERAL` | **NEGATIVE** | 0.6339 (63.4%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 1 (14.3%) | 0/1 (14.3%) | 6/6 (100.0%) | 100.0% | 0.0594 | +8.3 pp |
| `twitter-roberta-base-sentiment` | 7 | 6 (85.7%) | 0/1 (14.3%) | 1/6 (16.7%) | 28.6% | 0.4352 | +23.6 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 4 (57.1%) | 0/1 (14.3%) | 3/6 (50.0%) | 42.9% | 0.3542 | +4.2 pp |
| `bert-base-uncased-SST-2` | 7 | 1 (14.3%) | 0/1 (14.3%) | 6/6 (100.0%) | 85.7% | 0.1542 | +5.7 pp |
| `albert-base-v2-SST-2` | 7 | 1 (14.3%) | 0/1 (14.3%) | 6/6 (100.0%) | 100.0% | 0.2568 | +10.9 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 0 | 0 | 0 | 0 | 7 |
| `twitter-roberta-base-sentiment` | 0 | 5 | 0 | 0 | 2 |
| `twitter-roberta-base-sentiment-latest` | 0 | 3 | 1 | 0 | 3 |
| `bert-base-uncased-SST-2` | 0 | 0 | 1 | 0 | 6 |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 7 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 55.71%

### Pairwise Concordance Matrix
| Model | `Twitter-RoBERTa (Base)` | `Twitter-RoBERTa (Latest)` | `DistilBERT SST-2` | `ALBERT SST-2` | `BERT SST-2` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Twitter-RoBERTa (Base)` | 100.0% | 42.9% | 28.6% | 28.6% | 28.6% |
| `Twitter-RoBERTa (Latest)` | 42.9% | 100.0% | 42.9% | 42.9% | 42.9% |
| `DistilBERT SST-2` | 28.6% | 42.9% | 100.0% | 100.0% | 100.0% |
| `ALBERT SST-2` | 28.6% | 42.9% | 100.0% | 100.0% | 100.0% |
| `BERT SST-2` | 28.6% | 42.9% | 100.0% | 100.0% | 100.0% |

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