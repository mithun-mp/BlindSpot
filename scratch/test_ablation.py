import sys, os
sys.path.insert(0, os.path.abspath("."))
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.explainability.token_attributions import extract_words_with_positions
import numpy as np

m = HuggingFaceWrapper('distilbert-base-uncased-finetuned-sst-2-english')

for text in [
    'The movie was great and the acting was top notch.',
    'The movie was not great and the acting was top notch.'
]:
    print(f"\n--- Sentence: '{text}' ---")
    words = extract_words_with_positions(text)
    p0 = m.predict_proba([text])[0]
    top_idx = int(np.argmax(p0))
    top_label = m.labels[top_idx]
    base_score = float(p0[top_idx])
    print(f"Prediction: {top_label} (Confidence: {base_score:.4f})")
    
    masked = []
    for w in words:
        mw = text[:w['char_start']] + text[w['char_end']:]
        masked.append(' '.join(mw.split()))
    
    p_masked = m.predict_proba(masked)
    for w, pm in zip(words, p_masked):
        score = base_score - float(pm[top_idx])
        print(f"Word #{w['position']}: '{w['token']}' (occ {w['occurrence']}) -> weight: {score:+.5f}")
