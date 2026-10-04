"""
Evidence-Backed 4-Way Failure Taxonomy Classifier for BlindSpot.
Diagnoses model failures into:
1. Blind: The model fails to assign meaningful attribution to the linguistic operator (|w_op| < threshold).
2. Misweighted: The model recognizes the operator, but competing opposing features outweigh it.
3. Spurious: The decision shift is dominated by irrelevant/background lexical features (stop words, punctuation).
4. Undetermined: Insufficient or missing explanation evidence, or ambiguous causality.
"""
from typing import Dict, Any, List, Optional, Tuple, Union
import re
import uuid

from blindspot.core.types import FailureCategory, BehavioralOutcome
from blindspot.core.config import AttributionThresholds
from blindspot.testing.behavioral import classify_behavior


class TaxonomyClassifier:
    """
    Classifies auditing failures into the 4-way traceable taxonomy:
    Blind, Spurious, Misweighted, and Undetermined.
    Backed strictly by independent LIME and SHAP attribution evidence.
    """
    def __init__(self, thresholds: Optional[AttributionThresholds] = None):
        self.thresholds = thresholds or AttributionThresholds()
        self.stop_words = {
            "the", "a", "an", "is", "was", "are", "were", "it", "this", "that",
            "in", "on", "at", "to", "for", "of", "and", "or", "by", "with",
            "as", "be", "so", "than", "then", "there", "i", "you", "he", "she",
            "they", "we", "my", "your", "his", "her", "its", "their", "our",
        }
        self.negation_tokens = {
            "not", "never", "no", "n't", "neither", "nor", "hardly", "barely", "scarcely"
        }
        self.contrast_tokens = {
            "however", "but", "although", "though", "nevertheless", "yet", "nonetheless", "despite"
        }
        self.intensifier_tokens = {
            "very", "extremely", "highly", "completely", "totally", "absolutely", "exceptionally"
        }
        self.downtoner_tokens = {
            "somewhat", "slightly", "barely", "partially", "mildly", "scarcely", "fairly"
        }

    def _is_background_token(self, token: str) -> bool:
        """Determines if a token is a stop word, punctuation, or non-causal background feature."""
        t = str(token).lower().strip()
        if not t:
            return True
        if not any(c.isalnum() for c in t):
            return True
        return t in self.stop_words

    @staticmethod
    def _extract_weights(exp: Any) -> Dict[str, float]:
        """Extracts clean word -> attribution score mapping from any explanation structure."""
        if not exp:
            return {}
        if hasattr(exp, "token_weights") and isinstance(exp.token_weights, dict):
            exp = exp.token_weights
        elif isinstance(exp, dict) and "token_weights" in exp and isinstance(exp["token_weights"], dict):
            exp = exp["token_weights"]
        elif hasattr(exp, "token_attributions") and isinstance(exp.token_attributions, list):
            return {
                str(r.get("token", "")).lower(): float(r.get("attribution", 0.0))
                for r in exp.token_attributions
                if r.get("token")
            }
        elif isinstance(exp, dict) and "token_attributions" in exp and isinstance(exp["token_attributions"], list):
            return {
                str(r.get("token", "")).lower(): float(r.get("attribution", 0.0))
                for r in exp["token_attributions"]
                if r.get("token")
            }
        if isinstance(exp, dict):
            return {
                str(k).lower(): float(v)
                for k, v in exp.items()
                if isinstance(v, (int, float)) and not isinstance(v, bool)
            }
        return {}

    def classify_failure(
        self,
        perturbation_type: str,
        original_sentence: str,
        perturbed_sentence: str,
        original_label: str,
        perturbed_label: str,
        is_flipped: bool,
        expected_flip: bool,
        orig_explanation: Optional[Any] = None,
        pert_explanation: Optional[Any] = None,
        model_id: str = "",
        probe_id: str = "",
        confidence_delta: float = 0.0,
        expected_semantic_effect: str = "",
        semantic_intent: str = "",
        original_confidence: float = 1.0,
        perturbed_confidence: float = 1.0,
        lime_orig: Optional[Any] = None,
        lime_pert: Optional[Any] = None,
        shap_orig: Optional[Any] = None,
        shap_pert: Optional[Any] = None,
        operator_tokens: Optional[List[str]] = None,
        operator_type: Optional[str] = None,
        thresholds: Optional[AttributionThresholds] = None,
        counterfactual_evidence: Optional[Dict[str, Any]] = None,
        explanation_quality: Optional[Any] = None,
        behavioral_outcome: Optional[Union[BehavioralOutcome, str]] = None,
        target_polarity: Optional[Any] = None,
        behavioral_evidence: Optional[Dict[str, Any]] = None,
        behavioral_rationale: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluates a single original-perturbed pair and returns traceable failure diagnosis if a failure occurs.
        Returns None if model behaved correctly and explanation is sound.
        Strictly analyzes independent LIME and SHAP evidence without arithmetic fusion.
        """
        thresh = thresholds or self.thresholds

        # 1. Resolve LIME and SHAP independent weight maps
        l_pert = self._extract_weights(lime_pert or pert_explanation)
        s_pert = self._extract_weights(shap_pert)
        l_orig = self._extract_weights(lime_orig or orig_explanation)
        s_orig = self._extract_weights(shap_orig)

        # 2. Resolve Operator Tokens and Operator Type
        op_tokens = [str(t).lower().strip() for t in (operator_tokens or []) if str(t).strip()]
        if not op_tokens:
            ptype_lower = perturbation_type.lower()
            if "negation" in ptype_lower and "double" not in ptype_lower:
                op_tokens = [w for w in re.findall(r"\b\w+\b", perturbed_sentence.lower()) if w in self.negation_tokens] or ["not"]
                operator_type = operator_type or "negation"
            elif "contrast" in ptype_lower or "connective" in ptype_lower or "concession" in ptype_lower:
                op_tokens = [w for w in re.findall(r"\b\w+\b", perturbed_sentence.lower()) if w in self.contrast_tokens] or ["however"]
                operator_type = operator_type or "contrast"
            elif "intensity" in ptype_lower:
                op_tokens = [w for w in re.findall(r"\b\w+\b", perturbed_sentence.lower()) if w in self.intensifier_tokens or w in self.downtoner_tokens] or ["extremely"]
                operator_type = operator_type or "intensity"
            else:
                # Diff between original and perturbed words
                orig_words = set(re.findall(r"\b\w+\b", original_sentence.lower()))
                pert_words = re.findall(r"\b\w+\b", perturbed_sentence.lower())
                inserted = [w for w in pert_words if w not in orig_words and w not in self.stop_words]
                op_tokens = inserted[:2] if inserted else []
                operator_type = operator_type or (ptype_lower if ptype_lower else "perturbation")

        eff = expected_semantic_effect or ("invert" if expected_flip else "preserve")

        # 3. Behavioral Evaluation
        if behavioral_outcome is not None:
            if isinstance(behavioral_outcome, str):
                try:
                    outcome = BehavioralOutcome(behavioral_outcome)
                except ValueError:
                    outcome = BehavioralOutcome.UNDETERMINED
            else:
                outcome = behavioral_outcome
            base_evidence = dict(behavioral_evidence or {})
            beh_rationale = behavioral_rationale or ""
            if "expectation_match" not in base_evidence:
                base_evidence["expectation_match"] = (outcome in (BehavioralOutcome.EXPECTED_FLIP, BehavioralOutcome.EXPECTED_PRESERVE))
        else:
            outcome, beh_cat, base_evidence, beh_rationale = classify_behavior(
                original_label=original_label,
                probe_label=perturbed_label,
                original_confidence=original_confidence,
                probe_confidence=perturbed_confidence,
                expected_effect=eff,
                semantic_intent=semantic_intent or ("REVERSE_POLARITY" if expected_flip else "PRESERVE_MEANING"),
                expected_label_relation="DIFFERENT_LABEL" if expected_flip else "SAME_LABEL",
                target_polarity=target_polarity,
            )

        # If model met behavioral expectations and no attribution check requested
        if outcome in (BehavioralOutcome.EXPECTED_FLIP, BehavioralOutcome.EXPECTED_PRESERVE) and base_evidence.get("expectation_match", False):
            # Check for rare synonym attribution flip anomaly if requested
            if "substitution" in perturbation_type.lower() and not is_flipped and l_pert and l_orig:
                syn_keys = set(l_orig.keys()).intersection(set(l_pert.keys()))
                if syn_keys:
                    orig_pos = sum(1 for k in syn_keys if l_orig[k] > 0)
                    pert_pos = sum(1 for k in syn_keys if l_pert[k] > 0)
                    if (orig_pos > 0 and pert_pos == 0) or (orig_pos == 0 and pert_pos > 0):
                        return {
                            "category": FailureCategory.MISWEIGHTED.value,
                            "reason": "Synonym substitution caused unstable attribution polarity shift.",
                            "details": "Substituting a word with its synonym inverted attribution weights without label flip.",
                            "recommendation": "Incorporate embedding regularization to align representation spaces of close synonyms.",
                            "severity": "medium",
                            "evidence": {
                                "common_tokens": list(syn_keys),
                                "orig_positive_count": orig_pos,
                                "pert_positive_count": pert_pos,
                            },
                        }
            return None

        # 4. Behavioral Failure Detected — Diagnose Causality from Explainers
        evidence = dict(base_evidence)
        evidence.update({
            "probe_type": perturbation_type,
            "model_id": model_id,
            "probe_id": probe_id,
            "confidence_delta": confidence_delta,
            "behavioral_outcome": outcome.value,
        })

        # Calculate metrics for LIME
        l_total = sum(abs(v) for v in l_pert.values())
        l_op_vals = [l_pert[t] for t in op_tokens if t in l_pert]
        l_op_weight = max(l_op_vals, key=abs) if l_op_vals else 0.0
        l_op_abs = abs(l_op_weight)

        # Non-operator competing tokens
        l_competing = {k: v for k, v in l_pert.items() if k not in op_tokens and not self._is_background_token(k)}
        l_comp_sorted = sorted(l_competing.items(), key=lambda x: abs(x[1]), reverse=True)
        l_dom_comp, l_dom_weight = l_comp_sorted[0] if l_comp_sorted else ("none", 0.0)

        # Stopword / background / punctuation tokens
        l_stopwords = {k: v for k, v in l_pert.items() if self._is_background_token(k)}
        l_stop_sum = sum(abs(v) for v in l_stopwords.values())
        l_stop_ratio = (l_stop_sum / l_total) if l_total > 0 else 0.0

        # Calculate metrics for SHAP
        s_total = sum(abs(v) for v in s_pert.values())
        s_op_vals = [s_pert[t] for t in op_tokens if t in s_pert]
        s_op_weight = max(s_op_vals, key=abs) if s_op_vals else 0.0
        s_op_abs = abs(s_op_weight)

        s_competing = {k: v for k, v in s_pert.items() if k not in op_tokens and not self._is_background_token(k)}
        s_comp_sorted = sorted(s_competing.items(), key=lambda x: abs(x[1]), reverse=True)
        s_dom_comp, s_dom_weight = s_comp_sorted[0] if s_comp_sorted else ("none", 0.0)

        s_stopwords = {k: v for k, v in s_pert.items() if self._is_background_token(k)}
        s_stop_sum = sum(abs(v) for v in s_stopwords.values())
        s_stop_ratio = (s_stop_sum / s_total) if s_total > 0 else 0.0

        # Store independent taxonomy evidence
        evidence["taxonomy_evidence"] = {
            "operator_tokens": op_tokens,
            "operator_type": operator_type,
            "thresholds": thresh.to_dict(),
            "counterfactual_analysis": counterfactual_evidence or {},
            "explanation_quality": explanation_quality.to_dict() if hasattr(explanation_quality, "to_dict") else (explanation_quality or {}),
            "lime": {
                "status": "AVAILABLE" if l_pert else "UNAVAILABLE",
                "operator_weight": round(float(l_op_weight), 4),
                "operator_abs_weight": round(float(l_op_abs), 4),
                "dominant_competitor": l_dom_comp,
                "dominant_competitor_weight": round(float(l_dom_weight), 4),
                "total_attribution": round(float(l_total), 4),
                "stopword_ratio": round(float(l_stop_ratio), 4),
            },
            "shap": {
                "status": "AVAILABLE" if s_pert else "UNAVAILABLE",
                "operator_weight": round(float(s_op_weight), 4),
                "operator_abs_weight": round(float(s_op_abs), 4),
                "dominant_competitor": s_dom_comp,
                "dominant_competitor_weight": round(float(s_dom_weight), 4),
                "total_attribution": round(float(s_total), 4),
                "stopword_ratio": round(float(s_stop_ratio), 4),
            },
        }

        # -------------------------------------------------------------
        # SCIENTIFIC TAXONOMY DECISION TREE (Sections 11, 15, 16, 17, 36)
        # -------------------------------------------------------------

        # Case 0: Insufficient / Failed Explanations -> UNDETERMINED
        if (l_total < thresh.indeterminate_total_abs and s_total < thresh.indeterminate_total_abs):
            failure_cat = FailureCategory.UNDETERMINED
            rationale = "Attribution evidence is unavailable or near zero across explainers; cannot isolate failure causality."

        # Case 1: Missing Polarity Reversal / Failed Flip (MISSING_FLIP)
        elif outcome == BehavioralOutcome.MISSING_FLIP or expected_flip:
            has_lime = bool(l_pert)
            has_shap = bool(s_pert)

            # Subcase 1A: Strong explainer disagreement on operator token direction (Phase 8, 26 Test 4)
            if (
                has_lime
                and has_shap
                and l_op_abs >= thresh.operator_min_abs
                and s_op_abs >= thresh.operator_min_abs
                and (l_op_weight * s_op_weight < 0)
            ):
                failure_cat = FailureCategory.UNDETERMINED
                op_str = ", ".join(op_tokens) if op_tokens else "operator"
                rationale = (
                    f"Explainers strongly disagree on attribution direction for operator '{op_str}' "
                    f"(LIME: {l_op_weight:+.4f}, SHAP: {s_op_weight:+.4f}). Evidence is contradictory; taxonomy remains undetermined."
                )

            # Subcase 1B: Both explainers show negligible operator attribution -> BLIND
            elif (l_op_abs < thresh.operator_min_abs if has_lime else True) and (s_op_abs < thresh.operator_min_abs if has_shap else True):
                failure_cat = FailureCategory.BLIND
                op_str = ", ".join(op_tokens) if op_tokens else "operator"
                rationale = (
                    f"Model failed to produce expected polarity reversal and showed negligible attribution to "
                    f"linguistic operator '{op_str}' (LIME: {l_op_weight:+.4f}, SHAP: {s_op_weight:+.4f} < {thresh.operator_min_abs})."
                )

            # Subcase 1C: Operator registered, but competing features outweighed it -> MISWEIGHTED
            else:
                failure_cat = FailureCategory.MISWEIGHTED
                op_str = ", ".join(op_tokens) if op_tokens else "operator"
                comp_summary = f"'{l_dom_comp}' ({l_dom_weight:+.4f})" if l_dom_comp != "none" else f"'{s_dom_comp}' ({s_dom_weight:+.4f})"
                cf_note = ""
                if counterfactual_evidence and counterfactual_evidence.get("counterfactual_support"):
                    cf_note = " Counterfactual operator ablation restored the baseline target probability direction, supporting operator sensitivity."
                rationale = (
                    f"Model recognized linguistic operator '{op_str}' (LIME: {l_op_weight:+.4f}, SHAP: {s_op_weight:+.4f}), "
                    f"but opposing sentiment features ({comp_summary}) outweighed the operator, preventing expected polarity reversal.{cf_note}"
                )

        # Case 2: Meaning-Preserving Perturbation Unexpectedly Flipped (UNEXPECTED_FLIP)
        elif outcome in (BehavioralOutcome.UNEXPECTED_FLIP, BehavioralOutcome.UNEXPECTED_CHANGE):
            # Check if decision is dominated by irrelevant / stop / punctuation words -> SPURIOUS
            max_stop_ratio = max(l_stop_ratio, s_stop_ratio)
            l_all_sorted = sorted(l_pert.items(), key=lambda x: abs(x[1]), reverse=True)
            top_tok = l_all_sorted[0][0] if l_all_sorted else ""
            top_is_bg = self._is_background_token(top_tok)

            if max_stop_ratio >= thresh.spurious_stopword_ratio or top_is_bg:
                failure_cat = FailureCategory.SPURIOUS
                rationale = (
                    f"Model unexpectedly flipped prediction under meaning-preserving perturbation, "
                    f"driven primarily by irrelevant/background features (background attribution ratio: {max_stop_ratio:.1%}, top token: '{top_tok}') "
                    f"rather than semantic content."
                )
            else:
                failure_cat = FailureCategory.MISWEIGHTED
                rationale = (
                    f"Model unexpectedly flipped prediction under meaning-preserving perturbation "
                    f"due to disproportionate feature weight shift on semantic tokens."
                )

        # Case 3: Other Behavioral Inconsistencies / Degree Failures
        elif outcome == BehavioralOutcome.EXPECTED_PRESERVE and not base_evidence.get("expectation_match", True):
            failure_cat = FailureCategory.MISWEIGHTED
            rationale = beh_rationale or "Disproportionate confidence shift under degree modifier."

        else:
            failure_cat = FailureCategory.UNDETERMINED
            rationale = beh_rationale or "Behavioral deviation occurred without decisive attribution causality."

        severity = "high" if failure_cat in (FailureCategory.BLIND, FailureCategory.SPURIOUS) else "medium"

        # Actionable recommendations
        pert_lower = perturbation_type.lower()
        if failure_cat == FailureCategory.BLIND:
            if "negation" in pert_lower:
                rec = "Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures."
            elif "contrast" in pert_lower or "connective" in pert_lower:
                rec = "Augment training data with contrastive/adversative clause constructions and regularize cross-clause attention to fix Blind failures."
            else:
                rec = f"Augment training data and regularize behavior against {perturbation_type} perturbations to fix Blind failures."
        elif failure_cat == FailureCategory.MISWEIGHTED:
            rec = "Incorporate contrastive loss and clause-level balancing to prevent dominant clauses from overpowering linguistic operators."
        elif failure_cat == FailureCategory.SPURIOUS:
            rec = "Apply adversarial synonym swaps and invariant regularization to suppress spurious background sensitivity."
        else:
            rec = "Review counterfactual variations and inspect full probability distribution shifts."

        return {
            "category": failure_cat.value,
            "reason": rationale,
            "details": f"Under {perturbation_type}, model transition '{original_label} -> {perturbed_label}' was diagnosed as {failure_cat.value}. {rationale}",
            "recommendation": rec,
            "severity": severity,
            "evidence": evidence,
        }
