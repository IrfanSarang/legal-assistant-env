# 🏆 Scaler × Meta PyTorch OpenEnv Hackathon — Complete Context

## Event Overview
- **Hackathon**: Scaler School of Technology × Meta PyTorch OpenEnv Hackathon
- **Round 1 Deadline**: April 8, 2026, 11:59 PM IST
- **Finale**: April 25–26, 2026
- **Goal**: Build a complete, real-world OpenEnv environment an AI agent can learn from
- **Results**: April 10, 2026 (top 3,000 of 20,000 teams advance)

---

## Our Project: `Legal-Assistant` OpenEnv Environment

### Concept
An OpenEnv environment where an AI agent learns to **analyze legal documents** — a real-world task paralegal teams and legal software companies do daily. The agent reads contracts, NDAs, service agreements, and other legal documents, then performs structured legal analysis tasks of increasing complexity.

### Why This Domain?
- Real-world, high-stakes task (not a toy)
- Clear, deterministic grading criteria
- Rich partial-reward signal across the full trajectory
- Fills a genuine gap in the RL/agent evaluation ecosystem

---

## The 3 Tasks (Easy → Medium → Hard)

### Task 1: `format-check` (Easy)
**What the agent does:**
- Check if the document has proper page numbers
- Verify text alignment is justified (not left/center/right)
- Check font consistency (Times New Roman 12pt or Arial 11pt standard legal)
- Verify margin compliance (1-inch standard)
- Check for proper section headings
- Produce a structured format compliance report + summary

**Grader logic:**
- Scores 0.0–1.0 based on how many format issues are correctly identified vs ground truth
- Partial credit for finding some issues
- Bonus for clean structured summary

**Expected difficulty**: Easy — agent just needs to parse document metadata and structure

---

### Task 2: `content-review` (Medium)
**What the agent does:**
- Detect grammatical errors and spelling mistakes
- Identify logical inconsistencies (e.g., conflicting clause dates, contradictory terms)
- **Highlight Personal Identifiable Information (PII)**:
  - Names of parties (individuals and companies)
  - Email addresses
  - Phone numbers
  - Addresses
  - Company names
  - Shop/business names
- Produce an annotated summary with all findings categorized

**Grader logic:**
- Precision/recall scoring for PII extraction vs labeled ground truth
- Partial scores for grammar/logic checks
- Structured output format compliance bonus

**Expected difficulty**: Medium — requires NLP understanding + structured extraction

---

### Task 3: `compliance-check` (Hard)
**What the agent does:**
- Analyze contract clauses against **Indian Contract Act, 1872**
- Check compliance with:
  - Indian Contract Act, 1872 (offer, acceptance, consideration, capacity, free consent)
  - Indian IT Act, 2000 (for digital contracts)
  - Consumer Protection Act, 2019 (for B2C agreements)
  - DPDP Act, 2023 (for data privacy clauses)
  - Arbitration and Conciliation Act, 1996 (for dispute resolution clauses)
- Flag non-compliant clauses with specific law references
- Suggest compliant alternatives
- Produce a legal compliance summary report

**Grader logic:**
- Scored against curated ground-truth compliance checklists
- Partial credit for identifying correct law but wrong section
- Hard — frontier models still miss nuanced Indian law interpretations

**Expected difficulty**: Hard — requires deep legal reasoning about Indian law

---

## Project Structure

