# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☐ *(Sẽ bổ sung kiểm chéo trước CP3)* | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ *(Sẽ bổ sung kiểm chéo trước CP3)* | `evidence/interviews/` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ **(n = 21)** | `evidence/survey/questions.md`, `evidence/survey/results.csv` |

## 2. Số chính

- **Khảo sát (`n = 21` người dùng ví điện tử / app ngân hàng ngoài nhóm, thu từ 16:59 đến 18:27 ngày 27/11/2026):**
  - **Tần suất & bối cảnh giao dịch:** `17/21 (81,0%)` sử dụng ví/app ngân hàng hàng ngày hoặc vài lần/tuần; `14/21 (66,7%)` thường xuyên chuyển tiền cho người nhận mới lần đầu; `8/21 (38,1%)` chuyển khoản số tiền lớn đột xuất.
  - **Tỷ lệ gặp tình huống bị tạm giữ/chặn giao dịch:** `15/21 (71,4%)` bản thân đã từng gặp (`9/21` · `42,9%`) hoặc có người thân/bạn bè từng gặp (`6/21` · `28,6%`).
  - **Cảm xúc & Pain khi giao dịch bị tạm chặn (chọn tối đa 2):** `16/21 (76,2%)` hoang mang vì không biết tiền có bị trừ hay không; `11/21 (52,4%)` lo lắng sợ lỡ việc quan trọng; `10/21 (47,6%)` khó hiểu vì không biết tại sao giao dịch bị chặn.
  - **Pain cốt lõi ở Chat hỗ trợ hiện tại:** `17/21 (81,0%)` khó chịu nhất vì **Chatbot trả lời chung chung, không đúng vấn đề**; `8/21 (38,1%)` vì **chờ quá lâu mới gặp được nhân viên**; `8/21 (38,1%)` vì **phải trả lời quá nhiều câu hỏi**; `5/21 (23,8%)` vì phải kể lại sự việc từ đầu khi gặp nhân viên.
  - **Hậu quả thực tế:** `12/21 (57,1%)` từng bị **trễ hạn thanh toán hoặc công việc quan trọng**; `10/21 (47,6%)` **mất nhiều thời gian chờ hỗ trợ**; `6/21 (28,6%)` mất uy tín với người chờ nhận tiền; `6/21 (28,6%)` mất niềm tin vào ứng dụng.
  - **Ngưỡng chịu đựng câu hỏi & Kỳ vọng an toàn (cơ sở cho G10 & Guardrail):**
    - `18/21 (85,7%)` chỉ chấp nhận trả lời tối đa 1 câu (`5/21` · `23,8%`), 2–3 câu (`10/21` · `47,6%`) hoặc muốn gặp nhân viên ngay không muốn trả lời chatbot (`3/21` · `14,3%`).
    - `18/21 (85,7%)` từng gặp ít nhất 1 dấu hiệu lừa đảo (`11/21` bị thúc ép dọa khóa/phạt; `11/21` giả danh công an/ngân hàng/giao hàng; `9/21` đòi OTP/mật khẩu/cài app lạ; `7/21` yêu cầu đóng phí rút tiền).
    - `19/21 (90,5%)` đồng ý AI phải **giữ lệnh chặn và hướng dẫn xác minh độc lập** kể cả khi người dùng đang yêu cầu mở khóa; `17/21 (81,0%)` yêu cầu **tạm khóa phiên và chuyển nhân viên bảo mật** khi nghi lộ OTP/ATO.
- **Giới hạn mẫu:** Phần lớn mẫu khảo sát là sinh viên và người dùng trẻ trong cộng đồng học viên/người quen (chưa bao gồm nhân viên CSKH ví điện tử). Sẽ kiểm chéo thêm bằng phỏng vấn sâu (`≥ 3` người) và đào review công khai (`evidence/data-mining.md`) trước CP3.

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. *"Việc thì gấp, hỏi chatbot thì đần."* — `S08`, phiếu khảo sát Câu 8 (`evidence/survey/results.csv`).
2. *"Lỗi quá lâu lại thường xuyên bị làm tôi thà dùng tiền mặt còn hơn"* — `S18`, phiếu khảo sát Câu 8 (`evidence/survey/results.csv`).
3. *"Tôi lo rằng tiền sẽ bị mất và đặc biệt là lỡ dở mất công việc bên cạnh đó sẽ làm mất uy tín của tôi."* — `S10`, phiếu khảo sát Câu 8 (`evidence/survey/results.csv`).
4. *"Đột nhiên có thông báo, hoặc cuộc gọi bảo rằng mình dính vào một vụ việc nào đó mà không có bằng chứng"* — `S06`, phiếu khảo sát Câu 13 (`evidence/survey/results.csv`).
5. *"Người nhận tiền tự xưng là cơ quan nhà nước nhưng tài khoản là của cá nhân"* — `S21`, phiếu khảo sát Câu 13 (`evidence/survey/results.csv`).
6. *"Bị hối thúc, ép buộc phải làm ngay lập tức"* — `S03`, phiếu khảo sát Câu 13 (`evidence/survey/results.csv`).

## 4. Các nguồn có khớp nhau không

- **Khảo sát (`n = 21`) vs. Giả thuyết (`evidence/hypothesis.md`):** Khớp 100% ở điểm Chatbot hiện tại trả lời chung chung (`81,0%`) khiến người dùng hoang mang (`76,2%`) và trễ việc (`57,1%`), trong khi nguy cơ bị thao túng lừa đảo phổ biến (`85,7%` từng gặp dấu hiệu).
- **Nguồn thứ hai kiểm chéo:** Đang thu thập thêm dữ liệu đào review công khai (`evidence/data-mining.md`) và phỏng vấn sâu (`evidence/interviews/`) để đối chiếu trước CP3 (10:00 Thứ Bảy 28/11).

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **ĐÚNG** — `17/21 (81,0%)` phản ánh chatbot trả lời chung chung không đúng vấn đề (vượt ngưỡng giả thuyết `≥ 60%`), `12/21 (57,1%)` từng trễ hạn thanh toán/công việc và `19/21 (90,5%)` xác nhận cần giữ lệnh chặn khi có dấu hiệu lừa đảo. Điều vẫn chưa biết chính xác: thời gian xử lý trung bình (AHT) thực tế ở phía Tư vấn viên ví điện tử (sẽ phỏng vấn hoặc ghi rõ ước tính có nguồn trước CP3).
