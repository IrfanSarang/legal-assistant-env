"""
Legal-Assistant OpenEnv — Improved Inference Script
=====================================================
Improvements:
  1. Conversation history with sliding window — prevents token-limit crashes on step 3
  2. Reward-aware prompting — model is told its score, sub-scores, and env feedback
  3. Exhaustive system prompts tuned to exact grader criteria
  4. JSON repair via regex so malformed output never hard-zeros
  5. Lower temperature for more deterministic structured output

Usage:
    export API_BASE_URL=https://router.huggingface.co/v1
    export MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
    export HF_TOKEN=hf_xxx
    python inference.py
"""
from __future__ import annotations

import json
import os
import re
import textwrap
import time
from typing import Any, Dict, List, Optional

import httpx
from openai import OpenAI

# ── Config ────────────────────────────────────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME   = os.getenv("MODEL_NAME",   "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN     = os.getenv("HF_TOKEN",     None)

ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:7860")
MAX_STEPS    = 3
TEMPERATURE  = 0.10
MAX_TOKENS   = 1800

# Keep system message + last N user/assistant pairs to avoid context overflow
MAX_HISTORY_TURNS = 2

TASKS    = ["format-check", "content-review", "compliance-check"]
ENV_NAME = "legal-assistant"

client = OpenAI(api_key=HF_TOKEN or "dummy", base_url=API_BASE_URL)
http   = httpx.Client(base_url=ENV_BASE_URL, timeout=90.0)


# ── Log format (strict — do not change) ──────────────────────────────────────

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} "
        f"done={str(done).lower()} error={error_val}",
        flush=True,
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


# ── Env helpers ───────────────────────────────────────────────────────────────

def env_reset(task: str) -> Dict[str, Any]:
    resp = http.post("/reset", params={"task": task})
    resp.raise_for_status()
    return resp.json()

def env_step(payload: Dict[str, Any]) -> Dict[str, Any]:
    resp = http.post("/step", json=payload)
    resp.raise_for_status()
    return resp.json()


# ── History management ────────────────────────────────────────────────────────

def trim_history(messages: List[Dict[str, str]], max_turns: int) -> List[Dict[str, str]]:
    """
    Keep system message + last `max_turns` user/assistant pairs.
    Prevents context window overflow on long compliance analyses.
    """
    system = [m for m in messages if m["role"] == "system"]
    conversation = [m for m in messages if m["role"] != "system"]
    keep = max_turns * 2
    trimmed = conversation[-keep:] if len(conversation) > keep else conversation
    return system + trimmed


# ── System prompts ────────────────────────────────────────────────────────────

