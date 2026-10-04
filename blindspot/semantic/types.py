"""
Canonical Semantic Reference Label Space and Contracts (BlindSpot).
Provides strictly POSITIVE, NEGATIVE, and NEUTRAL semantic references,
human overrides, semantic relation contracts, and provenance tracking.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Union
import time
import json


class SemanticReferenceLabel(str, Enum):
    """
    Canonical Semantic Reference Polarity Label Space.
    STRICTLY POSITIVE, NEGATIVE, NEUTRAL.
    No other sentiment categories are permitted.
    """
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"

    @classmethod
    def validate_label(cls, val: Any) -> "SemanticReferenceLabel":
        """
        Validates and returns the strict SemanticReferenceLabel.
        Raises ValueError if val is not strictly POSITIVE, NEGATIVE, or NEUTRAL.
        """
        if isinstance(val, SemanticReferenceLabel):
            return val
        s = str(val or "").strip().upper()
        if s in ("POSITIVE", "POS"):
            return cls.POSITIVE
        elif s in ("NEGATIVE", "NEG"):
            return cls.NEGATIVE
        elif s in ("NEUTRAL", "NEU"):
            return cls.NEUTRAL
        else:
            raise ValueError(
                f"Invalid semantic polarity label: '{val}'. "
                f"Allowed semantic labels are strictly {cls.allowed_labels()}."
            )

    @classmethod
    def is_valid(cls, val: Any) -> bool:
        try:
            cls.validate_label(val)
            return True
        except ValueError:
            return False

    @classmethod
    def allowed_labels(cls) -> List[str]:
        return [cls.POSITIVE.value, cls.NEGATIVE.value, cls.NEUTRAL.value]


class SemanticRelation(str, Enum):
    """
    Canonical semantic relationship between baseline and probe sentence.
    Explicitly separated from semantic polarity.
    """
    PRESERVE_POLARITY = "PRESERVE_POLARITY"
    REVERSE_POLARITY = "REVERSE_POLARITY"
    SHIFT_TO_NEUTRAL = "SHIFT_TO_NEUTRAL"
    SHIFT_FROM_NEUTRAL = "SHIFT_FROM_NEUTRAL"
    CONTRAST_SHIFT = "CONTRAST_SHIFT"
    MEANING_CHANGED = "MEANING_CHANGED"
    UNCERTAIN = "UNCERTAIN"

    # Compatibility aliases
    PRESERVE = "PRESERVE_POLARITY"
    REVERSE = "REVERSE_POLARITY"
    OTHER = "UNCERTAIN"

    @classmethod
    def from_str(cls, val: Any) -> "SemanticRelation":
        if isinstance(val, SemanticRelation):
            return val
        s = str(val or "").strip().upper()
        # Direct matching
        for member in cls:
            if member.value == s or member.name == s:
                return member
        # Alias matching
        if s in ("PRESERVE", "PRESERVE_MEANING", "PRESERVE_POLARITY", "SAME_POLARITY", "SAME_LABEL"):
            return cls.PRESERVE_POLARITY
        elif s in ("REVERSE", "REVERSE_POLARITY", "INVERT", "DIFFERENT_LABEL", "FLIP"):
            return cls.REVERSE_POLARITY
        elif s == "SHIFT_TO_NEUTRAL":
            return cls.SHIFT_TO_NEUTRAL
        elif s == "SHIFT_FROM_NEUTRAL":
            return cls.SHIFT_FROM_NEUTRAL
        elif s in ("CONTRAST_SHIFT", "CONTRAST", "SHIFT_CONTRAST"):
            return cls.CONTRAST_SHIFT
        elif s in ("MEANING_CHANGED", "CHANGED"):
            return cls.MEANING_CHANGED
        elif s in ("UNCERTAIN", "OTHER", "UNKNOWN"):
            return cls.UNCERTAIN
        return cls.UNCERTAIN

    @classmethod
    def from_polarities(
        cls,
        baseline_polarity: Any,
        probe_polarity: Any,
    ) -> "SemanticRelation":
        """
        Authoritatively determines semantic relation from verified polarities.
        Distinguishes preservation, reversal, neutral transitions, or uncertain.
        """
        if baseline_polarity is None or probe_polarity is None:
            return cls.UNCERTAIN
        try:
            b = SemanticReferenceLabel.validate_label(baseline_polarity)
            p = SemanticReferenceLabel.validate_label(probe_polarity)
        except Exception:
            return cls.UNCERTAIN

        if b == p:
            return cls.PRESERVE_POLARITY
        elif (b == SemanticReferenceLabel.POSITIVE and p == SemanticReferenceLabel.NEGATIVE) or \
             (b == SemanticReferenceLabel.NEGATIVE and p == SemanticReferenceLabel.POSITIVE):
            return cls.REVERSE_POLARITY
        elif b != SemanticReferenceLabel.NEUTRAL and p == SemanticReferenceLabel.NEUTRAL:
            return cls.SHIFT_TO_NEUTRAL
        elif b == SemanticReferenceLabel.NEUTRAL and p != SemanticReferenceLabel.NEUTRAL:
            return cls.SHIFT_FROM_NEUTRAL
        else:
            return cls.UNCERTAIN


class VerificationStatus(str, Enum):
    """Human and AI verification status for semantic reference annotations."""
    UNVERIFIED = "UNVERIFIED"
    AUTOMATED_REFERENCE = "AUTOMATED_REFERENCE"
    HUMAN_VERIFIED = "HUMAN_VERIFIED"
    HUMAN_OVERRIDDEN = "HUMAN_OVERRIDDEN"
    UNAVAILABLE = "UNAVAILABLE"

    # Compatibility aliases
    GEMINI_ACCEPTED = "AUTOMATED_REFERENCE"
    GEMINI_VERIFIED = "HUMAN_VERIFIED"
    HUMAN_OVERRIDE = "HUMAN_OVERRIDDEN"
    MANUAL = "UNVERIFIED"


class ReferenceProvider(str, Enum):
    """Source provider for semantic reference."""
    GEMINI = "GEMINI"
    MANUAL = "MANUAL"
    LOCAL_HEURISTIC = "LOCAL_HEURISTIC"
    BENCHMARK = "BENCHMARK"
    NONE = "NONE"


def project_three_class_to_binary(
    negative_probability: Optional[float],
    neutral_probability: Optional[float],
    positive_probability: Optional[float],
    epsilon: float = 1e-4,
) -> Dict[str, Any]:
    """
    Deterministically projects 3-class semantic probabilities to 2-class (binary) polarity.

    Invariants:
    1. Preserves original 3-class probabilities.
    2. Excludes neutral_probability when determining binary polarity.
    3. If positive_probability > negative_probability: POSITIVE.
    4. If negative_probability > positive_probability: NEGATIVE.
    5. Else (including positive_probability == negative_probability): POSITIVE (deterministic tie-break).
    6. Never returns AMBIGUOUS for available semantic distributions.
    """
    neg_p = float(negative_probability if negative_probability is not None else 0.0)
    neu_p = float(neutral_probability if neutral_probability is not None else 0.0)
    pos_p = float(positive_probability if positive_probability is not None else 0.0)

    if pos_p > neg_p:
        label = "POSITIVE"
        status = "DERIVED_FROM_POLARITY_PROBABILITIES"
    elif neg_p > pos_p:
        label = "NEGATIVE"
        status = "DERIVED_FROM_POLARITY_PROBABILITIES"
    else:
        label = "POSITIVE"
        status = "DERIVED_FROM_POLARITY_PROBABILITIES"

    return {
        "label": label,
        "negative_probability": round(neg_p, 4),
        "positive_probability": round(pos_p, 4),
        "neutral_probability_excluded": round(neu_p, 4),
        "reference_class_count": 2,
        "status": status,
    }


@dataclass
class SemanticAnnotation:
    """
    Structured semantic reference annotation for a single sentence.
    Preserves full provenance, separation of polarity from relation,
    and authoritative 3-class and 2-class contracts.
    """
    sentence_id: str
    sentence_text: str
    semantic_polarity: Optional[SemanticReferenceLabel] = None
    confidence: Optional[float] = None  # None when uncalibrated or not returned by model
    reason: str = ""
    ambiguity: str = "LOW"  # LOW | MEDIUM | HIGH
    semantic_relation_to_baseline: Optional[SemanticRelation] = None
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    provider: str = ReferenceProvider.NONE.value
    gemini_polarity: Optional[SemanticReferenceLabel] = None
    gemini_confidence: Optional[float] = None
    human_verified_polarity: Optional[SemanticReferenceLabel] = None
    final_semantic_polarity: Optional[SemanticReferenceLabel] = None
    verification_source: str = "UNVERIFIED"
    model_used: Optional[str] = None
    schema_version: str = "v2.0"
    annotation_version: str = "v2.0"
    timestamp: float = field(default_factory=time.time)
    prompt_version: str = "v2.0"

    # Contract A & B fields (Phase 16 Repair)
    negative_probability: Optional[float] = None
    neutral_probability: Optional[float] = None
    positive_probability: Optional[float] = None
    reference_class_count: int = 3
    reference_label: Optional[str] = None
    three_class: Dict[str, Any] = field(default_factory=dict)
    two_class: Dict[str, Any] = field(default_factory=dict)
    binary_projection_label: Optional[str] = None
    binary_projection_status: Optional[str] = None
    status: str = "AVAILABLE"  # AVAILABLE | UNAVAILABLE
    failure_reason: Optional[str] = None
    credential_alias: Optional[str] = None
    request_id: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        # 1. Validate semantic_polarity if status is AVAILABLE
        if self.status == "UNAVAILABLE":
            self.verification_status = VerificationStatus.UNAVAILABLE
            self.semantic_polarity = None
            self.final_semantic_polarity = None
            self.semantic_relation_to_baseline = None
            self.three_class = {
                "label": "UNAVAILABLE",
                "status": "UNAVAILABLE",
                "failure_reason": self.failure_reason,
                "reference_class_count": 3,
            }
            self.two_class = {
                "label": "UNAVAILABLE",
                "status": "UNAVAILABLE",
                "failure_reason": self.failure_reason,
                "reference_class_count": 2,
            }
            self.binary_projection_label = "UNAVAILABLE"
            self.binary_projection_status = "UNAVAILABLE"
            self.reference_label = "UNAVAILABLE"
            return

        if self.semantic_polarity is not None and not isinstance(self.semantic_polarity, SemanticReferenceLabel):
            self.semantic_polarity = SemanticReferenceLabel.validate_label(self.semantic_polarity)

        # 2. Authoritative Probability Resolution
        if (
            self.negative_probability is not None
            and self.neutral_probability is not None
            and self.positive_probability is not None
        ):
            neg = float(self.negative_probability)
            neu = float(self.neutral_probability)
            pos = float(self.positive_probability)

            # Determine 3-class label strictly from probabilities (argmax)
            if neu >= neg and neu >= pos:
                computed_pol = SemanticReferenceLabel.NEUTRAL
            elif pos > neg:
                computed_pol = SemanticReferenceLabel.POSITIVE
            else:
                computed_pol = SemanticReferenceLabel.NEGATIVE

            self.semantic_polarity = computed_pol
            self.reference_label = computed_pol.value
            self.reference_class_count = 3
            if self.confidence is None:
                self.confidence = max(neg, neu, pos)

            self.three_class = {
                "label": computed_pol.value,
                "negative_probability": round(neg, 4),
                "neutral_probability": round(neu, 4),
                "positive_probability": round(pos, 4),
                "reference_class_count": 3,
                "status": "AVAILABLE",
            }

            proj = project_three_class_to_binary(neg, neu, pos)
            self.two_class = proj
            self.binary_projection_label = proj["label"]
            self.binary_projection_status = proj["status"]
        else:
            # Synthetic distribution from discrete label for backward-compat
            c = float(self.confidence) if self.confidence is not None else 1.0
            rem = max(0.0, (1.0 - c) / 2.0)
            if self.semantic_polarity == SemanticReferenceLabel.POSITIVE:
                self.positive_probability = c
                self.negative_probability = rem
                self.neutral_probability = rem
            elif self.semantic_polarity == SemanticReferenceLabel.NEGATIVE:
                self.negative_probability = c
                self.positive_probability = rem
                self.neutral_probability = rem
            else:
                self.neutral_probability = c
                self.positive_probability = rem
                self.negative_probability = rem

            self.reference_label = self.semantic_polarity.value
            self.reference_class_count = 3
            self.three_class = {
                "label": self.semantic_polarity.value,
                "negative_probability": round(self.negative_probability, 4),
                "neutral_probability": round(self.neutral_probability, 4),
                "positive_probability": round(self.positive_probability, 4),
                "reference_class_count": 3,
                "status": "AVAILABLE",
            }
            proj = project_three_class_to_binary(
                self.negative_probability, self.neutral_probability, self.positive_probability
            )
            self.two_class = proj
            self.binary_projection_label = proj["label"]
            self.binary_projection_status = proj["status"]

        if (self.provider == ReferenceProvider.NONE.value or not self.provider) and self.model_used and "gemini" in str(self.model_used).lower():
            self.provider = ReferenceProvider.GEMINI.value

        if self.human_verified_polarity is not None:
            if not isinstance(self.human_verified_polarity, SemanticReferenceLabel):
                self.human_verified_polarity = SemanticReferenceLabel.validate_label(self.human_verified_polarity)
            self.final_semantic_polarity = self.human_verified_polarity
            self.verification_source = "HUMAN_OVERRIDE"
            self.verification_status = VerificationStatus.HUMAN_OVERRIDDEN
        else:
            self.final_semantic_polarity = self.semantic_polarity
            if not self.verification_source or self.verification_source == "GEMINI_ACCEPTED":
                self.verification_source = self.verification_status.value

    def override_polarity(self, new_polarity: Union[str, SemanticReferenceLabel], reason: str = ""):
        """Applies a researcher override to this annotation."""
        validated = SemanticReferenceLabel.validate_label(new_polarity)
        self.human_verified_polarity = validated
        self.final_semantic_polarity = validated
        self.verification_source = "HUMAN_OVERRIDE"
        self.verification_status = VerificationStatus.HUMAN_OVERRIDDEN
        self.provider = ReferenceProvider.MANUAL.value
        if reason:
            orig = self.reason or ""
            self.reason = f"[HUMAN OVERRIDE] {reason} (Prior reason: {orig})".strip()

    def override_human(self, new_polarity: Union[str, SemanticReferenceLabel], reason: str = ""):
        """Alias for override_polarity."""
        self.override_polarity(new_polarity, reason)

    def accept_gemini(self):
        """Explicitly accepts automated/Gemini reference with human verification, preserving human polarity overrides if set."""
        if self.human_verified_polarity is not None:
            self.final_semantic_polarity = self.human_verified_polarity
            self.verification_source = "HUMAN_OVERRIDE"
            self.verification_status = VerificationStatus.HUMAN_OVERRIDDEN
        else:
            self.final_semantic_polarity = self.gemini_polarity or self.semantic_polarity
            self.verification_source = "HUMAN_VERIFIED"
            self.verification_status = VerificationStatus.HUMAN_VERIFIED

    def mark_uncertain(self, reason: str = ""):
        """Explicitly marks semantic reference/relation as UNCERTAIN."""
        self.semantic_relation_to_baseline = SemanticRelation.UNCERTAIN
        self.ambiguity = "HIGH"
        if reason:
            self.reason = f"[UNCERTAIN] {reason}".strip()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sentence_id": self.sentence_id,
            "sentence_text": self.sentence_text,
            "semantic_polarity": self.semantic_polarity.value if self.semantic_polarity else None,
            "confidence": round(self.confidence, 4) if self.confidence is not None else None,
            "reason": self.reason,
            "ambiguity": self.ambiguity,
            "semantic_relation_to_baseline": (
                self.semantic_relation_to_baseline.value
                if self.semantic_relation_to_baseline
                else None
            ),
            "verification_status": (
                self.verification_status.value
                if hasattr(self.verification_status, "value")
                else str(self.verification_status)
            ),
            "provider": self.provider,
            "gemini_polarity": self.gemini_polarity.value if self.gemini_polarity else None,
            "gemini_confidence": (
                round(self.gemini_confidence, 4) if self.gemini_confidence is not None else None
            ),
            "human_verified_polarity": (
                self.human_verified_polarity.value
                if self.human_verified_polarity
                else None
            ),
            "final_semantic_polarity": (
                self.final_semantic_polarity.value
                if self.final_semantic_polarity
                else None
            ),
            "verification_source": self.verification_source,
            "model_used": self.model_used,
            "schema_version": self.schema_version,
            "annotation_version": self.annotation_version,
            "timestamp": self.timestamp,
            "prompt_version": self.prompt_version,
            "negative_probability": (
                round(self.negative_probability, 4) if self.negative_probability is not None else None
            ),
            "neutral_probability": (
                round(self.neutral_probability, 4) if self.neutral_probability is not None else None
            ),
            "positive_probability": (
                round(self.positive_probability, 4) if self.positive_probability is not None else None
            ),
            "reference_class_count": self.reference_class_count,
            "reference_label": self.reference_label or (self.semantic_polarity.value if self.semantic_polarity else "UNAVAILABLE"),
            "three_class": self.three_class,
            "two_class": self.two_class,
            "binary_projection_label": self.binary_projection_label,
            "binary_projection_status": self.binary_projection_status,
            "status": self.status,
            "failure_reason": self.failure_reason,
            "credential_alias": self.credential_alias,
            "request_id": self.request_id,
            "raw_response": self.raw_response,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SemanticAnnotation":
        status = d.get("status", "AVAILABLE")
        raw_sem_pol = d.get("semantic_polarity")
        if status == "UNAVAILABLE" or raw_sem_pol is None or str(raw_sem_pol).upper() in ("UNAVAILABLE", "NONE"):
            sem_pol = None
        else:
            sem_pol = SemanticReferenceLabel.validate_label(raw_sem_pol)

        gem_pol = (
            SemanticReferenceLabel.validate_label(d["gemini_polarity"])
            if d.get("gemini_polarity") and str(d["gemini_polarity"]).upper() not in ("UNAVAILABLE", "NONE")
            else None
        )
        hum_pol = (
            SemanticReferenceLabel.validate_label(d["human_verified_polarity"])
            if d.get("human_verified_polarity") and str(d["human_verified_polarity"]).upper() not in ("UNAVAILABLE", "NONE")
            else None
        )
        raw_fin_pol = d.get("final_semantic_polarity")
        if status == "UNAVAILABLE" or raw_fin_pol is None or str(raw_fin_pol).upper() in ("UNAVAILABLE", "NONE"):
            fin_pol = None
        elif raw_fin_pol:
            fin_pol = SemanticReferenceLabel.validate_label(raw_fin_pol)
        else:
            fin_pol = sem_pol

        rel_val = d.get("semantic_relation_to_baseline")
        rel = SemanticRelation.from_str(rel_val) if rel_val else None

        v_status = VerificationStatus.UNVERIFIED
        raw_status = d.get("verification_status")
        if raw_status:
            try:
                v_status = VerificationStatus(raw_status)
            except Exception:
                # check aliases
                status_str = str(raw_status).upper()
                if "OVERRIDE" in status_str:
                    v_status = VerificationStatus.HUMAN_OVERRIDDEN
                elif "VERIFIED" in status_str:
                    v_status = VerificationStatus.HUMAN_VERIFIED
                elif "ACCEPTED" in status_str or "AUTOMATED" in status_str:
                    v_status = VerificationStatus.AUTOMATED_REFERENCE
                else:
                    v_status = VerificationStatus.UNVERIFIED

        raw_conf = d.get("confidence")
        conf_val = float(raw_conf) if raw_conf is not None else None

        raw_gem_conf = d.get("gemini_confidence")
        gem_conf_val = float(raw_gem_conf) if raw_gem_conf is not None else None

        provider_val = d.get("provider") or d.get("verification_source", ReferenceProvider.NONE.value)
        if provider_val.upper() in ("GEMINI", "GOOGLE_GEMINI"):
            provider_val = ReferenceProvider.GEMINI.value
        elif provider_val.upper() in ("MANUAL", "HUMAN_OVERRIDE", "HUMAN_OVERRIDDEN"):
            provider_val = ReferenceProvider.MANUAL.value
        elif provider_val.upper() in ("LOCAL_HEURISTIC", "ANTIGRAVITY_EXACT"):
            provider_val = ReferenceProvider.LOCAL_HEURISTIC.value

        return cls(
            sentence_id=d.get("sentence_id", ""),
            sentence_text=d.get("sentence_text", ""),
            semantic_polarity=sem_pol,
            confidence=conf_val,
            reason=d.get("reason", ""),
            ambiguity=d.get("ambiguity", "LOW"),
            semantic_relation_to_baseline=rel,
            verification_status=v_status,
            provider=provider_val,
            gemini_polarity=gem_pol,
            gemini_confidence=gem_conf_val,
            human_verified_polarity=hum_pol,
            final_semantic_polarity=fin_pol,
            verification_source=d.get("verification_source", v_status.value),
            model_used=d.get("model_used", ""),
            schema_version=d.get("schema_version", "v2.0"),
            annotation_version=d.get("annotation_version", "v2.0"),
            timestamp=float(d.get("timestamp", time.time())),
            prompt_version=d.get("prompt_version", "v2.0"),
            negative_probability=(
                float(d["negative_probability"]) if d.get("negative_probability") is not None else None
            ),
            neutral_probability=(
                float(d["neutral_probability"]) if d.get("neutral_probability") is not None else None
            ),
            positive_probability=(
                float(d["positive_probability"]) if d.get("positive_probability") is not None else None
            ),
            reference_class_count=int(d.get("reference_class_count", 3)),
            reference_label=d.get("reference_label"),
            three_class=d.get("three_class", {}),
            two_class=d.get("two_class", {}),
            binary_projection_label=d.get("binary_projection_label"),
            binary_projection_status=d.get("binary_projection_status"),
            status=d.get("status", "AVAILABLE"),
            failure_reason=d.get("failure_reason"),
            credential_alias=d.get("credential_alias"),
            request_id=d.get("request_id"),
            raw_response=d.get("raw_response"),
        )


@dataclass
class SemanticReferenceSet:
    """
    Immutable frozen semantic reference container anchoring baseline and all probes
    for an entire experiment. All benchmark models evaluate against this exact set.
    """
    baseline_annotation: SemanticAnnotation
    probe_annotations: Dict[str, SemanticAnnotation] = field(default_factory=dict)
    frozen: bool = False
    annotation_engine: str = "gemini"
    model: str = "gemini-flash-lite-latest"
    prompt_version: str = "v2.0"
    schema_version: str = "v2.0"
    provider: str = ReferenceProvider.NONE.value
    cache_hits: int = 0
    api_requests: int = 0
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    semantic_label_space: List[str] = field(default_factory=lambda: ["POSITIVE", "NEGATIVE", "NEUTRAL"])

    def override_baseline(self, new_polarity: Union[str, SemanticReferenceLabel], reason: str = ""):
        """Applies a human override to the baseline annotation and re-computes relations."""
        if self.frozen:
            raise RuntimeError("Cannot modify a frozen SemanticReferenceSet.")
        self.baseline_annotation.override_polarity(new_polarity, reason)
        self._recompute_relations()

    def override_probe(self, probe_id: str, new_polarity: Union[str, SemanticReferenceLabel], reason: str = ""):
        """Applies a human override to a probe annotation and re-computes relations."""
        if self.frozen:
            raise RuntimeError("Cannot modify a frozen SemanticReferenceSet.")
        if probe_id not in self.probe_annotations:
            raise KeyError(f"Probe ID '{probe_id}' not found in SemanticReferenceSet.")
        self.probe_annotations[probe_id].override_polarity(new_polarity, reason)
        self._recompute_relations()

    def accept_baseline(self):
        if self.frozen:
            raise RuntimeError("Cannot modify a frozen SemanticReferenceSet.")
        self.baseline_annotation.accept_gemini()
        self._recompute_relations()

    def accept_probe(self, probe_id: str):
        if self.frozen:
            raise RuntimeError("Cannot modify a frozen SemanticReferenceSet.")
        if probe_id in self.probe_annotations:
            self.probe_annotations[probe_id].accept_gemini()
            self._recompute_relations()

    def mark_probe_uncertain(self, probe_id: str, reason: str = ""):
        if self.frozen:
            raise RuntimeError("Cannot modify a frozen SemanticReferenceSet.")
        if probe_id in self.probe_annotations:
            self.probe_annotations[probe_id].mark_uncertain(reason)

    def freeze(self):
        """Freezes this semantic reference set so it cannot be modified during benchmark runs."""
        self._recompute_relations()
        self.frozen = True

    def _recompute_relations(self):
        """Updates expected relations from current final baseline and probe polarities."""
        base_pol = self.baseline_annotation.final_semantic_polarity
        if self.baseline_annotation.status == "UNAVAILABLE" or base_pol is None:
            for probe_id, annot in self.probe_annotations.items():
                if annot.semantic_relation_to_baseline != SemanticRelation.UNCERTAIN:
                    annot.semantic_relation_to_baseline = None
            return

        for probe_id, annot in self.probe_annotations.items():
            # If manually marked UNCERTAIN, preserve it
            if annot.semantic_relation_to_baseline == SemanticRelation.UNCERTAIN:
                continue
            if annot.status == "UNAVAILABLE" or annot.final_semantic_polarity is None:
                annot.semantic_relation_to_baseline = None
                continue
            probe_pol = annot.final_semantic_polarity
            annot.semantic_relation_to_baseline = SemanticRelation.from_polarities(base_pol, probe_pol)

    def get_expected_relation(self, probe_id: str) -> Optional[SemanticRelation]:
        """Returns the expected semantic relation of a probe to the baseline."""
        annot = self.probe_annotations.get(probe_id)
        if annot:
            if annot.semantic_relation_to_baseline is None:
                self._recompute_relations()
            return annot.semantic_relation_to_baseline
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "annotation_engine": self.annotation_engine,
            "model": self.model,
            "provider": self.provider,
            "prompt_version": self.prompt_version,
            "schema_version": self.schema_version,
            "frozen": self.frozen,
            "cache_hits": self.cache_hits,
            "api_requests": self.api_requests,
            "timestamp": self.timestamp,
            "semantic_label_space": self.semantic_label_space,
            "baseline": self.baseline_annotation.to_dict(),
            "probes": {pid: p.to_dict() for pid, p in self.probe_annotations.items()},
            "annotations": [self.baseline_annotation.to_dict()] + [p.to_dict() for p in self.probe_annotations.values()],
            "human_overrides": [
                p.to_dict() for p in [self.baseline_annotation] + list(self.probe_annotations.values())
                if p.verification_status == VerificationStatus.HUMAN_OVERRIDDEN
            ],
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SemanticReferenceSet":
        baseline_data = d.get("baseline")
        if not baseline_data and d.get("annotations"):
            baseline_data = d["annotations"][0]

        baseline = (
            SemanticAnnotation.from_dict(baseline_data)
            if baseline_data
            else SemanticAnnotation(
                sentence_id="baseline",
                sentence_text="",
                semantic_polarity=None,
                status="UNAVAILABLE",
                confidence=None,
            )
        )

        probes = {}
        if "probes" in d and isinstance(d["probes"], dict):
            for pid, pdata in d["probes"].items():
                probes[pid] = SemanticAnnotation.from_dict(pdata)
        elif "annotations" in d:
            for item in d["annotations"][1:]:
                pid = item.get("sentence_id", "")
                probes[pid] = SemanticAnnotation.from_dict(item)

        return cls(
            baseline_annotation=baseline,
            probe_annotations=probes,
            frozen=bool(d.get("frozen", False)),
            annotation_engine=d.get("annotation_engine", "gemini"),
            model=d.get("model", "gemini-flash-lite-latest"),
            provider=d.get("provider", ReferenceProvider.NONE.value),
            prompt_version=d.get("prompt_version", "v2.0"),
            schema_version=d.get("schema_version", "v2.0"),
            cache_hits=int(d.get("cache_hits", 0)),
            api_requests=int(d.get("api_requests", 0)),
            timestamp=d.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S")),
            semantic_label_space=d.get("semantic_label_space", ["POSITIVE", "NEGATIVE", "NEUTRAL"]),
        )
