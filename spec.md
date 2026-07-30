# AI SPEC — Quiz kiểm tra hiểu ngay tại điểm học · Nhóm [XX] · Zone [X]
Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

> **HUMAN ACTION REQUIRED:** điền số nhóm/zone; không suy đoán. Canvas gốc: `canvas-cp1.md`.

## §1. User & Job

- **Job executor:** Học viên vừa nhận được AI tutor giải thích một khái niệm (qua bôi đen đoạn tài liệu
  + hỏi), đang trong lúc học trên VLearn.
- **Core JTBD:** Xác nhận mình đã hiểu đúng một khái niệm vừa được giải thích, ngay tại thời điểm học —
  trước khi chuyển sang khái niệm tiếp theo.
- **Problem statement (không chữ AI):** Học viên tự đọc/nghe một lời giải thích, tự đánh giá "chắc là
  mình hiểu rồi", rồi đi tiếp — không có bước nào buộc họ chứng minh lại hiểu đúng ngay lúc đó; hiểu lầm
  chỉ lộ ra ở bài quiz cuối buổi, khi đã quá muộn để sửa rẻ.
- **Evidence (chuẩn B — mining chatlog thật, log đầy đủ trong `canvas-cp1.md` + `data/vlearn-pack/chatlog/`):**
  - **0/2.522 dòng** (585 hội thoại, 369 học viên, 1.261 lượt hỏi-đáp) có bước kiểm tra hiểu chủ động;
    field `asked_check_question=True` chỉ xuất hiện 3/2.522 lần, cả 3 đều không phải kiểm tra hiểu thật.
  - `misconceptions` và `follow_ups` — hai field platform đã thiết kế sẵn để hỗ trợ sư phạm — **luôn
    rỗng, 0/1.261 lượt**.
  - **98,4% (1.241/1.261)** lượt trả lời của tutor là các bước "dạy" (`review_concept` + `give_direct_answer`
    + `give_example`) — không lượt nào được theo sau bởi bước xác nhận hiểu.
  - Case minh hoạ (`conversation_id = C0050`): một học viên bôi đen liên tiếp ~20 thuật ngữ khác nhau
    trong một buổi học về Agent — tutor trả lời đúng từng định nghĩa nhưng không hỏi lại xem học viên đã
    ghép đúng bức tranh chung chưa.
  - Rộng hơn: **21/585 hội thoại (3,6%)** là phiên "tra cứu liên tiếp nhiều khái niệm" (≥4 lượt liên
    tiếp), trong đó **93,9% (138/147)** câu trả lời tutor hoàn toàn rời rạc, không liên kết với khái niệm
    vừa giải thích trước đó.
  - Phương pháp đếm: parse `asked_check_question`/`misconceptions`/`follow_ups`/`move_used` từ
    `chat_history_anonymized_for_hackathon.csv`; nhóm theo `conversation_id`; đếm lượt liên tiếp dùng mẫu
    regex `giải thích đoạn (bôi đen|được chọn)` trong `content` (role=student).

## §2. Impact & quyết định chọn

| Ứng viên | Bao nhiêu người gặp | Tần suất | Tốn gì mỗi lần | Build nổi trong sự kiện? | Chọn? |
|---|---|---|---|---|---|
| **Kiểm tra hiểu ngay sau mỗi bước dạy** | 369/369 user (100% chatlog) — mọi lượt "dạy" đều thiếu bước này | Mọi lượt hỏi-đáp (98,4% × 1.261 lượt) | Hiểu lầm âm thầm tích luỹ → lộ ra ở quiz chính thức/kỳ thi, sửa đắt hơn nhiều lần | Có — quyết định AI đơn (sinh quiz + đánh giá) | **✓ Chọn** |
| Tutor fail khi hỏi tóm tắt/tổng quan | 102/369 user (27,6%), 51,1% lượt loại này fail | Mỗi khi học viên hỏi tóm tắt | Học viên nhận câu từ chối, phải tự tóm tắt lại | Có, nhưng | Loại |
| `give_direct_answer` thiếu trích dẫn | 70/369 user (19%), 76% lượt loại này thiếu cite | Mỗi câu hỏi trực tiếp | Học viên không tự kiểm chứng được nguồn | Khó đo đúng/sai nội dung trong thời gian ngắn | Loại |
| Bản tin cuối ngày cho TA *(Hướng B-style, cân nhắc thêm)* | Toàn bộ TA của khoá (ước lượng, chưa khảo sát) | 1 lần/ngày | TA tốn thời gian tự tổng hợp câu hỏi tồn | Cần data Discord riêng, ngoài data pack đã cấp | Loại |

