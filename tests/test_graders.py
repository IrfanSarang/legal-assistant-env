"""
Unit tests for all 3 graders.
Run: pytest tests/test_graders.py -v
"""
import pytest
from app.features.environment.models import Action
from app.features.tasks.format_check.grader import FormatCheckGrader
from app.features.tasks.content_review.grader import ContentReviewGrader
from app.features.tasks.compliance_check.grader import ComplianceCheckGrader
from app.features.tasks.format_check.fixtures import FIXTURES as FC_FIXTURES
from app.features.tasks.content_review.fixtures import FIXTURES as CR_FIXTURES
from app.features.tasks.compliance_check.fixtures import FIXTURES as CC_FIXTURES


# ── Format Check Grader ───────────────────────────────────────────────────────

class TestFormatCheckGrader:
    grader = FormatCheckGrader()

    def _action(self, issues, summary="Compliant doc with some formatting issues found in the analysis."):
        return Action(task="format-check", analysis={"issues": issues, "summary": summary, "format_score": 0.5})

    def test_perfect_score(self):
        gt = FC_FIXTURES[0]["ground_truth"]
        issues = [{"type": t["type"], "description": t["description"], "severity": t["severity"]}
                  for t in gt["issues"]]
        action = self._action(issues, summary="Document is missing page numbers, text alignment is not justified, and line spacing is not defined.")
        reward = self.grader.grade(action, gt, step=0, max_steps=5)
        assert reward.score >= 0.7, f"Perfect answer should score >=0.7, got {reward.score}"
        assert 0.0 <= reward.score <= 1.0

    def test_empty_analysis_scores_low(self):
        gt = FC_FIXTURES[0]["ground_truth"]
        action = self._action([], summary="")
        reward = self.grader.grade(action, gt, step=0, max_steps=5)
        assert reward.score < 0.3

    def test_false_positives_penalized(self):
        # fc-002: compliant=[page_numbers,margins], issues=[headings,text_alignment,font]
        # line_spacing is uncovered — flagging it is a false positive
        gt = FC_FIXTURES[1]["ground_truth"]
        issues = [
            {"type": "headings", "description": "Inconsistent case", "severity": "high"},
            {"type": "line_spacing", "description": "Wrong spacing (not an issue here)", "severity": "low"},
        ]
        action = self._action(issues, summary="Found heading and line spacing issues.")
        reward = self.grader.grade(action, gt, step=0, max_steps=5)
        assert 0.0 <= reward.score <= 1.0
        assert reward.breakdown["false_positive_score"] < 1.0

    def test_score_in_valid_range(self):
        for fixture in FC_FIXTURES:
            action = self._action([])
            reward = self.grader.grade(action, fixture["ground_truth"], step=0, max_steps=5)
            assert 0.0 <= reward.score <= 1.0, f"Score out of range for {fixture['id']}"

    def test_done_at_last_step(self):
        gt = FC_FIXTURES[0]["ground_truth"]
        action = self._action([])
        reward = self.grader.grade(action, gt, step=4, max_steps=5)
        assert reward.done is True

    def test_not_done_at_early_step(self):
        gt = FC_FIXTURES[0]["ground_truth"]
        action = self._action([])
        reward = self.grader.grade(action, gt, step=0, max_steps=5)
        assert reward.done is False


# ── Content Review Grader ─────────────────────────────────────────────────────

