# DATA CARD — E3 Data Pipeline v2

**Dự án:** E3 · Giao dịch nghi lừa đảo bị tạm chặn (DTMD)  
**Phiên bản:** 2.1 (pipeline v2, benchmark CLI bản đầu)<br>
**Ngày tạo/cập nhật:** 27-11-2026  
**Trạng thái:** Giao dịch, sổ cái và hội thoại trong pipeline là dữ liệu tổng hợp (`synthetic`). Khảo sát thực địa có 21 người trả lời, được tổng hợp tại [`evidence/summary.md`](../evidence/summary.md). Một phần lời khảo sát đã được chuyển thể thành câu thử cho CLI.<br>
**Mục đích:** Phát triển và kiểm thử pipeline dữ liệu, kiểm tra logic nhãn/luồng hành động, và chuẩn bị benchmark cho AI hỗ trợ trong chat ví điện tử.

> **Cảnh báo sử dụng:** Không dataset nào trong gói này là bằng chứng về trải nghiệm/pain point của người dùng, tỷ lệ lừa đảo, hiệu quả phát hiện, hay hiệu năng mô hình. Các tình huống và nhãn kỳ vọng do nhóm thiết kế để kiểm thử theo đặc tả E3. Không dùng trực tiếp để ra quyết định giao dịch hoặc huấn luyện mô hình production nếu chưa được rà soát, bổ sung dữ liệu phù hợp và phê duyệt.

## 1. Nguồn gốc và phương pháp tạo dữ liệu của pipeline

- **Nguồn:** Nhóm tự thiết kế các tình huống theo đặc tả T01–T04, R01–R07 và các luật mở rộng R08/R10/R16/R20/R21/R22 được cung cấp trong dự án. Không lấy từ khách hàng, sổ cái thật, báo cáo lừa đảo thật hay nguồn tình báo bên ngoài.
- **Cách tạo:** Script `scripts/generate_synthetic.py` sinh JSONL theo danh sách kịch bản định nghĩa trong mã nguồn; mặc định `--seed 42`, `--benchmark-count 25`. Thời điểm dữ liệu được cố định trong script để kết quả tái lập.
- **Ẩn danh:** Không có PII thật để ẩn danh. ID người dùng, giao dịch, chat, người nhận và tham chiếu chứng từ đều là mã giả tổng hợp; `account_id_hash` là chuỗi giả, không phải hash của tài khoản thật.
- **Kiểm tra:** Pipeline chuẩn hóa, tạo fixture đánh giá luật/quyết định, kiểm tra schema và invariant. Đây là kiểm tra kỹ thuật trên fixture, không phải xác minh sự thật nghiệp vụ. Số lượt rà soát thủ công độc lập: **chưa thực hiện / chưa ghi nhận**.

## 2. Danh mục dataset

| Dataset | Raw (bản ghi) | Interim (bản ghi) | Vai trò / trường nội dung chính |
|---|---:|---:|---|
| `transactions` | 25 | 25 | Giao dịch giả lập: `tx_id`, `user_id`, `amount_vnd`, người nhận giả, trạng thái `TEMP_HELD`, trạng thái FaceID, cờ kích hoạt T, thời gian và `scenario_family_id`. |
| `ledger_transactions` | 25 | 25 | Lịch sử sổ cái giả lập theo người dùng, cửa sổ 365 ngày, người nhận và trạng thái giao dịch; dùng làm đầu vào tham chiếu cho T01/T03/T02. |
| `intelligence_sources` | 1 | 1 | Một bản ghi cảnh báo giả lập `APPROVED` gắn với kịch bản T04; không phải danh sách đen thật. |
| `conversations` | 25 | 25 | Một hội thoại/kịch bản, mỗi hội thoại hiện có một tin nhắn giả lập; gồm vai trò người nói, trạng thái định danh, nội dung, mục đích khai báo và tham chiếu chứng từ giả. |
| `scam_cases` | 7 | 7 | Bảy mô tả mẫu APP Scam tổng hợp, gắn các luật liên quan; không phải ca lừa đảo đã xác minh. |
| `benchmark_cases` | 25 | 25 | Bộ test với nhánh kỳ vọng, autonomy level, expected action, tool bắt buộc/cấm và critical failure. Có thể có biến thể paraphrase cùng `scenario_family_id`. |

**Dữ liệu processed:** `rule_assessments.jsonl` (25), `risk_decisions.jsonl` (25), `action_expectations.jsonl` (25), `benchmark_cases.jsonl` (25). Đây là đầu ra dẫn xuất từ fixture, không phải dataset nguồn độc lập.

