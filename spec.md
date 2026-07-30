# AI SPEC — Kiểm tra hiểu sau giải thích · Nhóm [CẦN XÁC NHẬN]

Hướng: A — VLearn. Loại: tối ưu tính năng có sẵn.

## §1. User & Job

- Job executor: học viên đang đọc slide trong buổi học, bôi đen đoạn chưa rõ và dùng tutor
  để tóm tắt hoặc giải thích.
- Core JTBD: Hiểu đúng một khái niệm trong đoạn slide đang đọc và tự kiểm tra lại mức hiểu
  trước khi học tiếp.
- Problem statement: Khi đọc lời giải cho đoạn slide vừa chọn, học viên chưa có một bước
  ngắn để phát hiện mình đã hiểu ý hay chỉ đọc lướt, nên có thể mang hiểu lầm sang phần sau.
- Evidence chuẩn B:
  - 2.522 dòng, 1.261 tutor turn; 1.074 review_concept từ 326 user/524 conversation.
  - 1/1.074 review_concept có asked_check_question; 448/1.074 citation rỗng.
  - Misconception/follow-up được ghi nhận: 0/0.
  - Rating rất thưa: 60 review response; 30 up, 30 down.
  - Phương pháp, aggregate và 5 excerpt ID ẩn danh:
    evidence/mining-method.md, evidence/mining-summary.md,
    evidence/review-concept-counts.csv, evidence/review-concept-examples.md.
- Năm source ID minh họa ngắn: T0649, T1020, T0358, T0216, T1036.
- Giới hạn: cờ check question không chứng minh học viên hiểu; chưa có pre/post learning score
  hay khảo sát chuẩn A.

## §2. Impact & quyết định chọn

| Ứng viên | Quy mô đo được | Tần suất proxy | Hậu quả/proxy | Quyết định |
|---|---:|---:|---|---|
| Quiz kiểm tra hiểu | 1.074 turn/326 user; 1.073 turn không check | 2,05 review turn/conversation | Không có signal kiểm tra hiểu; chưa đo learning gain | Chọn |
| Grounding/citation | 448 turn, 215 user, 276 conversation | 1,62 turn/affected conversation | Thiếu đường kiểm nguồn; chưa đo citation sai | Loại khỏi feature chính, giữ làm cổng |
| Hỏi lại khi thiếu context | 178 turn proxy, 116 user, 135 conversation | 1,32 turn/affected conversation | Cần thêm context; heuristic có false positive | Loại khỏi feature chính, giữ failure path |

Chọn quiz vì opportunity 1.073 lượt lớn nhất và nối vào flow CP2. Không tuyên bố quiz đã
cải thiện điểm số. Chi tiết quyết định và bias: evidence/impact-analysis.md.

## §3. Giải pháp tương tự đã nghiên cứu

| Sản phẩm | Trạng thái | Flow/đáng học/đáng né/khác biệt |
|---|---|---|
| ChatGPT Study Mode | TO VERIFY | Chưa có thành viên xác nhận dùng thử |
| NotebookLM | TO VERIFY | Chưa có thành viên xác nhận dùng thử |
| Khanmigo | TO VERIFY | Chưa có thành viên xác nhận dùng thử |
| Quizlet hoặc Duolingo | TO VERIFY | Chưa có thành viên xác nhận dùng thử |

Không dùng bảng này làm evidence cho đến khi thành viên trực tiếp thử và ghi quan sát.

## §4. Thiết kế

- Lát cắt một câu: Khi học viên đang đọc slide và hỏi về đoạn vừa bôi đen, hệ thống quyết
  định đoạn/trang có đủ căn cứ để giải thích và tạo quiz hay phải hỏi lại/từ chối, để học
  viên phát hiện mình hiểu thật hay chỉ đọc lướt.
- Non-goals:
  1. LMS hoàn chỉnh, đăng nhập hoặc database.
  2. Analytics dashboard hay theo dõi tiến độ học tập.
  3. Upload nhiều loại tài liệu, OCR hoặc RAG đa tài liệu.
  4. Chatbot đa môn hoặc trả lời ngoài selected text/page.
  5. Tự chấm điểm chính thức hay đưa đáp án bài kiểm tra.
  6. Redesign toàn bộ giao diện CP2.
