"""
Audit Compiler: Consolidates experiment metadata, model baselines, primary research metrics,
failure taxonomy diagnoses, cross-model concordance, and probe-level evidence into a unified,
data-driven audit report structure.

Supports dynamic factual data extraction and pure-text Markdown generation (excluding image syntax).
"""
import os
import json
import re
from typing import Dict, Any, List, Optional


FIGURE_DEFINITIONS = {
    "fig04": {
        "filename": "fig04_taxonomy_distribution.png",
        "title": "Figure 1: Failure Taxonomy Breakdown by Model",
        "category": "Behavioral Failure Taxonomy",
        "what_it_is": "Grouped bar chart displaying the count of diagnosed behavioral failure modes (Blind, Spurious, Misweighted, and Undetermined) across evaluated models.",
        "why_it_matters": "Distinguishes between attention blindness (ignoring operators) and feature misweighting (opposing tokens overpowering operators), guiding targeted architectural and data remediation.",
    },
    "fig12": {
        "filename": "fig12_change_vs_preserve.png",
        "title": "Figure 2: Stratified Sensitivity vs Invariance Fidelity",
        "category": "Sensitivity & Invariance",
        "what_it_is": "Dual-metric grouped bar chart contrasting Sensitivity (success rate in flipping on meaning-altering probes, in orange) against Invariance (success rate in preserving on meaning-preserving probes, in green).",
        "why_it_matters": "Separates responsive sensitivity to genuine semantic reversals from passive inertia under superficial or invariant linguistic modifications.",
    },
    "fig05": {
        "filename": "fig05_confidence_delta_by_probe.png",
        "title": "Figure 3: Mean Signed Confidence Shift by Probe",
        "category": "Confidence Dynamics",
        "what_it_is": "Horizontal divergence bar chart measuring the mean signed change in prediction confidence in percentage points (Δ Conf = p_pert - p_orig) for evaluated probes.",
        "why_it_matters": "Exposes sub-threshold prediction degradation where confidence significantly erodes under invariant edits or fails to attenuate under mitigating operators.",
    },
    "fig08": {
        "filename": "fig08_model_probe_heatmap.png",
        "title": "Figure 4: Model Probe Flip Matrix",
        "category": "Cross-Model Concordance",
        "what_it_is": "2D heatmap matrix (Probes on horizontal axis, Models on vertical axis) displaying discrete prediction stability: Red indicates a prediction label flip (FLIP); Green indicates prediction stability (SAME).",
        "why_it_matters": "Visualizes cross-architecture concordance, isolating systemic failure modes shared across model families from isolated single-model anomalies.",
    },
    "fig07": {
        "filename": "fig07_probe_level_comparison.png",
        "title": "Figure 5: Probe-Level Confidence Response Across Models",
        "category": "Probe Analysis",
        "what_it_is": "Grouped bar chart displaying the perturbed prediction confidence percentage across all models for evaluated diagnostic probes.",
        "why_it_matters": "Provides probe-by-probe comparative resolution, identifying specific linguistic triggers that elicit architecture-specific confidence collapse or stability.",
    },
    "fig10": {
        "filename": "fig10_probe_consistency.png",
        "title": "Figure 6: Behavioral Semantic Consistency Score by Model",
        "category": "Behavioral Consistency",
        "what_it_is": "Bar chart illustrating the overall Behavioral Consistency percentage achieved by each evaluated model, measuring strict compliance with expected semantic effects.",
        "why_it_matters": "Quantifies the proportion of probes where observed transitions obeyed the semantic contract (flipping when polarity is inverted, preserving when invariant).",
    },
    "fig13": {
        "filename": "fig13_per_model_scorecard.png",
        "title": "Figure 7: Per-Model Multi-Metric Executive Scorecard",
        "category": "Scorecards & Profiling",
        "what_it_is": "Three-panel comparative scorecard presenting Prediction Flip Rate (%), Behavioral Consistency (%), and Expected Calibration Error (ECE %) across models.",
        "why_it_matters": "Provides a tripartite summary of operational robustness, semantic compliance, and probabilistic calibration across all evaluated architectures.",
    },
}


