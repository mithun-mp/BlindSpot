"""
Explanation Lab: Feature Attributions, Token Impact, and Explainer Provenance.
Visualizes signed token attribution scores, side-by-side perturbation attribution shifts,
word-by-word sequence weighting, self-attention distributions, and provenance verification.
"""
import os
import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple

from blindspot.ui.components import render_provenance_badge, render_empty_state
from blindspot.storage.run_store import RunStore
from blindspot.explainability.alignment import compute_jaccard_similarity, compute_attribution_cosine
from blindspot.explainability.token_attributions import (
    align_token_attributions,
    extract_words_with_positions,
    _normalize_token_records,
)
from blindspot.explainability.word_ablation import WordAblationExplainer
from blindspot.explainability.attention_explainer import AttentionExplainer
from blindspot.models.cache import ModelCache


def _resolve_active_explanation_data(
    record: Dict[str, Any],
    selected_model: str,
    metric_choice: str,
) -> Tuple[Dict[str, Any], Dict[str, Any], List[Dict[str, Any]], bool, bool]:
    """
    Resolves original and perturbed explanation payloads, alignment rows, and formatting flags
    based on the user's chosen explainability metric.
    Returns: (orig_data, pert_data, aligned_rows, is_attention, is_signed)
    """
    seed_t = record.get("seed_text", "")
    pert_t = record.get("perturbed_text", "")

    if "SHAP" in metric_choice and "LIME" not in metric_choice:
        if "shap_orig" in record and "shap_pert" in record:
            orig_data = record["shap_orig"]
            pert_data = record["shap_pert"]
        else:
            orig_data = record.get("baseline", {}).get("explanations", {}).get("shap", {})
            pert_data = record.get("probe", {}).get("explanations", {}).get("shap", {})
        aligned_rows = align_token_attributions(seed_t, pert_t, orig_data, pert_data)
        return orig_data, pert_data, aligned_rows, False, True

    elif "Ablation" in metric_choice:
        # Check if pre-computed in record
        if "ablation_orig" in record and "ablation_pert" in record:
            orig_data = record["ablation_orig"]
            pert_data = record["ablation_pert"]
            aligned_rows = record.get("ablation_aligned") or align_token_attributions(seed_t, pert_t, orig_data, pert_data)
            return orig_data, pert_data, aligned_rows, False, True

        # Check if model is cached or can be loaded dynamically
        cache = ModelCache.get_shared_cache()
        try:
            model_wrapper = cache.get_or_load(selected_model)
        except Exception:
            model_wrapper = None

        if model_wrapper is not None:
            expl = WordAblationExplainer(model_wrapper)
            orig_exp = expl.explain(seed_t)
            pert_exp = expl.explain(pert_t)
            orig_data = orig_exp.to_dict()
            pert_data = pert_exp.to_dict()
            aligned_rows = align_token_attributions(seed_t, pert_t, orig_exp, pert_exp)
            record["ablation_orig"] = orig_data
            record["ablation_pert"] = pert_data
            record["ablation_aligned"] = aligned_rows
            return orig_data, pert_data, aligned_rows, False, True

        # Fallback to normalized records derived from base explanations
        orig_data = record.get("orig_explanation", {})
        pert_data = record.get("pert_explanation", {})
        aligned_rows = align_token_attributions(seed_t, pert_t, orig_data, pert_data)
        return orig_data, pert_data, aligned_rows, False, True

    elif "Attention" in metric_choice:
        # Check if pre-computed in record
        if "attention_orig" in record and "attention_pert" in record:
            orig_data = record["attention_orig"]
            pert_data = record["attention_pert"]
            aligned_rows = record.get("attention_aligned") or align_token_attributions(seed_t, pert_t, orig_data, pert_data)
            return orig_data, pert_data, aligned_rows, True, False

        # Check if model is cached or can be loaded dynamically
        cache = ModelCache.get_shared_cache()
        try:
            model_wrapper = cache.get_or_load(selected_model)
        except Exception:
            model_wrapper = None

        if model_wrapper is not None:
            expl = AttentionExplainer(model_wrapper)
            orig_exp = expl.explain(seed_t)
            pert_exp = expl.explain(pert_t)
            orig_data = orig_exp.to_dict()
            pert_data = pert_exp.to_dict()
            aligned_rows = align_token_attributions(seed_t, pert_t, orig_exp, pert_exp)
            record["attention_orig"] = orig_data
            record["attention_pert"] = pert_data
            record["attention_aligned"] = aligned_rows
            return orig_data, pert_data, aligned_rows, True, False

        # Fallback
        orig_data = record.get("orig_explanation", {})
        pert_data = record.get("pert_explanation", {})
        aligned_rows = align_token_attributions(seed_t, pert_t, orig_data, pert_data)
        return orig_data, pert_data, aligned_rows, True, False

    else:
        # LIME or Authoritative Multi-Explainer Default
        if "lime_orig" in record and "lime_pert" in record:
            orig_data = record["lime_orig"]
            pert_data = record["lime_pert"]
        elif "orig_explanation" in record:
            orig_data = record.get("orig_explanation", {})
            pert_data = record.get("pert_explanation", {})
        else:
            orig_data = record.get("baseline", {}).get("explanations", {}).get("lime", {})
            pert_data = record.get("probe", {}).get("explanations", {}).get("lime", {})

        aligned_rows = record.get("aligned_multimodel") or record.get("aligned_tokens") or align_token_attributions(seed_t, pert_t, orig_data, pert_data)
        return orig_data, pert_data, aligned_rows, False, True


