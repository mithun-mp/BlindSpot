"""
Gemini Semantic Reference Annotator Client (BlindSpot).
Integrates the official Google GenAI Python SDK and authoritative REST fallback
with multi-key credential rotation, model fallback chaining, failure classification,
and strict structured output contracts.

CRITICAL INVARIANTS:
- Gemini is NOT a benchmark target model; it is strictly an external semantic reference service.
- Local sentiment models or heuristics MUST NEVER masquerade as GEMINI ground truth.
- Credential rotation must be based on actual API failure classification (429/quota vs 503/model busy).
- Raw API keys are NEVER logged, printed, or persisted in results, cache, or UI.
- Models in fallback chain must be text-capable Gemini models.
- Baseline and probes are evaluated with identical zero-contamination prompts (no probe-type leakage).
"""
import os
import json
import time
import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Union

try:
    from google import genai
    from google.genai import types as genai_types
    HAS_GOOGLE_GENAI = True
except ImportError:
    HAS_GOOGLE_GENAI = False

import requests

from .types import (
    SemanticReferenceLabel,
    SemanticRelation,
    SemanticAnnotation,
    VerificationStatus,
    ReferenceProvider,
    project_three_class_to_binary,
)

logger = logging.getLogger("blindspot.semantic")


class FailureCategory(str, Enum):
    """Categorized API and inference failures for precise rotation decisions."""
    AUTH_FAILURE = "AUTH_FAILURE"
    QUOTA_EXHAUSTED = "QUOTA_EXHAUSTED"
    RATE_LIMITED = "RATE_LIMITED"
    MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"
    NETWORK_FAILURE = "NETWORK_FAILURE"
    INVALID_REQUEST = "INVALID_REQUEST"
    PARSER_FAILURE = "PARSER_FAILURE"
    UNKNOWN = "UNKNOWN"


class SemanticReferenceUnavailableError(RuntimeError):
    """Raised when the authoritative Gemini reference service cannot produce a result."""
    def __init__(self, message: str, failure_category: FailureCategory = FailureCategory.UNKNOWN):
        super().__init__(message)
        self.failure_category = failure_category


class AllCredentialsExhaustedError(SemanticReferenceUnavailableError):
    """Raised when all configured Gemini credentials have failed or exhausted quota."""
    def __init__(self, message: str = "All Gemini API credentials exhausted"):
        super().__init__(message, failure_category=FailureCategory.QUOTA_EXHAUSTED)


class ModelUnavailableError(SemanticReferenceUnavailableError):
    """Raised when all models in the fallback chain are unavailable/overloaded."""
    def __init__(self, message: str = "All text models in fallback chain unavailable"):
        super().__init__(message, failure_category=FailureCategory.MODEL_UNAVAILABLE)


@dataclass
class KeyCredential:
    """Safe internal representation of an API credential."""
    alias: str
    key: str
    status: str = "AVAILABLE"  # AVAILABLE | QUOTA_EXHAUSTED | AUTH_FAILURE | TEMPORARILY_FAILED
    failure_count: int = 0
    last_error: Optional[str] = None


