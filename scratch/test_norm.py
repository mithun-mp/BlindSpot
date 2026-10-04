import json
from blindspot.explainability.token_attributions import _normalize_token_records

with open("runs/exp_1790826791_038a27/results.json", "r", encoding="utf-8") as f:
    d = json.load(f)

m = d["models"]["distilbert-base-uncased-finetuned-sst-2-english"]
exp = m["explanations"][0]
seed_t = exp.get("seed_text")
pert_t = exp.get("perturbed_text")
attn_orig = exp.get("attention_orig")
attn_pert = exp.get("attention_pert")

print("seed_t:", seed_t)
records_orig = _normalize_token_records(seed_t, attn_orig)
print("records_orig:")
for r in records_orig:
    print(r)

print("\npert_t:", pert_t)
records_pert = _normalize_token_records(pert_t, attn_pert)
print("records_pert:")
for r in records_pert:
    print(r)
