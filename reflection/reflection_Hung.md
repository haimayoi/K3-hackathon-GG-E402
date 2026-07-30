# Reflection nhóm — VLearn Learning Check Agent

> **Lưu ý trước khi nộp:** Đây là bản nháp tổng hợp từ các bằng chứng hiện có trong repository. Mỗi thành viên cần đọc lại, chỉnh câu chữ theo trải nghiệm thật và bảo đảm có thể giải thích mọi nội dung dưới tên mình. Nhóm chưa ghi nhận kết quả kiểm thử người dùng trong `validation/`, vì vậy tài liệu này không tự tạo người tham gia, lời trích dẫn hay kết quả validation.

## Bối cảnh và quyết định sản phẩm chung

Qua ba lab trước, nhóm rút ra một chuỗi tư duy xuyên suốt:

- Từ **K3-Day02-AI-Product-Labs**, nhóm học cách đi từ vấn đề, workflow, metric và boundary trước khi chọn AI.
- Từ **Day-3-Lab-Chatbot-vs-react-agent-E402**, nhóm hiểu rằng không phải bài toán nào cũng cần một agent tự chủ cao; mức tự chủ phải tương xứng với độ phức tạp và chi phí khi sai.
- Từ **Day04-C401-Prompt-Engineering-Tool-Calling-Labs**, nhóm học cách cải thiện prompt và tool contract bằng log, test case và kết quả đo được thay vì đánh giá theo cảm giác.

Những bài học đó dẫn đến quyết định xây **VLearn Learning Check Agent** theo mô hình bounded agent. Sản phẩm chỉ xử lý một lát cắt rõ ràng: học viên chọn một đoạn trên đúng trang tài liệu, đặt câu hỏi, nhận câu trả lời có căn cứ và một câu quiz bốn lựa chọn để kiểm tra mức hiểu ngay tại thời điểm học. Phần sinh nội dung dùng AI, còn kiểm tra nguồn, cấu trúc output, chấm đáp án, giới hạn số lần thử và luồng retry được kiểm soát bằng code.

---

# Reflection — Hà Duyên Hùng

## Vai trò và những phần tôi có thể giải thích

Vai trò chính của tôi là **build và tích hợp prototype**. Tôi phụ trách biến spec thành một luồng có thể sử dụng: chọn tài liệu và trang, hiển thị PDF với text layer có thể bôi đen, nhận câu hỏi, xác minh đoạn được chọn, gọi learning agent, hiển thị câu trả lời và quiz, chấm đáp án rồi đưa ra feedback hoặc câu retry.

Tôi có thể giải thích vì sao hệ thống không được xây như một vòng lặp agent mở. Bài toán chỉ cần một state machine hữu hạn với các trạng thái rõ ràng như kiểm tra nguồn, đánh giá eligibility, sinh output có cấu trúc, verify và complete/abstain. Những phần có thể quyết định chắc chắn bằng code — kiểm tra trang, kiểm tra schema, số lượng bốn options, giới hạn index, chấm đáp án và tối đa hai lần generation — không nên giao lại cho model.

Tôi cũng có thể giải thích sự khác nhau giữa artifact CP2 và canonical app: CP2 chứng minh flow có thể bấm trọn bằng dữ liệu giả; bản hoàn thiện thay mock tutor, fixed confidence và static retry bằng PDF lookup thật, structured generation có validation, deterministic scoring, privacy-minimized trace và immutable run ID.

## AI đã hỗ trợ tôi như thế nào

AI giúp tăng tốc ở các công việc như dựng skeleton component, gợi ý contract giữa các module, phân tích lỗi và tạo test scaffolding. Tuy nhiên, code do AI đề xuất vẫn phải được kiểm tra ở cấp luồng hoàn chỉnh. Một component chạy riêng không có nghĩa trải nghiệm thật sẽ đúng, đặc biệt với state của Streamlit, render PDF trong browser, text selection và việc đồng bộ context giữa tài liệu với panel hội thoại.

Tôi giữ nguyên tắc dùng AI như một cộng sự tạo phương án, không phải người phê duyệt cuối. Các quyết định về state transition, giới hạn retry, sanitization lỗi provider và dữ liệu nào được phép lưu trong trace phải được thể hiện rõ trong code và test.

## Một thất bại cụ thể của dự án

Một hạn chế rõ ở prototype ban đầu là flow có thể demo nhưng còn dựa trên **mock tutor, confidence cố định và retry tĩnh**. Điều đó chứng minh giao diện, nhưng chưa chứng minh sản phẩm có thể giữ đúng source, xử lý output lỗi hoặc chấm nhất quán khi model thay đổi.

Nguyên nhân là nhóm tối ưu cho checkpoint “bấm được flow chính” trước, trong khi contract giữa dữ liệu tài liệu, model output và UI chưa đủ chặt. Bản hardening đã tách trách nhiệm thành các module: PDF/page lookup xác định nguồn, bounded state machine điều phối, schema validation bảo vệ UI, deterministic code chấm đáp án và test suite kiểm tra failure path. Tôi học được rằng prototype tốt phải nói rõ nó đang chứng minh điều gì; một mock hợp lệ ở CP2 không được trình bày như bằng chứng production readiness.

## Điều tôi học được

Từ lab Chatbot vs ReAct, tôi học được rằng kiến trúc tốt không phải kiến trúc có nhiều “agentic” nhất. Kiến trúc tốt là kiến trúc có mức tự chủ vừa đủ cho job cần giải quyết. VLearn cần model hiểu ngôn ngữ và tạo câu hỏi, nhưng không cần model tự quyết định vô hạn số bước hoặc tự do gọi nhiều công cụ.

Tôi cũng học được rằng observability là một phần của sản phẩm chứ không chỉ phục vụ debug. Khi có run ID, artifact version, reason code và trace đã giảm dữ liệu nhạy cảm, đội có thể tái hiện lỗi mà không cần lưu nguyên văn câu hỏi hoặc chain-of-thought của người dùng.

## Nếu có thêm một tuần

Tôi sẽ ưu tiên thêm end-to-end browser tests cho ba luồng rủi ro nhất: PDF render và bôi đen text, thay đổi trang trong khi đang có hội thoại, và provider trả về malformed output hoặc timeout. Ưu tiên thứ hai là đo latency theo từng state để biết thời gian nằm ở PDF extraction, provider hay rendering; từ đó tối ưu đúng nút thắt thay vì tối ưu theo cảm giác.

## Tài liệu đối chiếu

- Repository hiện tại: `README.md`, `spec.md`, `eval/golden_set.md`, `eval/run-01-20260730.md`, `eval/offline-validation-20260730.md`, `validation/README.md`.
- [K3-Day02-AI-Product-Labs](https://github.com/VinUni-AI20k/K3-Day02-AI-Product-Labs)
- [Day-3-Lab-Chatbot-vs-react-agent-E402](https://github.com/VinUni-AI20k/Day-3-Lab-Chatbot-vs-react-agent-E402)
- [Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student-k3](https://github.com/VinUni-AI20k/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student-k3)
