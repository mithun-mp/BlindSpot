import numpy as np
import time
from typing import List, Dict, Any, Union, Optional
import logging
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.core.types import ExplanationResult

logger = logging.getLogger(__name__)


class ShapExplainerWrapper:
    """
    Extracts SHAP (Shapley Additive exPlanations) token-level attributions.
    Provides robust multi-dimensional array handling, provenance tracking, and zero-dependency fallbacks.
    """
    def __init__(self, model_wrapper: HuggingFaceWrapper):
        self.model = model_wrapper
        self.explainer = None
        self.shap_version = None
        self.masker_type = None
        self._init_explainer()

    def _predict_fn(self, texts: Union[np.ndarray, List[str], str]) -> np.ndarray:
        """
        Adapter function ensuring text inputs are passed as List[str] to model wrapper.
        Uses batched pipeline prediction.
        """
        if isinstance(texts, np.ndarray):
            texts = texts.tolist()
        elif isinstance(texts, str):
            texts = [texts]

        clean_texts = [str(t) for t in texts]
        return self.model.predict_proba(clean_texts, batch_size=32)

    def _init_explainer(self):
        try:
            import shap
            self.shap_version = getattr(shap, "__version__", "unknown")
            masker = shap.maskers.Text()
            self.masker_type = "shap.maskers.Text"
            self.explainer = shap.Explainer(self._predict_fn, masker=masker)
        except Exception as e:
            logger.warning(f"SHAP package not available or initialization failed ({e}). Explanations will return explicit failure.")
            self.explainer = None

    def explain(
        self,
        text: str,
        target_class: Optional[str] = None,
        max_evals: int = 50,
    ) -> ExplanationResult:
        """
        Returns ExplanationResult with token SHAP value attributions for the target or top predicted class.
        Uses bounded max_evals and batched inference for speed (Phases 3, 4).
        """
        t0 = time.perf_counter()

        if not text or not text.strip():
            return ExplanationResult(
                token_weights={},
                token_attributions=[],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="shap",
                explainer_used="none",
                runtime_ms=0.0,
                tokenizer_name=self.masker_type or "shap.maskers.Text",
                status="AVAILABLE",
            )

        fallback_reason = None
        if self.explainer is not None:
            try:
                probas = self._predict_fn([text])[0]
                pred_class_idx = int(np.argmax(probas))
                pred_class_name = self.model.labels[pred_class_idx] if (hasattr(self.model, "labels") and pred_class_idx < len(self.model.labels)) else str(pred_class_idx)
                pred_class_prob = float(probas[pred_class_idx])

                # Resolve target class index explicitly (Phase 4)
                if target_class is not None and hasattr(self.model, "labels") and target_class in self.model.labels:
                    target_idx = self.model.labels.index(target_class)
                    target_name = target_class
                else:
                    target_idx = pred_class_idx
                    target_name = pred_class_name
                target_prob = float(probas[target_idx]) if target_idx < len(probas) else pred_class_prob

                try:
                    shap_values = self.explainer([text], max_evals=max_evals)
                except TypeError:
                    shap_values = self.explainer([text])

                tokens = shap_values.data[0]
                vals = shap_values.values

                if vals.ndim == 3:
                    vals_sample = vals[0]
                elif vals.ndim == 2:
                    vals_sample = vals
                else:
                    vals_sample = np.atleast_2d(vals)

                if vals_sample.ndim == 2:
                    if target_idx < vals_sample.shape[1]:
                        token_weights = vals_sample[:, target_idx]
                    else:
                        token_weights = vals_sample[:, 0]
                else:
                    token_weights = np.ravel(vals_sample)

                # Store raw shap data for provenance (Phase 3)
                raw_shap_data = {
                    "raw_tokens": [str(t) for t in tokens],
                    "raw_values": [float(v) for v in token_weights],
                    "shap_version": self.shap_version,
                    "masker": self.masker_type,
                    "max_evals": max_evals,
                }

                # Extract raw SHAP token map with occurrences (Phase 6)
                from blindspot.explainability.token_attributions import extract_words_with_positions
                words_info = extract_words_with_positions(text)

                raw_shap_map = {}
                shap_occ = {}
                for tok, val in zip(tokens, token_weights):
                    tok_clean = str(tok).strip()
                    if tok_clean:
                        tok_lower = tok_clean.lower()
                        shap_occ[tok_lower] = shap_occ.get(tok_lower, 0) + 1
                        raw_shap_map[(tok_lower, shap_occ[tok_lower])] = float(val)
                        if tok_lower not in raw_shap_map:
                            raw_shap_map[tok_lower] = float(val)

                token_records = []
                result = {}
                for w in words_info:
                    tok = w["token"]
                    tok_l = tok.lower()
                    occ = w["occurrence"]
                    score = raw_shap_map.get((tok_l, occ), raw_shap_map.get(tok_l, 0.0))
                    token_records.append({
                        "token": tok,
                        "position": w["position"],
                        "occurrence": occ,
                        "char_start": w.get("char_start"),
                        "char_end": w.get("char_end"),
                        "attribution": float(score),
                    })
                    if tok not in result:
                        result[tok] = float(score)

                runtime_ms = (time.perf_counter() - t0) * 1000.0
                return ExplanationResult(
                    token_weights=result,
                    token_attributions=token_records,
                    model_id=self.model.model_name,
                    text=text,
                    explainer_requested="shap",
                    explainer_used="shap",
                    fallback_used=False,
                    fallback_reason=None,
                    runtime_ms=runtime_ms,
                    explained_class=target_name,
                    explained_class_index=target_idx,
                    target_class_label=target_name,
                    target_class_index=target_idx,
                    target_class_probability=target_prob,
                    prediction_label=pred_class_name,
                    prediction_probability=pred_class_prob,
                    num_samples=max_evals,
                    tokenizer_name=self.masker_type or "shap_text_masker",
                    raw_explanations=raw_shap_data,
                    status="AVAILABLE",
                )
            except Exception as e:
                fallback_reason = str(e)
                logger.warning(f"SHAP explanation computation encountered ({e}). Returning explicit explainer failure.")
        else:
            fallback_reason = "SHAP explainer initialization failed or unavailable"

        runtime_ms = (time.perf_counter() - t0) * 1000.0
        return ExplanationResult(
            token_weights={},
            token_attributions=[],
            model_id=self.model.model_name,
            text=text,
            explainer_requested="shap",
            explainer_used="none",
            fallback_used=False,
            fallback_reason=fallback_reason,
            runtime_ms=runtime_ms,
            target_class_label=target_class or "",
            status="FAILED",
            error=fallback_reason,
        )