**Phân bố 25 benchmark case theo nhánh kỳ vọng:** `PRESSURE_TRANSFER` 7; `LEGITIMATE_URGENT` 6; `ACCOUNT_TAKEOVER` 7; `UNCLEAR` 5. Phân bố này được chủ động thiết kế, không phản ánh tần suất ngoài đời.

**Benchmark CLI** ([`eval/benchmark.csv`](../eval/benchmark.csv), bản đầu ngày 27-11-2026) có 20 câu thử để chạy `python run.py eval`. Trong đó, 10 câu mang nguồn `nguoi_dung` và 10 câu `tu_viet` từ kịch bản [`spec.md` §5](../spec.md). Hai ca tấn công là B14 và B15. Tập CSV này được dùng làm bộ đánh giá CLI, còn tập JSONL của pipeline kiểm thử logic dữ liệu và nhãn.

- **Chọn và làm sạch.** Lọc câu trả lời mở C8/C13 trong `evidence/survey/results.csv` có tình huống liên quan, chuyển thành tin nhắn hỗ trợ với ngữ cảnh tạm giữ khi cần, chỉ giữ mã phiếu `Sxx` và số câu để truy vết. Nội dung chuyển thể không được dùng làm trích dẫn nguyên văn hay bằng chứng về một giao dịch có thật. Không đưa tên, thời gian trả lời, tài khoản hay sao kê vào CSV. Mã thử ở B12 là dữ liệu giả.
- **Độ phủ.** Dùng bốn chiều gồm vai người nhắn, loại tình huống, mức đủ thông tin và hành vi mong đợi. Các mã B03, B05–B15 đối chiếu theo §5. Phần tình huống tự viết và nhãn kỳ vọng cần rà soát nghiệp vụ trước khi chốt.
- **Phân tập.** CSV là một tập đánh giá chung, chưa tách tập giữ riêng. Việc chia theo `scenario_family_id` chỉ áp dụng cho pipeline JSONL.

## 3. Quy trình xử lý và lineage

1. **Generate:** `scripts/generate_synthetic.py` tạo sáu file trong `data/raw/`.
2. **Normalize:** `scripts/normalize_data.py` tạo các file `data/interim/normalized_*.jsonl`; chuẩn hóa cấu trúc và giá trị để xử lý thống nhất.
3. **Rule assessment:** `scripts/build_rule_assessments.py` tạo `data/processed/rule_assessments.jsonl` từ adapter.
4. **Decision/action labels:** `scripts/build_decisions.py` tạo nhãn nhánh quyết định và kỳ vọng hành động.
5. **Validate:** `scripts/validate_data.py` kiểm tra cấu trúc và invariant an toàn; kết quả lần chạy đóng gói được lưu tại `reports/validation_report.json` và báo cáo chất lượng.
6. **Split:** `scripts/split_data.py` chia theo `scenario_family_id` để tránh đưa các biến thể cùng họ tình huống vào nhiều tập. Xem `data/processed/splits/` sau khi chạy pipeline.
7. **Report/evaluation:** `scripts/build_report.py` tạo báo cáo tổng hợp; `eval/evaluate.py` chấm output mô hình do người dùng cung cấp, không tự chạy mô hình.

Lệnh tái tạo mặc định:

```bash
python scripts/run_pipeline.py --seed 42 --benchmark-count 25
python -m unittest discover -s tests -v
```

## 4. Nhãn, rulebase và giới hạn tương thích

- Phiên bản tham chiếu: `T01-T04-candidate-v1`, `R01-R07-B1-v1.0`; luật mở rộng được liệt kê trong `config/rulebase_config.json`.
- Trạng thái đánh giá luật dùng `MATCHED`, `NOT_MATCHED`, `UNKNOWN`. `R05` là cờ xác minh và `R06` là cờ Safety/ATO, không cộng trọng số B1 theo đặc tả được cung cấp.
- Adapter hiện tại là **fixture / integration seam**, không phải implementation tương đương Rulebase Python thật. Cần TV1 thay adapter bằng import và gọi trực tiếp code trong `src/agents/rulebase/transaction_predicates.py`, `catalog.py`, `context_rules.py` và dịch vụ giao dịch liên quan; sau đó chạy lại toàn bộ benchmark.
- Đặc tả được bàn giao có mâu thuẫn ngưỡng: HIGH vừa ghi `>=75` vừa có mô tả `>=65`; MEDIUM vừa ghi `>=35` vừa có mô tả `>=30`. Gói giữ mâu thuẫn trong `config/rulebase_config.json`; **không coi ngưỡng nào là chuẩn production** trước khi đối chiếu codebase và thống nhất với nhóm.
- Cờ giao dịch trong dữ liệu sinh là giá trị kịch bản để tạo fixture. Trong production, T01–T04 phải được tính từ ledger/intelligence và thời điểm giao dịch, không tin trực tiếp cờ do client/chat tự khai.
- `expected` trong benchmark là nhãn mục tiêu do nhóm đặt theo ma trận E3, chưa được chuyên gia độc lập xác nhận.

