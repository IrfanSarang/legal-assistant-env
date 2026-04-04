"""
Integration tests for the LegalAssistantEnv class.
Run: pytest tests/test_env.py -v
"""
import pytest
from app.features.environment.env import LegalAssistantEnv
from app.features.environment.models import Action
from app.core.exceptions import EpisodeNotStartedError, TaskNotFoundError


class TestLegalAssistantEnv:

    def setup_method(self):
        self.env = LegalAssistantEnv()

    # ── reset() ──────────────────────────────────────────────────────────────

    def test_reset_returns_observation(self):
        obs = self.env.reset("format-check")
        assert obs.task == "format-check"
        assert obs.document_text != ""
        assert obs.step == 0
        assert obs.max_steps == 5
        assert obs.previous_reward == 0.0

    def test_reset_content_review(self):
        obs = self.env.reset("content-review")
        assert obs.task == "content-review"
        assert obs.max_steps == 8

    def test_reset_compliance_check(self):
        obs = self.env.reset("compliance-check")
        assert obs.task == "compliance-check"
        assert obs.max_steps == 10

    def test_reset_invalid_task_raises(self):
        with pytest.raises(TaskNotFoundError):
            self.env.reset("invalid-task")

    def test_reset_with_fixture_id(self):
        obs = self.env.reset("format-check", fixture_id="fc-001")
        assert obs.metadata["fixture_id"] == "fc-001"

    def test_reset_clears_previous_state(self):
        self.env.reset("format-check")
        action = Action(task="format-check", analysis={"issues": [], "summary": "test"})
        self.env.step(action)
        # Reset again
        obs = self.env.reset("content-review")
        assert obs.step == 0
        state = self.env.state()
        assert state.task == "content-review"

    # ── step() ───────────────────────────────────────────────────────────────

    def test_step_without_reset_raises(self):
        env = LegalAssistantEnv()
        action = Action(task="format-check", analysis={"issues": [], "summary": "test"})
        with pytest.raises(EpisodeNotStartedError):
            env.step(action)

    def test_step_returns_valid_reward_range(self):
        self.env.reset("format-check")
        action = Action(task="format-check", analysis={"issues": [], "summary": "No issues found."})
        _, reward, _, _ = self.env.step(action)
        assert 0.0 <= reward.score <= 1.0

    def test_step_advances_step_counter(self):
        self.env.reset("format-check")
        action = Action(task="format-check", analysis={"issues": [], "summary": "test"})
        obs, _, _, _ = self.env.step(action)
        assert obs.step == 1

    def test_episode_ends_at_max_steps(self):
        self.env.reset("format-check")
        action = Action(task="format-check", analysis={"issues": [], "summary": "test"})
        done = False
        for _ in range(5):
            _, _, done, _ = self.env.step(action)
            if done:
                break
        assert done is True

    def test_cumulative_reward_accumulates(self):
        self.env.reset("format-check", fixture_id="fc-001")
        action = Action(
            task="format-check",
            analysis={
                "issues": [
                    {"type": "page_numbers", "description": "missing", "severity": "high"},
                    {"type": "text_alignment", "description": "not justified", "severity": "medium"},
                ],
                "summary": "Found two formatting issues: page numbers missing and text alignment issues.",
            }
        )
        self.env.step(action)
        state = self.env.state()
        assert state.cumulative_reward > 0.0
        assert len(state.rewards_history) == 1

    # ── state() ──────────────────────────────────────────────────────────────

    def test_state_before_reset(self):
        env = LegalAssistantEnv()
        state = env.state()
        assert state.active is False
        assert state.step == 0

    def test_state_after_reset(self):
        self.env.reset("compliance-check")
        state = self.env.state()
        assert state.active is True
        assert state.task == "compliance-check"
        assert state.step == 0

    def test_state_after_step(self):
        self.env.reset("format-check")
        action = Action(task="format-check", analysis={"issues": [], "summary": "test"})
        self.env.step(action)
        state = self.env.state()
        assert state.step == 1
        assert len(state.rewards_history) == 1


# ── Full episode walkthrough ──────────────────────────────────────────────────

class TestFullEpisode:

    def test_format_check_full_episode(self):
        env = LegalAssistantEnv()
        obs = env.reset("format-check", fixture_id="fc-002")
        assert obs.document_text != ""

        rewards = []
        for i in range(obs.max_steps):
            action = Action(
                task="format-check",
                analysis={
                    "issues": [
                        {"type": "headings", "description": "Inconsistent heading case", "severity": "high"},
                        {"type": "text_alignment", "description": "Not fully justified", "severity": "medium"},
                    ],
                    "summary": "Document has heading inconsistency and text alignment issues.",
                }
            )
            _, reward, done, info = env.step(action)
            rewards.append(reward.score)
            assert 0.0 <= reward.score <= 1.0
            if done:
                break

        assert len(rewards) > 0
        assert all(0.0 <= r <= 1.0 for r in rewards)

    def test_all_tasks_run_without_error(self):
        env = LegalAssistantEnv()
        for task in ["format-check", "content-review", "compliance-check"]:
            obs = env.reset(task)
            action = Action(
                task=task,
                analysis={
                    "issues": [],
                    "errors": [],
                    "pii": {"names": [], "emails": [], "phones": [], "addresses": [], "companies": [], "shops": []},
                    "violations": [],
                    "compliant_clauses": [],
                    "summary": "Analysis complete.",
                }
            )
            _, reward, _, _ = env.step(action)
            assert 0.0 <= reward.score <= 1.0
