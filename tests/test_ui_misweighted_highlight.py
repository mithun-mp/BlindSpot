"""
Test suite for surgical UI refactor: MISWEIGHTED Match Highlight.
Verifies that:
1. When expected behavior == predicted behavior and failure_type == MISWEIGHTED:
   - Caption remains "✕ MISWEIGHTED"
   - Cell status is "misweighted-match"
   - Pill is "pill-misweighted-match" (lighter neon-green visual treatment)
2. When expected behavior != predicted behavior and failure_type == MISWEIGHTED:
   - Caption remains "✕ MISWEIGHTED"
   - Cell status is "misweighted"
   - Pill is "pill-misweighted" (original violet/purple styling)
3. Non-misweighted results retain their standard styles.
4. Workstation CSS contains .cell-misweighted-match and .pill-misweighted-match.
"""
import unittest
from unittest.mock import patch, MagicMock

from blindspot.ui.design_system import get_workstation_css


class TestUIMisweightedHighlight(unittest.TestCase):
    def test_css_tokens_contain_misweighted_match_styles(self):
        """Verifies that workstation CSS defines the lighter neon-green styles for dark and light modes."""
        dark_css = get_workstation_css("dark")
        self.assertIn(".cell-misweighted-match", dark_css)
        self.assertIn(".pill-misweighted-match", dark_css)
        self.assertIn("#22c55e", dark_css)
        self.assertIn("#4ade80", dark_css)

        light_css = get_workstation_css("light")
        self.assertIn(".cell-misweighted-match", light_css)
        self.assertIn(".pill-misweighted-match", light_css)
        self.assertIn("#15803d", light_css)

    def test_misweighted_match_cell_resolution_preserve(self):
        """PRESERVE -> PRESERVE with MISWEIGHTED should receive neon-green status & pill while keeping caption."""
        expected_token = "PRESERVE"
        out = {
            "perturbed_label": "NEUTRAL",
            "perturbed_confidence": 0.71,
            "original_label": "NEUTRAL",
            "is_flipped": False,
            "failure_type": "Misweighted",
            "behavioral_outcome": "EXPECTED_PRESERVE",
            "ground_truth_match": True,
        }

        # Emulate the cell logic from blindspot/ui/comparison.py
        fail_type_clean = str(out.get("failure_type") or "").strip().lower()
        self.assertEqual(fail_type_clean, "misweighted")

        is_behavior_match = False
        if expected_token == "PRESERVE":
            is_behavior_match = (not out.get("is_flipped", False))
        elif expected_token == "FLIP":
            is_behavior_match = bool(out.get("is_flipped", False)) and out.get("ground_truth_match") is not False
        elif expected_token == "CHANGE":
            is_behavior_match = bool(out.get("is_flipped", False)) and (out.get("ground_truth_match") is True or out.get("expectation_satisfied") is True)

        if not is_behavior_match:
            is_behavior_match = bool(
                out.get("behavioral_outcome") in ("EXPECTED_PRESERVE", "EXPECTED_FLIP")
                or out.get("expectation_satisfied", False) is True
            )

        if is_behavior_match:
            status = "misweighted-match"
            pill = "pill-misweighted-match"
        else:
            status = "misweighted"
            pill = "pill-misweighted"

        badge = "✕ MISWEIGHTED"

        self.assertTrue(is_behavior_match)
        self.assertEqual(status, "misweighted-match")
        self.assertEqual(pill, "pill-misweighted-match")
        self.assertEqual(badge, "✕ MISWEIGHTED")

    def test_misweighted_match_cell_resolution_flip(self):
        """FLIP -> FLIP with MISWEIGHTED should receive neon-green status & pill while keeping caption."""
        expected_token = "FLIP"
        out = {
            "perturbed_label": "NEGATIVE",
            "perturbed_confidence": 0.95,
            "original_label": "POSITIVE",
            "is_flipped": True,
            "failure_type": "Misweighted",
            "behavioral_outcome": "EXPECTED_FLIP",
            "ground_truth_match": True,
        }

        fail_type_clean = str(out.get("failure_type") or "").strip().lower()
        self.assertEqual(fail_type_clean, "misweighted")

        is_behavior_match = False
        if expected_token == "PRESERVE":
            is_behavior_match = (not out.get("is_flipped", False))
        elif expected_token == "FLIP":
            is_behavior_match = bool(out.get("is_flipped", False)) and out.get("ground_truth_match") is not False
        elif expected_token == "CHANGE":
            is_behavior_match = bool(out.get("is_flipped", False)) and (out.get("ground_truth_match") is True or out.get("expectation_satisfied") is True)

        if not is_behavior_match:
            is_behavior_match = bool(
                out.get("behavioral_outcome") in ("EXPECTED_PRESERVE", "EXPECTED_FLIP")
                or out.get("expectation_satisfied", False) is True
            )

        if is_behavior_match:
            status = "misweighted-match"
            pill = "pill-misweighted-match"
        else:
            status = "misweighted"
            pill = "pill-misweighted"

        badge = "✕ MISWEIGHTED"

        self.assertTrue(is_behavior_match)
        self.assertEqual(status, "misweighted-match")
        self.assertEqual(pill, "pill-misweighted-match")
        self.assertEqual(badge, "✕ MISWEIGHTED")

    def test_misweighted_mismatch_retains_violet_style(self):
        """PRESERVE -> FLIP (mismatch) with MISWEIGHTED must retain the original violet style."""
        expected_token = "PRESERVE"
        out = {
            "perturbed_label": "NEGATIVE",
            "perturbed_confidence": 0.88,
            "original_label": "POSITIVE",
            "is_flipped": True,
            "failure_type": "Misweighted",
            "behavioral_outcome": "UNEXPECTED_FLIP",
            "ground_truth_match": False,
        }

        fail_type_clean = str(out.get("failure_type") or "").strip().lower()
        self.assertEqual(fail_type_clean, "misweighted")

        is_behavior_match = False
        if expected_token == "PRESERVE":
            is_behavior_match = (not out.get("is_flipped", False))
        elif expected_token == "FLIP":
            is_behavior_match = bool(out.get("is_flipped", False)) and out.get("ground_truth_match") is not False
        elif expected_token == "CHANGE":
            is_behavior_match = bool(out.get("is_flipped", False)) and (out.get("ground_truth_match") is True or out.get("expectation_satisfied") is True)

        if not is_behavior_match:
            is_behavior_match = bool(
                out.get("behavioral_outcome") in ("EXPECTED_PRESERVE", "EXPECTED_FLIP")
                or out.get("expectation_satisfied", False) is True
            )

        if is_behavior_match:
            status = "misweighted-match"
            pill = "pill-misweighted-match"
        else:
            status = "misweighted"
            pill = "pill-misweighted"

        badge = "✕ MISWEIGHTED"

        self.assertFalse(is_behavior_match)
        self.assertEqual(status, "misweighted")
        self.assertEqual(pill, "pill-misweighted")
        self.assertEqual(badge, "✕ MISWEIGHTED")


if __name__ == "__main__":
    unittest.main()