class TestContentReviewGrader:
    grader = ContentReviewGrader()

    def _action(self, pii=None, errors=None, summary=""):
        return Action(
            task="content-review",
            analysis={
                "pii": pii or {"names": [], "emails": [], "phones": [], "addresses": [], "companies": [], "shops": []},
                "errors": errors or [],
                "summary": summary,
            }
        )

    def test_perfect_pii_scores_well(self):
        fixture = CR_FIXTURES[0]
        gt = fixture["ground_truth"]
        action = self._action(
            pii=gt["pii"],
            errors=[{"type": e["type"], "text": e["text"]} for e in gt["errors"]],
            summary="Found 2 PII contacts, 2 errors including spelling and logical inconsistency."
        )
        reward = self.grader.grade(action, gt, step=0, max_steps=8)
        assert reward.score >= 0.65
        assert 0.0 <= reward.score <= 1.0

    def test_empty_scores_low(self):
        gt = CR_FIXTURES[0]["ground_truth"]
        action = self._action()
        reward = self.grader.grade(action, gt, step=0, max_steps=8)
        assert reward.score < 0.3

    def test_phone_normalization(self):
        """Phone numbers with different formatting should still match."""
        gt = CR_FIXTURES[0]["ground_truth"]
        action = self._action(
            pii={
                "names": [], "emails": [], "phones": ["91-9876543210", "022 4455 6677"],
                "addresses": [], "companies": [], "shops": []
            }
        )
        reward = self.grader.grade(action, gt, step=0, max_steps=8)
        assert reward.breakdown["pii_phones"] > 0.5

    def test_all_fixtures_valid_range(self):
        for fixture in CR_FIXTURES:
            action = self._action()
            reward = self.grader.grade(action, fixture["ground_truth"], step=0, max_steps=8)
            assert 0.0 <= reward.score <= 1.0, f"Score out of range for {fixture['id']}"


# ── Compliance Check Grader ───────────────────────────────────────────────────

class TestComplianceCheckGrader:
    grader = ComplianceCheckGrader()

    def _action(self, violations=None, compliant=None, summary=""):
        return Action(
            task="compliance-check",
            analysis={
                "violations": violations or [],
                "compliant_clauses": compliant or [],
                "summary": summary,
            }
        )

    def test_correct_laws_score_well(self):
        fixture = CC_FIXTURES[0]
        gt = fixture["ground_truth"]
        violations = [
            {
                "clause": v["clause"],
                "law": v["law"],
                "section": v["section"],
                "issue": v["issue"],
                "suggestion": v["suggestion"],
            }
            for v in gt["violations"]
        ]
        action = self._action(
            violations=violations,
            summary="Multiple violations found under ICA 1872, DPDP Act 2023, and ACA 1996."
        )
        reward = self.grader.grade(action, gt, step=0, max_steps=10)
        assert reward.score >= 0.7
        assert 0.0 <= reward.score <= 1.0

    def test_empty_violations_scores_low(self):
        gt = CC_FIXTURES[0]["ground_truth"]
        action = self._action()
        reward = self.grader.grade(action, gt, step=0, max_steps=10)
        assert reward.score < 0.25

    def test_law_aliases_resolved(self):
        """Test that law alias resolution works (ICA = Indian Contract Act)."""
        gt = CC_FIXTURES[0]["ground_truth"]
        violations = [
            {
                "clause": "Clause 5",
                "law": "ICA",  # alias
                "section": "27",
                "issue": "Restraint of trade",
                "suggestion": "Remove this clause entirely as it is void under section 27 of the ICA.",
            }
        ]
        action = self._action(violations=violations)
        reward = self.grader.grade(action, gt, step=0, max_steps=10)
        assert reward.breakdown["law_identification"] > 0.0

    def test_all_fixtures_valid_range(self):
        for fixture in CC_FIXTURES:
            action = self._action()
            reward = self.grader.grade(action, fixture["ground_truth"], step=0, max_steps=10)
            assert 0.0 <= reward.score <= 1.0, f"Score out of range for {fixture['id']}"

    def test_score_in_valid_range_always(self):
        """Reward score must always be in [0.0, 1.0] — fuzz test."""
        gt = CC_FIXTURES[1]["ground_truth"]
        for _ in range(20):
            import random
            violations = [
                {"clause": "Random", "law": random.choice(["ICA", "DPDP", "CPA", "junk"]),
                 "section": str(random.randint(1, 100)), "issue": "some issue",
                 "suggestion": "Replace with compliant clause that meets statutory requirements."}
            ] * random.randint(0, 8)
            action = self._action(violations=violations)
            reward = self.grader.grade(action, gt, step=0, max_steps=10)
            assert 0.0 <= reward.score <= 1.0


# ── Cross-task sanity checks ──────────────────────────────────────────────────

class TestRewardModel:
    def test_reward_score_clamped(self):
        from app.features.environment.models import Reward
        r = Reward(score=1.5, breakdown={}, feedback="test", done=False)
        assert r.score == 1.0

        r2 = Reward(score=-0.5, breakdown={}, feedback="test", done=False)
        assert r2.score == 0.0
