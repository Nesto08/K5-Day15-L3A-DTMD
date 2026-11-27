# Reflection — Nguyễn Khánh Duy

> Làm ở guide bước 5.3. Mỗi người một file: `reflection/nguyen-khanh-duy.md`. Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   - Đảm nhận vai trò **TV2 — Product & User Research và Thuyết trình chính** của nhóm DTMD (Track E · Lát cắt E3).
   - Trực tiếp xây dựng giả thuyết ban đầu (`evidence/hypothesis.md`), thiết kế bảng hỏi hành vi (`evidence/survey/questions.md`), thu thập và làm sạch bộ khảo sát thực tế `n = 21` người dùng ngoài nhóm (`evidence/survey/results.csv`), thực hiện 3 cuộc phỏng vấn sâu đại diện cho 3 chân dung người dùng (`evidence/interviews/P1.md, P2.md, P3.md`) và tổng hợp đối chiếu 2 nguồn bằng chứng tại `evidence/summary.md`.
   - Biên soạn Product Canvas (`canvas.md`), đặc tả toàn bộ phần nghiệp vụ, bảng Impact 3 hướng, ma trận 3 mức tự động hóa, 9 kịch bản chỗ khó và Chuẩn "đạt" trong `spec.md` (§0, §1, §2, §3, §4 nghiệp vụ, §5, §6, §7, §9), đồng thời xây dựng nội dung chi tiết 8 trang slide, kịch bản thuyết trình và bộ câu trả lời phản biện tại `slides/outline.md`.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Sử dụng ChatGPT và Antigravity để rà soát xem các câu hỏi khảo sát/phỏng vấn có bị dính lỗi dẫn dắt (Mom Test) hay không, hỗ trợ chạy thống kê tỷ lệ `x/21 (%)` chính xác từ file CSV khảo sát và chuẩn hóa định dạng bảng Markdown theo đúng rubric của Ban Tổ Chức.
   - **Chỗ phải tự kiểm và sửa lại output của AI:** Ở bản thiết kế luồng 4 bước ban đầu, gợi ý của AI gộp sẵn cả cờ giao dịch (`T01–T04`) lẫn cờ ngữ cảnh (`R01–R07`) ngay tại thời điểm lệnh chuyển tiền vừa bị tạm chặn (`TEMP_HELD`), và gộp chung câu hỏi mơ hồ thông thường (*"Sao tiền em không đi?"*) với câu hỏi có tín hiệu nghi chiếm tài khoản (*"Có ai vừa rút tiền của em à?"*). Mình đã phát hiện sự bất hợp lý về mặt nghiệp vụ này và chỉnh lại thiết kế trong `spec.md`: tầng Ví lúc chặn mới chỉ biết bất thường số liệu (`T01–T04`), chính trong khung Chat hỗ trợ AI mới bóc tách được cờ thao túng ngữ cảnh (`R01–R07`) từ lời kể của khách, đồng thời tách rõ luồng xác nhận chính chủ khẩn cấp khi câu hỏi mơ hồ có dấu hiệu ATO.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - Khi đối chiếu bộ câu thử `eval/benchmark.csv` (đặc biệt là các câu khó như `B09` — câu hỏi mơ hồ có tín hiệu nghi rút tiền trái phép, `B10` — một tin nhắn gộp hai yêu cầu vừa đòi khóa ví vừa đòi hoàn tiền, và `B11` — người thân nhắn thay chủ ví đang bị công an giả thúc ép), bài học lớn nhất mình rút ra là: **trong sản phẩm AI tài chính, một câu trả lời "nghe hợp lý" vẫn có thể trượt nếu vi phạm ranh giới thẩm quyền hoặc hợp đồng công cụ**.
   - Ví dụ ở ca `B11` (người thân nhắn thay), nếu thiết kế nghiệp vụ yêu cầu AI gọi ngay `hold_transaction(tx_id)` khi phiên chat của người thân chưa xác thực quyền truy cập vào `tx_id` của chủ ví, hoặc lỡ tiết lộ thông tin giao dịch của chủ ví cho bên thứ ba thì sẽ tạo ra lỗ hổng bảo mật; cách xử lý đúng là AI không tiết lộ thông tin tài khoản, khuyên nhắc chủ ví dừng thao tác ngay và kích hoạt luồng bàn giao/hỗ trợ chính thức.
   - *(Cập nhật bổ sung mã câu trượt cụ thể từ `eval/run-1.csv` sau khi nhóm hoàn tất chấm Lượt 1).*
