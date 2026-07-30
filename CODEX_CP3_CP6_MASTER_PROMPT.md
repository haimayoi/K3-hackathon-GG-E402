# MASTER PROMPT CHO CODEX CLI — HOÀN THÀNH CHECKPOINT 3, 4 VÀ CHUẨN BỊ CHECKPOINT 5, 6

Bạn đang làm việc trực tiếp tại **root của repo hiện tại**. Hãy thực hiện công việc tuần tự, có kiểm thử, có log và report sau từng mốc nhỏ. Không hỏi lại người dùng nếu có thể suy luận hợp lý từ repo; khi thiếu dữ liệu con người như tên thành viên hoặc feedback thật, dùng placeholder rõ ràng và ghi thành blocker, tuyệt đối không bịa.

## 0. Bối cảnh và mục tiêu sản phẩm

Repo là prototype Streamlit cho hướng A — VLearn. Luồng hiện có:

1. Học viên xem slide PDF.
2. Học viên bôi đen một đoạn và nhập câu hỏi trong popup.
3. Câu hỏi được chuyển sang chat thread bên phải.
4. Chatbot trả lời dựa trên đoạn được chọn.
5. Hệ thống đưa ra quiz ngắn để kiểm tra học viên có thật sự hiểu câu trả lời hay không.
6. Nếu học viên trả lời sai, hệ thống giải thích đúng misconception và cho một câu kiểm tra lại đơn giản hơn.

**Lát cắt làm việc mặc định:**

> Khi một học viên đang đọc slide và hỏi về đoạn vừa bôi đen, hệ thống quyết định câu trả lời có đủ căn cứ để giải thích và tạo quiz kiểm tra hiểu hay không, để học viên nhận ra mình đã hiểu thật hay chỉ đọc lướt câu trả lời.

Không mở rộng sang LMS hoàn chỉnh, đăng nhập, database, analytics dashboard, upload nhiều loại tài liệu, chatbot đa môn học hoặc redesign toàn bộ giao diện.

## 1. Các file bắt buộc phải đọc trước khi sửa code

Đọc theo đúng thứ tự và ghi tóm tắt vào report audit:

1. `README.md`
2. `01-de-bai.md`
3. `02-guide.md`, đặc biệt §2.3–§2.7, §3, §4, §5
4. `03-template-ai-spec.md`
5. `04-rubric.md`, đặc biệt checklist CP3–CP6
6. `STREAMLIT_LEARNING_CHATBOT_FLOW.md`
7. `app.py`
8. Toàn bộ `components/`
9. `requirements.txt`
10. `data/vlearn-pack/README.md`
11. `data/vlearn-pack/chatlog/DATA_DICTIONARY.md`
12. Chỉ đọc CSV bằng script cục bộ, không copy toàn bộ nội dung ra report hoặc prompt ngoài.

Sau khi đọc, xác nhận bằng code và report các điểm hiện trạng sau, không chỉ tin mô tả:

- UI CP2 đã có document viewer, bôi đen text, popup nhập câu hỏi, chat thread và quiz.
- `components/chatbot_panel.py` hiện lấy answer/quiz từ `components/mock_data.py`.
- Confidence hiện là số hardcode và không phải bằng chứng đáng tin để quyết định user đã hiểu.
- Chưa có AI provider thật, trace AI, golden set, eval run, `spec.md`, `eval/`, `validation/`, `reflection/`.
- Kiểm tra sự không khớp giữa tên file ZIP/repo, branch hiện tại và thông tin thành viên; chỉ ghi nhận, không tự sửa tên người.

## 2. Quy tắc vận hành bắt buộc

1. Làm tuần tự theo các milestone bên dưới. Không nhảy sang CP4 nếu CP3 chưa có report rõ trạng thái.
2. Sau mỗi milestone nhỏ:
   - chạy kiểm thử phù hợp;
   - ghi command đã chạy, kết quả, file thay đổi, lỗi còn tồn tại;
   - tạo một report Markdown riêng;
   - chạy `git diff --check`;
   - ghi `git status --short` vào report.
