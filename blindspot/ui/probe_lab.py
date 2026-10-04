"""
Probe Research Workbench (Probe Lab) for BlindSpot.
Comprehensive interactive environment to generate, inspect, curate, edit,
verify, and stage canonical linguistic probes before experiment execution.
"""
import streamlit as st
import time
from typing import List, Dict, Any, Optional

from blindspot.core.types import (
    LinguisticProbe,
    SharedProbeSet,
    ProbeStatus,
    SemanticIntent,
    SentenceType,
)
from blindspot.perturbations.shared import SharedProbeGenerator, infer_semantic_intent, infer_expected_semantic_effect
from blindspot.perturbations.engine import PerturbationEngine
from blindspot.semantic import get_semantic_service
from blindspot.ui.components import render_semantic_reference_panel

SAMPLE_PRESETS = {
    "Literal": "The movie was great and the acting was top notch.",
    "Proverb": "A rolling stone gathers no moss.",
    "Idiom": "He decided to bite the bullet and finish the work.",
    "Figurative": "Her smile was a ray of sunshine in the dark.",
    "Sarcastic": "Oh fantastic, another flat tire on Monday morning.",
    "Ironic": "The fire station burned down yesterday afternoon.",
}


def render_probe_lab():
    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                🔬 PROBE RESEARCH WORKBENCH
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                Controlled linguistic perturbation catalog. Generate candidates, curate selections, inject custom probes, and stage verified stimuli for multimodel execution.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize workbench session state
    if "workbench_candidates" not in st.session_state:
        st.session_state["workbench_candidates"] = []
    if "workbench_selection" not in st.session_state:
        st.session_state["workbench_selection"] = {}
    if "workbench_seed" not in st.session_state:
        st.session_state["workbench_seed"] = SAMPLE_PRESETS["Literal"]
    if "workbench_sentence_type" not in st.session_state:
        st.session_state["workbench_sentence_type"] = SentenceType.LITERAL.value

    # ==========================================
    # 01 SOURCE SENTENCE & PROBING
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:14px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">01 SOURCE SENTENCE & PROBING</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    seed_text = st.text_input(
        "Source Sentence:",
        value=st.session_state["workbench_seed"],
        key="workbench_seed_input",
    )
    st.session_state["workbench_seed"] = seed_text
    selected_stype = SentenceType.LITERAL.value
    st.session_state["workbench_sentence_type"] = selected_stype

    # Perturbation categories
    col_cat1, col_cat2 = st.columns(2)
    with col_cat1:
        cat_neg = st.checkbox("Negation", value=True, key="wb_cat_neg")
        cat_dneg = st.checkbox("Double Negation", value=True, key="wb_cat_dneg")
        cat_conn = st.checkbox("Connectives", value=True, key="wb_cat_conn")
    with col_cat2:
        cat_syn = st.checkbox("Synonym Substitution", value=True, key="wb_cat_syn")
        cat_int = st.checkbox("Intensity", value=True, key="wb_cat_int")
        cat_cpos = st.checkbox("Contrast Positive", value=True, key="wb_cat_cpos")

    active_cats = []
    if cat_neg: active_cats.append("negation")
    if cat_dneg: active_cats.append("double_negation")
    if cat_conn: active_cats.append("connective")
    if cat_syn: active_cats.append("synonym_substitution")
    if cat_int: active_cats.append("intensity")
    if cat_cpos: active_cats.append("contrast_positive")

    if st.button("Generate Candidate Probes", type="primary", key="btn_wb_generate"):
        if not seed_text.strip():
            st.error("Please enter a valid source sentence.")
        elif not active_cats:
            st.warning("Please select at least one perturbation category.")
        else:
            with st.spinner("Generating controlled perturbations..."):
                gen = SharedProbeGenerator()
                pset = gen.generate_probes(
                    seed_texts=[seed_text.strip()],
                    perturbation_types=active_cats,
                    sentence_types={seed_text.strip(): selected_stype},
                    candidate_count=7,
                )
                st.session_state["workbench_candidates"] = pset.probes
                st.session_state["workbench_selection"] = {p.probe_id: True for p in pset.probes}
                st.success(f"Generated {len(pset.probes)} calibrated candidate probes across {len(active_cats)} categories.")
                st.rerun()

    # ==========================================
    # 02 CANDIDATE PROBES CATALOG
    # ==========================================
    candidates: List[LinguisticProbe] = st.session_state["workbench_candidates"]

    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:20px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">02 CANDIDATE PROBE CATALOG & SELECTION</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not candidates:
        st.info("No probes in catalog yet. Click 'Generate Candidate Probes' above or add custom probes below.")
    else:
        # Summary telemetry
        total_gen = len(candidates)
        total_sel = sum(1 for p in candidates if st.session_state["workbench_selection"].get(p.probe_id, False))
        total_ver = sum(1 for p in candidates if getattr(p, "status", "") == ProbeStatus.VERIFIED.value)

        st.markdown(
            f"""
            <div style="background:var(--bs-surface-2, #0f172a); border:1px solid var(--bs-border, #1e293b); border-radius:6px; padding:12px 16px; margin-bottom:14px; font-family:monospace; font-size:0.85rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>Original Sentence: <strong style="color:var(--bs-text-primary, #f1f5f9);">"{seed_text}"</strong></div>
                <div style="display:flex; gap:16px;">
                    <div>Generated Probes: <strong style="color:var(--bs-text-primary, #e2e8f0);">{total_gen}</strong></div>
                    <div>Selected: <strong style="color:var(--bs-accent, #38bdf8);">{total_sel}</strong></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Render probe items directly with individual tick/untick checkboxes
        displayed_probes = candidates

        for idx, probe in enumerate(displayed_probes):
            is_checked = st.session_state["workbench_selection"].get(probe.probe_id, True)
            border_color = "var(--bs-accent, #38bdf8)" if is_checked else "var(--bs-border, #26334d)"

            with st.container():
                col_chk, col_content = st.columns([1, 15])
                with col_chk:
                    chk_val = st.checkbox(
                        label="Select",
                        value=is_checked,
                        key=f"wb_chk_{probe.probe_id}",
                        label_visibility="collapsed",
                    )
                    if chk_val != is_checked:
                        st.session_state["workbench_selection"][probe.probe_id] = chk_val
                        st.rerun()

                with col_content:
                    st.markdown(
                        f"""
                        <div style="background:var(--bs-surface-1, #141824); border:1px solid {border_color}; border-radius:6px; padding:12px 16px; margin-bottom:10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                                <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
                                    <span style="background:var(--bs-surface-3, #1e2638); border:1px solid var(--bs-border, #334155); padding:2px 7px; border-radius:3px; font-family:monospace; font-size:0.75rem; color:var(--bs-text-secondary, #94a3b8); font-weight:bold;">
                                        #{idx + 1}
                                    </span>
                                    <span style="background:var(--bs-surface-2, #1e293b); color:var(--bs-accent, #38bdf8); font-weight:bold; font-size:0.75rem; padding:2px 8px; border-radius:3px; font-family:monospace;">
                                        {probe.perturbation_type.upper()}
                                    </span>
                                    <span style="background:var(--bs-surface-2, #0f172a); color:var(--bs-text-muted, #64748b); font-size:0.72rem; padding:2px 7px; border-radius:3px; font-family:monospace;">
                                        ID: {probe.probe_id}
                                    </span>
                                </div>
                            </div>
                            <div style="margin-top:6px; font-size:0.92rem; color:var(--bs-text-primary, #f1f5f9); font-family:monospace; line-height:1.45;">
                                {probe.perturbed_text}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # ==========================================
    # 03 ADD CUSTOM LINGUISTIC PROBE
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:20px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">03 CUSTOM PROBE INJECTION</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("+ Create Custom Controlled Probe", expanded=False):
        c_p_seed = st.text_input("Seed Sentence:", value=st.session_state["workbench_seed"], key="custom_p_seed")
        c_p_pert = st.text_input("Perturbed Variant:", placeholder="Enter carefully crafted linguistic variant...", key="custom_p_pert")

        col_cp1, col_cp2, col_cp3 = st.columns(3)
        with col_cp1:
            c_p_type = st.selectbox(
                "Perturbation Category:",
                options=["custom", "negation", "double_negation", "connective", "synonym_substitution", "intensity", "contrast_positive"],
                key="custom_p_type",
            )
        with col_cp2:
            c_p_intent = st.selectbox(
                "Semantic Intent:",
                options=[i.value for i in SemanticIntent],
                key="custom_p_intent",
            )
        with col_cp3:
            c_p_flip = st.selectbox(
                "Expected Flip:",
                options=[False, True],
                format_func=lambda x: "True (Invert Label)" if x else "False (Preserve Label)",
                key="custom_p_flip",
            )

        c_p_desc = st.text_input("Linguistic Rationale / Rule Description:", placeholder="e.g. Injected subtle pragmatic presupposition", key="custom_p_desc")

        if st.button("Add Custom Probe to Catalog", key="btn_add_custom_probe"):
            if not c_p_pert.strip():
                st.error("Please enter a perturbed variant text.")
            else:
                new_probe = LinguisticProbe.create(
                    seed_text=c_p_seed.strip(),
                    perturbed_text=c_p_pert.strip(),
                    perturbation_type=c_p_type,
                    description=c_p_desc.strip() or "Custom user probe",
                    expected_semantic_effect="invert" if c_p_flip else "preserve",
                    expected_flip=bool(c_p_flip),
                    category=c_p_type,
                    name=f"custom_{int(time.time())}",
                    semantic_intent=c_p_intent,
                    status=ProbeStatus.CUSTOM.value,
                    transformation=c_p_desc.strip(),
                )
                st.session_state["workbench_candidates"].append(new_probe)
                st.session_state["workbench_selection"][new_probe.probe_id] = True
                st.success(f"Added custom probe [{new_probe.probe_id[:10]}] to catalog.")
                st.rerun()

    # Edit Existing Probe
    if candidates:
        with st.expander("✏️ Edit Probe Definition", expanded=False):
            probe_options = {f"#{i+1} [{p.perturbation_type.upper()}] {p.perturbed_text[:30]}... ({p.probe_id[:8]})": p for i, p in enumerate(candidates)}
            chosen_lbl = st.selectbox("Select Probe to Edit:", options=list(probe_options.keys()), key="edit_probe_selector")
            target_probe = probe_options[chosen_lbl]

            e_pert = st.text_input("Perturbed Text:", value=target_probe.perturbed_text, key="edit_p_pert")
            e_col1, e_col2, e_col3 = st.columns(3)
            with e_col1:
                cur_cat_idx = ["custom", "negation", "double_negation", "connective", "synonym_substitution", "intensity", "contrast_positive"].index(target_probe.perturbation_type) if target_probe.perturbation_type in ["custom", "negation", "double_negation", "connective", "synonym_substitution", "intensity", "contrast_positive"] else 0
                e_cat = st.selectbox("Category:", options=["custom", "negation", "double_negation", "connective", "synonym_substitution", "intensity", "contrast_positive"], index=cur_cat_idx, key="edit_p_cat")
            with e_col2:
                cur_intent_idx = [i.value for i in SemanticIntent].index(getattr(target_probe, "semantic_intent", SemanticIntent.PRESERVE_MEANING.value)) if getattr(target_probe, "semantic_intent", None) in [i.value for i in SemanticIntent] else 0
                e_intent = st.selectbox("Semantic Intent:", options=[i.value for i in SemanticIntent], index=cur_intent_idx, key="edit_p_intent")
            with e_col3:
                e_flip = st.selectbox("Expected Flip:", options=[False, True], index=1 if target_probe.expected_flip else 0, format_func=lambda x: "True (Invert)" if x else "False (Preserve)", key="edit_p_flip")

            e_desc = st.text_input("Rationale:", value=target_probe.rationale or target_probe.description or "", key="edit_p_desc")

            if st.button("Save Probe Edits (New Version)", key="btn_save_probe_edits"):
                target_probe.perturbed_text = e_pert.strip()
                target_probe.perturbation_type = e_cat
                target_probe.category = e_cat
                target_probe.semantic_intent = e_intent
                target_probe.expected_flip = bool(e_flip)
                target_probe.expected_semantic_effect = "invert" if e_flip else "preserve"
                target_probe.description = e_desc.strip()
                target_probe.rationale = e_desc.strip()
                target_probe.status = ProbeStatus.USER_EDITED.value
                target_probe.probe_version = f"{target_probe.probe_version}-rev"
                st.success(f"Updated probe [{target_probe.probe_id[:10]}] to version {target_probe.probe_version} with status USER_EDITED.")
                st.rerun()

    # ==========================================
    # 03 SEMANTIC GROUND-TRUTH REFERENCE (GEMINI VERIFICATION & HUMAN OVERRIDE)
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:20px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">03 SEMANTIC GROUND-TRUTH REFERENCE (GEMINI VERIFICATION & HUMAN OVERRIDE)</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_probes = [p for p in candidates if st.session_state["workbench_selection"].get(p.probe_id, False)]
    wb_ref_set = st.session_state.get("workbench_semantic_reference")

    if not selected_probes:
        st.info("Select candidate probes above to establish and verify canonical semantic references.")
    else:
        c_sem1, c_sem2 = st.columns([3, 1])
        with c_sem1:
            st.caption("Establish canonical semantic references (POSITIVE, NEGATIVE, NEUTRAL) with Gemini and apply researcher overrides.")
        with c_sem2:
            if st.button("⚡ Annotate / Refresh Semantics", key="btn_wb_annotate_semantics", use_container_width=True):
                with st.spinner("Annotating baseline and selected probes..."):
                    svc = get_semantic_service()
                    wb_ref_set = svc.annotate_experiment(
                        baseline_text=st.session_state["workbench_seed"],
                        probes=selected_probes,
                        force_refresh=True,
                    )
                    st.session_state["workbench_semantic_reference"] = wb_ref_set
                    st.success("Semantic reference established!")
                    st.rerun()

        if wb_ref_set is not None:
            render_semantic_reference_panel(wb_ref_set, interactive=True, key_prefix="wb_sem")

    # ==========================================
    # 04 STAGE PROBE SET FOR EXPERIMENT
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:20px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">04 STAGE PROBE SET FOR EXPERIMENT</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    num_selected = len(selected_probes)

    stage_btn_label = f"Send to Experiment Lab ({num_selected} Selected)" if num_selected > 0 else "Send to Experiment Lab"
    if st.button(stage_btn_label, type="primary", key="btn_wb_stage", use_container_width=True):
        if not selected_probes:
            st.error("Please select at least one probe from the catalog above to stage.")
        else:
            for p in selected_probes:
                p.status = ProbeStatus.VERIFIED.value

            if wb_ref_set is None:
                svc = get_semantic_service()
                wb_ref_set = svc.annotate_experiment(
                    baseline_text=st.session_state["workbench_seed"],
                    probes=selected_probes,
                )
                st.session_state["workbench_semantic_reference"] = wb_ref_set

            if wb_ref_set is not None:
                if hasattr(wb_ref_set, "baseline_annotation") and wb_ref_set.baseline_annotation:
                    v_stat = getattr(wb_ref_set.baseline_annotation, "verification_status", None)
                    v_stat_str = v_stat.value if hasattr(v_stat, "value") else str(v_stat)
                    if v_stat_str == "UNVERIFIED":
                        wb_ref_set.baseline_annotation.accept_gemini()
                for pannot in getattr(wb_ref_set, "probe_annotations", {}).values():
                    pv_stat = getattr(pannot, "verification_status", None)
                    pv_stat_str = pv_stat.value if hasattr(pv_stat, "value") else str(pv_stat)
                    if pv_stat_str == "UNVERIFIED":
                        pannot.accept_gemini()
                if hasattr(wb_ref_set, "_recompute_relations"):
                    wb_ref_set._recompute_relations()

            staged_set = SharedProbeSet(
                probe_set_id=f"pset_{int(time.time())}",
                seed_texts=[st.session_state["workbench_seed"]],
                probes=selected_probes,
                sentence_types={st.session_state["workbench_seed"]: st.session_state["workbench_sentence_type"]},
                created_at=time.time(),
                probe_set_version="2.2.0",
                generator_version="2.2.0",
                semantic_reference_set=wb_ref_set,
            )
            is_valid, issues = staged_set.validate()
            if not is_valid:
                st.error(f"Cannot stage probes due to validation issues:\n- " + "\n- ".join(issues))
            else:
                st.session_state["staged_probe_set"] = staged_set
                st.session_state["exp_seed_text"] = st.session_state["workbench_seed"]
                st.session_state["current_page"] = "Experiment"
                st.rerun()
