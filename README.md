# VLearn Learning Check Agent

A bounded, source-grounded comprehension check for learners using the VLearn tutor. After a learner selects course text and asks a question, the app validates the cited page, answers from that context, creates exactly one four-option quiz, scores the selected answer deterministically, gives option-specific misconception feedback, and offers one easier retry.

This is a hackathon prototype, not an open-ended autonomous agent. Unknown group and zone metadata remain intentionally unfilled: **HUMAN ACTION REQUIRED — Group [XX], Zone [X]**.

## What works

- Select either supplied course slide deck and an exact PDF page.
- Highlight text on that page and ask a contextual tutor question.
- Deterministically verify that the selection occurs on the cited page.
- Run the bounded state machine:
  `RECEIVED_CONTEXT → ELIGIBILITY_CHECK → SOURCE_VALIDATION → QUIZ_GENERATION → QUIZ_VALIDATION → PRESENTED → ANSWER_EVALUATION → FEEDBACK → RETRY or COMPLETED`.
- Safely exit through `ABSTAINED` or `ERROR_FALLBACK` with explicit reason codes.
- Validate structured model output before display; malformed output gets at most one repair attempt.
- Display one correct answer and a targeted explanation for every wrong option.
- Attach a traceable source ID such as `d1:p29` and show a collapsible safe trace.
- Reset, skip/continue, handle insufficient context, and sanitize provider failures.

## Architecture

```text
PDF page selection
  → deterministic eligibility and page/selection validation
  → minimum relevant source window
  → one structured OpenAI generation
  → deterministic schema + source validation
  → Streamlit presentation
  → deterministic answer evaluation
  → easier retry or completion
```

Key files:

- `app.py` — canonical Streamlit entry point.
- `components/course_materials.py` — deterministic two-PDF/page lookup; no embeddings or vector database.
- `components/learning_agent.py` — bounded state machine, reason codes, model adapter, validation, attempt limits, trace metadata, and scoring.
- `components/chatbot_panel.py`, `components/quiz_panel.py`, `components/document_panel.py` — user experience.
- `tests/test_learning_agent.py` — offline behavior and guardrail suite.
- `eval/golden_set.jsonl` — preserved 28-case locked evaluation set.
- `eval/run_golden_set.py` — real-provider evaluation with immutable run IDs.

`components/ai_client.py` is a privacy-hardened compatibility adapter for the preserved golden-set contract. `codebase/` and `components/mock_data.py` are historical CP2 artifacts; they are not imported by the canonical app.

## Setup

Python 3.11 is recommended.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Configure `.env` locally:

```dotenv
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

`.env` and `.streamlit/secrets.toml` are ignored. Never commit keys.

## Launch

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Demo flow:

1. Choose Day 1, page 29.
2. Highlight the `top_p` explanation and ask “top_p khác temperature như thế nào?”.
3. Answer the generated quiz correctly.
4. Repeat and choose a wrong option to show targeted misconception feedback and the easier retry.
5. Ask `2 + 2 = ?` from selected course text to show `outside_course_scope` abstention.
6. Expand **Developer/demo trace** to show source, model, latency, validation, prompt hash/version, artifact version, and transitions without chain-of-thought.

## Test and evaluation

```powershell
# Compile
.\.venv\Scripts\python.exe -m compileall -q app.py components eval tests

# Offline tests (no API key or network)
.\.venv\Scripts\python.exe -m unittest discover -s tests -v

# Real 28-case golden-set evaluation
.\.venv\Scripts\python.exe eval\run_golden_set.py
```

Every live run uses `run-live-<UTC timestamp>-<random ID>` so previous evidence is never overwritten. Automated results cover status, schema, option count, correct-index validity, misconception coverage, state transitions, and retry limits. Groundedness, concept alignment, and domain correctness remain explicitly **HUMAN REVIEW REQUIRED** unless a deterministic check is reliable. A status/schema-only run must not be described as “100% accurate.”

The locked quality bar remains unchanged in `spec.md`: at least 80% status match, plus zero invented information/concepts outside the supplied passage across the golden set.

## Reason codes

`eligible`, `insufficient_context`, `outside_course_scope`, `source_not_found`, `source_mismatch`, `schema_invalid`, `verification_failed`, and `provider_error`.

## Real versus historical mock behavior

Canonical `app.py`:

- Real OpenAI structured generation: tutor answer, primary quiz, misconceptions, and easier retry.
- Real deterministic PDF/page lookup and selection verification.
- Deterministic scoring and bounded state transitions.
- No displayed confidence score; the former fixed `0.87` was removed from the live flow.

Historical only:

- `components/mock_data.py`, `STREAMLIT_LEARNING_CHATBOT_FLOW.md`, and `codebase/` preserve the CP2 mock prototype and original brief for audit history. Their fixed answer/confidence/retry values are not used by the canonical app.

## Privacy and safety

- The model receives only the selected text plus a small window from one verified page.
- Runtime traces store UUIDs, state/reason metadata, model, prompt version/hash, source ID, latency, validation outcome, error category, character counts, and text hashes—not full learner text, secrets, raw provider errors, or chain-of-thought.
- The app treats instructions embedded in course material as untrusted source data.
- Results support self-study only; they are not grades or learner profiling.

## Limitations

- Lexical grounding validation catches source/citation mismatch but cannot prove full semantic correctness. Human review remains required for groundedness, concept alignment, and sibling-concept accuracy.
- PDF text extraction quality depends on the supplied files.
- No authentication, persistence layer, learner profile, vector search, or autonomous tool loop.
- Provider availability and latency affect live generation.
- User validation evidence has not been fabricated; see `validation/README.md` for required human work.

## Team and evidence

Preserved assignment from `spec.md`:

| Area | Owner |
|---|---|
| Evidence and specification | Lê Hà Hải Vân |
| Prototype build | Hà Duyên Hùng |
| Prompt and golden-set evaluation | Tạ Minh Đức |

Group and zone: **HUMAN ACTION REQUIRED — [XX] / [X]**.

## Restricted data warning

The supplied VLearn data pack is currently tracked in Git even though its own documentation says it must not be committed to a submission repository or shared outside the course. It includes 12 tracked files: two PDFs, six full transcripts, the anonymized chatlog CSV, and three data-documentation files. Do not make this repository public. Removing or rewriting tracked data requires explicit approval and is intentionally not performed here.