## 5. An toàn và quyền sử dụng

- `SELF_DECLARED` không được dùng để xóa cờ rủi ro đã `MATCHED`; FaceID thành công không đồng nghĩa giao dịch an toàn.
- Nhánh APP Scam không được tự giải phóng giao dịch; nhánh gấp thật cần chuyển tư vấn viên ưu tiên; nhánh ATO cần chuyển luồng bảo mật; nhánh chưa rõ chỉ hỏi tối đa một câu làm rõ theo benchmark.
- Tên tool trong dữ liệu là nhãn/ý định hành động. Package không kết nối ví, không khóa ví/phiên thật, không giữ/nhả tiền và không gửi ticket thật.
- Dữ liệu chỉ dùng trong môi trường phát triển, demo và kiểm thử nội bộ. Không tái nhận diện cá nhân; không có cá nhân thật để nhận diện.

## 6. Giới hạn và rủi ro sai lệch

- Kích thước nhỏ (25 kịch bản) và phân bố cân bằng có chủ đích; không đại diện lưu lượng chat hoặc phân bố gian lận thực tế.
- Mỗi hội thoại hiện chỉ có một tin nhắn; chưa mô phỏng đầy đủ hội thoại nhiều lượt, sửa lời khai, người thân nhắn thay, nhiều yêu cầu trong một tin, hoặc thay đổi trạng thái theo thời gian.
- Chưa có dữ liệu thực địa về người đang bị thao túng nhưng FaceID hợp lệ, người cần viện phí tại quầy, tài khoản bị chiếm quyền, false positive/false negative, thời gian xử lý thực tế.
- Chưa đánh giá chất lượng truy hồi RAG, độ chính xác trích xuất ngữ cảnh, độ bền với chính tả/tiếng lóng/giọng vùng miền, hay hiệu năng LLM.
- Chưa có đo latency/token cost từ phiên chạy mô hình thật; các chỉ số này phải được thu thập ở `eval/model_outputs.jsonl` hoặc log tương đương.
- Synthetic benchmark có nguy cơ lộ mẫu/overfit nếu dùng đồng thời để phát triển prompt và báo cáo hiệu năng cuối. Cần tạo test set độc lập, khóa nhãn và đánh giá mù trước khi tuyên bố hiệu năng.

## 7. Kế hoạch bổ sung dữ liệu

1. Kiểm chéo nguồn và nội dung chuyển thể từ khảo sát. Nếu cần bổ sung câu thử, dùng lời phỏng vấn đã ẩn danh hoặc ví dụ công khai có nguồn. Dữ liệu giao dịch chạy thử tiếp tục dùng dữ liệu giả lập.
2. Thu thập nhãn từ ít nhất hai người gán nhãn độc lập theo guideline cho bốn nhánh, từng rule, mức độ chắc chắn và hành động an toàn; xử lý bất đồng bằng adjudication.
3. Bổ sung hard cases: FaceID đúng nhưng bị thao túng; viện phí thật; dò ngưỡng né kiểm soát; một tin có nhiều ý định; dấu hiệu ATO; người thân nhắn thay; câu mơ hồ về rút tiền.
4. Tách train/validation/test theo người dùng và `scenario_family_id`; giữ một tập test độc lập, không dùng để chỉnh prompt/rule.
5. Đo inter-annotator agreement, coverage theo nhóm tình huống, false positive/negative và critical safety violations; không chỉ báo cáo accuracy tổng.

## 8. Chủ sở hữu và phiên bản

- **Chủ sở hữu:** Nhóm DTMD / Track E3 (điền tên người chịu trách nhiệm dữ liệu trước khi dùng ngoài nhóm).
- **Người rà soát nghiệp vụ và phê duyệt nhãn:** Chưa ghi nhận.
- **Lịch sử:** v2.0 — lập data card theo pipeline E3 v2, ghi nhận nguồn synthetic, số lượng dataset, lineage, giới hạn adapter và các mâu thuẫn ngưỡng trong rulebase.
- **Lịch sử:** v2.1 — ghi nguồn khảo sát, cách chuyển thể và phạm vi benchmark CLI.
