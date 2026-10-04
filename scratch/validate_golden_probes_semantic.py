"""
Golden Probes Validation for Semantic Reference Subsystem Repair.
Runs the 7 golden probes against:
1. Gemini 3-class authoritative reference
2. Gemini 2-class deterministic binary projection
3. DistilBERT SST-2 (2-class target model)
4. CardiffNLP Twitter-RoBERTa (3-class target model)
Outputs the complete comparison table.
"""
import os
import sys
import json
import logging

logging.basicConfig(level=logging.WARNING)

from blindspot.semantic.service import get_semantic_service
from blindspot.semantic.types import SemanticReferenceLabel
from blindspot.models.cache import ModelCache
from blindspot.core.types import LinguisticProbe, SharedProbeSet
from blindspot.testing.behavioral import BehavioralTester

def main():
    print("=" * 80)
    print("BLINDSPOT — GOLDEN PROBES VALIDATION (SECTION 25)")
    print("=" * 80)

    # 1. Initialize Semantic Service
    service = get_semantic_service()
    print(f"Semantic Client Status: {service.client.status_string}")
    print(f"Model Chain: {service.client.model_chain}")
    print(f"Current Credential Alias: {service.client.current_key_alias}")

    # 2. Define the 7 golden probes
    baseline_text = "The movie was great and the acting was superb."

    probes_data = [
        {
            "probe_id": "P01_NEGATION",
            "type": "NEGATION_INSERTION",
            "text": "The movie was not great and the acting was superb.",
        },
        {
            "probe_id": "P02_DOUBLE_NEG",
            "type": "DOUBLE_NEGATION",
            "text": "The movie was not not great and the acting was superb.",
        },
        {
            "probe_id": "P03_INTENSITY_HIGH",
            "type": "INTENSITY",
            "text": "The movie was exceptionally great and the acting was absolutely superb.",
        },
        {
            "probe_id": "P04_INTENSITY_LOW",
            "type": "INTENSITY",
            "text": "The movie was somewhat great and the acting was relatively superb.",
        },
        {
            "probe_id": "P05_SYNONYM",
            "type": "SYNONYM_SUBSTITUTION",
            "text": "The film was great and the performance was superb.",
        },
        {
            "probe_id": "P06_CONTRAST_NEG",
            "type": "CONTRAST_NEGATIVE_APPEND",
            "text": "The movie was great and the acting was superb, but the plot was dreadful.",
        },
        {
            "probe_id": "P07_CONTRAST_POS",
            "type": "CONTRAST_POSITIVE_APPEND",
            "text": "The plot was dreadful, but the movie was great and the acting was superb.",
        },
    ]

    linguistic_probes = []
    for p in probes_data:
        lp = LinguisticProbe.create(
            seed_text=baseline_text,
            perturbed_text=p["text"],
            perturbation_type=p["type"],
            expected_flip=False,
            name=p["probe_id"],
        )
        lp.probe_id = p["probe_id"]
        linguistic_probes.append(lp)

    probe_set = SharedProbeSet(
        probe_set_id="golden_probes_eval",
        seed_texts=[baseline_text],
        probes=linguistic_probes,
    )

    # Annotate experiment through Semantic Service
    print("\nAnnotating experiment via Gemini Authoritative Reference...")
    ref_set = service.annotate_experiment(baseline_text, linguistic_probes, force_refresh=False)
    probe_set.semantic_reference_set = ref_set
    ref_set.freeze()

    # Load target models
    cache = ModelCache.get_shared_cache()
    distilbert_id = "distilbert-base-uncased-finetuned-sst-2-english"
    roberta_id = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    print(f"\nEvaluating Target Models:")
    print(f"1. {distilbert_id} (2-class)")
    model_2c = cache.get_or_load(distilbert_id)
    tester_2c = BehavioralTester(model_2c)
    eval_2c = tester_2c.evaluate_shared_probes(probe_set)

    print(f"2. {roberta_id} (3-class)")
    model_3c = cache.get_or_load(roberta_id)
    tester_3c = BehavioralTester(model_3c)
    eval_3c = tester_3c.evaluate_shared_probes(probe_set)

    # Report baseline
    base_annot = ref_set.baseline_annotation
    print("\n" + "=" * 80)
    print("BASELINE EVALUATION:")
    print(f"Text: '{baseline_text}'")
    print(f"Gemini 3-Class Reference: {base_annot.three_class.get('label')} "
          f"(NEG={base_annot.negative_probability:.2f}, NEU={base_annot.neutral_probability:.2f}, POS={base_annot.positive_probability:.2f})")
    print(f"Gemini 2-Class Projection: {base_annot.two_class.get('label')} "
          f"({base_annot.two_class.get('status')})")
    def get_base_info(b):
        if hasattr(b, 'prediction'):
            p = b.prediction
            lbl = getattr(p, 'label', p.get('label') if isinstance(p, dict) else str(p))
            conf = getattr(p, 'confidence', p.get('confidence', 0.0) if isinstance(p, dict) else 0.0)
            return lbl, conf
        elif isinstance(b, dict):
            p = b.get('prediction')
            if p:
                lbl = getattr(p, 'label', p.get('label') if isinstance(p, dict) else str(p))
                conf = getattr(p, 'confidence', p.get('confidence', 0.0) if isinstance(p, dict) else 0.0)
                return lbl, conf
            return b.get('predicted_label', b.get('label', 'UNKNOWN')), b.get('confidence', 0.0)
        return "UNKNOWN", 0.0

    b2_lbl, b2_conf = get_base_info(eval_2c['baselines'][baseline_text])
    b3_lbl, b3_conf = get_base_info(eval_3c['baselines'][baseline_text])
    print(f"DistilBERT (2-class) Pred: {b2_lbl} ({b2_conf:.2f})")
    print(f"Twitter-RoBERTa (3-class) Pred: {b3_lbl} ({b3_conf:.2f})")

    # Report probes
    print("\n" + "=" * 80)
    print(f"{'Probe ID':<18} | {'Type':<20} | {'Gemini 3-Class':<15} | {'Gemini 2-Class':<15} | {'DistilBERT (2c)':<16} | {'RoBERTa (3c)':<14} | {'Outcome (2c)':<16}")
    print("-" * 125)

    def get_pred_str(e):
        if not e:
            return "N/A"
        p = getattr(e, 'perturbed_prediction', e.get('perturbed_prediction') if isinstance(e, dict) else None)
        if not p:
            return "N/A"
        lbl = getattr(p, 'label', p.get('label') if isinstance(p, dict) else str(p))
        conf = getattr(p, 'confidence', p.get('confidence', 0.0) if isinstance(p, dict) else 0.0)
        return f"{lbl} ({conf:.2f})"

    def get_outcome(e):
        if not e:
            return "N/A"
        return getattr(e, 'behavioral_outcome', e.get('behavioral_outcome') if isinstance(e, dict) else "N/A")

    eval_map_2c = {
        getattr(e, 'probe_id', e.get('probe_id') if isinstance(e, dict) else ''): e
        for e in eval_2c["evaluations"]
    }
    eval_map_3c = {
        getattr(e, 'probe_id', e.get('probe_id') if isinstance(e, dict) else ''): e
        for e in eval_3c["evaluations"]
    }

    results_table = []
    for p in probes_data:
        pid = p["probe_id"]
        ptype = p["type"]
        annot = ref_set.probe_annotations.get(pid)
        e2 = eval_map_2c.get(pid)
        e3 = eval_map_3c.get(pid)

        g3 = f"{annot.three_class.get('label')} ({annot.positive_probability:.2f}/{annot.negative_probability:.2f})"
        g2 = f"{annot.two_class.get('label')}"
        d2 = get_pred_str(e2)
        r3 = get_pred_str(e3)
        out2 = str(get_outcome(e2))

        print(f"{pid:<18} | {ptype:<20} | {g3:<15} | {g2:<15} | {d2:<16} | {r3:<14} | {out2:<16}")
        results_table.append({
            "probe_id": pid,
            "type": ptype,
            "gemini_3class": annot.three_class,
            "gemini_2class": annot.two_class,
            "distilbert_prediction": d2,
            "roberta_prediction": r3,
            "outcome_2class": out2,
            "outcome_3class": str(get_outcome(e3)),
        })

    print("=" * 80)
    with open("scratch/golden_probes_validation_results.json", "w", encoding="utf-8") as f:
        json.dump(results_table, f, indent=2)
    print("Results saved to scratch/golden_probes_validation_results.json")

if __name__ == "__main__":
    main()