class UnifiedAuditData:
    """Encapsulates structured data compiled from an experiment run directory."""
    def __init__(self, exp_dir: str):
        self.exp_dir = exp_dir
        self.exp_id = os.path.basename(exp_dir)
        self.figures_dir = os.path.join(exp_dir, "figures")
        self.reports_dir = os.path.join(exp_dir, "reports")
        
        self.metadata: Dict[str, Any] = self._load_json("metadata.json")
        self.config: Dict[str, Any] = self._load_json("config.json")
        self.source_data: Dict[str, Any] = self._load_json(os.path.join("figures", "source_data.json"))
        self.results: Dict[str, Any] = self._load_json("results.json")
        
        # Load markdown report texts if present
        self.exp_summary_md = self._load_text(os.path.join("reports", "experiment_summary.md"))
        self.failure_summary_md = self._load_text(os.path.join("reports", "failure_summary.md"))
        self.probe_evidence_md = self._load_text(os.path.join("reports", "probe_level_evidence.md"))
        
        # Parse extracted tables and items
        self.models: List[str] = self._resolve_models()
        self.seed_sentences: List[str] = self._extract_seeds()
        self.baselines_table: List[Dict[str, Any]] = self._parse_baselines_table()
        self.metrics_table: List[Dict[str, Any]] = self._parse_metrics_table()
        self.taxonomy_table: List[Dict[str, Any]] = self._parse_taxonomy_table()
        self.pairwise_matrix: Dict[str, Any] = self._parse_pairwise_matrix()
        self.failures_list: List[Dict[str, Any]] = self._parse_failures()
        self.probe_evidence_rows: List[Dict[str, Any]] = self._parse_probe_evidence()

        # Dynamic figure observations
        self.figure_observations: Dict[str, str] = self._build_figure_observations()

    def _load_json(self, rel_path: str) -> Dict[str, Any]:
        full_path = os.path.join(self.exp_dir, rel_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _load_text(self, rel_path: str) -> str:
        full_path = os.path.join(self.exp_dir, rel_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                return ""
        return ""

    def _resolve_models(self) -> List[str]:
        if self.source_data.get("models"):
            return list(self.source_data["models"])
        if self.metadata.get("models"):
            return list(self.metadata["models"])
        models_dir = os.path.join(self.exp_dir, "models")
        if os.path.exists(models_dir):
            return sorted(os.listdir(models_dir))
        return []

    def _to_full_model(self, name: str) -> str:
        if not name:
            return ""
        clean = name.strip("`").strip()
        for m in self.models:
            if m == clean or m.endswith("/" + clean) or clean == m.split("/")[-1]:
                return m
        return clean

    def _extract_seeds(self) -> List[str]:
        seeds = []
        if self.exp_summary_md:
            for line in self.exp_summary_md.splitlines():
                if line.startswith("- **Seed #"):
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        seeds.append(parts[1].strip().strip('"'))
        if not seeds and self.metadata.get("seeds"):
            seeds = self.metadata["seeds"]
        return seeds

    def _parse_baselines_table(self) -> List[Dict[str, Any]]:
        rows = []
        if not self.exp_summary_md:
            return rows
        lines = self.exp_summary_md.splitlines()
        in_table = False
        for line in lines:
            if "Original Sentence Baselines" in line:
                in_table = True
                continue
            if in_table and line.startswith("## "):
                break
            if in_table and line.startswith("| `"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 5:
                    rows.append({
                        "model": self._to_full_model(parts[0]),
                        "prediction": parts[3].replace("**", ""),
                        "confidence": parts[4],
                    })
                elif len(parts) == 4:
                    rows.append({
                        "model": self._to_full_model(parts[0]),
                        "prediction": parts[2].replace("**", ""),
                        "confidence": parts[3],
                    })
                elif len(parts) == 3:
                    rows.append({
                        "model": self._to_full_model(parts[0]),
                        "prediction": parts[1].replace("**", ""),
                        "confidence": parts[2],
                    })
        return rows

    def _parse_metrics_table(self) -> List[Dict[str, Any]]:
        rows = []
        # Priority 1: From results.json with full evaluations and behavioral metrics
        if self.results and self.results.get("models"):
            for m_id, m_data in self.results["models"].items():
                evals = m_data.get("evaluations", [])
                m_metrics = m_data.get("behavioral_metrics", {}) or m_data.get("metrics", {})
                tot = m_metrics.get("total_probes", len(evals))

                obs_flips = sum(1 for e in evals if e.get("is_flipped"))
                obs_flip_r = m_metrics.get("observed_flip_rate", obs_flips / max(1, tot) if tot > 0 else 0.0)

                exp_flips_tot = sum(1 for e in evals if e.get("expected_flip"))
                corr_exp_flips = sum(1 for e in evals if e.get("expected_flip") and e.get("is_flipped"))
                exp_comp = m_metrics.get("expected_flip_compliance")
                if exp_comp is None:
                    exp_comp = corr_exp_flips / max(1, exp_flips_tot) if exp_flips_tot > 0 else 1.0

                pres_tot = sum(1 for e in evals if not e.get("expected_flip"))
                corr_pres = sum(1 for e in evals if (not e.get("expected_flip")) and (not e.get("is_flipped")))
                pres_r = m_metrics.get("preserve_rate")
                if pres_r is None:
                    pres_r = corr_pres / max(1, pres_tot) if pres_tot > 0 else 1.0

                consistency = m_metrics.get("behavioral_consistency")
                corr_cons = sum(1 for e in evals if e.get("expectation_satisfied", e.get("expectation_match", False)))
                if consistency is None:
                    consistency = corr_cons / max(1, tot) if tot > 0 else 1.0

                suite_share_r = m_metrics.get("suite_expected_flip_rate", m_metrics.get("expected_flip_rate", exp_flips_tot / max(1, tot) if tot > 0 else 0.0))
                ece = m_metrics.get("ece", 0.0)
                mean_delta = m_metrics.get("confidence_shifts", {}).get("mean_delta_pts", 0.0)

                obs_str = f"{obs_flips}/{tot} ({obs_flip_r*100:.1f}%)" if tot > 0 else f"{obs_flips} ({obs_flip_r*100:.1f}%)"
                comp_str = f"{corr_exp_flips}/{exp_flips_tot} ({exp_comp*100:.1f}%)" if exp_flips_tot > 0 else "N/A"
                suite_str = f"{exp_flips_tot}/{tot} ({suite_share_r*100:.1f}%)" if tot > 0 else f"{suite_share_r*100:.1f}%"
                pres_str = f"{corr_pres}/{pres_tot} ({pres_r*100:.1f}%)" if pres_tot > 0 else "N/A"
                cons_str = f"{corr_cons}/{tot} ({consistency*100:.1f}%)" if tot > 0 else f"{consistency*100:.1f}%"

                rows.append({
                    "model": self._to_full_model(m_id),
                    "probes": tot,
                    "observed_flips": obs_str,
                    "expected_flip_compliance": comp_str,
                    "expected_flips": comp_str,  # Backward compatibility alias
                    "suite_expected_flip_share": suite_str,
                    "preserve_rate": pres_str,
                    "consistency": cons_str,
                    "ece": f"{ece:.4f}" if isinstance(ece, float) else str(ece),
                    "mean_delta": f"{mean_delta:+.1f} pp" if isinstance(mean_delta, (int, float)) else str(mean_delta),
                })
            return rows

        # Priority 2: From source_data.json summary_metrics if available
        summary_metrics = self.source_data.get("summary_metrics", {})
        if summary_metrics:
            for m_id, m_dict in summary_metrics.items():
                tot = m_dict.get("total_probes", 0)
                obs_r = m_dict.get("observed_flip_rate", 0.0)
                obs_flips = round(obs_r * tot)

                suite_share_r = m_dict.get("suite_expected_flip_rate", m_dict.get("expected_flip_rate", 0.0))
                exp_flips_tot = round(suite_share_r * tot)

                exp_comp = m_dict.get("expected_flip_compliance")
                if exp_comp is not None:
                    corr_exp_flips = round(exp_comp * exp_flips_tot)
                    comp_str = f"{corr_exp_flips}/{exp_flips_tot} ({exp_comp*100:.1f}%)" if exp_flips_tot > 0 else f"{exp_comp*100:.1f}%"
                else:
                    comp_str = "N/A"

                pres_tot = tot - exp_flips_tot
                pres_r = m_dict.get("preserve_rate", 0.0)
                corr_pres = round(pres_r * pres_tot)

                cons_r = m_dict.get("behavioral_consistency", 0.0)
                corr_cons = round(cons_r * tot)

                ece = m_dict.get("ece", 0.0)
                mean_delta = m_dict.get("confidence_shifts", {}).get("mean_delta_pts", 0.0)

                obs_str = f"{obs_flips}/{tot} ({obs_r*100:.1f}%)" if tot > 0 else f"{obs_flips} ({obs_r*100:.1f}%)"
                suite_str = f"{exp_flips_tot}/{tot} ({suite_share_r*100:.1f}%)" if tot > 0 else f"{suite_share_r*100:.1f}%"
                pres_str = f"{corr_pres}/{pres_tot} ({pres_r*100:.1f}%)" if pres_tot > 0 else f"{pres_r*100:.1f}%"
                cons_str = f"{corr_cons}/{tot} ({cons_r*100:.1f}%)" if tot > 0 else f"{cons_r*100:.1f}%"

                rows.append({
                    "model": self._to_full_model(m_id),
                    "probes": tot,
                    "observed_flips": obs_str,
                    "expected_flip_compliance": comp_str,
                    "expected_flips": comp_str,  # Backward compatibility alias
                    "suite_expected_flip_share": suite_str,
                    "preserve_rate": pres_str,
                    "consistency": cons_str,
                    "ece": f"{ece:.4f}" if isinstance(ece, float) else str(ece),
                    "mean_delta": f"{mean_delta:+.1f} pp" if isinstance(mean_delta, (int, float)) else str(mean_delta),
                })
            return rows

        # Fallback parse from experiment_summary.md
        if self.exp_summary_md:
            lines = self.exp_summary_md.splitlines()
            in_table = False
            for line in lines:
                if "Primary Research Metrics" in line:
                    in_table = True
                    continue
                if in_table and line.startswith("## "):
                    break
                if in_table and line.startswith("| `"):
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 8:
                        rows.append({
                            "model": self._to_full_model(parts[0]),
                            "probes": parts[1],
                            "observed_flips": parts[2],
                            "expected_flip_compliance": parts[3],
                            "expected_flips": parts[3],
                            "suite_expected_flip_share": "N/A",
                            "preserve_rate": parts[4],
                            "consistency": parts[5],
                            "ece": parts[6],
                            "mean_delta": parts[7],
                        })
        return rows

    def _parse_taxonomy_table(self) -> List[Dict[str, Any]]:
        rows = []
        if self.exp_summary_md:
            lines = self.exp_summary_md.splitlines()
            in_table = False
            for line in lines:
                if "Behavioral Failure Taxonomy Counts" in line:
                    in_table = True
                    continue
                if in_table and line.startswith("## "):
                    break
                if in_table and line.startswith("| `"):
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 6:
                        rows.append({
                            "model": self._to_full_model(parts[0]),
                            "blind": int(parts[1]) if parts[1].isdigit() else parts[1],
                            "spurious": int(parts[2]) if parts[2].isdigit() else parts[2],
                            "misweighted": int(parts[3]) if parts[3].isdigit() else parts[3],
                            "undetermined": int(parts[4]) if parts[4].isdigit() else parts[4],
                            "compliant": int(parts[5]) if parts[5].isdigit() else parts[5],
                        })
        return rows

    def _parse_pairwise_matrix(self) -> Dict[str, Any]:
        result = {"models": [], "matrix": []}
        if not self.exp_summary_md:
            return result
        lines = self.exp_summary_md.splitlines()
        in_table = False
        for line in lines:
            if "Pairwise Concordance Matrix" in line:
                in_table = True
                continue
            if in_table and line.startswith("## "):
                break
            if in_table and line.startswith("| Model |"):
                headers = [self._to_full_model(p.strip().replace("`", "")) for p in line.split("|")[2:-1]]
                result["models"] = headers
            elif in_table and line.startswith("| `"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) > 1:
                    row_model = self._to_full_model(parts[0])
                    row_vals = parts[1:]
                    result["matrix"].append({"model": row_model, "values": row_vals})
        return result

    def _parse_failures(self) -> List[Dict[str, Any]]:
        failures = []
        if not self.failure_summary_md:
            return failures

        blocks = self.failure_summary_md.split("### Failure #")
        for b in blocks[1:]:
            lines = b.strip().splitlines()
            header = lines[0]
            # Format: 1: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
            fail_type = "Misweighted" if "[MISWEIGHTED]" in header else ("Blind" if "[BLIND]" in header else "Spurious")
            model_match = re.search(r"Model `([^`]+)`", header)
            model_name = self._to_full_model(model_match.group(1)) if model_match else ""

            item: Dict[str, Any] = {"category": fail_type, "model": model_name}
            for l in lines[1:]:
                l_str = l.strip()
                if l_str.startswith("- **Probe ID**:"):
                    item["probe_id"] = l_str.split(":", 1)[1].strip()
                elif l_str.startswith("- **Original Input**:"):
                    item["original"] = l_str.split(":", 1)[1].strip().strip('"')
                elif l_str.startswith("- **Perturbed Input**:"):
                    item["perturbed"] = l_str.split(":", 1)[1].strip().strip('"')
                elif l_str.startswith("- **Observed Transition**:"):
                    item["transition"] = l_str.split(":", 1)[1].strip()
                elif l_str.startswith("- **Prediction Flipped**:"):
                    item["flipped"] = l_str.split(":", 1)[1].strip()
                elif l_str.startswith("- **Diagnostic Reason**:"):
                    item["reason"] = l_str.split(":", 1)[1].strip()
                elif l_str.startswith("- **Evidence**:"):
                    item["evidence"] = l_str.split(":", 1)[1].strip()
                elif l_str.startswith("- **Actionable Recommendation**:"):
                    item["recommendation"] = l_str.split(":", 1)[1].strip()
            failures.append(item)
        return failures

    def _parse_probe_evidence(self) -> List[Dict[str, Any]]:
        rows = []
        if not self.probe_evidence_md:
            return rows

        current_model = ""
        for line in self.probe_evidence_md.splitlines():
            if line.startswith("## Model: `"):
                current_model = self._to_full_model(line.split("`")[1])
            elif line.startswith("| `prb_"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 11:
                    outcome_str = parts[9].strip("`")
                    fail_str = parts[10].replace("**", "")
                    is_pass = ("EXPECTED" in outcome_str.upper() and fail_str.lower() in ("none", "", "compliant"))
                    status_str = "✓ PASS" if is_pass else "✕ FAIL"
                    rows.append({
                        "model": current_model,
                        "probe_id": parts[0].strip("`"),
                        "category": parts[1],
                        "transition": parts[6],
                        "delta_conf": parts[7],
                        "flip": parts[8],
                        "outcome": outcome_str,
                        "failure": fail_str,
                        "status": status_str,
                    })
        return rows

    def _build_figure_observations(self) -> Dict[str, str]:
        """Dynamically computes factual observations for each of the 7 figures from actual run data."""
        obs = {}
        
        # Fig 4: Taxonomy
        total_failures = len(self.failures_list)
        blind_c = sum(1 for f in self.failures_list if str(f.get("category", "")).lower() == "blind")
        spurious_c = sum(1 for f in self.failures_list if str(f.get("category", "")).lower() == "spurious")
        misweighted_c = sum(1 for f in self.failures_list if str(f.get("category", "")).lower() == "misweighted")
        models_with_failures = sorted(list({f["model"] for f in self.failures_list if "model" in f}))
        models_str = ", ".join(models_with_failures) if models_with_failures else "none"
        
        obs["fig04"] = (
            f"Across {len(self.models)} evaluated models, a total of {total_failures} behavioral failure(s) were diagnosed: "
            f"{blind_c} Blind, {spurious_c} Spurious, and {misweighted_c} Misweighted. "
            f"Failures were observed in: {models_str}."
        )

        # Fig 5: Confidence Shifts
        summary_m = self.source_data.get("summary_metrics", {})
        all_mean_deltas = [m.get("confidence_shifts", {}).get("mean_delta_pts", 0.0) for m in summary_m.values() if "confidence_shifts" in m]
        if all_mean_deltas:
            avg_shift = sum(all_mean_deltas) / len(all_mean_deltas)
            min_shift = min(all_mean_deltas)
            max_shift = max(all_mean_deltas)
            obs["fig05"] = (
                f"Mean signed confidence shift across evaluated model architectures spans from {min_shift:+.1f} pp to {max_shift:+.1f} pp "
                f"(aggregate mean: {avg_shift:+.1f} pp). Directional shifts reflect probe category impacts on model certainty."
            )
        else:
            obs["fig05"] = "Signed confidence shifts quantify the degree to which linguistic operators attenuate or reinforce model prediction confidence."

        # Fig 7: Probe-Level Comparison
        total_probes = len(self.probe_evidence_rows) // max(1, len(self.models))
        obs["fig07"] = (
            f"Evaluates {total_probes} diagnostic probe instances side-by-side across architectures, revealing "
            f"variations in perturbed confidence levels and identifying linguistic triggers that cause divergent responses."
        )

        # Fig 8: Flip Matrix
        obs["fig08"] = (
            f"Cross-model stability matrix mapping prediction flips across all evaluated probes. "
            f"Highlights shared flips versus isolated architecture-specific label transitions."
        )

        # Fig 10: Consistency
        consistencies = [m.get("behavioral_consistency", 0.0) * 100 for m in summary_m.values()]
        if consistencies:
            min_c = min(consistencies)
            max_c = max(consistencies)
            avg_c = sum(consistencies) / len(consistencies)
            obs["fig10"] = (
                f"Behavioral consistency across models ranges from {min_c:.1f}% to {max_c:.1f}% (cohort mean: {avg_c:.1f}%). "
                f"Consistency measures empirical alignment between observed transitions and expected semantic effects."
            )
        else:
            obs["fig10"] = "Behavioral consistency scores summarize the proportion of probe tests satisfying semantic contract specifications."

        # Fig 12: Sensitivity vs Invariance
        sens_vals = [m.get("expected_flip_compliance", 0.0) * 100 for m in summary_m.values()]
        pres_vals = [m.get("preserve_rate", 0.0) * 100 for m in summary_m.values()]
        if sens_vals and pres_vals:
            avg_sens = sum(sens_vals) / len(sens_vals)
            avg_pres = sum(pres_vals) / len(pres_vals)
            obs["fig12"] = (
                f"Cohort sensitivity (flip compliance on meaning-altering probes) averaged {avg_sens:.1f}%, while "
                f"invariance fidelity (preservation rate on meaning-preserving probes) averaged {avg_pres:.1f}%."
            )
        else:
            obs["fig12"] = "Contrasts flip rates under polarity inversion against prediction retention rates under meaning-preserving edits."

        # Fig 13: Summary Scorecard
        eces = [m.get("ece", 0.0) for m in summary_m.values()]
        if eces:
            min_ece = min(eces)
            max_ece = max(eces)
            obs["fig13"] = (
                f"Executive multi-metric panel comparing flip rate, consistency score, and Expected Calibration Error "
                f"(ECE ranges from {min_ece:.4f} to {max_ece:.4f})."
            )
        else:
            obs["fig13"] = "Tripartite summary of operational flip rate, behavioral consistency, and calibration error across all models."

        return obs

    def build_clean_markdown(self) -> str:
        """
        Generates a complete, publication-grade Markdown audit document.
        STRICTLY EXCLUDES all image syntax (![...](...)) and image links.
        Contains only pure text, Markdown tables, and structured analytical sections.
        """
        lines = []
        lines.append(f"# BlindSpot Comprehensive Audit Report: {self.metadata.get('experiment_title', self.exp_id)}")
        lines.append("")
        lines.append("## 1. Executive Summary & Configuration")
        lines.append(f"- **Experiment ID**: `{self.exp_id}`")
        lines.append(f"- **Created Timestamp**: `{self.metadata.get('created_at', 'N/A')}`")
        lines.append(f"- **Pipeline Integrity Status**: `{self.metadata.get('pipeline_status', 'PASS')}`")
        lines.append(f"- **Total Target Models Evaluated**: {len(self.models)}")
        total_p = self.source_data.get("pipeline_integrity", {}).get("total_probes", len(self.probe_evidence_rows) // max(1, len(self.models)))
        lines.append(f"- **Evaluated Probes per Model**: {total_p}")
        lines.append(f"- **Total Diagnosed Failures**: {len(self.failures_list)}")
        lines.append("")

        if self.seed_sentences:
            lines.append("### Baseline Seed Sentences")
            for idx, s in enumerate(self.seed_sentences, 1):
                lines.append(f"- **Seed #{idx}**: \"{s}\"")
            lines.append("")

        if self.baselines_table:
            lines.append("## 2. Model Baseline Predictions")
            lines.append("| Model | Baseline Prediction | Confidence |")
            lines.append("| :--- | :---: | :---: |")
            for r in self.baselines_table:
                lines.append(f"| `{r['model']}` | **{r['prediction']}** | {r['confidence']} |")
            lines.append("")

        if self.metrics_table:
            lines.append("## 3. Primary Research Metrics & Calibration")
            suite_share_val = self.metrics_table[0].get("suite_expected_flip_share") if self.metrics_table else None
            if suite_share_val and suite_share_val != "N/A":
                lines.append(f"*- **Suite Expected-Flip Share**: {suite_share_val} (Proportion of test suite designed to elicit polarity reversal — suite property)*\n")
            lines.append("| Model | Probes | Observed Flips | Expected-Flip Compliance | Preserve Rate | Consistency | ECE | Mean Δ Conf |")
            lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
            for r in self.metrics_table:
                comp_val = r.get("expected_flip_compliance", r.get("expected_flips", "N/A"))
                lines.append(f"| `{r['model']}` | {r['probes']} | {r['observed_flips']} | {comp_val} | {r['preserve_rate']} | {r['consistency']} | {r['ece']} | {r['mean_delta']} |")
            lines.append("")

        if self.taxonomy_table:
            lines.append("## 4. Behavioral Failure Taxonomy Distribution")
            lines.append(f"*{self.figure_observations.get('fig04', '')}*")
            lines.append("")
            lines.append("| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |")
            lines.append("| :--- | :---: | :---: | :---: | :---: | :---: |")
            for r in self.taxonomy_table:
                lines.append(f"| `{r['model']}` | {r['blind']} | {r['spurious']} | {r['misweighted']} | {r['undetermined']} | {r['compliant']} |")
            lines.append("")

        lines.append("## 5. Sensitivity, Invariance, and Confidence Dynamics")
        lines.append(f"- **Stratified Sensitivity vs Invariance**: {self.figure_observations.get('fig12', '')}")
        lines.append(f"- **Confidence Shift Profile**: {self.figure_observations.get('fig05', '')}")
        lines.append("")

        lines.append("## 6. Cross-Model Concordance Analysis")
        lines.append(f"- **Stability & Flip Matrix Analysis**: {self.figure_observations.get('fig08', '')}")
        lines.append(f"- **Probe-Level Cross-Model Response**: {self.figure_observations.get('fig07', '')}")
        lines.append("")

        if self.pairwise_matrix.get("models") and self.pairwise_matrix.get("matrix"):
            lines.append("### Pairwise Model Agreement Matrix")
            header_str = "| Model | " + " | ".join([f"`{m}`" for m in self.pairwise_matrix["models"]]) + " |"
            sep_str = "| :--- | " + " | ".join([":---:" for _ in self.pairwise_matrix["models"]]) + " |"
            lines.append(header_str)
            lines.append(sep_str)
            for row in self.pairwise_matrix["matrix"]:
                row_str = f"| `{row['model']}` | " + " | ".join(row["values"]) + " |"
                lines.append(row_str)
            lines.append("")

        lines.append("## 7. Behavioral Consistency & Executive Scorecards")
        lines.append(f"- **Consistency Findings**: {self.figure_observations.get('fig10', '')}")
        lines.append(f"- **Multi-Metric Scorecard Findings**: {self.figure_observations.get('fig13', '')}")
        lines.append("")

        if self.failures_list:
            lines.append("## 8. Itemized Behavioral Failure Diagnoses")
            for idx, f in enumerate(self.failures_list, 1):
                lines.append(f"### Failure #{idx}: [{f.get('category', 'UNKNOWN').upper()}] — Model `{f.get('model', '')}`")
                lines.append(f"- **Probe ID**: `{f.get('probe_id', 'N/A')}`")
                if "original" in f:
                    lines.append(f"- **Original Input**: \"{f['original']}\"")
                if "perturbed" in f:
                    lines.append(f"- **Perturbed Input**: \"{f['perturbed']}\"")
                if "transition" in f:
                    lines.append(f"- **Observed Transition**: {f['transition']}")
                if "reason" in f:
                    lines.append(f"- **Diagnostic Reason**: {f['reason']}")
                if "evidence" in f:
                    lines.append(f"- **Attribution Evidence**: {f['evidence']}")
                if "recommendation" in f:
                    lines.append(f"- **Remediation Recommendation**: {f['recommendation']}")
                lines.append("")

        if self.probe_evidence_rows:
            lines.append("## 9. Granular Probe-Level Evidence Matrix")
            lines.append("| Model | Probe ID | Category | Transition | Δ Conf (pp) | Flip | Outcome | Failure Mode |")
            lines.append("| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |")
            for row in self.probe_evidence_rows:
                lines.append(f"| `{row['model']}` | `{row['probe_id']}` | {row['category']} | {row['transition']} | {row['delta_conf']} | {row['flip']} | `{row['outcome']}` | **{row['failure']}** |")
            lines.append("")

        return "\n".join(lines)