3. Tạo cấu trúc log:

```text
project_logs/
├── command-history.log
├── decisions.md
└── checkpoints/
    ├── CP3/
    └── CP4/
```

4. Mỗi report dùng mẫu:

```markdown
# [Mã milestone] — [Tên]
- Thời điểm:
- Mục tiêu:
- Hiện trạng trước khi làm:
- Thay đổi đã thực hiện:
- File thay đổi:
- Command/test đã chạy:
- Kết quả:
- Bằng chứng/đường dẫn artifact:
- Vấn đề còn lại:
- Trạng thái: PASS | PARTIAL | BLOCKED
- Bước tiếp theo:
```

5. Không dùng `git add .`. Nếu tạo commit, chỉ stage đúng file của milestone. Không commit `.env`, API key, `__pycache__`, `.venv`, raw data copy hoặc log chứa dữ liệu nhạy cảm.
6. Không sửa nội dung đề bài/rubric gốc (`01-de-bai.md` đến `04-rubric.md`) trừ khi có lỗi kỹ thuật rõ ràng; coi chúng là source of truth.
7. Không xóa hoặc thay toàn bộ custom document selector đang hoạt động. Chỉ sửa tối thiểu để truyền thêm metadata như số trang.
8. Không làm đẹp UI thêm trước khi CP3 đạt Definition of Done.
9. Không bịa kết quả AI, kết quả eval, khảo sát, tên người dùng thử hoặc quote validation.
10. Nếu thiếu API key, vẫn hoàn thiện code, golden set và runner; đánh dấu đúng `BLOCKED_BY_API_KEY`, ghi command chính xác người dùng cần chạy sau khi cấu hình key. Không được tạo kết quả giả.
11. Data pack chỉ dùng cục bộ. Artifact nộp repo chỉ được chứa mã `turn_id`/`conversation_id`, thống kê tổng hợp và trích đoạn rất ngắn cần thiết.
12. Giữ prototype ở mức **Mock có AI thật ở lõi**, không tuyên bố Working nếu chưa chạy end-to-end ổn định trên dữ liệu thật.

---

# PHẦN A — CHECKPOINT 3: AI THẬT + GOLDEN SET + ĐO LƯỢT ĐẦU

## CP3.0 — Audit repo và baseline

### Công việc

- Tạo `project_logs/checkpoints/CP3/00-repo-audit.md`.
- Liệt kê cây thư mục quan trọng, branch, remote, trạng thái Git và các file đang modified/untracked.
- Kiểm tra Python version.
- Tạo hoặc dùng virtual environment hiện có; không phá môi trường của người dùng.
- Cài dependency từ `requirements.txt` khi cần.
- Chạy:
  - `python -m compileall app.py components`
  - kiểm tra load được PDF mặc định và số trang;
  - smoke test import các component.
