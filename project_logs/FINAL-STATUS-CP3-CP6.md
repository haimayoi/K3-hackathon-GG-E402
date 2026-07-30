# Final status — CP3 đến CP6

- Thời điểm: 2026-07-30 (Asia/Saigon)
- Phạm vi: hoàn thiện code/artifact có thể làm tự động; không bịa API/eval/user/demo result.

## 1. Repo trước và sau

Trước: CP2 có PDF viewer 23 trang, selection popup, chat/quiz/retry nhưng answer/quiz lấy từ
components/mock_data.py, confidence hardcode; không provider/schema/trace/golden/eval/spec/
validation/reflection/demo/project logs.

Sau: giữ UI CP2, truyền page_number; thêm strict contract, Gemini adapter, learning engine,
citation validation, graceful failure/retry, trace sanitize, 14 unit tests, reproducible mining,
24-case golden set, eval runner/blocker, spec §1–§9, README runbook, CP5/CP6 templates/plans.

## 2. Trạng thái từng milestone

| Milestone | Trạng thái | Report/evidence |
|---|---|---|
| CP3.0 audit | PARTIAL | project_logs/checkpoints/CP3/00-repo-audit.md; venv install timeout nhưng global env test PASS |
| CP3.1 contract | PASS | project_logs/checkpoints/CP3/01-ai-contract.md |
| CP3.2 real-AI integration code | PASS | real smoke grounded và insufficient-context; xem BUGFIX-20260730/01-api-key-and-provider.md |
| CP3.3 mining/golden | PASS | project_logs/checkpoints/CP3/03-golden-set.md |
| CP3.4 eval definition/bar | PASS | project_logs/checkpoints/CP3/04-eval-definition-and-quality-bar.md |
| CP3.5 run 001 | PARTIAL | 24/24 case có kết quả; quality bar chưa đạt và còn ERROR do quota 429 |
| CP3.6 report | PARTIAL | project_logs/checkpoints/CP3/CP3-CHECKPOINT-REPORT.md |
| CP4.0 structure | PASS | project_logs/checkpoints/CP4/00-artifact-structure.md |
| CP4.1 evidence/impact | PASS | project_logs/checkpoints/CP4/01-evidence-and-impact.md |
| CP4.2 spec | PASS | project_logs/checkpoints/CP4/02-spec-draft.md |
| CP4.3 README/runbook | PASS | project_logs/checkpoints/CP4/03-readme-and-runbook.md |
| CP4.4 checkpoint | PASS | project_logs/checkpoints/CP4/CP4-CHECKPOINT-REPORT.md |
| CP5 prep | Artifact prep PASS; checkpoint PLAN_ONLY | project_logs/checkpoint-plans/CP5-PLAN.md |
| CP6 prep | Artifact prep PASS; checkpoint PLAN_ONLY | project_logs/checkpoint-plans/CP6-PLAN.md |

## 3. File tạo/sửa

Code/config tạo: .env.example; models/__init__.py; models/learning_response.py;
services/__init__.py; services/ai_client.py; services/learning_engine.py;
prompts/learning_assistant.md; scripts/mine_review_concept.py;
scripts/build_golden_set.py; scripts/run_eval.py; tests/conftest.py;
tests/test_learning_engine.py.

Code/config sửa: .gitignore; requirements.txt; app.py; components/chatbot_panel.py;
components/quiz_panel.py; components/document_selector_frontend/index.html. Các thay đổi CP2
có sẵn trong components/document_panel.py, components/mock_data.py, components/pdf_loader.py
được giữ, không hoàn nguyên.

