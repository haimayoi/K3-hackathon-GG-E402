# Mini Hackathon AI — Batch 03

## Bài nộp hiện tại — VLearn Grounded Learning Check

Lát cắt: Khi học viên đang đọc slide và hỏi về đoạn vừa bôi đen, hệ thống quyết định có đủ
căn cứ để giải thích và tạo quiz hay cần hỏi lại/từ chối, để học viên nhận ra mức hiểu thật.

### Trạng thái checkpoint

| Mốc | Trạng thái | Bằng chứng |
|---|---|---|
| CP1 | PARTIAL / chưa có Canvas và tên willing users trong repo | spec.md §1–§2, §8 |
| CP2 | PASS ở mức flow mock bấm được | app.py, components/ |
| CP3 | PARTIAL / BLOCKED_BY_API_QUOTA + quality bar chưa đạt | project_logs/checkpoints/CP3/CP3-CHECKPOINT-REPORT.md |
| CP4 | IN PROGRESS | project_logs/checkpoints/CP4/ |
| CP5 | PLAN ONLY | project_logs/checkpoint-plans/CP5-PLAN.md |
| CP6 | PLAN ONLY | project_logs/checkpoint-plans/CP6-PLAN.md |

### Thành viên và phân công

Tên workspace và branch không khớp nên không tự suy đoán danh tính.

| Phần | Người phụ trách |
|---|---|
| Spec | [CẦN ĐIỀN TÊN + MÃ HV] |
| Evidence | [CẦN ĐIỀN TÊN + MÃ HV] |
| Prompt/eval | [CẦN ĐIỀN TÊN + MÃ HV] |
| Code | [CẦN ĐIỀN TÊN + MÃ HV] |
| Demo/validation | [CẦN ĐIỀN TÊN + MÃ HV] |

### Phần thật và phần mock

- Thật trong code: PDF extraction/render/selection, page_number, structured validation,
  citation match, Gemini REST adapter, trace sanitize, eval/mining runner.
- Đã chứng minh Gemini call thật; run 001 có đủ 24 dòng nhưng còn quota ERROR và chưa đạt bar.
- Mock: ba TEST_CASES trong components/mock_data.py chỉ dùng khi USE_MOCK_LLM=true và UI
  hiện nhãn Mock mode. Không dùng mock làm kết quả eval chính thức.
- Mức khai báo: Mock có adapter AI thật ở lõi, không phải Working.

### Cấu trúc project

| Đường dẫn | Vai trò |
|---|---|
| app.py, components/ | Codebase Streamlit và custom document selector |
| models/, services/, prompts/ | Contract, provider, learning engine và prompt |
| tests/ | Unit tests |
| evidence/ | Mining method, aggregate, examples ngắn, impact |
| eval/ | Golden set, protocol, trace sanitize, run artifacts |
| validation/, demo/, reflection/ | Template/kế hoạch CP5–CP6 |
| project_logs/ | Command history, decisions, milestone reports |

Không di chuyển app.py/components vào codebase/ vì rủi ro làm hỏng app; đây là codebase được
ghi rõ theo cho phép của master prompt.

### Cài đặt và chạy

Python 3.10 trở lên. PowerShell:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    Copy-Item .env.example .env

Điền GEMINI_API_KEY trong .env hoặc environment cục bộ; không commit .env. Ứng dụng hiện
đọc environment variables trực tiếp, vì vậy nếu dùng file .env thì cần nạp biến vào shell
hoặc công cụ chạy trước khi start.

Chạy app:

Trong web, mở **Cấu hình AI** để nhập Gemini API key cho riêng session hiện tại và chọn model.
Key không được ghi vào file hay trace. App cũng hỗ trợ `GEMINI_API_KEY` hoặc `GOOGLE_API_KEY`
từ `.env`; model mặc định hiện tại là `gemini-3.5-flash`.

    python -m streamlit run app.py

Chạy demo mock tường minh:

    $env:USE_MOCK_LLM='true'
    python -m streamlit run app.py

Chạy unit tests và compile:

    python -m pytest -q
    python -m compileall app.py components services models scripts

Chạy mining và tạo lại golden set:

    python scripts/mine_review_concept.py
    python scripts/build_golden_set.py

Chạy eval thật:

    $env:LLM_PROVIDER='gemini'
    $env:LLM_MODEL='gemini-3.5-flash'
    $env:GEMINI_API_KEY='YOUR_KEY'
    $env:USE_MOCK_LLM='false'
    python scripts/run_eval.py --run-id run-001

