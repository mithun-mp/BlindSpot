"""
Regression Test Suite for Neutral-Shift Probes and Taxonomy Lineage.
Verifies all 11 required tests specified in Section 8:
- Test 1: Genuine BLIND (POSITIVE -> NEGATIVE, observed POS -> POS, op < 0.05)
- Test 2: Genuine MISWEIGHTED (POSITIVE -> NEGATIVE, observed POS -> POS, op >= 0.05)
- Test 3: Genuine SPURIOUS (Meaning-preserving flip dominated by background features)
- Test 4: Genuine UNDETERMINED: zero evidence (total attribution < 1e-4)
- Test 5: Genuine UNDETERMINED: explainer contradiction (LIME vs SHAP opposite signs >= 0.05)
- Test 6: NEUTRAL preservation (Expected NEU -> NEU, observed NEU -> NEU -> EXPECTED_PRESERVE, NONE)
- Test 7: POSITIVE -> NEUTRAL (Expected POS -> NEU, observed POS -> POS -> MISSING_FLIP)
- Test 8: NEGATIVE -> NEUTRAL (Expected NEG -> NEU, observed NEG -> NEG -> MISSING_FLIP)
- Test 9: NEUTRAL -> POSITIVE (Expected NEU -> POS, observed NEU -> NEU -> MISSING_FLIP)
- Test 10: NEUTRAL -> NEGATIVE (Expected NEU -> NEG, observed NEU -> NEU -> MISSING_FLIP -> MISWEIGHTED if op >= 0.05)
- Test 11: Semantic reference unavailable (Status UNAVAILABLE -> ProbeExpectation UNKNOWN / UNCONSTRAINED)
"""
import unittest

from blindspot.core.config import AttributionThresholds
from blindspot.core.types import (
    BehavioralOutcome,
    FailureCategory,
    SemanticPolarity,
    ExpectationType,
    BehavioralRelation,
    ProbeExpectation,
    SharedProbeSet,
    LinguisticProbe,
    PredictionResult,
)
from blindspot.semantic.types import SemanticReferenceSet, SemanticAnnotation, SemanticRelation
from blindspot.explainability.taxonomy import TaxonomyClassifier
from blindspot.testing.behavioral import classify_behavior, BehavioralTester


