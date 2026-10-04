"""
Reusable UI Components for BlindSpot Research Workstation.
Provides technical workstation headers, telemetry badges, model cards,
evidence-based failure records, terminal log lines, and prediction cards.
"""
import os
import re
import time
import html
import difflib
from typing import Dict, Any, Optional, List, Tuple

import streamlit as st
import pandas as pd

from blindspot.core.types import PredictionResult, FailureCategory
from blindspot.core.config import AttributionThresholds
from blindspot.execution.resources import ResourceManager


def render_workstation_header(system_status: str = "READY", active_runs: int = 0) -> None:
    """
    Renders top persistent technical workstation header with live hardware telemetry,
    status badges, and active run counters with zero hardcoded dummy values.
    """
    telemetry = ResourceManager.get_live_telemetry()
    cpu = telemetry["cpu"]
    ram = telemetry["ram"]
    net = telemetry["network"]

    cpu_pct = cpu["percent"]
    cpu_cores = cpu["logical_cores"]
    cpu_phys = cpu["physical_cores"]

    ram_pct = ram["percent"]
    ram_used = ram["used_gb"]
    ram_total = ram["total_gb"]

    net_down = f"{net['speed_down_kbps']:.0f}KB/s" if net['speed_down_kbps'] < 1024 else f"{net['speed_down_kbps']/1024:.1f}MB/s"
    net_up = f"{net['speed_up_kbps']:.0f}KB/s" if net['speed_up_kbps'] < 1024 else f"{net['speed_up_kbps']/1024:.1f}MB/s"

    status_color = "#10b981" if system_status == "READY" else ("#38bdf8" if system_status == "RUNNING" else "#f59e0b")

    header_html = f"""
    <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:10px 16px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
        <div>
            <div style="font-size:1.15rem; font-weight:700; letter-spacing:0.04em; color:#f1f5f9; display:inline-block;">
                BLINDSPOT <span style="font-size:0.8rem; font-weight:400; color:#38bdf8; margin-left:6px; border:1px solid #0284c7; padding:1px 6px; border-radius:3px;">WORKSTATION</span>
            </div>
            <div style="font-size:0.75rem; color:#94a3b8; letter-spacing:0.02em; margin-top:2px;">
                Multimodel Behavioral & Explainability Auditing Platform
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span style="background:#1a2030; border:1px solid #26334d; border-radius:4px; padding:3px 8px; font-size:0.75rem; font-family:monospace; color:#e2e8f0;">
                <span style="color:{status_color}; font-weight:bold;">●</span> {system_status.upper()}
            </span>
            <span style="background:#1a2030; border:1px solid #26334d; border-radius:4px; padding:3px 8px; font-size:0.75rem; font-family:monospace; color:#cbd5e1;">
                CPU: <strong style="color:#f1f5f9;">{cpu_pct:.0f}%</strong> ({cpu_phys}p/{cpu_cores}c)
            </span>
            <span style="background:#1a2030; border:1px solid #26334d; border-radius:4px; padding:3px 8px; font-size:0.75rem; font-family:monospace; color:#cbd5e1;">
                RAM: <strong style="color:#f1f5f9;">{ram_pct:.0f}%</strong>
            </span>
            <span style="background:#1a2030; border:1px solid #26334d; border-radius:4px; padding:3px 8px; font-size:0.75rem; font-family:monospace; color:#cbd5e1;">
                NET: <strong style="color:#38bdf8;">↓{net_down}</strong> <strong style="color:#a855f7;">↑{net_up}</strong>
            </span>
            <span style="background:#1a2030; border:1px solid #26334d; border-radius:4px; padding:3px 8px; font-size:0.75rem; font-family:monospace; color:#cbd5e1;">
                RUNS: <strong style="color:#38bdf8;">{active_runs}</strong>
            </span>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_technical_model_card(
    model_id: str,
    architecture: str = "Transformer",
    num_classes: int = 2,
    params_millions: Optional[float] = None,
    task: str = "Sentiment Classification",
    is_cached: bool = False,
    is_selected: bool = False,
    device: str = "cpu",
) -> None:
    """Renders structured technical model profile card."""
    card_border = "#38bdf8" if is_selected else "#26334d"
    card_bg = "#162238" if is_selected else "#141824"
    cache_badge = "<span style='background:#064e3b; color:#34d399; padding:2px 6px; border-radius:3px; font-size:0.7rem;'>LOADED</span>" if is_cached else "<span style='background:#1e293b; color:#94a3b8; padding:2px 6px; border-radius:3px; font-size:0.7rem;'>STANDBY</span>"
    param_text = f"{params_millions:.1f}M" if params_millions else "Unknown"

    html = f"""
    <div style="background:{card_bg}; border:1px solid {card_border}; border-radius:6px; padding:12px 14px; margin-bottom:8px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="color:#f1f5f9; font-size:0.95rem; font-family:monospace;">{model_id}</strong>
            {cache_badge}
        </div>
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:6px; margin-top:8px; font-size:0.75rem; color:#94a3b8; font-family:monospace;">
            <div>Arch: <span style="color:#e2e8f0;">{architecture}</span></div>
            <div>Classes: <span style="color:#e2e8f0;">{num_classes}</span></div>
            <div>Params: <span style="color:#e2e8f0;">{param_text}</span></div>
            <div>Device: <span style="color:#e2e8f0;">{device.upper()}</span></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_probe_preview_card(
    probe_id: str,
    original_text: str,
    perturbed_text: str,
    perturbation_type: str,
    expected_semantic_effect: str,
    expected_flip: bool,
) -> None:
    """Renders controlled linguistic probe preview with stable ID and explicit expectations."""
    flip_badge = "<span style='background:#991b1b; color:#fca5a5; padding:1px 6px; border-radius:3px; font-size:0.7rem;'>EXPECT FLIP</span>" if expected_flip else "<span style='background:#064e3b; color:#34d399; padding:1px 6px; border-radius:3px; font-size:0.7rem;'>PRESERVE</span>"

    html = f"""
    <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:10px 14px; margin-bottom:8px; font-family:monospace; font-size:0.8rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <span style="color:#38bdf8; font-weight:bold;">{probe_id}</span>
            <div style="display:flex; gap:6px;">
                <span style="background:#1e293b; color:#cbd5e1; padding:1px 6px; border-radius:3px; font-size:0.7rem;">{perturbation_type.upper()}</span>
                <span style="background:#1e293b; color:#cbd5e1; padding:1px 6px; border-radius:3px; font-size:0.7rem;">{expected_semantic_effect.upper()}</span>
                {flip_badge}
            </div>
        </div>
        <div style="color:#94a3b8; margin:2px 0;">ORIG: <span style="color:#e2e8f0;">{original_text}</span></div>
        <div style="color:#38bdf8; margin:2px 0;">PERT: <span style="color:#f8fafc; font-weight:600;">{perturbed_text}</span></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_prediction_card(result: PredictionResult, title: Optional[str] = None) -> None:
    """
    Renders standardized model prediction block with exact two-decimal confidence percentage,
    full normalized class probability distribution, dense ASCII/meter visualization,
    execution latency, active device, and operational model status.
    """
    header = title or (f"MODEL: {result.model_id}" if result.model_id else "MODEL PREDICTION")
    
    st.markdown(f"### {header}")
    st.markdown("────────────────────────────────────────")
    
    col_meta1, col_meta2, col_meta3 = st.columns(3)
    with col_meta1:
        st.caption(f"**Device:** `{result.device.upper()}`")
    with col_meta2:
        st.caption(f"**Latency:** `{result.latency_ms:.1f} ms`")
    with col_meta3:
        status_color = "#10b981" if result.model_status == "READY" else "#f59e0b"
        st.markdown(
            f"**Status:** <span style='background-color:{status_color}; color:white; padding:2px 8px; border-radius:4px; font-size:0.8em;'>{result.model_status}</span>",
            unsafe_allow_html=True
        )

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(
            label="Prediction",
            value=result.label,
        )
        st.metric(
            label="Confidence",
            value=result.formatted_confidence,
        )

    with col2:
        st.markdown("**Probability Distribution:**")
        # Visual block meters
        for cls_name, prob in result.probabilities.items():
            pct = prob * 100.0
            col_lbl, col_bar, col_pct = st.columns([2, 5, 2])
            with col_lbl:
                st.markdown(f"**{cls_name}**")
            with col_bar:
                st.progress(min(1.0, max(0.0, prob)))
            with col_pct:
                st.markdown(f"`{pct:6.2f}%`")

    with st.expander("Dense Workstation Telemetry", expanded=False):
        st.code(
            f"MODEL: {result.model_id or 'unknown'}\n"
            f"────────────────────────────\n"
            f"Prediction: {result.label}\n"
            f"Confidence: {result.formatted_confidence}\n\n"
            f"Probability Distribution:\n"
            f"{result.formatted_distribution_ascii}\n\n"
            f"Device: {result.device.upper()} | Latency: {result.latency_ms:.2f} ms | Status: {result.model_status}",
            language="text"
        )


# Syntactic and Semantic Operator Sets for In-Context Failure Attribution Highlighting
_NEGATION_OPERATORS = {
    "not", "never", "no", "n't", "neither", "nor", "hardly", "barely",
    "scarcely", "without", "cannot", "cant", "wont", "isnt", "arent",
    "wasnt", "werent", "dont", "doesnt", "didnt"
}

_CONNECTIVE_OPERATORS = {
    "but", "however", "although", "despite", "whereas", "while", "yet", "though"
}

_DEGREE_OPERATORS = {
    "very", "extremely", "absolutely", "slightly", "somewhat", "barely",
    "totally", "deeply", "immensely", "exceptionally", "really", "fairly",
    "quite", "hugely", "terribly", "incredibly", "remarkably", "substantially"
}

# Centralized operational blindness threshold (magnitude below which operator is unrepresented/ignored)
BLIND_THRESHOLD: float = AttributionThresholds().operator_min_abs  # Centralized: 0.05


def _analyze_and_highlight_tokens(
    orig_text: str,
    pert_text: str,
    category: str,
    evidence: Optional[Dict[str, Any]] = None,
    delta_pts: float = 0.0,
) -> Tuple[str, str, List[Dict[str, Any]], List[str]]:
    """
    Analyzes token-level shifts between original and perturbed inputs, identifying
    blinded operators, spurious triggers, and misweighted attributions.
    Produces HTML with styled highlight badges and extracts comparative token weight breakdown.
    """
    evidence = evidence or {}

    # Word tokenization preserving boundaries
    orig_tokens = re.findall(r"\b[\w']+\b|[^\w\s]|\s+", orig_text)
    pert_tokens = re.findall(r"\b[\w']+\b|[^\w\s]|\s+", pert_text)

    clean_orig = [t.lower().strip() for t in orig_tokens if re.match(r"[\w']+", t)]
    clean_pert = [t.lower().strip() for t in pert_tokens if re.match(r"[\w']+", t)]

    # Sequence alignment to detect modified, deleted, or inserted words
    sm = difflib.SequenceMatcher(None, clean_orig, clean_pert)
    diff_orig_words = set()
    diff_pert_words = set()

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            for w in clean_orig[i1:i2]:
                diff_orig_words.add(w)
        if tag in ("replace", "insert"):
            for w in clean_pert[j1:j2]:
                diff_pert_words.add(w)

    # Resolve token attributions if available
    token_weights_map: Dict[str, float] = {}

    # 0. Check probe bundle explanations for independent LIME / SHAP
    if "probe" in evidence and isinstance(evidence["probe"], dict):
        p_exps = evidence["probe"].get("explanations", {})
        l_tw = p_exps.get("lime", {}).get("token_weights", {})
        if l_tw:
            for k, v in l_tw.items():
                k_str = k[0] if isinstance(k, (tuple, list)) else str(k)
                token_weights_map[str(k_str).lower()] = float(v)

    # 1. From top_attributions
    if not token_weights_map:
        top_attribs = evidence.get("top_attributions", [])
        if isinstance(top_attribs, list):
            for item in top_attribs:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    k_str = item[0][0] if isinstance(item[0], (tuple, list)) else str(item[0])
                    token_weights_map[str(k_str).lower()] = float(item[1])
                elif isinstance(item, dict):
                    k = item.get("token") or item.get("word")
                    v = item.get("weight") or item.get("score")
                    if k is not None and v is not None:
                        k_str = k[0] if isinstance(k, (tuple, list)) else str(k)
                        token_weights_map[str(k_str).lower()] = float(v)

    # 2. From pert_explanation in evidence
    if not token_weights_map and "pert_explanation" in evidence:
        p_exp = evidence["pert_explanation"]
        if isinstance(p_exp, dict):
            tw = p_exp.get("token_weights", {})
            if isinstance(tw, dict):
                for k, v in tw.items():
                    k_str = k[0] if isinstance(k, (tuple, list)) else str(k)
                    token_weights_map[str(k_str).lower()] = float(v)

    # 3. Track whether attribution data is from a real explainer or heuristic fallback
    has_real_attributions = bool(token_weights_map)
    if not token_weights_map:
        # Only mark diff/operator tokens for visual highlighting, but flag as estimated
        for w in clean_pert:
            w_l = w.lower()
            if w_l in diff_pert_words or w_l in _NEGATION_OPERATORS or w_l in _CONNECTIVE_OPERATORS:
                token_weights_map[w_l] = 0.0  # Placeholder for highlighting only

    # Max weight for intensity normalization
    max_w = max([abs(v) for v in token_weights_map.values()], default=1.0)
    if max_w <= 0.001:
        max_w = 1.0

    # Format Original HTML
    orig_html_parts = []
    for token in orig_tokens:
        clean_t = token.lower().strip()
        escaped_t = html.escape(token)
        if clean_t in diff_orig_words:
            orig_html_parts.append(
                f'<span style="background:rgba(56, 189, 248, 0.2); border-bottom:2px dashed #38bdf8; color:#f1f5f9; padding:1px 3px; border-radius:2px;" title="Original Anchor Token">{escaped_t}</span>'
            )
        else:
            orig_html_parts.append(escaped_t)
    highlighted_orig = "".join(orig_html_parts)

    # Format Perturbed HTML with Category-Specific Highlights
    pert_html_parts = []
    flagged_tokens: List[str] = []
    breakdown_rows: List[Dict[str, Any]] = []

    # Extract relevant operator tokens from existing evidence and metadata
    ev_operator_tokens = set()
    if isinstance(evidence, dict):
        for op in evidence.get("operator_tokens") or []:
            ev_operator_tokens.add(str(op).lower().strip())
        tax_ev = evidence.get("taxonomy_evidence")
        if isinstance(tax_ev, dict):
            for op in tax_ev.get("operator_tokens") or []:
                ev_operator_tokens.add(str(op).lower().strip())
        probe_meta = evidence.get("probe")
        if isinstance(probe_meta, dict):
            for op in probe_meta.get("operator_tokens") or []:
                ev_operator_tokens.add(str(op).lower().strip())
            if isinstance(probe_meta.get("metadata"), dict):
                for op in probe_meta["metadata"].get("operator_tokens") or []:
                    ev_operator_tokens.add(str(op).lower().strip())

    for token in pert_tokens:
        clean_t = token.lower().strip()
        escaped_t = html.escape(token)
        is_diff = clean_t in diff_pert_words or clean_t in _NEGATION_OPERATORS or clean_t in _CONNECTIVE_OPERATORS or clean_t in _DEGREE_OPERATORS
        w = token_weights_map.get(clean_t, 0.0)
        intensity = min(1.0, max(0.15, abs(w) / max_w))

        # Check if token is a recognized operator from evidence or canonical operator sets
        is_operator = (
            clean_t in ev_operator_tokens
            or clean_t in _NEGATION_OPERATORS
            or clean_t in _CONNECTIVE_OPERATORS
        )
        is_blinded_operator = (
            category == "Blind"
            and is_operator
            and (abs(w) < BLIND_THRESHOLD)
        )

        if is_blinded_operator:
            # Highlight Blinded Operator in red
            flagged_tokens.append(clean_t)
            # Issue 4 fix: use actual weight in badge instead of hardcoded ~0.00
            weight_label = f"{w:+.2f}" if has_real_attributions else "N/A"
            pert_html_parts.append(
                f'<span style="background:rgba(239, 68, 68, 0.35); border:1px solid #ef4444; color:#fca5a5; padding:2px 7px; border-radius:4px; font-weight:bold; text-decoration:line-through;" title="BLINDED OPERATOR: Ignored by attention heads">{escaped_t}</span> '
                f'<span style="font-size:0.75rem; color:#ef4444; font-weight:bold; border:1px solid #ef4444; padding:1px 6px; border-radius:3px; background:#2a1215;">[BLINDED: {weight_label} Weight]</span>'
            )
            # Issue 5 fix: show actual shift and data source
            if has_real_attributions:
                pert_weight_str = f"{w:+.2f} (Suppressed)"
                shift_str = f"{abs(w):.2f} Attribution Weight"
                status_str = "BLINDED (Low Attribution Allocation)"
            else:
                pert_weight_str = "No data (Explainer not run)"
                shift_str = "No attribution data"
                status_str = "BLINDED (No explainer data available)"
            breakdown_rows.append({
                "token": clean_t,
                "orig_weight": "—",
                "pert_weight": pert_weight_str,
                "shift": shift_str,
                "expected": "Invert Polarity (-Δ)",
                "intensity": intensity,
                "status": status_str,
            })

        elif category == "Spurious" and (clean_t in diff_pert_words or is_diff):
            # Highlight Spurious Trigger in amber
            flagged_tokens.append(clean_t)
            pert_html_parts.append(
                f'<span style="background:rgba(245, 158, 11, 0.35); border:1px solid #f59e0b; color:#fde68a; padding:2px 7px; border-radius:4px; font-weight:bold;" title="SPURIOUS TRIGGER: Semantic-preserving token caused flip">{escaped_t}</span> '
                f'<span style="font-size:0.75rem; color:#f59e0b; font-weight:bold; border:1px solid #f59e0b; padding:1px 6px; border-radius:3px; background:#291e0a;">[SPURIOUS TRIGGER: Unwarranted Sensitivity]</span>'
            )
            # Issue 3 fix: don't fabricate baseline weights
            if has_real_attributions:
                pert_weight_str = f"{w:+.2f}"
            else:
                pert_weight_str = "No data"
            breakdown_rows.append({
                "token": clean_t,
                "orig_weight": "—",
                "pert_weight": pert_weight_str,
                "shift": f"{w:+.2f}" if has_real_attributions else "No attribution data",
                "expected": "Invariant (Preserve)",
                "intensity": intensity,
                "status": "SPURIOUS SENSITIVITY (Unwarranted Vector Shift)",
            })

        elif category == "Misweighted" and (is_diff or abs(w) >= 0.25):
            # Highlight according to intensity in purple/magenta
            flagged_tokens.append(clean_t)
            alpha_bg = 0.25 + 0.65 * intensity
            alpha_border = 0.4 + 0.6 * intensity
            pert_html_parts.append(
                f'<span style="background:rgba(168, 85, 247, {alpha_bg:.2f}); border:1px solid rgba(168, 85, 247, {alpha_border:.2f}); color:#ffffff; padding:2px 7px; border-radius:4px; font-weight:bold;" title="Attribution Intensity: {intensity:.0%} (Weight: {w:+.2f})">{escaped_t} <span style="font-size:0.72rem; opacity:0.9;">({w:+.2f})</span></span>'
            )
            # Issue 3 fix: don't fabricate baseline weights
            breakdown_rows.append({
                "token": clean_t,
                "orig_weight": "—",
                "pert_weight": f"{w:+.2f}" if has_real_attributions else "No data",
                "shift": f"{w:+.2f}" if has_real_attributions else "No attribution data",
                "expected": "Degree Calibration",
                "intensity": intensity,
                "status": f"MISWEIGHTED ({intensity:.0%} Intensity)",
            })

        elif abs(w) >= 0.30:
            # Secondary token with noticeable weight highlighted in subtle emerald or rose according to sign
            alpha_bg = 0.15 + 0.5 * intensity
            badge_c = "#10b981" if w >= 0 else "#ef4444"
            pert_html_parts.append(
                f'<span style="background:rgba({16 if w >= 0 else 239}, {185 if w >= 0 else 68}, {129 if w >= 0 else 68}, {alpha_bg:.2f}); border:1px solid {badge_c}; color:#ffffff; padding:1px 5px; border-radius:3px; font-size:0.85em;" title="Token Weight: {w:+.2f}">{escaped_t} <span style="font-size:0.7rem; opacity:0.85;">({w:+.2f})</span></span>'
            )
        else:
            pert_html_parts.append(escaped_t)

    highlighted_pert = "".join(pert_html_parts)
    return highlighted_orig, highlighted_pert, breakdown_rows, flagged_tokens


def render_failure_record(failure: Dict[str, Any], idx: int = 0) -> None:
    """
    Renders structured scientific evidence record for a failure taxonomy diagnosis.
    Features:
    - Side-by-side color-coded comparative flip cards (Blue for Target Contract; Red for Wrong / Green for Preserved-with-Misweighted).
    - In-context token highlighting:
        - BLIND: highlighted operator token in red badge (e.g. 'not' with '[BLINDED: ~0.00 Weight]').
        - SPURIOUS: highlighted trigger token in amber badge (e.g. 'decent' with '[SPURIOUS TRIGGER]').
        - MISWEIGHTED: multiple tokens highlighted according to intensity gradient in purple.
    - Expandable Deep-Dive diagnostic breakdown with comparative token weights table, intensity bars, causal narrative, remedies, and raw evidence payload.
    """
    category = failure.get("category", "Undetermined")
    model_id = failure.get("model_id", "Unknown")
    probe_id = failure.get("probe_id", failure.get("probe_type", "P_UNK"))
    probe_type = failure.get("probe_type", "Linguistic Probe")
    orig_text = failure.get("original_sentence", "")
    pert_text = failure.get("perturbed_sentence", "")
    orig_label = failure.get("original_label", "")
    pert_label = failure.get("perturbed_label", "")
    expected_flip = failure.get("expected_flip", True)
    is_flipped = failure.get("is_flipped", False)
    orig_conf = float(failure.get("original_confidence", 1.0))
    pert_conf = float(failure.get("perturbed_confidence", 1.0))
    delta_pts = float(failure.get("confidence_delta_pts", 0.0))
    semantic_intent = failure.get("semantic_intent", "")
    details = failure.get("details", "")
    recommendation = failure.get("recommendation", "Inspect model attention distribution.")
    evidence = failure.get("evidence", {})

    badge_color = {
        FailureCategory.BLIND.value: "#ef4444",
        FailureCategory.SPURIOUS.value: "#f97316",
        FailureCategory.MISWEIGHTED.value: "#a855f7",
        FailureCategory.UNDETERMINED.value: "#64748b",
    }.get(category, "#64748b")

    # ==========================================
    # 1. Resolve Expected vs Predicted Targets
    # ==========================================
    orig_label_clean = (orig_label or "POSITIVE").upper()
    pert_label_clean = (pert_label or "POSITIVE").upper()
    sem_ref = failure.get("semantic_reference") or failure.get("evidence", {}).get("semantic_reference") or {}
    sem_pol = sem_ref.get("final_semantic_polarity", "")
    sem_rel = sem_ref.get("semantic_relation_to_baseline", "")

    if not sem_pol and isinstance(failure.get("evidence"), dict):
        sem_pol = failure["evidence"].get("target_polarity", "")
        sem_rel = failure["evidence"].get("expected_effect", "")

    if sem_pol and sem_pol.upper() not in ("UNAVAILABLE", "NONE"):
        expected_target_label = sem_pol.upper()
        if sem_rel and sem_rel.upper() not in ("UNAVAILABLE", "NONE", "—"):
            expected_badge_text = f"EXPECTED {sem_rel.upper()}"
            expected_badge_bg = "#0284c7" if ("REVERSE" in sem_rel.upper() or "SHIFT" in sem_rel.upper()) else "#334155"
        else:
            expected_badge_text = f"EXPECTED {sem_pol.upper()}"
            expected_badge_bg = "#0284c7"
    elif expected_flip:
        if orig_label_clean == "POSITIVE":
            expected_target_label = "NEGATIVE"
        elif orig_label_clean == "NEGATIVE":
            expected_target_label = "POSITIVE"
        else:
            expected_target_label = "DIFFERENT_LABEL"
        expected_badge_text = "EXPECTED POLARITY FLIP"
        expected_badge_bg = "#0284c7"
    elif semantic_intent in ("PRESERVE_POLARITY", "PRESERVE_MEANING"):
        expected_target_label = orig_label_clean
        expected_badge_text = "EXPECTED POLARITY PRESERVE"
        expected_badge_bg = "#334155"
    else:
        expected_target_label = "UNDETERMINED"
        expected_badge_text = "UNDETERMINED CONTRACT"
        expected_badge_bg = "#64748b"

    expected_transition_text = f"{orig_label_clean} → {expected_target_label}"
    predicted_transition_text = f"{orig_label_clean} → {pert_label_clean}"

    # Determine Predicted Card Styling:
    # Rule: If flip didn't happen but still misweighted -> GREEN card with misweighted note.
    # If prediction was wrong (Blind missing flip or Spurious unexpected flip) -> RED card.
    if category == "Misweighted" and not is_flipped:
        pred_card_bg = "#06281e"
        pred_card_border = "#10b981"
        pred_card_text = "#6ee7b7"
        pred_status_badge = '<span style="background:#065f46; color:#a7f3d0; padding:2px 7px; border-radius:3px; font-size:0.7rem; font-weight:bold;">✓ LABEL PRESERVED</span>'
        pred_subnote = f'<div style="color:#f59e0b; font-size:0.75rem; margin-top:5px; font-weight:bold;">⚠️ Weights / Confidence Misweighted ({delta_pts:+.2f} pp)</div>'
    elif pert_label_clean == expected_target_label:
        pred_card_bg = "#06281e"
        pred_card_border = "#10b981"
        pred_card_text = "#6ee7b7"
        pred_status_badge = '<span style="background:#065f46; color:#a7f3d0; padding:2px 7px; border-radius:3px; font-size:0.7rem; font-weight:bold;">✓ SATISFIES LABEL CONTRACT</span>'
        pred_subnote = f'<div style="color:#10b981; font-size:0.75rem; margin-top:5px;">Confidence: {orig_conf:.1%} → {pert_conf:.1%} ({delta_pts:+.2f} pp)</div>'
    else:
        # Wrong prediction! Red card
        pred_card_bg = "#261214"
        pred_card_border = "#ef4444"
        pred_card_text = "#fca5a5"
        if category == "Blind":
            badge_label = "✕ MISSING FLIP — OPERATOR BLINDED"
        elif category == "Spurious":
            badge_label = "✕ UNEXPECTED FLIP — SPURIOUS SENSITIVITY"
        else:
            badge_label = "✕ UNEXPECTED TRANSITION"
        pred_status_badge = f'<span style="background:#7f1d1d; color:#fecaca; padding:2px 7px; border-radius:3px; font-size:0.7rem; font-weight:bold;">{badge_label}</span>'
        pred_subnote = f'<div style="color:#fca5a5; font-size:0.75rem; margin-top:5px;">Confidence Shift: {orig_conf:.1%} → {pert_conf:.1%} ({delta_pts:+.2f} pp)</div>'

    # Analyze and highlight tokens
    highlighted_orig, highlighted_pert, breakdown_rows, flagged_tokens = _analyze_and_highlight_tokens(
        orig_text=orig_text,
        pert_text=pert_text,
        category=category,
        evidence=evidence,
        delta_pts=delta_pts,
    )

    # ==========================================
    # 2. Render Main Failure Card Header & Grid
    # ==========================================
    st.markdown(
        f"""
        <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:14px 18px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="background:{badge_color}; color:#ffffff; font-weight:bold; padding:3px 9px; border-radius:3px; font-size:0.8rem; font-family:monospace;">
                        {category.upper()}
                    </span>
                    <span style="color:#cbd5e1; font-weight:600; font-family:monospace; font-size:0.85rem;">Model: <strong style="color:#f1f5f9;">{model_id}</strong></span>
                </div>
                <div style="font-family:monospace; font-size:0.8rem; color:#94a3b8;">
                    Probe: <span style="color:#38bdf8; font-weight:bold;">{probe_id}</span> ({probe_type})
                </div>
            </div>
            <!-- Comparative Expected vs Predicted Cards -->
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:12px;">
                <!-- Expected Contract Card (Blue) -->
                <div style="background:#0c192c; border:1px solid #38bdf8; border-radius:6px; padding:12px 14px; min-height:115px; font-family:monospace;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#94a3b8; font-size:0.75rem;">TARGET CONTRACT (EXPECTED)</span>
                        <span style="background:{expected_badge_bg}; color:#ffffff; padding:2px 7px; border-radius:3px; font-size:0.7rem; font-weight:bold;">{expected_badge_text}</span>
                    </div>
                    <div style="color:#38bdf8; font-size:1.25rem; font-weight:bold; margin-top:6px;">{expected_transition_text}</div>
                    <div style="color:#cbd5e1; font-size:0.75rem; margin-top:4px;">Intent: <span style="color:#f1f5f9; font-weight:600;">{semantic_intent or sem_rel or ('REVERSE_POLARITY' if expected_flip else ('PRESERVE_MEANING' if expected_target_label == orig_label_clean else 'SHIFT'))}</span></div>
                    <div style="color:#64748b; font-size:0.7rem; margin-top:2px;">Semantic Invariance / Inversion Criterion</div>
                </div>
                <!-- Predicted Transition Card (Color Coded Red or Green) -->
                <div style="background:{pred_card_bg}; border:1px solid {pred_card_border}; border-radius:6px; padding:12px 14px; min-height:115px; font-family:monospace;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#94a3b8; font-size:0.75rem;">OBSERVED MODEL PREDICTION</span>
                        {pred_status_badge}
                    </div>
                    <div style="color:{pred_card_text}; font-size:1.25rem; font-weight:bold; margin-top:6px;">{predicted_transition_text}</div>
                    {pred_subnote}
                    <div style="color:#64748b; font-size:0.7rem; margin-top:2px;">Empirical Classifier Output Transition</div>
                </div>
            </div>
            <!-- In-Context Sentence Displays with Inline Token Highlights -->
            <div style="background:#0b0e14; border:1px solid #1e2638; border-radius:4px; padding:10px 14px; margin-bottom:10px; font-family:monospace; font-size:0.85rem; line-height:1.6;">
                <div style="color:#94a3b8;">ORIGINAL: <span style="color:#f1f5f9;">"{highlighted_orig}"</span></div>
                <div style="color:#38bdf8; margin-top:6px;">PERTURBED: <span style="color:#ffffff;">"{highlighted_pert}"</span></div>
            </div>
            <!-- Quick Summary -->
            <div style="color:#cbd5e1; font-size:0.85rem; line-height:1.45; margin-bottom:4px;">
                <strong style="color:#38bdf8;">Evidence Summary:</strong> {details}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ==========================================
    # 3. Expandable More Option (Deep Diagnostic Breakdown)
    # ==========================================
    with st.expander(f"🔍 Deep Diagnostic Breakdown & Attributions — {category.upper()} (#{idx + 1})", expanded=False):
        st.markdown(
            f"""
            <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 16px; margin-bottom:12px;">
                <div style="color:#f1f5f9; font-size:0.95rem; font-weight:bold; margin-bottom:4px;">
                    Taxonomy Diagnostic Causality: <span style="color:{badge_color};">{category.upper()} FAILURE</span>
                </div>
                <div style="color:#cbd5e1; font-size:0.85rem; line-height:1.5;">
                    {failure.get('reason', details)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Scientific Taxonomy Evidence (Sections 14, 27, 29)
        tax_ev = evidence.get("taxonomy_evidence")
        if tax_ev and isinstance(tax_ev, dict):
            op_tokens = tax_ev.get("operator_tokens", [])
            op_type = tax_ev.get("operator_type", "linguistic operator")
            lime_diag = tax_ev.get("lime", {})
            shap_diag = tax_ev.get("shap", {})
            l_op_w = lime_diag.get("operator_weight")
            s_op_w = shap_diag.get("operator_weight")
            l_op_str = f"{l_op_w:+.4f}" if isinstance(l_op_w, (int, float)) else str(l_op_w or "N/A")
            s_op_str = f"{s_op_w:+.4f}" if isinstance(s_op_w, (int, float)) else str(s_op_w or "N/A")
            l_dom_c = lime_diag.get("dominant_competitor", "None")
            l_dom_w = lime_diag.get("dominant_competitor_weight")
            l_dom_str = f"{l_dom_w:+.4f}" if isinstance(l_dom_w, (int, float)) else str(l_dom_w or "N/A")
            s_dom_c = shap_diag.get("dominant_competitor", "None")
            s_dom_w = shap_diag.get("dominant_competitor_weight")
            s_dom_str = f"{s_dom_w:+.4f}" if isinstance(s_dom_w, (int, float)) else str(s_dom_w or "N/A")

            st.markdown(
                f"""
                <div style="background:#0b0f19; border:1px solid #334155; border-radius:6px; padding:12px 14px; margin-bottom:12px; font-family:monospace; font-size:0.83rem;">
                    <div style="color:#38bdf8; font-weight:bold; font-size:0.88rem; margin-bottom:6px;">
                        🔬 SCIENTIFIC TAXONOMY EVIDENCE (INDEPENDENT LIME & SHAP)
                    </div>
                    <div style="color:#cbd5e1; margin-bottom:8px;">
                        <strong>Operator Tokens:</strong> <span style="background:#1e293b; color:#38bdf8; padding:2px 8px; border-radius:3px; font-weight:bold;">{', '.join(op_tokens) if op_tokens else 'None detected'}</span>
                        &nbsp; <span style="color:#64748b;">(Operator Type: {op_type})</span>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                        <div style="background:#141824; border:1px solid #1e2638; border-radius:4px; padding:8px 10px;">
                            <div style="color:#38bdf8; font-weight:bold; font-size:0.8rem; margin-bottom:4px;">LIME SURROGATE EVIDENCE</div>
                            <div style="color:#94a3b8; font-size:0.78rem;">Operator Attribution: <strong style="color:#f1f5f9;">{l_op_str}</strong></div>
                            <div style="color:#94a3b8; font-size:0.78rem;">Dominant Competitor: <strong style="color:#f59e0b;">{l_dom_c}</strong> ({l_dom_str})</div>
                            <div style="color:#64748b; font-size:0.72rem;">Stopword Attribution Ratio: {float(lime_diag.get('stopword_ratio', 0.0)):.1%}</div>
                        </div>
                        <div style="background:#141824; border:1px solid #1e2638; border-radius:4px; padding:8px 10px;">
                            <div style="color:#a855f7; font-weight:bold; font-size:0.8rem; margin-bottom:4px;">SHAP KERNEL EVIDENCE</div>
                            <div style="color:#94a3b8; font-size:0.78rem;">Operator Attribution: <strong style="color:#f1f5f9;">{s_op_str}</strong></div>
                            <div style="color:#94a3b8; font-size:0.78rem;">Dominant Competitor: <strong style="color:#f59e0b;">{s_dom_c}</strong> ({s_dom_str})</div>
                            <div style="color:#64748b; font-size:0.72rem;">Stopword Attribution Ratio: {float(shap_diag.get('stopword_ratio', 0.0)):.1%}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Quality & Counterfactual diagnostic badges (Phases 8, 14)
            eq = evidence.get("explanation_quality") or tax_ev.get("explanation_quality") or {}
            cf = evidence.get("counterfactual_analysis") or tax_ev.get("counterfactual_analysis") or {}

            eq_status = eq.get("quality_status", "VALID") if isinstance(eq, dict) else "VALID"
            sign_agr = eq.get("cross_explainer_sign_agreement") if isinstance(eq, dict) else None
            sign_str = f"{sign_agr:.1%}" if isinstance(sign_agr, (int, float)) else "N/A"

            cf_supp = cf.get("counterfactual_support") if isinstance(cf, dict) else None
            if eq or cf:
                cf_badge = '<span style="color:#10b981; font-weight:bold;">CONFIRMED (Restored Target Direction)</span>' if cf_supp else ('<span style="color:#f59e0b;">INCONCLUSIVE</span>' if cf_supp is not None else '<span style="color:#64748b;">N/A</span>')
                st.markdown(
                    f"""
                    <div style="background:#0f172a; border:1px solid #1e293b; border-radius:4px; padding:8px 12px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; font-size:0.78rem;">
                        <div>
                            <span style="color:#94a3b8;">Explanation Reliability:</span> <strong style="color:#38bdf8;">{eq_status}</strong>
                            <span style="color:#64748b; margin-left:8px;">(Sign Agreement: {sign_str})</span>
                        </div>
                        <div>
                            <span style="color:#94a3b8;">Counterfactual Operator Ablation:</span> {cf_badge}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Baseline vs Probe Dual-Explainer Table (Section 6 & 18)
        aligned_mm = evidence.get("aligned_multimodel")
        if aligned_mm and isinstance(aligned_mm, list):
            st.markdown(
                """
                <div style="font-family:monospace; font-size:0.8rem; font-weight:bold; color:#cbd5e1; margin:10px 0 6px 0;">
                    📊 DUAL-EXPLAINER BASELINE VS PROBE TOKEN ATTRIBUTIONS (LIME & SHAP)
                </div>
                """,
                unsafe_allow_html=True,
            )
            mm_table_rows = []
            for r in aligned_mm:
                tok_name = r.get("token", "")
                occ = r.get("pert_occ") or r.get("orig_occ") or 1
                tot = r.get("total_occ", 1)
                tok_disp = f"{tok_name} (#{occ})" if tot > 1 else tok_name

                orig_l = f"{r.get('orig_lime'):+.4f}" if r.get('orig_lime') is not None else "—"
                orig_s = f"{r.get('orig_shap'):+.4f}" if r.get('orig_shap') is not None else "—"
                pert_l = f"{r.get('pert_lime'):+.4f}" if r.get('pert_lime') is not None else "—"
                pert_s = f"{r.get('pert_shap'):+.4f}" if r.get('pert_shap') is not None else "—"
                d_l = f"{r.get('delta_lime'):+.4f}" if r.get('delta_lime') is not None else "—"
                d_s = f"{r.get('delta_shap'):+.4f}" if r.get('delta_shap') is not None else "—"

                role = "OPERATOR" if r.get("is_operator") else r.get("status", "aligned").upper()

                mm_table_rows.append({
                    "Token": tok_disp,
                    "Baseline LIME": orig_l,
                    "Baseline SHAP": orig_s,
                    "Probe LIME": pert_l,
                    "Probe SHAP": pert_s,
                    "Δ LIME": d_l,
                    "Δ SHAP": d_s,
                    "Status": role,
                })
            st.dataframe(pd.DataFrame(mm_table_rows), use_container_width=True, hide_index=True)

        # Comparative Feature Weights Table (Especially for Misweighted, Blind, and Spurious)
        if breakdown_rows:
            st.markdown(
                """
                <div style="font-family:monospace; font-size:0.8rem; font-weight:bold; color:#cbd5e1; margin-bottom:6px;">
                    FEATURE WEIGHT & ATTRIBUTION SHIFT BREAKDOWN (ACTUAL VS EXPECTED)
                </div>
                """,
                unsafe_allow_html=True,
            )

            for b_row in breakdown_rows:
                token_name = b_row["token"]
                orig_w = b_row["orig_weight"]
                pert_w = b_row["pert_weight"]
                shift_w = b_row["shift"]
                exp_eff = b_row["expected"]
                status_txt = b_row["status"]
                intens_val = b_row["intensity"]

                st.markdown(
                    f"""
                    <div style="background:#0f172a; border-left:3px solid {badge_color}; border-radius:0 4px 4px 0; padding:8px 12px; margin-bottom:6px; font-family:monospace; font-size:0.82rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                        <div>
                            <span style="background:#1e293b; color:#38bdf8; padding:2px 8px; border-radius:3px; font-weight:bold;">{token_name}</span>
                            &nbsp; <span style="color:#94a3b8;">Original:</span> <strong style="color:#f1f5f9;">{orig_w}</strong>
                            &nbsp;→&nbsp; <span style="color:#94a3b8;">Probe:</span> <strong style="color:{badge_color};">{pert_w}</strong>
                            &nbsp; <span style="color:#64748b;">(Shift: {shift_w})</span>
                        </div>
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span style="color:#94a3b8;">Expected: <strong style="color:#38bdf8;">{exp_eff}</strong></span>
                            <span style="background:rgba(168,85,247,0.2); border:1px solid #a855f7; color:#f3e8ff; padding:1px 6px; border-radius:3px; font-size:0.75rem;">{intens_val:.0%} Intensity</span>
                            <span style="color:{badge_color}; font-weight:bold; font-size:0.75rem;">{status_txt}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Actionable Remediation
        st.markdown(
            f"""
            <div style="background:#1e293b; border-left:3px solid #38bdf8; padding:8px 12px; border-radius:0 4px 4px 0; color:#cbd5e1; font-size:0.82rem; margin-top:10px;">
                <strong style="color:#38bdf8;">Model Hardening & Remediation Advice:</strong> {recommendation}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Raw Evidence Payload Toggle
        if evidence:
            st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
            with st.expander("Inspect Raw JSON Evidence Payload", expanded=False):
                st.json(evidence)

    st.markdown("<div style='margin-bottom:14px;'></div>", unsafe_allow_html=True)


def render_console_log_line(timestamp_str: str, level: str, subsystem: str, message: str) -> None:
    """Renders formatted technical monospace log entry with severity and subsystem tags."""
    level_color = {
        "INFO": "#94a3b8",
        "SUCCESS": "#10b981",
        "WARNING": "#f59e0b",
        "ERROR": "#ef4444",
        "DEBUG": "#64748b",
    }.get(level.upper(), "#94a3b8")

    subsystem_color = {
        "BOOT": "#38bdf8",
        "UI": "#a855f7",
        "MODEL": "#3b82f6",
        "CACHE": "#10b981",
        "RUNNER": "#ec4899",
        "PROBE": "#eab308",
        "XAI": "#6366f1",
        "RESOURCE": "#14b8a6",
        "STORAGE": "#8b5cf6",
        "REPORT": "#06b6d4",
    }.get(subsystem.upper(), "#94a3b8")

    st.markdown(
        f"""
        <div style="font-family:'JetBrains Mono', Consolas, monospace; font-size:0.8rem; line-height:1.5; margin:1px 0; white-space:pre-wrap; word-break:break-all;">
            <span style="color:#64748b;">[{timestamp_str}]</span>
            <span style="color:{level_color}; font-weight:bold; display:inline-block; width:65px;">{level.upper()}</span>
            <span style="color:{subsystem_color}; font-weight:bold; display:inline-block; width:80px;">[{subsystem.upper()}]</span>
            <span style="color:#e2e8f0;">{message}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_empty_state(
    title: str,
    message: str,
    action_label: Optional[str] = None,
    action_key: Optional[str] = None,
) -> bool:
    """
    Renders clean, helpful empty state container with explanation and optional CTA button.
    Returns True if action button is clicked.
    """
    st.markdown(
        f"""
        <div style="background:#141824; border:1px dashed #26334d; border-radius:6px; padding:32px 20px; text-align:center; margin:20px 0;">
            <div style="font-size:1.1rem; font-weight:700; color:#f1f5f9; margin-bottom:8px;">{title}</div>
            <div style="color:#94a3b8; font-size:0.875rem; max-width:480px; margin:0 auto 16px auto; line-height:1.5;">{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if action_label:
        col_pad1, col_btn, col_pad2 = st.columns([2, 2, 2])
        with col_btn:
            return st.button(action_label, key=action_key, type="primary", use_container_width=True)
    return False


def render_failure_badge(category: str) -> None:
    """Renders visual badge for 4-way taxonomy failure category."""
    color_map = {
        FailureCategory.BLIND.value: "#ef4444",
        FailureCategory.SPURIOUS.value: "#f97316",
        FailureCategory.MISWEIGHTED.value: "#a855f7",
        FailureCategory.UNDETERMINED.value: "#64748b",
    }
    bg_color = color_map.get(category, "#64748b")
    st.markdown(
        f"<span style='background-color: {bg_color}; color: white; padding: 2px 8px; "
        f"border-radius: 3px; font-size: 0.8em; font-weight: bold; font-family: monospace;'>{category}</span>",
        unsafe_allow_html=True,
    )


def render_provenance_badge(explainer_used: str, fallback_used: bool = False, runtime_ms: float = 0.0) -> None:
    """Renders provenance tag indicating if native LIME/SHAP or LOO fallback was used."""
    if fallback_used:
        badge_html = (
            f"<span style='background-color: #9a3412; color: #ffedd5; padding: 2px 8px; "
            f"border-radius: 3px; font-size: 0.75em; font-family: monospace;'>FALLBACK: {explainer_used} ({runtime_ms:.1f}ms)</span>"
        )
    else:
        badge_html = (
            f"<span style='background-color: #065f46; color: #d1fae5; padding: 2px 8px; "
            f"border-radius: 3px; font-size: 0.75em; font-family: monospace;'>NATIVE: {explainer_used} ({runtime_ms:.1f}ms)</span>"
        )
    st.markdown(badge_html, unsafe_allow_html=True)


def render_markdown_with_images(content: str, base_dir: str = "runs"):
    """
    Renders markdown content in Streamlit. If local image references ![alt](path)
    are detected, renders them using st.image so they display properly in the browser.
    """
    img_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    last_idx = 0

    for match in img_pattern.finditer(content):
        pre_text = content[last_idx:match.start()].strip()
        if pre_text:
            st.markdown(pre_text)

        alt_text = match.group(1)
        img_rel_path = match.group(2).replace("\\", "/")
        img_full_path = os.path.join(base_dir, img_rel_path) if not os.path.isabs(img_rel_path) else img_rel_path

        if os.path.exists(img_full_path):
            st.image(img_full_path, caption=alt_text or os.path.basename(img_full_path), use_container_width=True)
        else:
            st.markdown(match.group(0))

        last_idx = match.end()

    remaining = content[last_idx:].strip()
    if remaining:
        st.markdown(remaining)


def render_gemini_usage_card(
    ref_set: Optional[Any] = None,
    requests_count: int = 0,
    cache_hits: int = 0,
    annotated_count: int = 0,
    failures: int = 0,
    retries: int = 0,
) -> None:
    """Renders persistent usage and telemetry panel for Gemini Semantic Reference (Section 20)."""
    if ref_set is not None:
        cache_hits = getattr(ref_set, "cache_hits", 0)
        requests_count = getattr(ref_set, "api_requests", 0)
        annotated_count = len(getattr(ref_set, "probe_annotations", {})) + 1
        est_tokens = (requests_count * 350) + (annotated_count * 45)
    else:
        est_tokens = (requests_count * 350) + (annotated_count * 45)

    html = f"""
    <div style="background:#0f172a; border:1px solid #1e293b; border-radius:6px; padding:10px 14px; margin:10px 0 14px 0; font-family:monospace; font-size:0.8rem;">
        <div style="color:#38bdf8; font-weight:bold; margin-bottom:6px;">⚡ GEMINI SEMANTIC REFERENCE USAGE</div>
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:8px; color:#94a3b8;">
            <div>Requests this experiment: <strong style="color:#f1f5f9;">{requests_count}</strong></div>
            <div>Cache hits: <strong style="color:#10b981;">{cache_hits}</strong></div>
            <div>Sentences annotated: <strong style="color:#e2e8f0;">{annotated_count}</strong></div>
            <div>API failures: <strong style="color:#e2e8f0;">{failures}</strong></div>
            <div>Retries: <strong style="color:#e2e8f0;">{retries}</strong></div>
            <div>Estimated tokens: <strong style="color:#e2e8f0;">~{est_tokens}</strong></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_semantic_reference_panel(
    ref_set: Any,
    interactive: bool = True,
    key_prefix: str = "sem_panel",
) -> None:
    """
    Renders dedicated Semantic Reference card and Human Verification / Override controls
    per Sections 4, 7, 9, 21, 27 of prompt.
    """
    if ref_set is None:
        st.info("Semantic reference set is not yet established.")
        return

    base_annot = getattr(ref_set, "baseline_annotation", None)
    if not base_annot:
        return

    is_online = getattr(ref_set, "annotation_engine", "manual") == "gemini"
    status_label = "Connected" if is_online else "Offline (Manual Mode)"
    status_color = "#10b981" if is_online else "#f59e0b"
    model_name = getattr(ref_set, "model", "manual")
    frozen_status = "🔒 FROZEN" if getattr(ref_set, "frozen", False) else "🔓 ACTIVE"

    provider_name = getattr(base_annot, "provider", "NONE")
    if provider_name == "GEMINI" or is_online:
        disp_provider = "Google Gemini"
    elif provider_name == "LOCAL_HEURISTIC":
        disp_provider = "Local Heuristic"
    else:
        disp_provider = "Manual"

    disp_provider = "Google Gemini" if (provider_name == "GEMINI" or is_online) else ("Local Heuristic" if provider_name == "LOCAL_HEURISTIC" else "Manual")

    actual_base_conf = base_annot.gemini_confidence if getattr(base_annot, "gemini_confidence", None) is not None else getattr(base_annot, "confidence", None)
    base_conf_html = f"<div>Confidence: <strong style='color:#e2e8f0;'>{actual_base_conf*100:.0f}%</strong></div>" if (actual_base_conf is not None and isinstance(actual_base_conf, (int, float)) and actual_base_conf > 0) else ""

    is_base_unavailable = (getattr(base_annot, "status", "AVAILABLE") == "UNAVAILABLE" or getattr(base_annot, "final_semantic_polarity", None) is None)
    base_v_status = base_annot.verification_status.value if hasattr(base_annot.verification_status, "value") else str(base_annot.verification_status)
    is_base_accepted = (base_v_status in ["HUMAN_VERIFIED", "VERIFIED", "HUMAN_OVERRIDDEN"])

    if is_base_unavailable:
        disp_base_status = "UNAVAILABLE"
        base_status_color = "#ef4444"
        base_ref_title = "Semantic Reference Unavailable"
        base_pol_html = 'Semantic Polarity: <strong style="color:#ef4444;">UNAVAILABLE</strong>'
        base_reason_html = f"<div>Reason: <span style='color:#f87171;'>{base_annot.failure_reason}</span></div>" if getattr(base_annot, "failure_reason", None) else "<div>Reason: <span style='color:#f87171;'>API Unavailable</span></div>"
    else:
        disp_base_status = "OVERRIDDEN" if base_v_status == "HUMAN_OVERRIDDEN" else ("ACCEPTED" if is_base_accepted else "UNVERIFIED")
        base_status_color = "#38bdf8" if base_v_status == "HUMAN_OVERRIDDEN" else ("#10b981" if is_base_accepted else "#f59e0b")
        base_ref_title = "Human-Overridden Semantic Reference" if base_v_status == "HUMAN_OVERRIDDEN" else ("Human-Verified Semantic Reference" if is_base_accepted else "Semantic Reference (Unverified)")
        base_pol_html = f'Semantic Polarity: <strong style="color:var(--bs-accent, #38bdf8);">{base_annot.final_semantic_polarity.value}</strong>'
        base_reason_html = ""

    def _strip_markdown_code_divs(raw_html: str) -> str:
        return "\n".join(l.strip() for l in raw_html.strip().splitlines() if l.strip())

    # Baseline Card
    base_card_html = f"""
<div style="background:var(--bs-surface-1, #0b1329); border:1px solid var(--bs-border, #1e3a8a); border-radius:6px; padding:12px 16px; margin:12px 0 14px 0;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
<span style="font-size:0.85rem; font-weight:bold; color:var(--bs-accent, #60a5fa); font-family:monospace;">
BASELINE SEMANTIC REFERENCE
</span>
<span style="font-size:0.75rem; font-family:monospace; color:var(--bs-text-secondary, #cbd5e1);">
Status: <strong style="color:{base_status_color};">{disp_base_status}</strong>
</span>
</div>
<div style="font-size:0.9rem; color:var(--bs-text-primary, #f1f5f9); margin-bottom:8px;">
"{base_annot.sentence_text}"
</div>
<div style="font-family:monospace; font-size:0.8rem; color:var(--bs-text-secondary, #94a3b8); display:flex; gap:16px; flex-wrap:wrap; align-items:center;">
<div>{base_pol_html}</div>
<div>Source: <span style="color:var(--bs-text-primary, #e2e8f0);">{disp_provider}</span></div>
{base_conf_html}
{base_reason_html}
<div>Classification: <strong style="color:#10b981;">{base_ref_title}</strong></div>
</div>
</div>
"""
    st.markdown(_strip_markdown_code_divs(base_card_html), unsafe_allow_html=True)

    # Baseline Controls (Global Accept 1 of 2 + Polarity Change Buttons)
    if interactive and not getattr(ref_set, "frozen", False):
        b_col1, b_col2, b_col3, b_col4 = st.columns(4)
        with b_col1:
            if is_base_accepted:
                st.markdown(
                    """<style>
                    div[data-testid="stColumn"]:nth-of-type(1) button[kind="primary"] {
                        background-color: #10b981 !important;
                        border-color: #10b981 !important;
                        color: #ffffff !important;
                    }
                    div[data-testid="stColumn"]:nth-of-type(1) button[kind="primary"]:hover {
                        background-color: #059669 !important;
                        border-color: #059669 !important;
                    }
                    </style>""",
                    unsafe_allow_html=True,
                )
                base_btn_name = "✓ Accepted"
            else:
                base_btn_name = "✓ Accept Baseline"

            if st.button(base_btn_name, key=f"{key_prefix}_accept_base", type="primary", use_container_width=True):
                base_annot.accept_gemini()
                ref_set._recompute_relations()
                st.rerun()
        base_cur_pol = getattr(base_annot.final_semantic_polarity, "value", str(base_annot.final_semantic_polarity))
        with b_col2:
            lbl_pos = "● POSITIVE" if base_cur_pol == "POSITIVE" else "Change to POSITIVE"
            if st.button(lbl_pos, key=f"{key_prefix}_base_pos", use_container_width=True):
                base_annot.override_human("POSITIVE")
                ref_set._recompute_relations()
                st.rerun()
        with b_col3:
            lbl_neg = "● NEGATIVE" if base_cur_pol == "NEGATIVE" else "Change to NEGATIVE"
            if st.button(lbl_neg, key=f"{key_prefix}_base_neg", use_container_width=True):
                base_annot.override_human("NEGATIVE")
                ref_set._recompute_relations()
                st.rerun()
        with b_col4:
            lbl_neu = "● NEUTRAL" if base_cur_pol == "NEUTRAL" else "Change to NEUTRAL"
            if st.button(lbl_neu, key=f"{key_prefix}_base_neu", use_container_width=True):
                base_annot.override_human("NEUTRAL")
                ref_set._recompute_relations()
                st.rerun()

    # Probes Reference List
    probe_annots = getattr(ref_set, "probe_annotations", {})
    num_probes = len(probe_annots)

    with st.expander(f"Inspect Probe Semantic References ({num_probes} probes)", expanded=True):
        # Global Accept 2 of 2 (Accept all probes simultaneously)
        all_probes_accepted = all(
            (getattr(pa.verification_status, "value", str(pa.verification_status)) in ["HUMAN_VERIFIED", "VERIFIED", "HUMAN_OVERRIDDEN"])
            for pa in probe_annots.values()
        ) if probe_annots else False

        if interactive and not getattr(ref_set, "frozen", False) and num_probes > 0:
            if all_probes_accepted:
                probe_btn_label = f"✓ All Probes Accepted ({num_probes})"
                st.markdown(
                    """<style>
                    div[data-testid="stExpander"] button[kind="primary"] {
                        background-color: #10b981 !important;
                        border-color: #10b981 !important;
                        color: #ffffff !important;
                    }
                    div[data-testid="stExpander"] button[kind="primary"]:hover {
                        background-color: #059669 !important;
                        border-color: #059669 !important;
                    }
                    </style>""",
                    unsafe_allow_html=True,
                )
            else:
                probe_btn_label = f"✓ Accept All Probes ({num_probes})"

            if st.button(probe_btn_label, key=f"{key_prefix}_accept_all_probes", type="primary", use_container_width=True):
                for pannot in probe_annots.values():
                    pannot.accept_gemini()
                ref_set._recompute_relations()
                st.rerun()
            st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)

        for pid, pannot in probe_annots.items():
            is_p_unavailable = (getattr(pannot, "status", "AVAILABLE") == "UNAVAILABLE" or getattr(pannot, "final_semantic_polarity", None) is None)
            rel_val = getattr(pannot, "semantic_relation_to_baseline", None)
            if is_p_unavailable or is_base_unavailable or rel_val is None:
                rel_str = "—"
                rel_color = "#94a3b8"
            else:
                rel_str = rel_val.value if hasattr(rel_val, "value") else str(rel_val)
                rel_color = "#10b981"

            if is_p_unavailable:
                p_final = "UNAVAILABLE"
                p_final_color = "#ef4444"
                disp_p_status = "UNAVAILABLE"
                p_status_color = "#ef4444"
            else:
                p_final = pannot.final_semantic_polarity.value if hasattr(pannot.final_semantic_polarity, "value") else str(pannot.final_semantic_polarity)
                p_final_color = "var(--bs-accent, #38bdf8)"
                p_status = pannot.verification_status.value if hasattr(pannot.verification_status, "value") else str(pannot.verification_status)
                is_p_accepted = (p_status in ["HUMAN_VERIFIED", "VERIFIED", "HUMAN_OVERRIDDEN"])
                disp_p_status = "OVERRIDDEN" if p_status == "HUMAN_OVERRIDDEN" else ("ACCEPTED" if is_p_accepted else "UNVERIFIED")
                p_status_color = "#38bdf8" if p_status == "HUMAN_OVERRIDDEN" else ("#10b981" if is_p_accepted else "#f59e0b")

            base_lbl = (
                base_annot.final_semantic_polarity.value
                if (base_annot and getattr(base_annot, "final_semantic_polarity", None))
                else "UNAVAILABLE"
            )

            actual_p_conf = getattr(pannot, "gemini_confidence", None) if getattr(pannot, "gemini_confidence", None) is not None else getattr(pannot, "confidence", None)
            p_conf_html = f"<div>Confidence: <strong style='color:#e2e8f0;'>{actual_p_conf*100:.0f}%</strong></div>" if (actual_p_conf is not None and isinstance(actual_p_conf, (int, float)) and actual_p_conf > 0) else ""

            probe_card_html = f"""
<div style="background:var(--bs-surface-1, #0f172a); border:1px solid var(--bs-border, #1e293b); border-radius:6px; padding:10px 14px; margin-bottom:8px; font-family:monospace; font-size:0.8rem;">
<div style="display:flex; justify-content:space-between; margin-bottom:4px;">
<span style="color:var(--bs-accent, #38bdf8); font-weight:bold;">PROBE: {pid[:10]}</span>
<span style="color:var(--bs-text-secondary, #94a3b8);">Status: <strong style="color:{p_status_color};">{disp_p_status}</strong></span>
</div>
<div style="color:var(--bs-text-primary, #f1f5f9); margin-bottom:6px;">"{pannot.sentence_text}"</div>
<div style="display:flex; gap:16px; flex-wrap:wrap; color:var(--bs-text-secondary, #94a3b8); font-size:0.75rem;">
<div>Baseline: <strong style="color:var(--bs-text-primary, #e2e8f0);">{base_lbl}</strong></div>
<div>Probe Polarity: <strong style="color:{p_final_color};">{p_final}</strong></div>
<div>Relation: <strong style="color:{rel_color};">{rel_str}</strong></div>
{p_conf_html}
</div>
</div>
"""
            st.markdown(_strip_markdown_code_divs(probe_card_html), unsafe_allow_html=True)

            # Preserved POSITIVE, NEGATIVE, NEUTRAL override buttons per probe
            if interactive and not getattr(ref_set, "frozen", False):
                p_c1, p_c2, p_c3 = st.columns(3)
                with p_c1:
                    lbl_ppos = "● POSITIVE" if p_final == "POSITIVE" else "➔ POSITIVE"
                    if st.button(lbl_ppos, key=f"{key_prefix}_pos_{pid}", use_container_width=True):
                        pannot.override_human("POSITIVE")
                        ref_set._recompute_relations()
                        st.rerun()
                with p_c2:
                    lbl_pneg = "● NEGATIVE" if p_final == "NEGATIVE" else "➔ NEGATIVE"
                    if st.button(lbl_pneg, key=f"{key_prefix}_neg_{pid}", use_container_width=True):
                        pannot.override_human("NEGATIVE")
                        ref_set._recompute_relations()
                        st.rerun()
                with p_c3:
                    lbl_pneu = "● NEUTRAL" if p_final == "NEUTRAL" else "➔ NEUTRAL"
                    if st.button(lbl_pneu, key=f"{key_prefix}_neu_{pid}", use_container_width=True):
                        pannot.override_human("NEUTRAL")
                        ref_set._recompute_relations()
                        st.rerun()


