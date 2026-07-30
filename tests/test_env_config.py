from pathlib import Path

from services.ai_client import AIConfig


def test_ai_config_reads_dotenv_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        'OPENAI_API_KEY=from-dotenv\nOPENAI_MODEL=gpt-5.6-terra\n',
        encoding='utf-8',
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv('OPENAI_MODEL', raising=False)
    monkeypatch.delenv('LLM_MODEL', raising=False)

    config = AIConfig.from_env()

    assert config.api_key == "from-dotenv"
    assert config.provider == "openai"
    assert config.model == 'gpt-5.6-terra'


def test_ai_config_reads_openai_key_from_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "openai-key")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    config = AIConfig.from_env()

    assert config.provider == "openai"
    assert config.model == "gpt-5.6-luna"
    assert config.api_key == "openai-key"