class TestNeutralShiftTaxonomyRegression(unittest.TestCase):
    def setUp(self):
        self.thresholds = AttributionThresholds(
            operator_min_abs=0.05,
            competing_dominance_ratio=1.0,
            spurious_stopword_ratio=0.40,
            indeterminate_total_abs=1e-4,
        )
        self.taxonomy = TaxonomyClassifier(thresholds=self.thresholds)

    # -------------------------------------------------------------------------
    # TEST 1: Genuine BLIND
    # -------------------------------------------------------------------------
    def test_01_genuine_blind(self):
        """Expected: POSITIVE -> NEGATIVE. Observed: POS -> POS. Operator < 0.05 in LIME and SHAP."""
        outcome, beh_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.95,
            probe_confidence=0.90,
            expected_effect="EXPECTED_FLIP",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
            target_polarity="NEGATIVE",
        )
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)

        lime_pert = {"token_weights": {"however": 0.012, "terrible": 0.015, "movie": 0.45, "great": 0.50}}
        shap_pert = {"token_weights": {"however": 0.008, "terrible": 0.010, "movie": 0.40, "great": 0.55}}

        diag = self.taxonomy.classify_failure(
            perturbation_type="contrast_negative_append",
            original_sentence="The movie was great.",
            perturbed_sentence="The movie was great, however it was terrible.",
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            is_flipped=False,
            expected_flip=True,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["however"],
            behavioral_outcome=outcome,
            target_polarity="NEGATIVE",
            behavioral_evidence=evidence,
            behavioral_rationale=rationale,
        )
        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.BLIND.value)

    # -------------------------------------------------------------------------
    # TEST 2: Genuine MISWEIGHTED
    # -------------------------------------------------------------------------
    def test_02_genuine_misweighted(self):
        """Expected: POSITIVE -> NEGATIVE. Observed: POS -> POS. Operator >= 0.05."""
        outcome, beh_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.95,
            probe_confidence=0.80,
            expected_effect="EXPECTED_FLIP",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
            target_polarity="NEGATIVE",
        )
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)

        lime_pert = {"token_weights": {"however": 0.12, "terrible": -0.25, "movie": 0.35, "great": 0.45}}
        shap_pert = {"token_weights": {"however": 0.08, "terrible": -0.20, "movie": 0.30, "great": 0.50}}

        diag = self.taxonomy.classify_failure(
            perturbation_type="contrast_negative_append",
            original_sentence="The movie was great.",
            perturbed_sentence="The movie was great, however it was terrible.",
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            is_flipped=False,
            expected_flip=True,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["however"],
            behavioral_outcome=outcome,
            target_polarity="NEGATIVE",
            behavioral_evidence=evidence,
            behavioral_rationale=rationale,
        )
        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.MISWEIGHTED.value)

    # -------------------------------------------------------------------------
    # TEST 3: Genuine SPURIOUS
    # -------------------------------------------------------------------------
    def test_03_genuine_spurious(self):
        """Meaning-preserving probe unexpectedly flips prediction, dominated by stop words."""
        outcome, beh_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.90,
            probe_confidence=0.60,
            expected_effect="EXPECTED_PRESERVE",
            semantic_intent="PRESERVE_POLARITY",
            expected_label_relation="SAME_LABEL",
            target_polarity="POSITIVE",
        )
        self.assertEqual(outcome, BehavioralOutcome.UNEXPECTED_FLIP)

        lime_pert = {"token_weights": {"the": -0.45, "is": -0.30, "film": 0.05, "great": 0.10}}
        shap_pert = {"token_weights": {"the": -0.40, "is": -0.35, "film": 0.02, "great": 0.08}}

        diag = self.taxonomy.classify_failure(
            perturbation_type="intensity",
            original_sentence="The film is great.",
            perturbed_sentence="The film is really great.",
            original_label="POSITIVE",
            perturbed_label="NEGATIVE",
            is_flipped=True,
            expected_flip=False,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["really"],
            behavioral_outcome=outcome,
            target_polarity="POSITIVE",
            behavioral_evidence=evidence,
            behavioral_rationale=rationale,
        )
        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.SPURIOUS.value)

    # -------------------------------------------------------------------------
    # TEST 4: Genuine UNDETERMINED: Zero Evidence
    # -------------------------------------------------------------------------
    def test_04_genuine_undetermined_zero_evidence(self):
        """Total attribution < 1e-4 -> UNDETERMINED."""
        outcome, beh_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.90,
            probe_confidence=0.85,
            expected_effect="EXPECTED_FLIP",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
            target_polarity="NEGATIVE",
        )
        lime_pert = {"token_weights": {"however": 0.00001, "bad": 0.00001}}
        shap_pert = {"token_weights": {"however": 0.00001, "bad": 0.00001}}

        diag = self.taxonomy.classify_failure(
            perturbation_type="contrast_negative_append",
            original_sentence="Good film.",
            perturbed_sentence="Good film, however bad.",
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            is_flipped=False,
            expected_flip=True,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["however"],
            behavioral_outcome=outcome,
            target_polarity="NEGATIVE",
        )
        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.UNDETERMINED.value)

    # -------------------------------------------------------------------------
    # TEST 5: Genuine UNDETERMINED: Explainer Contradiction
    # -------------------------------------------------------------------------
    def test_05_genuine_undetermined_explainer_contradiction(self):
        """LIME and SHAP strongly disagree on operator direction with |w| >= 0.05."""
        outcome, beh_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.90,
            probe_confidence=0.85,
            expected_effect="EXPECTED_FLIP",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
            target_polarity="NEGATIVE",
        )
        lime_pert = {"token_weights": {"not": 0.15, "great": 0.35}}
        shap_pert = {"token_weights": {"not": -0.18, "great": 0.30}}

        diag = self.taxonomy.classify_failure(
            perturbation_type="negation",
            original_sentence="Great movie.",
            perturbed_sentence="Not great movie.",
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            is_flipped=False,
            expected_flip=True,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["not"],
            behavioral_outcome=outcome,
            target_polarity="NEGATIVE",
        )
        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.UNDETERMINED.value)
        self.assertIn("disagree", diag["reason"].lower())

    # -------------------------------------------------------------------------
    # TEST 6: NEUTRAL Preservation
    # -------------------------------------------------------------------------
    def test_06_neutral_preservation(self):
        """Expected: NEUTRAL -> NEUTRAL. Observed: NEU -> NEU -> EXPECTED_PRESERVE, FailureCategory.NONE."""
        outcome, beh_cat, evidence, rationale = classify_behavior(
            original_label="NEUTRAL",
            probe_label="NEUTRAL",
            original_confidence=0.90,
            probe_confidence=0.88,
            expected_effect="EXPECTED_PRESERVE",
            semantic_intent="PRESERVE_POLARITY",
            expected_label_relation="SAME_LABEL",
            target_polarity="NEUTRAL",
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)
        self.assertEqual(beh_cat, FailureCategory.NONE)
        self.assertTrue(evidence["expectation_match"])

        diag = self.taxonomy.classify_failure(
            perturbation_type="synonym_substitution",
            original_sentence="The sun rises in the east.",
            perturbed_sentence="The sun comes up in the east.",
            original_label="NEUTRAL",
            perturbed_label="NEUTRAL",
            is_flipped=False,
            expected_flip=False,
            behavioral_outcome=outcome,
            target_polarity="NEUTRAL",
            behavioral_evidence=evidence,
        )
        self.assertIsNone(diag)

    # -------------------------------------------------------------------------
    # TEST 7: POSITIVE -> NEUTRAL
    # -------------------------------------------------------------------------
    def test_07_positive_to_neutral_missing_flip(self):
        """Expected: POSITIVE -> NEUTRAL. Observed: POS -> POS -> MISSING_FLIP, reaches XAI."""
        outcome, beh_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.92,
            probe_confidence=0.85,
            expected_effect="SHIFT_TO_NEUTRAL",
            semantic_intent="SHIFT_TO_NEUTRAL",
            expected_label_relation="DIFFERENT_LABEL",
            target_polarity="NEUTRAL",
        )
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)
        self.assertFalse(evidence["expectation_match"])

        lime_pert = {"token_weights": {"neutralizer": 0.12, "movie": 0.40, "great": 0.45}}
        shap_pert = {"token_weights": {"neutralizer": 0.09, "movie": 0.35, "great": 0.42}}

        diag = self.taxonomy.classify_failure(
            perturbation_type="neutralization",
            original_sentence="The movie was great.",
            perturbed_sentence="The movie was objectively an average release.",
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            is_flipped=False,
            expected_flip=True,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["neutralizer"],
            behavioral_outcome=outcome,
            target_polarity="NEUTRAL",
            behavioral_evidence=evidence,
        )
        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.MISWEIGHTED.value)

    # -------------------------------------------------------------------------
    # TEST 8: NEGATIVE -> NEUTRAL
    # -------------------------------------------------------------------------
    def test_08_negative_to_neutral_missing_flip(self):
        """Expected: NEGATIVE -> NEUTRAL. Observed: NEG -> NEG -> MISSING_FLIP, reaches XAI."""
        outcome, beh_cat, evidence, rationale = classify_behavior(
            original_label="NEGATIVE",
            probe_label="NEGATIVE",
            original_confidence=0.88,
            probe_confidence=0.82,
            expected_effect="SHIFT_TO_NEUTRAL",
            semantic_intent="SHIFT_TO_NEUTRAL",
            expected_label_relation="DIFFERENT_LABEL",
            target_polarity="NEUTRAL",
        )
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)

        lime_pert = {"token_weights": {"qualifier": 0.08, "bad": -0.35, "film": -0.40}}
        shap_pert = {"token_weights": {"qualifier": 0.07, "bad": -0.30, "film": -0.38}}

        diag = self.taxonomy.classify_failure(
            perturbation_type="neutralization",
            original_sentence="The film was bad.",
            perturbed_sentence="The film was not bad, just average.",
            original_label="NEGATIVE",
            perturbed_label="NEGATIVE",
            is_flipped=False,
            expected_flip=True,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["qualifier"],
            behavioral_outcome=outcome,
            target_polarity="NEUTRAL",
            behavioral_evidence=evidence,
        )
        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.MISWEIGHTED.value)

    # -------------------------------------------------------------------------
    # TEST 9: NEUTRAL -> POSITIVE
    # -------------------------------------------------------------------------
    def test_09_neutral_to_positive_missing_flip(self):
        """Expected: NEUTRAL -> POSITIVE. Observed: NEU -> NEU -> MISSING_FLIP, reaches XAI."""
        outcome, beh_cat, evidence, rationale = classify_behavior(
            original_label="NEUTRAL",
            probe_label="NEUTRAL",
            original_confidence=0.91,
            probe_confidence=0.89,
            expected_effect="SHIFT_FROM_NEUTRAL",
            semantic_intent="SHIFT_FROM_NEUTRAL",
            expected_label_relation="DIFFERENT_LABEL",
            target_polarity="POSITIVE",
        )
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)

        lime_pert = {"token_weights": {"delightful": 0.15, "sun": 0.05, "rises": 0.04}}
        shap_pert = {"token_weights": {"delightful": 0.12, "sun": 0.04, "rises": 0.05}}

        diag = self.taxonomy.classify_failure(
            perturbation_type="contrast_positive_append",
            original_sentence="The sun rises in the east.",
            perturbed_sentence="The sun rises in the east, which was delightful.",
            original_label="NEUTRAL",
            perturbed_label="NEUTRAL",
            is_flipped=False,
            expected_flip=True,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["delightful"],
            behavioral_outcome=outcome,
            target_polarity="POSITIVE",
            behavioral_evidence=evidence,
        )
        self.assertIsNotNone(diag)
        self.assertEqual(diag["category"], FailureCategory.MISWEIGHTED.value)

    # -------------------------------------------------------------------------
    # TEST 10: NEUTRAL -> NEGATIVE
    # -------------------------------------------------------------------------
    def test_10_neutral_to_negative_missing_flip_reaches_misweighted(self):
        """Expected: NEUTRAL -> NEGATIVE. Observed: NEU -> NEU -> MISSING_FLIP. Operator >= 0.05 -> MISWEIGHTED."""
        outcome, beh_cat, evidence, rationale = classify_behavior(
            original_label="NEUTRAL",
            probe_label="NEUTRAL",
            original_confidence=0.91,
            probe_confidence=0.93,
            expected_effect="SHIFT_FROM_NEUTRAL",
            semantic_intent="SHIFT_FROM_NEUTRAL",
            expected_label_relation="DIFFERENT_LABEL",
            target_polarity="NEGATIVE",
        )
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)

        # Real attributions from prb_56f813
        lime_pert = {
            "token_weights": {
                "however": 0.1075,
                "not": -0.0846,
                "rises": 0.0558,
                "west": 0.0438,
                "east": 0.0406,
                "sun": 0.0337,
                "sets": 0.0297,
            }
        }
        shap_pert = {
            "token_weights": {
                "rises": 0.0481,
                "sun": 0.0480,
                "not": -0.0302,
                "however": 0.0016,
            }
        }

        diag = self.taxonomy.classify_failure(
            perturbation_type="contrast_negative_append",
            original_sentence="sun rises in the east and sets in the west",
            perturbed_sentence="sun rises in the east and sets in the west, however it does not rise reliably.",
            original_label="NEUTRAL",
            perturbed_label="NEUTRAL",
            is_flipped=False,
            expected_flip=True,
            lime_pert=lime_pert,
            shap_pert=shap_pert,
            operator_tokens=["however"],
            behavioral_outcome=outcome,
            target_polarity="NEGATIVE",
            behavioral_evidence=evidence,
            behavioral_rationale=rationale,
        )
        self.assertIsNotNone(diag)
        # Must NOT be UNDETERMINED. Operator |0.1075| >= 0.05, outweighed -> MISWEIGHTED.
        self.assertEqual(diag["category"], FailureCategory.MISWEIGHTED.value)
        self.assertIn("however", diag["reason"])

    # -------------------------------------------------------------------------
    # TEST 11: Semantic Reference Unavailable
    # -------------------------------------------------------------------------
    def test_11_semantic_reference_unavailable_does_not_infer_neutral(self):
        """When semantic reference status is UNAVAILABLE, expectations remain UNKNOWN / UNCONSTRAINED."""
        class MockModel:
            model_name = "test-model"
            labels = ["positive", "negative", "neutral"]
            num_classes = 3
            def predict_result(self, text):
                return PredictionResult(label="neutral", confidence=0.85, probabilities={"neutral": 0.85, "positive": 0.10, "negative": 0.05})
            def predict_results_batch(self, texts, batch_size=16):
                return [self.predict_result(t) for t in texts]

        probe = LinguisticProbe(
            probe_id="prb_unavail_01",
            seed_text="Factual text.",
            perturbed_text="Factual text with clause.",
            perturbation_type="contrast",
            description="Factual test probe",
            transformation="append",
            expected_flip=False,
            expected_semantic_effect="UNAVAILABLE",
        )
        probe_set = SharedProbeSet(
            probe_set_id="ps_test",
            seed_texts=["Factual text."],
            probes=[probe],
        )

        # Create semantic reference set with UNAVAILABLE status
        annot = SemanticAnnotation.from_dict({
            "sentence_id": "prb_unavail_01",
            "status": "UNAVAILABLE",
            "semantic_relation_to_baseline": "UNAVAILABLE",
            "final_semantic_polarity": None,
            "semantic_polarity": None,
        })
        probe_set.semantic_reference_set = SemanticReferenceSet(
            baseline_annotation=annot,
            probe_annotations={"prb_unavail_01": annot},
        )

        tester = BehavioralTester(MockModel())
        results = tester.evaluate_shared_probes(probe_set)

        eval_item = results["evaluations"][0]
        # Must remain UNAVAILABLE / UNCONSTRAINED, never infer NEUTRAL or PRESERVE_POLARITY
        self.assertEqual(eval_item.expected_semantic_effect, "UNAVAILABLE")
        self.assertEqual(probe.expectation.expectation_type, ExpectationType.UNKNOWN)
        self.assertEqual(probe.expectation.expected_semantic_relation, BehavioralRelation.UNKNOWN)
        self.assertEqual(probe.expectation.validation_status, "UNAVAILABLE")


if __name__ == "__main__":
    unittest.main()