Docs/artifact tạo/sửa: README.md; spec.md; evidence/*; eval/README.md;
eval/golden-set.jsonl; eval/traces/*; eval/runs/run-001/results.*; eval/runs/run-001/summary.md;
validation/*; demo/*; reflection/TEMPLATE.md; project_logs/*.

Pre-existing untracked không tự stage/copy: CODEX_CP3_CP6_MASTER_PROMPT.md, data/uploads/,
data/vlearn-pack/slides/. Raw data pack không được copy sang artifact.

## 4. Test và smoke result

- python -m compileall app.py components services models scripts: PASS.
- python -m pytest -q: PASS, 14 passed.
- PDF smoke: PASS, D1 rồi D2; mỗi file 29 trang có text.
- Streamlit AppTest: PASS; D1 → D2 không exception. Chrome CDP: 29 page-card, cuộn tới trang cuối; process smoke đã dừng.
- Golden builder/validator: PASS, 24 case, 13 chatlog; 9 normal, 12 hard, 3 rare.
- API key không được in, ghi trace hoặc stage; UI password chỉ giữ trong session.
- Trace scan: không key/header/full selected_text; trace mới ghi provider/model đúng.
- git diff --check: PASS; git status ghi trong project_logs/command-history.log và lần cuối bên dưới.

## 5. Provider, run 001 và quality bar

- Provider/model đã kiểm chứng: Gemini REST / gemini-3.5-flash.
- Real call thành công: có; smoke `insufficient_context` và `grounded` + citation + quiz đều qua validation.
- Missing-key path: PASS, structured error, không quiz, app không crash.
- Quality bar đã khóa trước run: ít nhất 80% PASS, 100% không citation bịa, 100% case
  insufficient_context/ambiguous/out_of_scope không quiz.
- Run 001: 24/24 dòng; 10 PASS, 4 FAIL, 10 ERROR do quota HTTP 429; pass rate 41.67%; bar NO.
- Không có non-grounded quiz. Có 4 case bị tính citation/page failure, gồm ERROR hạ tầng; không đổi quality bar.

## 6. Evidence chính

Script tính 1.074 review_concept trên 1.261 tutor turn, khác con số 1.072 trong
DATA_DICTIONARY; mismatch được báo, không chỉnh số. Có 326 user/524 conversation;
1/1.074 check question; 448 citation rỗng; 60 rating chia 30 up/30 down; latency median
1.747ms, p90 2.435ms, max 13.240ms. Không suy ra user hiểu hay learning gain từ các số này.

## 7. Năm rủi ro ưu tiên cao

1. Run 001 chưa đạt bar và còn 10 ERROR do quota 429; quyết định hiện tại vẫn HOLD.
2. Chưa có user validation/pre-post outcome; quiz mới là signal proxy, không chứng minh hiểu.
3. Naming workspace/branch và tên/mã/phân công chưa khớp/chưa xác nhận, ảnh hưởng submission.
4. Citation substring/schema chỉ chặn một số lỗi; 4 FAIL cần đọc tay và sửa prompt/golden expectation có bằng chứng.
5. Wheel/touch đã smoke trên Chrome desktop nhưng vẫn cần human smoke trên trình duyệt/máy demo thực tế.

## 8. Placeholder và việc con người bắt buộc xử lý

- Xác nhận tên nhóm, tên/mã từng thành viên, phân công và naming mismatch.
- Điền ít nhất 3 willing users có thật; validation ít nhất 5 người, consent và quote thật.
- Thành viên trực tiếp thử/research sản phẩm tương tự hoặc giữ TO VERIFY.
- Chờ quota Gemini hồi phục, resume 10 ERROR; phân tích 4 FAIL; sau feedback chạy run 002 toàn bộ.
- Điền %/failure thật vào slide 4, ít nhất 2 quote thật vào slide 5.
- Tạo demo-slides.pdf, screenshot/video backup thật, dry run có bấm giờ và reflection cá nhân.

## 9. Lệnh vận hành

Chạy app:

    python -m streamlit run app.py

Chạy test:

    python -m pytest -q
    python -m compileall app.py components services models scripts

Chạy mining/golden:

    python scripts/mine_review_concept.py
    python scripts/build_golden_set.py

Chạy eval thật trong PowerShell:

    $env:LLM_PROVIDER='gemini'
    $env:LLM_MODEL='gemini-3.5-flash'
    $env:GEMINI_API_KEY='YOUR_KEY'
    $env:USE_MOCK_LLM='false'
    python scripts/run_eval.py --run-id run-001 --resume --delay-seconds 6

Không ghi key vào file, log hoặc command history đã commit.

## 10. Commit messages đề xuất theo nhóm file

Chỉ stage từng file rõ ràng, không dùng git add dot và không stage data pack/.env/cache.

1. feat(ai): add grounded learning engine and Gemini adapter
2. test(eval): add strict contract tests, golden set and eval runner
3. docs(evidence): add reproducible review-concept mining and impact analysis
4. docs(spec): complete CP4 spec, README runbook and checkpoint reports
5. docs(plans): add CP5 validation and CP6 demo templates

## 11. Trạng thái kết luận

- CP3: PARTIAL / API hoạt động, nhưng eval chưa đạt bar và còn BLOCKED_BY_API_QUOTA.
- CP4: PASS về artifact/rubric prep.
- CP5: PLAN_ONLY / cần con người validation.
- CP6: PLAN_ONLY / cần con người demo, dry run và reflection.
- Prototype: AI thật đã chạy ở lõi và web smoke PASS; vẫn không khai Working vì eval bar chưa đạt.

## 12. Bugfix web 2026-07-30

| Milestone | Trạng thái | Report |
|---|---|---|
| API key/provider/structured output | PASS | `project_logs/checkpoints/BUGFIX-20260730/01-api-key-and-provider.md` |
| D1 → D2 và giao diện chọn tài liệu | PASS | `project_logs/checkpoints/BUGFIX-20260730/02-slide-order-and-ui.md` |
| Scroll đủ 29 trang | PASS | `project_logs/checkpoints/BUGFIX-20260730/03-slide-scroll.md` |
| Local runtime/import cache | PASS | `project_logs/checkpoints/BUGFIX-20260730/04-local-runtime-import.md` |

Final verification: compile PASS; `pytest -q` 14 PASS; Streamlit AppTest 0 exception;
Chrome CDP xác nhận 29 page-card và trang cuối visible. Blocker còn lại là quota eval,
quality bar, human validation, thông tin thành viên và artifact demo thật.
