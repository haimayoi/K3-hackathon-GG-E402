# Canvas CP1 — Nhóm [XX] · Zone [X]

## 1. Hướng
**A — VLearn** · Loại: **Tính năng mới**

## 2. Job executor
Học viên vừa nhận được AI tutor giải thích một khái niệm (qua bôi đen đoạn tài liệu + hỏi), đang trong lúc học trên VLearn.

## 3. Pain — một câu
Tutor giải thích xong **không bao giờ** kiểm tra xem học viên có thực sự hiểu đúng hay không: **0/2.522 lượt** trong toàn bộ chatlog có bước kiểm tra hiểu chủ động, trong khi **98,4% (1.241/1.261)** lượt trả lời của tutor là các bước "dạy" (giải thích khái niệm / trả lời trực tiếp / cho ví dụ) — đáng lẽ mỗi bước dạy như vậy cần được xác nhận lại.

## 4. Bằng chứng đầu (mining chatlog thật — chuẩn B)

**Số đếm được:**
- Toàn bộ 2.522 dòng (585 hội thoại, 369 học viên, 1.261 lượt hỏi-đáp): chỉ **3/2.522** lượt có field `asked_check_question=True` — và cả 3 đều **không phải** kiểm tra hiểu chủ động thật sự (1 do học viên tự gõ "TẠO QUIZ...", 1 do input rác "asds", 1 do retrieval fail bị gắn nhãn nhầm).
- `misconceptions` và `follow_ups`: **luôn rỗng (0/1.261)** — hai field được thiết kế để hỗ trợ sư phạm nhưng chưa từng được dùng.
- `move_used` = `review_concept` (1.074) + `give_direct_answer` (146) + `give_example` (21) = **1.241/1.261 (98,4%)** lượt là các bước "dạy" — không lượt nào được theo sau bởi bước xác nhận hiểu.
- Case minh hoạ cụ thể (`conversation_id = C0050`): một học viên bôi đen **liên tiếp ~20 thuật ngữ khác nhau** trong cùng buổi học về Agent/ReAct (Agentic Fit, Tool Interaction, Function Calling, Conditional Edge, Perception, parse, fine-tune, eval...) — tutor trả lời đúng định nghĩa từng thuật ngữ nhưng không hề hỏi lại xem học viên đã ghép đúng bức tranh chung chưa.
- Rộng hơn: **21/585 hội thoại (3,6%)** là phiên "tra cứu liên tiếp nhiều khái niệm" (≥4 lượt liên tiếp, ≥50% dùng đúng mẫu "giải thích đoạn bôi đen") — trong đó **93,9% (138/147)** câu trả lời của tutor hoàn toàn rời rạc, không liên kết với khái niệm vừa giải thích trước đó.

**Phương pháp đếm** (để kiểm tra lại): parse cột `asked_check_question`, `misconceptions`, `follow_ups`, `move_used` từ `data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv`; nhóm hội thoại theo `conversation_id`, đếm số lượt liên tiếp dùng mẫu regex `giải thích đoạn (bôi đen|được chọn)` trong cột `content` (role=student).

**Ứng viên đã cân nhắc và loại** (giữ lại làm minh chứng quá trình):
- *Tutor fail khi hỏi tóm tắt/tổng quan* (51,1% fail, 102/369 user) — loại vì đây là fix retrieval bề mặt (UX), không chạm giá trị lõi "hiểu sâu" của khoá học.
- *`give_direct_answer` thiếu trích dẫn* (76%, 70/369 user) — loại vì khó đo đúng/sai nội dung trong thời gian ngắn.
- *Giả thuyết "day_code lỗi gây fail"* — bác bỏ, cite-empty rate gần như nhau giữa 2 nhóm (44,1% vs 47,1%).
- *Giả thuyết "học viên hỏi nhầm logistics"* — bác bỏ, chỉ 6,1% case refusal là câu hỏi logistics.

## 5. Lát cắt — MỘT CÂU
> Học viên vừa nhận được tutor giải thích một khái niệm · tutor quyết định chèn một câu quiz ngắn kiểm tra đúng khái niệm vừa giải thích, rồi đánh giá câu trả lời của học viên · nếu câu trả lời cho thấy chưa hiểu/chưa vững thì giải thích lại khái niệm đó theo cách khác (kèm trích dẫn), nếu đúng thì xác nhận và học viên tiếp tục · kết quả: hiểu lầm được phát hiện và sửa ngay tại thời điểm học, thay vì tới lúc quiz chính thức mới lộ ra.

**Non-goals** (không build ở bản này):
- Không theo dõi/liên kết nhiều khái niệm qua nhiều lượt hội thoại (không cần memory đa lượt).
- Không thay thế quiz cuối buổi chính thức.
- Không chấm điểm học viên.
- Không tự động báo cáo lên giảng viên ở bản đầu.

## 6. Automation dự kiến
**Conditional** — tự động chèn quiz kiểm tra sau các lượt "dạy" thật sự (`review_concept` / `give_direct_answer` / `give_example`); bỏ qua khi câu trả lời của tutor không phải nội dung học thuật (từ chối/logistics).

**Lý do (cost-of-error)**: quiz sai thời điểm gây phiền nhưng sửa rẻ — học viên bỏ qua được (nguyên tắc G8 — gạt bỏ dễ dàng). Ngược lại, im lặng không bao giờ kiểm tra thì hiểu sai âm thầm tích luỹ tới lúc thi mới lộ ra — cost đắt hơn nhiều (điểm số, niềm tin).

## 7. Willing users & Phân công

**Willing users (đồng ý thử prototype trước demo):**
Mai Việt Anh · Bùi Thái Sơn · Đoàn Ngọc Linh · Trần Phú Nghĩa · Dương Văn Kiên

**Phân công có tên:**
| Vai trò | Người phụ trách |
|---|---|
| Bằng chứng (evidence) + spec.md | Lê Hà Hải Vân |
| Build prototype | Hà Duyên Hùng |
| Prompt + golden set / eval | Tạ Minh Đức |
