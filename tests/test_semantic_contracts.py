"""
Test Suite for BlindSpot Semantic Reference Architecture Repair.
Strictly implements Tests 1 through 12 specified in Section 24:
1. 3-class positive (NEG=0.01, NEU=0.04, POS=0.95 -> 3-class=POSITIVE, 2-class=POSITIVE)
2. 3-class negative (NEG=0.90, NEU=0.08, POS=0.02 -> 3-class=NEGATIVE, 2-class=NEGATIVE)
3. Neutral leaning positive (NEG=0.20, NEU=0.55, POS=0.25 -> 3-class=NEUTRAL, 2-class=POSITIVE)
4. Neutral leaning negative (NEG=0.35, NEU=0.55, POS=0.10 -> 3-class=NEUTRAL, 2-class=NEGATIVE)
5. Neutral tie (NEG=0.20, NEU=0.60, POS=0.20 -> 3-class=NEUTRAL, 2-class=AMBIGUOUS)
6. Probabilities preserved (neutral_probability & 3-class label not overwritten by 2-class projection)
7. No local-model masquerading on Gemini failure (status=UNAVAILABLE, not disguised heuristic)
8. Quota rotation (KEY1 -> 429, KEY2 -> success: KEY1 rotated, KEY2 used)
9. Model busy (KEY1 + PRIMARY -> 503: same credential retained, SECONDARY_TEXT_MODEL used)
10. All credentials exhausted (SEMANTIC_REFERENCE_UNAVAILABLE raised, no fabricated ground truth)
11. Invalid response (Malformed JSON rejected, does not become semantic label)
12. Arbitrary text evaluation (model-derived, zero probe-ID or keyword rules)
"""
import unittest
from unittest.mock import patch, MagicMock
import json
import tempfile
import shutil

from blindspot.core.types import ExpectationType, BehavioralRelation
from blindspot.semantic.types import (
    SemanticReferenceLabel,
    SemanticRelation,
    VerificationStatus,
    ReferenceProvider,
    SemanticAnnotation,
    SemanticReferenceSet,
    project_three_class_to_binary,
)
from blindspot.semantic.client import (
    GeminiSemanticClient,
    FailureCategory,
    AllCredentialsExhaustedError,
    ModelUnavailableError,
    SemanticReferenceUnavailableError,
)
from blindspot.semantic.service import SemanticReferenceService
from blindspot.semantic.cache import SemanticAnnotationCache


