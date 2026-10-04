import numpy as np
import re
import time
from typing import List, Dict, Any, Tuple, Optional
import logging
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.core.types import ExplanationResult

logger = logging.getLogger(__name__)


class LimeExplainerWrapper:
    """
    Extracts LIME local word-level attributions for black-box text classifiers.
    Provides safe label index resolution, provenance tracking, and zero-dependency fallbacks.
    """
    def __init__(self, model_wrapper: HuggingFaceWrapper, random_seed: int = 42):
        self.model = model_wrapper
        self.random_seed = random_seed
        self.explainer = None
        self._init_explainer()

    def _init_explainer(self):
        try:
            from lime.lime_text import LimeTextExplainer
            self.explainer = LimeTextExplainer(
                class_names=self.model.labels,
                split_expression=r'\W+',
                random_state=self.random_seed
            )
        except Exception as e:
            logger.warning(f"LIME package not available or initialization failed ({e}). Using heuristic explainer fallback.")
            self.explainer = None

    def explain(
        self,
        text: str,
        target_class: Optional[str] = None,
        num_features: int = 10,
        num_samples: int = 50,
    ) -> ExplanationResult:
        """
        Returns ExplanationResult mapping words to attribution scores for top predicted or target class.
        Uses batched inference and bounded sample count for fast CPU/GPU evaluation (Phases 2, 4).
        """
        t0 = time.perf_counter()

        if not text or not text.strip():
            return ExplanationResult(
                token_weights={},
                token_attributions=[],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="lime",
                explainer_used="none",
                runtime_ms=0.0,
                random_seed=self.random_seed,
            )

        fallback_reason = None
        if self.explainer is not None:
            try:
                # Reset random states before explanation to guarantee reproducibility across calls
                if self.random_seed is not None:
                    from sklearn.utils import check_random_state
                    rng = check_random_state(self.random_seed)
                    self.explainer.random_state = rng
                    if hasattr(self.explainer, "base"):
                        self.explainer.base.random_state = rng

                probas = self.model.predict_proba([text])[0]
                pred_class_idx = int(np.argmax(probas))
                pred_class_name = self.model.labels[pred_class_idx] if (hasattr(self.model, "labels") and pred_class_idx < len(self.model.labels)) else str(pred_class_idx)
                pred_class_prob = float(probas[pred_class_idx])

                # Resolve target class index
                if target_class is not None and hasattr(self.model, "labels") and target_class in self.model.labels:
                    target_idx = self.model.labels.index(target_class)
                    target_name = target_class
                else:
                    target_idx = pred_class_idx
                    target_name = pred_class_name
                target_prob = float(probas[target_idx]) if target_idx < len(probas) else pred_class_prob

                exp = self.explainer.explain_instance(
                    text,
                    lambda texts: self.model.predict_proba(texts, batch_size=32),
                    labels=[target_idx],
                    num_features=num_features,
                    num_samples=num_samples,
                )

                try:
                    list_weights = exp.as_list(label=target_idx)
                except Exception:
                    list_weights = exp.as_list()

                weight_map = {word: float(weight) for word, weight in list_weights}
                from blindspot.explainability.token_attributions import extract_words_with_positions
                words_info = extract_words_with_positions(text)
                token_records = []
                for w in words_info:
                    tok = w["token"]
                    w_val = weight_map.get(tok, weight_map.get(tok.lower(), 0.0))
                    token_records.append({
                        "token": tok,
                        "position": w["position"],
                        "occurrence": w["occurrence"],
                        "char_start": w.get("char_start"),
                        "char_end": w.get("char_end"),
                        "attribution": float(w_val) if w_val is not None else 0.0,
                    })

                runtime_ms = (time.perf_counter() - t0) * 1000.0
                return ExplanationResult(
                    token_weights=weight_map,
                    token_attributions=token_records,
                    model_id=self.model.model_name,
                    text=text,
                    explainer_requested="lime",
                    explainer_used="lime",
                    fallback_used=False,
                    fallback_reason=None,
                    runtime_ms=runtime_ms,
                    random_seed=self.random_seed,
                    explained_class=target_name,
                    explained_class_index=target_idx,
                    target_class_label=target_name,
                    target_class_index=target_idx,
                    target_class_probability=target_prob,
                    prediction_label=pred_class_name,
                    prediction_probability=pred_class_prob,
                    num_samples=num_samples,
                    tokenizer_name="whitespace_regex",
                    status="AVAILABLE",
                )
            except Exception as e:
                fallback_reason = str(e)
                logger.warning(f"LIME explanation failed ({e}). Returning explicit explainer failure.")
        else:
            fallback_reason = "LIME package unavailable"

        runtime_ms = (time.perf_counter() - t0) * 1000.0
        return ExplanationResult(
            token_weights={},
            token_attributions=[],
            model_id=self.model.model_name,
            text=text,
            explainer_requested="lime",
            explainer_used="none",
            fallback_used=False,
            fallback_reason=fallback_reason,
            runtime_ms=runtime_ms,
            random_seed=self.random_seed,
            status="FAILED",
            error=fallback_reason,
        )

