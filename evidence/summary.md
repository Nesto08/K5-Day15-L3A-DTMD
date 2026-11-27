# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1 (14 điểm).
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: **có nguồn thứ hai kiểm lại nguồn thứ nhất**, khớp nhau hoặc giải thích rõ chỗ lệch.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☐ *(Không dùng làm nguồn chính; chỉ tham chiếu quy trình công khai MoMo/ZaloPay)* | — |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☑ **(3/3 người ngoài nhóm, đủ 3 persona)** | `evidence/interviews/P1.md`, `P2.md`, `P3.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ **(n = 21 người ngoài nhóm)** | `evidence/survey/questions.md`, `evidence/survey/results.csv` |

## 2. Số chính

- **Nguồn 1 — Khảo sát diện rộng (`n = 21` người dùng ví điện tử / app ngân hàng ngoài nhóm, thu ngày 27/11/2026):**
  - **Tần suất & bối cảnh giao dịch:** `17/21 (81,0%)` sử dụng ví/app ngân hàng hàng ngày hoặc vài lần/tuần; `14/21 (66,7%)` thường xuyên chuyển tiền cho người nhận mới lần đầu; `8/21 (38,1%)` chuyển khoản số tiền lớn đột xuất.
  - **Tỷ lệ gặp tình huống bị tạm giữ/chặn giao dịch:** `15/21 (71,4%)` bản thân đã từng gặp (`9/21` · `42,9%`) hoặc có người thân/bạn bè từng gặp (`6/21` · `28,6%`).
  - **Cảm xúc & Pain khi giao dịch bị tạm chặn (chọn tối đa 2):** `16/21 (76,2%)` hoang mang vì không biết tiền có bị trừ hay không; `11/21 (52,4%)` lo lắng sợ lỡ việc quan trọng; `10/21 (47,6%)` khó hiểu vì không biết tại sao giao dịch bị chặn.
  - **Pain cốt lõi ở Chat hỗ trợ hiện tại:** `17/21 (81,0%)` khó chịu nhất vì **Chatbot trả lời chung chung, không đúng vấn đề**; `8/21 (38,1%)` vì **chờ quá lâu mới gặp được nhân viên**; `8/21 (38,1%)` vì **phải trả lời quá nhiều câu hỏi**; `5/21 (23,8%)` vì **phải kể lại sự việc từ đầu khi gặp nhân viên**.
  - **Hậu quả thực tế:** `12/21 (57,1%)` từng bị **trễ hạn thanh toán hoặc công việc quan trọng**; `10/21 (47,6%)` **mất nhiều thời gian chờ hỗ trợ**; `6/21 (28,6%)` mất uy tín với người chờ nhận tiền; `6/21 (28,6%)` mất niềm tin vào ứng dụng.
  - **Ngưỡng chịu đựng câu hỏi & Kỳ vọng an toàn (cơ sở cho G10 & Guardrail):**
    - `18/21 (85,7%)` chỉ chấp nhận trả lời tối đa 1 câu (`5/21` · `23,8%`), 2–3 câu (`10/21` · `47,6%`) hoặc muốn gặp nhân viên ngay không muốn trả lời chatbot (`3/21` · `14,3%`).
    - `18/21 (85,7%)` từng gặp ít nhất 1 dấu hiệu lừa đảo (`11/21` bị thúc ép dọa khóa/phạt; `11/21` giả danh công an/ngân hàng/giao hàng; `9/21` đòi OTP/mật khẩu/cài app lạ; `7/21` yêu cầu đóng phí rút tiền).
    - `19/21 (90,5%)` đồng ý AI phải **giữ lệnh chặn và hướng dẫn xác minh độc lập** kể cả khi người dùng đang yêu cầu mở khóa; `17/21 (81,0%)` yêu cầu **tạm khóa phiên và chuyển nhân viên bảo mật** khi nghi lộ OTP/ATO.

- **Nguồn 2 — Phỏng vấn sâu kiểm chéo (`3/3 người` ngoài nhóm, hỏi chuyện thực tế trong 1 tháng qua — *n nhỏ không ghi %*):**
  - **3/3 người** đều gặp tình huống giao dịch chuyển tiền bị chậm/tạm giữ yêu cầu xác minh lại trong 1 tháng qua.
  - **Số lần gặp / tháng:** `P1` ~2 lần/tháng · `P2` 1–2 lần/tháng · `P3` 2–3 lần/tháng (trung bình **~1,5–2 lần/tháng** ở nhóm giao dịch thường xuyên).
  - **Thời gian mất mỗi lần:** **15–30 phút/lần** (`P1` ~20 phút · `P2` 15–20 phút · `P3` ~30 phút).

| Mã | Vai (Persona) | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| **P1** | Sinh viên 21 tuổi (mua hàng online, đặt cọc qua MB Bank & MoMo) | **Có** (tuần trước chuyển cọc 1 triệu ₫ mua điện thoại buổi tối bị giữ xác minh) | ~2 lần / tháng | **~20 phút** | Xem lịch sử giao dịch → bấm menu Chatbot hỗ trợ → chờ gặp nhân viên thật và phải khai lại thông tin từ đầu |
| **P2** | Nhân viên văn phòng 27 tuổi (thanh toán dịch vụ & đối tác qua Techcombank) | **Có** (2 tuần trước chuyển 5 triệu ₫ xác nhận đơn dịch vụ giờ nghỉ trưa bị giữ kiểm tra) | 1–2 lần / tháng | **15–20 phút** | Kiểm tra số dư → đi qua nhiều bước menu tĩnh của Chatbot vì sợ tự chuyển lại sẽ bị trừ tiền 2 lần |
| **P3** | Chủ shop kinh doanh online 30 tuổi (chuyển tiền lấy hàng hằng ngày qua VCB, BIDV, Shinhan) | **Có** (đầu tháng chuyển >10 triệu ₫ cho nhà cung cấp buổi tối bị treo kiểm tra an toàn) | 2–3 lần / tháng | **~30 phút** | Chụp màn hình giao dịch → hỏi Chatbot (bị chỉ dẫn kiểm tra mạng/cập nhật app vô bổ) → chờ nhân viên và phải đọc lại STK, số tiền, giờ giao dịch từ đầu |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên — tổng 9 trích dẫn)

1. *"Việc thì gấp, hỏi chatbot thì đần."* — `S08`, phiếu khảo sát Câu 8 (`evidence/survey/results.csv`).
2. *"Lỗi quá lâu lại thường xuyên bị làm tôi thà dùng tiền mặt còn hơn"* — `S18`, phiếu khảo sát Câu 8 (`evidence/survey/results.csv`).
3. *"Tôi lo rằng tiền sẽ bị mất và đặc biệt là lỡ dở mất công việc bên cạnh đó sẽ làm mất uy tín của tôi."* — `S10`, phiếu khảo sát Câu 8 (`evidence/survey/results.csv`).
4. *"Đột nhiên có thông báo, hoặc cuộc gọi bảo rằng mình dính vào một vụ việc nào đó mà không có bằng chứng"* — `S06`, phiếu khảo sát Câu 13 (`evidence/survey/results.csv`).
5. *"Người nhận tiền tự xưng là cơ quan nhà nước nhưng tài khoản là của cá nhân"* — `S21`, phiếu khảo sát Câu 13 (`evidence/survey/results.csv`).
6. *"Bị hối thúc, ép buộc phải làm ngay lập tức"* — `S03`, phiếu khảo sát Câu 13 (`evidence/survey/results.csv`).
7. *"Nếu một người đang hoảng mà app chỉ hiện thông báo kiểu 'Giao dịch không thể thực hiện vì lý do bảo mật' thì họ sẽ càng hoang mang. Có người sẽ nghĩ ngân hàng bị lỗi, có người lại tìm cách chuyển qua tài khoản khác hoặc làm theo hướng dẫn của người đang gọi điện cho họ."* — `P1` (Sinh viên 21 tuổi, `evidence/interviews/P1.md`).
8. *"Những việc liên quan đến tiền đã bị trừ, giao dịch nghi ngờ gian lận, khóa tài khoản hoặc mở lại giao dịch giá trị lớn thì mình muốn nhân viên thật xử lý. Những quyết định liên quan trực tiếp đến tiền thì mình không muốn để bot tự quyết định."* — `P2` (Nhân viên văn phòng 27 tuổi, `evidence/interviews/P2.md`).
9. *"Chatbot yêu cầu chọn vấn đề, mình chọn giao dịch bị treo nhưng nó lại hướng dẫn kiểm tra kết nối mạng, cập nhật ứng dụng rồi thử lại... Đặc biệt, nếu chuyển sang nhân viên thì mình muốn họ nhìn thấy luôn lịch sử chat và thông tin giao dịch trước đó. Mình không muốn phải kể lại toàn bộ câu chuyện từ đầu."* — `P3` (Chủ shop online 30 tuổi, `evidence/interviews/P3.md`).

## 4. Các nguồn có khớp nhau không (Kiểm chéo Khảo sát `n = 21` và Phỏng vấn `3/3 người`)

Hai nguồn bằng chứng độc lập **khớp chặt chẽ và bổ sung trực tiếp cho nhau**:
- **Khảo sát (`n = 21`) đo độ rộng của Pain**, còn **Phỏng vấn (`3/3 người`) giải thích cơ chế "Vì sao" và cung cấp số phút định lượng**:
  1. *Vì sao `17/21 (81,0%)` ghét chatbot trả lời chung chung và `16/21 (76,2%)` hoang mang không biết tiền đã trừ chưa?* Phỏng vấn `P2` và `P3` làm rõ: khi lệnh chuyển 5–10 triệu ₫ bị treo mà bot chỉ bắt chọn menu tĩnh hoặc khuyên "kiểm tra mạng/cập nhật app", người dùng **không dám tự chuyển lại lần nữa vì sợ bị trừ tiền 2 lần (thanh toán trùng)**, buộc phải ngồi chờ mất **15–30 phút/ca**.
  2. *Vì sao `19/21 (90,5%)` đồng ý phải giữ chặn khi nghi lừa đảo, nhưng người bị lừa ngoài đời vẫn cố chuyển tiền?* Phỏng vấn `P1` và `P2` chỉ ra: khi app chỉ báo vỏn vẹn *"tạm giữ vì lý do bảo mật"* mà không chỉ rõ dấu hiệu thao túng cụ thể (giả danh công an, đòi phí mở khóa, đòi OTP), nạn nhân đang hoảng sẽ tưởng hệ thống ngân hàng bị lỗi kỹ thuật và càng nghe theo lời kẻ đang gọi điện dẫn dắt.
  3. *Vì sao cần `G10` (hỏi tối đa 1 câu) và `Handoff Summary` chuyển nhân viên?* Khảo sát cho thấy `18/21 (85,7%)` chỉ chịu trả lời tối đa 1–3 câu (hoặc muốn gặp nhân viên ngay); phỏng vấn `P1, P2, P3` đều xác nhận ngưỡng kiên nhẫn khi đang gấp chỉ là **1–2 câu trọng tâm**, và `P1, P3` đặc biệt bức xúc việc phải khai lại số tài khoản/số tiền/thời gian từ đầu khi gặp nhân viên — xác nhận tính thiết yếu của phiếu bàn giao **`Handoff Summary`** và quy tắc **AI không tự mở khóa/khóa ví thật (`P2`)**.

## 5. Kết luận

- Giả thuyết ở `evidence/hypothesis.md`: **ĐÚNG** — được xác nhận bởi cả hai nguồn đạt ngưỡng (`Khảo sát n = 21` với `81,0%` gặp pain chatbot trả lời chung chung, vượt ngưỡng giả thuyết `≥ 60%`; và `Phỏng vấn 3/3 người` mất `15–30 phút/lần`).
- **Giới hạn của bằng chứng:** Cỡ mẫu khảo sát (`n = 21`) và phỏng vấn (`3 người`) tập trung vào phía **chủ ví / người dùng cá nhân & hộ kinh doanh online**; thời gian xử lý nội bộ của Tư vấn viên CSKH (~10 phút/ca trong bảng Impact `spec.md` §2) là số ước tính dựa trên tổng thời gian chờ 15–30 phút mà `P1–P3` ghi nhận.