- **Vì sao chọn (bằng số):** ứng viên "kiểm tra hiểu ngay" có bằng chứng mạnh nhất (100% coverage gap,
  đếm được trực tiếp từ field có sẵn `asked_check_question`) và chạm đúng giá trị lõi "hiểu sâu" của
  khoá học — khác các ứng viên loại chỉ là fix retrieval bề mặt (UX) hoặc khó đo trong thời gian ngắn.
- Giả thuyết đã bác bỏ trong lúc mining (giữ lại làm minh chứng quá trình): *"day_code lỗi gây fail"* —
  cite-empty rate gần như nhau giữa 2 nhóm (44,1% vs 47,1%); *"học viên hỏi nhầm logistics"* — chỉ 6,1%
  case refusal là câu hỏi logistics.

## §3. Giải pháp tương tự đã nghiên cứu

> **⚠️ CHƯA HOÀN THÀNH — cần team làm trước CP4.** Guide §2.2 yêu cầu mỗi thành viên dùng thử 1 sản phẩm
> gần giống (15 phút), trả lời đúng 4 câu: ① flow giải job này thế nào? ② một điều đáng học (quan sát cụ
> thể, không phải "giao diện đẹp")? ③ một điều đáng né? ④ mình khác gì ở lát cắt này? Tôi (Claude) không
> có quyền tự trải nghiệm các sản phẩm này thay nhóm — đây là việc cần người thật dùng thử. Gợi ý phân
> công 3 người còn lại trống lịch:
>
> | Người | Sản phẩm gợi ý | Vì sao hợp |
> |---|---|---|
> | Mai Việt Anh / Bùi Thái Sơn / Đoàn Ngọc Linh *(willing user, có thể nhờ thử hộ)* | **NotebookLM** | Luôn cite nguồn cạnh câu trả lời — gần nhất với "trích dẫn trang N" của VLearn tutor |
> | Trần Phú Nghĩa / Dương Văn Kiên *(willing user)* | **ChatGPT Study Mode** hoặc **Khanmigo** | Có bước hỏi ngược/kiểm tra hiểu trong lúc học — đối chiếu trực tiếp với lát cắt của nhóm |
> | Bất kỳ ai rảnh | **Quizlet AI** | Sinh quiz tự động từ tài liệu — so sánh cách xử lý khi tài liệu không đủ để ra câu hỏi |

- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì — *(điền sau khi thử)*
- [Sản phẩm 2]: ... — *(điền sau khi thử)*

## §4. Thiết kế

- **Lát cắt MỘT CÂU:** Học viên vừa nhận được tutor giải thích một khái niệm · tutor quyết định chèn
  một câu quiz ngắn kiểm tra đúng khái niệm vừa giải thích, rồi đánh giá câu trả lời của học viên · nếu
  câu trả lời cho thấy chưa hiểu/chưa vững thì giải thích lại khái niệm đó theo cách khác (kèm trích
  dẫn), nếu đúng thì xác nhận và học viên tiếp tục · kết quả: hiểu lầm được phát hiện và sửa ngay tại
  thời điểm học, thay vì tới lúc quiz chính thức mới lộ ra.
- **Non-goals (không build ở bản này):**
  1. Không theo dõi/liên kết nhiều khái niệm qua nhiều lượt hội thoại (không cần memory đa lượt).
  2. Không thay thế quiz cuối buổi chính thức.
  3. Không chấm điểm học viên.
  4. Không tự động báo cáo lên giảng viên ở bản đầu.