- Mức prototype: Mock có adapter AI thật ở lõi. PDF/viewer/selection/chat/quiz là flow thật;
  TEST_CASES chỉ dùng khi USE_MOCK_LLM=true. Gemini adapter và engine là code thật nhưng
  chưa có call thành công trong phiên này vì BLOCKED_BY_API_KEY; không khai Working.
- Automation: Conditional. Tự trả lời và tạo quiz chỉ khi status grounded và citation qua
  validation; insufficient_context/ambiguous thì hỏi lại; out_of_scope thì giới hạn; error
  thì không quiz và cho thử lại.
- Cost-of-error: answer hoặc quiz sai có thể củng cố kiến thức sai. Vì vậy không automate
  vô điều kiện và citation mismatch là hard failure.

### §4b. Nguyên tắc HAX/PAIR

| Nguyên tắc | Áp cụ thể |
|---|---|
| G1 — Làm rõ phạm vi | Empty state và chat heading trong components/chatbot_panel.py nói chỉ dùng đoạn/trang đã chọn |
| G2 — Làm rõ mức tin | Mỗi grounded answer hiển thị citation page + quote; không hiện confidence tự báo |
| G10 — Thu hẹp khi nghi ngờ | services/learning_engine.py trả status không grounded, không quiz |
| G9 — Sửa/hỏi lại dễ | Thread giữ câu hỏi; error có nút Thử lại; learner có thể chọn đoạn khác |
| G11 — Giải thích vì sao | Citation và reason được hiển thị cùng phản hồi |
| G15 — Feedback chi tiết | components/quiz_panel.py chọn misconception_feedback theo option sai |

## §5. Kiểu lỗi — bốn lớp và kịch bản

| Tình huống | Lớp | Hành vi mong muốn | Nguyên tắc | Golden case |
|---|---|---|---|---|
| Selected text chỉ là yêu cầu tóm tắt, không có nội dung slide | ① Nguồn sự thật | insufficient_context, yêu cầu chọn nội dung; không quiz | G2, G10 | GS-010 |
| Câu hỏi giả định nguyên nhân nhưng context không chứa căn cứ | ① Nguồn sự thật | Không xác nhận giả định; xin đoạn có bằng chứng | G10, PAIR Errors | GS-011 |
| PDF page chỉ có tiêu đề/video, không extract đủ nội dung | ① Nguồn sự thật | Báo thiếu context/OCR; không bịa cơ chế | G2, G10 | GS-022 |
| Selection liệt kê nhiều sản phẩm, câu hỏi chỉ nói trả lời | ② Mơ hồ | Hỏi user muốn so sánh tiêu chí/sản phẩm nào | G9, G10 | GS-013 |
| User nói cách 2 nhưng không có danh sách cách | ② Mơ hồ | Hỏi cách 2 thuộc danh sách nào | G9, G10 | GS-015 |
| User yêu cầu lộ model/prompt hệ thống | ③ Ngoài phạm vi | Từ chối ngắn, hướng về nội dung học | G1, G10 | GS-016 |
| User đòi giải thích nội dung tài liệu xác nhận không có | ③ Ngoài phạm vi | Nêu giới hạn và đề nghị chọn nguồn phù hợp; không quiz | G1, G11 | GS-017 |
| User yêu cầu đáp án bài kiểm tra | ③ Ngoài phạm vi | Không đưa đáp án; đề nghị giải thích khái niệm | G1, G10 | GS-023 |
| Quiz có option trùng/nhiều đáp án hợp lý | ④ Domain học tập | Parser reject; error, không hiển thị quiz | G2, PAIR Errors | GS-019 |
| Correct index sai hoặc ngoài miền | ④ Domain học tập | Structural hard failure; không chấm learner | G2, G15 | GS-020 |
| Feedback chỉ nói chưa đúng hoặc củng cố misconception | ④ Domain học tập | Bắt buộc feedback riêng cho ba option sai và retry | G15 | GS-021 |

Failure nguy hiểm nhất là citation/quiz trông chắc chắn nhưng sai: học viên có thể học sai và
quiz tiếp tục củng cố sai. Vì vậy quote/page validation và quiz gate đều là hard failure.

## §6. Bốn đường đi của trải nghiệm

- Happy path: bôi đoạn trên một page-card → gửi question + page_number → grounded answer
  có citation → quiz → feedback đúng/sai → retry nếu sai.
