from altair.utils import Optional
import numpy as np
from typing import Dict, List, Any

def compute_jaccard_similarity(exp1: Dict[str, float], exp2: Dict[str, float], top_k: int = 5) -> float:
    """
    Computes Jaccard similarity of top K tokens by absolute attribution score.
    """
    sorted1 = sorted(exp1.items(), key=lambda x: abs(x[1]), reverse=True)[:top_k]
    sorted2 = sorted(exp2.items(), key=lambda x: abs(x[1]), reverse=True)[:top_k]

    set1 = set(k.lower() for k, _ in sorted1)
    set2 = set(k.lower() for k, _ in sorted2)

    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0

    intersection = set1.intersection(set2)
    union = set1.union(set2)

    return float(len(intersection) / len(union))

def compute_attribution_cosine(exp1: Dict[str, float], exp2: Dict[str, float]) -> float:
    """
    Computes Cosine Similarity between attribution vectors across common vocabulary.
    """
    common_words = set(exp1.keys()).union(set(exp2.keys()))
    if not common_words:
        return 1.0

    v1 = np.array([exp1.get(w, 0.0) for w in common_words])
    v2 = np.array([exp2.get(w, 0.0) for w in common_words])

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(np.dot(v1, v2) / (norm1 * norm2))


def compute_explanation_quality(
    lime_exp: Optional[Any],
    shap_exp: Optional[Any],
    aligned_multimodel: Optional[List[Dict[str, Any]]] = None,
) -> Any:
    """
    Computes ExplanationQuality assessing availability, validity, cross-explainer sign agreement,
    and rank correlation across independent LIME and SHAP attributions (Phases 7, 8).
    """
    from blindspot.core.types import ExplanationQuality

    lime_avail = bool(lime_exp and getattr(lime_exp, "status", "") == "AVAILABLE" and getattr(lime_exp, "token_weights", None))
    shap_avail = bool(shap_exp and getattr(shap_exp, "status", "") == "AVAILABLE" and getattr(shap_exp, "token_weights", None))
    lime_valid = lime_avail and (not getattr(lime_exp, "fallback_used", False))
    shap_valid = shap_avail and (not getattr(shap_exp, "fallback_used", False))

    sign_agreement = None
    rank_corr = None

    if aligned_multimodel:
        lime_vals = []
        shap_vals = []
        sign_matches = 0
        total_eval = 0

        for row in aligned_multimodel:
            l_w = row.get("pert_lime") if "pert_lime" in row else row.get("orig_lime")
            s_w = row.get("pert_shap") if "pert_shap" in row else row.get("orig_shap")
            if l_w is not None and s_w is not None and (abs(l_w) > 1e-4 or abs(s_w) > 1e-4):
                total_eval += 1
                if (l_w > 0 and s_w > 0) or (l_w < 0 and s_w < 0) or (abs(l_w) <= 1e-4 and abs(s_w) <= 1e-4):
                    sign_matches += 1
                lime_vals.append(float(l_w))
                shap_vals.append(float(s_w))

        if total_eval > 0:
            sign_agreement = float(sign_matches / total_eval)

        if len(lime_vals) >= 3:
            try:
                from scipy.stats import spearmanr
                corr, _ = spearmanr(lime_vals, shap_vals)
                if not np.isnan(corr):
                    rank_corr = float(corr)
            except Exception:
                pass

    if lime_valid and shap_valid:
        if sign_agreement is not None and sign_agreement < 0.40:
            status = "DISAGREEMENT"
        else:
            status = "VALID"
    elif lime_valid or shap_valid:
        status = "PARTIAL"
    elif (lime_exp and getattr(lime_exp, "status", "") == "FAILED") or (shap_exp and getattr(shap_exp, "status", "") == "FAILED"):
        status = "FAILED"
    else:
        status = "UNAVAILABLE"

    return ExplanationQuality(
        lime_available=lime_avail,
        shap_available=shap_avail,
        lime_valid=lime_valid,
        shap_valid=shap_valid,
        token_alignment_valid=bool(aligned_multimodel),
        target_class_valid=bool(lime_exp and getattr(lime_exp, "target_class_label", None)),
        cross_explainer_sign_agreement=sign_agreement,
        cross_explainer_rank_correlation=rank_corr,
        quality_status=status,
    )