class CredentialManager:
    """
    Manages multiple Gemini credentials with health tracking and rotation on quota exhaustion.
    Never prints or logs raw keys.
    """
    def __init__(
        self,
        explicit_keys: Optional[List[str]] = None,
        explicit_key: Optional[str] = None,
    ):
        self.credentials: List[KeyCredential] = []
        self.current_index: int = 0
        self._resolve_credentials(explicit_keys, explicit_key)

    def _resolve_credentials(
        self,
        explicit_keys: Optional[List[str]] = None,
        explicit_key: Optional[str] = None,
    ):
        # If explicit keys parameter is passed, use ONLY explicit keys
        if explicit_keys is not None:
            raw_keys = [k.strip() for k in explicit_keys if k and k.strip()]
            self.credentials = [
                KeyCredential(alias=f"gemini_key_{idx + 1}", key=k)
                for idx, k in enumerate(raw_keys)
            ]
            self.current_index = 0
            return

        if explicit_key is not None:
            raw_keys = [explicit_key.strip()] if explicit_key.strip() else []
            self.credentials = [
                KeyCredential(alias=f"gemini_key_{idx + 1}", key=k)
                for idx, k in enumerate(raw_keys)
            ]
            self.current_index = 0
            return

        # Otherwise, resolve from environment and .env hierarchy
        raw_keys: List[str] = []
        env_var_names = [
            "BLINDSPOT_GEMINI_API_KEY_1",
            "BLINDSPOT_GEMINI_API_KEY_2",
            "BLINDSPOT_GEMINI_API_KEY_3",
            "GEMINI_API_KEY_1",
            "GEMINI_API_KEY_2",
            "GEMINI_API_KEY_3",
            "GEMINI_API_KEY",
            "GOOGLE_API_KEY",
        ]
        for var_name in env_var_names:
            val = os.environ.get(var_name, "").strip()
            if val and val not in raw_keys:
                raw_keys.append(val)

        # Local .env file parsing: ALWAYS merge keys from .env
        root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
        if os.path.exists(root_env):
            try:
                with open(root_env, "r", encoding="utf-8") as f:
                    for line in f:
                        clean_line = line.strip()
                        if clean_line and not clean_line.startswith("#") and "=" in clean_line:
                            k, v = clean_line.split("=", 1)
                            k_clean = k.strip()
                            v_clean = v.strip().strip('"').strip("'")
                            if k_clean in env_var_names and v_clean and v_clean not in raw_keys:
                                raw_keys.append(v_clean)
            except Exception as ex:
                logger.debug(f"[SEMANTIC] Could not read .env file: {ex}")

        # Build managed credentials with safe aliases
        self.credentials = [
            KeyCredential(alias=f"gemini_key_{idx + 1}", key=k)
            for idx, k in enumerate(raw_keys)
        ]
        self.current_index = 0

    @property
    def has_credentials(self) -> bool:
        return len(self.credentials) > 0

    def get_current(self) -> Optional[KeyCredential]:
        if not self.credentials:
            return None
        for offset in range(len(self.credentials)):
            idx = (self.current_index + offset) % len(self.credentials)
            if self.credentials[idx].status == "AVAILABLE":
                self.current_index = idx
                return self.credentials[idx]
        return None

    def rotate(self, failure_cat: FailureCategory, reason: str = "") -> Optional[KeyCredential]:
        """Rotates to next available credential when current exhausts quota or fails auth."""
        if not self.credentials:
            return None
        curr = self.credentials[self.current_index]
        curr.failure_count += 1
        curr.last_error = reason

        if failure_cat in (FailureCategory.QUOTA_EXHAUSTED, FailureCategory.RATE_LIMITED):
            curr.status = "QUOTA_EXHAUSTED"
            logger.info(f"[SEMANTIC] key={curr.alias} result=quota_exhausted")
        elif failure_cat == FailureCategory.AUTH_FAILURE:
            curr.status = "AUTH_FAILURE"
            logger.warning(f"[SEMANTIC] key={curr.alias} result=auth_failure")
        else:
            curr.status = "TEMPORARILY_FAILED"

        # Find next available
        for offset in range(1, len(self.credentials) + 1):
            next_idx = (self.current_index + offset) % len(self.credentials)
            if self.credentials[next_idx].status == "AVAILABLE":
                next_cred = self.credentials[next_idx]
                logger.info(f"[SEMANTIC] rotating credential -> {next_cred.alias}")
                self.current_index = next_idx
                return next_cred

        logger.warning("[SEMANTIC] All credentials exhausted or disabled.")
        return None

    def reset_temporary_failures(self):
        for c in self.credentials:
            if c.status == "TEMPORARILY_FAILED":
                c.status = "AVAILABLE"


DEFAULT_SEMANTIC_MODEL_CHAIN = [
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite-preview",
    "gemini-3-flash-preview",
    "gemini-flash-latest",
]


