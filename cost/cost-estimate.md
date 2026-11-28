# Chi phí vận hành trợ lý E3

## 1. Persona và quy mô

| Persona | Tỷ trọng người dùng | Phiên/người/tháng | Lượt hỏi/phiên | Nguồn |
| --- | ---: | ---: | ---: | --- |
| Dùng ít | 60% | 1 | 1 | Kịch bản hỏi một lượt trong spec §2. |
| Dùng vừa | 30% | 1,5 | 3 | Kịch bản hỏi nhiều lượt trong spec §2. |
| Dùng nhiều | 10% | 2 | 2 | Kịch bản có yêu cầu kép hoặc ngoài phạm vi trong spec §2. |

Tỷ trọng, tần suất dùng trợ lý và số lượt hỏi là **tự ước tính**. Nhóm dùng khoảng **1–3 lần gặp sự cố/tháng** từ phỏng vấn P1–P3 để tham chiếu. Khảo sát n = 21 bổ sung bằng chứng về vấn đề, còn tần suất sử dụng trợ lý chưa được đo. Tần suất bình quân theo persona là **1,25 phiên/người/tháng**. [Spec §2 và §8](../spec.md) · [Tổng hợp khảo sát và phỏng vấn](../evidence/summary.md) · [Cấu hình persona](personas.yaml)

| Kịch bản | Chủ ví gặp sự cố/tháng | Phiên hỗ trợ/tháng | Căn cứ |
| --- | ---: | ---: | --- |
| Thấp | 5.000 | 6.250 | 0,5 lần quy mô cơ sở (tự ước tính). |
| Cơ sở | 10.000 | 12.500 | 1 triệu chủ ví tích cực × 1% gặp sự cố trong tháng (cả hai là tự ước tính). |
| Cao | 20.000 | 25.000 | 2 lần quy mô cơ sở (tự ước tính). |