- Thêm các pattern cần thiết vào `.gitignore`: `.env`, `.env.*` nhưng giữ `.env.example`, `.venv/`, `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, log runtime không cần commit.
- Không xóa raw data pack.

### Definition of Done

- Có audit report.
- Compile/import baseline chạy được hoặc có lỗi được ghi chính xác.
- Có danh sách rõ phần mock và phần thật hiện tại.

## CP3.1 — Thiết kế contract AI có cấu trúc

### Quyết định thiết kế bắt buộc

Không dùng “LLM tự báo confidence” làm điều kiện chính. Thay bằng trạng thái có thể giải thích:

- `grounded`: đủ căn cứ trong đoạn đã chọn/trang slide, được phép trả lời và tạo quiz.
- `insufficient_context`: đoạn chọn không đủ, yêu cầu học viên chọn thêm hoặc hỏi rõ hơn; không tạo quiz.
- `ambiguous`: câu hỏi mơ hồ; hỏi lại một câu cụ thể; không tạo quiz.
- `out_of_scope`: câu hỏi ngoài phạm vi tài liệu/lát cắt; từ chối ngắn gọn và hướng dẫn bước tiếp; không tạo quiz.
- `error`: lỗi provider/parser; graceful failure, không tạo quiz.

### Schema output đề xuất

Tạo model/schema có validate nghiêm cho output AI:

```json
{
  "status": "grounded | insufficient_context | ambiguous | out_of_scope",
  "answer": "string",
  "citations": [
    {"page": 8, "quote": "trích đoạn ngắn có trong context"}
  ],
  "reason": "lý do ngắn cho trạng thái",
  "quiz": {
    "question": "string",
    "options": ["A...", "B...", "C...", "D..."],
    "correct_option_index": 1,
    "correct_explanation": "string",
    "misconception_feedback": {
      "0": "string",
      "2": "string",
      "3": "string"
    },
    "retry_question": "string",
    "retry_options": ["A...", "B..."],
    "correct_retry_option_index": 0,
    "retry_correct_explanation": "string",
    "retry_wrong_explanation": "string"
  }
}
```

Ràng buộc:

- `quiz` chỉ được có khi `status == grounded`.
- Chỉ có đúng một đáp án đúng.
- Question và answer phải dựa trên selected text/page context.
- Citation quote phải xuất hiện trong context sau normalize khoảng trắng; nếu không khớp thì coi là hard failure.
- Không hỏi lại nội dung mà selected text đã nói rõ.
- Không đưa đáp án quiz vào wording của câu hỏi.

### File mong đợi

Có thể điều chỉnh tên theo kiến trúc repo, nhưng ưu tiên:

```text
services/
├── __init__.py
├── ai_client.py
└── learning_engine.py
models/
├── __init__.py
└── learning_response.py
prompts/
└── learning_assistant.md
```

Tạo report `project_logs/checkpoints/CP3/01-ai-contract.md` và ghi rõ vì sao bỏ confidence threshold khỏi quyết định trung tâm.

## CP3.2 — Tích hợp lời gọi AI thật vào luồng hiện tại

### Provider

- Tạo adapter provider, cấu hình bằng biến môi trường.
- Ưu tiên hỗ trợ một provider thật ổn định trước; có thể chọn Gemini theo guide hoặc OpenAI-compatible nếu môi trường repo đang có key.
- Dùng các biến rõ ràng, ví dụ:
  - `LLM_PROVIDER`
  - `LLM_MODEL`
  - `GEMINI_API_KEY`
  - hoặc `OPENAI_API_KEY`, `OPENAI_BASE_URL`
  - `USE_MOCK_LLM=false`
- Tạo `.env.example` không có key thật.
- Không log key, header authorization hoặc toàn bộ environment.

### Tích hợp UI

- Sửa custom frontend tối thiểu để submission chứa thêm `page_number` của page-card chứa selection.
- `components/chatbot_panel.py` phải gọi `learning_engine` thay vì lấy answer trực tiếp từ `TEST_CASES`.
- Hiển thị spinner trong lúc gọi AI.
- Với `grounded`: hiển thị answer + citation trang + quiz.
- Với `insufficient_context`/`ambiguous`: hiển thị câu hỏi làm rõ, không có quiz.
- Với `out_of_scope`: hiển thị giới hạn và hành động tiếp theo, không có quiz.
- Với lỗi provider/parser: thông báo thân thiện và nút/thao tác thử lại; app không crash.
- Giữ `mock_data.py` chỉ làm chế độ fallback demo khi `USE_MOCK_LLM=true`, có nhãn rõ “Mock mode”. Không để mock là default khi key đã có.
- Không hiển thị confidence threshold trên UI.

### Trace tối thiểu

Tạo trace đã sanitize cho mỗi AI call:

```text
eval/traces/<timestamp-or-run-id>.json
```

Trace gồm:

- timestamp;
- provider/model;
- case/event id;
- page number;
- hash selected text;
- question;
- status;
- latency;
- parse/validation result;
- citation validation result;
- error nếu có.

Không ghi API key. Với case lấy từ data pack, ưu tiên source ID và hash/trích đoạn ngắn, không copy đoạn dài.

### Test

Tạo unit tests tối thiểu cho:

- parse JSON hợp lệ;
- reject quiz khi status không grounded;
- reject citation không nằm trong context;
- exactly one correct option;
- graceful fallback khi provider lỗi;
- page number truyền từ frontend đến learning turn.

Dùng `pytest` nếu phù hợp và bổ sung dependency cần thiết.

Tạo report `project_logs/checkpoints/CP3/02-real-ai-integration.md`.

## CP3.3 — Mining `review_concept` và tạo golden set

### Mining evidence

Tạo script:

```text
scripts/mine_review_concept.py
```

Script phải đọc trực tiếp:

```text
data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv
```

Chỉ tập trung tutor rows có `move_used == review_concept`, nhưng vẫn đối chiếu tổng dữ liệu. Tính bằng code, không copy số từ DATA_DICTIONARY:

- số tutor turn;
- số `review_concept`;
- số unique user và conversation có `review_concept`;
- tỷ lệ `asked_check_question == True` trong `review_concept`;
- tỷ lệ citation rỗng trong `review_concept`;
- số misconceptions/follow_ups được ghi nhận;
- rating up/down trong số response được rating;
- latency median, p90 và outlier;
- kiểm tra và ghi nhận nếu số liệu thực tế khác DATA_DICTIONARY.

Output:

```text
evidence/
├── mining-method.md
├── mining-summary.md
├── review-concept-counts.csv
└── review-concept-examples.md
```

`review-concept-examples.md` chứa ít nhất 5 ví dụ ngắn, có `turn_id`/`conversation_id`, không dán hội thoại dài và không có thông tin nhận diện.

### Golden set

Tạo tối thiểu **24 case** trong:

```text
eval/golden-set.jsonl
```

Cơ cấu:

- 8–10 case thường;
- ít nhất 2 case cho mỗi lớp khó ①②③④;
- 2–4 case hiếm;
- ít nhất 12 case lấy hoặc phát triển từ chatlog thật, lưu source ID;
- case từ slide PDF phải có page number/reference.

Mỗi case nên có:

```json
{
  "case_id": "GS-001",
  "source_type": "chatlog | slide | synthetic",
  "source_ref": "Txxxx hoặc page N",
  "selected_text": "context tối thiểu",
  "page_number": 8,
  "question": "...",
  "case_type": "normal | hard | rare",
  "risk_class": "normal | source_truth | ambiguity | out_of_scope | domain_specific",
  "expected_status": "grounded | insufficient_context | ambiguous | out_of_scope",
  "expected_facts": ["..."],
  "expected_citation_page": 8,
  "must_not_contain": ["..."],
  "hard_fail_conditions": ["fabricated citation", "quiz when not grounded"]
}
```

Không đưa nguyên data pack vào file. Trích context tối thiểu và source ID đủ kiểm lại.

Tạo report `project_logs/checkpoints/CP3/03-golden-set.md` với bảng kiểm cơ cấu case.

## CP3.4 — Định nghĩa eval và chốt quality bar trước lượt chạy

Tạo `eval/README.md` mô tả cách chấm. Các chiều chất lượng phải kiểm chứng được:

1. **Grounded correctness**: các fact chính khớp selected text/context.
2. **Citation validity**: đúng page và quote thật sự nằm trong context.
3. **Relevance & size**: trả lời đúng câu hỏi, không lan sang kiến thức ngoài context nếu không báo rõ.
4. **Quiz validity**: quiz đo đúng ý vừa giải thích, đúng một đáp án, distractor hợp lý.
5. **Graceful handling**: case thiếu context/mơ hồ/out-of-scope không đoán liều và không sinh quiz.
6. **Misconception repair**: feedback chỉ ra đúng điểm sai, không chỉ nói “chưa đúng”.

### Hard failures

- Bịa citation/page.
- Trả lời sai kiến thức nhưng trình bày như chắc chắn.
- Sinh quiz khi context không đủ hoặc câu hỏi ngoài phạm vi.
- Đáp án được đánh dấu đúng thực tế sai hoặc có nhiều hơn một đáp án đúng.

### Quality bar mặc định cần khóa trước run 1

Dùng bar sau nếu repo chưa có bar khác:

> Đạt khi ít nhất **80% toàn bộ golden set PASS**, đồng thời **100% case không có citation bịa** và **100% case insufficient/ambiguous/out-of-scope không sinh quiz**.

Ghi bar này vào `spec.md` draft trước khi chạy eval lần 1 và không tự hạ bar sau khi thấy kết quả.

Tạo report `project_logs/checkpoints/CP3/04-eval-definition-and-quality-bar.md`.

## CP3.5 — Chạy trọn bộ eval lần 1

Tạo runner:

```text
scripts/run_eval.py
```

Runner phải:

- đọc toàn bộ `eval/golden-set.jsonl`;
- gọi cùng learning engine mà Streamlit dùng;
- lưu output của mọi case, kể cả fail/error;
- chạy structural checks và hard-failure checks;
- hỗ trợ phần đánh giá theo rubric bằng rule rõ ràng hoặc evaluator có structured output;
- không silently skip case;
- tính tổng PASS/FAIL/ERROR và %;
- so sánh với quality bar đã khóa;
- ghi latency và model;
- có thể resume nhưng summary cuối phải phản ánh đủ toàn bộ set.

Output:

```text
eval/runs/run-001/
├── results.jsonl
├── results.csv
├── summary.md
├── failures.md
└── config.json
```

Nếu không có API key:

- không tạo output giả;
- tạo `eval/runs/run-001/BLOCKED_BY_API_KEY.md`;
- report phải ghi CP3 là PARTIAL/BLOCKED;
- cung cấp command chạy lại sau khi key được cấu hình.

Sau run 1, chỉ phân tích failure đau nhất, chưa cần sửa nhiều feature. Ghi:

- failure phổ biến nhất;
- hard failure nguy hiểm nhất;
- giả thuyết nguyên nhân;
- thay đổi nhỏ nhất nên thử ở run 2.

Tạo report `project_logs/checkpoints/CP3/05-eval-run-001.md`.

## CP3.6 — Báo cáo checkpoint 3

Tạo:

```text
project_logs/checkpoints/CP3/CP3-CHECKPOINT-REPORT.md
```

Report phải đối chiếu từng checkbox rubric:

- [ ] lời gọi AI thật, không hardcode;
- [ ] trace/log AI trong repo và đã sanitize;
- [ ] golden set ≥20, đủ case khó, ≥10 case từ chatlog thật;
- [ ] bảng kết quả đủ mọi case;
- [ ] có % và so với quality bar;
- [ ] phần mock được ghi rõ;
- [ ] app không crash ở failure path.

Mỗi checkbox phải có đường dẫn file chứng minh. Nếu thiếu key hoặc test chưa chạy, đánh dấu `[ ]`, không được đánh dấu đạt giả.

Chỉ sau khi report CP3 hoàn thành mới chuyển sang CP4.

---

# PHẦN B — CHECKPOINT 4: SPEC GẦN CUỐI + EVIDENCE + THIẾT KẾ RỦI RO

## CP4.0 — Tạo cấu trúc artifact chuẩn

Không di chuyển code vội nếu có nguy cơ làm app hỏng. Có thể giữ `app.py` và `components/` ở root, nhưng README phải ghi rõ đây là `codebase`. Tạo các folder còn thiếu:

```text
evidence/
eval/
validation/
reflection/
demo/
project_logs/
```

Tạo report `project_logs/checkpoints/CP4/00-artifact-structure.md`.

## CP4.1 — Hoàn thiện evidence chuẩn B và bảng impact

Từ output mining, tạo evidence có thể kiểm lại:

- phương pháp lọc `role == tutor` và `move_used == review_concept`;
- script và command chạy;
- số đếm;
- ít nhất 5 ví dụ ngắn có source ID;
- hạn chế/bias của dữ liệu;
- không suy diễn “user hiểu” chỉ từ việc chatbot đã trả lời.

Tạo bảng impact ít nhất 3 ứng viên, ví dụ:

1. Quiz kiểm tra hiểu sau câu trả lời `review_concept`.
2. Cải thiện grounding/citation cho câu trả lời không có nguồn.
3. Phát hiện thiếu context và hỏi lại thay vì trả lời/từ chối chung chung.

Mỗi ứng viên phải có số liệu từ script: số user/turn bị ảnh hưởng, tần suất và hậu quả. Giữ ứng viên bị loại cùng lý do định lượng. Không bịa số “thời gian tiết kiệm” nếu chưa đo; có thể ghi rõ “chưa đo” và dùng proxy phù hợp.

Tạo report `project_logs/checkpoints/CP4/01-evidence-and-impact.md`.

## CP4.2 — Viết `spec.md` theo đúng template §1–§9

Tạo `spec.md` theo `03-template-ai-spec.md`. Nội dung phải khớp code hiện tại, không viết một feature khác.

### §1 User & Job

- Job executor cụ thể: học viên đang đọc slide và dùng tutor để tóm tắt/giải thích.
- Core JTBD không có chữ AI/sản phẩm.
- Problem statement không có chữ AI.
- Evidence trỏ về `evidence/`.

### §2 Impact & quyết định chọn

- Bảng ≥3 ứng viên có số.
- Có ứng viên đã loại và lý do.
- Chọn quiz kiểm tra hiểu sau giải thích dựa trên evidence và khả năng prototype.

### §3 Giải pháp tương tự

- Chỉ ghi nhận quan sát có căn cứ.
- Nếu chưa có thành viên dùng thử sản phẩm tương tự, tạo bảng `TO VERIFY`, không giả vờ đã research.
- Gợi ý đối tượng so sánh: ChatGPT Study Mode, NotebookLM, Khanmigo, Quizlet/Duolingo; nhưng không bịa quote hoặc tính năng chi tiết chưa kiểm chứng.

### §4 Thiết kế

- Lát cắt một câu.
- Ít nhất 3 non-goals.
- Mức prototype: Mock, AI thật ở lõi, phần còn lại ghi rõ.
- Automation: **Conditional** — tự trả lời/tạo quiz khi grounded; hỏi lại/từ chối khi thiếu căn cứ.
- Lý do cost-of-error: quiz sai có thể củng cố kiến thức sai, vì vậy không automate vô điều kiện.
- Ít nhất 4 nguyên tắc HAX/PAIR, phải trỏ vị trí cụ thể trong UI/code:
  - G1: làm rõ phạm vi ngay empty state/chat heading;
  - G2: nêu answer dựa trên trang/đoạn nào;
  - G10: thiếu context thì thu hẹp/hỏi lại, không sinh quiz;
  - G9 hoặc G11: user có thể hỏi lại và thấy citation/reason;
  - G15 nếu có feedback chi tiết.

### §5 Kiểu lỗi — ít nhất 8 kịch bản, phủ 4 lớp

Tối thiểu 2 case/lớp:

1. **Nguồn sự thật:** selected text không chứa câu trả lời; citation quote không tồn tại; PDF page không extract được.
2. **Mơ hồ/thiếu thông tin:** chọn nhiều chủ đề; hỏi “cái này là gì?”; selection quá ngắn; đại từ không rõ.
3. **Ngoài phạm vi/thẩm quyền:** hỏi đáp án bài kiểm tra; hỏi nội dung ngoài tài liệu; yêu cầu kết luận không có căn cứ.
4. **Đặc thù domain học tập:** quiz có nhiều đáp án đúng; đáp án đúng bị gắn sai; feedback củng cố misconception; câu quiz chỉ kiểm tra nhớ câu chữ chứ không kiểm tra hiểu.

Mỗi dòng phải có tình huống, lớp, hành vi mong muốn, nguyên tắc áp dụng và golden-set case ID.

### §6 Bốn đường đi

Mô tả đúng hành vi đã có trong app:

- happy path;
- low-confidence/ambiguous path, nhưng không dùng số confidence tự báo;
- failure/no-grounding path;
- correction path khi user hỏi lại hoặc trả lời quiz sai;
- out-of-scope và domain-specific case.

### §7 Kiểm thử

- Trỏ về `eval/golden-set.jsonl` và run 001.
- Đưa quality bar đã khóa.
- Ghi kết quả trung thực, kể cả thấp hoặc blocked.

### §8 Phân công & kế hoạch

- Không tự bịa tên thành viên.
- Tìm tên/mã học viên từ README, branch hoặc file hiện có; nếu không chắc, dùng `[CẦN ĐIỀN]`.
- Tạo bảng phân công spec/evidence/prompt/code/demo.
- Willing users phải là placeholder nếu chưa có tên thật.

### §9 Changelog

- Ghi các thay đổi từ CP2 đến CP4, trỏ về failure/evidence.

Tạo report `project_logs/checkpoints/CP4/02-spec-draft.md`.

## CP4.3 — Đồng bộ README và tài liệu chạy dự án

Cập nhật root `README.md` theo hướng project submission nhưng không làm mất source-of-truth của ban tổ chức. README cần có:

- tên tính năng và lát cắt;
- trạng thái CP1–CP6;
- thành viên/mã học viên/phân công, placeholder nếu chưa chắc;
- phần nào real, phần nào mock;
- cấu trúc repo;
- cách tạo môi trường và chạy Streamlit;
- cách cấu hình `.env`;
- cách chạy unit tests;
- cách chạy mining và eval;
- đường dẫn CP3/CP4 report;
- cảnh báo data privacy;
- known limitations.

Kiểm tra naming mismatch giữa ZIP, branch và README; ghi cảnh báo để người dùng quyết định, không tự gán danh tính.

Tạo report `project_logs/checkpoints/CP4/03-readme-and-runbook.md`.

## CP4.4 — Soát rubric và đóng checkpoint 4

Tạo:

```text
project_logs/checkpoints/CP4/CP4-CHECKPOINT-REPORT.md
```

Đối chiếu:

- [ ] evidence chuẩn A/B có log và script kiểm lại;
- [ ] bảng impact ≥3 ứng viên;
- [ ] có ứng viên đã loại;
- [ ] 4 lớp cụ thể;
- [ ] ≥8 kịch bản;
- [ ] ≥4 nguyên tắc có vị trí áp dụng;
- [ ] quality bar bằng số và đã khóa trước run;
- [ ] spec đủ §1–§9;
- [ ] danh sách việc còn thiếu trước CP5;
- [ ] `git diff --check` pass;
- [ ] unit tests/compile pass hoặc lỗi được ghi trung thực.

Chạy security scan đơn giản:

- tìm chuỗi giống API key/token trong tracked/untracked files;
- xác nhận `.env` không được stage;
- xác nhận không có bản copy data pack mới trong artifact nộp.

Không tự chỉnh quality bar sau kết quả run 1.

---

# PHẦN C — LẬP SẴN KẾ HOẠCH CHECKPOINT 5 VÀ 6

Không bịa validation hoặc tuyên bố dry run đã làm. Chỉ tạo plan/template sẵn dùng.

## CP5 — Validation + changelog + dry run

Tạo:

```text
validation/
├── README.md
├── session-script.md
├── feedback-log.csv
├── feedback-summary-template.md
└── consent-and-privacy-note.md

