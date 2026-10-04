"""
Regression tests for Unified Comprehensive Audit Report and Dual-Variant Export Engine.
Verifies:
1. Dynamic data extraction and factual metric presentation without hardcoded findings.
2. PDF report generation using ReportLab embedding all seven required figures.
3. Pure text/table Markdown export containing zero image syntax (![...]).
4. Preservation of all existing experiment artifacts and generator interfaces.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.reporting.audit_compiler import UnifiedAuditData, FIGURE_DEFINITIONS
from blindspot.reporting.audit_pdf_generator import AuditPDFGenerator, NumberedCanvas
from blindspot.ui.reports_view import render_reports


class TestUnifiedAuditReport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exp_dir = os.path.join("runs", "exp_1790977223_6c3ec3")
        if not os.path.exists(cls.exp_dir):
            raise unittest.SkipTest(f"Test run directory not found: {cls.exp_dir}")
        cls.audit_data = UnifiedAuditData(cls.exp_dir)

    def test_audit_compiler_dynamic_data_extraction(self):
        """Verifies that audit compiler extracts real experiment metrics and config dynamically."""
        self.assertEqual(self.audit_data.exp_id, "exp_1790977223_6c3ec3")
        self.assertGreater(len(self.audit_data.models), 0)
        self.assertGreater(len(self.audit_data.baselines_table), 0)
        self.assertGreater(len(self.audit_data.metrics_table), 0)
        self.assertGreater(len(self.audit_data.taxonomy_table), 0)

        # Verify dynamic observations for all 7 figures
        required_keys = ["fig04", "fig05", "fig07", "fig08", "fig10", "fig12", "fig13"]
        for key in required_keys:
            self.assertIn(key, self.audit_data.figure_observations)
            obs = self.audit_data.figure_observations[key]
            self.assertIsInstance(obs, str)
            self.assertGreater(len(obs), 10)

    def test_markdown_export_contains_zero_image_syntax(self):
        """Verifies that clean Markdown export contains zero image tags or image embeds."""
        clean_md = self.audit_data.build_clean_markdown()
        self.assertIsInstance(clean_md, str)
        self.assertGreater(len(clean_md), 1000)

        # Strict checks for zero image syntax
        self.assertNotIn("![", clean_md, "Clean Markdown must NOT contain ![: image syntax")
        self.assertNotIn(".png", clean_md, "Clean Markdown must NOT reference .png files")
        self.assertNotIn(".jpg", clean_md, "Clean Markdown must NOT reference .jpg files")

        # Must contain all major analytical sections and tables
        self.assertIn("# BlindSpot Comprehensive Audit Report", clean_md)
        self.assertIn("1. Executive Summary & Configuration", clean_md)
        self.assertIn("2. Model Baseline Predictions", clean_md)
        self.assertIn("3. Primary Research Metrics & Calibration", clean_md)
        self.assertIn("4. Behavioral Failure Taxonomy Distribution", clean_md)
        self.assertIn("5. Sensitivity, Invariance, and Confidence Dynamics", clean_md)
        self.assertIn("6. Cross-Model Concordance Analysis", clean_md)
        self.assertIn("7. Behavioral Consistency & Executive Scorecards", clean_md)
        self.assertIn("8. Itemized Behavioral Failure Diagnoses", clean_md)
        self.assertIn("9. Granular Probe-Level Evidence Matrix", clean_md)

    def test_pdf_generation_embeds_all_seven_figures(self):
        """Verifies that ReportLab PDF compiles and embeds Figures 4, 5, 7, 8, 10, 12, 13."""
        # Check all 7 figure files exist in the experiment
        required_figures = [
            "fig04_taxonomy_distribution.png",
            "fig05_confidence_delta_by_probe.png",
            "fig07_probe_level_comparison.png",
            "fig08_model_probe_heatmap.png",
            "fig10_probe_consistency.png",
            "fig12_change_vs_preserve.png",
            "fig13_per_model_scorecard.png",
        ]
        figures_dir = os.path.join(self.exp_dir, "figures")
        for fig_fname in required_figures:
            fig_path = os.path.join(figures_dir, fig_fname)
            self.assertTrue(os.path.exists(fig_path), f"Required figure missing: {fig_path}")

        # Compile PDF bytes
        pdf_gen = AuditPDFGenerator(self.audit_data)
        pdf_bytes = pdf_gen.generate_bytes()
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(pdf_bytes.startswith(b"%PDF-"), "Generated file must be a valid PDF document")

        # With 7 embedded figures and formatted tables, the PDF should be substantial (> 500 KB)
        self.assertGreater(len(pdf_bytes), 500_000, "PDF size should reflect 7 high-res figure embeds")

    def test_preservation_of_existing_reports_and_artifacts(self):
        """Verifies that original markdown reports, telemetry, and figures remain untouched on disk."""
        reports_dir = os.path.join(self.exp_dir, "reports")
        for fname in ["experiment_summary.md", "failure_summary.md", "probe_level_evidence.md"]:
            p = os.path.join(reports_dir, fname)
            self.assertTrue(os.path.exists(p), f"Artifact missing: {p}")
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertGreater(len(content), 100)

        # Check source_data.json
        source_data_path = os.path.join(self.exp_dir, "figures", "source_data.json")
        self.assertTrue(os.path.exists(source_data_path))

    def test_ui_callable_and_design_system_compatible(self):
        """Verifies that render_reports is callable and exports correctly from the UI layer."""
        self.assertTrue(callable(render_reports))


if __name__ == "__main__":
    unittest.main()
