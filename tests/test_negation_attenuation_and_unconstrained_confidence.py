"""
Test Suite verifying:
1. Negation polarity reversal attenuation to NEUTRAL is correctly diagnosed as MISWEIGHTED
   (rather than bypassed by generic DIFFERENT_LABEL as MATCH).
2. Polarity preservation with UNCONSTRAINED confidence is treated as a valid MATCH (EXPECTED_PRESERVE / NONE),
   even if confidence drops by >15pp, adhering to the core architectural invariant.
"""
import unittest

from blindspot.core.types import BehavioralOutcome, FailureCategory, SemanticPolarity
from blindspot.testing.behavioral import classify_behavior


class TestNegationAttenuationAndUnconstrainedConfidence(unittest.TestCase):

    def test_negation_attenuation_to_neutral_is_misweighted(self):
        """
        When a probe introduces negation on a POSITIVE input and targets NEGATIVE,
        a 3-class model predicting NEUTRAL attenuates sentiment instead of inverting it.
        It must be classified as UNEXPECTED_CHANGE and FailureCategory.MISWEIGHTED.
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEUTRAL",
            original_confidence=0.667,
            probe_confidence=0.486,
            expected_effect="EXPECTED_FLIP",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
            expected_confidence_relation="UNCONSTRAINED",
            target_polarity="NEGATIVE",
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.NEUTRAL,
        )
        self.assertEqual(outcome, BehavioralOutcome.UNEXPECTED_CHANGE)
        self.assertEqual(failure_type, FailureCategory.MISWEIGHTED)
        self.assertFalse(evidence["expectation_match"])
        self.assertIn("neutralized sentiment", rationale.lower())

    def test_polarity_preservation_unconstrained_confidence_is_match(self):
        """
        When double negation preserves polarity (POSITIVE -> POSITIVE) and
        expected_confidence_relation is UNCONSTRAINED, a confidence movement (e.g. -17.22pp)
        must NOT trigger a false failure. It must be EXPECTED_PRESERVE and FailureCategory.NONE.
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.743,
            probe_confidence=0.571,
            expected_effect="EXPECTED_PRESERVE",
            semantic_intent="PRESERVE_POLARITY",
            expected_label_relation="SAME_LABEL",
            expected_confidence_relation="UNCONSTRAINED",
            target_polarity="POSITIVE",
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.POSITIVE,
            confidence_delta_threshold_pp=15.0,
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)
        self.assertEqual(failure_type, FailureCategory.NONE)
        self.assertTrue(evidence["expectation_match"])
        self.assertTrue(evidence["preservation"])
        self.assertIn("correctly preserved", rationale.lower())

    def test_polarity_preservation_constrained_confidence_still_enforces_threshold(self):
        """
        When expected_confidence_relation is constrained (e.g. SAME_CONFIDENCE or INCREASE),
        confidence drops exceeding threshold are still diagnosed as MISWEIGHTED.
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.743,
            probe_confidence=0.571,
            expected_effect="EXPECTED_PRESERVE",
            semantic_intent="PRESERVE_POLARITY",
            expected_label_relation="SAME_LABEL",
            expected_confidence_relation="SAME_CONFIDENCE",
            target_polarity="POSITIVE",
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.POSITIVE,
            confidence_delta_threshold_pp=15.0,
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)
        self.assertEqual(failure_type, FailureCategory.MISWEIGHTED)
        self.assertFalse(evidence["expectation_match"])
        self.assertIn("collapsed by", rationale.lower())


if __name__ == "__main__":
    unittest.main()
