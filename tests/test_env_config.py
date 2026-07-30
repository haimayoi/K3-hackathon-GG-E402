from pathlib import Path

from services.ai_client import AIConfig


def test_ai_config_reads_dotenv_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("GEMINI_API_KEY=from-dotenv\nLLM_PROVIDER=gemini\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_PROVIDER", raising=False)

    config = AIConfig.from_env()

    assert config.api_key == "from-dotenv"
    assert config.provider == "gemini"
