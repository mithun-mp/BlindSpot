import json

with open("runs/exp_1790826791_038a27/results.json", "r", encoding="utf-8") as f:
    d = json.load(f)

m = d["models"]["distilbert-base-uncased-finetuned-sst-2-english"]
exp = m["explanations"][0]

attn_orig = exp.get("attention_orig", {})
print("ATTENTION ORIG TOKENS:")
for r in attn_orig.get("token_attributions", []):
    print(f"  pos={r.get('position')} tok={r.get('token')} attr={r.get('attribution')} ({r.get('attribution')*100:.2f}%)")

attn_pert = exp.get("attention_pert", {})
print("ATTENTION PERT TOKENS:")
for r in attn_pert.get("token_attributions", []):
    print(f"  pos={r.get('position')} tok={r.get('token')} attr={r.get('attribution')} ({r.get('attribution')*100:.2f}%)")
