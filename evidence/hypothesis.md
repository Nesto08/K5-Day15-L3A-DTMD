# Giả thuyết — viết TRƯỚC khi tìm bằng chứng (5 phút, commit ngay)

> Điền ở guide bước 1.1. Ôn lại: ngày 2 · lab ngày 2.
> Viết **trước** khi đọc dòng data đầu tiên hay hỏi người đầu tiên, để không sửa cho khớp kết quả. Kết quả ngược giả thuyết vẫn đủ điểm nếu số là thật.

- Ngày giờ viết: 2026-11-27 16:30 (Trước CP1)
- Người dùng chính (một vai cụ thể): Chủ ví điện tử / ứng dụng ngân hàng cá nhân vừa thực hiện lệnh chuyển tiền VND (cho người nhận mới hoặc số tiền lớn đột biến) nhưng giao dịch bị hệ thống an toàn tạm chặn/treo (`TEMP_HELD`) do chạm cờ giao dịch (`T01–T04`), đang sốt ruột nhắn tin vào khung Chat hỗ trợ 24/7 để hỏi lý do và yêu cầu xử lý ngay.
- **Mình nghĩ:** Chủ ví điện tử cá nhân gặp khó khi giao dịch chuyển tiền bị tạm giữ (`TEMP_HELD`) và nhắn vào chat hỗ trợ vì chatbot hiện tại chỉ trả lời rập khuôn theo menu tĩnh, không giải thích rõ giao dịch chạm dấu hiệu rủi ro nào và không khai thác được ngữ cảnh hội thoại (`R01–R07`) để phân biệt giữa "người cần chuyển tiền gấp hợp lệ" với "nạn nhân đang bị kẻ gian thao túng tâm lý hối thúc (APP Scam) hoặc bị chiếm tài khoản (ATO)", hậu quả là người gấp thật mất 15–30 phút chờ tổng đài viên trong lo lắng/lỡ việc khẩn cấp (viện phí, đặt cọc), còn người đang bị thao túng tâm lý lại cố nài nỉ mở khóa hoặc tìm cách lách chặn khiến tiền chuyển đi mất trắng trong vài giây.
- **Có thể còn cách giải thích khác:** Người dùng không đọc kỹ thông báo trên màn hình mà chỉ muốn bấm cho nhanh; hoặc số ca bị tạm chặn chỉ chiếm tỷ lệ nhỏ và đa số người dùng chấp nhận gọi hotline chờ nhân viên trực (8h–20h) mà không dùng khung chat.
- **Mình đúng nếu thấy:**
  1. Trong khảo sát (≥ 20 người dùng ví/ngân hàng ngoài nhóm) hoặc phỏng vấn (≥ 3 người): **≥ 60% người từng gặp giao dịch bị giữ/chậm hoặc nhận tin hối thúc chuyển tiền** phản ánh rằng họ cảm thấy hoang mang/bức xúc vì thông báo và phản hồi của chatbot hỗ trợ quá mơ hồ, mất trung bình **≥ 10–15 phút** xoay xở hoặc chờ nhân viên hỗ trợ.
  2. Trong dữ liệu đào review công khai (Google Play / App Store của các ví điện tử như MoMo, ZaloPay) và trang Trợ giúp công khai: **≥ 30% các review phàn nàn về việc khóa/giữ giao dịch & hỗ trợ khách hàng** nhắc trực tiếp đến việc bot trả lời máy móc, giữ tiền không rõ lý do hoặc chờ nhân viên xử lý quá lâu.
- **Nguồn sẽ dùng** (≥1 nguồn đạt ngưỡng, guide 1.2): [x] đào data · [x] phỏng vấn ≥3 · [x] khảo sát ≥20 — nguồn chính: **Khảo sát ≥ 20 người dùng ví điện tử/ngân hàng số ngoài nhóm + Đào data review công khai & trang Trợ giúp công khai** · nguồn để kiểm lại: **Phỏng vấn sâu ≥ 3 người dùng thực tế ngoài nhóm**.