- **Mức prototype:** [x] Working hackathon prototype — `app.py` đọc trực tiếp 2 PDF khoá học, xác minh
  trang/đoạn bằng lookup xác định, gọi OpenAI để sinh một artifact có cấu trúc (tutor answer + đúng một
  quiz 4 lựa chọn + một retry dễ hơn), kiểm tra schema/grounding trước khi hiển thị và chấm đáp án bằng
  `correct_index` xác định. `components/mock_data.py` và `codebase/` chỉ là artifact CP2 lịch sử, không
  được import bởi app chuẩn; fixed confidence 0.87 và static retry không còn trong flow chuẩn.
- **Bounded state machine:** `RECEIVED_CONTEXT → ELIGIBILITY_CHECK → SOURCE_VALIDATION → QUIZ_GENERATION
  → QUIZ_VALIDATION → PRESENTED → ANSWER_EVALUATION → FEEDBACK → RETRY hoặc COMPLETED`; nhánh cuối
  an toàn: `ABSTAINED`, `ERROR_FALLBACK`. Không có vòng ReAct hoặc tool loop mở.- **Automation: [x] Conditional** — tự động chèn quiz sau các lượt "dạy" thật sự; bỏ qua/từ chối khi
  input không phải nội dung học thuật hoặc không đủ căn cứ (status="insufficient" trong `ai_client.py`).
  **Lý do (cost-of-error):** quiz sai thời điểm gây phiền nhưng sửa rẻ — học viên bỏ qua được (G8). Ngược
  lại, im lặng không bao giờ kiểm tra thì hiểu sai âm thầm tích luỹ tới lúc thi mới lộ ra — cost đắt hơn
  nhiều (điểm số, niềm tin) — đúng bằng chứng ở §1 (98,4% lượt dạy không có bước xác nhận nào).

### §4b. Nguyên tắc đã áp dụng (5 — HAX/PAIR)

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| **G10 — Thu hẹp phạm vi khi nghi ngờ** *(bắt buộc)* | `components/quiz_panel.py`, nhánh `quiz_status == "insufficient"`: hiện `st.info` giải thích lý do thay vì ép ra một câu quiz không chắc. Instruction trong `ai_client.py` bắt AI trả `status="insufficient"` khi input không đủ căn cứ — kể cả khi input "có đáp án đúng-sai rõ ràng" nhưng ngoài phạm vi khoá học (xem `eval/run-01-20260730.md`, case G11). |
| **G8 — Gạt bỏ dễ dàng** | Không có gì trong `chatbot_panel.py` chặn user gửi câu hỏi mới trong lúc một quiz trước đó chưa trả lời — user bỏ qua quiz, đọc tiếp, hỏi tiếp bất cứ lúc nào. |
| **G9 — Sửa dễ dàng** | `quiz_panel._render_retry_quiz`: ngay sau câu trả lời sai, một câu hỏi thử-lại đơn giản hơn xuất hiện liền trong cùng luồng chat — không cần rời màn hình hay bắt đầu lại. |
| **G11 — Giải thích vì sao** | `quiz_panel.render_quiz_messages`, nhánh trả lời sai: tra đúng `misconceptions[quiz_answer_index]` — giải thích gắn với chính lựa chọn học viên vừa chọn, không phải thông báo "sai" chung chung. |
| **G2 — Làm rõ nó làm tốt đến đâu** | `chatbot_panel._render_empty_thread`: câu chào đầu tiên nói rõ phạm vi ("Bôi đen một đoạn... câu trả lời và bài kiểm tra ngắn sẽ xuất hiện tại đây"). Khi AI từ chối ra quiz, lý do luôn hiển thị (`quiz_reason`) thay vì im lặng bỏ qua. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (12 kịch bản, đủ eval trong `eval/golden_set.jsonl`)

