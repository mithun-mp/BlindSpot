import json
from blindspot.explainability.token_attributions import extract_words_with_positions

def _normalize_token_records_fixed(text: str, exp) -> list:
    words = extract_words_with_positions(text)
    if not words:
        return []

    existing = None
    if isinstance(exp, dict):
        existing = exp.get("token_attributions")
    elif hasattr(exp, "token_attributions"):
        existing = exp.token_attributions

    if existing:
        if len(existing) == len(words) and all(
            str(existing[i].get("token", "")).lower() == words[i]["token"].lower()
            for i in range(len(words))
        ):
            res = []
            for i, (w_info, r) in enumerate(zip(words, existing)):
                merged = dict(r)
                merged["position"] = w_info["position"]
                merged["occurrence"] = w_info["occurrence"]
                merged["char_start"] = w_info.get("char_start")
                merged["char_end"] = w_info.get("char_end")
                # Ensure attribution is float
                val = merged.get("attribution", merged.get("attention_weight", merged.get("weight", 0.0)))
                merged["attribution"] = float(val) if val is not None else 0.0
                res.append(merged)
            return res

        seen_occ = {}
        lookup = {}
        for r in existing:
            tok = str(r.get("token", "")).lower()
            seen_occ[tok] = seen_occ.get(tok, 0) + 1
            val = r.get("attribution", r.get("attention_weight", r.get("weight", 0.0)))
            lookup[(tok, seen_occ[tok])] = float(val) if val is not None else 0.0
            if tok not in lookup:
                lookup[tok] = float(val) if val is not None else 0.0
    else:
        lookup = {}

    weights_dict = {}
    if isinstance(exp, dict):
        if "token_weights" in exp and isinstance(exp["token_weights"], dict):
            weights_dict = exp["token_weights"]
        else:
            weights_dict = exp
    elif hasattr(exp, "token_weights"):
        weights_dict = exp.token_weights or {}

    records = []
    for w in words:
        tok = w["token"]
        tok_l = tok.lower()
        val = lookup.get((tok_l, w["occurrence"]))
        if val is None:
            val = lookup.get(tok_l)
        if val is None:
            val = weights_dict.get(tok, weights_dict.get(tok_l, 0.0))
        records.append({
            "token": tok,
            "position": w["position"],
            "occurrence": w["occurrence"],
            "attribution": float(val) if val is not None else 0.0,
            "char_start": w.get("char_start"),
            "char_end": w.get("char_end"),
        })
    return records

with open("runs/exp_1790826791_038a27/results.json", "r", encoding="utf-8") as f:
    d = json.load(f)

m = d["models"]["distilbert-base-uncased-finetuned-sst-2-english"]
exp = m["explanations"][0]
seed_t = exp.get("seed_text")
pert_t = exp.get("perturbed_text")
attn_orig = exp.get("attention_orig")
attn_pert = exp.get("attention_pert")

res_o = _normalize_token_records_fixed(seed_t, attn_orig)
print("FIXED records_orig:")
for r in res_o:
    print(f"  #{r['position']} {r['token']:8s} {r['attribution']*100:.1f}%")

res_p = _normalize_token_records_fixed(pert_t, attn_pert)
print("\nFIXED records_pert:")
for r in res_p:
    print(f"  #{r['position']} {r['token']:8s} {r['attribution']*100:.1f}%")
