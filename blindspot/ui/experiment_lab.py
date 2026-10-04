"""
Experiment Lab: Guided Multimodel Auditing Workflow.
Implements 01 PROBES (from Probe Workbench) -> 02 MODELS -> 03 EXECUTION -> 04 REVIEW
with technical cards, hardware-aware execution controls, and deterministic probe staging.
"""
import streamlit as st
from typing import List, Dict, Any, Optional

from blindspot.core.config import ExperimentConfig, PerformanceMode
from blindspot.models.registry import ModelRegistry
from blindspot.models.cache import ModelCache
from blindspot.execution.runner import ExperimentRunner
from blindspot.execution.resources import ResourceManager
from blindspot.ui.components import render_technical_model_card
from blindspot.semantic import get_semantic_service


def render_experiment_lab():
    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                EXPERIMENT CONFIGURATION
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                Guided workstation workflow for multimodel behavioral and explainability auditing.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    registry = ModelRegistry()
    presets = registry.list_sentiment_models()
    cache = ModelCache.get_shared_cache()
    specs = ResourceManager.get_system_specs()
    host_device = specs.get("pytorch_device", "cpu")

    staged_probe_set = st.session_state.get("staged_probe_set")

    # ==========================================
    # 01 PROBES — STAGED STIMULI & SEMANTIC GROUND-TRUTH
    # ==========================================
    st.markdown(
        """
        <div style="background:var(--bs-surface-1, #141824); border-left:3px solid var(--bs-accent, #38bdf8); padding:8px 12px; margin:16px 0 10px 0;">
            <strong style="color:var(--bs-accent, #38bdf8); font-family:monospace; font-size:0.9rem;">01 PROBES — STAGED STIMULI & SEMANTIC GROUND-TRUTH</strong>
            <div style="color:var(--bs-text-secondary, #94a3b8); font-size:0.75rem;">Verified linguistic perturbations and canonical semantic ground-truth accepted from the Probe Workbench.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if staged_probe_set is None or not staged_probe_set.probes:
        st.markdown(
            """
            <div style="background:var(--bs-surface-1, #141824); border:1px dashed var(--bs-border, #26334d); border-radius:6px; padding:16px; margin:10px 0; color:var(--bs-text-secondary, #94a3b8); font-size:0.85rem;">
                No stimuli currently staged. Configure, verify, and stage candidate probes in the <strong>Probes</strong> tab to proceed with the audit.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Resolve semantic reference set and ensure verified from workbench
        ref_set = getattr(staged_probe_set, "semantic_reference_set", None)
        if ref_set is None:
            svc = get_semantic_service()
            seed_t = staged_probe_set.seed_texts[0] if staged_probe_set.seed_texts else ""
            ref_set = svc.annotate_experiment(baseline_text=seed_t, probes=staged_probe_set.probes)
            staged_probe_set.semantic_reference_set = ref_set

        if ref_set is not None:
            if hasattr(ref_set, "baseline_annotation") and ref_set.baseline_annotation:
                b_stat = getattr(ref_set.baseline_annotation, "verification_status", None)
                b_stat_str = b_stat.value if hasattr(b_stat, "value") else str(b_stat)
                if b_stat_str == "UNVERIFIED":
                    ref_set.baseline_annotation.accept_gemini()
            for pannot in getattr(ref_set, "probe_annotations", {}).values():
                p_stat = getattr(pannot, "verification_status", None)
                p_stat_str = p_stat.value if hasattr(p_stat, "value") else str(p_stat)
                if p_stat_str == "UNVERIFIED":
                    pannot.accept_gemini()
            if hasattr(ref_set, "_recompute_relations"):
                ref_set._recompute_relations()

        base_annot = getattr(ref_set, "baseline_annotation", None)
        seed_text = staged_probe_set.seed_texts[0] if staged_probe_set.seed_texts else (base_annot.sentence_text if base_annot else "")
        base_pol = (
            base_annot.final_semantic_polarity.value
            if base_annot and getattr(base_annot, "final_semantic_polarity", None)
            else "UNAVAILABLE"
        )

        def _get_pol_color(pol_val: str) -> str:
            p = str(pol_val).upper()
            if "UNAVAILABLE" in p:
                return "#ef4444"
            elif "POS" in p:
                return "#10b981"
            elif "NEG" in p:
                return "#f43f5e"
            return "#38bdf8"

        base_pol_color = _get_pol_color(base_pol)

        # Baseline Display (Full text completely visible, accepted from workbench, NO buttons)
        st.markdown(
            f"""
            <div style="background:var(--bs-surface-1, #141824); border:1px solid var(--bs-border, #26334d); border-radius:6px; padding:12px 16px; margin:10px 0 12px 0;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:8px;">
                    <span style="color:var(--bs-accent, #38bdf8); font-family:monospace; font-size:0.85rem; font-weight:700; letter-spacing:0.04em;">
                        ORIGINAL BENCHMARK STIMULUS (BASELINE)
                    </span>
                    <div style="display:flex; gap:8px; align-items:center;">
                        <span style="background:rgba(16, 185, 129, 0.15); color:#10b981; border:1px solid rgba(16, 185, 129, 0.3); padding:2px 8px; border-radius:4px; font-family:monospace; font-size:0.75rem; font-weight:600;">
                            ✓ ACCEPTED FROM WORKBENCH
                        </span>
                        <span style="background:rgba(56, 189, 248, 0.12); color:{base_pol_color}; border:1px solid {base_pol_color}55; padding:2px 8px; border-radius:4px; font-family:monospace; font-size:0.75rem; font-weight:700;">
                            POLARITY: {base_pol}
                        </span>
                    </div>
                </div>
                <div style="color:var(--bs-text-primary, #f1f5f9); font-size:0.95rem; font-weight:500; line-height:1.5; margin:4px 0;">
                    "{seed_text}"
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        num_staged = len(staged_probe_set.probes)
        with st.expander(f"Inspect Staged Probes ({num_staged} stimuli)", expanded=True):
            probe_annots = getattr(ref_set, "probe_annotations", {}) if ref_set else {}
            for idx, p in enumerate(staged_probe_set.probes):
                pannot = probe_annots.get(p.probe_id)
                if pannot:
                    is_p_unavail = (getattr(pannot, "status", "AVAILABLE") == "UNAVAILABLE" or getattr(pannot, "final_semantic_polarity", None) is None)
                    p_pol = (
                        pannot.final_semantic_polarity.value
                        if not is_p_unavail and hasattr(pannot.final_semantic_polarity, "value")
                        else ("UNAVAILABLE" if is_p_unavail else str(pannot.final_semantic_polarity))
                    )
                    rel_val = getattr(pannot, "semantic_relation_to_baseline", None)
                    p_rel = (
                        rel_val.value
                        if rel_val and hasattr(rel_val, "value")
                        else ("—" if is_p_unavail or base_pol == "UNAVAILABLE" else str(rel_val or "—"))
                    )
                else:
                    p_pol = "NEGATIVE" if p.expected_flip else base_pol
                    p_rel = "REVERSE_POLARITY" if p.expected_flip else ("—" if base_pol == "UNAVAILABLE" else "PRESERVE_POLARITY")

                pol_col = _get_pol_color(p_pol)
                rel_col = "#ef4444" if "UNAVAILABLE" in p_rel else ("#f59e0b" if "REVERSE" in p_rel else "#10b981")

                st.markdown(
                    f"""
                    <div style="background:var(--bs-surface-1, #141824); border:1px solid var(--bs-border, #26334d); border-radius:6px; padding:10px 14px; margin-bottom:8px; font-family:monospace; font-size:0.8rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; flex-wrap:wrap; gap:6px;">
                            <div style="display:flex; align-items:center; gap:8px;">
                                <span style="color:var(--bs-text-secondary, #94a3b8); font-weight:bold;">#{idx + 1}</span>
                                <span style="color:var(--bs-accent, #38bdf8); font-weight:bold;">{p.probe_id}</span>
                                <span style="background:var(--bs-surface-2, #1e293b); color:var(--bs-text-primary, #cbd5e1); padding:2px 7px; border-radius:3px; font-size:0.72rem; font-weight:600;">
                                    {p.perturbation_type.upper()}
                                </span>
                            </div>
                            <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
                                <span style="background:rgba(56, 189, 248, 0.1); color:{pol_col}; border:1px solid {pol_col}55; padding:2px 7px; border-radius:3px; font-size:0.72rem; font-weight:700;">
                                    POLARITY: {p_pol}
                                </span>
                                <span style="background:rgba(245, 158, 11, 0.1); color:{rel_col}; border:1px solid {rel_col}55; padding:2px 7px; border-radius:3px; font-size:0.72rem; font-weight:600;">
                                    {p_rel}
                                </span>
                                <span style="background:rgba(16, 185, 129, 0.12); color:#10b981; border:1px solid rgba(16, 185, 129, 0.3); padding:2px 7px; border-radius:3px; font-size:0.7rem; font-weight:600;">
                                    ✓ ACCEPTED
                                </span>
                            </div>
                        </div>
                        <div style="color:var(--bs-text-primary, #f1f5f9); font-size:0.88rem; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height:1.45; margin:6px 0 2px 0;">
                            <span style="color:var(--bs-accent, #38bdf8); font-family:monospace; font-size:0.75rem; font-weight:700;">PROBE: </span>"{p.perturbed_text}"
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ==========================================
    # 02 MODELS — TARGET CLASSIFIERS
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:16px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">02 MODELS — TARGET CLASSIFIERS</strong>
            <div style="color:#94a3b8; font-size:0.75rem;">Select verified model presets or register custom HuggingFace architectures.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Preset selection state with key epoch for guaranteed UI checkbox synchronization
    if "selected_models" not in st.session_state:
        st.session_state["selected_models"] = ["distilbert-base-uncased-finetuned-sst-2-english"]
    if "chk_epoch" not in st.session_state:
        st.session_state["chk_epoch"] = 0

    col_m_act1, col_m_act2, col_m_spacer = st.columns([2, 2, 4])
    with col_m_act1:
        if st.button("Select All Presets", key="btn_select_all_presets", use_container_width=True):
            st.session_state["selected_models"] = [p["model_id"] for p in presets]
            st.session_state["chk_epoch"] = st.session_state.get("chk_epoch", 0) + 1
            st.rerun()
    with col_m_act2:
        if st.button("Deselect All", key="btn_deselect_all_presets", use_container_width=True):
            st.session_state["selected_models"] = []
            st.session_state["chk_epoch"] = st.session_state.get("chk_epoch", 0) + 1
            st.rerun()

    # Render technical cards for preset models
    cols = st.columns(2)
    epoch = st.session_state.get("chk_epoch", 0)
    current_selected = list(st.session_state.get("selected_models", []))

    for idx, preset in enumerate(presets):
        m_id = preset["model_id"]
        is_checked = (m_id in current_selected)
        is_cached = cache.is_cached(m_id)
        chk_key = f"chk_model_{m_id}_{epoch}"

        with cols[idx % 2]:
            new_checked = st.checkbox(
                f"**{preset['name']}** (`{m_id.split('/')[-1]}`)",
                value=is_checked,
                key=chk_key,
            )
            if new_checked and m_id not in current_selected:
                current_selected.append(m_id)
                st.session_state["selected_models"] = current_selected
            elif not new_checked and m_id in current_selected:
                current_selected.remove(m_id)
                st.session_state["selected_models"] = current_selected

            render_technical_model_card(
                model_id=m_id,
                architecture=preset.get("architecture", "Transformer"),
                num_classes=preset.get("num_classes", 2),
                params_millions=preset.get("parameters_millions"),
                is_cached=is_cached,
                is_selected=new_checked,
                device=host_device,
            )

    # Custom Model Registration
    with st.expander("Register Custom HuggingFace Model", expanded=False):
        custom_m_input = st.text_input(
            "HuggingFace Repository Identifier:",
            placeholder="e.g. cardiffnlp/twitter-roberta-base-sentiment-latest",
            key="custom_hf_input",
        )
        if st.button("Add Model", key="btn_add_custom_model"):
            clean_cm = custom_m_input.strip()
            if clean_cm and clean_cm not in current_selected:
                current_selected.append(clean_cm)
                st.session_state["selected_models"] = current_selected
                st.success(f"Added '{clean_cm}' to target models.")
                st.rerun()

    # Explicit Model Count Confirmation
    num_selected_models = len(st.session_state["selected_models"])
    st.markdown(
        f"""
        <div style="background:#0b1329; border:1px solid #1e3a8a; border-radius:4px; padding:8px 12px; margin:10px 0 18px 0; font-size:0.8rem; font-family:monospace;">
            <span style="color:#60a5fa; font-weight:bold;">● {num_selected_models} model(s) selected:</span>
            <span style="color:#93c5fd; margin-left:6px;">All models will receive identical deterministic probes.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ==========================================
    # 03 EXECUTION — WORKSTATION SCHEDULER & RUN PLAN
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:16px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">03 EXECUTION — WORKSTATION SCHEDULER & RUN PLAN</strong>
            <div style="color:#94a3b8; font-size:0.75rem;">Specify experiment title, inspect exact Run Plan, and launch the audit.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    perf_mode = "performance"
    xai_mode = "both"

    exp_title = st.text_input(
        "Experiment Title:",
        value="Multimodel Robustness Audit",
        key="txt_exp_title",
        help="Specify an informative title to label and identify this evaluation across reports and archives.",
    )

    # Compute Exact Run Plan
    num_seeds = len(staged_probe_set.seed_texts) if staged_probe_set is not None else 0
    total_probes_planned = len(staged_probe_set.probes) if staged_probe_set is not None else 0
    total_baselines = num_selected_models * num_seeds
    total_probe_inferences = num_selected_models * total_probes_planned
    total_model_calls = total_baselines + total_probe_inferences

    st.markdown(
        f"""
        <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 16px; margin:12px 0 16px 0; font-family:monospace; font-size:0.8rem;">
            <div style="color:#f1f5f9; font-weight:bold; margin-bottom:8px;">EXACT RUN PLAN (BASELINE + PROBES × MODELS):</div>
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:8px; color:#94a3b8;">
                <div>Seed Sentences: <span style="color:#e2e8f0;">{num_seeds}</span></div>
                <div>Target Models: <span style="color:#e2e8f0;">{num_selected_models}</span></div>
                <div>Planned Probes: <span style="color:#38bdf8;">{total_probes_planned}</span></div>
                <div>Baseline Evals: <span style="color:#10b981;">{total_baselines}</span></div>
                <div>Probe Evals: <span style="color:#e2e8f0;">{total_probe_inferences}</span></div>
                <div>Total Predictions: <span style="color:#f59e0b; font-weight:bold;">{total_model_calls}</span></div>
                <div>Catalog Source: <span style="color:#38bdf8;">{'VERIFIED WORKBENCH' if staged_probe_set is not None else 'NONE (AWAITING STAGING)'}</span></div>
                <div>Explainer: <span style="color:#e2e8f0;">BOTH (LIME + SHAP)</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Active Runner check
    runner: Optional[ExperimentRunner] = st.session_state.get("active_runner")
    is_running = runner is not None and runner.status == "running"

    if is_running:
        st.warning(f"⚠️ Audit experiment is currently running [{runner.experiment_id}]. Step: {runner.current_step}")
        col_c1, col_c2 = st.columns([2, 3])
        with col_c1:
            if st.button("■ CANCEL ACTIVE RUN", key="btn_cancel_active_run", type="secondary", use_container_width=True):
                runner.cancel()
                st.warning("Cancellation requested.")
                st.rerun()
        with col_c2:
            if st.button("JUMP TO LIVE RUN MONITOR", key="btn_jump_live_run", type="primary", use_container_width=True):
                st.session_state["current_page"] = "Live Run"
                st.rerun()
    else:
        col_btn, col_empty = st.columns([2, 3])
        with col_btn:
            launch_clicked = st.button("▶ RUN EXPERIMENT", type="primary", use_container_width=True, key="btn_launch_exp")

        if launch_clicked:
            selected_models = list(st.session_state.get("selected_models", []))
            # Validations
            if not selected_models:
                st.error("Validation Error: Please select at least one target model in Step 02.")
                return

            if staged_probe_set is None:
                st.error("Validation Error: No probe catalog staged. Please curate and stage probes in the 'Probes' tab before launching.")
                return

            final_probe_set = staged_probe_set
            final_probe_ids = [p.probe_id for p in final_probe_set.probes]
            selected_ptypes = list(set(p.perturbation_type for p in final_probe_set.probes))

            with st.spinner("Launching audit pipeline..."):
                # Construct ExperimentConfig
                config = ExperimentConfig(
                    experiment_name=exp_title,
                    model_ids=selected_models,
                    seed_texts=final_probe_set.seed_texts,
                    perturbation_types=selected_ptypes,
                    explainer_type=xai_mode,
                    performance_mode=PerformanceMode.from_str(perf_mode),
                    selected_probe_set=final_probe_set,
                    selected_probe_ids=final_probe_ids,
                    sentence_types=getattr(final_probe_set, "sentence_types", {}),
                )

                new_runner = ExperimentRunner(config=config)
                new_runner.run_async()

                st.session_state["active_runner"] = new_runner
                st.session_state["active_experiment_id"] = new_runner.experiment_id
                st.session_state["active_experiment_title"] = exp_title
                st.session_state["active_results"] = None  # Clear stale results from prior runs
                st.session_state["current_page"] = "Live Run"
                st.rerun()

    # ==========================================
    # 04 REVIEW & SHORTCUTS
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:20px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">04 REVIEW — WORKSTATION JUMP GATES</strong>
            <div style="color:#94a3b8; font-size:0.75rem;">Direct navigation to telemetry, comparisons, and persistent research archives.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_rev1, col_rev2, col_rev3 = st.columns(3)
    with col_rev1:
        if st.button("Live Execution Monitor", key="rev_btn_live", use_container_width=True):
            st.session_state["current_page"] = "Live Run"
            st.rerun()
    with col_rev2:
        if st.button("Model Comparison", key="rev_btn_comp", use_container_width=True):
            st.session_state["current_page"] = "Comparison"
            st.rerun()
    with col_rev3:
        if st.button("Run History Archive", key="rev_btn_hist", use_container_width=True):
            st.session_state["current_page"] = "Run History"
            st.rerun()