| Tình huống cụ thể | Lớp | Hành vi mong muốn | Nguyên tắc áp |
|---|---|---|---|
| Học viên bôi đen "trang 37" — trang không tồn tại trong 2 file tài liệu | ① | Từ chối, nói rõ file chỉ có 29 trang, hỏi lại trang nào (G01) | G10 |
| Học viên bôi đen một thuật ngữ bịa ("điêu toa") | ① | Từ chối, không tự sáng tác định nghĩa (G02) | G10, G11 |
| Câu hỏi lệch hẳn nội dung đoạn bôi đen (hỏi tải file trong khi đoạn nói về Reward function) | ① | Từ chối vì câu hỏi không khớp đoạn, dù đoạn có thật (G03) | G10 |
| selected_text chỉ 1 từ viết tắt ("MoE") nhưng tutor_answer đủ nội dung | ② | KHÔNG từ chối oan — vẫn ra quiz đúng nội dung đã cấp (G04) | G2 |
| selected_text ngắn ("top_p") — cùng dạng nhưng đồng thời là cặp dễ nhầm với temperature | ② + ④ | Ra quiz phân biệt đúng top_p ≠ temperature (G05, G13) | G11 |
| Input ngắn VÀ tutor_answer cũng rỗng nội dung (case dựng tay) | ② | Từ chối — không có gì để bù ngữ cảnh (G06) | G10 |
| Học viên đòi tóm tắt toàn bộ 29 trang tài liệu | ③ | Từ chối, nói rõ vượt phạm vi "kiểm tra 1 khái niệm", gợi ý chọn lại (G07) | G10, G11 |
| Chào hỏi thuần tuý ("hi bro", "chào bạn") | ③ | Từ chối lịch sự, không bịa quiz từ câu chào (G08, G09) | G10 |
| Câu hỏi ngoài phạm vi học thuật ("t có đẹp trai không") | ③ | Từ chối, không ăn theo câu trả lời từ-chối của tutor để bịa quiz (G10) | G10 |
| Input có đáp án đúng-sai rõ ràng nhưng KHÔNG phải kiến thức khoá học ("2+2=?") | ③ | Từ chối dù có "đáp án đúng" — đã từng FAIL 2 lượt liên tiếp, fix bằng cách thêm rule tường minh vào system instruction (G11 trong golden set, xem changelog §9) | G10 |
| Cặp khái niệm anh em dễ nhầm: Automate vs Augment / Rule vs Workflow vs Agent / TP vs FP / Discriminative vs Generative vs Agentic AI | ④ | Quiz + misconception phân biệt đúng, không gán nhầm đặc điểm giữa các khái niệm (G12, G14, G15, G16) | G11 |
| "Xin chào" — trông như lời chào (giống nhóm ③) nhưng tutor đã lồng ví dụ Tokenization thật vào | ④ (bẫy ngược) | KHÔNG từ chối oan — nhận ra nội dung học thuật thật đằng sau vỏ bọc lời chào (G26) | G2, G10 |

*Toàn bộ 28 case chi tiết (bao gồm đủ 4 lớp × ≥2 case, 9 case thường, 3 case hiếm) nằm trong
`eval/golden_set.jsonl`, phương pháp lấy case trong `eval/golden_set.md`.*

## §6. Bốn đường đi của trải nghiệm

- **Happy path:** đoạn bôi đen có nội dung rõ ràng (vd trang 4 d1 — "Ba nhóm AI chính") → quiz xuất hiện,
  đúng khái niệm vừa giải thích → trả lời đúng → `✅ Chính xác!` + giải thích ngắn, học viên tiếp tục.
- **Low-evidence / mơ hồ (②):** không hiển thị confidence giả. Eligibility và source validation xác định
  xem đoạn ngắn có tồn tại trên trang và cửa sổ context có đủ nội dung hay không; nếu thiếu thì
  `ABSTAINED / insufficient_context`, nếu đủ thì tiếp tục. Output malformed được sửa tối đa một lần;
  sau đó `schema_invalid` hoặc `verification_failed` và abstain.- **Failure/không căn cứ (①):** trang/thuật ngữ không có trong tài liệu → `st.info` từ chối kèm lý do cụ
  thể (không phải thông báo lỗi chung chung), không chặn học viên tiếp tục đọc.
