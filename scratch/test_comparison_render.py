import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

results = json.load(open("runs/exp_1790977223_6c3ec3/results.json", "r", encoding="utf-8"))
cross = results.get("cross_model_comparison", {})
matrix_data = cross.get("model_probe_matrix", [])
all_known_models = list(results.get("models", {}).keys())

for item in matrix_data:
    p_id = item["probe_id"]
    if "prb_52ce79" not in p_id:
        continue
    sem_ref = item.get("semantic_reference") or {}
    sem_pol = sem_ref.get("final_semantic_polarity", "")
    sem_rel = sem_ref.get("semantic_relation_to_baseline", "")
    exp_flip = item.get("expected_flip", False)

    if sem_pol:
        rel_tag = f" [{sem_rel}]" if sem_rel else ""
        expected_desc = f"{sem_pol}{rel_tag}"
        expected_token = "FLIP" if "REVERSE" in str(sem_rel).upper() else ("PRESERVE" if "PRESERVE" in str(sem_rel).upper() else "CHANGE")
    elif exp_flip:
        expected_token = "FLIP"
    else:
        expected_token = "PRESERVE"

    m_outputs = item.get("models", {})
    for m_id in all_known_models:
        out = m_outputs.get(m_id, {})
        fail_type = out.get("failure_type")
        fail_type_clean = str(fail_type or "").strip().lower()

        is_behavior_match = False
        if fail_type_clean == "misweighted":
            if expected_token == "PRESERVE":
                is_behavior_match = (not out.get("is_flipped", False))
            elif expected_token == "FLIP":
                is_behavior_match = bool(out.get("is_flipped", False)) and out.get("ground_truth_match") is not False
            elif expected_token == "CHANGE":
                is_behavior_match = bool(out.get("is_flipped", False)) and (out.get("ground_truth_match") is True or out.get("expectation_satisfied") is True)

            if not is_behavior_match:
                is_behavior_match = bool(
                    out.get("behavioral_outcome") in ("EXPECTED_PRESERVE", "EXPECTED_FLIP")
                    or out.get("expectation_satisfied", False) is True
                )

            if is_behavior_match:
                status = "misweighted-match"
                pill = "pill-misweighted-match"
            else:
                status = "misweighted"
                pill = "pill-misweighted"

            badge = "✕ MISWEIGHTED"
        elif fail_type_clean == "spurious":
            badge = "✕ SPURIOUS"
        elif fail_type_clean == "blind":
            badge = "✕ BLIND"
        elif fail_type_clean == "undetermined":
            badge = "? UNDETERMINED"
        else:
            status = "match"
            pill = "pill-match"
            badge = "✓ MATCH"

        print(f"Model: {m_id}")
        print(f"  fail_type_clean: {fail_type_clean}")
        print(f"  badge: {badge}")
        print(f"  status: {status}")
        print(f"  pill: {pill}")
        print(f"  is_behavior_match: {is_behavior_match}")