```
legal-assistant-env/
├── app/                          # FastAPI application (feature-based)
│   ├── main.py                   # FastAPI app entry point
│   ├── core/
│   │   ├── config.py             # Settings, env vars
│   │   └── logging.py            # Structured logging
│   ├── features/
│   │   ├── environment/          # OpenEnv core
│   │   │   ├── models.py         # Pydantic: Observation, Action, Reward
│   │   │   ├── env.py            # LegalAssistantEnv class
│   │   │   └── router.py         # /step /reset /state endpoints
│   │   ├── tasks/
│   │   │   ├── format_check/     # Task 1
│   │   │   │   ├── grader.py
│   │   │   │   └── fixtures.py   # Sample documents + ground truth
│   │   │   ├── content_review/   # Task 2
│   │   │   │   ├── grader.py
│   │   │   │   └── fixtures.py
│   │   │   └── compliance_check/ # Task 3
│   │   │       ├── grader.py
│   │   │       └── fixtures.py
│   │   └── health/
│   │       └── router.py
├── inference.py                  # ← MUST be in root, uses [START]/[STEP]/[END] format
├── openenv.yaml                  # OpenEnv spec metadata
├── Dockerfile                    # Multi-stage production Docker build
├── requirements.txt
├── README.md
└── HACKATHON_CONTEXT.md          # ← This file
```

---

## OpenEnv API Spec (Must Implement)

### Endpoints
- `POST /reset` → returns initial `Observation`
- `POST /step` → takes `Action`, returns `(Observation, Reward, done, info)`
- `GET /state` → returns current state

### Pydantic Models
```python
class Action(BaseModel):
    task: str           # "format-check" | "content-review" | "compliance-check"
    document_text: str  # The legal document content
    analysis: dict      # Agent's structured analysis output

class Observation(BaseModel):
    task: str
    document_text: str
    instructions: str
    step: int
    max_steps: int
    previous_reward: float

class Reward(BaseModel):
    score: float        # 0.0 – 1.0
    breakdown: dict     # Partial scores per sub-criterion
    feedback: str       # Human-readable feedback
    done: bool
```

---

## Environment Variables Required

```bash
API_BASE_URL=https://router.huggingface.co/v1   # LLM API endpoint
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct            # Model identifier
HF_TOKEN=hf_xxx                                  # Hugging Face token / API key
```

---

## inference.py Log Format (STRICT — do not deviate)

```
[START] task=format-check env=legal-assistant model=Qwen2.5-72B-Instruct
[STEP] step=1 action=format_check reward=0.45 done=false error=null
[STEP] step=2 action=content_review reward=0.72 done=false error=null
[STEP] step=3 action=compliance_check reward=0.61 done=true error=null
[END] success=true steps=3 score=0.593 rewards=0.45,0.72,0.61
```

---

## Evaluation Weights

| Criterion | Weight | Notes |
|-----------|--------|-------|
| Real-world utility | 30% | Legal doc analysis is used daily |
| Task & grader quality | 25% | 3 tasks, 0.0–1.0 graders, deterministic |
| Environment design | 20% | Clean state, reward shaping, episode boundaries |
| Code quality & spec compliance | 15% | FastAPI feature-based, openenv validate passes |
| Creativity & novelty | 10% | Indian law compliance is novel in OpenEnv |

---

## Pre-Submission Checklist

- [ ] `openenv validate` passes
- [ ] `docker build && docker run` works
- [ ] HF Space deployed and returns 200 on `/reset`
- [ ] `inference.py` runs < 20 min on 2vCPU / 8GB RAM
- [ ] All 3 graders return scores in [0.0, 1.0]
- [ ] `[START]`/`[STEP]`/`[END]` logs emit correctly
- [ ] `API_BASE_URL`, `MODEL_NAME`, `HF_TOKEN` env vars configured

---

## Key Constraints

- Inference script runtime: **< 20 minutes**
- Machine: **2 vCPU, 8 GB RAM**
- LLM calls: **OpenAI client only** (pointing to HF router)
- Inference script: **must be named `inference.py`** in project root
- All LLM API calls use `API_BASE_URL` + `MODEL_NAME` + `HF_TOKEN`

---

## Useful Links
- Dashboard: https://www.scaler.com/school-of-technology/meta-pytorch-hackathon/dashboard
- Discord: https://discord.gg/Dedhy5pkWD
- Support: help_openenvhackathon@scaler.com
- Bootcamp recording: https://www.youtube.com/live/kkCNMz0Ptd8
- OpenEnv course repo: https://github.com/raun/openenv-course/tree/main