Nếu thiếu key, runner trả exit 2 và chỉ tạo BLOCKED_BY_API_KEY.md, không tạo bảng giả.

### Reports

- CP3: project_logs/checkpoints/CP3/CP3-CHECKPOINT-REPORT.md
- CP4: project_logs/checkpoints/CP4/CP4-CHECKPOINT-REPORT.md
- Final: project_logs/FINAL-STATUS-CP3-CP6.md

### Data privacy, naming và hạn chế

- data/vlearn-pack chỉ dùng cục bộ; không copy raw pack sang evidence/eval.
- Artifact chỉ dùng aggregate, ID ẩn danh và excerpt tối đa 180 ký tự.
- Trace lưu hash selected text, không lưu key, authorization header hay full selected text.
- Không commit .env, API key, .venv, cache hoặc runtime log.
- Workspace là DAY05_2A202601587_LeHaHaiVan nhưng branch là
  2A202601465---Ha_Duyen_Hung; chưa có tên nhóm/thành viên trong README gốc. Con người phải
  xác nhận trước khi nộp; repo không tự gán danh tính.
- Known limitations: eval chưa đạt bar và còn quota ERROR, chưa có OCR cho page ảnh, chưa có
  validation người dùng, research tương tự và demo dry run; rule-based eval là proxy và
  không thay human review.

---

## Tài liệu gốc của ban tổ chức

**SPEC → Prototype → Demo.** Đây không phải cuộc thi code — đây là cuộc thi **tư duy sản phẩm AI**.

- Thời lượng: **1,5 ngày** (một ngày build + một buổi demo)
- Nhóm: **4-5 người** · zone tối đa 5 nhóm · thi theo lớp

## Bắt đầu từ đâu?

1. Đọc **`01-de-bai.md`** để chọn hướng và hiểu tiêu chí.
2. Mở **`02-guide.md`** — hướng dẫn từng giai đoạn, đứng ở đâu đọc mục đó.
3. Viết spec theo **`03-template-ai-spec.md`** — deliverable trung tâm của cả sự kiện.
4. Đọc **`04-rubric.md`** ngay từ đầu — biết trước bài được chấm theo tiêu chí nào.

| File / thư mục | Nội dung |
|---|---|
| `01-de-bai.md` | Đề bài 3 hướng · 5 tiêu chí nghiệm thu · ràng buộc chung |
| `02-guide.md` | Hướng dẫn 5 giai đoạn: khám phá → spec → build → đo & validate → demo |
| `03-template-ai-spec.md` | Template AI Spec (nộp 23:59 ngày 1) |
| `04-rubric.md` | Rubric 100 điểm (25 nộp checkpoint + 75 chấm bài) + checklist xác minh 6 mốc |
| `data/` | Dữ liệu thật đã ẩn danh: chatlog VLearn tutor + 6 transcript bài giảng bản sạch — dùng để tìm bằng chứng và xây golden set |
| `tham-khao/` | JTBD Playbook (PDF) + worksheet JTBD đầy đủ — đọc khi muốn đào sâu |

## Lịch — 6 mốc

| Mốc | Khoá 3 | Khoá 4 |
|---|---|---|
| Khai mạc + phát đề | 09:00 ngày 1 | 14:00 ngày 1 |
| CP1 · Chốt Canvas | 10:00 ngày 1 | 15:00 ngày 1 |
| CP2 · Show được thứ bấm được | 12:00 ngày 1 | 17:00 ngày 1 |
| CP3 · AI chạy thật + đo lượt đầu | 16:00 ngày 1 | 10:30 ngày 2 |
| CP4 · Chốt tiến độ — spec nộp hạn cứng **23:59 ngày 1** | 17:30 ngày 1 | 12:00 ngày 2 |
| CP5 · Xác minh + validation + dry run | 09:00 ngày 2 | 14:00 ngày 2 |
| CP6 · Demo | 10:00 ngày 2 | 15:00 ngày 2 |

Mỗi mốc cần show gì và được xác minh thế nào: xem bảng trong `04-rubric.md`.

## Nộp bài

Một repo nhóm, cấu trúc như sau. Spec chốt lúc 23:59 ngày 1; bản hoàn chỉnh trước CP6.

