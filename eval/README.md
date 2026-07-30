# eval/

- `ai_call_log.jsonl` — auto-generated trace of every real Gemini call from
  `components/ai_client.generate_comprehension_quiz` (one JSON line per call:
  input text, raw model output, status, latency). This is the CP3 evidence
  that the AI call is real and not hardcoded.
- `golden_set.*` — the ≥20 hand-built test cases (guide §2.6 / rubric R4), to
  add next: ≥2 per lớp chỗ khó (①②③④) + 8-10 case thường + 2-4 case hiếm,
  ≥10 derived from the real chatlog.
- Each eval run (`chạy trọn bộ → bảng % → sửa → chạy lại`) gets its own
  results file here, kept even when a run fails the quality bar.