class TestSemanticContracts(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.cache = SemanticAnnotationCache(cache_path=f"{self.tmp_dir}/test_cache.json")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    # ----------------------------------------------------------------------
    # TEST 1: 3-class positive
    # NEG=0.01, NEU=0.04, POS=0.95 -> 3-class = POSITIVE, 2-class = POSITIVE
    # ----------------------------------------------------------------------
    def test_01_three_class_positive(self):
        annot = SemanticAnnotation(
            sentence_id="s1",
            sentence_text="The cinematography was breathtaking.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,  # will be computed from probabilities
            negative_probability=0.01,
            neutral_probability=0.04,
            positive_probability=0.95,
        )
        self.assertEqual(annot.three_class["label"], "POSITIVE")
        self.assertEqual(annot.three_class["reference_class_count"], 3)
        self.assertEqual(annot.two_class["label"], "POSITIVE")
        self.assertEqual(annot.two_class["reference_class_count"], 2)
        self.assertEqual(annot.binary_projection_label, "POSITIVE")
        self.assertEqual(annot.binary_projection_status, "DERIVED_FROM_POLARITY_PROBABILITIES")

    # ----------------------------------------------------------------------
    # TEST 2: 3-class negative
    # NEG=0.90, NEU=0.08, POS=0.02 -> 3-class = NEGATIVE, 2-class = NEGATIVE
    # ----------------------------------------------------------------------
    def test_02_three_class_negative(self):
        annot = SemanticAnnotation(
            sentence_id="s2",
            sentence_text="The sound mixing was atrocious.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.90,
            neutral_probability=0.08,
            positive_probability=0.02,
        )
        self.assertEqual(annot.three_class["label"], "NEGATIVE")
        self.assertEqual(annot.three_class["reference_class_count"], 3)
        self.assertEqual(annot.two_class["label"], "NEGATIVE")
        self.assertEqual(annot.two_class["reference_class_count"], 2)
        self.assertEqual(annot.binary_projection_label, "NEGATIVE")

    # ----------------------------------------------------------------------
    # TEST 3: Neutral leaning positive
    # NEG=0.20, NEU=0.55, POS=0.25 -> 3-class = NEUTRAL, 2-class = POSITIVE
    # ----------------------------------------------------------------------
    def test_03_neutral_leaning_positive(self):
        annot = SemanticAnnotation(
            sentence_id="s3",
            sentence_text="The film was not bad.",
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            negative_probability=0.20,
            neutral_probability=0.55,
            positive_probability=0.25,
        )
        # 3-class is strictly NEUTRAL because NEU (0.55) > POS (0.25) & NEG (0.20)
        self.assertEqual(annot.three_class["label"], "NEUTRAL")
        self.assertEqual(annot.semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        # 2-class projection excludes NEUTRAL and compares POS (0.25) vs NEG (0.20) -> POSITIVE
        self.assertEqual(annot.two_class["label"], "POSITIVE")
        self.assertEqual(annot.binary_projection_label, "POSITIVE")
        self.assertEqual(annot.two_class["status"], "DERIVED_FROM_POLARITY_PROBABILITIES")

    # ----------------------------------------------------------------------
    # TEST 4: Neutral leaning negative
    # NEG=0.35, NEU=0.55, POS=0.10 -> 3-class = NEUTRAL, 2-class = NEGATIVE
    # ----------------------------------------------------------------------
    def test_04_neutral_leaning_negative(self):
        annot = SemanticAnnotation(
            sentence_id="s4",
            sentence_text="The film was not particularly great.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.35,
            neutral_probability=0.55,
            positive_probability=0.10,
        )
        # 3-class is NEUTRAL
        self.assertEqual(annot.three_class["label"], "NEUTRAL")
        # 2-class projection compares NEG (0.35) vs POS (0.10) -> NEGATIVE
        self.assertEqual(annot.two_class["label"], "NEGATIVE")
        self.assertEqual(annot.binary_projection_label, "NEGATIVE")

    # ----------------------------------------------------------------------
    # TEST 5: Neutral tie
    # NEG=0.20, NEU=0.60, POS=0.20 -> 3-class = NEUTRAL, 2-class = POSITIVE (deterministic tie-break)
    # ----------------------------------------------------------------------
    def test_05_neutral_tie(self):
        annot = SemanticAnnotation(
            sentence_id="s5",
            sentence_text="The runtime is 120 minutes.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.20,
            neutral_probability=0.60,
            positive_probability=0.20,
        )
        self.assertEqual(annot.three_class["label"], "NEUTRAL")
        # Polarity probabilities are tied -> POSITIVE (deterministic tie-break, never AMBIGUOUS)
        self.assertEqual(annot.two_class["label"], "POSITIVE")
        self.assertEqual(annot.binary_projection_label, "POSITIVE")
        self.assertEqual(annot.two_class["status"], "DERIVED_FROM_POLARITY_PROBABILITIES")

    # ----------------------------------------------------------------------
    # TEST 6: Probabilities must be preserved
    # Projecting to binary does not overwrite neutral_probability or 3-class label
    # ----------------------------------------------------------------------
    def test_06_probabilities_preserved(self):
        proj = project_three_class_to_binary(
            negative_probability=0.21,
            neutral_probability=0.51,
            positive_probability=0.28,
        )
        self.assertEqual(proj["label"], "POSITIVE")
        self.assertEqual(proj["neutral_probability_excluded"], 0.51)
        self.assertEqual(proj["negative_probability"], 0.21)
        self.assertEqual(proj["positive_probability"], 0.28)

        annot = SemanticAnnotation(
            sentence_id="s6",
            sentence_text="A complex statement.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.21,
            neutral_probability=0.51,
            positive_probability=0.28,
        )
        # Verify 3-class retained
        self.assertEqual(annot.three_class["label"], "NEUTRAL")
        self.assertEqual(annot.three_class["neutral_probability"], 0.51)
        self.assertEqual(annot.neutral_probability, 0.51)
        # Verify 2-class derived without mutating 3-class
        self.assertEqual(annot.two_class["label"], "POSITIVE")
        self.assertEqual(annot.two_class["negative_probability"], 0.21)
        self.assertEqual(annot.two_class["positive_probability"], 0.28)

        # Verify serialization preserves both
        d = annot.to_dict()
        self.assertIn("three_class", d)
        self.assertIn("two_class", d)
        self.assertEqual(d["three_class"]["label"], "NEUTRAL")
        self.assertEqual(d["two_class"]["label"], "POSITIVE")
        self.assertEqual(d["neutral_probability"], 0.51)

    # ----------------------------------------------------------------------
    # TEST 7: No local-model masquerading
    # Simulate Gemini failure -> status = UNAVAILABLE, NOT a local heuristic
    # ----------------------------------------------------------------------
    def test_07_no_local_model_masquerading(self):
        client = GeminiSemanticClient(api_keys=["mock_key"])
        service = SemanticReferenceService(client=client, cache=self.cache)

        # Force Gemini client annotate_batch to raise an API failure
        with patch.object(client, "annotate_batch", side_effect=AllCredentialsExhaustedError("API Quota Exceeded")):
            ref_set = service.annotate_experiment(
                baseline_text="The food was great.",
                probes=[{"probe_id": "p1", "perturbed_text": "The food was terrible."}],
                force_refresh=True,
            )

        # Must be explicitly UNAVAILABLE, never silently substituted by DistilBERT or VADER
        self.assertEqual(ref_set.baseline_annotation.status, "UNAVAILABLE")
        self.assertEqual(ref_set.baseline_annotation.verification_status, VerificationStatus.UNAVAILABLE)
        self.assertEqual(ref_set.baseline_annotation.provider, ReferenceProvider.GEMINI.value)
        self.assertIn("Quota Exceeded", ref_set.baseline_annotation.failure_reason)

        probe_annot = ref_set.probe_annotations["p1"]
        self.assertEqual(probe_annot.status, "UNAVAILABLE")
        self.assertEqual(probe_annot.provider, ReferenceProvider.GEMINI.value)

    # ----------------------------------------------------------------------
    # TEST 8: Quota rotation
    # Simulate: KEY1 -> 429, KEY2 -> success. KEY1 rotated, KEY2 used.
    # ----------------------------------------------------------------------
    def test_08_quota_rotation(self):
        client = GeminiSemanticClient(api_keys=["mock_key_1", "mock_key_2"])
        self.assertEqual(client.credential_manager.get_current().alias, "gemini_key_1")

        mock_success_json = json.dumps({
            "annotations": [
                {
                    "sentence_id": "baseline",
                    "negative_probability": 0.05,
                    "neutral_probability": 0.05,
                    "positive_probability": 0.90,
                    "label": "POSITIVE",
                    "reason_short": "Strong positive",
                    "ambiguity": "LOW",
                }
            ]
        })

        call_count = 0

        def mock_post(url, *args, **kwargs):
            nonlocal call_count
            call_count += 1
            mock_resp = MagicMock()
            if "key=mock_key_1" in url:
                mock_resp.status_code = 429
                mock_resp.text = '{"error": {"code": 429, "message": "RESOURCE_EXHAUSTED"}}'
                return mock_resp
            elif "key=mock_key_2" in url:
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [{"content": {"parts": [{"text": mock_success_json}]}}]
                }
                return mock_resp
            mock_resp.status_code = 500
            return mock_resp

        with patch("blindspot.semantic.client.HAS_GOOGLE_GENAI", False):
            with patch("requests.post", side_effect=mock_post):
                result = client.annotate_batch(
                    baseline_text="Excellent performance.",
                    probes=[],
                )

        self.assertIn("baseline", result)
        self.assertEqual(result["baseline"].three_class["label"], "POSITIVE")
        self.assertEqual(result["baseline"].credential_alias, "gemini_key_2")
        # KEY1 is marked QUOTA_EXHAUSTED
        self.assertEqual(client.credential_manager.credentials[0].status, "QUOTA_EXHAUSTED")
        self.assertEqual(client.credential_manager.credentials[1].status, "AVAILABLE")

    # ----------------------------------------------------------------------
    # TEST 9: Model busy
    # Simulate: KEY1 + PRIMARY_MODEL -> 503.
    # Behavior: Same credential retained, SECONDARY_TEXT_MODEL used.
    # ----------------------------------------------------------------------
    def test_09_model_busy_fallback(self):
        client = GeminiSemanticClient(
            api_keys=["mock_key_1", "mock_key_2"],
            model_chain=["gemini-3.5-flash", "gemini-3.1-flash-lite"],
        )

        mock_success_json = json.dumps({
            "annotations": [
                {
                    "sentence_id": "baseline",
                    "negative_probability": 0.02,
                    "neutral_probability": 0.08,
                    "positive_probability": 0.90,
                    "label": "POSITIVE",
                    "reason_short": "Secondary model positive",
                    "ambiguity": "LOW",
                }
            ]
        })

        models_queried = []

        def mock_post(url, *args, **kwargs):
            mock_resp = MagicMock()
            if "gemini-3.5-flash" in url:
                models_queried.append("gemini-3.5-flash")
                mock_resp.status_code = 503
                mock_resp.text = '{"error": {"code": 503, "message": "The model is overloaded. High demand."}}'
                return mock_resp
            elif "gemini-3.1-flash-lite" in url:
                models_queried.append("gemini-3.1-flash-lite")
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [{"content": {"parts": [{"text": mock_success_json}]}}]
                }
                return mock_resp
            mock_resp.status_code = 500
            return mock_resp

        with patch("blindspot.semantic.client.HAS_GOOGLE_GENAI", False):
            with patch("requests.post", side_effect=mock_post):
                result = client.annotate_batch(
                    baseline_text="Splendid display.",
                    probes=[],
                )

        self.assertIn("baseline", result)
        # Succeeded on secondary model
        self.assertEqual(result["baseline"].model_used, "gemini-3.1-flash-lite")
        # Credential was NOT burned or exhausted: KEY1 is still AVAILABLE!
        self.assertEqual(client.credential_manager.credentials[0].status, "AVAILABLE")
        self.assertEqual(result["baseline"].credential_alias, "gemini_key_1")
        self.assertIn("gemini-3.5-flash", models_queried)
        self.assertIn("gemini-3.1-flash-lite", models_queried)

    # ----------------------------------------------------------------------
    # TEST 10: All credentials exhausted
    # Raises SEMANTIC_REFERENCE_UNAVAILABLE, never fabricates reference.
    # ----------------------------------------------------------------------
    def test_10_all_credentials_exhausted(self):
        client = GeminiSemanticClient(api_keys=["mock_key_1", "mock_key_2"])

        def mock_post(url, *args, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 429
            mock_resp.text = '{"error": {"code": 429, "message": "Quota exceeded"}}'
            return mock_resp

        with patch("blindspot.semantic.client.HAS_GOOGLE_GENAI", False):
            with patch("requests.post", side_effect=mock_post):
                with self.assertRaises(AllCredentialsExhaustedError):
                    client.annotate_batch("A test input.", [])

    # ----------------------------------------------------------------------
    # TEST 11: Invalid response
    # Malformed Gemini JSON must NOT become a semantic label.
    # ----------------------------------------------------------------------
    def test_11_invalid_response(self):
        client = GeminiSemanticClient(api_keys=["mock_key"])

        def mock_post(url, *args, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            # Malformed JSON (truncated string)
            mock_resp.json.return_value = {
                "candidates": [{"content": {"parts": [{"text": '{"annotations": [{"sentence_id": "base", "label": "POS'}]}}]
            }
            return mock_resp

        with patch("blindspot.semantic.client.HAS_GOOGLE_GENAI", False):
            with patch("requests.post", side_effect=mock_post):
                with self.assertRaises(SemanticReferenceUnavailableError):
                    client.annotate_batch("Valid text.", [])

    # ----------------------------------------------------------------------
    # TEST 12: Arbitrary text
    # Evaluator operates dynamically on text it has never seen before.
    # No probe-ID lookup, no keyword hard-coding.
    # ----------------------------------------------------------------------
    def test_12_arbitrary_unseen_text(self):
        client = GeminiSemanticClient(api_keys=["mock_key"])

        unseen_text = "Quantum decoherence in superconducting qubits is non-trivial."
        mock_response_json = json.dumps({
            "annotations": [
                {
                    "sentence_id": "arbitrary_99",
                    "negative_probability": 0.15,
                    "neutral_probability": 0.70,
                    "positive_probability": 0.15,
                    "label": "NEUTRAL",
                    "reason_short": "Technical scientific statement",
                    "ambiguity": "LOW",
                }
            ]
        })

        def mock_post(url, *args, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                "candidates": [{"content": {"parts": [{"text": mock_response_json}]}}]
            }
            return mock_resp

        with patch("blindspot.semantic.client.HAS_GOOGLE_GENAI", False):
            with patch("requests.post", side_effect=mock_post):
                result = client.annotate_batch(
                    baseline_text=unseen_text,
                    probes=[],
                )

        annot = result.get("baseline") or result.get("arbitrary_99")
        self.assertIsNotNone(annot)
        self.assertEqual(annot.three_class["label"], "NEUTRAL")
        self.assertEqual(annot.two_class["label"], "POSITIVE")


class TestForensicSemanticPipelineContract(unittest.TestCase):
    """
    Strict regression test suite verifying the 14 forensic contract rules
    specified in Section 14 of the prompt.
    """

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.cache = SemanticAnnotationCache(cache_path=f"{self.tmp_dir}/test_cache.json")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    # TEST 1: Gemini/API failure must NOT produce NEUTRAL.
    # Expected: polarity != NEUTRAL (None), status = UNAVAILABLE, no semantic behavioral relation
    def test_01_api_failure_never_produces_neutral(self):
        client = GeminiSemanticClient(api_keys=["mock_key"])
        service = SemanticReferenceService(client=client, cache=self.cache)

        with patch.object(client, "annotate_batch", side_effect=AllCredentialsExhaustedError("All credentials failed")):
            ref_set = service.annotate_experiment(
                baseline_text="The cinematography was breathtaking.",
                probes=[{"probe_id": "p1", "perturbed_text": "The cinematography was bad."}],
                force_refresh=True,
            )

        base = ref_set.baseline_annotation
        self.assertEqual(base.status, "UNAVAILABLE")
        self.assertIsNot(base.semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertIsNone(base.semantic_polarity)
        self.assertIsNone(base.final_semantic_polarity)

        probe = ref_set.probe_annotations["p1"]
        self.assertEqual(probe.status, "UNAVAILABLE")
        self.assertIsNot(probe.semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertIsNone(probe.semantic_polarity)
        self.assertIsNone(probe.final_semantic_polarity)
        self.assertIsNone(probe.semantic_relation_to_baseline)

    # TEST 2: Successful Gemini POSITIVE remains POSITIVE.
    def test_02_successful_gemini_positive_remains_positive(self):
        annot = SemanticAnnotation(
            sentence_id="s_pos",
            sentence_text="A masterpiece of storytelling.",
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            negative_probability=0.03,
            neutral_probability=0.07,
            positive_probability=0.90,
        )
        self.assertEqual(annot.status, "AVAILABLE")
        self.assertEqual(annot.semantic_polarity, SemanticReferenceLabel.POSITIVE)
        self.assertEqual(annot.final_semantic_polarity, SemanticReferenceLabel.POSITIVE)
        self.assertEqual(annot.three_class["label"], "POSITIVE")
        self.assertEqual(annot.two_class["label"], "POSITIVE")

    # TEST 3: Successful Gemini NEGATIVE remains NEGATIVE.
    def test_03_successful_gemini_negative_remains_negative(self):
        annot = SemanticAnnotation(
            sentence_id="s_neg",
            sentence_text="An absolute waste of time.",
            semantic_polarity=SemanticReferenceLabel.NEGATIVE,
            negative_probability=0.88,
            neutral_probability=0.09,
            positive_probability=0.03,
        )
        self.assertEqual(annot.status, "AVAILABLE")
        self.assertEqual(annot.semantic_polarity, SemanticReferenceLabel.NEGATIVE)
        self.assertEqual(annot.final_semantic_polarity, SemanticReferenceLabel.NEGATIVE)
        self.assertEqual(annot.three_class["label"], "NEGATIVE")
        self.assertEqual(annot.two_class["label"], "NEGATIVE")

    # TEST 4: Successful Gemini NEUTRAL remains NEUTRAL as the semantic reference.
    def test_04_successful_gemini_neutral_remains_neutral_semantic_reference(self):
        annot = SemanticAnnotation(
            sentence_id="s_neu",
            sentence_text="The runtime is 105 minutes.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.10,
            neutral_probability=0.80,
            positive_probability=0.10,
        )
        self.assertEqual(annot.status, "AVAILABLE")
        self.assertEqual(annot.semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(annot.final_semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(annot.three_class["label"], "NEUTRAL")

    # TEST 5: Genuine NEUTRAL probability fallback selection:
    # 3-class label = NEUTRAL, binary fallback = higher of positive vs negative.
    def test_05_genuine_neutral_higher_binary_alternative_selected(self):
        annot = SemanticAnnotation(
            sentence_id="s_neu_lead",
            sentence_text="The film was okay I suppose.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.18,
            neutral_probability=0.52,
            positive_probability=0.30,
        )
        self.assertEqual(annot.semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(annot.final_semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(annot.three_class["label"], "NEUTRAL")
        # Higher of positive (0.30) vs negative (0.18) is POSITIVE
        self.assertEqual(annot.two_class["label"], "POSITIVE")

    # TEST 6: Genuine NEUTRAL with POSITIVE higher than NEGATIVE selects POSITIVE.
    def test_06_genuine_neutral_positive_higher_than_negative(self):
        annot = SemanticAnnotation(
            sentence_id="s_neu_pos",
            sentence_text="The acting was not bad at all.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.15,
            neutral_probability=0.55,
            positive_probability=0.30,
        )
        self.assertEqual(annot.semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(annot.two_class["label"], "POSITIVE")

    # TEST 7: Genuine NEUTRAL with NEGATIVE higher than POSITIVE selects NEGATIVE.
    def test_07_genuine_neutral_negative_higher_than_positive(self):
        annot = SemanticAnnotation(
            sentence_id="s_neu_neg",
            sentence_text="The movie was not particularly impressive.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.32,
            neutral_probability=0.58,
            positive_probability=0.10,
        )
        self.assertEqual(annot.semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(annot.two_class["label"], "NEGATIVE")

    # TEST 8: POSITIVE -> NEUTRAL remains SHIFT_TO_NEUTRAL.
    def test_08_positive_to_neutral_remains_shift_to_neutral(self):
        base = SemanticAnnotation(
            sentence_id="base",
            sentence_text="The movie was great.",
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            negative_probability=0.05,
            neutral_probability=0.05,
            positive_probability=0.90,
        )
        probe = SemanticAnnotation(
            sentence_id="p1",
            sentence_text="The movie was okay.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.15,
            neutral_probability=0.60,
            positive_probability=0.25,
        )
        ref_set = SemanticReferenceSet(baseline_annotation=base, probe_annotations={"p1": probe})
        ref_set._recompute_relations()
        self.assertEqual(probe.semantic_relation_to_baseline, SemanticRelation.SHIFT_TO_NEUTRAL)

    # TEST 9: NEGATIVE -> NEUTRAL remains SHIFT_TO_NEUTRAL.
    def test_09_negative_to_neutral_remains_shift_to_neutral(self):
        base = SemanticAnnotation(
            sentence_id="base",
            sentence_text="The movie was terrible.",
            semantic_polarity=SemanticReferenceLabel.NEGATIVE,
            negative_probability=0.90,
            neutral_probability=0.05,
            positive_probability=0.05,
        )
        probe = SemanticAnnotation(
            sentence_id="p1",
            sentence_text="The movie was ordinary.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.25,
            neutral_probability=0.60,
            positive_probability=0.15,
        )
        ref_set = SemanticReferenceSet(baseline_annotation=base, probe_annotations={"p1": probe})
        ref_set._recompute_relations()
        self.assertEqual(probe.semantic_relation_to_baseline, SemanticRelation.SHIFT_TO_NEUTRAL)

    # TEST 10: NEUTRAL -> POSITIVE remains SHIFT_FROM_NEUTRAL.
    def test_10_neutral_to_positive_remains_shift_from_neutral(self):
        base = SemanticAnnotation(
            sentence_id="base",
            sentence_text="The movie was okay.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.15,
            neutral_probability=0.60,
            positive_probability=0.25,
        )
        probe = SemanticAnnotation(
            sentence_id="p1",
            sentence_text="The movie was extraordinary.",
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            negative_probability=0.02,
            neutral_probability=0.08,
            positive_probability=0.90,
        )
        ref_set = SemanticReferenceSet(baseline_annotation=base, probe_annotations={"p1": probe})
        ref_set._recompute_relations()
        self.assertEqual(probe.semantic_relation_to_baseline, SemanticRelation.SHIFT_FROM_NEUTRAL)

    # TEST 11: NEUTRAL -> NEGATIVE remains SHIFT_FROM_NEUTRAL.
    def test_11_neutral_to_negative_remains_shift_from_neutral(self):
        base = SemanticAnnotation(
            sentence_id="base",
            sentence_text="The movie was okay.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.15,
            neutral_probability=0.60,
            positive_probability=0.25,
        )
        probe = SemanticAnnotation(
            sentence_id="p1",
            sentence_text="The movie was atrocious.",
            semantic_polarity=SemanticReferenceLabel.NEGATIVE,
            negative_probability=0.92,
            neutral_probability=0.05,
            positive_probability=0.03,
        )
        ref_set = SemanticReferenceSet(baseline_annotation=base, probe_annotations={"p1": probe})
        ref_set._recompute_relations()
        self.assertEqual(probe.semantic_relation_to_baseline, SemanticRelation.SHIFT_FROM_NEUTRAL)

    # TEST 12: Unavailable semantic reference never becomes PRESERVE_POLARITY.
    def test_12_unavailable_never_becomes_preserve_polarity(self):
        base = SemanticAnnotation(
            sentence_id="base",
            sentence_text="Baseline text.",
            semantic_polarity=None,
            status="UNAVAILABLE",
            failure_reason="API error",
        )
        probe = SemanticAnnotation(
            sentence_id="p1",
            sentence_text="Probe text.",
            semantic_polarity=None,
            status="UNAVAILABLE",
            failure_reason="API error",
        )
        ref_set = SemanticReferenceSet(baseline_annotation=base, probe_annotations={"p1": probe})
        ref_set._recompute_relations()

        # Crucial invariant: never fabricate PRESERVE_POLARITY
        self.assertIsNone(probe.semantic_relation_to_baseline)
        self.assertNotEqual(probe.semantic_relation_to_baseline, SemanticRelation.PRESERVE_POLARITY)

    # TEST 13: Baseline semantic reference and binary expectation remain separate.
    def test_13_baseline_semantic_reference_and_binary_expectation_separate(self):
        base = SemanticAnnotation(
            sentence_id="base",
            sentence_text="Average experience.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.18,
            neutral_probability=0.52,
            positive_probability=0.30,
        )
        # 3-class semantic reference
        self.assertEqual(base.semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(base.final_semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(base.three_class["label"], "NEUTRAL")

        # 2-class binary expectation
        self.assertEqual(base.two_class["label"], "POSITIVE")
        self.assertEqual(base.binary_projection_label, "POSITIVE")

        # Invariant: binary projection does not overwrite semantic reference
        self.assertNotEqual(base.final_semantic_polarity.value, base.two_class["label"])

    # TEST 14: Probe semantic reference and binary expectation remain separate.
    def test_14_probe_semantic_reference_and_binary_expectation_separate(self):
        probe = SemanticAnnotation(
            sentence_id="p1",
            sentence_text="Rather unremarkable.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.34,
            neutral_probability=0.56,
            positive_probability=0.10,
        )
        # 3-class semantic reference
        self.assertEqual(probe.semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(probe.final_semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(probe.three_class["label"], "NEUTRAL")

        # 2-class binary expectation
        self.assertEqual(probe.two_class["label"], "NEGATIVE")
        self.assertEqual(probe.binary_projection_label, "NEGATIVE")

        # Invariant: probe semantic reference remains NEUTRAL
        self.assertEqual(probe.final_semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(probe.two_class["label"], "NEGATIVE")

    # TEST 15: Neutral binary projection contract exact examples
    # TEST 15: Neutral binary projection contract exact examples
    def test_15_neutral_binary_projection_contract_exact_examples(self):
        # Example 1: pos = 0.60, neg = 0.20, neu = 0.20 -> binary = POSITIVE
        proj1 = project_three_class_to_binary(
            negative_probability=0.20,
            neutral_probability=0.20,
            positive_probability=0.60,
        )
        self.assertEqual(proj1["label"], "POSITIVE")

        # Example 2: pos = 0.20, neg = 0.60, neu = 0.20 -> binary = NEGATIVE
        proj2 = project_three_class_to_binary(
            negative_probability=0.60,
            neutral_probability=0.20,
            positive_probability=0.20,
        )
        self.assertEqual(proj2["label"], "NEGATIVE")

        # Example 3: pos = 0.05, neg = 0.05, neu = 0.90 -> binary = POSITIVE (tie-break)
        proj3 = project_three_class_to_binary(
            negative_probability=0.05,
            neutral_probability=0.90,
            positive_probability=0.05,
        )
        self.assertEqual(proj3["label"], "POSITIVE")

        # Invariant: 3-class polarity is strictly NEUTRAL and not overwritten by binary projection
        annot3 = SemanticAnnotation(
            sentence_id="ex3",
            sentence_text="Example 3 text.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.05,
            neutral_probability=0.90,
            positive_probability=0.05,
        )
        self.assertEqual(annot3.two_class["label"], "POSITIVE")
        self.assertEqual(annot3.binary_projection_label, "POSITIVE")
        self.assertEqual(annot3.semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(annot3.final_semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(annot3.three_class["label"], "NEUTRAL")

    # TEST 16: Baseline NEUTRAL + Probe NEGATIVE remains SHIFT_FROM_NEUTRAL under 2-class model evaluation
    def test_16_neutral_to_negative_remains_shift_from_neutral_under_2class_model(self):
        from blindspot.core.types import LinguisticProbe, SharedProbeSet
        from blindspot.testing.behavioral import BehavioralTester

        base = SemanticAnnotation(
            sentence_id="base",
            sentence_text="The film was okay.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.05,
            neutral_probability=0.90,
            positive_probability=0.05,
        )
        probe_annot = SemanticAnnotation(
            sentence_id="p1",
            sentence_text="The film was awful.",
            semantic_polarity=SemanticReferenceLabel.NEGATIVE,
            negative_probability=0.90,
            neutral_probability=0.05,
            positive_probability=0.05,
        )
        ref_set = SemanticReferenceSet(baseline_annotation=base, probe_annotations={"p1": probe_annot})
        ref_set._recompute_relations()

        # Invariant 1: Semantic relation must be SHIFT_FROM_NEUTRAL, never REVERSE_POLARITY
        self.assertEqual(probe_annot.semantic_relation_to_baseline, SemanticRelation.SHIFT_FROM_NEUTRAL)

        # Invariant 2: When evaluated by BehavioralTester on a 2-class model, relation remains SHIFT_FROM_NEUTRAL
        probe_obj = LinguisticProbe(
            probe_id="p1",
            seed_text="The film was okay.",
            perturbed_text="The film was awful.",
            perturbation_type="negative_injection",
            description="injecting negative sentiment",
            expected_flip=True,
            expected_semantic_effect="SHIFT_FROM_NEUTRAL",
            semantic_intent="SHIFT_FROM_NEUTRAL",
        )
        probe_set = SharedProbeSet(probe_set_id="test_set_16", seed_texts=["The film was okay."], probes=[probe_obj], semantic_reference_set=ref_set)

        mock_2class_model = MagicMock()
        mock_2class_model.num_classes = 2
        mock_2class_model.labels = ["NEGATIVE", "POSITIVE"]
        mock_2class_model.model_name = "mock_2class"
        mock_2class_model.predict_result.return_value = MagicMock(
            label="POSITIVE", confidence=0.85, probabilities={"POSITIVE": 0.85, "NEGATIVE": 0.15}, semantic_polarity=MagicMock(value="POSITIVE")
        )
        mock_2class_model.predict_results_batch.return_value = [
            MagicMock(
                label="NEGATIVE", confidence=0.88, probabilities={"POSITIVE": 0.12, "NEGATIVE": 0.88}, semantic_polarity=MagicMock(value="NEGATIVE"),
                evaluate_semantic_compatibility=MagicMock()
            )
        ]

        tester = BehavioralTester(mock_2class_model)
        results = tester.evaluate_shared_probes(probe_set)
        evaluations = results["evaluations"]

        self.assertEqual(len(evaluations), 1)
        eval_item = evaluations[0]
        # Invariant: expectation MUST NOT be converted into POLARITY_REVERSED / REVERSE_POLARITY
        self.assertEqual(eval_item.expected_semantic_effect, "SHIFT_FROM_NEUTRAL")
        self.assertEqual(probe_obj.expectation.expected_semantic_relation, BehavioralRelation.NEUTRAL_TO_NEGATIVE)
        self.assertNotEqual(probe_obj.expectation.expected_semantic_relation, BehavioralRelation.POLARITY_REVERSED)

    # TEST 17: Baseline POSITIVE + Probe NEUTRAL remains SHIFT_TO_NEUTRAL under 2-class model evaluation
    def test_17_positive_to_neutral_remains_shift_to_neutral_under_2class_model(self):
        from blindspot.core.types import LinguisticProbe, SharedProbeSet
        from blindspot.testing.behavioral import BehavioralTester

        base = SemanticAnnotation(
            sentence_id="base",
            sentence_text="The film was great.",
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            negative_probability=0.05,
            neutral_probability=0.05,
            positive_probability=0.90,
        )
        probe_annot = SemanticAnnotation(
            sentence_id="p1",
            sentence_text="The film was not bad.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            negative_probability=0.10,
            neutral_probability=0.70,
            positive_probability=0.20,
        )
        ref_set = SemanticReferenceSet(baseline_annotation=base, probe_annotations={"p1": probe_annot})
        ref_set._recompute_relations()

        # Invariant 1: Semantic relation must be SHIFT_TO_NEUTRAL, never PRESERVE_POLARITY
        self.assertEqual(probe_annot.semantic_relation_to_baseline, SemanticRelation.SHIFT_TO_NEUTRAL)

        probe_obj = LinguisticProbe(
            probe_id="p1",
            seed_text="The film was great.",
            perturbed_text="The film was not bad.",
            perturbation_type="downtoning",
            description="downtoning positive sentiment",
            expected_flip=False,
            expected_semantic_effect="SHIFT_TO_NEUTRAL",
            semantic_intent="SHIFT_TO_NEUTRAL",
        )
        probe_set = SharedProbeSet(probe_set_id="test_set_17", seed_texts=["The film was great."], probes=[probe_obj], semantic_reference_set=ref_set)

        mock_2class_model = MagicMock()
        mock_2class_model.num_classes = 2
        mock_2class_model.labels = ["NEGATIVE", "POSITIVE"]
        mock_2class_model.model_name = "mock_2class"
        mock_2class_model.predict_result.return_value = MagicMock(
            label="POSITIVE", confidence=0.90, probabilities={"POSITIVE": 0.90, "NEGATIVE": 0.10}, semantic_polarity=MagicMock(value="POSITIVE")
        )
        mock_2class_model.predict_results_batch.return_value = [
            MagicMock(
                label="POSITIVE", confidence=0.75, probabilities={"POSITIVE": 0.75, "NEGATIVE": 0.25}, semantic_polarity=MagicMock(value="POSITIVE"),
                evaluate_semantic_compatibility=MagicMock()
            )
        ]

        tester = BehavioralTester(mock_2class_model)
        results = tester.evaluate_shared_probes(probe_set)
        evaluations = results["evaluations"]

        self.assertEqual(len(evaluations), 1)
        eval_item = evaluations[0]
        # Invariant: expectation MUST NOT be converted into SAME_POLARITY / PRESERVE_POLARITY
        self.assertEqual(eval_item.expected_semantic_effect, "SHIFT_TO_NEUTRAL")
        self.assertEqual(probe_obj.expectation.expected_semantic_relation, BehavioralRelation.POSITIVE_TO_NEUTRAL)
        self.assertNotEqual(probe_obj.expectation.expected_semantic_relation, BehavioralRelation.SAME_POLARITY)


if __name__ == "__main__":
    unittest.main()
