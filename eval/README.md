# Evaluation

## Preserved assets

- `golden_set.jsonl` / `golden_set.md` — locked 28-case evaluation set and human-review rubric.
- `run-01-20260730.*` — preserved historical OpenAI run evidence; never overwritten.
- `run-live-20260730T114022Z-7889852f.*` — current real-provider run after hardening.
- `ai_call_log.jsonl` — historical CP3 raw-call evidence. It contains full prompt/output text and is retained only because existing evidence must not be removed. New code does not append to it.

## Current results

The current live run measured:

- Status match: **27/28 (96%)**.
- Schema validity among matched `ok` cases: **18/18 (100%)**.
- Failure: G26 was over-refused (`expected=ok`, `actual=insufficient`).
- Groundedness, concept alignment, and domain correctness: **HUMAN REVIEW REQUIRED**. They were not converted into an automated “accuracy” claim.

The locked status threshold (≥80%) is met. The locked zero-invention condition cannot be declared passed until the required human review of dimensions 2/3/5 is complete.

## Commands

```powershell
# Offline guardrails
.\.venv\Scripts\python.exe -m unittest discover -s tests -v

# Real provider (requires OPENAI_API_KEY in ignored .env)
.\.venv\Scripts\python.exe eval\run_golden_set.py
```

The live runner uses `run-live-<UTC>-<random ID>` filenames, so repeated runs never overwrite evidence. It automates status and schema only. `components/ai_client.py` logs privacy-minimized call metadata to ignored `eval/live_call_traces.jsonl`; it does not log full learner text, secrets, raw provider errors, or chain-of-thought.

## Human review procedure

For every `status=ok` case, two reviewers should independently inspect the exact cited PDF page and score:

1. Groundedness — every substantive claim is supported by the cited source.
2. Concept alignment — the quiz tests the concept just explained.
3. Domain correctness — especially sibling concepts in class ④.

Record disagreements and adjudication without changing the locked quality bar or deleting failed runs.