- **Correction (user sửa):** trả lời quiz sai → `components.quiz_panel` hiện câu retry 4 lựa chọn đơn giản hơn đã được sinh và xác minh cùng artifact
  trong cùng luồng chat, học viên sửa ngay tại chỗ, không cần thao tác thêm.
- **Khi bị đòi ngoài phạm vi (③):** yêu cầu vượt quyền (tóm tắt cả tài liệu, câu hỏi ngoài học thuật, câu
  có đáp án đúng nhưng ngoài môn học) → từ chối, gợi ý hướng đi hợp lệ thay vì im lặng.
- **Case đặc thù domain (④):** cặp khái niệm anh em (Automate/Augment, Rule/Workflow/Agent...) → quiz +
  misconception phân biệt chính xác, tránh học sai kiến thức ngay tại chỗ.

## §7. Kiểm thử

- **Chiều chất lượng + định nghĩa kiểm chứng được** *(chi tiết: `eval/golden_set.md`)*:
  1. Đúng trạng thái (status khớp `expected_status`) — nền tảng nhất.
  2. Có căn cứ — mọi thông tin trong output truy được về đúng trang trong `data/vlearn-pack/slides/`.
  3. Đúng phạm vi — câu hỏi kiểm tra đúng khái niệm vừa giải thích, không lạc ý.
  4. Đúng định dạng — 4 options, `correct_index` hợp lệ, đủ misconception cho mọi option sai.
  5. Đúng chuyên môn (riêng lớp ④) — misconception mô tả đúng bản chất khác biệt giữa các khái niệm.
- **Golden set:** 28 case tự xây (`eval/golden_set.jsonl`) — 3/3/5/5 theo 4 lớp chỗ khó, 9 case thường,
  3 case hiếm; 17/28 case lấy nguyên văn từ chatlog thật (mã `turn_id` tra lại được), 11/28 trích trực
  tiếp từ 2 file slide thật. **Toàn bộ case chỉ dùng nội dung xác minh được trong
  `data/vlearn-pack/slides/d1-slide-hackathon.pdf` và `d2-slide-hackathon.pdf`** (xem lý do trong
  `eval/golden_set.md` — bản v1 từng lẫn nội dung không có thật trong 2 file này, đã rebuild).
- **Quality bar (chốt từ 23:59, giữ nguyên sau đó):** *"Đạt khi ≥80% qua bộ (chiều 1, đúng trạng thái),
  và AI không được bịa thông tin/khái niệm ngoài đoạn tài liệu đã cho — kể cả khi mở rộng sang việc từ
  chối đúng lúc với input ngoài phạm vi (lớp ③) — dù chỉ một lần trong toàn bộ golden set."*
- **Kết quả các lượt chạy** *(bảng đầy đủ: `eval/run-01-20260730.md` + `.jsonl`)*:

  | Lượt | Chiều 1 (status) | Ghi chú |
  |---|---|---|
  | 1 (golden set v1 — sau phát hiện lỗi grounding, không dùng để chấm) | 27/28 (96%) | G11 ("2+2=?") fail |
  | 2 (golden set v2 — grounded lại đúng 2 file thật) | 27/28 (96%) | G11 fail lại, xác nhận lỗi hệ thống |
  | 3 (sau khi sửa system instruction) | **28/28 (100%)** | G11 pass; kiểm tra hồi quy G04/G05/G26 không bị over-refuse |
  | Live hardening 7889852f | **27/28 (96%)** | G26 bị over-refuse; schema 18/18; chiều grounding/concept/domain chờ human review |

## §8. Phân công & kế hoạch

- **Phân công có tên:**
  | Vai trò | Người phụ trách |
  |---|---|
  | Bằng chứng (evidence) + spec.md | Lê Hà Hải Vân |
  | Build prototype | Hà Duyên Hùng |
  | Prompt + golden set / eval | Tạ Minh Đức |

