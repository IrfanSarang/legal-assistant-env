"""
Core configuration — reads from environment variables.
All LLM calls use API_BASE_URL + MODEL_NAME + HF_TOKEN as required by hackathon rules.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # ── LLM (Required by hackathon) ──────────────────────────────────────────
    api_base_url: str = "https://router.huggingface.co/v1"
    model_name: str = "Qwen/Qwen2.5-72B-Instruct"
    hf_token: str = "dummy-token"

    # ── Environment metadata ─────────────────────────────────────────────────
    environment_name: str = "legal-assistant"
    environment_version: str = "1.0.0"

    # ── Episode config ───────────────────────────────────────────────────────
    max_steps_format_check: int = 5
    max_steps_content_review: int = 8
    max_steps_compliance_check: int = 10

    # ── Server ───────────────────────────────────────────────────────────────
    port: int = 7860
    host: str = "0.0.0.0"
    log_level: str = "INFO"
    debug: bool = False

    def max_steps_for_task(self, task: str) -> int:
        mapping = {
            "format-check": self.max_steps_format_check,
            "content-review": self.max_steps_content_review,
            "compliance-check": self.max_steps_compliance_check,
        }
        return mapping.get(task, 5)


@lru_cache()
def get_settings() -> Settings:
    return Settings()
