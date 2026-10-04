"""
Transformer Self-Attention Explainer.
Extracts internal self-attention weights from Hugging Face transformer models across sentence words.
Maps subword tokens to whole words using token character offset mappings.
Normalizes word attention weights to sum to 1.0 (100% attention distribution).
Provides robust heuristic fallback if transformer internals or PyTorch attentions are unavailable.
"""
import time
import re
import numpy as np
from typing import Dict, List, Any, Optional
import logging
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.core.types import ExplanationResult
from blindspot.explainability.token_attributions import extract_words_with_positions, TokenAttributionsDict

logger = logging.getLogger(__name__)


class AttentionExplainer:
    """
    Extracts whole-word self-attention distributions from transformer classification architectures.
    """
    def __init__(self, model_wrapper: HuggingFaceWrapper):
        self.model = model_wrapper

    def explain(self, text: str) -> ExplanationResult:
        """
        Extracts normalized attention weights for each word in the input text in sentence order.
        """
        t0 = time.perf_counter()

        if not text or not text.strip():
            return ExplanationResult(
                token_weights={},
                token_attributions=[],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="attention",
                explainer_used="attention",
                runtime_ms=0.0,
            )

        words_info = extract_words_with_positions(text)
        if not words_info:
            return ExplanationResult(
                token_weights={},
                token_attributions=[],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="attention",
                explainer_used="attention",
                runtime_ms=0.0,
            )

        # Attempt PyTorch transformer attention extraction
        word_scores = None
        fallback_used = False
        fallback_reason = None

        if hasattr(self.model, "pipeline") and self.model.pipeline is not None:
            try:
                import torch
                tok = self.model.pipeline.tokenizer
                mod = self.model.pipeline.model

                if tok is not None and mod is not None:
                    # Tokenize with offsets
                    inputs = tok(text, return_offsets_mapping=True, return_tensors="pt")
                    offset_mapping = inputs.pop("offset_mapping")[0].tolist()

                    # Move tensors to model device
                    device = getattr(mod, "device", "cpu")
                    inputs = {k: v.to(device) for k, v in inputs.items()}

                    mod.eval()
                    with torch.no_grad():
                        outputs = mod(**inputs, output_attentions=True)

                    if hasattr(outputs, "attentions") and outputs.attentions is not None and len(outputs.attentions) > 0:
                        # Extract last layer attention: (batch, num_heads, seq_len, seq_len)
                        last_layer_attn = outputs.attentions[-1][0]
                        # Mean attention from token 0 ([CLS]) across all attention heads
                        cls_attn = last_layer_attn[:, 0, :].mean(dim=0).cpu().numpy()

                        # Map token-level attention to word spans
                        scores = []
                        for w in words_info:
                            w_start, w_end = w["char_start"], w["char_end"]
                            overlapping = []
                            for t_idx, (t_start, t_end) in enumerate(offset_mapping):
                                if t_start == t_end:  # Special token ([CLS], [SEP])
                                    continue
                                if max(w_start, t_start) < min(w_end, t_end):
                                    overlapping.append(cls_attn[t_idx])
                            s = float(np.mean(overlapping)) if overlapping else 0.0
                            scores.append(s)

                        word_scores = scores
                    else:
                        fallback_reason = "Model forward pass did not return attention matrices"
            except Exception as e:
                fallback_reason = str(e)
                logger.debug(f"PyTorch attention extraction failed: {e}. Using salience fallback.")

        # Explicit failure if PyTorch transformer attention is unavailable (Phase 17)
        if word_scores is None:
            runtime_ms = (time.perf_counter() - t0) * 1000.0
            return ExplanationResult(
                token_weights={},
                token_attributions=[],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="attention",
                explainer_used="none",
                fallback_used=False,
                fallback_reason=fallback_reason or "PyTorch attention tensors unavailable",
                runtime_ms=runtime_ms,
                status="ATTENTION_UNAVAILABLE",
                error=fallback_reason or "PyTorch attention tensors unavailable",
            )

        total_score = sum(word_scores)
        if total_score > 0:
            norm_scores = [float(s / total_score) for s in word_scores]
        else:
            norm_scores = [0.0] * len(words_info)

        token_records = []
        weight_map = {}
        for w, s in zip(words_info, norm_scores):
            rec = {
                "token": w["token"],
                "position": w["position"],
                "occurrence": w["occurrence"],
                "attribution": s,
                "attention_weight": s,
                "char_start": w["char_start"],
                "char_end": w["char_end"],
            }
            token_records.append(rec)
            if w["token"] not in weight_map:
                weight_map[w["token"]] = s
            if w["token"].lower() not in weight_map:
                weight_map[w["token"].lower()] = s

        runtime_ms = (time.perf_counter() - t0) * 1000.0
        return ExplanationResult(
            token_weights=TokenAttributionsDict(weight_map, token_records),
            token_attributions=token_records,
            model_id=self.model.model_name,
            text=text,
            explainer_requested="attention",
            explainer_used="attention",
            fallback_used=False,
            fallback_reason=None,
            runtime_ms=runtime_ms,
            status="AVAILABLE",
        )

