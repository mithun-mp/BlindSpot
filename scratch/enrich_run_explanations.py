import sys, os
sys.path.insert(0, os.path.abspath("."))
import json
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.explainability.word_ablation import WordAblationExplainer
from blindspot.explainability.attention_explainer import AttentionExplainer
from blindspot.explainability.token_attributions import align_token_attributions
from blindspot.explainability.alignment import compute_jaccard_similarity, compute_attribution_cosine

run_path = "runs/exp_1790826791_038a27/results.json"
with open(run_path, "r", encoding="utf-8") as f:
    data = json.load(f)

m_id = "distilbert-base-uncased-finetuned-sst-2-english"
if m_id in data.get("models", {}):
    m_info = data["models"][m_id]
    explanations = m_info.get("explanations", [])
    print(f"Found {len(explanations)} explanations for {m_id}")
    
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
        
        # Also fix the base aligned_tokens to use sequential order
        exp["aligned_tokens"] = align_token_attributions(s_text, p_text, exp.get("orig_explanation"), exp.get("pert_explanation"))
        print(f"Enriched probe #{idx+1}: {exp.get('perturbation_type')}")

with open(run_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
print("Saved enriched run data successfully!")