def render_explanation_lab():
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                TOKEN-LEVEL EXPLAINABILITY & PROVENANCE
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                Model-specific feature attributions (Word Ablation Sensitivity / Transformer Attention / LIME), token weight shifts, and runtime provenance.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    store = RunStore()
    available_runs = [
        r for r in store.list_runs(include_archived=False)
        if os.path.exists(os.path.join(store.get_run_dir(r.get("experiment_id", "")), "results.json"))
    ]

    results = st.session_state.get("active_results")
    if not results:
        runner = st.session_state.get("active_runner")
        if runner and runner.status == "completed" and getattr(runner, "_result", None):
            results = runner._result
            st.session_state["active_results"] = results

    if not results:
        if available_runs:
            st.info("💡 No active experiment in the current browser session. Select and load a completed experiment run below to explore feature attributions:")
            col1, col2 = st.columns([3, 1])
            with col1:
                run_opts = [r["experiment_id"] for r in available_runs]
                selected_run = st.selectbox(
                    "Select Completed Experiment:",
                    options=run_opts,
                    format_func=lambda x: f"{store.get_run_title(x)} ({x})",
                    key="xai_load_run_sel",
                )
            with col2:
                st.write("")
                st.write("")
                if st.button("LOAD RUN", key="xai_btn_load_run", use_container_width=True):
                    run_data = store.load_run(selected_run)
                    if "results" in run_data:
                        st.session_state["active_results"] = run_data["results"]
                        st.session_state["active_experiment_id"] = selected_run
                        st.session_state["active_experiment_title"] = store.get_run_title(selected_run)
                        st.rerun()

            st.markdown("<hr style='border:1px solid #1e293b; margin:20px 0;'>", unsafe_allow_html=True)

        clicked = render_empty_state(
            title="NO EXPLAINABILITY RECORDS LOADED",
            message="No active audit experiment results found in session. Execute an audit with explainability enabled in Experiment Lab or load a completed run.",
            action_label="GO TO EXPERIMENT LAB",
            action_key="xai_empty_to_exp",
        )
        if clicked:
            st.session_state["current_page"] = "Experiment"
            st.rerun()
        return

    # Run switcher header if multiple runs exist
    if available_runs and len(available_runs) > 1:
        current_exp_id = results.get("experiment_id", "")
        with st.expander("🔄 Switch Loaded Experiment Run", expanded=False):
            c_sel1, c_sel2 = st.columns([3, 1])
            with c_sel1:
                run_opts = [r["experiment_id"] for r in available_runs]
                idx = run_opts.index(current_exp_id) if current_exp_id in run_opts else 0
                switch_exp = st.selectbox(
                    "Switch Experiment:",
                    options=run_opts,
                    index=idx,
                    format_func=lambda x: f"{store.get_run_title(x)} ({x})",
                    key="xai_switch_exp",
                )
            with c_sel2:
                st.write("")
                st.write("")
                if st.button("SWITCH RUN", key="xai_btn_switch", use_container_width=True):
                    if switch_exp != current_exp_id:
                        run_data = store.load_run(switch_exp)
                        if "results" in run_data:
                            st.session_state["active_results"] = run_data["results"]
                            st.session_state["active_experiment_id"] = switch_exp
                            st.session_state["active_experiment_title"] = store.get_run_title(switch_exp)
                            st.rerun()

    models_data = results.get("models", {})
    model_ids = list(models_data.keys())

    col_sel1, col_sel2 = st.columns([2, 4])
    with col_sel1:
        selected_model = st.selectbox("Target Model Architecture:", options=model_ids, key="xai_sel_model")

    m_info = models_data.get(selected_model, {})
    explanations = m_info.get("explanations", [])

    if not explanations:
        st.warning(f"No explanation records available for '{selected_model}'. Ensure explainability was enabled during experiment execution.")
        return

    probe_labels = [
        f"Probe #{i + 1}: [{e.get('perturbation_type', 'UNK').upper()}] - {e.get('perturbed_text', '')[:40]}..."
        for i, e in enumerate(explanations)
    ]
    with col_sel2:
        selected_idx = st.selectbox(
            "Select Probe Evaluation Stimulus:",
            options=range(len(probe_labels)),
            format_func=lambda i: probe_labels[i],
            key="xai_sel_probe",
        )

    record = explanations[selected_idx]
    ptype = record.get("perturbation_type", "Unknown")
    seed_t = record.get("seed_text", "")
    pert_t = record.get("perturbed_text", "")

    st.markdown(
        f"""
        <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 16px; margin:14px 0;">
            <div style="font-family:monospace; font-size:0.8rem; color:#38bdf8; font-weight:bold; margin-bottom:6px;">
                EVALUATION CONTEXT: {ptype.upper()}
            </div>
            <div style="font-family:monospace; font-size:0.8rem; color:#94a3b8; margin:3px 0;">
                ORIGINAL: <span style="color:#f1f5f9;">"{seed_t}"</span>
            </div>
            <div style="font-family:monospace; font-size:0.8rem; color:#38bdf8; margin:3px 0;">
                PERTURBED: <span style="color:#ffffff; font-weight:bold;">"{pert_t}"</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================================
    # EXPLAINABILITY CONTROLS: METRIC CHOICE & DISPLAY ORDER
    # =========================================================================
    ctrl_col1, ctrl_col2 = st.columns([1, 1])
    with ctrl_col1:
        metric_choice = st.selectbox(
            "Explainability Metric:",
            options=[
                "Independent LIME & SHAP (Authoritative Multi-Explainer)",
                "LIME Feature Attribution",
                "SHAP Shapley Values",
                "Transformer Attention Weights (Secondary)",
                "Word Ablation Sensitivity (Secondary)",
            ],
            key="xai_metric_choice",
            help="Select the attribution method. LIME and SHAP are the authoritative scientific explainers.",
        )
    with ctrl_col2:
        display_mode = st.radio(
            "Token Display Order:",
            options=[
                "Sentence Sequence Order",
                "Salience Ranking",
            ],
            horizontal=True,
            key="xai_display_mode",
            help="Sentence Sequence Order displays every word in natural order (1..N). Salience Ranking sorts by weight magnitude.",
        )

    # Resolve active explanation payload based on user selection
    orig_data, pert_data, aligned_rows, is_attention, is_signed = _resolve_active_explanation_data(
        record=record,
        selected_model=selected_model,
        metric_choice=metric_choice,
    )

    # Extract sequential normalized token records for both sentences
    orig_records = _normalize_token_records(seed_t, orig_data)
    pert_records = _normalize_token_records(pert_t, pert_data)

    # Reconcile aligned rows with current records
    aligned_rows = align_token_attributions(seed_t, pert_t, orig_data, pert_data)

    # Find key probe stimulus (e.g. 'not')
    probe_stimulus = next((r for r in aligned_rows if r.get("is_probe_stimulus")), None)

    # Dynamic Attribution Alignment Metrics
    orig_w_dict = {r["token"]: r["attribution"] for r in orig_records}
    pert_w_dict = {r["token"]: r["attribution"] for r in pert_records}
    jaccard = compute_jaccard_similarity(orig_w_dict, pert_w_dict)
    cosine = compute_attribution_cosine(orig_w_dict, pert_w_dict)

    col_a1, col_a2, col_a3 = st.columns([1, 1, 1.2])
    with col_a1:
        st.metric(
            label="Attribution Jaccard Similarity",
            value=f"{jaccard:.3f}",
            help="Overlap of top salient feature tokens between original and perturbed text.",
        )
    with col_a2:
        st.metric(
            label="Attribution Cosine Alignment",
            value=f"{cosine:.3f}",
            help="Directional alignment of attribution vectors in feature space.",
        )
    with col_a3:
        if probe_stimulus:
            p_tok = probe_stimulus.get("token", "")
            p_val = probe_stimulus.get("pert_val")
            val_txt = f"{p_val*100.0:.1f}%" if is_attention and p_val is not None else (f"{p_val:+.3f}" if p_val is not None else "N/A")
            st.metric(
                label="Probe Stimulus Detected",
                value=f"'{p_tok}' ({probe_stimulus.get('status', '').upper()})",
                delta=val_txt,
                delta_color="off",
                help="Primary linguistic operator inserted or modified by this probe stimulus.",
            )
        else:
            st.metric(
                label="Probe Alignment Status",
                value=f"{len(aligned_rows)} Tokens Aligned",
                help="All word tokens successfully mapped across original and perturbed sentences.",
            )

    # Compute max absolute value for visual bar normalization
    max_orig = max([abs(r.get("attribution", 0.0)) for r in orig_records], default=1.0)
    max_pert = max([abs(r.get("attribution", 0.0)) for r in pert_records], default=1.0)
    max_scale = max(max_orig, max_pert, 0.0001)

    # =========================================================================
    # SIDE-BY-SIDE ORIGINAL VS PERTURBED ATTRIBUTIONS
    # =========================================================================
    col_orig, col_pert = st.columns(2)

    with col_orig:
        st.markdown("#### ORIGINAL ATTRIBUTION")
        render_provenance_badge(
            explainer_used=orig_data.get("explainer_used", "ablation" if "Ablation" in metric_choice else ("attention" if "Attention" in metric_choice else "lime")),
            fallback_used=orig_data.get("fallback_used", False),
            runtime_ms=orig_data.get("runtime_ms", 0.0),
        )

        if not orig_records:
            st.caption("No token weights extracted.")
        else:
            display_orig = list(orig_records)
            if display_mode == "Salience Ranking":
                display_orig = sorted(display_orig, key=lambda r: abs(r.get("attribution", 0.0)), reverse=True)

            for r in display_orig:
                score = r.get("attribution", 0.0)
                tok = r.get("token", "")
                pos = r.get("position", 1)
                occ = r.get("occurrence", 1)

                if is_attention:
                    bar_color = "#38bdf8"
                    pct = min(100.0, max(4.0, (score / max_scale) * 100.0))
                    score_str = f"{score * 100.0:4.1f}%"
                else:
                    bar_color = "#10b981" if score >= 0 else "#ef4444"
                    pct = min(100.0, max(4.0, (abs(score) / max_scale) * 100.0))
                    score_str = f"{score:+.3f}"

                occ_tag = f" <span style='color:#64748b; font-size:0.7rem;'>#{occ}</span>" if r.get("occurrence", 1) > 1 else ""

                card_html = (
                    f'<div style="display:flex; justify-content:space-between; align-items:center; '
                    f'font-family:monospace; font-size:0.8rem; margin:3px 0; padding:2px 6px; border-radius:4px;">'
                    f'<span style="color:#64748b; font-size:0.75rem; width:28px;">#{pos}</span>'
                    f'<span style="color:#f1f5f9; width:120px; overflow:hidden; text-overflow:ellipsis; font-weight:600;">{tok}{occ_tag}</span>'
                    f'<div style="flex-grow:1; margin:0 8px; background:#1e293b; border-radius:3px; height:8px;">'
                    f'<div style="width:{pct:.1f}%; background:{bar_color}; height:8px; border-radius:3px;"></div>'
                    f'</div>'
                    f'<span style="color:{bar_color}; font-weight:bold; width:60px; text-align:right;">{score_str}</span>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

    with col_pert:
        st.markdown("#### PERTURBED ATTRIBUTION (PROBE)")
        render_provenance_badge(
            explainer_used=pert_data.get("explainer_used", "ablation" if "Ablation" in metric_choice else ("attention" if "Attention" in metric_choice else "lime")),
            fallback_used=pert_data.get("fallback_used", False),
            runtime_ms=pert_data.get("runtime_ms", 0.0),
        )

        if not pert_records:
            st.caption("No token weights extracted.")
        else:
            display_pert = list(pert_records)
            if display_mode == "Salience Ranking":
                display_pert = sorted(display_pert, key=lambda r: abs(r.get("attribution", 0.0)), reverse=True)

            # Map delta and probe stimulus flags from aligned_rows
            aligned_map = {}
            for ar in aligned_rows:
                if ar.get("pert_pos") is not None:
                    aligned_map[ar["pert_pos"]] = ar

            for r in display_pert:
                score = r.get("attribution", 0.0)
                tok = r.get("token", "")
                pos = r.get("position", 1)
                occ = r.get("occurrence", 1)

                ar = aligned_map.get(pos, {})
                is_stimulus = ar.get("is_probe_stimulus", False) or ar.get("status") == "inserted"
                delta = ar.get("delta")

                if is_attention:
                    bar_color = "#38bdf8"
                    pct = min(100.0, max(4.0, (score / max_scale) * 100.0))
                    score_str = f"{score * 100.0:4.1f}%"
                else:
                    bar_color = "#10b981" if score >= 0 else "#ef4444"
                    pct = min(100.0, max(4.0, (abs(score) / max_scale) * 100.0))
                    score_str = f"{score:+.3f}"

                occ_tag = f" <span style='color:#64748b; font-size:0.7rem;'>#{occ}</span>" if r.get("occurrence", 1) > 1 else ""

                if is_stimulus:
                    badge_html = "<span style='background:#f59e0b; color:#0f172a; font-size:0.65rem; font-weight:bold; padding:2px 5px; border-radius:3px; margin-left:6px;'>PROBE</span>"
                    row_bg = "background:rgba(245, 158, 11, 0.12); border:1px solid rgba(245, 158, 11, 0.35);"
                else:
                    badge_html = ""
                    row_bg = "background:transparent;"

                delta_html = ""
                if delta is not None and abs(delta) >= 0.001:
                    if is_attention:
                        d_color = "#38bdf8" if delta >= 0 else "#94a3b8"
                        delta_html = f"<span style='color:{d_color}; font-size:0.7rem; margin-right:4px;'>({delta*100.0:+.1f}%)</span>"
                    else:
                        d_color = "#10b981" if delta > 0 else "#ef4444"
                        delta_html = f"<span style='color:{d_color}; font-size:0.7rem; margin-right:4px;'>({delta:+.2f})</span>"

                card_html = (
                    f'<div style="display:flex; justify-content:space-between; align-items:center; '
                    f'font-family:monospace; font-size:0.8rem; margin:3px 0; padding:2px 6px; border-radius:4px; {row_bg}">'
                    f'<span style="color:#64748b; font-size:0.75rem; width:28px;">#{pos}</span>'
                    f'<span style="color:#f1f5f9; width:120px; overflow:hidden; text-overflow:ellipsis; font-weight:600;">{tok}{occ_tag}{badge_html}</span>'
                    f'<div style="flex-grow:1; margin:0 8px; background:#1e293b; border-radius:3px; height:8px;">'
                    f'<div style="width:{pct:.1f}%; background:{bar_color}; height:8px; border-radius:3px;"></div>'
                    f'</div>'
                    f'{delta_html}'
                    f'<span style="color:{bar_color}; font-weight:bold; width:60px; text-align:right;">{score_str}</span>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

    # =========================================================================
    # ALIGNED PROBE TOKEN SHIFT MATRIX (PROBE FIX INSPECTOR)
    # =========================================================================
    st.markdown("<hr style='border:1px solid #1e293b; margin:24px 0 16px;'>", unsafe_allow_html=True)
    st.markdown("#### 🔬 ALIGNED PROBE TOKEN SHIFT MATRIX")
    st.caption("Word-by-word sequence alignment identifying exact probe insertions, deletions, substitutions, and sensitivity shifts.")

    has_multimodel = any(ar.get("orig_lime") is not None or ar.get("pert_lime") is not None or ar.get("orig_shap") is not None for ar in aligned_rows)
    matrix_rows = []
    for idx, ar in enumerate(aligned_rows):
        tok = ar.get("token") or ar.get("pert_token") or ar.get("orig_token")
        o_pos = f"#{ar['orig_pos']}" if ar.get("orig_pos") is not None else "—"
        p_pos = f"#{ar['pert_pos']}" if ar.get("pert_pos") is not None else "—"
        status = ar.get("status", "aligned").upper()
        if ar.get("is_operator"):
            status_badge = f"🎯 {status} (OPERATOR)"
        elif ar.get("is_probe_stimulus"):
            status_badge = f"🎯 {status} (STIMULUS)"
        elif ar.get("is_key_shift"):
            status_badge = f"⚡ {status} (KEY SHIFT)"
        else:
            status_badge = status

        if has_multimodel and "Independent" in metric_choice:
            orig_l = f"{ar.get('orig_lime'):+.4f}" if ar.get("orig_lime") is not None else "—"
            orig_s = f"{ar.get('orig_shap'):+.4f}" if ar.get("orig_shap") is not None else "—"
            pert_l = f"{ar.get('pert_lime'):+.4f}" if ar.get("pert_lime") is not None else "—"
            pert_s = f"{ar.get('pert_shap'):+.4f}" if ar.get("pert_shap") is not None else "—"
            d_l = f"{ar.get('delta_lime'):+.4f}" if ar.get("delta_lime") is not None else "—"
            d_s = f"{ar.get('delta_shap'):+.4f}" if ar.get("delta_shap") is not None else "—"

            diag = "Perturbation Operator" if ar.get("is_operator") else ("Inserted word" if status == "INSERTED" else "Stable Aligned Word")
            matrix_rows.append({
                "#": idx + 1,
                "Token": tok,
                "Role": status_badge,
                "Base LIME": orig_l,
                "Base SHAP": orig_s,
                "Probe LIME": pert_l,
                "Probe SHAP": pert_s,
                "Δ LIME": d_l,
                "Δ SHAP": d_s,
                "Diagnostic": diag,
            })
        else:
            o_val = ar.get("orig_val")
            p_val = ar.get("pert_val")
            delta = ar.get("delta")

            if is_attention:
                o_str = f"{o_val*100.0:.1f}%" if o_val is not None else "—"
                p_str = f"{p_val*100.0:.1f}%" if p_val is not None else "—"
                d_str = f"{(p_val - o_val)*100.0:+.1f}%" if (o_val is not None and p_val is not None) else "—"
            else:
                o_str = f"{o_val:+.4f}" if o_val is not None else "—"
                p_str = f"{p_val:+.4f}" if p_val is not None else "—"
                d_str = f"{delta:+.4f}" if delta is not None else "—"

            # Diagnostic interpretation
            if status == "INSERTED":
                diag = "New linguistic modifier added by probe"
            elif status == "REMOVED":
                diag = "Original word omitted by probe"
            elif ar.get("polarity_changed"):
                diag = "Sign flipped (+ ↔ -)"
            elif delta is not None and abs(delta) > 0.05:
                diag = "Significant sensitivity shift"
            else:
                diag = "Stable across perturbation"

            matrix_rows.append({
                "#": idx + 1,
                "Token": tok,
                "Orig Pos": o_pos,
                "Probe Pos": p_pos,
                "Probe Status": status_badge,
                "Original Weight": o_str,
                "Probe Weight": p_str,
                "Weight Shift (Δ)": d_str,
                "Diagnostic": diag,
            })

    if matrix_rows:
        df_matrix = pd.DataFrame(matrix_rows)
        st.dataframe(df_matrix, use_container_width=True, hide_index=True)

    # =========================================================================
    # DIAGNOSTIC VISUALIZATIONS
    # =========================================================================
    exp_id = results.get("experiment_id", "")
    fig_dir = os.path.join("runs", exp_id, "figures") if exp_id else ""
    if fig_dir and os.path.exists(fig_dir):
        xai_figs = [
            ("fig05_confidence_delta_by_probe.png", "Figure 5: Confidence Delta by Probe Category"),
            ("fig06_confidence_delta_distribution.png", "Figure 6: Overall Confidence Shift Density"),
            ("attribution_comparison.png", "Token Attribution Shift"),
            ("probe_alignment_summary.png", "Explanation Alignment Across Probes"),
        ]
        available_xai = [f for f, t in xai_figs if os.path.exists(os.path.join(fig_dir, f))]
        if available_xai:
            st.markdown("---")
            with st.expander("📈 Diagnostic Graphs: Attribution Shifts & Confidence Dynamics", expanded=False):
                g_cols = st.columns(2)
                for idx, f_name in enumerate(available_xai):
                    f_title = next(t for f, t in xai_figs if f == f_name)
                    with g_cols[idx % 2]:
                        st.caption(f"**{f_title}**")
                        st.image(os.path.join(fig_dir, f_name), use_container_width=True)
