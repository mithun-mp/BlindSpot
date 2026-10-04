"""
Reports View: Interactive Diagnostic Visualizations, Graphs, and Markdown Audit Reports.
Features publication-grade figure gallery, single-figure inspector with mathematical interpretations,
raw source data exporter, and markdown report viewer with embedded figures.
"""
import streamlit as st
import os
import json
from typing import Dict, Any, List

import importlib
from blindspot.storage.run_store import RunStore
from blindspot.ui.components import render_empty_state, render_markdown_with_images
import blindspot.reporting.audit_compiler as audit_compiler_mod
import blindspot.reporting.audit_pdf_generator as audit_pdf_gen_mod

importlib.reload(audit_compiler_mod)
importlib.reload(audit_pdf_gen_mod)

from blindspot.reporting.audit_compiler import UnifiedAuditData, FIGURE_DEFINITIONS
from blindspot.reporting.audit_pdf_generator import AuditPDFGenerator


THESIS_FIGURE_METADATA = {
    "fig01_prediction_distribution.png": {
        "title": "Figure 1: Model Prediction Distribution",
        "category": "Behavioral Responses",
        "description": "Normalized distribution of predicted sentiment classes across all evaluated perturbation probes for each model architecture.",
        "interpretation": "Reveals whether models exhibit systematic classification skew under semantic perturbations.",
    },
    "fig02_flip_rates.png": {
        "title": "Figure 2: Observed vs Expected Flip Rates",
        "category": "Behavioral Responses",
        "description": "Compares empirical prediction flip percentage against the theoretical expected flip contract.",
        "interpretation": "High divergence indicates model sensitivity to invariant edits or blindness to polarity reversals.",
    },
    "fig03_expected_vs_observed.png": {
        "title": "Figure 3: Expected vs Observed Semantic Behavioral Rate",
        "category": "Behavioral Responses",
        "description": "Quantifies the proportion of probes where observed behavioral transitions matched the expected semantic effect.",
        "interpretation": "Direct measure of model behavioral compliance against linguistic invariants.",
    },
    "fig04_taxonomy_distribution.png": {
        "title": "Figure 4: 4-Way Behavioral Failure Taxonomy Distribution",
        "category": "Taxonomy & Failures",
        "description": "Proportional distribution of diagnosed behavioral failures: BLIND, SPURIOUS, MISWEIGHTED, and COMPLIANT (None).",
        "interpretation": "Primary thesis visualization diagnosing the structural nature of model brittleness.",
    },
    "fig05_confidence_delta_by_probe.png": {
        "title": "Figure 5: Signed Confidence Shift by Linguistic Category",
        "category": "Confidence Dynamics",
        "description": "Box/bar visualization of signed confidence changes in percentage points across probe categories.",
        "interpretation": "Tracks whether downtoners correctly reduce confidence and intensifiers strengthen it.",
    },
    "fig06_confidence_delta_distribution.png": {
        "title": "Figure 6: Overall Confidence Shift Density",
        "category": "Confidence Dynamics",
        "description": "Density distribution of signed confidence deltas across all models and probe evaluations.",
        "interpretation": "Highlights whether model predictions experience subtle confidence erosion even without discrete label flips.",
    },
    "fig07_probe_level_comparison.png": {
        "title": "Figure 7: Probe-Level Response Across Models",
        "category": "Probe Analysis",
        "description": "Side-by-side bar chart of perturbed prediction confidence for individual diagnostic probes across target architectures.",
        "interpretation": "Identifies which specific linguistic structures trigger cross-architecture consensus vs disagreement.",
    },
    "fig08_model_probe_heatmap.png": {
        "title": "Figure 8: Model Probe Flip Matrix",
        "category": "Cross-Model Concordance",
        "description": "Interactive matrix displaying prediction stability (FLIP vs SAME) for every probe across all models.",
        "interpretation": "Instantly visualizes shared vs architecture-specific failure modes.",
    },
    "fig09_transition_matrix.png": {
        "title": "Figure 9: Label Transition Matrix",
        "category": "Behavioral Responses",
        "description": "Heatmap depicting transition dynamics from original predicted classes to perturbed predicted classes.",
        "interpretation": "Highlights directional transition biases (e.g. Negative to Neutral vs Negative to Positive).",
    },
    "fig10_probe_consistency.png": {
        "title": "Figure 10: Behavioral Consistency by Category",
        "category": "Probe Analysis",
        "description": "Behavioral consistency score (%) achieved by each model broken down by perturbation category.",
        "interpretation": "Pinpoints linguistic categories where specific models are robust or brittle.",
    },
    "fig11_model_agreement.png": {
        "title": "Figure 11: Cross-Model Pairwise Agreement Matrix",
        "category": "Cross-Model Concordance",
        "description": "Heatmap displaying pairwise prediction agreement percentages between all evaluated models.",
        "interpretation": "Evaluates architectural diversity and consensus behavior across distinct model families.",
    },
    "fig12_change_vs_preserve.png": {
        "title": "Figure 12: Change vs Preserve Sensitivity Profile",
        "category": "Behavioral Responses",
        "description": "Scatter comparison of flip rate on meaning-altering probes vs preserve rate on meaning-preserving probes.",
        "interpretation": "The ideal robust classifier sits in the top-right quadrant (100% change, 100% preserve).",
    },
    "fig13_per_model_scorecard.png": {
        "title": "Figure 13: Comprehensive Robustness Scorecard",
        "category": "Scorecards & Profiling",
        "description": "Multi-metric performance summary per model incorporating consistency, preserve rate, and ECE calibration.",
        "interpretation": "Holistic executive scorecard for model auditing and deployment readiness.",
    },
    "fig14_runtime_profile.png": {
        "title": "Figure 14: Execution Latency & Profiling Breakdown",
        "category": "Scorecards & Profiling",
        "description": "Runtime latency profiling separating inference, explainability (LIME/SHAP), and analysis overhead.",
        "interpretation": "Documents computational efficiency and batching performance.",
    },
    "fig15_probe_category_comparison.png": {
        "title": "Figure 15: Cross-Category Resilience Comparison",
        "category": "Probe Analysis",
        "description": "Comparative bar chart summarizing failure frequencies across linguistic perturbation families.",
        "interpretation": "Guides targeted dataset augmentation and adversarial regularization.",
    },
}


