# ⚖️ Legal-Assistant — OpenEnv Environment

> **Scaler × Meta PyTorch OpenEnv Hackathon | Round 1**  
> An AI agent environment for legal document analysis — format checking, PII extraction, and Indian law compliance.

---

## Overview

**Legal-Assistant** is an OpenEnv environment where an AI agent learns to analyze legal documents. This is a real-world task performed daily by paralegals, legal associates, and compliance teams at law firms and LegalTech companies across India.

The environment exposes **3 tasks of increasing difficulty**, each with curated legal document fixtures and deterministic graders that score agent performance from `0.0` to `1.0`.

---

## Tasks

| Task | Difficulty | Max Steps | Expected Score (frontier) |
|------|-----------|-----------|--------------------------|
| `format-check` | 🟢 Easy | 5 | ~0.75 |
| `content-review` | 🟡 Medium | 8 | ~0.62 |
| `compliance-check` | 🔴 Hard | 10 | ~0.45 |

### Task 1: `format-check` (Easy)
Check legal documents for standard formatting compliance:
- Page numbers (present and correctly placed)
- Text alignment (fully justified body text)
- Font compliance (Times New Roman 12pt or Arial 11pt)
- Margin compliance (1-inch standard)
- Heading consistency and numbering
- Line spacing (1.5x or double)

**Grader:** F1 score on issue types × 0.60 + summary quality × 0.20 + false-positive penalty × 0.10 + count accuracy × 0.10

---

### Task 2: `content-review` (Medium)
Identify content errors and extract all PII:
- **Errors:** grammar, spelling mistakes, logical inconsistencies
- **PII:** names, emails, phone numbers, addresses, company names, shop names

**Grader:** Per-category PII F1 scores + error detection recall + summary quality

---

### Task 3: `compliance-check` (Hard)
Analyze contract clauses against Indian law:
- **Indian Contract Act, 1872** — penalty clauses (S.74), restraint of trade (S.27), restraint of proceedings (S.28), free consent (S.14)
- **DPDP Act, 2023** — consent requirements (S.6), purpose limitation (S.4), data principal rights (S.17)
- **Consumer Protection Act, 2019** — unfair trade practices (S.2(47)), unfair contract terms (S.2(48))
- **Arbitration and Conciliation Act, 1996** — written agreement (S.7), seat of arbitration (S.20)
- **IT Act, 2000** — electronic contract validity (S.10A)

**Grader:** Law identification F1 × 0.40 + section citation accuracy × 0.30 + suggestion quality × 0.20 + completeness × 0.10

---

## Observation Space

```json
{
  "task": "format-check | content-review | compliance-check",
  "document_text": "<full legal document text>",
  "instructions": "<task-specific analysis instructions>",
  "step": 0,
  "max_steps": 5,
  "previous_reward": 0.0,
  "metadata": {
    "fixture_id": "fc-001",
    "difficulty": "easy",
    "document_type": "NDA",
    "jurisdiction": "India"
  }
}
```

## Action Space

```json
{
  "task": "format-check",
  "analysis": {
    // format-check:
    "issues": [{"type": "page_numbers", "description": "...", "severity": "high"}],
    "summary": "...",
    "format_score": 0.7,

    // content-review:
    "errors": [{"type": "spelling", "text": "Febuary", "correction": "February"}],
    "pii": {"names": ["..."], "emails": ["..."], "phones": ["..."], "addresses": ["..."], "companies": ["..."], "shops": ["..."]},
    "summary": "...",

    // compliance-check:
    "violations": [{"clause": "...", "law": "Indian Contract Act", "section": "27", "issue": "...", "suggestion": "..."}],
    "compliant_clauses": ["..."],
    "summary": "..."
  },
  "step_notes": "optional reasoning trace"
}
```

---

## Setup & Usage

### Prerequisites
- Python 3.11+
- Docker (optional)

### Local Development

```bash
# 1. Clone and install
git clone <your-repo>
cd legal-assistant-env
pip install -r requirements.txt

# 2. Configure environment variables
cp .env.example .env
# Edit .env with your API_BASE_URL, MODEL_NAME, HF_TOKEN

# 3. Start the server
uvicorn app.main:app --host 0.0.0.0 --port 7860 --reload

# 4. Test the API
curl http://localhost:7860/
curl -X POST "http://localhost:7860/env/reset?task=format-check"
```

### Docker

```bash
docker build -t legal-assistant .
docker run -p 7860:7860 \
  -e API_BASE_URL=https://router.huggingface.co/v1 \
  -e MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
  -e HF_TOKEN=hf_xxx \
  legal-assistant
```

### Run Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Run Inference

```bash
export API_BASE_URL=https://router.huggingface.co/v1
export MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
export HF_TOKEN=hf_xxx
export ENV_BASE_URL=http://localhost:7860

python inference.py
```

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check + env info |
| `/health` | GET | Health check |
| `/env/reset` | POST | Start new episode |
| `/env/step` | POST | Submit agent action |
| `/env/state` | GET | Current episode state |
| `/docs` | GET | Interactive Swagger UI |

---

## Reward Design

Rewards are **shaped across the trajectory** — not just binary end-of-episode:

- Partial credit for each correctly identified issue/violation
- Per-category PII extraction scored independently
- False positive penalties prevent gaming with exhaustive lists
- Summary quality bonus for well-structured output

---

## Project Structure

```
legal-assistant-env/
├── app/
│   ├── main.py                        # FastAPI app factory
│   ├── core/
│   │   ├── config.py                  # Pydantic Settings
│   │   ├── logging.py                 # Structured logging
│   │   └── exceptions.py             # Custom exceptions
│   └── features/
│       ├── environment/              # OpenEnv core
│       │   ├── models.py             # Action, Observation, Reward
│       │   ├── env.py                # LegalAssistantEnv
│       │   ├── state.py              # Episode state
│       │   └── router.py             # API routes
│       ├── tasks/
│       │   ├── base.py               # BaseTask, f1_score utils
│       │   ├── format_check/         # Task 1
│       │   ├── content_review/       # Task 2
│       │   └── compliance_check/     # Task 3 + Indian law DB
│       └── health/
│           └── router.py
├── tests/
│   ├── test_env.py                   # Integration tests
│   └── test_graders.py               # Grader unit tests
├── inference.py                      # Baseline inference script
├── openenv.yaml                      # OpenEnv spec
├── Dockerfile                        # Multi-stage production build
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Baseline Scores

Expected scores using `Qwen/Qwen2.5-72B-Instruct`:

| Task | Baseline Score |
|------|---------------|
| format-check | ~0.72 |
| content-review | ~0.58 |
| compliance-check | ~0.41 |
| **Average** | **~0.57** |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_BASE_URL` | ✅ | LLM API endpoint (HF router) |
| `MODEL_NAME` | ✅ | Model identifier |
| `HF_TOKEN` | ✅ | Hugging Face API key |
| `ENV_BASE_URL` | For inference | URL of running env server |

---

## Hackathon Compliance

- ✅ `openenv.yaml` present with full metadata
- ✅ `inference.py` in project root
- ✅ Uses OpenAI client for all LLM calls
- ✅ `[START]` / `[STEP]` / `[END]` log format
- ✅ `API_BASE_URL`, `MODEL_NAME`, `HF_TOKEN` env vars
- ✅ Inference runtime < 20 minutes
- ✅ Docker build works
- ✅ 3+ tasks with deterministic graders scoring 0.0–1.0
- ✅ Meaningful reward shaping (not binary)
