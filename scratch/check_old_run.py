import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

b_file = "runs/exp_1790953982_26da69/models/cardiffnlp__twitter-roberta-base-sentiment-latest/behavioral.json"
if os.path.exists(b_file):
    data = json.load(open(b_file, "r", encoding="utf-8"))
    for item in data:
        if "prb_52ce79" in item.get("probe_id", ""):
            print("=== exp_1790953982_26da69 behavioral.json for prb_52ce79 ===")
            print("original_label:", item.get("original_label"))
            print("perturbed_label:", item.get("perturbed_label"))
            print("transition_type:", item.get("transition_type"))
            print("is_flipped:", item.get("is_flipped"))
            print("raw_label_flip:", item.get("raw_label_flip"))
            print("polarity_flip:", item.get("polarity_flip"))
            print("expected_relation:", item.get("expected_relation"))
            print("observed_relation:", item.get("observed_relation"))
            print("behavioral_outcome:", item.get("behavioral_outcome"))
            print("failure_type:", item.get("failure_type"))
            print("rationale:", item.get("rationale"))
            print("expectation_satisfied:", item.get("expectation_satisfied"))
            print("ground_truth_match:", item.get("ground_truth_match"))
            print("semantic_reference:", json.dumps(item.get("semantic_reference"), indent=2))