demo/
├── dry-run-checklist.md
└── timing-sheet.md

project_logs/checkpoint-plans/CP5-PLAN.md
```

`CP5-PLAN.md` phải có timeline tuần tự:

1. Freeze feature sau CP4; chỉ sửa bug/failure có bằng chứng.
2. Chọn ≥5 người ngoài nhóm, ưu tiên ≥2 willing users đã khai.
3. Mỗi phiên 10 phút: giao task, im lặng quan sát, hỏi đúng 3 câu theo guide.
4. Log tên/vai, task, quan sát, quote nguyên văn, severity.
5. Tổng hợp pattern lặp.
6. Chọn 1–2 thay đổi nhỏ có impact cao.
7. Cập nhật `spec.md` §9 changelog.
8. Chạy lại toàn bộ golden set sau thay đổi thành `run-002`.
9. So sánh run 001 và run 002, không đổi quality bar.
10. Chuẩn bị slide final và dry run 5 phút có bấm giờ.
11. Kiểm tra ngẫu nhiên mỗi thành viên giải thích được phần có tên mình.

Tạo checklist xác minh CP5 đúng rubric, nhưng để unchecked cho đến khi có bằng chứng thật.

## CP6 — Demo 5 phút + Q&A

Tạo:

```text
demo/
├── slide-outline-6-pages.md
├── demo-script-5-minutes.md
├── live-cases.md
├── judge-card-backup-cases.md
├── qa-prep.md
└── backup-plan.md

