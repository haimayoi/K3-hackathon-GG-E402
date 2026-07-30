
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
