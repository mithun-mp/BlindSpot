"""
Word-Level Ablation / Leave-One-Out (LOO) Sensitivity Explainer.
Computes the exact signed (+/-) marginal impact on model confidence when each
individual word in the sentence sequence is omitted.
Preserves exact sentence order, token positions (1..N), character offsets,
and multiple occurrences of identical words without overwriting.
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


class WordAblationExplainer:
    """
    Extracts word-level feature importance via Leave-One-Out (LOO) probability delta.
    Evaluates every word in sequential order.
    """
    def __init__(self, model_wrapper: HuggingFaceWrapper):
        self.model = model_wrapper

    def explain(
        self,
        text: str,
        target_class_idx: Optional[int] = None,
    ) -> ExplanationResult:
        """
        Returns ExplanationResult mapping every word in sequence to its signed confidence delta.
        Positive score indicates word supports the predicted class.
        Negative score indicates word opposes the predicted class.
        """
        t0 = time.perf_counter()

        if not text or not text.strip():
            return ExplanationResult(
                token_weights={},
                token_attributions=[],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="ablation",
                explainer_used="word_ablation",
                runtime_ms=0.0,
            )

        words_info = extract_words_with_positions(text)
        if not words_info:
            return ExplanationResult(
                token_weights={},
                token_attributions=[],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="ablation",
                explainer_used="word_ablation",
                runtime_ms=0.0,
            )

        # Baseline prediction
        base_probas = self.model.predict_proba([text])[0]
        if target_class_idx is None:
            target_class_idx = int(np.argmax(base_probas))
        base_score = float(base_probas[target_class_idx])

        # Single word special handling
        if len(words_info) == 1:
            w_item = words_info[0]
            # When sole word removed, empty string probability is 0.5 (neutral)
            score = float(base_score - 0.5)
            rec = {
                "token": w_item["token"],
                "position": 1,
                "occurrence": 1,
                "attribution": score,
                "char_start": w_item["char_start"],
                "char_end": w_item["char_end"],
            }
            runtime_ms = (time.perf_counter() - t0) * 1000.0
            return ExplanationResult(
                token_weights=TokenAttributionsDict({w_item["token"]: score}, [rec]),
                token_attributions=[rec],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="ablation",
                explainer_used="word_ablation",
                runtime_ms=runtime_ms,
            )

        # Build masked variants for all words
        masked_texts = []
        for w in words_info:
            mw = text[:w["char_start"]] + text[w["char_end"]:]
            clean_mw = " ".join(mw.split())
            masked_texts.append(clean_mw if clean_mw else " ")

        masked_probas = self.model.predict_proba(masked_texts, batch_size=32)

        token_records = []
        weight_map = {}
        for w, pm in zip(words_info, masked_probas):
            score = float(base_score - pm[target_class_idx])
            rec = {
                "token": w["token"],
                "position": w["position"],
                "occurrence": w["occurrence"],
                "attribution": score,
                "char_start": w["char_start"],
                "char_end": w["char_end"],
            }
            token_records.append(rec)
            # Support case-insensitive and case-sensitive lookups in weight_map
            if w["token"] not in weight_map:
                weight_map[w["token"]] = score
            if w["token"].lower() not in weight_map:
                weight_map[w["token"].lower()] = score

        runtime_ms = (time.perf_counter() - t0) * 1000.0
        return ExplanationResult(
            token_weights=TokenAttributionsDict(weight_map, token_records),
            token_attributions=token_records,
            model_id=self.model.model_name,
            text=text,
            explainer_requested="ablation",
            explainer_used="word_ablation",
            runtime_ms=runtime_ms,
        )