reflection/
└── TEMPLATE.md

project_logs/checkpoint-plans/CP6-PLAN.md
```

Nội dung demo phải bám đúng 6 slide trong guide:

1. User & Job — có số evidence.
2. Vì sao chọn — impact 3 ứng viên + ứng viên loại.
3. Giải pháp + live demo — 1 happy case và 1 hard/failure case.
4. Kết quả đo — % so với bar + failure lớn nhất.
5. User thật nói gì — chừa placeholder cho ≥2 quote thật và thay đổi đã làm.
6. Nếu thêm 1 tuần — 2–3 việc bám failure/feedback, không roadmap dài.

`demo-script-5-minutes.md` phải chia thời gian tổng tối đa 5 phút và có phần nói cho từng thành viên bằng placeholder tên.

`live-cases.md` phải chọn:

- một case grounded ổn định từ slide;
- một case thiếu context/mơ hồ/out-of-scope để chứng minh graceful failure;
- không dùng cả hai case happy path.

`backup-plan.md` gồm screenshot/video ngắn, output mẫu đã log và phương án khi API/network hỏng. Không tạo video giả; chỉ checklist cách tạo.

`qa-prep.md` phải chuẩn bị câu trả lời cho:

- Vì sao conditional, không automate toàn bộ?
- Failure nguy hiểm nhất?
- Confidence được xác định thế nào và vì sao không tin self-reported confidence?
- Golden set lấy từ đâu?
- Có data leakage không?
- Vì sao quiz chứng minh hiểu hơn việc chỉ đọc answer?
- Nếu quiz do AI sinh sai thì sao?
- Phần nào real, phần nào mock?
- Nếu kết quả dưới quality bar thì ship/limited/hold?

---

# PHẦN D — KIỂM TRA CUỐI VÀ KẾT QUẢ CODEX PHẢI TRẢ VỀ

Sau khi hoàn tất, chạy tối thiểu:

```bash
python -m compileall app.py components services models scripts
pytest -q
git diff --check
git status --short
```

Nếu Streamlit đã cài, chạy smoke test headless hoặc ít nhất import app và load PDF. Nếu có API key, chạy một real AI smoke case và toàn bộ eval run 001.

Tạo báo cáo tổng:

```text
project_logs/FINAL-STATUS-CP3-CP6.md
```

Báo cáo cuối phải có:

1. Tóm tắt repo trước/sau.
2. Danh sách file tạo/sửa.
3. CP3 PASS/PARTIAL/BLOCKED và bằng chứng.
4. CP4 PASS/PARTIAL/BLOCKED và bằng chứng.
5. CP5 plan đã tạo, việc nào cần con người.
6. CP6 plan đã tạo, việc nào cần con người.
7. Test result.
8. API/provider/model dùng thật hoặc blocker.
9. Quality bar và kết quả run 001.
10. 5 rủi ro còn lại ưu tiên cao nhất.
11. Các placeholder bắt buộc người dùng điền.
12. Đề xuất commit message theo từng nhóm file.

Trong phản hồi cuối của Codex CLI, không chỉ nói “done”. Hãy in:

- trạng thái từng milestone;
- đường dẫn các report quan trọng;
- lệnh chạy app;
- lệnh chạy eval;
- blocker cần người dùng xử lý;
- tuyệt đối không in API key hoặc raw data dài.
