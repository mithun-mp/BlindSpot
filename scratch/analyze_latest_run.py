import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

exp_dir = "runs/exp_1790985879_4bb019"
comp_file = os.path.join(exp_dir, "aggregate", "comparison.json")

if os.path.exists(comp_file):
    data = json.load(open(comp_file, "r", encoding="utf-8"))
    matrix = data.get("model_probe_matrix", [])
    for row in matrix:
        if "prb_52ce79" in row.get("probe_id", "") or True:
            print("=== PROBE ID:", row.get("probe_id"), "===")
            print("PERTURBED TEXT:", row.get("perturbed_text"))
            print("EXPECTED DESC:", row.get("expected_desc"))
            print("EXPECTED FLIP:", row.get("expected_flip"))
            for m_id, m_out in row.get("models", {}).items():
                print(f"  [{m_id}]")
                print(f"    orig: {m_out.get('original_label')} ({m_out.get('original_confidence')})")
                print(f"    pert: {m_out.get('perturbed_label')} ({m_out.get('perturbed_confidence')})")
                print(f"    trans: {m_out.get('transition_type')}")
                print(f"    flip: {m_out.get('is_flipped')}")
                print(f"    sat: {m_out.get('expectation_satisfied')}")
                print(f"    gt: {m_out.get('ground_truth_match')}")
                print(f"    outcome: {m_out.get('behavioral_outcome')}")
                print(f"    fail_type: {m_out.get('failure_type')}")
