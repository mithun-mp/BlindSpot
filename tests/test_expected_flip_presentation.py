"""
Unit and regression tests for BlindSpot Expected-Flip Presentation Enhancement.

Validates that:
1. The 7-probe investigative case:
   Expected flips: {P1, P6}
   Actual flips:   {P3, P4}
   Correctly renders:
     Observed Flips = 2/7 (28.6%)
     Expected-Flip Compliance = 0/2 (0.0%)
     Preserve Rate = 3/5 (60.0%)
     Behavioral Consistency = 3/7 (42.9%)
     Suite Expected-Flip Share = 2/7 (28.6%)
   And never confuses suite flip share (28.6%) with model compliance (0.0%).
2. The real DistilBERT run (exp_1790977223_6c3ec3) displays:
     Expected-Flip Compliance = 2/2 (100.0%)
   And never displays 0/2 (28.6%).
3. Clean markdown and PDF generator produce unambiguous headers and correct values.
"""
import os
import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.reporting.audit_compiler import UnifiedAuditData
from blindspot.reporting.audit_pdf_generator import AuditPDFGenerator
from blindspot.testing.metrics import (
    compute_observed_flip_rate,
    compute_expected_flip_rate,
    compute_expected_flip_compliance,
    compute_preserve_rate,
    compute_behavioral_consistency,
)


class TestExpectedFlipPresentation(unittest.TestCase):
    def test_investigative_seven_probe_case_mathematics_and_presentation(self):
        """
        Investigates the exact 7-probe scenario:
        P1: Expected FLIP, Actual PRESERVE -> FAIL
        P2: Expected PRESERVE, Actual PRESERVE -> PASS
        P3: Expected PRESERVE, Actual FLIP -> FAIL
        P4: Expected PRESERVE, Actual FLIP -> FAIL
        P5: Expected PRESERVE, Actual PRESERVE -> PASS
        P6: Expected FLIP, Actual PRESERVE -> FAIL
        P7: Expected PRESERVE, Actual PRESERVE -> PASS
        """
        evals = [
            {"probe_id": "P1", "expected_flip": True, "is_flipped": False, "polarity_flip": False, "expectation_match": False, "expectation_satisfied": False},
            {"probe_id": "P2", "expected_flip": False, "is_flipped": False, "polarity_flip": False, "expectation_match": True, "expectation_satisfied": True},
            {"probe_id": "P3", "expected_flip": False, "is_flipped": True, "polarity_flip": True, "expectation_match": False, "expectation_satisfied": False},
            {"probe_id": "P4", "expected_flip": False, "is_flipped": True, "polarity_flip": True, "expectation_match": False, "expectation_satisfied": False},
            {"probe_id": "P5", "expected_flip": False, "is_flipped": False, "polarity_flip": False, "expectation_match": True, "expectation_satisfied": True},
            {"probe_id": "P6", "expected_flip": True, "is_flipped": False, "polarity_flip": False, "expectation_match": False, "expectation_satisfied": False},
            {"probe_id": "P7", "expected_flip": False, "is_flipped": False, "polarity_flip": False, "expectation_match": True, "expectation_satisfied": True},
        ]

        # 1. Mathematical Ground Truth
        obs_rate = compute_observed_flip_rate(evals)
        suite_flip_rate = float(sum(1 for e in evals if e.get("expected_flip")) / len(evals))
        compliance = compute_expected_flip_compliance(evals)
        pres_rate = compute_preserve_rate(evals)
        consistency = compute_behavioral_consistency(evals)

        self.assertAlmostEqual(obs_rate, 2 / 7, places=4)
        self.assertAlmostEqual(suite_flip_rate, 2 / 7, places=4)
        self.assertAlmostEqual(compliance, 0.0, places=4)
        self.assertAlmostEqual(pres_rate, 3 / 5, places=4)
        self.assertAlmostEqual(consistency, 3 / 7, places=4)

        # 2. Emulate Runner Table Rendering
        tot = len(evals)
        obs_flips = sum(1 for e in evals if e.get("is_flipped"))
        exp_flips_tot = sum(1 for e in evals if e.get("expected_flip"))
        corr_exp_flips = sum(1 for e in evals if e.get("expected_flip") and e.get("is_flipped"))
        pres_tot = sum(1 for e in evals if not e.get("expected_flip"))
        corr_pres = sum(1 for e in evals if (not e.get("expected_flip")) and (not e.get("is_flipped")))
        corr_cons = sum(1 for e in evals if e.get("expectation_satisfied"))

        obs_str = f"{obs_flips}/{tot} ({obs_rate * 100:.1f}%)"
        comp_str = f"{corr_exp_flips}/{exp_flips_tot} ({compliance * 100:.1f}%)"
        suite_str = f"{exp_flips_tot}/{tot} ({suite_flip_rate * 100:.1f}%)"
        pres_str = f"{corr_pres}/{pres_tot} ({pres_rate * 100:.1f}%)"
        cons_str = f"{corr_cons}/{tot} ({consistency * 100:.1f}%)"

        self.assertEqual(obs_str, "2/7 (28.6%)")
        self.assertEqual(comp_str, "0/2 (0.0%)")
        self.assertEqual(suite_str, "2/7 (28.6%)")
        self.assertEqual(pres_str, "3/5 (60.0%)")
        self.assertEqual(cons_str, "3/7 (42.9%)")

        # Crucial disambiguation checks:
        self.assertNotEqual(comp_str, "0/2 (28.6%)")
        self.assertNotEqual(comp_str, "28.6%")
        self.assertNotEqual(comp_str, "2/2 (100.0%)")

    def test_distilbert_run_acceptance_presentation(self):
        """
        Acceptance Test 2:
        Verifies that for active run exp_1790977223_6c3ec3, DistilBERT renders:
        Expected-Flip Compliance = 2/2 (100.0%)
        NOT 0/2 (28.6%) or 28.6%.
        """
        exp_dir = os.path.join("runs", "exp_1790977223_6c3ec3")
        audit_data = UnifiedAuditData(exp_dir)

        # Find DistilBERT row in metrics_table
        distilbert_row = None
        for row in audit_data.metrics_table:
            if "distilbert" in row["model"].lower():
                distilbert_row = row
                break

        self.assertIsNotNone(distilbert_row, "DistilBERT row must exist in metrics table")
        self.assertEqual(distilbert_row["probes"], 7)
        self.assertEqual(distilbert_row["observed_flips"], "2/7 (28.6%)")
        self.assertEqual(distilbert_row["expected_flip_compliance"], "2/2 (100.0%)")
        self.assertEqual(distilbert_row["expected_flips"], "2/2 (100.0%)")
        self.assertEqual(distilbert_row["suite_expected_flip_share"], "2/7 (28.6%)")
        self.assertEqual(distilbert_row["preserve_rate"], "5/5 (100.0%)")
        self.assertEqual(distilbert_row["consistency"], "7/7 (100.0%)")

        # Clean markdown must reflect correct headers and values
        clean_md = audit_data.build_clean_markdown()
        self.assertIn("Expected-Flip Compliance", clean_md)
        self.assertIn("Suite Expected-Flip Share", clean_md)
        self.assertIn("2/7 (28.6%)", clean_md)
        self.assertIn("distilbert-base-uncased-finetuned-sst-2-english", clean_md)
        self.assertIn("2/2 (100.0%)", clean_md)

        # PDF generator must build clean valid bytes without error
        pdf_gen = AuditPDFGenerator(audit_data)
        pdf_bytes = pdf_gen.generate_bytes()
        self.assertTrue(pdf_bytes.startswith(b"%PDF-"))


if __name__ == "__main__":
    unittest.main()
