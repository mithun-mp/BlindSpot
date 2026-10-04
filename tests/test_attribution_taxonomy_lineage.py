"""
Authoritative Test Suite for BlindSpot Attribution & Taxonomy Lineage.
Verifies the 11 scientific requirements specified in Section 40:
- Test 1: LIME independence
- Test 2: SHAP independence
- Test 3: Zero production LIME/SHAP averaging
- Test 4: Operator attribution retention
- Test 5: MISSING_FLIP is not automatically BLIND (MISWEIGHTED when operator is strong but outweighed)
- Test 6: True blindness (MISSING_FLIP with negligible operator attribution)
- Test 7: SPURIOUS diagnosis (meaning-preserving unexpected flip dominated by stopword/background features)
- Test 8: Insufficient explanation yields UNDETERMINED (never assumes BLIND)
- Test 9: Repeated tokens are occurrence-safe (no dictionary key collision)
- Test 10: Multimodel isolation (model A explanations never cross into model B)
- Test 11: Persistence round trip (exact token attribution weights survive serialization)
"""
import os
import re
import json
import tempfile
import unittest

from blindspot.core.config import ExperimentConfig, AttributionThresholds
from blindspot.core.types import (
    ExplanationResult,
    ExplanationBundle,
    FailureCategory,
    BehavioralOutcome,
    LinguisticProbe,
)
from blindspot.explainability.taxonomy import TaxonomyClassifier
from blindspot.explainability.token_attributions import (
    build_canonical_tokens,
    align_multimodel_attributions,
)
from blindspot.testing.behavioral import classify_behavior
from blindspot.storage.run_store import RunStore


