# Reflection 

# Reflection — Tạ Minh Đức

## Vai trò và những phần tôi có thể giải thích

Vai trò chính của tôi là **prompt, golden set và evaluation**. Tôi tập trung biến các yêu cầu sản phẩm thành system instruction, output contract và test case có expected status rõ ràng. Bộ golden set gồm 28 case, bao phủ bốn lớp chỗ khó cùng các case thường và case hiếm. Các chiều kiểm tra gồm đúng trạng thái, có căn cứ, đúng phạm vi, đúng schema và đúng chuyên môn ở các khái niệm dễ nhầm.

Tôi có thể giải thích vì sao prompt engineering trong dự án này không chỉ là chỉnh câu chữ. Prompt là một phần của interface giữa sản phẩm và model; nó phải hoạt động cùng source context, schema, verifier, reason code và regression suite. Tôi cũng có thể giải thích các case G04/G05/G26 dùng để phát hiện over-refusal và G11 dùng để phát hiện việc model tạo quiz cho nội dung có đáp án rõ nhưng nằm ngoài phạm vi khoá học.

## AI đã hỗ trợ tôi như thế nào

AI giúp tạo nhanh các biến thể câu hỏi, phương án distractor, giả thuyết failure mode và bản nháp system instruction. Phần con người phải kiểm tra là mỗi case có thật sự grounded, distractor có phản ánh một misconception hợp lý hay không và thay đổi prompt có sửa đúng lỗi mà không phá hành vi cũ.

Tôi không đánh giá prompt chỉ bằng một vài câu trả lời đẹp trong live chat. Mỗi thay đổi cần một giả thuyết, một failure cụ thể, một bản prompt có version và một lần chạy lại toàn bộ eval set. Đây là bài học trực tiếp từ lab Prompt Engineering & Tool Calling: tối ưu dựa trên log và mismatch quan sát được, không dựa trên cảm giác.

## Một thất bại cụ thể của dự án

Case **G11 — “2+2=?”** thất bại ở hai lượt liên tiếp: model trả `status="ok"` và tự tạo quiz phép cộng dù nội dung không thuộc khoá học. Instruction cũ chỉ mô tả các ví dụ như input quá ngắn, logistics hoặc văn bản ngẫu nhiên, nên model suy luận rằng nội dung có đáp án đúng-sai rõ ràng là đủ điều kiện tạo quiz.

Cách sửa là thêm rule tường minh: “có đáp án đúng-sai rõ ràng không đồng nghĩa với đủ điều kiện ra quiz”, kèm ví dụ ngoài phạm vi. Lượt chạy tiếp theo đạt 28/28 về expected status. Quan trọng hơn, nhóm chạy lại G04, G05 và G26 để kiểm tra bản sửa không khiến model từ chối nhầm input ngắn nhưng vẫn có nội dung học thuật. Một live run sau đó vẫn cho thấy G26 có thể over-refuse, nhắc tôi rằng một lần đạt 100% không xoá bỏ rủi ro regression khi provider hoặc model thay đổi.

## Điều tôi học được

Tôi học được rằng prompt không phải guardrail duy nhất. Với các hành vi có thể xác định chắc chắn — prompt injection rõ ràng, trang không tồn tại, source mismatch, schema sai, vượt số lần thử — deterministic checks nên chặn trước hoặc sau model. Prompt tập trung vào phần cần hiểu ngữ nghĩa; code kiểm soát invariant.

Tôi cũng hiểu rõ hơn giá trị của test case “bẫy ngược”. Nếu chỉ thêm case cần từ chối, prompt sẽ ngày càng bảo thủ và có thể làm sản phẩm vô dụng. Eval tốt phải đo đồng thời false acceptance và false refusal, đặc biệt với input ngắn hoặc ngôn ngữ đời thường của học viên.

## Nếu có thêm một tuần

Tôi sẽ tách golden set thành development set và locked regression set để giảm nguy cơ tối ưu prompt quá sát các ví dụ đã thấy. Tôi cũng sẽ mở rộng tập adversarial paraphrase bằng tiếng Việt, thêm kiểm tra semantic quality cho distractor và misconception, rồi chạy nhiều lượt trên model/provider mục tiêu để đo độ ổn định thay vì chỉ báo một tỷ lệ pass đơn lẻ.

---

## Tổng kết chung của nhóm

Điều quan trọng nhất nhóm học được là xây sản phẩm AI không bắt đầu từ model và cũng không kết thúc ở một demo trả lời đúng. Một sản phẩm đáng tin cần nối được:

**pain có bằng chứng → workflow cụ thể → mức tự chủ phù hợp → source và boundary rõ → eval có thể tái hiện → trải nghiệm cho phép người dùng hiểu, bỏ qua và sửa sai.**

VLearn Learning Check Agent chưa phải sản phẩm hoàn thiện. Kết quả golden set và automated tests là bằng chứng kỹ thuật, không thay thế validation với người dùng thật. Tuy vậy, dự án đã giúp nhóm chuyển từ tư duy “làm chatbot/agent” sang tư duy “thiết kế một quyết định AI có phạm vi, có phép đo và có người chịu trách nhiệm”.
