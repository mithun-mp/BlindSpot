"""
Publication-Grade Audit PDF Generator for BlindSpot.
Compiles executive summaries, metadata, data tables, behavioral failure diagnoses,
and embeds the 7 core thesis figures (Figures 4, 5, 7, 8, 10, 12, 13) with in-depth
scientific explanations using ReportLab.
"""
import os
import io
from typing import Dict, Any, List, Optional
from PIL import Image as PILImage

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage,
    KeepTogether,
    HRFlowable,
    CondPageBreak,
)
from reportlab.pdfgen.canvas import Canvas

from blindspot.reporting.audit_compiler import UnifiedAuditData, FIGURE_DEFINITIONS


class NumberedCanvas(Canvas):
    """Two-pass canvas to compute dynamic total page numbers and paint running headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.exp_id = ""

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            Canvas.showPage(self)
        Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 762, "BlindSpot Multimodel Robustness Audit — Diagnostic Report")
            if self.exp_id:
                self.drawRightString(576, 762, f"Run: {self.exp_id}")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 756, 576, 756)

        # Running Footer (all pages)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 24, page_str)
        self.drawString(36, 24, "CONFIDENTIAL & PROPRIETARY — SCIENTIFIC RESEARCH AUDIT")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 34, 576, 34)

        self.restoreState()


class AuditPDFGenerator:
    """Compiles the complete audit report into a publication-grade PDF containing all 7 figures."""

    def __init__(self, audit_data: UnifiedAuditData):
        self.data = audit_data
        self.styles = self._setup_styles()

    def _setup_styles(self) -> Dict[str, ParagraphStyle]:
        base_styles = getSampleStyleSheet()
        custom = {}

        custom["Title"] = ParagraphStyle(
            "AuditTitle",
            parent=base_styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#0f172a"),
            alignment=0,
            spaceAfter=4,
        )

        custom["Subtitle"] = ParagraphStyle(
            "AuditSubtitle",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#475569"),
            spaceAfter=12,
        )

        custom["H1"] = ParagraphStyle(
            "AuditH1",
            parent=base_styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#0f2942"),
            spaceBefore=14,
            spaceAfter=6,
            keepWithNext=True,
        )

        custom["H2"] = ParagraphStyle(
            "AuditH2",
            parent=base_styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#1e293b"),
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True,
        )

        custom["Body"] = ParagraphStyle(
            "AuditBody",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=4,
        )

        custom["BodyBold"] = ParagraphStyle(
            "AuditBodyBold",
            parent=custom["Body"],
            fontName="Helvetica-Bold",
        )

        custom["Caption"] = ParagraphStyle(
            "AuditCaption",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#0369a1"),
            spaceBefore=4,
            spaceAfter=3,
        )

        custom["CalloutText"] = ParagraphStyle(
            "AuditCallout",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#334155"),
        )

        custom["TableHead"] = ParagraphStyle(
            "AuditTableHead",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#ffffff"),
            alignment=1,
        )

        custom["TableCell"] = ParagraphStyle(
            "AuditTableCell",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.5,
            textColor=colors.HexColor("#1e293b"),
        )

        custom["TableCellCenter"] = ParagraphStyle(
            "AuditTableCellCenter",
            parent=custom["TableCell"],
            alignment=1,
        )

        return custom

    def generate_bytes(self) -> bytes:
        """Builds and returns the PDF document as raw binary bytes."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=36,
            rightMargin=36,
            topMargin=46,
            bottomMargin=46,
        )

        story = []

        # 1. Header Banner
        exp_title = self.data.metadata.get("experiment_title", self.data.exp_id)
        story.append(Paragraph(f"BlindSpot Robustness Audit: {exp_title}", self.styles["Title"]))
        story.append(Paragraph(f"Experiment Run: <b>{self.data.exp_id}</b> | Multi-Model Diagnostic Certification Report", self.styles["Subtitle"]))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=10))

        # 2. Executive Metadata Box
        meta_table_data = [
            [
                Paragraph(f"<b>Created:</b> {self.data.metadata.get('created_at', 'N/A')}", self.styles["CalloutText"]),
                Paragraph(f"<b>Evaluated Models:</b> {len(self.data.models)}", self.styles["CalloutText"]),
                Paragraph(f"<b>Integrity Status:</b> <font color='#16a34a'><b>{self.data.metadata.get('pipeline_status', 'PASS')}</b></font>", self.styles["CalloutText"]),
            ],
            [
                Paragraph(f"<b>Total Diagnosed Failures:</b> {len(self.data.failures_list)}", self.styles["CalloutText"]),
                Paragraph(f"<b>Probes per Model:</b> {len(self.data.probe_evidence_rows) // max(1, len(self.data.models))}", self.styles["CalloutText"]),
                Paragraph("<b>Audit Framework:</b> Deterministic Behavioral + Attribution XAI", self.styles["CalloutText"]),
            ]
        ]
        meta_table = Table(meta_table_data, colWidths=[180, 180, 180])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 10))

        # 3. Model Baseline Predictions
        if self.data.baselines_table:
            b_head = [
                Paragraph("Model", self.styles["TableHead"]),
                Paragraph("Baseline Class", self.styles["TableHead"]),
                Paragraph("Confidence", self.styles["TableHead"]),
            ]
            b_rows = [b_head]
            for r in self.data.baselines_table:
                b_rows.append([
                    Paragraph(f"<b>{r['model']}</b>", self.styles["TableCell"]),
                    Paragraph(f"<b>{r['prediction']}</b>", self.styles["TableCellCenter"]),
                    Paragraph(r['confidence'], self.styles["TableCellCenter"]),
                ])
            b_table = Table(b_rows, colWidths=[240, 150, 150])
            b_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            story.append(KeepTogether([
                Paragraph("1. Model Architecture Baselines", self.styles["H1"]),
                Spacer(1, 4),
                b_table,
            ]))
            story.append(Spacer(1, 10))

        # 4. Primary Research Metrics Table
        if self.data.metrics_table:
            m_head = [
                Paragraph("Model Architecture", self.styles["TableHead"]),
                Paragraph("Probes", self.styles["TableHead"]),
                Paragraph("Observed Flips", self.styles["TableHead"]),
                Paragraph("Expected-Flip<br/>Compliance", self.styles["TableHead"]),
                Paragraph("Preserve<br/>Rate", self.styles["TableHead"]),
                Paragraph("Consistency", self.styles["TableHead"]),
                Paragraph("ECE", self.styles["TableHead"]),
                Paragraph("Mean Δ", self.styles["TableHead"]),
            ]
            m_rows = [m_head]
            for r in self.data.metrics_table:
                comp_val = r.get("expected_flip_compliance", r.get("expected_flips", ""))
                m_rows.append([
                    Paragraph(f"<b>{r['model']}</b>", self.styles["TableCell"]),
                    Paragraph(str(r['probes']), self.styles["TableCellCenter"]),
                    Paragraph(r['observed_flips'], self.styles["TableCellCenter"]),
                    Paragraph(f"<b>{comp_val}</b>", self.styles["TableCellCenter"]),
                    Paragraph(r['preserve_rate'], self.styles["TableCellCenter"]),
                    Paragraph(f"<b>{r['consistency']}</b>", self.styles["TableCellCenter"]),
                    Paragraph(r['ece'], self.styles["TableCellCenter"]),
                    Paragraph(r['mean_delta'], self.styles["TableCellCenter"]),
                ])
            m_table = Table(m_rows, colWidths=[150, 36, 68, 76, 60, 65, 45, 40])
            m_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            block_elements = [
                Paragraph("2. Primary Research Metrics & Probabilistic Calibration", self.styles["H1"]),
            ]
            suite_share_val = self.data.metrics_table[0].get("suite_expected_flip_share") if self.data.metrics_table else None
            if suite_share_val and suite_share_val != "N/A":
                block_elements.append(Paragraph(f"<i>Suite Expected-Flip Share: {suite_share_val} (Test suite composition: polarity-reversal probes — suite property, not model performance)</i>", self.styles["Subtitle"]))
                block_elements.append(Spacer(1, 2))
            else:
                block_elements.append(Spacer(1, 4))
            block_elements.append(m_table)
            story.append(KeepTogether(block_elements))
            story.append(Spacer(1, 10))

        # 5. Section: Failure Taxonomy & FIGURE 1 (Hang section title with Figure 1)
        story.append(self._build_figure_block("fig04", section_title="3. Behavioral Failure Taxonomy & Root Cause Distribution"))
        if self.data.taxonomy_table:
            t_head = [
                Paragraph("Model Architecture", self.styles["TableHead"]),
                Paragraph("Blind", self.styles["TableHead"]),
                Paragraph("Spurious", self.styles["TableHead"]),
                Paragraph("Misweighted", self.styles["TableHead"]),
                Paragraph("Undetermined", self.styles["TableHead"]),
                Paragraph("Compliant (None)", self.styles["TableHead"]),
            ]
            t_rows = [t_head]
            for r in self.data.taxonomy_table:
                t_rows.append([
                    Paragraph(f"<b>{r['model']}</b>", self.styles["TableCell"]),
                    Paragraph(str(r['blind']), self.styles["TableCellCenter"]),
                    Paragraph(str(r['spurious']), self.styles["TableCellCenter"]),
                    Paragraph(str(r['misweighted']), self.styles["TableCellCenter"]),
                    Paragraph(str(r['undetermined']), self.styles["TableCellCenter"]),
                    Paragraph(f"<b>{r['compliant']}</b>", self.styles["TableCellCenter"]),
                ])
            t_table = Table(t_rows, colWidths=[180, 65, 65, 75, 75, 80])
            t_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            story.append(t_table)
            story.append(Spacer(1, 10))

        # 6. Section: Sensitivity vs Invariance Dynamics (Hang section title with Figure 2)
        story.append(self._build_figure_block("fig12", section_title="4. Sensitivity vs Invariance Fidelity & Confidence Dynamics"))
        story.append(Spacer(1, 6))
        story.append(self._build_figure_block("fig05"))
        story.append(Spacer(1, 10))

        # 7. Section: Cross-Model Concordance (Hang section title with Figure 4)
        story.append(self._build_figure_block("fig08", section_title="5. Cross-Model Concordance & Architectural Stability"))
        story.append(Spacer(1, 6))
        story.append(self._build_figure_block("fig07"))
        story.append(Spacer(1, 6))

        if self.data.pairwise_matrix.get("models") and self.data.pairwise_matrix.get("matrix"):
            num_cols = len(self.data.pairwise_matrix["models"])
            first_w = 140
            rem_w = max(40, (540 - first_w) / max(1, num_cols))
            p_head = [Paragraph("Model", self.styles["TableHead"])] + [
                Paragraph(m[:14], self.styles["TableHead"]) for m in self.data.pairwise_matrix["models"]
            ]
            p_rows = [p_head]
            for row in self.data.pairwise_matrix["matrix"]:
                p_rows.append(
                    [Paragraph(f"<b>{row['model'][:20]}</b>", self.styles["TableCell"])] +
                    [Paragraph(val, self.styles["TableCellCenter"]) for val in row["values"]]
                )
            p_table = Table(p_rows, colWidths=[first_w] + [rem_w] * num_cols)
            p_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 2.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ]))
            story.append(KeepTogether([
                Paragraph("<b>Pairwise Prediction Agreement Matrix (%)</b>", self.styles["H2"]),
                Spacer(1, 2),
                p_table,
            ]))
            story.append(Spacer(1, 10))

        # 8. Section: Behavioral Consistency & Executive Scorecards (Hang section title with Figure 6)
        story.append(self._build_figure_block("fig10", section_title="6. Behavioral Consistency & Multi-Metric Profiles"))
        story.append(Spacer(1, 6))
        story.append(self._build_figure_block("fig13"))
        story.append(Spacer(1, 10))

        # 9. Section: Itemized Failure Diagnoses
        if self.data.failures_list:
            first_box = self._build_failure_box(1, self.data.failures_list[0])
            story.append(KeepTogether([
                Paragraph("7. Itemized Behavioral Failure Diagnoses & Explanations", self.styles["H1"]),
                Spacer(1, 4),
                first_box,
            ]))
            story.append(Spacer(1, 6))

            for idx, f in enumerate(self.data.failures_list[1:], 2):
                story.append(self._build_failure_box(idx, f))
                story.append(Spacer(1, 6))

        # 10. Granular Probe-Level Evidence Table
        if self.data.probe_evidence_rows:
            story.append(CondPageBreak(120))
            story.append(Paragraph("8. Granular Probe-Level Empirical Evidence Matrix", self.styles["H1"]))
            e_head = [
                Paragraph("Model", self.styles["TableHead"]),
                Paragraph("Probe ID", self.styles["TableHead"]),
                Paragraph("Category", self.styles["TableHead"]),
                Paragraph("Observed Transition", self.styles["TableHead"]),
                Paragraph("Δ Conf", self.styles["TableHead"]),
                Paragraph("Flip", self.styles["TableHead"]),
                Paragraph("Outcome", self.styles["TableHead"]),
                Paragraph("Diagnosis", self.styles["TableHead"]),
            ]
            e_rows = [e_head]
            for row in self.data.probe_evidence_rows:
                fail_color = "#b91c1c" if row['failure'] != "None" else "#15803d"
                e_rows.append([
                    Paragraph(row['model'], self.styles["TableCell"]),
                    Paragraph(row['probe_id'], self.styles["TableCell"]),
                    Paragraph(row['category'][:14], self.styles["TableCell"]),
                    Paragraph(row['transition'], self.styles["TableCell"]),
                    Paragraph(row['delta_conf'], self.styles["TableCellCenter"]),
                    Paragraph(row['flip'], self.styles["TableCellCenter"]),
                    Paragraph(row['outcome'], self.styles["TableCellCenter"]),
                    Paragraph(f"<font color='{fail_color}'><b>{row['failure']}</b></font>", self.styles["TableCellCenter"]),
                ])
            e_table = Table(e_rows, colWidths=[110, 45, 55, 115, 45, 35, 75, 60], repeatRows=1)
            e_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ]))
            story.append(e_table)

        # Build document with NumberedCanvas
        def canvas_maker(*args, **kwargs):
            canvas = NumberedCanvas(*args, **kwargs)
            canvas.exp_id = self.data.exp_id
            return canvas

        doc.build(story, canvasmaker=canvas_maker)
        return buffer.getvalue()

    def _build_failure_box(self, idx: int, f: Dict[str, Any]) -> Table:
        """Constructs an individual styled failure card table."""
        f_flowables = []
        cat_badge = f.get('category', 'UNKNOWN').upper()
        f_flowables.append(Paragraph(
            f"<b>Failure #{idx}: <font color='#8e44ad'>[{cat_badge}]</font> — Model <code>{f.get('model', '')}</code></b>",
            self.styles["H2"]
        ))
        f_flowables.append(Paragraph(f"• <b>Probe ID:</b> <code>{f.get('probe_id', 'N/A')}</code>", self.styles["Body"]))
        if "transition" in f:
            f_flowables.append(Paragraph(f"• <b>Observed Transition:</b> {f['transition']}", self.styles["Body"]))
        if "reason" in f:
            f_flowables.append(Paragraph(f"• <b>Diagnostic Reason:</b> {f['reason']}", self.styles["Body"]))
        if "evidence" in f:
            f_flowables.append(Paragraph(f"• <b>XAI Attribution Evidence:</b> {f['evidence']}", self.styles["Body"]))
        if "recommendation" in f:
            f_flowables.append(Paragraph(f"• <b>Remediation Recommendation:</b> {f['recommendation']}", self.styles["Body"]))
        f_flowables.append(Spacer(1, 4))

        f_box = Table([[f_flowables]], colWidths=[540])
        f_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#fbfcfe")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        return f_box

    def _build_figure_block(self, fig_key: str, section_title: Optional[str] = None) -> KeepTogether:
        """Constructs a self-contained figure card with image and structured explanation.
        If section_title is provided, it is kept together with the figure so it never orphans alone."""
        flowables = []
        if section_title:
            flowables.append(Paragraph(section_title, self.styles["H1"]))
            flowables.append(Spacer(1, 4))

        fig_info = FIGURE_DEFINITIONS.get(fig_key, {})
        fname = fig_info.get("filename", "")
        fig_path = os.path.join(self.data.figures_dir, fname)

        # Figure Caption Header (Sequential Figure 1 to 7)
        flowables.append(Paragraph(f"<b>{fig_info.get('title', fname)}</b>", self.styles["Caption"]))

        # Image Flowable (if exists on disk)
        if os.path.exists(fig_path):
            try:
                with PILImage.open(fig_path) as pil_img:
                    orig_w, orig_h = pil_img.size
                max_w = 510
                max_h = 240
                scale = min(max_w / orig_w, max_h / orig_h)
                flowables.append(RLImage(fig_path, width=orig_w * scale, height=orig_h * scale))
                flowables.append(Spacer(1, 3))
            except Exception:
                flowables.append(Paragraph(f"<i>[Image file {fname} could not be loaded]</i>", self.styles["CalloutText"]))
        else:
            flowables.append(Paragraph(f"<i>[Figure {fname} not found in experiment figures directory]</i>", self.styles["CalloutText"]))

        # Structured Explanation Callout Box
        obs_text = self.data.figure_observations.get(fig_key, "")
        callout_content = [
            Paragraph(f"<b>What this figure is:</b> {fig_info.get('what_it_is', '')}", self.styles["CalloutText"]),
            Spacer(1, 2),
            Paragraph(f"<b>Empirical Observation:</b> {obs_text}", self.styles["CalloutText"]),
            Spacer(1, 2),
            Paragraph(f"<b>Diagnostic Significance:</b> {fig_info.get('why_it_matters', '')}", self.styles["CalloutText"]),
        ]
        callout_table = Table([[callout_content]], colWidths=[520])
        callout_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0f9ff")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#38bdf8")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        flowables.append(callout_table)
        flowables.append(Spacer(1, 6))

        return KeepTogether(flowables)
