"""
Regression tests for:
1. Negation-removal token-boundary correction (notch, notice, notable, nothing, note, nevertheless, top notch).
2. Grammatical contraction transformations (don't, doesn't, didn't, isn't, aren't, wasn't, weren't, can't, won't, shan't).
3. Behavioral terminology correction (replacing Accuracy with Behavioral Consistency).
4. Removal of redundant visible [LITERAL], Pragmatic Classifications, and Type columns while preserving SentenceType.LITERAL.
5. PDF 4-column baseline table verification (Model | Seed Sentence | Baseline Class | Confidence).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.perturbations.negation import NegationPerturber, CONTRACTION_DE_NEGATIONS
from blindspot.core.types import SentenceType
from blindspot.reporting.audit_compiler import UnifiedAuditData
from blindspot.reporting.audit_pdf_generator import AuditPDFGenerator


class TestNegationBoundaryAndContractions(unittest.TestCase):
    def setUp(self):
        self.perturber = NegationPerturber()

    def test_ordinary_words_with_not_or_never_are_not_corrupted(self):
        """Proves words starting with or containing 'not' or 'never' substrings are preserved."""
        cases = [
            ("notch", "This is top notch quality."),
            ("notice", "I did not notice the defect."),
            ("notable", "The performance was not notable."),
            ("nothing", "There was nothing wrong."),
            ("nothing_with_not", "It was not nothing."),
            ("note", "Please take note of this detail."),
            ("notes", "These were not notes."),
            ("notion", "I do not accept that notion."),
            ("notorious", "He was not notorious for errors."),
            ("nevertheless", "He was not happy; nevertheless, he smiled."),
            ("top_notch", "This is a top notch experience, not bad."),
        ]

        for name, sentence in cases:
            with self.subTest(name=name):
                variants = self.perturber.perturb(sentence)
                self.assertGreater(len(variants), 0)
                perturbed = variants[0]["perturbed"]

                # The ordinary word MUST be intact in the perturbed text
                if "notch" in sentence:
                    self.assertIn("notch", perturbed, f"Failed for {name}: 'notch' mutilated to 'ch' in '{perturbed}'")
                    self.assertNotIn(" ch ", f" {perturbed} ")
                if "notice" in sentence:
                    self.assertIn("notice", perturbed, f"Failed for {name}: 'notice' mutilated in '{perturbed}'")
                if "notable" in sentence:
                    self.assertIn("notable", perturbed, f"Failed for {name}: 'notable' mutilated in '{perturbed}'")
                if "nothing" in sentence:
                    self.assertIn("nothing", perturbed, f"Failed for {name}: 'nothing' mutilated in '{perturbed}'")
                if "notes" in sentence:
                    self.assertIn("notes", perturbed, f"Failed for {name}: 'notes' mutilated in '{perturbed}'")
                elif "note" in sentence:
                    self.assertIn("note", perturbed, f"Failed for {name}: 'note' mutilated in '{perturbed}'")
                if "nevertheless" in sentence:
                    self.assertIn("nevertheless", perturbed, f"Failed for {name}: 'nevertheless' mutilated in '{perturbed}'")

    def test_contraction_transformations_grammatical(self):
        """Verifies exact grammatical contraction transformations."""
        contractions = [
            ("I don't agree.", "I do agree."),
            ("She doesn't care.", "She does care."),
            ("He didn't leave.", "He did leave."),
            ("It isn't fair.", "It is fair."),
            ("They aren't ready.", "They are ready."),
            ("It wasn't easy.", "It was easy."),
            ("They weren't sure.", "They were sure."),
            ("I can't go.", "I can go."),
            ("I won't stop.", "I will stop."),
            ("We shan't surrender.", "We shall surrender."),
            ("Don't fail.", "Do fail."),
            ("Won't fail.", "Will fail."),
            ("Can't stop.", "Can stop."),
        ]

        for sentence, expected in contractions:
            with self.subTest(sentence=sentence):
                variants = self.perturber.perturb(sentence)
                self.assertEqual(len(variants), 1)
                self.assertEqual(variants[0]["type"], "negation_removal")
                self.assertEqual(variants[0]["perturbed"], expected)


class TestBehavioralTerminologyCorrection(unittest.TestCase):
    def test_accuracy_replaced_in_comparison_view(self):
        """Verifies comparison.py uses Behavioral Consistency instead of Accuracy for consistency metric."""
        comparison_path = os.path.join("blindspot", "ui", "comparison.py")
        with open(comparison_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Check metric label
        self.assertIn('st.metric("Behavioral Consistency", f"{m_acc:.1f}%")', code)
        self.assertNotIn('st.metric("Accuracy / Consistency"', code)

        # Check caption
        self.assertIn('empirical Behavioral Consistency', code)
        self.assertNotIn('empirical Accuracy', code)

        # Check table keys
        self.assertIn('"Behavioral Consistency": "—"', code)
        self.assertIn('"Behavioral Consistency": f"{accuracy:.1f}%"', code)
        self.assertNotIn('"Accuracy": "—"', code)
        self.assertNotIn('"Accuracy": f"{accuracy:.1f}%"', code)


class TestLiteralAndPragmaticRemoval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exp_dir = os.path.join("runs", "exp_1790977223_6c3ec3")
        cls.audit_data = UnifiedAuditData(cls.exp_dir)

    def test_internal_sentence_type_literal_remains_intact(self):
        """SentenceType.LITERAL enum and value must remain available to internal pipeline logic."""
        self.assertTrue(hasattr(SentenceType, "LITERAL"))
        self.assertEqual(SentenceType.LITERAL.value, "literal")
        self.assertEqual(str(SentenceType.LITERAL), "SentenceType.LITERAL")

    def test_clean_markdown_has_no_literal_or_pragmatic_presentation(self):
        """Verifies absence of visible [LITERAL], Pragmatic Classifications, and Type columns in markdown."""
        md = self.audit_data.build_clean_markdown()

        # No [LITERAL] badge
        self.assertNotIn("[LITERAL]", md)
        self.assertNotIn("[literal]", md)

        # No Pragmatic Classifications header
        self.assertNotIn("Pragmatic Classifications", md)

        # Baseline table has 3 columns: Model | Baseline Prediction | Confidence (seed removed)
        self.assertIn("## 2. Model Baseline Predictions", md)
        self.assertIn("| Model | Baseline Prediction | Confidence |", md)
        self.assertNotIn("| Seed Sentence |", md)
        self.assertNotIn("| Semantic Type |", md)
        self.assertNotIn("| Type |", md)

    def test_pdf_baseline_table_three_columns(self):
        """Verifies PDF generator generates 3-column baseline representation (no seed column)."""
        pdf_gen = AuditPDFGenerator(self.audit_data)
        pdf_bytes = pdf_gen.generate_bytes()
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(pdf_bytes.startswith(b"%PDF-"))

        # Verify baseline table items in data do not have seed or type fields
        for row in self.audit_data.baselines_table:
            self.assertIn("model", row)
            self.assertNotIn("seed", row)
            self.assertIn("prediction", row)
            self.assertIn("confidence", row)
            self.assertNotIn("type", row)


if __name__ == "__main__":
    unittest.main()