SYSTEM_PROMPTS = {

"format-check": textwrap.dedent("""
    You are a senior legal document formatter. Your job is to produce an EXHAUSTIVE
    formatting audit that a grader will score against a ground-truth checklist.

    CHECK EVERY CATEGORY — missing a category loses points:

    1. page_numbers   — Are page numbers present on every page? Correct position?
    2. text_alignment — Is body text fully justified? Are headings consistently aligned?
    3. font           — Consistent typeface throughout? Body 12pt Times New Roman or 11pt Arial?
                        Headings 14pt bold? Mixed fonts = issue.
    4. margins        — 1-inch (2.54 cm) on all four sides? Consistent across pages?
    5. headings       — Hierarchical numbering (1., 1.1, 1.1.1)? Consistent capitalisation style?
    6. line_spacing   — Body text double-spaced or 1.5-spaced? Consistent between sections?

    SEVERITY:
    - high   → required element missing or structural violation
    - medium → inconsistency between sections
    - low    → minor deviation from standard

    Output ONLY a valid JSON object. No markdown, no prose before or after:
    {
      "issues": [
        {
          "type": "<page_numbers|text_alignment|font|margins|headings|line_spacing>",
          "description": "<precise description>",
          "location": "<e.g. Section 2, Page 3, Footer>",
          "severity": "<high|medium|low>"
        }
      ],
      "summary": "<2-3 sentence compliance summary>",
      "format_score": <float 0.0-1.0>
    }

    Report every issue you find. Do not invent issues that are not there.
    If a category is fully compliant, omit it from issues.
""").strip(),

"content-review": textwrap.dedent("""
    You are a senior legal content reviewer specialising in PII extraction and accuracy.

    Perform a COMPLETE two-part review:

    PART 1 — ERROR DETECTION (find ALL instances):
    • grammar            — subject-verb disagreement, tense errors, dangling modifiers
    • spelling           — misspelled words (check every word carefully)
    • logical_inconsistency — contradictory dates, conflicting terms,
                              MATH ERRORS (verify: installment × count = total?),
                              DATE ERRORS (verify: start date + duration = end date?)

    PART 2 — PII EXTRACTION (extract VERBATIM):
    • names      — ALL person names including relatives mentioned (S/o, D/o, W/o means father/mother)
    • emails     — all email addresses
    • phones     — all phone/fax/mobile numbers
    • addresses  — full physical or postal addresses
    • companies  — registered company or organisation names
    • shops      — trade names, brand names, DBA names

    RULES:
    - Check math explicitly: multiply installments x count, compare to stated total.
    - Check dates explicitly: add duration to start date, compare to stated end date.
    - Empty arrays [] are valid — do not fabricate entries.

    Output ONLY a valid JSON object. No markdown, no prose before or after:
    {
      "errors": [
        {
          "type": "<grammar|spelling|logical_inconsistency>",
          "text": "<exact text from document>",
          "correction": "<corrected version>",
          "location": "<section or paragraph>"
        }
      ],
      "pii": {
        "names":     [],
        "emails":    [],
        "phones":    [],
        "addresses": [],
        "companies": [],
        "shops":     []
      },
      "summary": "<2-3 sentence summary mentioning PII categories and error types found>"
    }
""").strip(),

"compliance-check": textwrap.dedent("""
    You are an expert in Indian commercial and contract law with 20+ years of experience.

    Audit the document against ALL five statutes. Missing a statute costs points.

    STATUTES TO CHECK:
    1. Indian Contract Act, 1872 — S.10 (free consent), S.14 (free consent definition),
       S.23 (unlawful/public policy), S.27 (restraint of trade),
       S.28 (restraint of legal proceedings), S.74 (penalty/liquidated damages)
    2. Information Technology Act, 2000 — S.4 (electronic records), S.5 (e-signatures),
       S.79 (intermediary liability)
    3. Consumer Protection Act, 2019 — S.2(47) (unfair trade practices),
       S.2(48) (unfair contract terms), S.49 (consumer commission jurisdiction)
    4. Digital Personal Data Protection Act, 2023 — S.4 (lawful processing/purpose limitation),
       S.6 (consent — must be free, specific, informed, unambiguous; no deemed consent),
       S.8 (Data Fiduciary obligations), S.17 (data portability and erasure)
    5. Arbitration and Conciliation Act, 1996 — S.7 (valid arbitration agreement),
       S.11 (arbitrator appointment), S.20 (seat of arbitration)

    For EACH violation:
    - Name the exact document clause
    - Cite FULL statute name and specific section number
    - Explain precisely what is non-compliant
    - Give a concrete compliant alternative (2+ sentences)

    Also list compliant clauses — grader gives partial credit for these.

    Output ONLY a valid JSON object. No markdown, no prose before or after:
    {
      "violations": [
        {
          "clause": "<clause/section of the document>",
          "law": "<full name of Indian statute>",
          "section": "<e.g. 27>",
          "issue": "<what is non-compliant and why>",
          "suggestion": "<specific compliant alternative, 2+ sentences>"
        }
      ],
      "compliant_clauses": ["<description of a compliant clause>"],
      "summary": "<2-3 sentence overall compliance status>"
    }
""").strip(),

}


# ── Prompt builders ───────────────────────────────────────────────────────────

def build_initial_user_prompt(obs: Dict[str, Any]) -> str:
    return textwrap.dedent(f"""
        TASK: {obs.get('task', '')}
        STEP: 1 of {obs.get('max_steps', MAX_STEPS)}

        INSTRUCTIONS FROM ENVIRONMENT:
        {obs.get('instructions', '')}

        DOCUMENT TO ANALYZE:
        ───────────────────────────────────────
        {obs.get('document_text', '')}
        ───────────────────────────────────────

        Perform a thorough analysis. Return ONLY the JSON object.
    """).strip()


def build_refinement_user_prompt(
    obs: Dict[str, Any],
    step_num: int,
    prev_reward: float,
    env_feedback: str,
    prev_analysis_json: str,
    breakdown: Optional[Dict[str, float]] = None,
) -> str:
    breakdown_str = ""
    if breakdown:
        sorted_bd = sorted(breakdown.items(), key=lambda x: x[1])
        breakdown_str = "\nSUB-SCORES (fix the lowest ones first):\n" + "\n".join(
            f"  {k}: {v:.3f}" for k, v in sorted_bd
        )

    return textwrap.dedent(f"""
        TASK: {obs.get('task', '')}
        STEP: {step_num} of {obs.get('max_steps', MAX_STEPS)}

        YOUR PREVIOUS SCORE: {prev_reward:.2f} / 1.00
        {breakdown_str}

        ENVIRONMENT FEEDBACK — ACT ON EVERY POINT:
        {env_feedback}

        YOUR PREVIOUS ANALYSIS (improve this — keep all correct findings):
        ───────────────────────────────────────
        {prev_analysis_json}
        ───────────────────────────────────────

        DOCUMENT:
        ───────────────────────────────────────
        {obs.get('document_text', '')}
        ───────────────────────────────────────

        - Address every item in ENVIRONMENT FEEDBACK.
        - Do NOT remove correct findings from the previous step.
        - Return ONLY the improved JSON object.
    """).strip()


