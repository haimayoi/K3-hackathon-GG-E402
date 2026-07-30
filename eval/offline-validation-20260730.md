# Offline validation — 2026-07-30

Command:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Result: **17 tests run, 17 passed, 0 failed**.

Automated coverage:

- valid grounded concept;
- short input with enough context;
- short input without context;
- nonexistent page/source;
- unrelated request;
- general knowledge outside course scope;
- unseen out-of-scope paraphrase;
- prompt-injection-like source text;
- malformed model output and one repair attempt;
- provider failure sanitization;
- over-refusal regression;
- confusing sibling concepts;
- deterministic wrong-answer/retry behavior;
- maximum two generation attempts;
- source mismatch reason code;
- canonical Streamlit app startup with expected controls and zero exceptions.

Checks include state/reason code, schema, four-option count, correct-index bounds, misconception coverage, retry behavior, source validation, and attempt limits. These tests use a deterministic fake provider; they do not claim semantic model accuracy.