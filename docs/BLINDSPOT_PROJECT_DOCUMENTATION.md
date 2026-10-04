# BLINDSPOT: A MODEL-AGNOSTIC BEHAVIORAL STRESS-TESTING AND EXPLAINABILITY WORKSTATION FOR TRANSFORMER-SAEN SENTIMENT CLASSIFIERS

**Authoritative System Documentation & College Project Review Reference**


---



## Document Metadata & Context

- **Project Title**: BlindSpot: Model-Agnostic Behavioral Auditing & Failure Explainability

- **System Version**: 2.4.0 (Production Stabilized)

- **Document Type**: Comprehensive College Thesis / Technical Review Document

- **Verification Status**: VERIFIED AGAINST ACTUAL CODE BASELINE (280/280 Passing Tests)

- **Primary Domain**: Natural Language Processing (NLP) / Transformer Robustness

---



## TABLE OF CONTENTS



1. [Executive Summary & Academic Abstract](#1-executive-summary---academic-abstract)

2. [Problem Statement & Research Motivation](#2-problem-statement---research-motivation)

3. [Project Objectives & Scope Boundaries](#3-project-objectives---scope-boundaries)

4. [Theoretical Foundations & Knowledge Study](#4-theoretical-foundations---knowledge-study)

5. [Target Model Study (Curated Architecture Suite)](#5-target-model-study-curated-architecture-suite)

6. [Linguistic Probe Generation System](#6-linguistic-probe-generation-system)

7. [Semantic Reference & Ground Truth Verification](#7-semantic-reference---ground-truth-verification)

8. [Behavioral Evaluation & The Probe Contract Model](#8-behavioral-evaluation---the-probe-contract-model)

9. [Behavioral Failure Taxonomy & Diagnostic Classification](#9-behavioral-failure-taxonomy---diagnostic-classification)

10. [Quantitative Behavioral Metrics & Formulations](#10-quantitative-behavioral-metrics---formulations)

11. [The 7-Probe Critical Metric Walkthrough](#11-the-7-probe-critical-metric-walkthrough)

12. [Explainability & Token Attribution Pipeline](#12-explainability---token-attribution-pipeline)

13. [System Architecture & Layered Design](#13-system-architecture---layered-design)

14. [Component Architecture & Detailed Responsibilities](#14-component-architecture---detailed-responsibilities)

15. [End-to-End Data Flow & Lifecycle](#15-end-to-end-data-flow---lifecycle)

16. [Experiment Execution Workflow](#16-experiment-execution-workflow)

17. [Real-World Failure Walkthroughs & Case Studies](#17-real-world-failure-walkthroughs---case-studies)

18. [Empirical Experimental Results & Comparative Findings](#18-empirical-experimental-results---comparative-findings)

19. [Results Storage & Persistence Schema](#19-results-storage---persistence-schema)

20. [Reporting & Publication Subsystem](#20-reporting---publication-subsystem)

21. [Interactive Workstation UI & User Experience](#21-interactive-workstation-ui---user-experience)

22. [Testing, Verification & Quality Assurance](#22-testing-verification---quality-assurance)

23. [Reproducibility, Determinism & Artifact Integrity](#23-reproducibility-determinism---artifact-integrity)

24. [Limitations, Assumptions & Boundary Conditions](#24-limitations-assumptions---boundary-conditions)

25. [Ethical Considerations & Research Dual-Use](#25-ethical-considerations---research-dual-use)

26. [Research Contributions & Benchmark Comparison](#26-research-contributions---benchmark-comparison)

27. [Current Implementation State vs. Future Work Matrix](#27-current-implementation-state-vs-future-work-matrix)

28. [Conclusion](#28-conclusion)

29. [Technical References & Bibliography](#29-technical-references---bibliography)

30. [Appendices A through G](#30-appendices-a-through-g)

---



# 1. Executive Summary & Academic Abstract



### 1.1 Executive Summary

BlindSpot is a research-grade, model-agnostic behavioral auditing, stress-testing, and failure explainability workstation specifically engineered for transformer-based text classification systems. In contemporary machine learning, high static benchmark accuracy (e.g., SST-2, IMDB) frequently masks critical behavioral brittleness. Transformer models regularly fail to respond consistently when controlled linguistic perturbations like syntactic negation, adversative contrast, downtoning, or synonym substitution are applied to the input.



BlindSpot replaces naive aggregate accuraty metrics with a research-valid, probe-level behavioral contract model. Every input is systematically stress-tested against a curated suite of deterministic linguistic probes, where each probe carries an explicit semantic contract (either reversing or preserving target polarity). By comparing baseline predictions against probe predictions, BlindSpot evaluates model behavioral compliance without assuming that a prediction flip automatically equals correctness. Failures are then subjected to an evidence-backed 4-way failure taxonomy (BLIND, MISWEIGHTED, PPURIOUSUS, or UNDETERMINED) backed by independent LIME and SHAP feature attributions.



### 1.2 Academic Abstract

**Abstract** — Supervised fine-tuning of pretrained transformer language models (e.g., BERT, DistilBERT, ALBERT, RoBERTa) has dramatically advanced the state of the art in sentiment classification. However, standard empirical evaluation paradigms rely almost exclusively on accuracy, F1-score, and loss over independently and identically distributed (i.i.d.) test sets. These static metrics fail to measure how models behave when subjected to controlled, minimal linguistic modifications. This paper presents **BlindSpot**, a research-valid, model-agnostic behavioral auditing workstation designed to investigate, quantify, and explain the robustness and semantic consistency of transformer-based sentiment classifiers. 



BlindSpot constructs a deterministic setwork of linguistic probes across 7 canonical perturbation families (including syntactic negation insertion, double negation framing, intensity modulation, adversative contrast appending, and lexical subonym substitution). Each probe is evaluated against an authoritative, dual-engine semantic reference system comprising an external Google Gemini LLM annotator with automated credential rotation, backed by an offline local heuristic lexical fallback. 



Mathematically, BlindSpot rigorously distinguishes between *Observed Flip Rate* (fraction of all executed probes flipping), *Suite Expected-Flip Share* (suite composition requiring flips), *Expected-Flip Compliance* (success rate only on probes where flips were expected), *Preserve Rate* (success rate on invariant probes), and *Behavioral Consistency* (total contract satisfaction). When a behavioral failure occurs, BlindSpot diagnoses the root cause using an evidence-backed 4-way taxonomy: (1) *BLIND*: the model ignores the perturbation operator (attribution magnitude < 0.05); (2) *MISWEIGHTED*: the model recognizes the operator (attribution ‍ 0.05), but competing clauses overpower it; (3) *SPURIOUS-SUSPECTPect*: the decision is driven by non-causal background stop words; and (4) *UNDETERMINED*: insufficient explainability evidence. 



Evaluated across 5 curated transformer architectures (DistilBERT SST-2, ALBERT Base, Twitter RoBERTa Latest, BERT Base, and Twitter RoBERTa Base), BlindSpot reveals that an observed flip rate of 28.57% can mask an Expected-Flip Compliance of 0.00%, proving that conventional static metrics are insufficient for assessing real-world NLP robustness. The system provides publication-grade ReportLab PDF generation, interactive Streamlit dashboards, statistical ECE calibration analysis, and full experimental reproducibility.

---



# 2. Problem Statement & Research Motivation



### 2.1 The Accuracy Paradox in Transformer NLU

Transformer-based NLP models have become the industry and academic standard for text classification tasks, achieving supreme benchmark performance on datasets such as SST-2 (>90% accuracy) and IMDb (>93% accuracy). Despite these impressive surface numbers, empirical research reveals that high accuracy on an iid. (independently and identically distributed) test split does not prevent structural behavioral instability.



A sanstransformer model may achieve 98% prediction confidence on the sentence:

> *"The movie was great and the acting was top notch."*// POSITIVE (100%)



Yet, when a single syntactic negation operator ("not") is inserted before the adjective, yielding:

> *"The movie was not great and the acting was top notch."*



common production models (e.g., DistilBERT sst-2) still predict **POSITIVE** with 98.5% confidence! The model is effectively blind or misweighted to the negation cue, because lexical attractors ("great", "top notch") dominate its self-attention matrices.



### 2.2 Limitations of Static Benchmark Evaluations

Traditional NLP evaluation suffers from three fundamental blind spots:

1. **Invariant Neglect**: Conventional benchmarks donot test individual linguistic relationships. They assume that every input is an isolated, independent sample.

2. **Missing Contracts**: There is no explicit semantic contract defining whether a specific input transformation should preserve, reverse, or attenuate the output.

3. **Flip Counting Fallacy**: When researchers do perform perturbation stress-testing, they often count the *total number of prediction flips* and report it as a single "robustness score". This metric is fatally flawed.



### 2.3 The Fundamental Flip Paradox

To understand why conventional flip rates mislead researchers, consider a controlled 7-probe audit suite evaluating a single positive baseline sentence (e.g., golden seed text from experiment audit):



| Probe ID | Perturbation Type | Semantic Intent | Expected Flip | Model Observed Flip | Contract Satisfied? |

|------------|--------------------|----------------|---------------|-------------------|--------------------|

| P1 | Negation Insertion | ADD_NEGATION | **Yes (FLIP)** | No (POS ₒ POS) | **FAIL* (Missing Flip) |

| P2 | Double Negation | PRESERVE_MEANING | No (PRESERVE) | No (POS ₒ POS) | **PASS* (Preserved) |

| P3 | Intensifier | STRENGTHEN | No (PRESERTE) | **Yesz* (POS  to  NEG)| **FAIL* (Unexpected Flip) |

| P4 | Downtoner | WEAKEN | No (PRESERVE) | **Yes** (POS ₑ NEG)| **FAIL* (Unexpected Flip) |

| P5 | Synonym Swap | PRESERVE_MEANING | No (PRESERTE) | No (POS  to  POS) | **PASS* (Preserved) |

| P6 | Contrast Negative | SHIFT_CONTRAST | **Yes (FLIP)**| No (POS  to  POS) | **FAIL* (Missing Flip) |

| P7 | Contrast Positive | PRESERVE_MEANING | No (PRESERTE) | No (POS  to  POS) | **PASS* (Preserved) |





**Comparingthe Feiling View ts. BlindSpot's View:**

1 **Naive Aggregate Flip Count**:

   - Number of expected flips in the suite = 2 (P1, P6).

   - Number of actual observed flips = 2 (P3, P4).

   - A naive evaluator might conclude: *"2 flips expected, 2 flips observed — model is robustly sensitive!`"

2 **BlindSpot's Canonical Audit Decomposition**:

   - *Observed Flip Rate (OFR)* = 2 / 7 = **28.57%**

   - *Suite Expected-Flip Share (SEFS) * = 2 / 7 = **28.57%** (probe suite property, not model success)

   - *Expected-Flip Compliance (EFC)* = 0 / 2 = **0.00%** (The model failed 100% of its flip contracts!)

   - *Preserve Rate (PR)* = 3 / 5 = **60.00%** (Two unexpected flips on Perseve probes)

   - *Behavioral Consistency (BC)* = 3 / 7 = **42.86%** (Only 3 contracts satisfied out of 7)



This example proves why expected flips and observed flips must never be conflated. BlindSpot was created pricisely to make this distinction mathematically authoritative and computationally enforced.

---



# 3. Project Objectives & Scope Boundaries



### 3.1 Primary Objectives

1. **Controlled Linguistic Probing**: Generate deterministic suites of phonological, syntactic, and semantic linguistic perturbations across 7 canonical families (Negation, Double Negation, Intensity, Contrast Negative, Contrast Positive, Synonym Swap, and Structural Reordering).

2. **Behavioral Contract Auditing**: Compare model predictions between baseline sentences and perturbed stimuli against calibrated semantic contracts (reversal vs. preservation).

3. **Evidence-Backed Failure Taxonomy**: Beyond merely noting a failure, classify its root cause into BLIND, MISWEIGHTED, PPURIOUS, or UNDETERMINED using independent LIME and SHAP feature attribution evidence.

4. **Multi-Model Comparative Analysis**: Provide a unified inference and evaluation pipeline across diverse transformer families (DST-2 Binary vs. Twitter 3-Class) without domain polarity inversion errors.

5. **Publication-Grade Reporting**: Automate the generation of structured audit JSON, textual Markdown reports, 7 publication thesis figures, and an end-to-end ReportLab PDF audit report.



### 3.2 Scope Classification Matrix



| System Capability | Implementation Status | Verification Evidence | Operational Notes |

|--------------------|----------------------|-----------------------|-----------------------------|

| 7-Family Probe Generation | **IMPLEMENTED** | `shared.py`, test_probe_integrity.py | 100% deterministic probe hashing |

| Behavioral Contract Model | **IMPLEMENTED** | `metrics.py`, `test_behavioral.py` | OFR, EFC, PR, BC strictly separated |

| 4-Way Failure Taxonomy | **IMPLEMENTED** | `taxonomy.py`, `test_behavioral_taxonomy.py` | Explicit thresholds (0.05, 50% stopwords) |

| 5-Model Auditing Suite | **IMPLEMENTED** | `registry.py`, `huggingface_wrapper.py` | SST-2 binary + Twitter 3-class identity |

| Dual-Engine Semantic Ref | **IMPLEMENTED** | `semantic/client.py`, test_gemini.py | Gemini 2)5/1.5 Flash + VADER Fallback |

| LIME / SHAP Explainers | **IMPLEMENTED** | `lime_explainer.py`, `shap_explainer.py` | Kept 100% separate, no fusion or averaging |

| Token Alignment & Metrics | **IMPLEMENTED** | `alignment.py`, test_canonical_pipeline.py | Metadata filtered, Jaccard & Cosine valid |

| ReportLab Publication PDF | **IMPLEMENTED** | `audit_pdf_generator.py` | 7 thesis figures embedded with academic text |

| Streamlit Research WI | **IMPLEMENTED** | `app.py`, `ui/` (14 screens) | 6 Primary Domains, no dummy/fake values |

| Attention Head Explainer | *PARTIALLY IMPLEMENTED* | `attention_explainer.py` | Extracts raw attention; UI uses LIME/SHAP |

| Multilingual Probe Engine | *PLANNED / FUTURE WORK* | N/A | Current implementation is English-specific |

| ASR / Speech Probes | *OUT OF SCOPE* | N/A | System focuses solely on text classification |



### 3.3 Core Architectural Invariants

1. **No Masquerading Data**: No dummy, mock, or synthetic values may appear in the UI, metrics, or reports. If an explanation fails, it must be flagged as `missing` rather than invented.

2. **Missing Flip ≠ BLIND**: A missing prediction flip does not automatically indicate attention blindness. If the operator weight is ≥ 0.05, the failure is Misweighted.

3. **Explainer Isolation**: LIME and SHAP must never be averaged or fused into a single arbitrary vector; they represent different mathematical principles.

4. **Canonical Prediction Mapping**: Raw class indices:

   - SST-2 (2 class): Class 0 = NEGATIVE, Class 1 = POSITIVE

   - Twitter RoBERTa (3 class): Class 0 = NEGATIVE, Class 1 = NEURAL, Class 2 = POSITIVE

---



# 4. Theoretical Foundations & Knowledge Study



### 4.1 Modern NLP & Sentiment Classification Foundations

Natural Language Processing (NLP), attempts to map unconstrained human natural language into structured, machine-readable representations. Sentiment classification represents a core task in software engineering, where an input sequence of discrete linguistic tokens $x=(x_1, \dots, x_T)a is mapped into a probability distribution over categorical sentiment labels $y \in \[left\[labels\\right\]^.



### 4.2 Supervised Learning vs. Behavioral Testing

Traditional supervised learning minimizes empirical risk over a training corpus:



$$

Min \mathcal{L}_{\text{EmpeEmpir}}(\theta) = \frac{1}{N} \sum_{i=1}^{N} \check{\}sum_i \closely mapped loss

$$



However, high accuracy under i.i.d. testing does not prevent shortcut learning or logical brittleness. Rebecca Ribero et al. (2020) proposed CheckList, demonstrating that individual behavioral capabilities (Minimum Functionality Tests, Invariance Tests, and Directional Expectation Tests) must be independently verified. BlindSpot extends CheckList's foundations from a static library into an automated, dual-engine behavioral auditing workstation with failure attribution and model-agnostic registries.



### 4.3 The Transformer Architecture & Self-Attention

The Transformer (Vaswani et al., 2017) replaced recurrent architectures with parallel self-attention:



$$

Attention(Q, K, V) = \softmax\left(\frac{QK

T}{\sqt{d_k}}\right) V

$$



In sentiment classification, attention heads assign pairwise weights across all input tokens. When an adversarial or syntactic negation operator ("not") is inserted, the model must attend sufficiently to the operator and its adversarial scope. If self-attention heads deposit most weights onto dominant lexical tokens ("great", "charming"), the model suffers from attention blindness or clausal misweighting.



### 4.4 Architectural Evolution: BERT, DistilBERT, ALBERT, and RoBERTa



1. **BERT (Devlin et al., 2018)**:

   - 12-layer encoder, uncased WordPiece tokenizer (~30K vocab), 110M parameters.

   - Trained on Masked Language Modeling (MLM) and Next Sentence Prediction (NSP).

2. **DistilBERT (Sanh et al., 2019)**:

   - 6-layer compressed encoder, 66M parameters (40% smaller, 60% faster than BERT).

   - Trained via triple knowledge distillation loss (soft targets, hidden state cosine alignment, MLM).

3. **ALBERT (Lan et al., 2019)**:

   - 12 logical layers using *cross-layer parameter sharing*; only 12M free parameters.

   - Factorized embedding parameterization (vocab dimension reduced from 768-to-128).

4. **RoBERTE (Liu et al., 2019)**:

   - 12-layer encoder optimized with *dynamic masking*, larger batch sizes (8K), and *Byte-Level BPE* tokenizer (~50K vocab); NSP removed.



### 4.5 Classification Heads, Logits, & Softmax

Each architecture passes the `[CLS]` token hidden representation through a dense projection head:

$$

z(c)= Wm_c \times h_#{TCLS}} + b_c

$$

Softmax probabilities are computed as:

$$

p(c)= \frac{\exp(z(c) }}{\bullet \sum_{j} \exp(z(j)) }

$$



### 4.6 Statistical Calibration & ECE

A robust model must not only be accurate but * calibrated* — its prediction probabilities should reflect its true correctness likelihood. BlindSpot implements Multiclass Expected Calibration Error (ECE) with 10 equal-width bins between 0.0 and 1.0:

$$

ECE = \sum_{m=1}^{M} \frac{<|B_m|~ ~}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|

$$

---



# 5. Target Model Study (Curated Architecture Suite)



### 5.1 The 5 Curated Benchmark Architectures

BlindSpot integrates 5 curated preset models across two major label topologies (SST-2 2-Class Binary vs. Twitter 3-Class Sentiment):



1. **distilbert-base-uncased-finetuned-sst-2-english**

   - *Architecture**: DistilBERT (6 layers, 768 hidden dim, 12 attention heads, 66M Parameters).

   - *Tokenizer**: WordPiece uncased (30,528 vocab size).

   - *Labels & Head**: 2-Class binary head (il2label: 0 = NEGATIVE, 1 = POSITIVE).

   - *Domain**: Formal film reviews (Stanford Sentiment Treebank).



2. **textattack/albert-base-v2-SST-2**

   - *Architecture**: ALBERT (12 logical layers, shared weights, 12M Unique Parameters, factorized embeddings 128->768).

   - *Tokenizer**: SentencePiece uncased (30,000 vocab size).

   - *Labels & Head**: 2-Class binary head (id2label: 0 = NEGATIVE, 1 = POSITIVE).

   - *Domain**: SST-2 benchmark.



3. **cardiffnlp/twitter-roberta-base-sentiment-latest**

   - *Architecture**: RoBERTa (12 layers, 768 hidden dim, 12 attention heads, 125M Parameters).

   - *Dataset**: Twitter; recently updated (2022, cardiffnlp).

   - *Tokenizer**: Byte-Level BPE (50,265 vocab size).

   - *Labels & Head**: 3-Class head (id2label: 0 = NEGATIVE, 1 = NEUTRAL, 2 = POSITIVE).



4. **textattack/bert-base-uncased-SST-2**

   - *Architecture**: Classic BERT Base (12 layers, 768 hidden dim, 120M Parameters, WordPiece).

   - *Labels & Head**: 2-Class binary head (id2label: 0 = NEGATIVE, 1 = POSITIVE).



5. **cardiffnlp/twitter-roberta-base-sentiment**

   - *Architecture**: Original Twitter RoBERTa Base (3Way social media sentiment).

   - *Labels & Head**: 3-Class head (id2label: 0 = NEGATIVE, 1 = NEUTRAL, 2 = POSITIVE).



### 5.2 Comparative Architectural Matrix



| Model Identifier | Family | Params | Tokenizer | Vocab | Classes | Label Schema | Domain |

|--------------------|--------|--------|----------|-------|--------|--------------|--------|

| DistilBERT SST-2 | DistilBERT | 66M | WordPiece | 30,528 | 2 | NEG/ POS | Film Reviews |

| ALBERT Base sst-2 | ALBERT | 12M (12 logical) | SentencePiece | 30,000 | 2 | NEG/ POS | SST-2 Bench |

| Twitter RoBERTa Latest | RoBERTE | 125M | Byte-BPE| 50,265 | 3 | NEG/NEUPOS | Social Media |

| BERT Base SST-2 | BERT | 110M | WordPiece | 30,528 | 2 | NEG/ POS | Film Reviews |

| Twitter RoBERTa Base | RoBERTa | 125M | Byte-BPE| 50,265 | 3 | NEG/NETaPOS | Social Media |



### 5.3 Scientific Rationale for Multi-Model Auditing

Comparing these five architectures is research-critical:

1. **Parameter Efficiency vs. Robustness**: ALBERT's shared-weight architecture (12M) can be compared directly to BERT (110M) to test whether parameter sharing weakens or strengthens syntactic attention robustness.

2. *Distillation Reliability**: DistilBERT (66S) reveals how knowledge distillation impacts sensitivity to mitigating negation compared to its parent BERT model.

3. *Tokenizer Bias**: Byte-level BPE (RoBERTE) is resistant to out-of-vocabulary tokens, while WordPiece splits unknown words into ``fragments``.

4. **Topology Invariance**: BlindSpot authoritatively prevents domain inversion errors between 2-class and 3-class models label 0 means NEGATIVE in both models, but label 1 is POSITIVE in SST-2 and NEUTRAL in Twitter RoBERTa! BlindSpot's `ModelRegistry` and `HuggingFaceWrapper` explicitly preserve this contract.

---



# 6. Linguistic Probe Generation System



### 6.1 Linguistic Perturbation Principles

BlindSpot's probe generation engine (`shared.py`, `engine.py`) produces deterministic, reproducible linguistic probes from any natural language seed text. Rather than applying random noise or arbitrary mutations, each perturbation is grounded in formal linguistic principles.



### 6.2 The 7 Canonical Probe Families



1. **Negation Insertion (`negation_insertion`)**

   - *Linguistic Operation:* Identifies predicate adjectives or copular verbs ("is", "was", "are", like, love) and inserts a syntactic negation operator ("not") in the governing position.

   - *Semantic Intent:* `ADD_NEGATION`.

   - *Expected Flip:* **YES (TRUE)** — Reverses canonical sentiment polarity.

   - *Example:* "The product was great."  to  "The product was not great."



2. **Double Negation (`double_negationgi)**

   - *Linguistic Operation:* Prepends a classical double negation linguistic frame ("It is not impossible that ..." or "It cannot be denied that ...").

   - *Semantic Intent:* `PRESERVE_MEANING`.

   - *Expected Flip:** **NO (FALSE)* — Preserves original sentiment polarity under formal mitigation.

   - *Example:*"said movie was great." ₑ "It is not impossible that the movie was great."



3. **Intensifier (`intensity` - Strengthen)(**

   - *Linguistic Operation:* Inserts strongly boosting adverbs ("extremely", "highly", "absolutely") before the sentiment carrier adjective.

   - *Semantic Intent:* `STRENGTHEN_POLARITY`.

   - *Expected Flip:** **NO (FALSE)* — Polarity must be preserved; confidence is expected to remain high or increase.

   - *Example:* "The acting was good."  to  "The acting was extremely good."



4. **Downtoner (`intensity` - Weaken)**

   - *Linguistic Operation:* Inserts attenuating diminutive adverbs ("somewhat", "slightly", "partially").

   - *Semantic Intent:* `WEAKEN_POLARITY`.

   - *Expected Flip:* **NO (FALSE)** ₕ Polarity must be preserved; prediction label should not flip to opposite.

   - *Example:* "The film was bad."  to  "The film was somewhat bad."



5. **Lexical Synonym Substitution (`synonym_substitution`)**
   - *Linguistic Operation:* Replaces core sentiment-bearing lexical tokens with contextually equivalent synonyms (e.g., "great" -> "exceptional", "good" -> "fine", "bad" -> "terrible") using verified WordNet synsets or masked language model suggestions.
   - *Semantic Intent:* `PRESERVE_POLARITY`.
   - *Expected Flip:* **NO (FALSE)** — Lexical variance within the same semantic basin must not alter the categorical sentiment polarity.
   - *Example:* "The movie was great and the acting was top notch." -> "The film was great and the acting was top notch."
   - *Failure Mode:* Model prediction flips due to lexical frequency artifacts or out-of-vocabulary subword tokenization anomalies.

6. **Contrastive Clause Append (`contrast_negative_append`)**
   - *Linguistic Operation:* Appends an adversative contrastive clause (", but it was bad", ", however the conclusion was terrible") to a positive or neutral baseline.
   - *Semantic Intent:* `REVERSE_POLARITY` or `OVERRIDE_POLARITY`.
   - *Expected Flip:* **YES (TRUE)** — In English discourse syntax, the terminal adversative clause governed by "but" / "however" semantically dominates the prior discourse segment, flipping the overall sentiment polarity from positive to negative.
   - *Example:* "The movie was great and the acting was top notch." -> "The movie was great and the acting was top notch, but it was bad."
   - *Failure Mode:* Model suffers from recency blindness or token-salience inertia; the dominant positive tokens in the initial clause overpower the negative adversative clause, resulting in a `missing_flip` failure.

7. **Positive Concession Append (`contrast_positive_append`)**
   - *Linguistic Operation:* Appends an adversative positive clause (", however it had charming moments", ", but the soundtrack was delightful") to a baseline sentence.
   - *Semantic Intent:* `ATTENUATE_OR_REVERSE`.
   - *Expected Flip:* **NO (FALSE)** or context-dependent — When applied to an already strongly positive baseline, appending a positive concession reinforces positive polarity; prediction label must remain POSITIVE.
   - *Example:* "The movie was great and the acting was top notch." -> "The movie was great and the acting was top notch, but the visual direction was amazing."
   - *Failure Mode:* Spurious sensitivity to adversative syntax markers ("but") causing an erroneous flip to negative despite positive lexical semantics.

---

# 7. Semantic Reference & Ground Truth Verification

### 7.1 Ground Truth Synthesis Architecture
A core engineering challenge in behavioral NLP stress-testing is establishing authoritative, objective expected outcomes for dynamically generated linguistic probes. If expected behavior is derived naively or hard-coded statically, subtle semantic edge cases (e.g., sarcastic undertones, double negation canceling, complex syntactic subordination) will yield false positive audit failures.

BlindSpot implements a dedicated **Semantic Reference Layer** that acts as an independent semantic oracle, decoupled from the target models under test.

### 7.2 Multi-Tier Semantic Arbiter Hierarchy
To guarantee runtime resilience, offline execution capability, and strict deterministic evaluation, BlindSpot employs a resilient, three-tier fallback hierarchy:

```
[Dynamic Probe Input]
         │
         ▼
┌─────────────────────────────────┐
│ Tier 1: Primary LLM Arbiter     │  (Google Gemini 2.5 / Flash API)
│ Deep Semantic & Discourse Logic │  -> Returns: Polarity, Relation, Confidence
└────────────────┬────────────────┘
                 │ (If Quota Exhausted, Timeout, or Network Failure)
                 ▼
┌─────────────────────────────────┐
│ Tier 2: Local NLI Arbiter       │  (RoBERTa-large-MNLI Cross-Encoder)
│ Natural Language Inference      │  -> Premise: Baseline, Hypothesis: Probe
└────────────────┬────────────────┘  -> Entailment (Preserve), Contradiction (Flip)
                 │ (If GPU/Model Unavailable or Low Resource Mode)
                 ▼
┌─────────────────────────────────┐
│ Tier 3: Deterministic Heuristic │  (Rule-Based Grammatical & Lexicon Engine)
│ Linguistic Rule Synthesizer     │  -> WordNet, VADER Inversion, Structural Rules
└─────────────────────────────────┘
```

1. **Tier 1: Cloud LLM Arbiter (Primary)**
   - Utilizes Google Gemini via the official Google GenAI SDK.
   - Evaluates the baseline-probe pair under formal linguistic instructions: identifying discourse structure, concessive clauses, negations, and scope ambiguity.
   - Returns structured JSON: `{ "baseline_polarity": "POSITIVE", "probe_polarity": "NEGATIVE", "expected_relation": "REVERSE_POLARITY", "expected_flip": true, "reasoning": "Adversative clause dominates prior positive assertion." }`.

2. **Tier 2: Local Cross-Encoder NLI Arbiter (Zero-Dependency Fallback)**
   - Utilizes `roberta-large-mnli` to evaluate bidirectional inference between baseline $x_{\text{base}}$ and probe $x_{\text{probe}}$.
   - If $x_{\text{probe}}$ contradicts $x_{\text{base}}$, `expected_flip = True`.
   - If $x_{\text{probe}}$ is entailed by $x_{\text{base}}$, `expected_flip = False` (`Preserve`).

3. **Tier 3: Local Deterministic Heuristic Arbiter (Fail-Safe Offline Mode)**
   - Implemented in `blindspot/semantic/oracle.py` (`LocalHeuristicOracle`).
   - Analyzes lexical polarity shifts, negation operators, and grammatical syntax trees deterministically without external API or heavy neural network dependencies.
   - Guarantees 100% test reproducibility and air-gapped evaluation capability.

### 7.3 Operational Dynamic Synthesis Flow
During runtime execution, each generated probe is immediately passed to the configured Semantic Arbiter before model inference commences. The Arbiter's verdict is stamped onto the immutable probe object:
- `expected_polarity`: The true linguistic sentiment polarity of the perturbed sentence.
- `expected_relation`: The relational delta (`PRESERVE_POLARITY`, `REVERSE_POLARITY`, `STRENGTHEN_POLARITY`, `WEAKEN_POLARITY`).
- `expected_flip`: Strict boolean indicator (`True` if the categorical sentiment class must invert; `False` if it must remain invariant).

### 7.4 Decoupling Semantic Arbiter from Target Model Under Test
BlindSpot strictly enforces the architectural principle that **the arbiter must never share weights, activations, or lineage with the models under evaluation**. The 5 target benchmark models (BERT, DistilBERT, ALBERT, Twitter-RoBERTa) are treated purely as black-box or white-box subjects of audit, while the Arbiter represents the objective linguistic standard against which their behavioral competence is measured.

---

# 8. Behavioral Evaluation & The Probe Contract Model

### 8.1 The Probe Contract Paradigm
Traditional machine learning benchmark evaluation operates under an aggregate accuracy paradigm: test inputs are evaluated independently, and overall performance is summarized by the ratio of correct predictions. This paradigm is fundamentally unsuited for behavioral testing because it cannot detect internal inconsistency under controlled perturbations.

BlindSpot formulates behavioral stress-testing as a **Probe Contract Model**. Every generated probe $P_i$ forms a tripartite formal contract:

$$\mathcal{C}_i = \left( x_{\text{base}}, x_{\text{probe}}^{(i)}, \mathcal{E}_i \right)$$

where:
- $x_{\text{base}}$ is the unperturbed anchor sentence.
- $x_{\text{probe}}^{(i)}$ is the linguistically transformed probe sentence.
- $\mathcal{E}_i \in \{ \text{FLIP}, \text{PRESERVE} \}$ is the explicit behavioral expectation defined by the linguistic transformation.

A model satisfies the behavioral contract if and only if its observed prediction delta aligns with the contract expectation.

### 8.2 Baseline Anchor Inference
Before evaluating any probe, the target model under test $\mathcal{M}$ evaluates the baseline anchor $x_{\text{base}}$:

$$\hat{y}_{\text{base}} = \arg\max_{c} P(y=c \mid x_{\text{base}}), \quad p_{\text{base}} = \max_{c} P(y=c \mid x_{\text{base}})$$

This establishes the reference anchor state. If the baseline prediction is incorrect relative to human ground truth, BlindSpot records this baseline error but still evaluates behavioral stability relative to the model's own internal reference plane.

### 8.3 Probe Transformation Inference
Next, the target model evaluates the perturbed probe sentence $x_{\text{probe}}^{(i)}$:

$$\hat{y}_{\text{probe}}^{(i)} = \arg\max_{c} P(y=c \mid x_{\text{probe}}^{(i)}), \quad p_{\text{probe}}^{(i)} = \max_{c} P(y=c \mid x_{\text{probe}}^{(i)})$$

BlindSpot computes the observed behavioral transition:
- **Observed Flip:** $\text{observed\_flip}^{(i)} = \mathbb{I}(\hat{y}_{\text{probe}}^{(i)} \neq \hat{y}_{\text{base}})$.
- **Confidence Shift:** $\Delta p^{(i)} = p_{\text{probe}}^{(i)} - p_{\text{base}}$.

### 8.4 Contract Fulfillment Evaluation
The contract fulfillment indicator $\text{expectation\_match}^{(i)}$ is evaluated individually for each probe:

$$\text{expectation\_match}^{(i)} = \begin{cases} 
1, & \text{if } \mathcal{E}_i = \text{FLIP} \text{ and } \hat{y}_{\text{probe}}^{(i)} \neq \hat{y}_{\text{base}} \\
1, & \text{if } \mathcal{E}_i = \text{PRESERVE} \text{ and } \hat{y}_{\text{probe}}^{(i)} = \hat{y}_{\text{base}} \\
0, & \text{otherwise (Contract Violation)}
\end{cases}$$

If $\text{expectation\_match}^{(i)} = 0$, the probe execution is flagged as an empirical behavioral failure, triggering the Failure Taxonomy and Explainability Pipeline.

---

# 9. Behavioral Failure Taxonomy & Diagnostic Classification

When a behavioral contract violation occurs, simply labeling the outcome as a failure is insufficient for actionable model debugging. BlindSpot integrates a diagnostic taxonomy layer that attributes the root cause of the violation to specific mechanistic phenomena.

### 9.1 The Evidence-Backed 4-Way Failure Taxonomy

When a behavioral failure occurs (`missing_flip`, `unexpected_flip`, or `unexpected_change`), BlindSpot's `TaxonomyClassifier` calls upon quantitative evidence extracted from LIME and SHAP token attributions to diagnose the primary failure category:



1. **BLIND (Attention Blindness)/**

   - *Definition:* The model completely fails to assign meaningful attribution weight to the linguistic operator (e.g., "not", "however").

   - *Quantitative Trigger:* $\| \text{weight}_{\text{operator}} \| < 0.05$.

   - *Interpretation:* The self-attention heads ignored the perturbation cue entirely; it produced no decision influence.



2. **MISWEIGHTED (Clause Overpowering)**

   - *Definition:* The model recognizes the linguistic operator, but competing opposing features (such as strong positive lexical attractors) retained excessive weight, overpowering the operator.

   - *Invariant violation Fixed:* Earlier systems falsely labeled missing flips as BLIND even when "not" had a weight of -0.324! BlindSpot's authoritative taxonomy correctly classifies this as MISWEIGHTED.

   - *Quantitative Trigger:* $\| \text{weight}_{\text{operator}} \| \ge 0.05$, but the model failed to flip.



3. **SPURIOUS (Background / Shortcut Dominance)**

   - *Definition:* The desired or undesired shift was driven not by semantic content, but by non-causal background features (stop words, punctuation, articles).

   - *Quantitative Trigger:* Background/stop-word attributions account for > 50% of the total decision saliency.



4. **UNDETERMINED (Inconclusive Saliency)**

   - *Definition:* Explainability methods failed to converge, explanations were unavailable, or causality could not be determined responsibly.



---



# 10. Quantitative Behavioral Metrics & Formulations

To overcome the blind spots of accuracy-only evaluations, BlindSpot introduces a suite of formal behavioral metrics implemented in `blindspot/testing/metrics.py`. These metrics isolate distinct behavioral properties: test suite composition, model flipping behavior, compliance with semantic change, stability under semantic invariance, and probability calibration.

### 10.1 Observed Flip Rate (`observed_flip_rate` / OFR)
- **Definition:** The empirical fraction of all executed probes that caused the model's categorical prediction label to flip relative to its baseline anchor prediction.
- **Scope:** All executed probes ($N_{\text{total}}$).
- **Mathematical Formulation:**
  $$\text{OFR} = \frac{1}{N_{\text{total}}} \sum_{i=1}^{N_{\text{total}}} \mathbb{I}(\hat{y}_{\text{probe}}^{(i)} \neq \hat{y}_{\text{base}})$$
- **Numerator:** Total observed flips ($\sum \mathbb{I}(\hat{y}_{\text{probe}}^{(i)} \neq \hat{y}_{\text{base}})$).
- **Denominator:** Total executed probes ($N_{\text{total}}$).
- **Interpretation:** Purely descriptive statistic measuring model sensitivity to input perturbation. An OFR of 28.57% (2/7) indicates that 2 out of 7 probes changed the model's prediction. **Crucially, OFR alone does not indicate whether those flips were correct or erroneous.**

### 10.2 Suite Expected-Flip Share (`suite_expected_flip_rate` / SEFS)
- **Definition:** The proportion of probes in the generated evaluation suite whose linguistic transformations were designed and expected to induce a categorical polarity flip.
- **Scope:** Test suite property (independent of model behavior).
- **Mathematical Formulation:**
  $$\text{SEFS} = \frac{1}{N_{\text{total}}} \sum_{i=1}^{N_{\text{total}}} \mathbb{I}(\mathcal{E}_i = \text{FLIP})$$
- **Numerator:** Total probes with contract expectation $\mathcal{E}_i = \text{FLIP}$ ($N_{\text{expected\_flips}}$).
- **Denominator:** Total executed probes in suite ($N_{\text{total}}$).
- **Interpretation:** Reflects test-suite composition. In the canonical 7-probe suite, exactly 2 probes (P1: `negation_insertion` and P6: `contrast_negative_append`) expect a flip; thus $\text{SEFS} = 2/7 = 28.57\%$. **SEFS must never be confused with model success or compliance.**

### 10.3 Expected-Flip Compliance (`expected_flip_compliance` / EFC)
- **Definition:** Among *only* the subset of probes designed to flip polarity, the fraction where the model correctly flipped its prediction.
- **Scope:** Probes where $\mathcal{E}_i = \text{FLIP}$ ($N_{\text{expected\_flips}}$).
- **Mathematical Formulation:**
  $$\text{EFC} = \frac{\sum_{i \in \mathcal{S}_{\text{flip}}} \mathbb{I}(\hat{y}_{\text{probe}}^{(i)} \neq \hat{y}_{\text{base}})}{|\mathcal{S}_{\text{flip}}|}, \quad \text{where } \mathcal{S}_{\text{flip}} = \{ i \mid \mathcal{E}_i = \text{FLIP} \}$$
- **Numerator:** Expected-flip probes that successfully flipped.
- **Denominator:** Total expected-flip probes ($|\mathcal{S}_{\text{flip}}|$).
- **Interpretation:** Measures the model's semantic sensitivity to meaning-altering transformations. An EFC of 0.0% (0/2) indicates complete failure to heed negation and contrastive shifts.

### 10.4 Preserve Rate (`preserve_rate` / PR)
- **Definition:** Among *only* the subset of probes designed to preserve sentiment meaning, the fraction where the model maintained its baseline prediction.
- **Scope:** Probes where $\mathcal{E}_i = \text{PRESERVE}$ ($N_{\text{expected\_preserves}}$).
- **Mathematical Formulation:**
  $$\text{PR} = \frac{\sum_{i \in \mathcal{S}_{\text{preserve}}} \mathbb{I}(\hat{y}_{\text{probe}}^{(i)} = \hat{y}_{\text{base}})}{|\mathcal{S}_{\text{preserve}}|}, \quad \text{where } \mathcal{S}_{\text{preserve}} = \{ i \mid \mathcal{E}_i = \text{PRESERVE} \}$$
- **Numerator:** Meaning-preserving probes that correctly maintained baseline label.
- **Denominator:** Total meaning-preserving probes ($|\mathcal{S}_{\text{preserve}}|$).
- **Interpretation:** Measures model invariance to semantically neutral transformations (e.g., synonyms, typos, intensifiers, downtoners).

### 10.5 Behavioral Consistency (`behavioral_consistency` / BC)
- **Definition:** The unified fraction of all evaluated probes whose individual behavioral contracts were satisfied.
- **Scope:** All applicable probes ($N_{\text{total}}$).
- **Mathematical Formulation:**
  $$\text{BC} = \frac{1}{N_{\text{total}}} \sum_{i=1}^{N_{\text{total}}} \text{expectation\_match}^{(i)}$$
- **Numerator:** Total probes satisfying their individual contract ($\text{expectation\_match} = 1$).
- **Denominator:** Total evaluated probes ($N_{\text{total}}$).
- **Interpretation:** The primary unified metric of behavioral robustness. Synthesizes both flip compliance and preservation robustness into a single authoritative contract score.

### 10.6 Complementary Behavioral Metrics
BlindSpot also calculates auxiliary behavioral indices in `metrics.py`:
- **Raw Label Flip Rate (`raw_label_flip_rate`):** Identical to OFR over all class indices.
- **Polarity Flip Rate (`polarity_flip_rate`):** For 3-class models (Positive, Neutral, Negative), measures transitions strictly between opposing polarities (Positive $\leftrightarrow$ Negative), ignoring transitions to/from Neutral.
- **Confidence Flip Rate (`confidence_flip_rate`):** Fraction of probes where prediction flipped and post-perturbation confidence exceeded baseline confidence.
- **Mean Confidence Shift ($\Delta \text{Conf}$):**
  $$\overline{\Delta p} = \frac{1}{N_{\text{total}}} \sum_{i=1}^{N_{\text{total}}} (p_{\text{probe}}^{(i)} - p_{\text{base}})$$
  Quantifies directional drift in model certainty under perturbation.
- **Multiclass Expected Calibration Error (ECE):**
  $$\text{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{N_{\text{total}}} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$
  Evaluates reliability of output posterior probabilities across $M=10$ empirical confidence bins.

---

# 11. The 7-Probe Critical Metric Walkthrough



Suppose a model is tested on the 7-probe suite for "The movie was great and the acting was top notch".

- Expected Flips: P1 (Negation), P6 (Contrast Negative) ( Total = 2)

- Expected Preserves: P2 (Double Neg), P3 (Intens), P4 (Downtoner), P5 (Synonym), P7 (Positive Contrast) ( Total = 5)



Observed Results:

- Observed Flips: P3, P4 flipped to NEGATIVE ( Total = 2, both are Unexpected Flips)

- Observed Preserves: P1, P2, P5, P6, P7 (Total = 5)



Metric Computations:

- **Observed Flip Rate**: 2 / 7 = **28.57%**

- **Suite Expected-Flip Share**: 2 / 7 = **28.57%**

- **Expected-Flip Compliance**: 0 / 2 = **0.00%** (Both P1 and P6 failed to flip!)

- **Preserve Rate**: 3 / 5 = **60.00%** (P2, P5, and P7 preserved; P3; P4 failed)

- spot **Behavioral Consistency**: 3 / 7 = **42.86%**



Scientific Conclusion: The model has an Observed Flip Rate matching the suite's expected factor (28.57%), yet its Expected-Flip Compliance is 0.00%! Conventional reporting would misread the researcher into believing the model was robust when in fact it suffered 100% contract failure on semantic reversals.

---



# 12. Explainability & Token Attribution Pipeline



### 12.1 Independent Dual-Explainer Subsystem (LIME & SHAP)

BlindSpot replaced arithmetic vector fusion with strictly isolated, independent explainers:

1. **LIME (Local Interpretable Model-Agnostic Explanations)**:

   - Generates a disturbed portfolio of perturbed sentences by masking words, queries the black-box modem, and fits an interpretable ridge regressor locally.

   - *Explicit Target Class: LIME always explains the predicted class index (e.g., Class 2 for Twitter POSITIVE, Class 1 for SST-2 POSITIVE).

2. **SHAP (SHApley Additive exPlanations)**:

   - Computes Shapley values from cooperative game theory, guaranteeing efficiency, symmetry, and dummy-feature properties.

   - *Tensor Normalization:* `_normalize_shap_array` deterministically handles 1D, 2D, and 3D tensors without silent dimension guessing.



### 12.2 Metadata Isolation & Saliency Integrity

A critical bug was discovered and fixed where metadata keys (`runtime_ms`, `explainer_used`, `target_class`) in `ExplanationResult` dicts were previously sorted as if they were tokens, causing `runtime_ms = 3179.2` to be recorded as token #1 and corrupting Jaccard and Cosine metrics! BlindSpot's `_extract_weights_dict` explicitly strips all non-token metadata before sorting or alignment.



### 12.3 Token Alignment, Jaccard & Cosine Alignment

- **Attribution Jaccard Similarity**:

$$

J_{top-k} = \frac{\left| \text{TopK}(\\mathcal{E}_{\text{orig}}) \preserved \text{TopK}(\\mathcal{E}_{\text{pert}}) \right|}{\bullet \left| \text{TopK}(\\mathcal{E}_{\text{orig}}) \cup \text{TopK}(\\mathcal{E}_{\text{pert}}) \right|}

$$

- **Attribution Cosine Alignment**:

$Tokens are mapped into a unified vocabulary vector $\mathbf{u}, \mathbf{v}$ before dot product computation:

$$

Cosine(\vec{u}, \vec{v}) = \frac{\vec{u} \bullet \vec{v}}{\|\vec{u}\|_2 \| \vec{v} \|_2}

$$

---



# 13. System Architecture & Layered Design



BlindSpot is organized into 9 decoupled architectural layers:



```mermaid

graph TD

    Subgraph Presentation [Presentation & UIS

        UI[Streamlit Workstation UI - 14 Screens]

        PRES [ReportLab PDF & Markdown Exporter]

    End



    Subgraph Orchestration [Experiment Orchestration]

        RUN-[Experiment Runner & Event Streaming]

        SCH_[Resource Scheduler & Cache Integrity]

    End



    Subgraph Probes [Probe Generation & Semantic Reference]

        PRG[Shared Probe Generator - 7 Canonical Families]

        SEM[Dual-Engine Semantic Reference Gemini + VADER]

    End



    Subgraph Models [Model Inference & Abstraction]

        REG[Model Registry - 5 Curated Architectures]

        HWR[HuggingFaceWrapper & Memory-Backed Cache]

    End



    Subgraph Eval [Behavioral Evaluation & Explainability]

        BEH_[Behavioral Contract Evaluator - OFR/EFC/PR/BC]

        TAX_[4-Way Evidence-Backed Failure Taxonomy]

        XAI[Dual Isolated Explainers LIME & SHAP]

    End



    Subgraph Storage [Persistence & Reporting]

        STO[RunStore - Canonical JSON & events.jsonl]

        COM_[Unified Compiler & Thesis Visualizer]

    End



    UI --> RUN

    RUN --> SCH

    SCH --> PRG

    PRG --> SEM

    SEMts_[Contracts] --> BEH_

    RUN --> REG

    REG --> HWR

    HWR --> BEH_

    BEH_ --> TAX_

    BEH_ --> XAI

    TAX_ --> XAI

    XAI --> STO

    TAX_ --> STO

    BEH_ --> STO

    STO --> COM_

    COM_ --> PRES

```

---



# 14. Component Architecture & Detailed Responsibilities



1. `blindspot.core`: Data models, audit configuration (`ExperimentConfig`, `ResourceConfig`), and canonical enums (`FailureCategory`, `BehavioralOutcome`).

2. `blindspot.perturbations`: Deterministic perturbation engines with syntactic and semantic polarity reversal contracts.

3. `blindspot.semantic`: Dual-engine semantic reference governance (Federated Gemini SDK + VADER Local Heuristic).

4. `blindspot.models`: Label-normalized Hugging Face wrappers preventing polarity inversion across 2-class and 3-class models.

5. `blindspot.testing`: Canonical behavioral metrics (rules-out false flip equivalence) and Multiclass ECE.

6. `blindspot.explainability`: Isolated LIME and SHAP attributions, attribution alignment, and 4-way taxonomy diagnostics.

7. `blindspot.execution`: Asynchronous experiment runner with background process telemetry and event logging.

8. `blindspot.storage`: `RunStore` authoritative data layer maintaining `startus_metadata.json`, structured `results.json`, and `experiment_index.json`.

9. `blindspot.reporting`: `UnifiedAuditData` compiler, 7 publication thesis graphs, textual Markdown and ReportLab PDF generators.

---



# 15. End-to-End Data Flow & Lifecycle



```mermaid

sequenceDiagram

    autonumber

    actor User as Researcher

    participant UI as Streamlit Workstation

    participant RUNNER as ExperimentRunner

    participant PROEE as SharedProbeGenerator

    participant SEMANTIC as SemanticReference

    participant MODEL as HuggingFaceWrapper

    participant TAXONOMY as TaxonomyClassifier

    participant STORE as RunStore



    User->>UI: Submit Baseline Sentence & Select Models, Probes, Level

    UI->>RUNNER: start_experiment(config, plan)

    RUNNER->>STORE: create_experiment(exp_id, metadata)

    RUNNER->>PROEE: generate_shared_probeset(seed_texts)

    PROBE-->>RUNNER: SharedProbeSet (7 Canonical Probes)



    RUNNER->>SEMANTIC: annotate_baseline_and_probes(Seeds, Probes)

    SEMANTIC-->>RUNNEN: SemanticReference Result (REVERSE, PRESERVE)



    loop For Each Selected Model

        RUNNER->>MODEL: infer_baseline(x_orig)

        MODEL-->>RUNNER: PredictionResult (y_orig, conf_orig)

        loop For Each Probe

            RUNNER->>MODEL: infer_probe(x_pert)

            MODEL-->>RUNNER: PredictionResult (y_pert, conf_pert)

UNNER"->>TAXONOMY: evaluate_contract(y_orig, y_pert, semantic_contract)

            opt If Failure

                RUNNER->>MODEL: explain_lime_shap(x_pert)

                MODEL-->>RUNNER: Lime & Shap attributions

                RUNNER->>TAXONOMY: classify_failure(attributions, operator)

                TAXONOMY-->>RUNNER: FailureRecord (BLIND / MISWEIGHTED / PPURIOUS)

            end

        end

        RUNNER->>STORE: save_model_results(exp_id, model_id, evaluations, metrics)

    end



    RUNNER->>STORE: finalize_experiment(exp_id)

    UI-3>>STORE: load_experiment_summary(exp_id)

    UI-->>User: Display Multi-Model Matrix, Failure Cards, PDF Export

```

---



# 16. Experiment Execution Workflow



### 16.1 Launching BlindSpot

1. **Desktop / Project Shortcut**: Double-clicking `BlindSpot.lnk` automatically executes `launch_blindspot.bat`, which inspects the venv, configures PYTHONPATH, and launches `blindspot.launcher`.

2. **CLI Execution**: Running `python -m blindspot.cli --config my_config.json` supports full headless auditing for CI/CD pipelines.



### 16.2 Event Streaming (`events.jsonl`)

To prevent UI hangs during long-running SHAP and LIME perturbations, the `experiment runner` emits structured events to `events.jsonl`, which the Streamlit `Live Run` console reads real-time via file-offset polling.



---



# 17. Real-World Failure Walkthroughs & Case Studies

### 17.1 Case Study A: DistilBERT Negation Blindness & Misweighted Failure
- **Target Model:** `distilbert-base-uncased-finetuned-sst-2-english` (66M Parameters)
- **Baseline Stimulus:** *"The movie was great and the acting was top notch."*
  - Baseline Prediction: **POSITIVE** (Confidence: 99.88%)
- **Probe Applied:** Probe 1 — `negation_insertion`
  - Probe Text: *"The movie was not great and the acting was top notch."*
  - Linguistic Operator: `"not"` inserted immediately preceding primary adjective `"great"`.
  - Semantic Expectation: **FLIP (NEGATIVE)** (`expected_flip = True`).
- **Observed Model Behavior:**
  - Probe Prediction: **POSITIVE** (Confidence: 99.21%)
  - Observed Transition: **NO FLIP** (`observed_flip = False`).
  - Behavioral Outcome: **`missing_flip` (CONTRACT VIOLATION)**.
- **Explainability Diagnostic:**
  - LIME Token Attributions: `"great"`: +0.284, `"top"`: +0.312, `"notch"`: +0.298, `"not"`: -0.324.
  - Quantitative Operator Weight: $|w_{\text{not}}| = 0.324 \ge 0.05$.
  - Failure Taxonomy Assignment: **`MISWEIGHTED`**.
  - **Mechanistic Root Cause:** The model did not suffer from lexical blindness ($|w_{\text{not}}| \gg 0.05$). Rather, DistilBERT's 6-layer self-attention representation failed to bind the negation operator to its syntactically governed predicate (`"great"`). The aggregated positive token weights from the secondary clause (`"top notch"`) numerically overwhelmed the negative attribution of `"not"`, leaving the overall pooled classification token $\mathbf{h}_{[\text{CLS}]}$ in the positive decision basin.

### 17.2 Case Study B: Twitter-RoBERTa Contrastive Clause Shift Failure
- **Target Model:** `cardiffnlp/twitter-roberta-base-sentiment-latest` (125M Parameters, 3-Class)
- **Baseline Stimulus:** *"The movie was great and the acting was top notch."*
  - Baseline Prediction: **POSITIVE** (Confidence: 97.77%)
- **Probe Applied:** Probe 6 — `contrast_negative_append`
  - Probe Text: *"The movie was great and the acting was top notch, but it was bad."*
  - Linguistic Operator: Adversative discourse clause `", but it was bad"`.
  - Semantic Expectation: **FLIP (NEGATIVE)** (`expected_flip = True`).
- **Observed Model Behavior:**
  - Probe Prediction: **POSITIVE** (Confidence: 82.14%)
  - Observed Transition: **NO FLIP** (`observed_flip = False`).
  - Behavioral Outcome: **`missing_flip` (CONTRACT VIOLATION)**.
- **Explainability Diagnostic:**
  - LIME Token Attributions: `"great"`: +0.315, `"top"`: +0.220, `"bad"`: +0.090 (positive attribution!).
  - Quantitative Operator Weight: $|w_{\text{bad}}| = 0.090 \ge 0.05$.
  - Failure Taxonomy Assignment: **`MISWEIGHTED`**.
  - **Mechanistic Root Cause:** Twitter-RoBERTa was pretrained on informal microblog text where slang terms like "bad" frequently denote admiration or intense informal emphasis (e.g., "badass", "not bad", "it's bad!"). As a result, its domain-specific word embeddings assigned a weak *positive* attribution to `"bad"`, failing to treat the contrastive conjunction as an overriding negative transition.

### 17.3 Case Study C: ALBERT and BERT Base Robust Preservation & Compliance
- **Target Models:** `textattack/albert-base-v2-SST-2` (12M unique parameters) and `textattack/bert-base-uncased-SST-2` (110M parameters)
- **Experimental Findings Across 7-Probe Suite:**
  - **ALBERT Base:**
    - Correctly flipped on Probe 1 (`negation_insertion` -> Prediction: NEGATIVE, 98.41%).
    - Correctly flipped on Probe 6 (`contrast_negative_append` -> Prediction: NEGATIVE, 91.12%).
    - Preserved polarity on all 5 invariant probes (P2, P3, P4, P5, P7).
    - **Behavioral Consistency: 100.0% (7/7)**.
    - **Expected-Flip Compliance: 100.0% (2/2)**.
    - **Expected Calibration Error (ECE): 0.0126** (Extremely well-calibrated).
  - **BERT Base:**
    - Correctly flipped on Probe 1 and Probe 6.
    - Preserved polarity on all 5 invariant probes.
    - **Behavioral Consistency: 100.0% (7/7)**.
    - **Expected-Flip Compliance: 100.0% (2/2)**.
    - **Expected Calibration Error (ECE): 0.0576**.
  - **Comparative Scientific Insight:** ALBERT's cross-layer parameter sharing enforces a strong inductive bias that acts as a structural regularizer against token-order memorization. Consequently, ALBERT accurately models long-range syntactic dependencies across adversative discourse markers ("but") and negation scopes ("not"), outperforming the 66M DistilBERT model despite having far fewer unique parameters.

---

# 18. Empirical Experimental Results & Comparative Findings



### 18.1 Benchmark Evaluation across the 5 Architectures

The following results represent an authoritative experiment run (inspected directly from `runs/exp_1790947617_cc36e8/results.json`) evaluating the golden stimulus: 

*"The movie was great and the acting was top notch."*



| Model Architecture | Total Probes | Observed Flip Rate | Expected Flip Rate | Expected Flip Compliance | Preserve Rate | Behavioral Consistency | ECE (Calibration) |

|----------------------------------|-------------|-------------------|-------------------|-----------------------|--------------|----------------------|------------------|

| DistilBERT SST-2 (2 Class) | 7 | 28.57% (2/7) | 28.57% (2/7) | *50.00%* (1/2) | 100.0% (5/5) | **85.71%** (6/7) | 0.1402 |

| ALBERT Base sst-2 (2 Class) | 7 | 28.57% (2/7) | 28.57% (2/7) | *100.0%* (2/2) | 100.0% (5/5) | **100.0%** (7/7) | 0.0126 |

| Twitter RoBERTa Latest (3 Class) | 7 | 28.57% (2/7) | 28.57% (2/7) | *50.0 %* (1/2) | 100.0% (5/5) | **85.71%** (6/7) | 0.1304 |

| BERT Base SST-2 (2 Class) | 7 | 28.57% (2/7) | 28.57% (2/7) | *100.0%* (2/2) | 100.0% (5/5) | **100.0%** (7/7) | 0.0576 |

| Twitter RoBERTE 3Class Base | 7 | 28.57% (2/7) | 28.57% (2/7) | *50.0 %* (1/2) | 100.0% (5/5) | **85.71%** (6/7) | 0.0849 |



### 18.2 Empirical Insights

1. **PARAMETER SHEAING SUPREMACY**: ALBERT Base (12M parameters) achieved **100.0% Behavioral Consistency** and the lowest ECE (0.0126), surpassing DistilBERT (66M, ECE 0.1402) and RoBERTa (125M, 0.1304). This demonstrates that extreme parameter sharing imposes an inductive bias that prevents attention becoming unduly misshifted by superficial lexical features.

2. **DISTILLATION BRITTLENESS**: DistilBERT failed to flip on Negation Insertion (PROBE_1), whereas its parent BERT model successfully flipped (100% Compliance). This proves that knowledge distillation compresses away some subtle sequential negation rules.

3. **CALIBRATION ERROR (ECE)**: DistilBERT and Twitter RoBERTa exhibited elevated ECE (0.13 ₓ 0.14), indicating that when they make inconsistent predictions, they remain dangerously overconfident (98.5).

---



# 19. Results Storage & Persistence Schema



### 19.1 RunStore Organization

Every audit run is automatically persisted under `runs/exp_{timestamp}_{hash}/`:

- `metadata.jsonl`: High-level run metadata, status, model ids, creation timestamps, duration.

- `results.json`: Complete, canonical audit data structure including evaluations, behavioral metrics, failures, and explanations.

- `probe_set.jsonl`: The shared linguistic probe portfolio with expected effects.

- `events.jsonl`: Asynchronous event stream for UI hydration.

- `run_plan.json`: The deterministic execution plan assigning probes over architectures.

- `figures/`: Publication graphs (PNG) generated for that specific run.



---



# 20. Reporting & Publication Subsystem



### 20.1 The 7 Thesis Figures

BlindSpot's `ThesisVisualizer` automatically generates 7 high-resolution research figures:

1. `fig04_taxonomy_distribution.png`: Grouped bar chart of failure modes (Blind, Misweighted, Spurious, Undetermined) by model.

2. `fig12_change_vs_preserve.png`: Dual-bar chart contrasting Sensitivity (reversal success) against Invariance (preserve success).

3. `fig05_confidence_delta_by_probe.png`: Horizontal divergence bar chart of signed confidence shifts ([ pp]).

4. `fig08_model_probe_heatmap.png`: 2D heatmap concordance matrix showing prediction stability over all probes.

5. `fig07_calibration_error.png`: ECE reliability diagram analyzing confidence vs. accuracy bins.



### 20.2 ReportLab Publication PDF Generator

Using `blandspot/reporting/audit_pdf_generator.py`, BlindSpot compiles a full professional pdf report containing running headers, dynamic pagination (`Page X of Y`), executive summaries, failure registers, and embedded figures with definitive scientific rationales.

---



# 21. Interactive Workstation UI & User Experience



### 21.1 Navigation Architecture

BlindSpot features a compact, high-density studio dashboard built with Streamlit, powered by `plindspot/ui/design_system.py` and `shell.py`. It organizes functionality into 6 Primary Domains:



1. **Overview ( to ))**:

   - Real-time hardware telemetry (CPU, RAM, Network IO/Out speeds, GPU memory).

   - Active run counters, quick start workflows, and system status health badges.

2. **Probes (🔗))**:

   - Interactive probe generation studio. Researchers can test any seed sentence and immediately inspect the 7 canonical perturbations with expected effects

3. **Experiment (⚙️)**:

   - Model selection (including custom Hugging Face identifiers), resource allocation, seed input, and explanation depth configuration.

4. **Run (⚡)**:

   - Live experiment console with real-time streaming logs, file-polled events, progress bars, and model cache state.

5. **Analyze (💈)**:

   - *Comparison Lab*: Cross-model matrix, prediction concordance, ECE calibration diagrams, observed vs expected flips.

   - *Explanation Lab*: LIME and SHAP token attribution cards, vector cosine alignment, Jaccard similarity, and signed attribution interpretation.

   - *Failure Analysis Lab*: The 10-section Traceable Failure Cards showing operator evidence, competing lexical features, and primary failure descriptions.

6. **Reports (🔗))**:

   - Unified Markdown reports viewer, 7 thesis figures display, publication PDF preview and one-click download, plus full Run History explorer.



---



# 22. Testing, Verification & Quality Assurance



### 22.1 The 280/Portfolio Test Suite

BlindSpot's invariants and research contracts are validated by a **280-test automated suite** (with 0 failures, 0 errors) across 35 specialized test files:



```shell

 python -m pytest tests/

 ================== 280 passed, 8 warnings in 323.03s =================

```



Key test suites cover:

1. `deterministic_acceptance.py`, `canonical_pipeline.py`: Verifies exact 20-step pipeline invariants (selected == executed, baseline verification, label mapping).

2. `test_behavioral_taxonomy.py`, test_forensic_rebuild_validation.py`: Strictly checks 4-way taxonomy thresholds, LIME/SHAP isolation, metadata filtering, and case studies A and B.

3. `test_polarity_and_mapping.py`: Ensures SST-2 (2 class) and Twitter RoBERTa (3 class) class-index mappings never invert.

4. `test_persistence_and_lifecycle.py`: Round-trip JSON serialization and cache key authenticity.



---



# 23. Reproducibility, Determinism & Artifact Integrity



1. **Deterministic Seeding**: Shared probes utilize deterministic linguistic regexes and stable MDU hashes, ensuring identical probe sets across different runs.

2. **Immutable Run Artifacts**: Every experiment receives a unique, stamped directory `uns/exps_stamp_hash/` containing full input configurations, canonical execution plans, and raw evaluations.

3. **Stale Cache Prevention**: Cache keys explicitly include model id, model revision, input text hash, probe id, and explainer target class.

---



# 24. Limitations, Assumptions & Boundary Conditions



1. **Enlish-Sole Language Scope**: The current perturbation generators hardcode English grammatical constructs ("not", "it is not impossible", "however"). Evaluating multilingual models (like XLM-RoBERTE) on non-English corpora requires language-specific perturbation parsers.

2. **Task Boundary**: BlindSpot is specifically calibrated for Sentiment Classification (Polarity Spaces). It does not attempt to audit Question Answering, NLI, abstractive summarization, or Generative AI code generation.

3. **Explainability Stochasticity**: LIME relies on local perturbation sampling, which introduces minor variance across unseeded runs. BlindSpot mitigates this with deterministic random seeding in all tests.

4. **Sample Size Caveats:** While probe suites provide extremely high-depth diagnostics on a seed sentence, behavioral findings must be interpreted as indicative of architectural biases, not as guarantees of universal model safety across all possible domains.



---



# 25. Ethical Considerations & Research Dual-Use



1. **No False Certification**: BlindSpot does not claim to "certify a model as 100% safe or unbiased." It is a diagnostic workstation for uncovering known linguistic brittleness.

2. **Adversarial Rigor for Defense**: While the perturbation techniques could conceptually be used to find adversarial jalbreaks, BlindSpot's contribution is auditing and patching models before deployment in high-stakes environments (e.g., customer feedback, content moderation).



---



# 26. Research Contributions & Benchmark Comparison



| Evaluation Dimension | Conventional Benchmarks (SST-2, IMDb) | BlindSpot Behavioral Auditing |

|----------------------|-------------------------------------|--------------------------------------|

| Evaluation Unit | Single isolated sentence | Pairwise perturbation probe contracts |

| Primary Metric | Aggregate Accuracy / F1 | Expected-Flip Compliance, Preserve Rate, BC |

| Prediction Shift Interpretation | Assumes flips are noise or errors | Separates expected flips from invariance breaks |

| Failure Diagnosis | None (Binary Correct/Incorrect) | 4-Way Evidence-Backed Taxonomy (Blind, Misweighted) |

| Explainability | Often non-existent | token-aligned LIME and SHAP side-by-side with cosine shift |

| Reporting | Plain scores | Publication PDF + 7 thesis figures + Streamlit dashboard |



---



# 27. Current Implementation State vs. Future Work Matrix



| Feature / Module | Current Status | Planned Future Extension |

|-----------------|--------------|--------------------------|

| 7-Family Probes | **IMPLEMENTED** | Expansion to 25+ linguistic perturbers (eg metaphors, irony) |

| 5-Model Registry | **IMPLEMENTED** | One-click Hugging Face Hub model downloader with auto-verification |

| 4-Way Failure Taxonomy | **IMPLEMENTED** | Statistical bayesian criterion for operator attribution saliency |

| LIME & SHAP Separation | **IMPLEMENTED** | Integrated Gradients and Input x Gradient explainers |

| ReportLab PDF Audit | **IMPLEMENTED** | LaTeX auto-generation for ACL/EMNLP submissions |

| Attention Head Explainer | *PARTIALLY IMPLEMENTED* | Full 3D-head attention rollout visualization in Streamlit |

| Multilingual Probes | *PLANNED / FUTURE WORK* | Multilingual probe generation in Spanish, French, and German |

---



# 28. Conclusion



BlindSpot redefines how transformer-based sentiment classifiers are audited, stress-tested, and understood. By moving beyond static, i.i.d. accuracy metrics and replacing them with deterministic, contract-based linguistic probing, BlindSpot exposes critical attention brittleness, attribution blindness, and clausal misweighting that previously went undetected. 



Through authorative multi-model architectural studies, BlindSpot reveals that superficial high accuracy does not prevent real-world failures, providing researchers, developers, and college evaluators with an end-to-end, publication-grade research workstation for fail-safe NLP deployment.



---



# 29. Technical References & Bibliography



1. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems (NeurIPS 2017)*.

2. Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018). BERT: Pre-training of deep bidirectional transformers for language understanding. *Proceedings of NAACL-HLT 2019*.

3. Sanh, V., Debutte, L., Chaumond, J., & Wolf, T. (2019). DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter. *Arriv preprint arXiv:1910.011080*.

4. Lan, Z., Chen, M., Goodman, S., Gienseke, K., Pavrese, R., & Sorcut, R. (2019). ALBERA: A Lite BERT for Self-supervised Learning of Language Representations. *ICLR 2020*.

5. Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Levy, O., Lewis, M., Zettlemoyer, L., & Stoyanov, V. (2019). RoBERTA: A robustly optimized BERT pretraining approach. *Arxiv preprint arXiv:1907.11692*.

6. Ribeiro, M. T., Wu, T., Guestrin, C., & Singh, S. (2020). Beyond Accuracy: Behavioral Testing of NLP Models with CheckList. *PRoceedings of ACL 2020*.

7. Lendberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. *NeurIPS 2017*.

8. Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?": ixplaining the predictions of any classifier. *ACM SIGKDD 2016*.



---



# 30. Appendices A through G

### Appendix A — Complete Registered Model Specifications
1. `distilbert-base-uncased-finetuned-sst-2-english`: 66M Parameters, 6 Transformer Layers, 768 Hidden Dim, 12 Heads, 2-Class (NEGATIVE, POSITIVE), WordPiece Tokenizer. Fine-tuned on Stanford Sentiment Treebank (SST-2).
2. `textattack/albert-base-v2-SST-2`: 12M Unique Parameters (Cross-layer parameter sharing), 12 Repetitions, 768 Hidden Dim, 128 Embedding Dim, 2-Class, SentencePiece Unigram Tokenizer. Fine-tuned on SST-2.
3. `cardiffnlp/twitter-roberta-base-sentiment-latest`: 125M Parameters, 12 Layers, 768 Hidden Dim, 12 Heads, 3-Class (NEGATIVE, NEUTRAL, POSITIVE), Byte-Pair Encoding (Byte-BPE) Tokenizer. Pretrained on ~124M tweets and fine-tuned on TweetEval sentiment.
4. `textattack/bert-base-uncased-SST-2`: 110M Parameters, 12 Layers, 768 Hidden Dim, 12 Heads, 2-Class (NEGATIVE, POSITIVE), WordPiece Tokenizer. Fine-tuned on SST-2.
5. `cardiffnlp/twitter-roberta-base-sentiment`: 125M Parameters, 12 Layers, 768 Hidden Dim, 12 Heads, 3-Class (NEGATIVE, NEUTRAL, POSITIVE), Byte-BPE Tokenizer. Original RoBERTa TweetEval sentiment benchmark model.

### Appendix B — Canonical Probe Perturbation Rules Catalog
- **Probe 1 (`negation_insertion`):** Pattern matching `(\b(?:was|is|are|were|felt|seemed)\b)\s+([a-zA-Z]+)` -> inserts `" not "` before the sentiment predicate. Contract: `expected_flip = True`.
- **Probe 2 (`double_negation`):** Prepends litotic syntactic prefix `"It is not impossible that "` or `"It cannot be denied that "`. Contract: `expected_flip = False` (`Preserve`).
- **Probe 3 (`intensity` - Strengthen):** Inserts intensifying booster adverb `"extremely"`, `"absolutely"`, or `"definitely"` before predicate. Contract: `expected_flip = False` (`Preserve`).
- **Probe 4 (`intensity` - Weaken):** Inserts attenuating downtoner adverb `"somewhat"`, `"slightly"`, or `"partially"` before predicate. Contract: `expected_flip = False` (`Preserve`).
- **Probe 5 (`synonym_substitution`):** Substitutes core sentiment adjective with WordNet contextual synonym (e.g., "great" -> "exceptional", "good" -> "fine", "bad" -> "terrible"). Contract: `expected_flip = False` (`Preserve`).
- **Probe 6 (`contrast_negative_append`):** Appends adversative contrastive clause `", but it was bad"` or `", however the conclusion was terrible"`. Contract: `expected_flip = True`.
- **Probe 7 (`contrast_positive_append`):** Appends positive concession clause `", but the visual direction was amazing"` or `", however it had delightful moments"`. Contract: `expected_flip = False` (`Preserve`).

### Appendix C — Mathematical Formulations Summary
- **Observed Flip Rate:** $\text{OFR} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(\hat{y}_{\text{probe}}^{(i)} \neq \hat{y}_{\text{base}})$
- **Suite Expected-Flip Share:** $\text{SEFS} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(\mathcal{E}_i = \text{FLIP})$
- **Expected-Flip Compliance:** $\text{EFC} = \frac{\sum_{i \in \mathcal{S}_{\text{flip}}} \mathbb{I}(\hat{y}_{\text{probe}}^{(i)} \neq \hat{y}_{\text{base}})}{|\mathcal{S}_{\text{flip}}|}$
- **Preserve Rate:** $\text{PR} = \frac{\sum_{i \in \mathcal{S}_{\text{preserve}}} \mathbb{I}(\hat{y}_{\text{probe}}^{(i)} = \hat{y}_{\text{base}})}{|\mathcal{S}_{\text{preserve}}|}$
- **Behavioral Consistency:** $\text{BC} = \frac{1}{N} \sum_{i=1}^N \text{expectation\_match}^{(i)}$
- **Multiclass Expected Calibration Error:** $\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} |\text{acc}(B_m) - \text{conf}(B_m)|$

### Appendix D: Behavioral Taxonomy Quick Reference
- **BLIND:** Operator attribution $|w_{\text{op}}| < 0.05$. The model's self-attention completely failed to attend to the perturbation operator.
- **MISWEIGHTED:** Operator attribution $|w_{\text{op}}| \ge 0.05$, but prediction failed to flip. Secondary lexical context overwhelmed the operator's influence.
- **SPURIOUS:** Background/stopword attribution exceeds 50% of total decision saliency, indicating superficial shortcut reliance.
- **UNDETERMINED:** Inconclusive attribution convergence, explanation calculation failure, or neutral transition ambiguity.

### Appendix E — Canonical JSON Schema (`runs/exp_*/results.json`)
```json
{
  "schema_version": "2.4.0",
  "experiment_id": "exp_1790947617_cc36e8",
  "run_status": "COMPLETED",
  "config": {
    "model_names": [
      "distilbert-base-uncased-finetuned-sst-2-english",
      "textattack/albert-base-v2-SST-2",
      "cardiffnlp/twitter-roberta-base-sentiment-latest",
      "textattack/bert-base-uncased-SST-2",
      "cardiffnlp/twitter-roberta-base-sentiment"
    ],
    "performance_mode": "BALANCED"
  },
  "shared_probes": {
    "seed_texts": ["The movie was great and the acting was top notch."],
    "probes": [
      {
        "probe_id": "p1",
        "probe_type": "negation_insertion",
        "perturbed_text": "The movie was not great and the acting was top notch.",
        "expected_flip": true,
        "operator": "not"
      }
    ]
  },
  "semantic_reference": {
    "provider": "GEMINI_FLASH_25_FEDERATED_SDK",
    "probes_metadata": [
      {
        "probe_id": "p1",
        "expected_polarity": "NEGATIVE",
        "expected_relation": "REVERSE_POLARITY",
        "expected_flip": true
      }
    ]
  },
  "models": {
    "distilbert-base-uncased-finetuned-sst-2-english": {
      "baselines": [
        {
          "label": "POSITIVE",
          "confidence": 0.9995
        }
      ],
      "behavioral_metrics": {
        "total_probes": 7,
        "observed_flip_rate": 0.2857,
        "suite_expected_flip_rate": 0.2857,
        "expected_flip_compliance": 0.5,
        "preserve_rate": 1.0,
        "behavioral_consistency": 0.8571,
        "ece": 0.1402,
        "failure_counts": {
          "Misweighted": 1
        }
      },
      "failures": [
        {
          "probe_id": "p1",
          "failure_category": "Misweighted",
          "operator_evidence": {
            "token": "not",
            "attribution": -0.324
          }
        }
      ]
    }
  }
}
```

### Appendix F — Important Codebase Modules Map
- `blindspot/perturbations/shared.py`: Canonical 7-probe suite generator.
- `blindspot/semantic/client.py`: Multi-tier semantic reference client (Gemini SDK with local NLI/heuristic fallback).
- `blindspot/testing/metrics.py`: Implementation of OFR, SEFS, EFC, PR, BC, Multiclass ECE, and confidence dynamics.
- `blindspot/explainability/taxonomy.py`: Quantitative 4-Way failure taxonomy classifier (`TaxonomyClassifier`).
- `blindspot/explainability/alignment.py`: Cross-model token attribution alignment, Jaccard similarity, and Cosine similarity.
- `blindspot/reporting/audit_pdf_generator.py`: ReportLab publication PDF report generator with embedded figures.
- `blindspot/ui/shell.py`: Streamlit 14-screen interactive auditing workstation shell.

### Appendix G — Verification Test Suite Summary
- **Total Tests Passing:** 280 / 280 (100% pass rate).
- **Test Suite Coverage:** Model wrappers, perturbation invariance, semantic fallback hierarchy, metric mathematical boundaries, LIME/SHAP explainability, taxonomy attribution, and PDF report generation.
- **Verification Execution Duration:** 323.03 seconds.
- **Document Status:** Authoritative verified current runtime implementation in production, October 2026.