MoMo công bố phục vụ hơn **30 triệu người dùng** vào 06/06/2026. Đây là mốc công khai về quy mô của một ví tại Việt Nam. Quy mô chủ ví gặp sự cố trong ba kịch bản là giả định của nhóm. [Công bố của MoMo](https://www.momo.vn/tin-tuc/thong-cao-bao-chi/momo-dong-hanh-ngay-tai-chinh-so-2026-khang-dinh-8835)

## 2. Chạy mô phỏng và tính chi phí

Giá API tiêu chuẩn, đơn vị USD/1 triệu token, kiểm tra ngày 28/11/2026. Bảng giá của đề cho phép dẫn nguồn chính thức đối với model ngoài danh sách. [Bảng giá của đề](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/further-reading/model-prices.md)

| Mức giá | Model | Token vào | Token ra |
| --- | --- | ---: | ---: |
| Rẻ | GPT-5.4 nano | 0,20 | 1,25 |
| Mạnh | GPT-5.4 | 2,50 | 15,00 |

[Nguồn giá GPT-5.4 nano](https://developers.openai.com/api/docs/models/gpt-5.4-nano) · [Nguồn giá GPT-5.4](https://developers.openai.com/api/docs/models/gpt-5.4)

```powershell
python run.py simulate --try --rate-from eval/run-2.csv
python run.py simulate --rate-from eval/run-2.csv
```

Lượt thử hoàn tất 10/10 phiên với model thật và không có phiên lỗi. Lượt chính dùng seed 42 và cấu hình 50 phiên. [CSV lượt thử](simulate-try.csv) · [Tóm tắt lượt thử](simulate-try-summary.md)

Lượt chính `simulate-1@20261128-113402` hoàn tất **50/50 phiên, 84 lượt hỏi**, gồm 31 phiên dùng ít, 15 phiên dùng vừa và 4 phiên dùng nhiều. Đối chiếu CSV với trace cho kết quả **80 lượt gọi model, 174 lượt gọi công cụ, 74.967 token vào và 11.351 token ra**. Tổng thời gian xử lý ghi trong CSV là **136,669 giây**, trung bình **2,733 giây/phiên**. Có **0/50 phiên lỗi**; trace không ghi lỗi model. [CSV lượt chính](simulate-1.csv) · [Trace lượt chính](../traces/simulate-1.jsonl) · [Tóm tắt tự sinh](simulate-1-summary.md)

Khung gọi `answer(text)` riêng cho từng lượt hỏi rồi cộng số đo theo phiên. Số đo phản ánh khối lượng các lượt độc lập được ghép theo persona. Chi phí hội thoại giữ ngữ cảnh qua các lượt có thể khác. [Khung mô phỏng](simulate.py) · [Điểm vào của trợ lý](../codebase/agent.py)

### Bảng chi phí từ lượt chính

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (5.000 người) | Chi phí / tháng — cơ sở (10.000 người) | Chi phí / tháng — cao (20.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.4-nano-2026-03-17 (vào 0.2 · ra 1.25 $/1M) | $0.00058 | $0.00090 | $0.00053 | $4.12 | $8.24 | $16.47 | $0.00082 |
| gpt-5.4 (vào 2.5 · ra 15.0 $/1M) | $0.0072 | $0.0110 | $0.0066 | $50.46 | $100.93 | $201.86 | $0.0101 |

Tỷ lệ dùng trong công thức là **13/20 (65%)** từ lượt 2. Chi phí tác vụ thành công bằng chi phí bình quân mỗi phiên chia cho 0,65. Ví dụ, với nano, **0,000583643 / 0,65 ≈ 0,00090 USD**. Đây là ước tính dùng tỷ lệ đạt theo câu thử làm đại diện cho tỷ lệ thành công của phiên. Chi phí tháng bằng tổng theo persona của **số chủ ví × tỷ trọng người dùng × số phiên/người/tháng × chi phí bình quân một phiên của persona**. [Lượt 2 đã chấm](../eval/run-2.csv) · [Công thức của khung](simulate.py)

Cả hai hàng dùng số token đo bằng **GPT-5.4 nano**. Hàng GPT-5.4 áp đơn giá của model mạnh lên cùng số token và dùng 65% làm giả định so sánh. Chất lượng và mức tiêu thụ token thực tế của GPT-5.4 chưa được đo. Bảng tính chi phí API theo giá tiêu chuẩn, trước thuế, gồm token vào và token ra.

## 3. So với impact

Spec §2 dùng **1,2 ca/người/tháng × (15 phút khách chờ + 10 phút công tư vấn viên)** để ước tính **30 phút thời gian hiện đang mất/người/tháng**, gồm 18 phút của khách và 12 phút của tư vấn viên. Tần suất 1,2 trong ước tính impact là số làm tròn theo spec. Bảng chi phí dùng tần suất có trọng số 1,25 từ ba persona. Phần thời gian thực sự thu hồi cần đo trong pilot. [Spec §2 và §8](../spec.md)

Để so cùng đơn vị, lấy **1 USD/giờ** làm giả định minh họa cho giá trị thời gian. Nếu thu hồi đủ 30 phút thì giá trị là **0,50 USD/người/tháng**. Để bù riêng chi phí API ở quy mô cơ sở, nano cần tiết kiệm khoảng **3 giây/người/tháng** và GPT-5.4 cần khoảng **36 giây/người/tháng** theo giả định đó. Ngưỡng này tính từ chi phí/người/tháng nhân với 3.600 giây/giờ. Chi phí hạ tầng, tích hợp và giờ công duyệt nằm ngoài phép tính.

**Kết luận:** Đáng thử pilot có nhân viên duyệt vì ngưỡng hòa vốn riêng của API thấp. Mở rộng cần đo thời gian tiết kiệm thực tế và đạt chuẩn an toàn, hiện lượt 2 đạt 65% và điều kiện cảnh báo khi bị thúc ép đạt 4/6. [Báo cáo đánh giá](../eval/report.md)