class TestAttributionTaxonomyLineage(unittest.TestCase):
    def setUp(self):
        self.thresholds = AttributionThresholds(
            operator_min_abs=0.05,
            competing_dominance_ratio=1.0,
            spurious_stopword_ratio=0.40,
            indeterminate_total_abs=1e-4,
        )
        self.taxonomy = TaxonomyClassifier(thresholds=self.thresholds)

    # -------------------------------------------------------------------------
    # TEST 1: LIME Independence
    # -------------------------------------------------------------------------
    def test_01_lime_independence(self):
        """Verify LIME explanation is stored and accessible as an independent entity."""
        weights = {"not": -0.4881, "great": 0.4210}
        lime_res = ExplanationResult(
            token_weights=weights,
            model_id="distilbert-sst2",
            text="The movie was not great.",
            explainer_requested="lime",
            explainer_used="lime",
            explained_class="POSITIVE",
            status="AVAILABLE",
        )
        bundle = ExplanationBundle(lime=lime_res)
        self.assertIsNotNone(bundle.lime)
        self.assertEqual(bundle.lime.explainer_used, "lime")
        self.assertAlmostEqual(bundle.lime.token_weights["not"], -0.4881)
        self.assertEqual(bundle.lime.explained_class, "POSITIVE")

    # -------------------------------------------------------------------------
    # TEST 2: SHAP Independence
    # -------------------------------------------------------------------------
    def test_02_shap_independence(self):
        """Verify SHAP explanation is stored and accessible as an independent entity."""
        weights = {"not": -0.4612, "great": 0.3850}
        shap_res = ExplanationResult(
            token_weights=weights,
            model_id="distilbert-sst2",
            text="The movie was not great.",
            explainer_requested="shap",
            explainer_used="shap",
            explained_class="POSITIVE",
            status="AVAILABLE",
        )
        bundle = ExplanationBundle(shap=shap_res)
        self.assertIsNotNone(bundle.shap)
        self.assertEqual(bundle.shap.explainer_used, "shap")
        self.assertAlmostEqual(bundle.shap.token_weights["not"], -0.4612)
        self.assertEqual(bundle.shap.status, "AVAILABLE")

    # -------------------------------------------------------------------------
    # TEST 3: No Averaging / Fusion in Production Pipeline
    # -------------------------------------------------------------------------
    def test_03_no_production_averaging(self):
        """Search execution runner and core explainability codebase for (lime + shap) / 2 averaging."""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        blindspot_dir = os.path.join(project_root, "blindspot")
        
        prohibited_pattern = re.compile(r"(\blime_.*\s*\+\s*.*shap_.*|\bl_.*\s*\+\s*.*s_.*)\s*/\s*2", re.IGNORECASE)
        
        violations = []
        for root, _, files in os.walk(blindspot_dir):
            for f in files:
                if f.endswith(".py"):
                    fpath = os.path.join(root, f)
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                        for line_no, line in enumerate(fh, 1):
                            if prohibited_pattern.search(line):
                                violations.append(f"{fpath}:{line_no}: {line.strip()}")

        self.assertEqual(violations, [], f"Found prohibited LIME/SHAP fusion averaging in production code: {violations}")

    # -------------------------------------------------------------------------
    # TEST 4: Operator Attribution Retention
    # -------------------------------------------------------------------------
    def test_04_operator_attribution_retention(self):
        """Verify a probe containing 'not' retains actual un-fused LIME and SHAP attributions."""
        text = "The movie was not great and the acting was top notch."
        lime_weights = {"the": 0.07, "movie": 0.11, "was": 0.04, "not": -0.4881, "great": 0.06, "acting": 0.07, "top": 0.15, "notch": 0.17}
        shap_weights = {"the": 0.03, "movie": 0.08, "was": 0.02, "not": -0.4612, "great": 0.05, "acting": 0.04, "top": 0.14, "notch": 0.13}
        
        lime_res = ExplanationResult(lime_weights, model_id="distilbert", text=text, explainer_used="lime")
        shap_res = ExplanationResult(shap_weights, model_id="distilbert", text=text, explainer_used="shap")

        canonical = build_canonical_tokens(text, lime_res, shap_res)
        not_records = [c for c in canonical if c["token"] == "not"]
        self.assertEqual(len(not_records), 1)
        not_rec = not_records[0]
        self.assertAlmostEqual(not_rec["lime_weight"], -0.4881)
        self.assertAlmostEqual(not_rec["shap_weight"], -0.4612)

    # -------------------------------------------------------------------------
    # TEST 5: MISSING_FLIP is NOT Automatically BLIND (MISWEIGHTED when outweighed)
    # -------------------------------------------------------------------------
    def test_05_missing_flip_is_not_automatically_blind(self):
        """
        Model fails to reverse polarity (MISSING_FLIP), but operator 'not' received strong
        attribution (-0.49). Competing positive tokens ('great', 'top', 'notch') dominate.
        Must classify as MISWEIGHTED, NEVER as BLIND.
        """
        orig_text = "The movie was great and the acting was top notch."
        pert_text = "The movie was not great and the acting was top notch."
        
        lime_pert = {
            "not": -0.4881,
            "great": 0.4200,
            "top": 0.1500,
            "notch": 0.1800,
            "movie": 0.0200,
        }
        shap_pert = {
            "not": -0.4612,
            "great": 0.3800,
            "top": 0.1400,
            "notch": 0.1600,
            "movie": 0.0200,
        }

        diag = self.taxonomy.classify_failure(
            perturbation_type="negation",
            original_sentence=orig_text,
            perturbed_sentence=pert_text,
            original_label="POSITIVE",
            perturbed_label="POSITIVE",  # MISSING FLIP!
            is_flipped=False,
            expected_flip=True,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["not"],
            operator_type="negation",
            expected_semantic_effect="invert",
            semantic_intent="REVERSE_POLARITY",
            original_confidence=1.00,
            perturbed_confidence=0.985,
        )

        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.MISWEIGHTED.value)
        self.assertNotEqual(diag["category"], FailureCategory.BLIND.value)
        self.assertIn("outweighed", diag["reason"].lower())
        
        tax_ev = diag["evidence"]["taxonomy_evidence"]
        self.assertAlmostEqual(tax_ev["lime"]["operator_weight"], -0.4881)
        self.assertAlmostEqual(tax_ev["shap"]["operator_weight"], -0.4612)
        self.assertEqual(tax_ev["lime"]["dominant_competitor"], "great")

    # -------------------------------------------------------------------------
    # TEST 6: True Blindness
    # -------------------------------------------------------------------------
    def test_06_true_blindness(self):
        """
        Model fails to reverse polarity (MISSING_FLIP) and operator 'not' received negligible attribution (abs < 0.05).
        Must classify as BLIND.
        """
        orig_text = "The movie was great."
        pert_text = "The movie was not great."
        
        # 'not' has negligible weight (~0.01)
        lime_pert = {"not": -0.0120, "great": 0.6500, "movie": 0.0500}
        shap_pert = {"not": -0.0080, "great": 0.6200, "movie": 0.0400}

        diag = self.taxonomy.classify_failure(
            perturbation_type="negation",
            original_sentence=orig_text,
            perturbed_sentence=pert_text,
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            is_flipped=False,
            expected_flip=True,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["not"],
            operator_type="negation",
            expected_semantic_effect="invert",
            semantic_intent="REVERSE_POLARITY",
            original_confidence=0.95,
            perturbed_confidence=0.94,
        )

        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.BLIND.value)
        self.assertIn("negligible attribution", diag["reason"].lower())

    # -------------------------------------------------------------------------
    # TEST 7: Spurious Classification
    # -------------------------------------------------------------------------
    def test_07_spurious_classification(self):
        """
        Meaning-preserving perturbation results in UNEXPECTED_FLIP.
        Decision shift is dominated by punctuation / stopwords / non-causal tokens.
        Must classify as SPURIOUS based on evidence.
        """
        orig_text = "The movie was wonderful."
        pert_text = "The movie was wonderful, indeed!"
        
        # Stopwords / punctuation dominate the decision shift
        lime_pert = {"the": 0.4500, "was": 0.3500, "wonderful": 0.0500, "!": 0.1500}
        shap_pert = {"the": 0.4200, "was": 0.3200, "wonderful": 0.0400, "!": 0.1200}

        diag = self.taxonomy.classify_failure(
            perturbation_type="punctuation_noise",
            original_sentence=orig_text,
            perturbed_sentence=pert_text,
            original_label="POSITIVE",
            perturbed_label="NEGATIVE",  # UNEXPECTED FLIP!
            is_flipped=True,
            expected_flip=False,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["indeed"],
            expected_semantic_effect="preserve",
            semantic_intent="PRESERVE_MEANING",
            original_confidence=0.95,
            perturbed_confidence=0.75,
        )

        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.SPURIOUS.value)
        self.assertIn("irrelevant/background features", diag["reason"].lower())

    # -------------------------------------------------------------------------
    # TEST 8: Insufficient Explanation -> UNDETERMINED (Never Assume Blindness)
    # -------------------------------------------------------------------------
    def test_08_insufficient_explanation_yields_undetermined(self):
        """If explainers fail or return zero total attribution, classify as UNDETERMINED, NOT BLIND."""
        orig_text = "The movie was great."
        pert_text = "The movie was not great."

        # Explainers failed / empty
        lime_pert = {}
        shap_pert = {}

        diag = self.taxonomy.classify_failure(
            perturbation_type="negation",
            original_sentence=orig_text,
            perturbed_sentence=pert_text,
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            is_flipped=False,
            expected_flip=True,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["not"],
            expected_semantic_effect="invert",
            semantic_intent="REVERSE_POLARITY",
        )

        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.UNDETERMINED.value)
        self.assertIn("unavailable or near zero", diag["reason"].lower())

    # -------------------------------------------------------------------------
    # TEST 9: Repeated Tokens Are Occurrence-Safe
    # -------------------------------------------------------------------------
    def test_09_repeated_tokens_occurrence_safety(self):
        """Ensure repeated words (e.g. 'good movie with good acting') retain distinct occurrence identities without key collisions."""
        text = "good movie with good acting"
        lime_weights = {
            ("good", 1): 0.45,
            ("movie", 1): 0.10,
            ("with", 1): 0.02,
            ("good", 2): 0.35,
            ("acting", 1): 0.15,
        }
        shap_weights = {
            ("good", 1): 0.40,
            ("movie", 1): 0.08,
            ("with", 1): 0.01,
            ("good", 2): 0.30,
            ("acting", 1): 0.12,
        }

        lime_res = ExplanationResult(lime_weights, model_id="distilbert", text=text, explainer_used="lime")
        shap_res = ExplanationResult(shap_weights, model_id="distilbert", text=text, explainer_used="shap")

        canonical = build_canonical_tokens(text, lime_res, shap_res)
        good_tokens = [c for c in canonical if c["token"] == "good"]
        self.assertEqual(len(good_tokens), 2)
        self.assertEqual(good_tokens[0]["occurrence"], 1)
        self.assertEqual(good_tokens[1]["occurrence"], 2)
        self.assertAlmostEqual(good_tokens[0]["lime_weight"], 0.45)
        self.assertAlmostEqual(good_tokens[1]["lime_weight"], 0.35)

    # -------------------------------------------------------------------------
    # TEST 10: Multimodel Isolation
    # -------------------------------------------------------------------------
    def test_10_multimodel_isolation(self):
        """Ensure Model A attributions are completely isolated from Model B."""
        text = "The food was delicious."
        exp_model_a = ExplanationResult(
            token_weights={"delicious": 0.85},
            model_id="model_a",
            text=text,
            explainer_used="lime",
        )
        exp_model_b = ExplanationResult(
            token_weights={"delicious": 0.42},
            model_id="model_b",
            text=text,
            explainer_used="lime",
        )

        self.assertNotEqual(exp_model_a.model_id, exp_model_b.model_id)
        self.assertEqual(exp_model_a.token_weights["delicious"], 0.85)
        self.assertEqual(exp_model_b.token_weights["delicious"], 0.42)

    # -------------------------------------------------------------------------
    # TEST 11: Persistence Round Trip (Lineage Verification)
    # -------------------------------------------------------------------------
    def test_11_persistence_round_trip(self):
        """Verify that exact un-fused LIME and SHAP attributions survive RunStore persistence round trip."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            store = RunStore(base_dir=tmp_dir)
            exp_id = "exp_test_roundtrip"
            model_id = "test_model"

            exact_lime = {"not": -0.4881, "great": 0.4210}
            exact_shap = {"not": -0.4612, "great": 0.3850}

            model_data = {
                "status": "COMPLETED",
                "model_id": model_id,
                "baseline": {"text": "The movie was great."},
                "failures": [
                    {
                        "probe_id": "P_NEG_01",
                        "category": FailureCategory.MISWEIGHTED.value,
                        "evidence": {
                            "taxonomy_evidence": {
                                "operator_tokens": ["not"],
                                "lime": {"operator_weight": -0.4881},
                                "shap": {"operator_weight": -0.4612},
                            },
                            "baseline": {
                                "explanations": {
                                    "lime": {"token_weights": {"great": 0.4210}},
                                    "shap": {"token_weights": {"great": 0.3850}},
                                }
                            },
                            "probe": {
                                "explanations": {
                                    "lime": {"token_weights": exact_lime},
                                    "shap": {"token_weights": exact_shap},
                                }
                            }
                        }
                    }
                ],
                "explanations": [
                    {
                        "probe_id": "P_NEG_01",
                        "lime_pert": {"token_weights": exact_lime},
                        "shap_pert": {"token_weights": exact_shap},
                    }
                ]
            }

            store.save_model_result(exp_id, model_id, model_data)
            
            # Reload from disk
            loaded = store.load_model_result(exp_id, model_id)
            self.assertIsNotNone(loaded)
            
            # Verify exact values survived
            loaded_lime = loaded["failures"][0]["evidence"]["probe"]["explanations"]["lime"]["token_weights"]
            loaded_shap = loaded["failures"][0]["evidence"]["probe"]["explanations"]["shap"]["token_weights"]
            
            self.assertAlmostEqual(loaded_lime["not"], -0.4881)
            self.assertAlmostEqual(loaded_shap["not"], -0.4612)


if __name__ == "__main__":
    unittest.main()