# ── LLM call ─────────────────────────────────────────────────────────────────

def call_llm(messages: List[Dict[str, str]]) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    return response.choices[0].message.content or ""


# ── JSON parsing with repair fallback ────────────────────────────────────────

def parse_llm_output(raw: str, task: str) -> Dict[str, Any]:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    shells: Dict[str, Dict[str, Any]] = {
        "format-check": {"issues": [], "summary": raw[:300], "format_score": 0.0},
        "content-review": {
            "errors": [],
            "pii": {"names": [], "emails": [], "phones": [], "addresses": [], "companies": [], "shops": []},
            "summary": raw[:300],
        },
        "compliance-check": {"violations": [], "compliant_clauses": [], "summary": raw[:300]},
    }
    return shells.get(task, {"summary": raw[:300]})


# ── Episode runner ────────────────────────────────────────────────────────────

def run_task(task: str) -> float:
    log_start(task=task, env=ENV_NAME, model=MODEL_NAME)

    rewards: List[float] = []
    error_msg: Optional[str] = None

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPTS[task]}
    ]

    prev_reward: float = 0.0
    prev_analysis_json: str = ""
    env_feedback: str = ""
    prev_breakdown: Dict[str, float] = {}

    try:
        obs = env_reset(task)
        actual_steps = min(MAX_STEPS, obs.get("max_steps", MAX_STEPS))
        done = False

        for step_num in range(1, actual_steps + 1):
            try:
                if step_num == 1:
                    user_content = build_initial_user_prompt(obs)
                else:
                    user_content = build_refinement_user_prompt(
                        obs=obs,
                        step_num=step_num,
                        prev_reward=prev_reward,
                        env_feedback=env_feedback,
                        prev_analysis_json=prev_analysis_json,
                        breakdown=prev_breakdown,
                    )

                messages.append({"role": "user", "content": user_content})

                # Trim to last MAX_HISTORY_TURNS before calling LLM
                trimmed = trim_history(messages, max_turns=MAX_HISTORY_TURNS)
                raw_response = call_llm(trimmed)

                # Append to full history for trimming logic
                messages.append({"role": "assistant", "content": raw_response})

                analysis = parse_llm_output(raw_response, task)
                prev_analysis_json = json.dumps(analysis, indent=2)

                result = env_step({
                    "task": task,
                    "analysis": analysis,
                    "step_notes": (
                        f"Step {step_num}/{actual_steps} | "
                        f"prev_score={prev_reward:.2f} | "
                        f"refinement={'yes' if step_num > 1 else 'no'}"
                    ),
                })

                reward_obj = result["reward"]
                reward_score = reward_obj["score"]
                done = result["done"]
                obs = result["observation"]

                env_feedback = reward_obj.get("feedback", "No specific feedback provided.")
                prev_breakdown = reward_obj.get("breakdown", {})
                prev_reward = reward_score

                rewards.append(reward_score)
                log_step(
                    step=step_num,
                    action=task.replace("-", "_"),
                    reward=reward_score,
                    done=done,
                    error=None,
                )

                if done:
                    break

                time.sleep(0.5)

            except Exception as e:
                error_msg = str(e)[:80]
                rewards.append(0.0)
                log_step(
                    step=step_num,
                    action=task.replace("-", "_"),
                    reward=0.0,
                    done=True,
                    error=error_msg,
                )
                break

    except Exception as e:
        error_msg = str(e)[:80]
        rewards = [0.0]
        log_step(step=1, action=task.replace("-", "_"), reward=0.0, done=True, error=error_msg)

    final_score = sum(rewards) / len(rewards) if rewards else 0.0
    success = final_score >= 0.1 and error_msg is None

    log_end(
        success=success,
        steps=len(rewards),
        score=final_score,
        rewards=rewards,
    )

    return final_score


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    print(f"Legal-Assistant Improved Inference | Model: {MODEL_NAME}", flush=True)
    print(f"API: {API_BASE_URL} | Env: {ENV_BASE_URL}", flush=True)
    print("=" * 60, flush=True)

    all_scores: Dict[str, float] = {}

    for task in TASKS:
        score = run_task(task)
        all_scores[task] = score
        print(f"  \u2713 {task}: {score:.3f}", flush=True)
        print("-" * 40, flush=True)

    avg = sum(all_scores.values()) / len(all_scores)
    print(f"\nFINAL AVERAGE SCORE: {avg:.3f}", flush=True)
    for task, score in all_scores.items():
        print(f"  {task}: {score:.3f}", flush=True)


if __name__ == "__main__":
    main()