"""
Regression tests verifying:
1. Complete elimination of orphaned section titles in the audit PDF report (hanging titles with figures).
2. Sequential figure numbering from Figure 1 to 7 (denoted from 1 to n instead of legacy thesis numbers).
"""
import os
import sys
import unittest
import pypdf

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.reporting.audit_compiler import UnifiedAuditData, FIGURE_DEFINITIONS
from blindspot.reporting.audit_pdf_generator import AuditPDFGenerator


class TestPDFLayoutAndSequentialFigureNumbering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exp_dir = os.path.join("runs", "exp_1790977223_6c3ec3")
        if not os.path.exists(cls.exp_dir):
            raise unittest.SkipTest(f"Experiment run not found: {cls.exp_dir}")
        cls.audit_data = UnifiedAuditData(cls.exp_dir)
        cls.pdf_gen = AuditPDFGenerator(cls.audit_data)
        cls.pdf_bytes = cls.pdf_gen.generate_bytes()

    def test_figure_definitions_numbered_from_1_to_n(self):
        """Verifies that FIGURE_DEFINITIONS denote figures sequentially from Figure 1 to 7."""
        expected_sequence = [
            ("fig04", "Figure 1: Failure Taxonomy Breakdown by Model"),
            ("fig12", "Figure 2: Stratified Sensitivity vs Invariance Fidelity"),
            ("fig05", "Figure 3: Mean Signed Confidence Shift by Probe"),
            ("fig08", "Figure 4: Model Probe Flip Matrix"),
            ("fig07", "Figure 5: Probe-Level Confidence Response Across Models"),
            ("fig10", "Figure 6: Behavioral Semantic Consistency Score by Model"),
            ("fig13", "Figure 7: Per-Model Multi-Metric Executive Scorecard"),
        ]

        for fig_key, expected_title in expected_sequence:
            self.assertIn(fig_key, FIGURE_DEFINITIONS)
            actual_title = FIGURE_DEFINITIONS[fig_key].get("title", "")
            self.assertEqual(actual_title, expected_title, f"Mismatch for {fig_key}")

        # Ensure no legacy disconnected titles remain
        for fig_key, info in FIGURE_DEFINITIONS.items():
            title = info.get("title", "")
            self.assertNotIn("Figure 14", title)
            self.assertNotIn("Figure 15", title)

    def test_pdf_layout_no_orphaned_section_titles(self):
        """
        Verifies that section titles are hung with their corresponding figures and
        never appear orphaned at the bottom of a page without their content.
        """
        import io
        reader = pypdf.PdfReader(io.BytesIO(self.pdf_bytes))
        self.assertGreater(len(reader.pages), 5)

        pages_text = [page.extract_text() for page in reader.pages]

        # Page 1: Must NOT have Section 3 title orphaned at the bottom
        page1_text = pages_text[0]
        self.assertNotIn(
            "3. Behavioral Failure Taxonomy & Root Cause Distribution",
            page1_text,
            "Section 3 title must NOT be orphaned on Page 1"
        )

        # Page 2: Must start with Section 3 title and Figure 1
        page2_text = pages_text[1]
        self.assertIn(
            "3. Behavioral Failure Taxonomy & Root Cause Distribution",
            page2_text,
            "Section 3 title must appear at the top of Page 2"
        )
        self.assertIn(
            "Figure 1: Failure Taxonomy Breakdown by Model",
            page2_text,
            "Figure 1 must hang with Section 3 title on Page 2"
        )
        self.assertNotIn(
            "4. Sensitivity vs Invariance Fidelity & Confidence Dynamics",
            page2_text,
            "Section 4 title must NOT be orphaned on Page 2"
        )

        # Page 3: Must start with Section 4 title and Figure 2
        page3_text = pages_text[2]
        self.assertIn(
            "4. Sensitivity vs Invariance Fidelity & Confidence Dynamics",
            page3_text,
            "Section 4 title must appear on Page 3"
        )
        self.assertIn(
            "Figure 2: Stratified Sensitivity vs Invariance Fidelity",
            page3_text,
            "Figure 2 must hang with Section 4 title on Page 3"
        )

        # Page 4: Contains Figure 3 and must NOT have Section 5 title orphaned at bottom
        page4_text = pages_text[3]
        self.assertIn(
            "Figure 3: Mean Signed Confidence Shift by Probe",
            page4_text,
            "Figure 3 must appear on Page 4"
        )
        self.assertNotIn(
            "5. Cross-Model Concordance & Architectural Stability",
            page4_text,
            "Section 5 title must NOT be orphaned on Page 4"
        )

        # Page 5: Must start with Section 5 title and Figure 4
        page5_text = pages_text[4]
        self.assertIn(
            "5. Cross-Model Concordance & Architectural Stability",
            page5_text,
            "Section 5 title must appear on Page 5"
        )
        self.assertIn(
            "Figure 4: Model Probe Flip Matrix",
            page5_text,
            "Figure 4 must hang with Section 5 title on Page 5"
        )

        # Page 6: Contains Figure 5 and must NOT have Section 6 title orphaned at bottom
        page6_text = pages_text[5]
        self.assertIn(
            "Figure 5: Probe-Level Confidence Response Across Models",
            page6_text,
            "Figure 5 must appear on Page 6"
        )
        self.assertNotIn(
            "6. Behavioral Consistency & Multi-Metric Profiles",
            page6_text,
            "Section 6 title must NOT be orphaned on Page 6"
        )

        # Page 7: Must start with Section 6 title and Figure 6
        page7_text = pages_text[6]
        self.assertIn(
            "6. Behavioral Consistency & Multi-Metric Profiles",
            page7_text,
            "Section 6 title must appear on Page 7"
        )
        self.assertIn(
            "Figure 6: Behavioral Semantic Consistency Score by Model",
            page7_text,
            "Figure 6 must hang with Section 6 title on Page 7"
        )
        self.assertIn(
            "Figure 7: Per-Model Multi-Metric Executive Scorecard",
            page7_text,
            "Figure 7 must appear on Page 7"
        )


if __name__ == "__main__":
    unittest.main()
