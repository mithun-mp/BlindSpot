import json
from blindspot.explainability.alignment import compute_jaccard_similarity, compute_attribution_cosine
from blindspot.explainability.token_attributions import (
    _normalize_token_records,
    align_token_attributions,
)
from blindspot.ui.explanation_lab import _resolve_active_explanation_data

with open("runs/exp_1790826791_038a27/results.json", "r", encoding="utf-8") as f:
    d = json.load(f)

m_id = "distilbert-base-uncased-finetuned-sst-2-english"
exp_rec = d["models"][m_id]["explanations"][0]

for metric in ["Transformer Attention Weights", "Word Ablation Sensitivity (LOO)"]:
    print(f"\n==================== METRIC: {metric} ====================")
    orig_data, pert_data, aligned_rows, is_attn, is_signed = _resolve_active_explanation_data(
        record=exp_rec,
        selected_model=m_id,
        metric_choice=metric,
    )
    seed_t = exp_rec["seed_text"]
    pert_t = exp_rec["perturbed_text"]

    orig_records = _normalize_token_records(seed_t, orig_data)
    pert_records = _normalize_token_records(pert_t, pert_data)
    aligned_rows = align_token_attributions(seed_t, pert_t, orig_data, pert_data)

    orig_w_dict = {r["token"]: r["attribution"] for r in orig_records}
    pert_w_dict = {r["token"]: r["attribution"] for r in pert_records}
    jaccard = compute_jaccard_similarity(orig_w_dict, pert_w_dict)
    cosine = compute_attribution_cosine(orig_w_dict, pert_w_dict)

    print(f"Jaccard: {jaccard:.3f}, Cosine: {cosine:.3f}")

    print("\nORIGINAL:")
    for r in orig_records:
        score = r["attribution"]
        score_s = f"{score*100.0:4.1f}%" if is_attn else f"{score:+.4f}"
        print(f"  #{r['position']:2d} {r['token']:8s} -> {score_s}")

    print("\nPERTURBED (PROBE):")
    aligned_map = {ar["pert_pos"]: ar for ar in aligned_rows if ar.get("pert_pos") is not None}
    for r in pert_records:
        score = r["attribution"]
        score_s = f"{score*100.0:4.1f}%" if is_attn else f"{score:+.4f}"
        ar = aligned_map.get(r["position"], {})
        stim = " [PROBE STIMULUS]" if ar.get("is_probe_stimulus") else ""
        print(f"  #{r['position']:2d} {r['token']:8s} -> {score_s}{stim}")