```
repo/
├── README.md          ← thành viên (mã HV + tên) + phân công có tên từng phần
├── spec.md            ← AI Spec theo 03-template-ai-spec.md
├── demo-slides.pdf    ← slide 6 trang theo 02-guide.md §5.1
├── codebase/          ← prototype (ghi rõ phần nào mock)
├── eval/              ← golden set + bảng kết quả các lượt chạy
├── validation/        ← feedback log từ vòng user test
└── reflection/        ← mỗi người 1 file
```

## Chấm điểm

Tổng **100 điểm = 25 điểm nộp checkpoint + 75 điểm chấm bài nộp**. Chi tiết từng ý điểm: `04-rubric.md`.

**25 điểm nộp — mỗi checkpoint 5 điểm (CP1-CP5):** nộp đúng hạn → 5 điểm · nộp muộn → 0 điểm cho mốc đó. Mỗi thành viên nộp riêng, cả nhóm dùng chung một link repo.

**75 điểm chấm — trên artifact trong repo, mỗi con điểm trỏ về một file:**

| Khối | Điểm | Chấm trên file nào |
|---|---|---|
| R1 · Bằng chứng & impact | 15 | `spec.md` §1-§2 + log khảo sát/mining |
| R2 · Lát cắt & thiết kế | 15 | `spec.md` §4 |
| R3 · Chỗ khó & kịch bản rủi ro | 11 | `spec.md` §5-§6 |
| R4 · Kiểm thử | 15 | `spec.md` §7 + `eval/` |
| R5 · Prototype chạy được | 8 | `codebase/` + demo |
| R6 · Validation với user | 8 | `validation/` |
| R7 · Quy trình & repo | 3 | cấu trúc repo |

Ba điều nên biết trước khi làm:

- Điểm dựa trên **chuỗi quyết định và bằng chứng**, không dựa trên mức độ hoành tráng của sản phẩm.
- Kết quả đo **ghi nhận trung thực** — kể cả khi không đạt mục tiêu nhóm tự đặt — vẫn được tính đủ điểm. Số liệu bị chỉnh sửa hoặc che giấu sẽ không được tính.
- Reflection cá nhân chấm riêng theo rubric của khoá. Điểm vòng demo, chấm chéo trong zone và thưởng thêm (nếu có) theo thể lệ công bố lúc khai mạc.

## Luật chung

1. Prototype có 3 mức **Sketch / Mock / Working** — mức nào cũng bắt buộc **≥1 lời gọi AI chạy thật**.
2. **Vibe-coding rule:** dùng AI để build thoải mái, nhưng không giải thích được phần có tên mình thì phần đó 0 điểm (kiểm tra tại CP5).
3. **Quality bar** chốt tại spec.md 23:59 ngày 1 và giữ nguyên sau đó.
4. Chỉ dùng dữ liệu trong `data/` hoặc dữ liệu giả tự sinh — không dùng dữ liệu thật của người thật. Không commit API key.
5. Tuân thủ **quy định bảo mật dữ liệu** bên dưới — đây là điều kiện để được cấp data.

## Bảo mật dữ liệu được cung cấp

Dữ liệu trong `data/` là dữ liệu thật của khoá học (đã ẩn danh), cấp riêng cho hackathon này. Khi nhận data, nhóm cam kết:

1. **Chỉ dùng trong phạm vi hackathon** — cho việc tìm bằng chứng, xây golden set và build prototype. Không dùng cho mục đích khác.
2. **Không chia sẻ ra ngoài khoá học** — không đăng lên mạng xã hội, không gửi cho người ngoài, không đưa vào bất kỳ dataset hay repo công khai nào.
3. **Không commit data pack vào repo nộp bài** — repo nhóm chỉ chứa trích dẫn ngắn để minh hoạ (vài dòng); golden set trích từ data ghi rõ mã đoạn/mã hội thoại thay vì dán nguyên văn dài.
4. **Cẩn trọng khi đưa data vào công cụ ngoài** — chỉ đưa phần tối thiểu cần cho việc đang làm; lưu ý API/công cụ free tier có thể dùng dữ liệu để huấn luyện (xem `02-guide.md` §3.4).
5. **Không cố suy ngược danh tính** từ dữ liệu đã ẩn danh ([học viên], mã U/C/T/M).
6. Sau sự kiện, **xoá các bản sao data pack** khỏi máy cá nhân và các công cụ đã upload nếu ban tổ chức yêu cầu.

Vi phạm được xử lý theo quy định của khoá và có thể ảnh hưởng trực tiếp đến điểm của nhóm.
