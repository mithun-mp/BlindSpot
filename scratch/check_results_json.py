import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

exp_dir = "runs/exp_1790977223_6c3ec3"
results_file = os.path.join(exp_dir, "results.json")

if os.path.exists(results_file):
    data = json.load(open(results_file, "r", encoding="utf-8"))
    matrix = data.get("cross_model_comparison", {}).get("model_probe_matrix", [])
    print(f"Total rows in results.json matrix: {len(matrix)}")
    for row in matrix:
        if "prb_52ce79" in row.get("probe_id", ""):
            print("=== PROBE ID:", row.get("probe_id"), "===")
            print("EXPECTED DESC:", row.get("expected_desc"))
            for m_id, m_out in row.get("models", {}).items():
                print(f"  [{m_id}]")
                print(f"    pert: {m_out.get('perturbed_label')}")
                print(f"    fail_type: {m_out.get('failure_type')}")
                print(f"    sat: {m_out.get('expectation_satisfied')}")
                print(f"    outcome: {m_out.get('behavioral_outcome')}")
