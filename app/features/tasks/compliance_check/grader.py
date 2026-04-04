"""
Grader for Task 3: compliance-check
Scores against curated Indian law compliance ground truth.

Score breakdown:
  - law_identification  (0.40): Did agent correctly identify the relevant laws?
  - section_citation    (0.30): Are section numbers correct?
  - suggestion_quality  (0.20): Are remediation suggestions reasonable?
  - completeness        (0.10): Did agent find all violations (recall)?
"""
from __future__ import annotations

from typing import Any, Dict, List

from app.features.environment.models import Action, Reward
from app.features.tasks.compliance_check.indian_law_db import resolve_law, is_valid_section

LAW_ID_WEIGHT = 0.40
SECTION_WEIGHT = 0.30
SUGGESTION_WEIGHT = 0.20
COMPLETENESS_WEIGHT = 0.10


class ComplianceCheckGrader:
    """Deterministic grader for the compliance-check task."""

    def grade(
        self,
        action: Action,
        ground_truth: Dict[str, Any],
        step: int,
        max_steps: int,
    ) -> Reward:
        analysis = action.analysis
        gt_violations = ground_truth.get("violations", [])
        agent_violations = analysis.get("violations", [])

        # ── Score 1: Law identification ───────────────────────────────────────
        law_score = self._score_law_identification(agent_violations, gt_violations)

        # ── Score 2: Section citation accuracy ───────────────────────────────
        section_score = self._score_section_citations(agent_violations, gt_violations)

        # ── Score 3: Suggestion quality ───────────────────────────────────────
        suggestion_score = self._score_suggestions(agent_violations, gt_violations)

        # ── Score 4: Completeness (recall of violations) ───────────────────────
        completeness_score = self._score_completeness(agent_violations, gt_violations)

        total = (
            law_score * LAW_ID_WEIGHT
            + section_score * SECTION_WEIGHT
            + suggestion_score * SUGGESTION_WEIGHT
            + completeness_score * COMPLETENESS_WEIGHT
        )
        total = round(max(0.0, min(1.0, total)), 4)

        done = step + 1 >= max_steps

        breakdown = {
            "law_identification": round(law_score, 4),
            "section_citations": round(section_score, 4),
            "suggestion_quality": round(suggestion_score, 4),
            "completeness": round(completeness_score, 4),
        }

        feedback = self._build_feedback(
            breakdown, total, len(gt_violations), len(agent_violations),
            gt_violations=gt_violations,
            agent_violations=agent_violations,
            ground_truth=ground_truth,
        )

        return Reward(score=total, breakdown=breakdown, feedback=feedback, done=done)

    def _score_law_identification(self, agent_violations: List[Any], gt_violations: List[Dict]) -> float:
        if not gt_violations:
            return 1.0
        if not agent_violations:
            return 0.0

        gt_laws = {resolve_law(v.get("law", "")) for v in gt_violations if resolve_law(v.get("law", ""))}

        agent_laws = set()
        for v in agent_violations:
            if isinstance(v, dict):
                resolved = resolve_law(v.get("law", ""))
                if resolved:
                    agent_laws.add(resolved)

        if not gt_laws:
            return 0.5

        intersection = len(gt_laws & agent_laws)
        precision = intersection / len(agent_laws) if agent_laws else 0.0
        recall = intersection / len(gt_laws)

        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)

    def _score_section_citations(self, agent_violations: List[Any], gt_violations: List[Dict]) -> float:
        if not gt_violations:
            return 1.0

        gt_pairs = set()
        for v in gt_violations:
            law = resolve_law(v.get("law", ""))
            if law:
                gt_pairs.add((law, str(v.get("section", "")).strip()))

        if not gt_pairs:
            return 0.5

        agent_correct = 0
        agent_total = 0
        for v in agent_violations:
            if not isinstance(v, dict):
                continue
            law = resolve_law(v.get("law", ""))
            section = str(v.get("section", "")).strip()
            if law and section:
                agent_total += 1
                if (law, section) in gt_pairs:
                    agent_correct += 1

        if agent_total == 0:
            return 0.0

        precision = agent_correct / agent_total
        recall = agent_correct / len(gt_pairs) if gt_pairs else 0.0

        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)

    def _score_suggestions(self, agent_violations: List[Any], gt_violations: List[Dict]) -> float:
        if not agent_violations:
            return 0.0

        valid_suggestions = 0
        for v in agent_violations:
            if not isinstance(v, dict):
                continue
            suggestion = v.get("suggestion", "")
            if suggestion and len(suggestion.strip()) >= 20:
                valid_suggestions += 1

        score = valid_suggestions / max(len(gt_violations), 1)
        return min(1.0, score)

    def _score_completeness(self, agent_violations: List[Any], gt_violations: List[Dict]) -> float:
        if not gt_violations:
            return 1.0
        if not agent_violations:
            return 0.0

        gt_laws = [resolve_law(v.get("law", "")) for v in gt_violations]
        gt_laws = [l for l in gt_laws if l]

        agent_laws = []
        for v in agent_violations:
            if isinstance(v, dict):
                resolved = resolve_law(v.get("law", ""))
                if resolved:
                    agent_laws.append(resolved)

        found = sum(1 for gl in gt_laws if gl in agent_laws)
        return found / len(gt_laws) if gt_laws else 0.0

    def _build_feedback(
        self,
        breakdown: Dict,
        total: float,
        gt_count: int,
        agent_count: int,
        gt_violations: List[Dict] = None,
        agent_violations: List[Any] = None,
        ground_truth: Dict[str, Any] = None,
    ) -> str:
        parts = [f"Compliance-check score: {total:.3f}"]
        hints = (ground_truth or {}).get("hints", {})

        if breakdown["law_identification"] < 0.5:
            laws_hint = hints.get("laws_to_check", "")
            if laws_hint:
                parts.append(f"Law identification weak — hint: {laws_hint}")
            else:
                parts.append("Law identification is weak — cite specific Indian laws (ICA 1872, DPDP 2023, CPA 2019, ACA 1996)")

        if breakdown["section_citations"] < 0.4:
            # Show which law+section pairs were missed
            if gt_violations and agent_violations is not None:
                from app.features.tasks.compliance_check.indian_law_db import resolve_law
                agent_pairs = set()
                for v in agent_violations:
                    if isinstance(v, dict):
                        law = resolve_law(v.get("law", ""))
                        sec = str(v.get("section", "")).strip()
                        if law and sec:
                            agent_pairs.add((law, sec))
                missed_pairs = []
                for v in (gt_violations or []):
                    law = resolve_law(v.get("law", ""))
                    sec = str(v.get("section", "")).strip()
                    if law and sec and (law, sec) not in agent_pairs:
                        missed_pairs.append(f"{law} S.{sec}")
                if missed_pairs:
                    parts.append(f"Missing section citations: {', '.join(missed_pairs[:4])}")
                else:
                    parts.append("Section citations need improvement — cite specific section numbers")
            else:
                parts.append("Section citations need improvement — cite specific section numbers")

        if breakdown["suggestion_quality"] < 0.5:
            parts.append("Improve remediation suggestions — each violation needs a specific compliant alternative (min 20 chars)")

        if breakdown["completeness"] < 0.5:
            parts.append(f"Incomplete — found {agent_count} violations, expected ~{gt_count}")
            # Give clause-level hints for missed violations
            if gt_violations and agent_violations is not None:
                from app.features.tasks.compliance_check.indian_law_db import resolve_law
                agent_laws_found = {resolve_law(v.get("law", "")) for v in agent_violations if isinstance(v, dict)}
                for v in (gt_violations or []):
                    law = resolve_law(v.get("law", ""))
                    if law and law not in agent_laws_found:
                        clause_key = v.get("clause", "").split("—")[0].strip().lower().replace(" ", "_")
                        clause_hint = hints.get(clause_key, "")
                        if clause_hint:
                            parts.append(f"Missed: {v.get('clause', '')} — hint: {clause_hint}")
                        break  # one hint at a time to avoid overwhelming

        if total >= 0.7:
            parts.append("Good compliance analysis!")

        return " | ".join(parts)