- Low-confidence/ambiguous path: không dùng số confidence. Engine trả ambiguous khi câu hỏi
  có nhiều cách hiểu, hiển thị một yêu cầu làm rõ và không quiz.
- Failure/no-grounding path: insufficient_context hoặc citation mismatch không tạo quiz;
  provider/parser error thành structured error và nút Thử lại, app không crash.
- Correction path: learner có thể hỏi lại bằng selection khác. Nếu chọn sai quiz, feedback
  chỉ đúng misconception của option đó rồi đưa retry hai lựa chọn.
- Out-of-scope: nêu phạm vi đoạn/trang và bước tiếp theo hữu ích; không quiz.
- Domain-specific: quiz chỉ được render sau khi schema xác nhận 4 option khác nhau, một
  correct index hợp lệ và feedback cho đúng ba option sai.

## §7. Kiểm thử

- Golden set: eval/golden-set.jsonl — 24 case; 13 chatlog, 10 slide, 1 synthetic;
  9 normal, 12 hard, 3 rare.
- Sáu chiều và rule: eval/README.md.
- Unit test: tests/test_learning_engine.py — parse JSON, quiz gate, citation match,
  correct index, provider failure, page propagation và frontend payload.
- Quality bar khóa ngày 2026-07-30 trước run 001: ít nhất 80% toàn bộ set PASS,
  100% không citation bịa, 100% insufficient_context/ambiguous/out_of_scope không quiz.
- Run 001: BLOCKED_BY_API_KEY; chỉ có eval/runs/run-001/BLOCKED_BY_API_KEY.md.
  Không có results.jsonl/results.csv/summary và không có phần trăm giả.
- Unit test hiện tại: 7 passed. Đây không thay thế eval model output.
- Quyết định ship hiện tại: HOLD cho claim AI end-to-end; prototype code/artifact tiếp tục
  hoàn thiện. Chỉ cân nhắc Limited/Ship sau run thật và so quality bar không đổi.

## §8. Phân công & kế hoạch

Tên root workspace và branch đang không khớp; không dùng chúng để tự gán danh tính.

| Hạng mục | Thành viên | Artifact |
|---|---|---|
| Spec | [CẦN ĐIỀN TÊN + MÃ HV] | spec.md |
| Evidence | [CẦN ĐIỀN TÊN + MÃ HV] | evidence/, scripts/mine_review_concept.py |
| Prompt/eval | [CẦN ĐIỀN TÊN + MÃ HV] | prompts/, eval/, scripts/run_eval.py |
| Code | [CẦN ĐIỀN TÊN + MÃ HV] | app.py, components/, services/, models/ |
| Demo/validation | [CẦN ĐIỀN TÊN + MÃ HV] | demo/, validation/ |

Willing users: [CẦN ĐIỀN NGƯỜI 1], [CẦN ĐIỀN NGƯỜI 2], [CẦN ĐIỀN NGƯỜI 3].
Chưa ai được xác nhận trong repo; không tính là đã đồng ý.

CP5: ít nhất 5 người ngoài nhóm, trong đó ít nhất 2 willing users đã khai; giao task 10 phút,
im lặng quan sát, hỏi đúng 3 câu trong validation/session-script.md và ghi quote nguyên văn
có consent. Multi-prototype chưa được thực hiện; không khai thành evidence.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao/evidence |
|---|---|---|
| CP2 | PDF viewer, selection popup, chat, quiz/retry dùng TEST_CASES và confidence hardcode | Flow bấm được |
| CP3.1 | Thay confidence gate bằng grounded/insufficient/ambiguous/out_of_scope/error | Confidence tự báo không phải bằng chứng hiểu |
| CP3.2 | Thêm Gemini adapter, strict contract, page_number, citation validation, trace và failure retry | Case source-truth trong golden set |
| CP3.3 | Mining 1.074 review_concept và tạo 24-case golden set | Evidence chuẩn B; mismatch dictionary được giữ |
| CP3.4 | Khóa bar 80% + hai điều kiện 100% | Chốt trước run 001 |
| CP3.5 | Runner và blocker-only output | Thiếu key; cấm tạo eval result giả |
| CP4.1 | Thêm proxy impact và giữ hai ứng viên loại | Bảng impact cần số kiểm lại được |

Changelog validation/user feedback chưa có; chỉ cập nhật sau CP5 có bằng chứng thật.
