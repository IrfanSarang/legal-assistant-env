"""
Grader for Task 2: content-review
Scores PII extraction (precision/recall) and error detection coverage.

Score breakdown:
  - pii_names     (0.15): F1 for extracted names
  - pii_emails    (0.10): F1 for emails (exact match)
  - pii_phones    (0.10): F1 for phone numbers
  - pii_addresses (0.08): Partial-match score for addresses
  - pii_companies (0.07): F1 for company names
  - pii_shops     (0.05): F1 for shop names
  - error_detect  (0.25): Coverage of known errors (type-level recall)
  - summary       (0.20): Summary completeness
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

from app.features.environment.models import Action, Reward
from app.features.tasks.base import f1_score, partial_match_score

PII_WEIGHTS = {
    "names": 0.15,
    "emails": 0.10,
    "phones": 0.10,
    "addresses": 0.08,
    "companies": 0.07,
    "shops": 0.05,
}
ERROR_WEIGHT = 0.25
SUMMARY_WEIGHT = 0.20


def normalize_phone(phone: str) -> str:
    """Normalize phone number to digits only for comparison."""
    return re.sub(r"[^0-9]", "", phone)


class ContentReviewGrader:
    """Deterministic grader for the content-review task."""

    def grade(
        self,
        action: Action,
        ground_truth: Dict[str, Any],
        step: int,
        max_steps: int,
    ) -> Reward:
        analysis = action.analysis
        gt_pii = ground_truth.get("pii", {})
        gt_errors = ground_truth.get("errors", [])

        agent_pii = analysis.get("pii", {})
        agent_errors = analysis.get("errors", [])

        breakdown = {}
        total = 0.0

        # ── PII Scoring ──────────────────────────────────────────────────────
        for field, weight in PII_WEIGHTS.items():
            expected = gt_pii.get(field, [])
            predicted = agent_pii.get(field, [])

            if field == "phones":
                expected_norm = [normalize_phone(p) for p in expected]
                predicted_norm = [normalize_phone(p) for p in predicted]
                score = f1_score(predicted_norm, expected_norm)
            elif field in ("addresses",):
                score = partial_match_score(predicted, expected)
            else:
                score = f1_score(predicted, expected)

            breakdown[f"pii_{field}"] = round(score, 4)
            total += score * weight

        # ── Error Detection Scoring ───────────────────────────────────────────
        error_score = self._score_errors(agent_errors, gt_errors)
        breakdown["error_detection"] = round(error_score, 4)
        total += error_score * ERROR_WEIGHT

        # ── Summary Scoring ───────────────────────────────────────────────────
        summary = analysis.get("summary", "")
        summary_score = self._score_summary(summary, gt_pii, gt_errors)
        breakdown["summary"] = round(summary_score, 4)
        total += summary_score * SUMMARY_WEIGHT

        total = round(max(0.0, min(1.0, total)), 4)
        done = step + 1 >= max_steps

        feedback = self._build_feedback(
            breakdown, total, gt_pii, agent_pii, gt_errors, agent_errors,
            ground_truth=ground_truth,
        )

        return Reward(score=total, breakdown=breakdown, feedback=feedback, done=done)

    def _score_errors(self, agent_errors: List[Any], gt_errors: List[Dict]) -> float:
        """Score error detection by type-level recall with partial credit."""
        if not gt_errors:
            return 1.0 if not agent_errors else 0.9

        gt_types = [e.get("type", "") for e in gt_errors]
        agent_types = []
        for err in agent_errors:
            if isinstance(err, dict):
                t = err.get("type", "").lower()
                agent_types.append(t)

        found = 0
        for gt_type in gt_types:
            if any(gt_type.lower() in at for at in agent_types):
                found += 1

        recall = found / len(gt_types)

        fp = max(0, len(agent_errors) - len(gt_errors))
        fp_penalty = min(0.15, fp * 0.05)

        return max(0.0, recall - fp_penalty)

    def _score_summary(self, summary: str, gt_pii: Dict, gt_errors: List) -> float:
        if not summary or not summary.strip():
            return 0.0
        length = len(summary.strip())
        score = 0.0
        if length >= 100:
            score += 0.5
        elif length >= 50:
            score += 0.3
        else:
            score += 0.1
        summary_lower = summary.lower()
        mentioned = sum(1 for k in gt_pii if k in summary_lower and gt_pii[k])
        score += min(0.5, mentioned * 0.1)
        return min(1.0, score)

    def _build_feedback(
        self,
        breakdown: Dict,
        total: float,
        gt_pii: Dict,
        agent_pii: Dict,
        gt_errors: List,
        agent_errors: List,
        ground_truth: Dict[str, Any] = None,
    ) -> str:
        parts = [f"Content-review score: {total:.3f}"]
        hints = (ground_truth or {}).get("hints", {})

        # PII feedback with hints
        weak_pii = [k for k in PII_WEIGHTS if breakdown.get(f"pii_{k}", 0) < 0.5 and gt_pii.get(k)]
        if weak_pii:
            hint_strs = []
            for k in weak_pii:
                if k in hints:
                    hint_strs.append(f"{k} (hint: {hints[k]})")
                else:
                    hint_strs.append(k)
            parts.append(f"Low PII scores for: {', '.join(hint_strs)}")

        # Error feedback with hints
        error_score = breakdown.get("error_detection", 0)
        if error_score < 0.5:
            error_hint = hints.get("errors", "")
            if error_hint:
                parts.append(f"Missed errors — hint: {error_hint}")
            else:
                parts.append(f"Missed many errors — {len(gt_errors)} errors in document")
        elif error_score == 1.0:
            parts.append("All error types correctly identified!")

        if breakdown.get("summary", 0) < 0.4:
            parts.append("Summary needs more detail — mention PII categories and error types found")

        return " | ".join(parts)