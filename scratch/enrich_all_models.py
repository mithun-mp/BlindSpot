import sys, os
sys.path.insert(0, os.path.abspath("."))
import json
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.explainability.word_ablation import WordAblationExplainer
from blindspot.explainability.attention_explainer import AttentionExplainer
from blindspot.explainability.token_attributions import align_token_attributions

run_path = "runs/exp_1790826791_038a27/results.json"
with open(run_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for m_id, m_info in data.get("models", {}).items():
    explanations = m_info.get("explanations", [])
    if not explanations:
        continue
    # Check if already enriched
    if "ablation_orig" in explanations[0]:
        print(f"Model {m_id} already enriched, skipping.")
        continue
    
    print(f"Enriching {m_id} ({len(explanations)} probes)...")
    try:
        wrapper = HuggingFaceWrapper(m_id)
        abl_exp = WordAblationExplainer(wrapper)
        attn_exp = AttentionExplainer(wrapper)
        
        for idx, exp in enumerate(explanations):
            s_text = exp["seed_text"]
            p_text = exp["perturbed_text"]
            
            abl_orig = abl_exp.explain(s_text)
            abl_pert = abl_exp.explain(p_text)
            attn_orig = attn_exp.explain(s_text)
            attn_pert = attn_exp.explain(p_text)
            
            exp["ablation_orig"] = abl_orig.to_dict()
            exp["ablation_pert"] = abl_pert.to_dict()
            exp["attention_orig"] = attn_orig.to_dict()
            exp["attention_pert"] = attn_pert.to_dict()
            exp["ablation_aligned"] = align_token_attributions(s_text, p_text, abl_orig, abl_pert)
            exp["attention_aligned"] = align_token_attributions(s_text, p_text, attn_orig, attn_pert)
            exp["aligned_tokens"] = align_token_attributions(s_text, p_text, exp.get("orig_explanation"), exp.get("pert_explanation"))
        print(f"Finished {m_id}")
    except Exception as e:
        print(f"Error enriching {m_id}: {e}")

with open(run_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
print("Saved all models to results.json successfully!")