def _render_audit_figure(fig_key: str, figures_dir: str, audit_data: UnifiedAuditData):
    """Renders a single core thesis figure card with high-res PNG, download button, and scientific explanation."""
    fig_info = FIGURE_DEFINITIONS.get(fig_key, {})
    fname = fig_info.get("filename", "")
    fig_path = os.path.join(figures_dir, fname)
    title = fig_info.get("title", fname)
    category = fig_info.get("category", "General")
    what_it_is = fig_info.get("what_it_is", "")
    why_it_matters = fig_info.get("why_it_matters", "")
    observation = audit_data.figure_observations.get(fig_key, "")

    st.markdown(
        f"""
        <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 18px; margin:14px 0 10px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-size:1.05rem; font-weight:700; color:#f1f5f9;">{title}</span>
                <span style="background:#0284c7; color:#f0f9ff; padding:2px 8px; border-radius:3px; font-size:0.75rem; font-family:monospace;">{category.upper()}</span>
            </div>
            <div style="color:#cbd5e1; font-size:0.85rem; margin-bottom:4px;"><b>Figure Definition:</b> {what_it_is}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if os.path.exists(fig_path):
        st.image(fig_path, use_container_width=True)
        col_dl, col_blank = st.columns([1, 3])
        with col_dl:
            with open(fig_path, "rb") as fp:
                st.download_button(
                    label=f"⬇️ Download {fname} (300 DPI)",
                    data=fp.read(),
                    file_name=fname,
                    mime="image/png",
                    key=f"dl_unified_{fig_key}_{fname}",
                )
    else:
        st.info(f"Figure file `{fname}` not generated for this experiment run.")

    st.markdown(
        f"""
        <div style="background:#0f172a; border-left:3px solid #38bdf8; border-radius:0 4px 4px 0; padding:10px 14px; margin:6px 0 16px 0; font-size:0.82rem;">
            <div style="color:#38bdf8; font-weight:600; margin-bottom:2px;">🔍 Empirical Observation:</div>
            <div style="color:#e2e8f0; margin-bottom:6px;">{observation}</div>
            <div style="color:#94a3b8; font-style:italic;">💡 Diagnostic Significance: {why_it_matters}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_reports():
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                DIAGNOSTIC VISUALIZATIONS & ARTIFACTS
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                Unified publication-grade audit report, thesis diagnostic visualizations, and dual-variant export engine.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    store = RunStore()
    available_runs = store.list_runs(include_archived=False)

    # Resolve active experiment ID
    active_results = st.session_state.get("active_results")
    default_exp_id = active_results.get("experiment_id", "") if active_results else ""

    if not default_exp_id and available_runs:
        default_exp_id = available_runs[0].get("experiment_id", "")

    if not default_exp_id:
        render_empty_state(
            title="NO EXPERIMENT DATA FOUND",
            message="No active or historical audit runs are available. Launch an audit in Experiment Lab to generate diagnostic figures and reports.",
            action_label="GO TO EXPERIMENT LAB",
            action_key="rep_empty_to_exp",
        )
        return

    # Run selector in top header
    run_options = [r.get("experiment_id", "") for r in available_runs if r.get("experiment_id")]
    if default_exp_id not in run_options:
        run_options.insert(0, default_exp_id)

    col_exp1, col_exp2 = st.columns([3, 1])
    with col_exp1:
        sel_idx = run_options.index(default_exp_id) if default_exp_id in run_options else 0
        selected_exp_id = st.selectbox(
            "Selected Experiment Artifacts:",
            options=run_options,
            index=sel_idx,
            format_func=lambda x: f"{store.get_run_title(x)} ({x})",
            key="rep_sel_exp_id",
        )

    exp_dir = store.get_run_dir(selected_exp_id)
    figures_dir = os.path.join(exp_dir, "figures")
    reports_dir = os.path.join(exp_dir, "reports")

    sel_title = store.get_run_title(selected_exp_id)
    with col_exp2:
        st.markdown(
            f"""
            <div style="background:#141824; border:1px solid #26334d; border-radius:4px; padding:6px 12px; margin-top:24px; font-family:monospace; font-size:0.75rem; color:#94a3b8; text-align:center;">
                <div style="color:#64748b; font-size:0.68rem;">EXPERIMENT:</div>
                <div style="color:#38bdf8; font-weight:bold; font-size:0.82rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="{sel_title}">{sel_title}</div>
                <div style="color:#64748b; font-size:0.65rem;">{selected_exp_id}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Compile structured audit data dynamically from experiment artifacts
    audit_data = UnifiedAuditData(exp_dir)

    # Unified Tabs: Consolidated Comprehensive Audit Report + Raw Telemetry Data
    tab_audit, tab_source = st.tabs([
        "📑 Comprehensive Audit Report",
        "📊 Raw Telemetry Data (source_data.json)",
    ])

    # -------------------------------------------------------------
    # TAB 1: CONSOLIDATED COMPREHENSIVE AUDIT REPORT
    # -------------------------------------------------------------
    with tab_audit:
        # Top Action Toolbar for Dual-Variant Downloads
        st.markdown(
            """
            <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 18px; margin-bottom:18px;">
                <div style="font-size:0.95rem; font-weight:700; color:#f1f5f9; margin-bottom:4px;">
                    🚀 AUDIT REPORT EXPORT TOOLBAR
                </div>
                <div style="color:#94a3b8; font-size:0.8rem; margin-bottom:10px;">
                    Download the complete certified audit report. Choose between a publication-grade PDF containing all 7 embedded figures and in-depth analyses, or a pure text & tables Markdown document.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_dl_pdf, col_dl_md = st.columns(2)
        with col_dl_pdf:
            try:
                importlib.reload(audit_compiler_mod)
                importlib.reload(audit_pdf_gen_mod)
                pdf_gen = audit_pdf_gen_mod.AuditPDFGenerator(audit_data)
                pdf_bytes = pdf_gen.generate_bytes()
                st.download_button(
                    label="📄 Download Audit Report (PDF with All 7 Figures)",
                    data=pdf_bytes,
                    file_name=f"{selected_exp_id}_audit_report.pdf",
                    mime="application/pdf",
                    key="dl_pdf_full",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"Error compiling PDF: {str(e)}")

        with col_dl_md:
            clean_md = audit_data.build_clean_markdown()
            st.download_button(
                label="📝 Download Audit Report (Markdown - Text & Tables Only)",
                data=clean_md,
                file_name=f"{selected_exp_id}_audit_report.md",
                mime="text/markdown",
                key="dl_md_clean",
                use_container_width=True,
            )

        st.markdown("---")

        # 1. Executive Summary & Configuration
        st.markdown(
            f"""
            <div style="font-size:1.15rem; font-weight:700; color:#38bdf8; margin:16px 0 8px 0;">
                1. Executive Summary & Audit Configuration
            </div>
            """,
            unsafe_allow_html=True,
        )

        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        with kpi_col1:
            st.metric("Target Models", len(audit_data.models))
        with kpi_col2:
            total_p = audit_data.source_data.get("pipeline_integrity", {}).get("total_probes", len(audit_data.probe_evidence_rows) // max(1, len(audit_data.models)))
            st.metric("Probes Evaluated", total_p)
        with kpi_col3:
            st.metric("Diagnosed Failures", len(audit_data.failures_list))
        with kpi_col4:
            st.metric("Pipeline Integrity", audit_data.metadata.get("pipeline_status", "PASS"))

        if audit_data.seed_sentences:
            st.markdown("##### Baseline Seed Sentences")
            for idx, s in enumerate(audit_data.seed_sentences, 1):
                st.markdown(f"- **Seed #{idx}**: *\"{s}\"*")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Model Baseline Predictions
        if audit_data.baselines_table:
            st.markdown(
                """
                <div style="font-size:1.15rem; font-weight:700; color:#38bdf8; margin:16px 0 8px 0;">
                    2. Original Sentence Baselines
                </div>
                """,
                unsafe_allow_html=True,
            )
            clean_baselines = [
                {
                    "Model": r.get("model", ""),
                    "Baseline Prediction": r.get("prediction", ""),
                    "Confidence": r.get("confidence", ""),
                }
                for r in audit_data.baselines_table
            ]
            st.table(clean_baselines)
            st.markdown("<br>", unsafe_allow_html=True)

        # 3. Primary Research Metrics
        if audit_data.metrics_table:
            st.markdown(
                """
                <div style="font-size:1.15rem; font-weight:700; color:#38bdf8; margin:16px 0 8px 0;">
                    3. Primary Research Metrics & Probabilistic Calibration
                </div>
                """,
                unsafe_allow_html=True,
            )
            suite_share_val = audit_data.metrics_table[0].get("suite_expected_flip_share") if audit_data.metrics_table else None
            if suite_share_val and suite_share_val != "N/A":
                st.caption(f"ℹ️ **Suite Expected-Flip Share**: {suite_share_val} — Percentage of probes in this test suite whose expected semantic effect is polarity reversal (test suite property).")
            clean_metrics = [
                {
                    "Model": r.get("model", ""),
                    "Probes": r.get("probes", 0),
                    "Observed Flips": r.get("observed_flips", ""),
                    "Expected-Flip Compliance": r.get("expected_flip_compliance", r.get("expected_flips", "")),
                    "Preserve Rate": r.get("preserve_rate", ""),
                    "Consistency": r.get("consistency", ""),
                    "ECE": r.get("ece", ""),
                    "Mean Δ Conf": r.get("mean_delta", ""),
                }
                for r in audit_data.metrics_table
            ]
            st.table(clean_metrics)
            st.markdown("<br>", unsafe_allow_html=True)

        # 4. Behavioral Failure Taxonomy & FIGURE 4
        st.markdown(
            """
            <div style="font-size:1.15rem; font-weight:700; color:#38bdf8; margin:16px 0 8px 0;">
                4. Behavioral Failure Taxonomy & Root Cause Distribution
            </div>
            """,
            unsafe_allow_html=True,
        )
        _render_audit_figure("fig04", figures_dir, audit_data)
        if audit_data.taxonomy_table:
            st.markdown("##### Failure Taxonomy Counts Breakdown")
            clean_taxonomy = [
                {
                    "Model": r.get("model", ""),
                    "Blind": r.get("blind", 0),
                    "Spurious": r.get("spurious", 0),
                    "Misweighted": r.get("misweighted", 0),
                    "Undetermined": r.get("undetermined", 0),
                    "Compliant": r.get("compliant", 0),
                }
                for r in audit_data.taxonomy_table
            ]
            st.table(clean_taxonomy)
        st.markdown("<br>", unsafe_allow_html=True)

        # 5. Sensitivity vs Invariance Dynamics (FIGURE 12 & FIGURE 5)
        st.markdown(
            """
            <div style="font-size:1.15rem; font-weight:700; color:#38bdf8; margin:16px 0 8px 0;">
                5. Sensitivity vs Invariance Fidelity & Confidence Dynamics
            </div>
            """,
            unsafe_allow_html=True,
        )
        _render_audit_figure("fig12", figures_dir, audit_data)
        _render_audit_figure("fig05", figures_dir, audit_data)
        st.markdown("<br>", unsafe_allow_html=True)

        # 6. Cross-Model Concordance (FIGURE 8 & FIGURE 7)
        st.markdown(
            """
            <div style="font-size:1.15rem; font-weight:700; color:#38bdf8; margin:16px 0 8px 0;">
                6. Cross-Model Concordance & Architectural Stability
            </div>
            """,
            unsafe_allow_html=True,
        )
        _render_audit_figure("fig08", figures_dir, audit_data)
        _render_audit_figure("fig07", figures_dir, audit_data)

        if audit_data.pairwise_matrix.get("models") and audit_data.pairwise_matrix.get("matrix"):
            st.markdown("##### Pairwise Prediction Agreement Matrix (%)")
            matrix_data = []
            for row in audit_data.pairwise_matrix["matrix"]:
                entry = {"Model": row["model"]}
                for m_name, val in zip(audit_data.pairwise_matrix["models"], row["values"]):
                    entry[m_name] = val
                matrix_data.append(entry)
            st.table(matrix_data)
        st.markdown("<br>", unsafe_allow_html=True)

        # 7. Behavioral Consistency & Executive Scorecards (FIGURE 10 & FIGURE 13)
        st.markdown(
            """
            <div style="font-size:1.15rem; font-weight:700; color:#38bdf8; margin:16px 0 8px 0;">
                7. Behavioral Consistency & Multi-Metric Profiles
            </div>
            """,
            unsafe_allow_html=True,
        )
        _render_audit_figure("fig10", figures_dir, audit_data)
        _render_audit_figure("fig13", figures_dir, audit_data)
        st.markdown("<br>", unsafe_allow_html=True)

        # 8. Itemized Behavioral Failure Diagnoses
        st.markdown(
            """
            <div style="font-size:1.15rem; font-weight:700; color:#38bdf8; margin:16px 0 8px 0;">
                8. Itemized Behavioral Failure Diagnoses & Explanations
            </div>
            """,
            unsafe_allow_html=True,
        )
        if not audit_data.failures_list:
            st.success("✅ No behavioral failure modes were diagnosed for this experiment run. All evaluated models complied with semantic invariants.")
        else:
            for idx, f in enumerate(audit_data.failures_list, 1):
                badge_color = "#8e44ad" if f.get("category") == "Misweighted" else ("#c0392b" if f.get("category") == "Blind" else "#d35400")
                st.markdown(
                    f"""
                    <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 16px; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-size:0.95rem; font-weight:bold; color:#f1f5f9;">Failure #{idx}: Model <code>{f.get('model', '')}</code></span>
                            <span style="background:{badge_color}; color:#ffffff; padding:2px 8px; border-radius:3px; font-size:0.75rem; font-family:monospace;">{f.get('category', 'UNKNOWN').upper()}</span>
                        </div>
                        <div style="color:#94a3b8; font-size:0.8rem; margin:2px 0;"><b>Probe ID:</b> <code>{f.get('probe_id', 'N/A')}</code></div>
                        <div style="color:#e2e8f0; font-size:0.82rem; margin:2px 0;"><b>Observed Transition:</b> {f.get('transition', 'N/A')}</div>
                        <div style="color:#cbd5e1; font-size:0.82rem; margin:4px 0;"><b>Diagnostic Reason:</b> {f.get('reason', 'N/A')}</div>
                        <div style="color:#38bdf8; font-size:0.8rem; margin:4px 0;"><b>Attribution Evidence:</b> {f.get('evidence', 'N/A')}</div>
                        <div style="color:#10b981; font-size:0.8rem; margin:4px 0;"><b>Actionable Recommendation:</b> {f.get('recommendation', 'N/A')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("<br>", unsafe_allow_html=True)

        # 9. Granular Probe-Level Evidence Matrix
        if audit_data.probe_evidence_rows:
            st.markdown(
                """
                <div style="font-size:1.15rem; font-weight:700; color:#38bdf8; margin:16px 0 8px 0;">
                    9. Granular Probe-Level Empirical Evidence Matrix
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.dataframe(audit_data.probe_evidence_rows, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 2: RAW TELEMETRY DATA (source_data.json)
    # -------------------------------------------------------------
    with tab_source:
        source_data_path = os.path.join(figures_dir, "source_data.json")
        if not os.path.exists(source_data_path):
            st.info(f"No source_data.json found at `{source_data_path}`.")
        else:
            with open(source_data_path, "r", encoding="utf-8") as f:
                source_json = json.load(f)

            st.markdown(
                """
                <div style="color:#94a3b8; font-size:0.85rem; margin-bottom:10px;">
                    Raw numerical coordinates and metrics backing all publication figures. Exportable for external plotting tools (Origin, Prism, LaTeX TikZ).
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.download_button(
                label="⬇️ Download source_data.json",
                data=json.dumps(source_json, indent=2),
                file_name=f"{selected_exp_id}_source_data.json",
                mime="application/json",
                key="dl_source_json_btn",
            )

            st.json(source_json)
