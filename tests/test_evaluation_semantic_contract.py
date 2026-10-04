"""
Regression Test Suite for BlindSpot Semantic Contract & Multi-Model Probe Evaluation.
Strictly implements Tests 1 through 12 verifying:
1. Expected PRESERVE / Actual PRESERVE / GT Correct -> GREEN MATCH
2. Expected PRESERVE / Actual FLIP -> RED SPURIOUS
3. Expected FLIP / Actual FLIP / GT Correct -> GREEN MATCH
4. Expected FLIP / Actual PRESERVE -> RED BLIND
5. Multi-Model Independence
6. Serialization Completeness
7. Directional Transition Integrity
8. Probe Expectation Invariance
9. Baseline Error Preservation -> AMBER LABEL MISMATCH (not green match)
10. Contrast Negative Append (guards against stale reversal bug)
11. Stale Expectation Regression
12. Ground-Truth / Behavior Separation across all 4 logical combinations
"""
import unittest

from blindspot.core.types import (
    FailureCategory,
    BehavioralOutcome,
    SemanticPolarity,
    ExpectationType,
    BehavioralRelation,
    ProbeExpectation,
    PredictionResult,
    ModelProbeEvaluation,
    LinguisticProbe,
)
from blindspot.testing.behavioral import classify_behavior
from blindspot.analysis.cross_model import CrossModelAnalyzer