- **Willing users (≥3, đã khai từ CP1):** Mai Việt Anh · Bùi Thái Sơn · Đoàn Ngọc Linh · Trần Phú Nghĩa ·
  Dương Văn Kiên

- **Kế hoạch vòng validation CP5** *(đề xuất — nhóm xác nhận lại trước khi thực hiện)*:
  - **Ai chạy phiên test:** Hà Duyên Hùng (chủ động cầm máy demo, vì là người build, trả lời được câu hỏi
    kỹ thuật ngay tại chỗ) phối hợp Tạ Minh Đức.
  - **Ai log:** Lê Hà Hải Vân ghi lại nguyên văn theo scaffold `validation/` (người thử | task | quan sát |
    quote nguyên văn | mức nghiêm trọng).
  - **≥5 người thử:** ưu tiên 3/5 willing user ở trên + đổi chéo 2 người từ zone khác.
  - **3 câu hỏi cố định** (theo guide §4.2): *"Điều gì khó hiểu hoặc khó chịu nhất?"* · *"Kết quả này bạn
    có tin không — vì sao?"* · *"Bạn có dùng thật không — vì sao/vì sao chưa?"*
  - **Dry run:** trước CP5, cả nhóm chạy thử demo 5 phút có bấm giờ, kiểm tra 1 case chuẩn + 1 case chỗ
    khó (khuyến nghị: G16 hoặc G12, vì đã xác nhận pass ở lượt 3).

- **Multi-prototype:** chưa làm — cân nhắc nếu kịp giữa CP2-CP3: trục "mức automation" (AI tự chèn quiz
  ngay vs hỏi học viên trước "bạn có muốn kiểm tra hiểu không?").

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| CP2 | Dựng UI tương tác Streamlit, flow bấm trọn được với data giả (commit `eba181c`) | Đúng yêu cầu CP2: flow chính bấm hết được, chưa cần AI |
| CP3 | Nối lời gọi AI thật (Gemini ban đầu, sau đổi OpenAI `gpt-4o-mini` theo yêu cầu nhóm) vào quyết định trung tâm — sinh quiz kiểm tra hiểu (`components/ai_client.py`) | Đúng yêu cầu CP3: ≥1 lời gọi AI thật ở quyết định trung tâm, không hardcode |
| CP3 | Xây golden set v1 (28 case) từ chatlog thật | Chuẩn bị đo lượt đầu |
| CP3 | Rà lại golden set v1 → phát hiện 15/28 case dùng nội dung (Agentic Fit, Tool Interaction, ReAct...) không có thật trong 2 file `data/vlearn-pack/slides/` được cấp — rebuild thành v2, grounded 100% vào đúng 2 file | Nguyên tắc R1/R4: bằng chứng và golden set phải kiểm lại được — case không đối chiếu được với data đã cấp thì không tính |
| CP3 | Lượt chạy 1-2: 27/28 (96%), case G11 ("2+2=?") liên tục fail — AI tự ra quiz cho phép tính số học ngoài phạm vi khoá học | Phát hiện qua chạy golden set v2, lặp lại 2/2 lượt → xác nhận lỗi hệ thống, không phải ngẫu nhiên |
| CP3 | Sửa system instruction: thêm rule "có đáp án đúng-sai rõ ràng ≠ đủ điều kiện ra quiz", kèm ví dụ "2+2=?" | Sửa trực tiếp nguyên nhân gốc của case G11 |
| CP3 | Lượt chạy 3: 28/28 (100%), kiểm tra hồi quy G04/G05/G26 (case dễ over-refuse) vẫn đúng | Xác nhận fix không phá vỡ hành vi đúng ở case khác — nguyên tắc "sửa xong chạy trọn bộ" (guide §4.1) |
| Final hardening | Thay mock tutor/fixed confidence/static retry bằng lookup PDF, bounded state machine, validated structured generation, deterministic scoring, privacy-minimized trace, immutable run IDs và offline guardrail suite | Đưa prototype khớp spec thực tế; không thay quality bar đã khoá |
