import json
from blindspot.explainability.token_attributions import _normalize_token_records

with open("runs/exp_1790826791_038a27/results.json", "r", encoding="utf-8") as f:
    d = json.load(f)

m = d["models"]["distilbert-base-uncased-finetuned-sst-2-english"]
exp = m["explanations"][0]
seed_t = exp.get("seed_text")
pert_t = exp.get("perturbed_text")
abl_orig = exp.get("ablation_orig")
abl_pert = exp.get("ablation_pert")

print("ABLATION ORIG:")
for r in _normalize_token_records(seed_t, abl_orig):
    print(f"  #{r['position']} {r['token']:8s} {r['attribution']:+.4f}")

print("\nABLATION PERT:")
for r in _normalize_token_records(pert_t, abl_pert):
    print(f"  #{r['position']} {r['token']:8s} {r['attribution']:+.4f}")
