# Golden set — quiz kiểm tra hiểu (quyết định AI trung tâm)

`golden_set.jsonl` — 28 case, chấm hàm `generate_comprehension_quiz(selected_text, tutor_answer)`
trong `components/ai_client.py`.

## Ràng buộc nguồn sự thật — CHỈ 2 tài liệu thật của khoá

Toàn bộ `selected_text`/`tutor_answer` trong bộ này **chỉ được phép bám vào nội dung thật sự có trong**:
- `data/vlearn-pack/slides/d1-slide-hackathon.pdf` — "AI & LLM Foundation" (29 trang)
- `data/vlearn-pack/slides/d2-slide-hackathon.pdf` — "Xác định bài toán cho AI" (29 trang)

Số trang trích trong mỗi case là **vị trí trang trong 2 file này** (1-29), không phải số trang gốc in ở
footer một số slide (vd "DAY 02 · 45/83") — footer đó là số trang của bộ slide gốc 83 trang, còn file
hackathon chỉ trích 29 trang. Cách kiểm lại: mở đúng 2 file trên, dùng `pypdf`/đọc trực tiếp trang được
ghi trong case, đối chiếu nội dung.

**Vì sao ràng buộc này quan trọng:** rà lại golden set bản đầu (v1) phát hiện nhiều case dùng nội dung
thật từ chatlog (Agentic Fit, Tool Interaction, Long Horizon, ReAct Thought/Action/Observation, Zero-shot/
Few-shot) — những khái niệm này **không tồn tại trong 2 file slide được cấp**, mà đến từ một buổi giảng
Agent khác (có thể ngày 3+) không có trong `data/`. Dùng case như vậy để chấm "có căn cứ" (chiều 2) là
tự đánh lừa — TA sẽ không thể mở file đã cấp ra để kiểm lại. Bản v2 (hiện tại) đã loại bỏ toàn bộ case đó
và thay bằng nội dung xác minh được trong đúng 2 file.

## Phương pháp lấy case (kiểm lại được)

- **17/28 case** (`source: "chatlog:T####"`) lấy `selected_text` nguyên văn từ một lượt hỏi thật trong
  `data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv` (mã `turn_id` tra lại được) —
  nhưng chỉ giữ những turn mà **chủ đề trùng với nội dung thật có trong d1/d2** (xác minh bằng cách trích
  toàn văn cả 2 PDF qua `pypdf` rồi đối chiếu từ khoá). `tutor_answer` được viết lại cho khớp chính xác
  với câu chữ thật trên đúng trang trong file (câu trả lời gốc trong chatlog có thể trích số trang của
  bộ 83-trang gốc nên không dùng nguyên văn).
- **11/28 case** (`source: "slide:d{1,2}-p{N}"`) lấy `selected_text` trích trực tiếp từ nội dung thật của
  slide (không qua chatlog) — dùng khi cần một khái niệm/cặp dễ nhầm quan trọng nhưng không có sẵn lượt
  hỏi thật nào trùng chủ đề.
- Case class③ (ngoài phạm vi) và một phần class① (nguồn sự thật) không phụ thuộc chủ đề slide cụ thể —
  giữ nguyên từ chatlog thật vì bản chất câu hỏi (chào hỏi, đòi tóm tắt cả buổi, phép cộng, thuật ngữ bịa)
  không đổi dù đối chiếu với tài liệu nào.

## Phân bổ theo 4 lớp chỗ khó (canvas-cp1.md / 01-de-bai.md)

| Lớp | Số case | Câu hỏi cụ thể hoá cho quyết định "sinh quiz" |
|---|---|---|
| ① Nguồn sự thật | 3 (G01-G03) | Trang không tồn tại / thuật ngữ không có trong 2 file / câu hỏi lệch hẳn nội dung đoạn — quiz-gen có bịa không? |
| ② Mơ hồ/thiếu info | 3 (G04-G06) | selected_text chỉ 1 từ viết tắt (MoE, top_p) — quiz-gen có phân biệt "ngắn nhưng tutor_answer đủ" (nên ra quiz) với "ngắn và không có gì để bù" (nên từ chối) không? |
| ③ Ngoài phạm vi | 5 (G07-G11) | Chào hỏi, đòi tóm tắt cả 29 trang, phép cộng — quiz-gen có từ chối thay vì cố ra quiz vô nghĩa không? |
| ④ Đặc thù domain | 5 (G12-G16) | Các cặp/bộ khái niệm thật trong slide dễ nhầm: Discriminative/Generative/Agentic AI (3 nhóm, trang 4) · temperature/top_p (trang 29) · Rule/Workflow/Agent (trang 18) · Automate/Augment (trang 17, d2) · TP/FP (trang 22, d2) |
| Thường | 9 (G17-G25) | Case giải thích rõ ràng có căn cứ thật trong slide — quiz có bám sát, không bịa thêm không? |
| Hiếm | 3 (G26-G28) | "Xin chào" bẫy ngược (nội dung Tokenization thật lồng bên trong, trang 13) · danh sách 4 anti-pattern (trang 7, d2) · thang 4 mức độ agent (trang 23, d1) |

## 5 chiều chất lượng — định nghĩa kiểm chứng được

Chấm từng case theo 5 chiều pass/fail (2 người chấm độc lập, so sánh trên ≥5 case khó trước khi chốt
định nghĩa — theo guide §2.6.4):

1. **Đúng trạng thái (status match)** — `status` trả về khớp `expected_status`. *(nền tảng nhất)*
2. **Có căn cứ (grounded)** — case `status=ok`: mọi thông tin trong output truy được về **đúng trang đã
   ghi trong `source`, trong 1 trong 2 file PDF** — mở file ra đối chiếu trực tiếp được.
3. **Đúng phạm vi (on-concept)** — câu hỏi kiểm tra đúng khái niệm vừa giải thích, không lạc ý (quan
   trọng với G27-G28 có nhiều ý trong 1 đoạn).
4. **Đúng định dạng (valid schema)** — đúng 4 options, `correct_index` hợp lệ (0-3), có `misconceptions`
   cho mọi option sai.
5. **Đúng chuyên môn (domain-correct)** — riêng nhóm lớp ④: misconception phải mô tả đúng bản chất khác
   biệt giữa các khái niệm anh em, không chỉ nói "sai".

## Quality bar — đề xuất (nhóm cần chốt số cuối trong spec.md trước 23:59 N1)

Đề xuất ban đầu: **Đạt khi ≥80% case pass chiều 1 VÀ ≥90% trong số case `status=ok` pass đồng thời cả
chiều 2+3+4** — chiều 1 là hard gate vì lớp ①③ (bịa/vượt phạm vi) là failure mode nguy hiểm nhất theo đề
bài. Một khi ghi vào spec.md thì giữ nguyên, không đổi khi thấy kết quả thấp.

## Cách chạy

`python eval/run_golden_set.py` (cần `OPENAI_API_KEY` trong `.env`) — tự động chấm chiều 1 (status) +
chiều 4 (schema), ghi bảng đầy đủ vào `eval/run-0N-YYYYMMDD.md/.jsonl`. Chiều 2/3/5 đọc tay theo bảng
trên, đối chiếu trực tiếp với đúng trang trong `data/vlearn-pack/slides/`.
