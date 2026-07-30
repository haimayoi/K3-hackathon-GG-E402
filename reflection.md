# Reflection nhóm — VLearn Learning Check Agent

> **Lưu ý trước khi nộp:** Đây là bản nháp tổng hợp từ các bằng chứng hiện có trong repository. Mỗi thành viên cần đọc lại, chỉnh câu chữ theo trải nghiệm thật và bảo đảm có thể giải thích mọi nội dung dưới tên mình. Nhóm chưa ghi nhận kết quả kiểm thử người dùng trong `validation/`, vì vậy tài liệu này không tự tạo người tham gia, lời trích dẫn hay kết quả validation.

## Bối cảnh và quyết định sản phẩm chung

Qua ba lab trước, nhóm rút ra một chuỗi tư duy xuyên suốt:

- Từ **K3-Day02-AI-Product-Labs**, nhóm học cách đi từ vấn đề, workflow, metric và boundary trước khi chọn AI.
- Từ **Day-3-Lab-Chatbot-vs-react-agent-E402**, nhóm hiểu rằng không phải bài toán nào cũng cần một agent tự chủ cao; mức tự chủ phải tương xứng với độ phức tạp và chi phí khi sai.
- Từ **Day04-C401-Prompt-Engineering-Tool-Calling-Labs**, nhóm học cách cải thiện prompt và tool contract bằng log, test case và kết quả đo được thay vì đánh giá theo cảm giác.

Những bài học đó dẫn đến quyết định xây **VLearn Learning Check Agent** theo mô hình bounded agent. Sản phẩm chỉ xử lý một lát cắt rõ ràng: học viên chọn một đoạn trên đúng trang tài liệu, đặt câu hỏi, nhận câu trả lời có căn cứ và một câu quiz bốn lựa chọn để kiểm tra mức hiểu ngay tại thời điểm học. Phần sinh nội dung dùng AI, còn kiểm tra nguồn, cấu trúc output, chấm đáp án, giới hạn số lần thử và luồng retry được kiểm soát bằng code.

---

# Reflection — Lê Hà Hải Vân

## Vai trò và những phần tôi có thể giải thích

Vai trò chính của tôi là phụ trách **bằng chứng và `spec.md`**. Tôi tập trung làm rõ người dùng, pain point, lát cắt prototype, quality bar và ranh giới mà hệ thống không được vượt qua. Một quyết định quan trọng là không mô tả sản phẩm như một “AI tutor làm mọi thứ”, mà giới hạn nó vào một việc có thể kiểm chứng: giúp học viên tự kiểm tra xem mình có thực sự hiểu đoạn vừa đọc hay không.

Tôi có thể giải thích cách nhóm chuyển các yêu cầu sản phẩm thành bốn lớp tình huống khó: nguồn sự thật, input mơ hồ hoặc thiếu thông tin, yêu cầu ngoài phạm vi và lỗi đặc thù domain. Tôi cũng có thể giải thích các nguyên tắc G2, G8, G9, G10 và G11 trong spec: làm rõ phạm vi, cho phép bỏ qua, hỗ trợ sửa sai, thu hẹp khi thiếu căn cứ và giải thích dựa trên lựa chọn cụ thể của học viên.

Trong kế hoạch validation, tôi phụ trách cấu trúc ghi nhận evidence: người thử, task, hành vi quan sát được, trích dẫn nguyên văn có sự đồng ý, mức nghiêm trọng và quyết định sản phẩm. Tại thời điểm viết reflection, thư mục `validation/` vẫn là template trống; do đó tôi chưa xem lời khen xã giao hoặc giả định của nhóm là bằng chứng người dùng.

## AI đã hỗ trợ tôi như thế nào

AI hữu ích khi giúp tổng hợp nhanh tài liệu, gợi ý cách nhóm các failure mode và kiểm tra độ rõ của câu chữ trong spec. Tuy nhiên, tôi không coi một kết luận do AI tạo ra là evidence. Những thông tin quan trọng phải quay về nguồn có thể đối chiếu: slide thật, chatlog đã được cấp, golden set hoặc kết quả chạy được lưu trong repository.

Điểm tôi cần tự chịu trách nhiệm là quyết định điều gì được xem là pain có bằng chứng, đâu là phạm vi hợp lệ và quality bar nào đủ chặt. AI có thể viết một problem statement nghe thuyết phục nhưng vẫn sai nếu dữ liệu phía dưới không kiểm tra lại được.

## Một thất bại cụ thể của dự án

Thất bại đáng nhớ nhất ở phần evidence là **golden set v1 có 15/28 case chứa nội dung không tồn tại trong hai file slide được cấp**. Các case nghe hợp lý về mặt chủ đề, nhưng không thể truy ngược về nguồn thật nên không đủ điều kiện dùng để đánh giá một sản phẩm grounded.

Nguyên nhân gốc là nhóm đã ưu tiên độ đa dạng của test case trước tính truy xuất nguồn. Cách sửa là rà lại từng case, rebuild golden set v2 và chỉ giữ nội dung đối chiếu được với `d1-slide-hackathon.pdf` hoặc `d2-slide-hackathon.pdf`. Bài học của tôi là một eval set không tự động trở thành evidence chỉ vì nó có nhiều dòng; chất lượng phụ thuộc vào provenance và khả năng kiểm tra lại.

## Điều tôi học được

Tôi học được rằng product management cho sản phẩm AI không dừng ở việc mô tả user flow. PM phải định nghĩa được nguồn sự thật, hành vi khi hệ thống không chắc chắn, chi phí của lỗi và phép đo thành công trước khi đội build tối ưu model.

Tôi cũng hiểu rõ hơn sự khác biệt giữa “AI có thể làm” và “AI nên được phép tự làm”. Với sản phẩm học tập, câu trả lời hoặc quiz sai có thể khiến học viên ghi nhớ sai kiến thức. Vì vậy, lựa chọn bounded agent, citation theo trang, structured output và cơ chế abstain phù hợp hơn việc tăng mức tự chủ chỉ để demo trông thông minh hơn.

## Nếu có thêm một tuần

Ưu tiên đầu tiên của tôi là thực hiện đúng protocol trong `validation/README.md` với ít nhất năm người ngoài nhóm, ghi nhận hành vi và câu nói nguyên văn thay vì chỉ hỏi họ có thích tính năng hay không. Sau đó tôi sẽ lập một traceability matrix nối từng pain, yêu cầu, failure mode và thay đổi sản phẩm với một evidence ID cụ thể. Như vậy nhóm có thể phân biệt rõ đâu là quyết định dựa trên người dùng và đâu mới chỉ là giả thuyết kỹ thuật.

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

---

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

## Tài liệu đối chiếu

- Repository hiện tại: `README.md`, `spec.md`, `eval/golden_set.md`, `eval/run-01-20260730.md`, `eval/offline-validation-20260730.md`, `validation/README.md`.
- [K3-Day02-AI-Product-Labs](https://github.com/VinUni-AI20k/K3-Day02-AI-Product-Labs)
- [Day-3-Lab-Chatbot-vs-react-agent-E402](https://github.com/VinUni-AI20k/Day-3-Lab-Chatbot-vs-react-agent-E402)
- [Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student-k3](https://github.com/VinUni-AI20k/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student-k3)
