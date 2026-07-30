# Prototype — VLearn Learning Check Agent

Working Streamlit prototype: real OpenAI-backed comprehension check on top of the two
supplied course slide decks. Full architecture, HAX principles, and quality bar live in
`spec.md` and `README.md` at the repo root — this file only covers what's in this folder.

- `app.py` — Streamlit entry point.
- `components/` — `course_materials.py` (deterministic PDF/page lookup), `learning_agent.py`
  (bounded state machine + reason codes + model adapter + scoring), `ai_client.py`
  (OpenAI structured-generation adapter), `chatbot_panel.py` / `quiz_panel.py` /
  `document_panel.py` (UI), `document_selector_frontend/` (PDF.js text-selection widget),
  `mock_data.py` (historical CP2 artifact, not imported by the app).
- `requirements.txt` — dependencies for this prototype.

## Run (from the repo root, not from inside this folder)

`data/vlearn-pack/`, `.env`, and `.streamlit/config.toml` are resolved relative to the
process working directory, so always launch from the repo root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r codebase/requirements.txt
Copy-Item .env.example .env   # fill in OPENAI_API_KEY
streamlit run codebase/app.py
```

`tests/` and `eval/run_golden_set.py` (both at repo root, per the submission structure)
import from here by adding `codebase/` to `sys.path` — see either file's top for the exact
line.

## What used to be here

An earlier, fully-mocked CP2 prototype (fixed 3-question quiz, `0–3/3` scoring, static
citations) lived in this folder before the CP3 rebuild. It is preserved in git history, not
in the working tree, to avoid a TA finding stale, contradictory behavior next to the real
prototype.
