import sys, os
sys.path.insert(0, os.path.abspath("."))
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from blindspot.explainability.token_attributions import extract_words_with_positions

def get_word_attention(model_name: str, text: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, attn_implementation="eager")
    model.eval()
    
    words = extract_words_with_positions(text)
    inputs = tokenizer(text, return_offsets_mapping=True, return_tensors="pt")
    offset_mapping = inputs.pop("offset_mapping")[0].tolist()
    
    with torch.no_grad():
        outputs = model(**inputs, output_attentions=True)
    
    # outputs.attentions is a tuple of (batch, num_heads, seq_len, seq_len) for each layer
    # Average across all heads in the last layer, or average across all layers & heads:
    # Look at attention from [CLS] (token 0) to each token:
    last_layer_attn = outputs.attentions[-1][0] # (num_heads, seq_len, seq_len)
    cls_attn = last_layer_attn[:, 0, :].mean(dim=0).cpu().numpy() # (seq_len,)
    
    # Map token attention to words
    word_attns = []
    for w in words:
        w_start, w_end = w["char_start"], w["char_end"]
        # Find which tokens overlap with this word
        overlapping_scores = []
        for t_idx, (t_start, t_end) in enumerate(offset_mapping):
            if t_start == t_end: # special token like [CLS], [SEP]
                continue
            # Check overlap
            if max(w_start, t_start) < min(w_end, t_end):
                overlapping_scores.append(cls_attn[t_idx])
        
        score = float(np.mean(overlapping_scores)) if overlapping_scores else 0.0
        word_attns.append(score)
    
    # Normalize word attentions to sum to 1.0 (percentage distribution)
    total_attn = sum(word_attns)
    if total_attn > 0:
        word_attns = [s / total_attn for s in word_attns]
        
    print(f"\n--- Attention for {model_name} on '{text}' ---")
    for w, a in zip(words, word_attns):
        print(f"Word #{w['position']}: '{w['token']}' -> attention: {a*100:.2f}%")

get_word_attention("distilbert-base-uncased-finetuned-sst-2-english", "The movie was great and the acting was top notch.")
get_word_attention("distilbert-base-uncased-finetuned-sst-2-english", "The movie was not great and the acting was top notch.")