class GeminiSemanticClient:
    """
    Communicates authoritatively with the Google Gemini API to produce structured
    semantic references. Supports SDK and REST paths, multi-key rotation, text model
    fallback, and explicit failure classification.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_keys: Optional[List[str]] = None,
        model_name: Optional[str] = None,
        fallback_model_name: Optional[str] = None,
        model_chain: Optional[List[str]] = None,
        timeout_seconds: int = 15,
        max_retries: int = 2,
        max_retries_per_model: Optional[int] = None,
    ):
        # Resolve credentials with explicit check
        self.credential_manager = CredentialManager(
            explicit_keys=api_keys,
            explicit_key=api_key,
        )

        # Resolve model chain
        if model_chain:
            self.model_chain = [m.strip() for m in model_chain if m and m.strip()]
        else:
            env_chain = os.environ.get("GEMINI_MODEL_CHAIN", "").strip()
            if env_chain:
                self.model_chain = [m.strip() for m in env_chain.split(",") if m.strip()]
            else:
                primary = model_name or os.environ.get("GEMINI_MODEL", "").strip() or DEFAULT_SEMANTIC_MODEL_CHAIN[0]
                secondary = fallback_model_name or os.environ.get("GEMINI_FALLBACK_MODEL", "").strip() or (DEFAULT_SEMANTIC_MODEL_CHAIN[1] if len(DEFAULT_SEMANTIC_MODEL_CHAIN) > 1 else None)
                chain = [primary]
                if secondary and secondary not in chain:
                    chain.append(secondary)
                for default_m in DEFAULT_SEMANTIC_MODEL_CHAIN:
                    if default_m not in chain:
                        chain.append(default_m)
                self.model_chain = chain

        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries_per_model or max_retries

        # Telemetry
        self.requests_count: int = 0
        self.sentences_annotated_count: int = 0
        self.api_failures_count: int = 0
        self.retries_count: int = 0
        self.last_request_time: Optional[float] = None
        self.last_error: Optional[str] = None
        self.last_failure_category: Optional[FailureCategory] = None

    @property
    def is_online(self) -> bool:
        """True strictly if at least one API credential is configured."""
        return self.credential_manager.has_credentials

    @property
    def model_name(self) -> str:
        return self.model_chain[0] if self.model_chain else DEFAULT_SEMANTIC_MODEL_CHAIN[0]

    @property
    def fallback_model_name(self) -> str:
        return self.model_chain[1] if len(self.model_chain) > 1 else ""

    @property
    def api_key(self) -> str:
        """Returns current key without exposing in string representation."""
        curr = self.credential_manager.get_current()
        return curr.key if curr else ""

    @property
    def current_key_alias(self) -> str:
        curr = self.credential_manager.get_current()
        return curr.alias if curr else "none"

    @property
    def status_string(self) -> str:
        if not self.is_online:
            return "Disabled (No API Key)"
        curr = self.credential_manager.get_current()
        alias = curr.alias if curr else "exhausted"
        return f"Connected ({self.model_name}) via [{alias}]"

    def _get_structured_schema(self) -> Dict[str, Any]:
        """
        Structured JSON schema enforcing Contract A 3-class probabilities and label.
        Probabilities must be floats between 0.0 and 1.0 and sum to 1.0.
        """
        return {
            "type": "OBJECT",
            "properties": {
                "annotations": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "sentence_id": {"type": "STRING"},
                            "semantic_polarity": {
                                "type": "STRING",
                                "enum": ["POSITIVE", "NEGATIVE", "NEUTRAL"],
                                "description": "Strict argmax polarity label: NEGATIVE, NEUTRAL, or POSITIVE."
                            },
                            "label": {
                                "type": "STRING",
                                "enum": ["POSITIVE", "NEGATIVE", "NEUTRAL"],
                                "description": "Strict argmax polarity label: NEGATIVE, NEUTRAL, or POSITIVE."
                            },
                            "negative_probability": {
                                "type": "NUMBER",
                                "description": "Probability of negative affective polarity (0.0 to 1.0)."
                            },
                            "neutral_probability": {
                                "type": "NUMBER",
                                "description": "Probability of neutral/objective polarity (0.0 to 1.0)."
                            },
                            "positive_probability": {
                                "type": "NUMBER",
                                "description": "Probability of positive affective polarity (0.0 to 1.0)."
                            },
                            "reason_short": {"type": "STRING"},
                            "ambiguity": {
                                "type": "STRING",
                                "enum": ["LOW", "MEDIUM", "HIGH"]
                            },
                            "semantic_relation_to_baseline": {
                                "type": "STRING",
                                "enum": [
                                    "PRESERVE_POLARITY",
                                    "REVERSE_POLARITY",
                                    "SHIFT_TO_NEUTRAL",
                                    "SHIFT_FROM_NEUTRAL",
                                    "CONTRAST_SHIFT",
                                    "MEANING_CHANGED",
                                    "UNCERTAIN",
                                ],
                            },
                        },
                        "required": [
                            "sentence_id",
                            "negative_probability",
                            "neutral_probability",
                            "positive_probability",
                            "label",
                        ],
                    },
                }
            },
            "required": ["annotations"],
        }

    def _build_batch_prompt(
        self,
        baseline_text: str,
        probes: List[Dict[str, str]],
    ) -> str:
        """
        Constructs zero-contamination prompt for Gemini semantic annotation.
        No probe-type, expected flip, or perturbation category is ever leaked.
        """
        prompt_lines = [
            "You are an authoritative linguistic semantic evaluator establishing ground truth for sentiment analysis.",
            "",
            "SCIENTIFIC INSTRUCTIONS:",
            "1. Evaluate each sentence independently based strictly on the text provided.",
            "2. Judge the affective sentiment polarity: NEGATIVE, NEUTRAL, or POSITIVE.",
            "3. Output calibrated probabilities: negative_probability, neutral_probability, positive_probability.",
            "   - Probabilities must each be between 0.0 and 1.0.",
            "   - Probabilities must sum to approximately 1.0 (negative + neutral + positive ≈ 1.0).",
            "4. The 'label' and 'semantic_polarity' MUST be the strict argmax among the three probabilities.",
            "5. Do NOT assume negation automatically inverts sentiment.",
            "   Example: 'The engine is not damaged' describes absence of defect -> NEUTRAL/favorable, NOT negative.",
            "6. Return ONLY the requested structured JSON matching the provided schema.",
            "",
            "SENTENCES TO EVALUATE:",
            f"- ID: baseline | Text: \"{baseline_text}\"",
        ]
        for p in probes:
            pid = p.get("probe_id", "")
            ptext = p.get("perturbed_text", "")
            prompt_lines.append(f"- ID: {pid} | Text: \"{ptext}\"")

        return "\n".join(prompt_lines)

    def classify_failure(
        self,
        ex: Exception,
        status_code: Optional[int] = None,
        response_text: str = "",
    ) -> FailureCategory:
        """
        Accurately classifies failures to distinguish credential issues (429/quota)
        from model availability issues (503/high demand).
        """
        if status_code in (401, 403):
            return FailureCategory.AUTH_FAILURE
        if status_code == 429:
            return FailureCategory.QUOTA_EXHAUSTED
        if status_code in (500, 502, 503, 504):
            return FailureCategory.MODEL_UNAVAILABLE
        if status_code == 400:
            return FailureCategory.INVALID_REQUEST

        ex_str = f"{type(ex).__name__}: {str(ex)} {response_text}".lower()

        if any(w in ex_str for w in ("api_key_invalid", "permission_denied", "unauthenticated", "invalid api key", "forbidden")):
            return FailureCategory.AUTH_FAILURE
        if any(w in ex_str for w in ("429", "resource_exhausted", "quota", "rate limit", "too many requests")):
            return FailureCategory.QUOTA_EXHAUSTED
        if any(w in ex_str for w in ("503", "unavailable", "high demand", "overloaded", "model busy", "temporarily unavailable", "deadline_exceeded")):
            return FailureCategory.MODEL_UNAVAILABLE
        if any(w in ex_str for w in ("connectionerror", "connecttimeout", "socket", "timed out", "econnreset")):
            return FailureCategory.NETWORK_FAILURE
        if any(w in ex_str for w in ("jsondecodeerror", "json syntax", "parsing error", "malformed json")):
            return FailureCategory.PARSER_FAILURE
        if any(w in ex_str for w in ("invalid_argument", "bad request")):
            return FailureCategory.INVALID_REQUEST

        return FailureCategory.UNKNOWN

    def annotate_batch(
        self,
        baseline_text: str,
        probes: List[Dict[str, str]],
    ) -> Dict[str, SemanticAnnotation]:
        """
        Annotates baseline and a list of probes with Contract A (3-class) and
        Contract B (2-class binary projection).
        Implements credential rotation and model fallback chaining.
        """
        if not self.is_online:
            raise SemanticReferenceUnavailableError(
                "Gemini API key is not configured. Client is offline.",
                failure_category=FailureCategory.AUTH_FAILURE,
            )

        prompt = self._build_batch_prompt(baseline_text, probes)
        schema = self._get_structured_schema()

        # State machine across credentials and models
        model_idx = 0
        transient_retries = 0

        while True:
            current_cred = self.credential_manager.get_current()
            if not current_cred:
                self.last_failure_category = FailureCategory.QUOTA_EXHAUSTED
                raise AllCredentialsExhaustedError("All Gemini API credentials have failed or exhausted quota.")

            if model_idx >= len(self.model_chain):
                self.last_failure_category = FailureCategory.MODEL_UNAVAILABLE
                raise ModelUnavailableError(f"All text models in fallback chain {self.model_chain} are unavailable.")

            current_model = self.model_chain[model_idx]
            self.requests_count += 1
            self.last_request_time = time.time()

            logger.info(
                f"[SEMANTIC] provider=gemini model={current_model} key={current_cred.alias} attempt={transient_retries + 1}"
            )

            try:
                # 1. Primary: Google GenAI SDK if available
                raw_json_str = None
                if HAS_GOOGLE_GENAI:
                    try:
                        sdk_client = genai.Client(api_key=current_cred.key)
                        config = genai_types.GenerateContentConfig(
                            temperature=0.0,
                            response_mime_type="application/json",
                            response_schema=schema,
                        )
                        response = sdk_client.models.generate_content(
                            model=current_model,
                            contents=prompt,
                            config=config,
                        )
                        raw_json_str = response.text or ""
                    except Exception as sdk_ex:
                        failure_cat = self.classify_failure(sdk_ex)
                        logger.debug(f"[SEMANTIC] SDK call failed ({sdk_ex}), trying REST fallback...")

                # 2. REST Fallback with same authoritative Gemini service and credential
                if raw_json_str is None:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{current_model}:generateContent?key={current_cred.key}"
                    payload = {
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "temperature": 0.0,
                            "responseMimeType": "application/json",
                            "responseSchema": schema,
                        },
                    }
                    resp = requests.post(
                        url,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=self.timeout_seconds,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        raw_json_str = (
                            data.get("candidates", [{}])[0]
                            .get("content", {})
                            .get("parts", [{}])[0]
                            .get("text", "")
                        )
                    else:
                        failure_cat = self.classify_failure(
                            Exception(f"HTTP {resp.status_code}"),
                            status_code=resp.status_code,
                            response_text=resp.text,
                        )
                        err_msg = f"Gemini API returned status {resp.status_code}: {resp.text[:200]}"
                        ex = RuntimeError(err_msg)
                        ex.failure_category = failure_cat
                        raise ex

                # 3. Parse and strictly validate structured output
                parsed = self.parse_structured_response(raw_json_str)
                annotations_list = parsed.get("annotations", [])
                if not annotations_list:
                    raise ValueError(f"Gemini returned empty 'annotations' list: {raw_json_str[:150]}")

                result = self._validate_and_build_annotations(
                    annotations_list=annotations_list,
                    baseline_text=baseline_text,
                    probes=probes,
                    model_used=current_model,
                    credential_alias=current_cred.alias,
                    raw_response=parsed,
                )
                self.sentences_annotated_count += len(result)
                logger.info(f"[SEMANTIC] result=success model={current_model}")
                return result

            except Exception as ex:
                self.api_failures_count += 1
                self.last_error = str(ex)
                failure_cat = getattr(ex, "failure_category", None) or self.classify_failure(ex)
                self.last_failure_category = failure_cat

                if failure_cat in (FailureCategory.QUOTA_EXHAUSTED, FailureCategory.RATE_LIMITED):
                    logger.info(f"[SEMANTIC] key={current_cred.alias} result=quota_exhausted")
                    rotated = self.credential_manager.rotate(failure_cat, reason=str(ex))
                    if not rotated:
                        raise AllCredentialsExhaustedError("All Gemini API credentials have exhausted quota.")
                    continue

                elif failure_cat == FailureCategory.AUTH_FAILURE:
                    logger.warning(f"[SEMANTIC] key={current_cred.alias} result=auth_failure")
                    rotated = self.credential_manager.rotate(failure_cat, reason=str(ex))
                    if not rotated:
                        raise AllCredentialsExhaustedError("All Gemini API credentials failed authentication.")
                    continue

                elif failure_cat == FailureCategory.MODEL_UNAVAILABLE:
                    # 503 / Model Busy: DO NOT burn credentials! Advance model in fallback chain
                    logger.info(f"[SEMANTIC] result=503 model_unavailable model={current_model}")
                    model_idx += 1
                    if model_idx < len(self.model_chain):
                        next_model = self.model_chain[model_idx]
                        logger.info(f"[SEMANTIC] fallback=model:{next_model}")
                        transient_retries = 0
                        continue
                    else:
                        raise ModelUnavailableError(f"All models in chain {self.model_chain} are unavailable.")

                elif failure_cat == FailureCategory.NETWORK_FAILURE:
                    transient_retries += 1
                    if transient_retries <= self.max_retries:
                        logger.warning(f"[SEMANTIC] Network error on {current_model}. Retrying ({transient_retries}/{self.max_retries})...")
                        time.sleep(1.0 * transient_retries)
                        continue
                    else:
                        model_idx += 1
                        transient_retries = 0
                        continue

                elif failure_cat == FailureCategory.PARSER_FAILURE:
                    logger.error(f"[SEMANTIC] Malformed response from Gemini on {current_model}: {ex}")
                    raise SemanticReferenceUnavailableError(
                        f"Malformed Gemini structured response: {ex}",
                        failure_category=FailureCategory.PARSER_FAILURE,
                    )

                else:
                    logger.error(f"[SEMANTIC] Unrecoverable Gemini failure on {current_model}: {ex}")
                    raise SemanticReferenceUnavailableError(
                        f"Gemini API call failed: {ex}",
                        failure_category=failure_cat,
                    )

    def _validate_and_build_annotations(
        self,
        annotations_list: List[Dict[str, Any]],
        baseline_text: str,
        probes: List[Dict[str, str]],
        model_used: str,
        credential_alias: str,
        raw_response: Dict[str, Any],
    ) -> Dict[str, SemanticAnnotation]:
        """
        Builds canonical SemanticAnnotation instances fulfilling Contract A (3-class)
        and Contract B (2-class projection).
        """
        probe_texts = {p.get("probe_id", ""): p.get("perturbed_text", "") for p in probes}
        results: Dict[str, SemanticAnnotation] = {}

        for item in annotations_list:
            sid = str(item.get("sentence_id", "")).strip()
            raw_neg = item.get("negative_probability")
            raw_neu = item.get("neutral_probability")
            raw_pos = item.get("positive_probability")

            # Fallback if probabilities missing but confidence / label present
            if raw_neg is None or raw_neu is None or raw_pos is None:
                raw_label = str(item.get("label") or item.get("semantic_polarity", "NEUTRAL")).upper()
                c = float(item.get("confidence", 1.0))
                rem = max(0.0, (1.0 - c) / 2.0)
                if "POS" in raw_label:
                    pos, neg, neu = c, rem, rem
                elif "NEG" in raw_label:
                    neg, pos, neu = c, rem, rem
                else:
                    neu, pos, neg = c, rem, rem
            else:
                neg = max(0.0, min(1.0, float(raw_neg)))
                neu = max(0.0, min(1.0, float(raw_neu)))
                pos = max(0.0, min(1.0, float(raw_pos)))

            # Normalization (ensure probabilities sum to 1.0)
            tot = neg + neu + pos
            if tot > 0:
                neg = neg / tot
                neu = neu / tot
                pos = pos / tot

            # Contract A: Determine 3-class label strictly from probabilities (argmax)
            if neu >= neg and neu >= pos:
                label_val = SemanticReferenceLabel.NEUTRAL
            elif pos > neg:
                label_val = SemanticReferenceLabel.POSITIVE
            else:
                label_val = SemanticReferenceLabel.NEGATIVE

            reason = str(item.get("reason_short", item.get("reason", ""))).strip()
            ambiguity = str(item.get("ambiguity", "LOW")).upper()
            if ambiguity not in ("LOW", "MEDIUM", "HIGH"):
                ambiguity = "LOW"

            raw_rel = item.get("semantic_relation_to_baseline")
            rel = SemanticRelation.from_str(raw_rel) if raw_rel else None

            stext = baseline_text if sid == "baseline" else probe_texts.get(sid, "")

            annot = SemanticAnnotation(
                sentence_id=sid,
                sentence_text=stext,
                semantic_polarity=label_val,
                confidence=max(neg, neu, pos),
                reason=reason,
                ambiguity=ambiguity,
                semantic_relation_to_baseline=rel,
                verification_status=VerificationStatus.AUTOMATED_REFERENCE,
                provider=ReferenceProvider.GEMINI.value,
                gemini_polarity=label_val,
                gemini_confidence=max(neg, neu, pos),
                model_used=model_used,
                negative_probability=neg,
                neutral_probability=neu,
                positive_probability=pos,
                reference_class_count=3,
                reference_label=label_val.value,
                status="AVAILABLE",
                credential_alias=credential_alias,
                raw_response=raw_response,
            )
            results[sid] = annot

        return results

    def parse_structured_response(self, text_response: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Strict validation of structured response format."""
        parsed = json.loads(text_response) if isinstance(text_response, str) else text_response
        if isinstance(parsed, dict):
            # Check top-level polarity
            for key in ("semantic_polarity", "label"):
                if key in parsed:
                    val = parsed[key]
                    if not SemanticReferenceLabel.is_valid(val):
                        raise ValueError(f"Invalid semantic polarity: '{val}'")
            # Check annotations array
            if "annotations" in parsed:
                for item in parsed["annotations"]:
                    for key in ("semantic_polarity", "label"):
                        if key in item:
                            val = item[key]
                            if not SemanticReferenceLabel.is_valid(val):
                                raise ValueError(f"Invalid semantic polarity in annotations: '{val}'")
                return parsed
            elif "semantic_polarity" in parsed or "negative_probability" in parsed:
                return {"annotations": [parsed]}
        raise ValueError("Missing 'annotations' or valid semantic polarity in Gemini response.")

    def _parse_structured_response(self, text_response: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Backward-compatibility alias."""
        return self.parse_structured_response(text_response)

    def get_usage_telemetry(self) -> Dict[str, Any]:
        curr = self.credential_manager.get_current()
        return {
            "is_online": self.is_online,
            "status": self.status_string,
            "model_chain": self.model_chain,
            "current_model": self.model_name,
            "current_credential_alias": curr.alias if curr else "none",
            "requests_count": self.requests_count,
            "sentences_annotated_count": self.sentences_annotated_count,
            "api_failures_count": self.api_failures_count,
            "retries_count": self.retries_count,
            "last_request_time": self.last_request_time,
            "last_error": self.last_error,
            "last_failure_category": (
                self.last_failure_category.value if self.last_failure_category else None
            ),
        }
