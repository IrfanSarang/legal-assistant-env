"""
Grader for Task 1: format-check
Deterministic scoring — compares agent's identified issues against ground truth.

Score breakdown (weights must sum to 1.0):
  - issue_f1     (0.60): F1 score on identified issue types vs ground truth types
  - summary      (0.20): Summary quality (non-empty, meets min length)
  - false_pos    (0.10): Penalty for false positive issue types
  - count_est    (0.10): How close agent's issue count is to ground truth count
"""
from __future__ import annotations

from typing import Any, Dict, List

from app.features.environment.models import Action, Reward
from app.features.tasks.base import f1_score

VALID_ISSUE_TYPES = {
    "page_numbers",
    "text_alignment",
    "font",
    "margins",
    "headings",
    "line_spacing",
}


class FormatCheckGrader:
    """Deterministic grader for the format-check task."""

    ISSUE_F1_WEIGHT = 0.60
    SUMMARY_WEIGHT = 0.20
    FALSE_POS_WEIGHT = 0.10
    COUNT_WEIGHT = 0.10

    def grade(
        self,
        action: Action,
        ground_truth: Dict[str, Any],
        step: int,
        max_steps: int,
    ) -> Reward:
        analysis = action.analysis
        gt_issues = ground_truth.get("issues", [])
        gt_types = {issue["type"] for issue in gt_issues}
        gt_count = ground_truth.get("issue_count", len(gt_issues))

        # Extract agent's reported issue types
        agent_issues = analysis.get("issues", [])
        agent_types = self._extract_issue_types(agent_issues)

        # ── Score 1: F1 on issue types ───────────────────────────────────────
        issue_f1 = f1_score(list(agent_types), list(gt_types))

        # ── Score 2: Summary quality ─────────────────────────────────────────
        summary = analysis.get("summary", "")
        summary_score = self._score_summary(summary)

        # ── Score 3: False positive penalty ──────────────────────────────────
        false_positives = agent_types - gt_types - set(ground_truth.get("compliant", []))
        fp_penalty = min(1.0, len(false_positives) * 0.15)
        fp_score = max(0.0, 1.0 - fp_penalty)

        # ── Score 4: Issue count estimation ──────────────────────────────────
        agent_count = len(agent_issues)
        count_diff = abs(agent_count - gt_count)
        count_score = max(0.0, 1.0 - (count_diff / max(gt_count, 1)) * 0.5)

        # ── Weighted total ────────────────────────────────────────────────────
        total = (
            issue_f1 * self.ISSUE_F1_WEIGHT
            + summary_score * self.SUMMARY_WEIGHT
            + fp_score * self.FALSE_POS_WEIGHT
            + count_score * self.COUNT_WEIGHT
        )
        total = round(max(0.0, min(1.0, total)), 4)

        # ── Done: final step or agent declares done ───────────────────────────
        done = step + 1 >= max_steps

        breakdown = {
            "issue_f1": round(issue_f1, 4),
            "summary": round(summary_score, 4),
            "false_positive_score": round(fp_score, 4),
            "count_accuracy": round(count_score, 4),
        }

        feedback = self._build_feedback(
            agent_types, gt_types, false_positives, issue_f1, summary_score, total,
            ground_truth=ground_truth,
        )

        return Reward(score=total, breakdown=breakdown, feedback=feedback, done=done)

    def _extract_issue_types(self, issues: List[Any]) -> set:
        types = set()
        for issue in issues:
            if isinstance(issue, dict):
                t = issue.get("type", "").lower().strip()
                if t in VALID_ISSUE_TYPES:
                    types.add(t)
            elif isinstance(issue, str):
                t = issue.lower().strip()
                if t in VALID_ISSUE_TYPES:
                    types.add(t)
        return types

    def _score_summary(self, summary: str) -> float:
        if not summary or not summary.strip():
            return 0.0
        length = len(summary.strip())
        if length < 20:
            return 0.3
        if length < 50:
            return 0.6
        return 1.0

    def _build_feedback(
        self,
        agent_types: set,
        gt_types: set,
        false_positives: set,
        issue_f1: float,
        summary_score: float,
        total: float,
        ground_truth: Dict[str, Any] = None,
    ) -> str:
        lines = [f"Format-check score: {total:.3f}"]
        missed = gt_types - agent_types
        hints = (ground_truth or {}).get("hints", {})

        if missed:
            hint_strs = []
            for t in sorted(missed):
                if t in hints:
                    hint_strs.append(f"{t} (hint: {hints[t]})")
                else:
                    hint_strs.append(t)
            lines.append(f"Missed issue types: {', '.join(hint_strs)}")

        if false_positives:
            compliant = set((ground_truth or {}).get("compliant", []))
            fp_with_context = []
            for t in sorted(false_positives):
                if t in compliant:
                    fp_with_context.append(f"{t} (this category is compliant in this document)")
                else:
                    fp_with_context.append(t)
            lines.append(f"False positives (not in this document): {', '.join(fp_with_context)}")

        if issue_f1 == 1.0:
            lines.append("All issue types correctly identified!")
        if summary_score < 0.6:
            lines.append("Summary is too short — write at least 50 characters summarising findings.")

        return " | ".join(lines)