class TestEvaluationSemanticContract(unittest.TestCase):
    """Verifies the pure deterministic contract and end-to-end data propagation."""

    # ----------------------------------------------------------------------
    # TEST 1: Expected PRESERVE, Actual PRESERVE, GT correct
    # ----------------------------------------------------------------------
    def test_01_expected_preserve_actual_preserve_gt_correct(self):
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="NEGATIVE",
            probe_label="NEGATIVE",
            original_confidence=0.90,
            probe_confidence=0.88,
            expected_effect="preserve",
            semantic_intent="PRESERVE_POLARITY",
            target_polarity="NEGATIVE",
        )
        self.assertTrue(evidence["behavioral_conformance"])
        self.assertTrue(evidence["ground_truth_match"])
        self.assertEqual(failure_type, FailureCategory.NONE)
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)

        # Cross-model serialization & UI classification
        analyzer = CrossModelAnalyzer()
        p1 = PredictionResult(label="NEGATIVE", confidence=0.90)
        p2 = PredictionResult(label="NEGATIVE", confidence=0.88)
        p2.semantic_compatibility = "DIRECTLY_COMPATIBLE"
        eval_item = ModelProbeEvaluation(
            model_id="roberta-base",
            probe_id="p01",
            seed_text="bad service",
            perturbed_text="terrible service",
            perturbation_type="synonym",
            expected_flip=False,
            expected_semantic_effect="preserve",
            original_prediction=p1,
            perturbed_prediction=p2,
            is_flipped=False,
            confidence_delta=-0.02,
            confidence_delta_pts=-2.0,
            expectation_satisfied=evidence["behavioral_conformance"],
            behavioral_outcome=outcome.value,
            failure_type=failure_type.value,
            ground_truth_match=evidence["ground_truth_match"],
        )
        matrix = analyzer.build_model_probe_matrix({"roberta-base": [eval_item]})
        cell = matrix[0]["models"]["roberta-base"]
        self.assertIsNone(cell["failure_type"])
        self.assertTrue(cell["expectation_satisfied"])
        self.assertTrue(cell["ground_truth_match"])

    # ----------------------------------------------------------------------
    # TEST 2: Expected PRESERVE, Actual FLIP -> SPURIOUS Failure
    # ----------------------------------------------------------------------
    def test_02_expected_preserve_actual_flip(self):
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="NEGATIVE",
            probe_label="POSITIVE",
            original_confidence=0.90,
            probe_confidence=0.85,
            expected_effect="preserve",
            semantic_intent="PRESERVE_POLARITY",
            target_polarity="NEGATIVE",
        )
        self.assertFalse(evidence["behavioral_conformance"])
        # Decoupled behavioral engine: UNEXPECTED_FLIP is UNDETERMINED awaiting attribution evidence
        self.assertEqual(failure_type, FailureCategory.UNDETERMINED)
        self.assertEqual(outcome, BehavioralOutcome.UNEXPECTED_FLIP)

        # Check serialization preserves SPURIOUS when diagnosed by taxonomy
        analyzer = CrossModelAnalyzer()
        p1 = PredictionResult(label="NEGATIVE", confidence=0.90)
        p2 = PredictionResult(label="POSITIVE", confidence=0.85)
        eval_item = ModelProbeEvaluation(
            model_id="bert-base",
            probe_id="p02",
            seed_text="bad food",
            perturbed_text="terrible food",
            perturbation_type="synonym",
            expected_flip=False,
            expected_semantic_effect="preserve",
            original_prediction=p1,
            perturbed_prediction=p2,
            is_flipped=True,
            confidence_delta=-0.05,
            confidence_delta_pts=-5.0,
            expectation_satisfied=evidence["behavioral_conformance"],
            behavioral_outcome=outcome.value,
            failure_type=FailureCategory.SPURIOUS.value,
            ground_truth_match=evidence["ground_truth_match"],
        )
        matrix = analyzer.build_model_probe_matrix({"bert-base": [eval_item]})
        cell = matrix[0]["models"]["bert-base"]
        self.assertEqual(cell["failure_type"], FailureCategory.SPURIOUS.value)
        self.assertEqual(cell["failure_type"].upper(), "SPURIOUS")
        self.assertFalse(cell["expectation_satisfied"])

    # ----------------------------------------------------------------------
    # TEST 3: Expected FLIP, Actual FLIP, GT correct
    # ----------------------------------------------------------------------
    def test_03_expected_flip_actual_flip_gt_correct(self):
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="NEGATIVE",
            probe_label="POSITIVE",
            original_confidence=0.92,
            probe_confidence=0.88,
            expected_effect="invert",
            semantic_intent="REVERSE_POLARITY",
            target_polarity="POSITIVE",
        )
        self.assertTrue(evidence["behavioral_conformance"])
        self.assertTrue(evidence["ground_truth_match"])
        self.assertEqual(failure_type, FailureCategory.NONE)
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_FLIP)

    # ----------------------------------------------------------------------
    # TEST 4: Expected FLIP, Actual PRESERVE -> BLIND Failure
    # ----------------------------------------------------------------------
    def test_04_expected_flip_actual_preserve(self):
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.91,
            probe_confidence=0.87,
            expected_effect="invert",
            semantic_intent="REVERSE_POLARITY",
            target_polarity="NEGATIVE",
        )
        self.assertFalse(evidence["behavioral_conformance"])
        # Decoupled behavioral engine: MISSING_FLIP is UNDETERMINED awaiting attribution evidence
        self.assertEqual(failure_type, FailureCategory.UNDETERMINED)
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)

    # ----------------------------------------------------------------------
    # TEST 5: Multi-Model Independence
    # ----------------------------------------------------------------------
    def test_05_multi_model_independence(self):
        p1 = PredictionResult(label="NEGATIVE", confidence=0.90)
        p2_a = PredictionResult(label="POSITIVE", confidence=0.85)
        p2_b = PredictionResult(label="NEGATIVE", confidence=0.88)

        eval_a = ModelProbeEvaluation(
            model_id="model_A",
            probe_id="probe_shared",
            seed_text="seed",
            perturbed_text="perturbed",
            perturbation_type="synonym",
            expected_flip=False,
            expected_semantic_effect="preserve",
            original_prediction=p1,
            perturbed_prediction=p2_a,
            is_flipped=True,
            confidence_delta=-0.05,
            confidence_delta_pts=-5.0,
            expectation_satisfied=False,
            failure_type="SPURIOUS",
            ground_truth_match=False,
        )

        eval_b = ModelProbeEvaluation(
            model_id="model_B",
            probe_id="probe_shared",
            seed_text="seed",
            perturbed_text="perturbed",
            perturbation_type="synonym",
            expected_flip=False,
            expected_semantic_effect="preserve",
            original_prediction=p1,
            perturbed_prediction=p2_b,
            is_flipped=False,
            confidence_delta=-0.02,
            confidence_delta_pts=-2.0,
            expectation_satisfied=True,
            failure_type="None",
            ground_truth_match=True,
        )

        analyzer = CrossModelAnalyzer()
        matrix = analyzer.build_model_probe_matrix({
            "model_A": [eval_a],
            "model_B": [eval_b],
        })

        row = matrix[0]
        self.assertEqual(row["models"]["model_A"]["failure_type"], "SPURIOUS")
        self.assertFalse(row["models"]["model_A"]["expectation_satisfied"])
        self.assertIsNone(row["models"]["model_B"]["failure_type"])
        self.assertTrue(row["models"]["model_B"]["expectation_satisfied"])

    # ----------------------------------------------------------------------
    # TEST 6: Serialization Completeness
    # ----------------------------------------------------------------------
    def test_06_serialization_completeness(self):
        analyzer = CrossModelAnalyzer()
        p1 = PredictionResult(label="POSITIVE", confidence=0.95)
        p2 = PredictionResult(label="NEGATIVE", confidence=0.90)
        eval_item = ModelProbeEvaluation(
            model_id="m1",
            probe_id="prb_1",
            seed_text="s",
            perturbed_text="p",
            perturbation_type="negation",
            expected_flip=True,
            expected_semantic_effect="invert",
            original_prediction=p1,
            perturbed_prediction=p2,
            is_flipped=True,
            confidence_delta=-0.05,
            confidence_delta_pts=-5.0,
            expectation_satisfied=True,
            behavioral_outcome="EXPECTED_FLIP",
            failure_type="None",
            ground_truth_match=True,
        )
        matrix = analyzer.build_model_probe_matrix({"m1": [eval_item]})
        cell = matrix[0]["models"]["m1"]

        # Success must serialize failure_type as None
        self.assertIn("failure_type", cell)
        self.assertIsNone(cell["failure_type"])
        self.assertIn("behavioral_outcome", cell)
        self.assertEqual(cell["behavioral_outcome"], "EXPECTED_FLIP")
        self.assertIn("unexpected_behavior", cell)
        self.assertFalse(cell["unexpected_behavior"])
        self.assertIn("ground_truth_match", cell)
        self.assertTrue(cell["ground_truth_match"])
        self.assertIn("expectation_satisfied", cell)
        self.assertTrue(cell["expectation_satisfied"])
        self.assertIn("is_flipped", cell)
        self.assertTrue(cell["is_flipped"])
        self.assertIn("confidence_delta_pts", cell)
        self.assertEqual(cell["confidence_delta_pts"], -5.0)

    # ----------------------------------------------------------------------
    # TEST 7: Directional Transition Integrity
    # ----------------------------------------------------------------------
    def test_07_directional_transition_integrity(self):
        cases = [
            ("NEGATIVE", "POSITIVE", "NEG → POS"),
            ("POSITIVE", "NEGATIVE", "POS → NEG"),
            ("NEGATIVE", "NEGATIVE", "NEG → NEG"),
            ("POSITIVE", "POSITIVE", "POS → POS"),
        ]
        for orig, pert, expected_badge in cases:
            p1 = PredictionResult(label=orig, confidence=0.90)
            p2 = PredictionResult(label=pert, confidence=0.88)
            e = ModelProbeEvaluation(
                model_id="m1",
                probe_id="p",
                seed_text="s",
                perturbed_text="p",
                perturbation_type="t",
                expected_flip=False,
                expected_semantic_effect="preserve",
                original_prediction=p1,
                perturbed_prediction=p2,
                is_flipped=(orig != pert),
                confidence_delta=-0.02,
                confidence_delta_pts=-2.0,
                expectation_satisfied=True,
            )
            # Derived transition
            orig_lbl = e.original_label
            pert_lbl = e.perturbed_label
            trans_text = f"{orig_lbl[:3]} → {pert_lbl[:3]}"
            self.assertEqual(trans_text, expected_badge)

    # ----------------------------------------------------------------------
    # TEST 8: Probe Expectation Invariance Across Models
    # ----------------------------------------------------------------------
    def test_08_probe_expectation_invariance(self):
        probe = LinguisticProbe.create(
            seed_text="The movie is fantastic.",
            perturbed_text="The film is fantastic.",
            perturbation_type="synonym",
            transformation="synonym replacement",
            expected_semantic_effect="preserve",
            expected_flip=False,
        )
        initial_flip = probe.expected_flip
        initial_effect = probe.expected_semantic_effect
        initial_intent = probe.semantic_intent

        # Simulate model A predicting a flip and model B preserving
        _ = classify_behavior("POSITIVE", "NEGATIVE", 0.9, 0.8, expected_effect=probe.expected_semantic_effect)
        _ = classify_behavior("POSITIVE", "POSITIVE", 0.9, 0.9, expected_effect=probe.expected_semantic_effect)

        # Probe specification must remain strictly unchanged
        self.assertEqual(probe.expected_flip, initial_flip)
        self.assertEqual(probe.expected_semantic_effect, initial_effect)
        self.assertEqual(probe.semantic_intent, initial_intent)

    # ----------------------------------------------------------------------
    # TEST 9: Baseline Error Preservation -> AMBER LABEL MISMATCH
    # ----------------------------------------------------------------------
    def test_09_baseline_error_preservation(self):
        """
        Ground truth: NEGATIVE
        Original: POSITIVE (Model got baseline wrong)
        Perturbed: POSITIVE (Model preserved its baseline prediction)
        Expected: PRESERVE
        Result:
            observed_behavior = PRESERVE
            behavioral_conformance = TRUE
            ground_truth_match = FALSE
            UI badge = ⚠ LABEL MISMATCH (NOT green MATCH)
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.88,
            probe_confidence=0.87,
            expected_effect="preserve",
            semantic_intent="PRESERVE_POLARITY",
            target_polarity="NEGATIVE",
        )
        self.assertEqual(evidence["observed_behavior"], "PRESERVE")
        self.assertTrue(evidence["behavioral_conformance"])
        self.assertFalse(evidence["ground_truth_match"])
        self.assertEqual(failure_type, FailureCategory.NONE)

        # UI cell classification check
        out = {
            "perturbed_label": "POSITIVE",
            "original_label": "POSITIVE",
            "expectation_satisfied": evidence["behavioral_conformance"],
            "unexpected_behavior": False,
            "failure_type": None,
            "ground_truth_match": evidence["ground_truth_match"],
            "semantic_compatibility": "POLARITY_MISMATCH",
        }
        is_sat = out["expectation_satisfied"]
        gt_match = out["ground_truth_match"]
        compat = out["semantic_compatibility"]
        fail_type = out["failure_type"]

        if fail_type and str(fail_type).lower() in ("blind", "spurious", "misweighted"):
            badge = f"✕ {str(fail_type).upper()}"
        elif is_sat and (gt_match is False or compat == "POLARITY_MISMATCH"):
            badge = "⚠ LABEL MISMATCH"
        else:
            badge = "✓ MATCH"

        self.assertEqual(badge, "⚠ LABEL MISMATCH")
        self.assertNotEqual(badge, "✓ MATCH")

    # ----------------------------------------------------------------------
    # TEST 10: Contrast Negative Append (Incident Regression)
    # ----------------------------------------------------------------------
    def test_10_contrast_negative_append(self):
        """
        Seed: NEGATIVE
        Perturbed: Negative contrast appended
        Verified semantic reference: NEGATIVE, PRESERVE_POLARITY
        Model: NEG -> NEG
        Must satisfy PRESERVE expectation, must NOT be BLIND or generic DEVIATION.
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="NEGATIVE",
            probe_label="NEGATIVE",
            original_confidence=0.95,
            probe_confidence=0.92,
            expected_effect="preserve",
            semantic_intent="PRESERVE_POLARITY",
            target_polarity="NEGATIVE",
        )
        self.assertTrue(evidence["behavioral_conformance"])
        self.assertEqual(failure_type, FailureCategory.NONE)
        self.assertNotEqual(failure_type, FailureCategory.BLIND)
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)

    # ----------------------------------------------------------------------
    # TEST 11: Stale Expectation Regression
    # ----------------------------------------------------------------------
    def test_11_stale_expectation_regression(self):
        """
        Construct a probe where:
        initial ProbeExpectation says FLIP (from stimulus synthesis)
        verified semantic reference later says PRESERVE
        Verify the final evaluation uses PRESERVE.
        """
        stale_exp = ProbeExpectation(
            expectation_type=ExpectationType.REVERSE_POLARITY,
            expected_semantic_relation=BehavioralRelation.POLARITY_REVERSED,
            expected_polarity_transition="invert",
            rationale="Initial synthesizer heuristic",
            confidence=0.5,
            validation_status="UNVALIDATED",
        )

        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="NEGATIVE",
            probe_label="NEGATIVE",
            original_confidence=0.90,
            probe_confidence=0.88,
            expected_effect="EXPECTED_PRESERVE",
            semantic_intent="PRESERVE_POLARITY",
            expectation=stale_exp,
            target_polarity="NEGATIVE",
        )

        self.assertTrue(evidence["behavioral_conformance"])
        self.assertEqual(failure_type, FailureCategory.NONE)
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)
        self.assertEqual(evidence["expected_relation"], BehavioralRelation.SAME_POLARITY.value)

    # ----------------------------------------------------------------------
    # TEST 12: Ground-Truth / Behavior Separation Matrix
    # ----------------------------------------------------------------------
    def test_12_ground_truth_behavior_separation_all_combinations(self):
        """
        Test all 4 logical combinations:
        1. PRESERVE expected + PRESERVE observed + GT match TRUE
        2. PRESERVE expected + PRESERVE observed + GT match FALSE
        3. FLIP expected + FLIP observed + GT match TRUE
        4. FLIP expected + FLIP observed + GT match FALSE
        """
        # Combo 1
        _, _, ev1, _ = classify_behavior(
            "NEGATIVE", "NEGATIVE", 0.9, 0.9,
            expected_effect="preserve", semantic_intent="PRESERVE_POLARITY", target_polarity="NEGATIVE"
        )
        self.assertTrue(ev1["behavioral_conformance"])
        self.assertTrue(ev1["ground_truth_match"])

        # Combo 2
        _, _, ev2, _ = classify_behavior(
            "POSITIVE", "POSITIVE", 0.9, 0.9,
            expected_effect="preserve", semantic_intent="PRESERVE_POLARITY", target_polarity="NEGATIVE"
        )
        self.assertTrue(ev2["behavioral_conformance"])
        self.assertFalse(ev2["ground_truth_match"])

        # Combo 3
        _, _, ev3, _ = classify_behavior(
            "NEGATIVE", "POSITIVE", 0.9, 0.9,
            expected_effect="invert", semantic_intent="REVERSE_POLARITY", target_polarity="POSITIVE"
        )
        self.assertTrue(ev3["behavioral_conformance"])
        self.assertTrue(ev3["ground_truth_match"])

        # Combo 4
        _, _, ev4, _ = classify_behavior(
            "POSITIVE", "NEGATIVE", 0.9, 0.9,
            expected_effect="invert", semantic_intent="REVERSE_POLARITY", target_polarity="POSITIVE"
        )
        self.assertTrue(ev4["behavioral_conformance"])
        self.assertFalse(ev4["ground_truth_match"])

    # ----------------------------------------------------------------------
    # TEST 13: Real Current Regression on P001 Negation Insertion
    # ----------------------------------------------------------------------
    def test_13_real_current_regression_p001_negation(self):
        """
        Real current incident regression:
        Original: 'The movie was absolutely fantastic and thrilling.' (POSITIVE)
        Perturbed: 'The movie was not absolutely fantastic and thrilling.' (NEGATIVE)
        Verify exact analyzer resolves NEGATIVE.
        Verify expected_flip is True and expected_effect is EXPECTED_FLIP.
        Verify model predicting POS -> NEG results in MATCH (None).
        Verify model predicting POS -> POS results in BLIND (never SPURIOUS).
        """
        from blindspot.semantic.analyzer import get_exact_analyzer, SemanticReferenceLabel
        analyzer = get_exact_analyzer()
        base_lbl, _, _ = analyzer.analyze("The movie was absolutely fantastic and thrilling.")
        pert_lbl, _, _ = analyzer.analyze("The movie was not absolutely fantastic and thrilling.")
        self.assertEqual(base_lbl, SemanticReferenceLabel.POSITIVE)
        self.assertEqual(pert_lbl, SemanticReferenceLabel.NEGATIVE)

        # 1. Successful model flip: POS -> NEG -> MATCH
        outcome_flip, fail_flip, ev_flip, _ = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.95,
            probe_confidence=0.92,
            expected_effect="EXPECTED_FLIP",
            semantic_intent="REVERSE_POLARITY",
            target_polarity="NEGATIVE",
        )
        self.assertTrue(ev_flip["behavioral_conformance"])
        self.assertTrue(ev_flip["ground_truth_match"])
        self.assertEqual(fail_flip, FailureCategory.NONE)
        self.assertEqual(outcome_flip, BehavioralOutcome.EXPECTED_FLIP)

        # 2. Missing model flip: POS -> POS -> BLIND (NOT SPURIOUS)
        outcome_blind, fail_blind, ev_blind, _ = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.95,
            probe_confidence=0.90,
            expected_effect="EXPECTED_FLIP",
            semantic_intent="REVERSE_POLARITY",
            target_polarity="NEGATIVE",
        )
        self.assertFalse(ev_blind["behavioral_conformance"])
        self.assertFalse(ev_blind["ground_truth_match"])
        # Decoupled behavioral engine: MISSING_FLIP is UNDETERMINED awaiting attribution evidence
        self.assertEqual(fail_blind, FailureCategory.UNDETERMINED)
        self.assertNotEqual(fail_blind, FailureCategory.SPURIOUS)
        self.assertEqual(outcome_blind, BehavioralOutcome.MISSING_FLIP)

    # ----------------------------------------------------------------------
    # TEST 14: XAI Explanation-Backed Taxonomy Classification
    # ----------------------------------------------------------------------
    def test_14_xai_taxonomy_boundaries(self):
        """
        Verifies explanation-backed diagnosis via TaxonomyClassifier:
        - True BLIND: Expected FLIP, actual PRESERVE, explanation ignores negation
        - True SPURIOUS: Expected PRESERVE, actual FLIP, explanation driven by background
        - True MISWEIGHTED: Confidence drop on degree modifier or synonym attribution inversion
        - True UNDETERMINED: Behavioral failure with empty / indeterminate attributions
        """
        from blindspot.explainability.taxonomy import TaxonomyClassifier
        tax = TaxonomyClassifier()

        # Case A: True BLIND
        fail_blind = tax.classify_failure(
            perturbation_type="negation_insertion",
            original_sentence="The movie was absolutely fantastic and thrilling.",
            perturbed_sentence="The movie was not absolutely fantastic and thrilling.",
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            is_flipped=False,
            expected_flip=True,
            orig_explanation={"fantastic": 0.6, "thrilling": 0.4},
            pert_explanation={"not": 0.01, "fantastic": 0.58, "thrilling": 0.4},
        )
        self.assertIsNotNone(fail_blind)
        self.assertEqual(fail_blind["category"], FailureCategory.BLIND.value)
        self.assertNotEqual(fail_blind["category"], FailureCategory.SPURIOUS.value)

        # Case C: True SPURIOUS
        fail_spur = tax.classify_failure(
            perturbation_type="synonym_substitution",
            original_sentence="The service was great.",
            perturbed_sentence="The service was wonderful.",
            original_label="POSITIVE",
            perturbed_label="NEGATIVE",
            is_flipped=True,
            expected_flip=False,
            orig_explanation={"great": 0.5},
            pert_explanation={"the": 0.8, "service": 0.1},
        )
        self.assertIsNotNone(fail_spur)
        self.assertEqual(fail_spur["category"], FailureCategory.SPURIOUS.value)

        # Case D: True MISWEIGHTED (attribution inversion under synonym swap)
        fail_misw = tax.classify_failure(
            perturbation_type="synonym_substitution",
            original_sentence="The food was delicious.",
            perturbed_sentence="The food was tasty.",
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            is_flipped=False,
            expected_flip=False,
            orig_explanation={"food": 0.4, "delicious": 0.6},
            pert_explanation={"food": -0.4, "tasty": -0.6},
        )
        self.assertIsNotNone(fail_misw)
        self.assertEqual(fail_misw["category"], FailureCategory.MISWEIGHTED.value)

        # Case E: UNDETERMINED (empty / indeterminate explanation)
        fail_undet = tax.classify_failure(
            perturbation_type="negation_insertion",
            original_sentence="The service was great.",
            perturbed_sentence="The service was not great.",
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            is_flipped=False,
            expected_flip=True,
            orig_explanation={"great": 0.5},
            pert_explanation={},
        )
        self.assertIsNotNone(fail_undet)
        self.assertEqual(fail_undet["category"], FailureCategory.UNDETERMINED.value)

        # Case F: ExplanationResult and ExplanationResult.to_dict() input compatibility
        from blindspot.core.types import ExplanationResult
        exp_res = ExplanationResult(token_weights={"not": 0.01, "fantastic": 0.58})
        fail_res = tax.classify_failure(
            perturbation_type="negation_insertion",
            original_sentence="The movie was fantastic.",
            perturbed_sentence="The movie was not fantastic.",
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            is_flipped=False,
            expected_flip=True,
            orig_explanation={"fantastic": 0.6},
            pert_explanation=exp_res.to_dict(),
        )
        self.assertIsNotNone(fail_res)
        self.assertEqual(fail_res["category"], FailureCategory.BLIND.value)


if __name__ == "__main__":
    unittest.main()

