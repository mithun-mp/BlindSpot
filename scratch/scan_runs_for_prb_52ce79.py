import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

runs_dir = "runs"
matches = []

for r_name in os.listdir(runs_dir):
    r_path = os.path.join(runs_dir, r_name)
    if not os.path.isdir(r_path) or not r_name.startswith("exp_"):
        continue
    comp_file = os.path.join(r_path, "aggregate", "comparison.json")
    if not os.path.exists(comp_file):
        continue
    try:
        data = json.load(open(comp_file, "r", encoding="utf-8"))
        matrix = data.get("model_probe_matrix", [])
        for row in matrix:
            if "prb_52ce79" in row.get("probe_id", ""):
                models = row.get("models", {})
                tw = models.get("cardiffnlp/twitter-roberta-base-sentiment-latest", {})
                if tw:
                    matches.append({
                        "run": r_name,
                        "label": tw.get("perturbed_label"),
                        "sat": tw.get("expectation_satisfied"),
                        "fail": tw.get("failure_type"),
                        "outcome": tw.get("behavioral_outcome"),
                        "gt": tw.get("ground_truth_match"),
                    })
    except Exception as e:
        pass

print(f"Total matching runs checked: {len(matches)}")
for m in sorted(matches, key=lambda x: x["run"]):
    print(f"Run: {m['run']} | label: {m['label']} | sat: {m['sat']} | fail: {m['fail']} | outcome: {m['outcome']} | gt: {m['gt']}")
