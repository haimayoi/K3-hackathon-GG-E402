# Mining method — review_concept

- Nguồn duy nhất: data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv.
- Đọc bằng csv.DictReader với UTF-8 BOM, đối chiếu tổng số dòng trước khi lọc.
- Tutor turn: role sau trim/lower bằng tutor.
- Pattern: move_used bằng chính xác review_concept trên tutor rows.
- Citation/misconception/follow-up rỗng khi JSON parse thành list rỗng.
- asked_check_question nhận true, 1 hoặc yes; rating chỉ tính dòng không rỗng.
- Latency tính trên avg_latency_ms của review rows; p90 dùng quantile inclusive.
- Outlier báo cáo minh bạch bằng max và proxy đếm latency từ 10.000 ms.
- Proxy thiếu context đếm tutor content có ít nhất một marker: không tìm thấy,
  không có thông tin, cung cấp thêm, chưa tìm thấy, không thể truy cập.
- Artifact chỉ chứa aggregate, ID ẩn danh và excerpt tối đa 180 ký tự; không sao chép raw pack.

Chạy lại:

    python scripts/mine_review_concept.py

Hạn chế: log chỉ gồm turn completed trong một tuần, rating rất thưa, và cờ
asked_check_question không chứng minh người học hiểu. Không suy diễn causal impact hay
thời gian tiết kiệm từ các proxy này.
