# Tổng hợp bằng chứng nhu cầu · CP3 và CP4

Giả thuyết được ghi trước khi phỏng vấn ở [hypothesis.md](hypothesis.md). Người dùng mục tiêu là sinh viên ngoài nhóm đã tự chọn linh kiện cho máy tính để bàn lần đầu, ưu tiên lần chọn trong 30 ngày gần nhất.

## Tiến độ thu thập

Bằng chứng CP3 có **3 cuộc phỏng vấn thật với sinh viên đúng đối tượng** và **9 ví dụ nguyên văn từ khảo sát**, kèm hai trích dẫn phỏng vấn được phép lưu. Bản xuất Google Forms ngày 27/11/2026 có **20 phản hồi**, gồm 8 phản hồi đã ghi tại CP2 và 12 bổ sung. Sáu người bổ sung qua sàng lọc, nâng tổng lên **10 người đúng đối tượng**. [Issue #13](https://github.com/tdisokay2/K5-Day15-L3A-LoiChoi/issues/13)

| Nguồn | Tiến độ ghi nhận trong repo | Ngưỡng theo guide |
|---|---|---|
| Phỏng vấn | 3 sinh viên ngoài nhóm, lần chọn hoặc rà trong 30 ngày qua. CP3 ghi khoảng chung 10–20 phút. CP4 xác nhận thời lượng riêng ở mục bên dưới. | Đủ 3 người đúng vai. Hướng dẫn dự kiến 10–15 phút/người. |
| Khảo sát | 20 phản hồi. Câu 1 có 10 “Có”, 9 “Không” và 1 “Không chắc chắn”. | 10/20 người đúng vai, còn thiếu 10 phản hồi đủ điều kiện |
| Đào dữ liệu hành vi | Chưa có tập dữ liệu hành vi đã phân tích | Có mẫu số, cách đếm chạy lại được và ví dụ có nguồn |

Bản phân tích dùng [CSV ẩn danh](survey/results.csv) và [bộ câu hỏi](survey/questions.md). Ghép bản mới với CP2 bằng bộ 9 đáp án giống hệt nhau. Giữ 8 mã S01–S08 để các dẫn chiếu cũ vẫn tra được, rồi gắn mã S09–S20 cho 12 dòng mới theo thứ tự xuất. Bỏ dấu thời gian và cột không có tiêu đề nằm ngoài 9 câu đã đối chiếu. Giữ nguyên đáp án và ô trống ở 9 câu, kể cả các dòng bị loại khi sàng lọc.

Câu 1 hỏi người trả lời có phải là sinh viên ngoài nhóm và từng tự chọn linh kiện cho máy bàn đầu tiên hay không. Chỉ phân tích 10 dòng chọn “Có”. Chín dòng trả lời đủ 9 câu, riêng S09 để trống câu 4 và có câu 7 hợp lệ. Với câu 7, mẫu số là người đúng đối tượng có đáp án hợp lệ, gồm cả “không kiểm tra”. Tử số là số người chọn tra thêm, nhờ xác nhận, đổi/hoãn chọn linh kiện hoặc làm thêm bước khác. Nếu có dòng “Không nhớ” hoặc bỏ trống ở câu 7 thì ghi riêng. [Guide của BTC, bước 1.2](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/02-guide.md)

## Kết quả

| Câu | Kết quả trong 10 phản hồi qua sàng lọc |
|---|---|
| Câu 2 · Lần chọn gần nhất | 2 trong 7 ngày qua, 1 cách đây 8–30 ngày, 3 cách đây 31–90 ngày, 4 hơn 90 ngày. |
| Câu 3 · Số nguồn | 1 tự đối chiếu, 2 dùng một nguồn, 3 dùng hai nguồn, 4 dùng từ ba nguồn trở lên. |
| Câu 4 · Cách dựa vào chủ yếu | 3 hỏi trợ lý AI, 2 xem tài liệu hãng. Hỏi bạn bè/cộng đồng, hỏi người bán, xem trang bán hàng và dựa vào kiến thức của mình mỗi cách có 1. Một dòng để trống. |
| Câu 5 · Trạng thái danh sách | 5 đã chốt, 5 chốt một phần. |
| Câu 6 · Việc tốn thời gian nhất | 6 chọn giá/ngân sách, 2 chọn hiệu năng, 1 chọn xác định đúng mã, 1 chọn kiểm tương thích. |
| Câu 7 · Bước phát sinh | **8/10 (80%)** báo làm thêm một bước, gồm 6 tra thêm và 2 nhờ xác nhận. Hai người chọn không kiểm tra. Không có đáp án “Không nhớ” hay ô trống ở câu này. Baseline CP2 là 2/4. |
| Câu 8 · Phần phân vân | 4 chọn CPU–mainboard, 2 chọn GPU–vỏ, 1 chọn mainboard–RAM và 3 chọn có kiểm tra và không phân vân. |
| Câu 9 · Số lần trong 30 ngày | 4 chọn 0 lần, 1 chọn 1 lần, 5 chọn 2 lần. |
| Câu 10 · Thời gian phát sinh | Bản xuất chưa có câu 10, nên chưa có số phút. |

Chỉ 3/10 người cho biết lần chọn hoặc rà gần nhất nằm trong 30 ngày. S02, S07, S09 và S12 chọn 2 lần phát sinh trong 30 ngày nhưng cho biết lần rà gần nhất đã quá 30 ngày. S16 báo tra thêm ở lần rà trong 30 ngày nhưng chọn 0 lần phát sinh trong cùng khoảng thời gian. S01 và S07 chọn không kiểm tra ở câu 7 trong khi câu 3 hoặc 8 mô tả việc kiểm tra. Giữ nguyên các dòng, tính câu 7 theo quy tắc trên và chưa dùng câu 9 để ước lượng tần suất cho cả nhóm đối tượng.

### Ví dụ đáp án đã ẩn danh

| Mã | Đáp án trong bản xuất | Câu |
|---|---|---|
| S01 | Tìm giá hoặc cân đối ngân sách | 6 |
| S02 | Tra thêm thông số, tài liệu hoặc nguồn khác | 7 |
| S05 | Nhờ người khác xác nhận | 7 |
| S07 | Kiểm tra xem các linh kiện có dùng được với nhau không | 6 |
| S07 | Lần đó tôi không kiểm tra xem các linh kiện có dùng được với nhau | 7 |
| S09 | Card đồ họa có vừa vỏ máy không | 8 |
| S12 | CPU có được bo mạch chủ (mainboard) hỗ trợ không | 8 |
| S15 | Tôi có kiểm tra và không phân vân | 8 |
| S16 | 0 lần | 9 |

Chín ví dụ là đáp án trắc nghiệm nguyên văn từ tám người qua sàng lọc. Giá/ngân sách được chọn là việc tốn thời gian nhất nhiều hơn rà tương thích. Bản xuất khảo sát chưa có số phút để kiểm mức tổn thất. [Dữ liệu khảo sát](survey/results.csv)

## Kết quả phỏng vấn

Ba người được phỏng vấn ngày 27/11/2026. Cả ba là sinh viên ngoài nhóm đã tự chọn ít nhất một linh kiện cho chiếc PC đầu tiên và kể chuyện trong vòng 30 ngày trước buổi hỏi. P2 đủ điều kiện vì đã tự chọn một linh kiện sau khi xem trên mạng, dù anh họ hỗ trợ lên cấu hình.

| Phiếu | Việc xảy ra | Có bước phát sinh do tương thích theo tiêu chí giả thuyết? |
|---|---|---|
| [P1](interviews/P1.md) | Phát hiện sai socket khi ráp thử và phải đổi mainboard. | Có |
| [P2](interviews/P2.md) | Rà lại cấu hình rồi mua, mọi thứ suôn sẻ. | Không ghi nhận |
| [P3](interviews/P3.md) | Đổi một linh kiện vì hết hàng rồi rà lại danh sách. | Không ghi nhận. Nguyên nhân được kể là hết hàng. |

**Kết quả 1/3 người**, dưới tiêu chí **2/3** đặt trước. P1 cho thấy sai tương thích có thể dẫn đến đổi linh kiện. Tỷ lệ 8/10 của khảo sát đo việc phát sinh theo câu trắc nghiệm. [Giả thuyết](hypothesis.md)

- P1 kể: “Mình tưởng khớp rồi, đến lúc ráp thử mới biết sai.” [Phiếu P1](interviews/P1.md)
- P3 kể: “Mất bao lâu thì mình không nhớ nổi.” [Phiếu P3](interviews/P3.md)

P2 không đồng ý trích nguyên văn.

Phiếu P1 ghi 2 lần và 40 phút, chưa xác định 40 phút có phải thời gian tăng thêm do đổi mainboard. P2 ghi 0 lần và 5 phút, chưa rõ 5 phút thuộc bước rà thường lệ hay phát sinh. P3 kể một lần đổi do hết hàng và không nhớ số phút. Chưa đủ số liệu cùng định nghĩa để tính impact theo phút/người/tháng.

## Xác nhận bổ sung cho CP4 · 28/11/2026

Nguồn là thông tin Dũng cung cấp sau khi hỏi lại P1–P3. Số CP3 ở trên được giữ để truy lịch sử. Kết quả phỏng vấn vẫn là **1/3 người báo vướng tương thích**. Thời lượng xác nhận của các buổi phỏng vấn ban đầu là **P1 20 phút, P2 20 phút, P3 25 phút**. Cả ba buổi dài hơn khoảng 10–15 phút trong hướng dẫn.

| Phiếu | Số lần trong 30 ngày | Thời gian lần gần nhất |
|---|---|---|
| [P1](interviews/P1.md) | **3 lần vướng tương thích**, cập nhật từ số 2 lần ghi tại CP3. | **Khoảng 30 phút phát sinh cho cả 3 lần** theo hồi tưởng. **40 phút** là tổng thời gian rà và xử lý ở lần gần nhất. P1 còn nhắc **khoảng 20 phút** khi nói về việc tra lại, chưa rõ thuộc lần nào. |
| [P2](interviews/P2.md) | **0 lần vướng tương thích**. | **5 phút rà thường lệ**, **0 phút phát sinh** ở lần được kể. |
| [P3](interviews/P3.md) | **1 lần đổi linh kiện do hết hàng**. Chưa ghi nhận vướng tương thích. | **10 phút tổng thời gian đổi linh kiện và rà lại**. Chưa tách được phần thời gian tăng thêm do hết hàng. |

**Impact thời gian do tương thích trong mẫu:** 1 người báo vướng × 3 lần trong 30 ngày × khoảng 10 phút trung bình/lần = **khoảng 30 phút trong 30 ngày**. Trung bình 10 phút/lần được tính từ tổng 30 phút P1 tự báo chia cho 3 lần. Chưa có thời gian tách riêng theo từng lần. Câu 9 khảo sát còn mâu thuẫn, nên chưa có căn cứ suy rộng tần suất, quy mô người gặp hoặc ROI.

## Bàn giao

- **Dương:** bàn giao 3 phỏng vấn đúng đối tượng, 1/3 có bước phát sinh do tương thích, 9 ví dụ khảo sát và 2 trích dẫn phỏng vấn. Khảo sát có 20 phản hồi, 10 qua sàng lọc, 8/10 báo phát sinh. Impact trong mẫu là khoảng 30 phút/30 ngày theo hồi tưởng của P1.
- **Thắng:** dùng 3 lần/30 ngày và trung bình khoảng 10 phút phát sinh/lần như số liệu tham chiếu của riêng P1. Mô phỏng hiện dùng quy mô 100/300/800 người dùng mỗi tháng và 1/2/4 lượt dùng mỗi người mỗi tháng theo persona. Ghi rõ đây là giả định mô phỏng. Câu 9 khảo sát hỏi số lần phát sinh do tương thích, có phản hồi mâu thuẫn và chưa đo lượt dùng công cụ. Chưa có số liệu về quy mô thực hoặc số phút tiết kiệm để chứng minh ROI. [Cấu hình persona](../cost/personas.yaml)
- **Khánh:** phiếu P1 gợi ý tình huống sai socket sau khi mua. Câu 8 của S01 (RAM), S09 (GPU–vỏ) và S12 (CPU–mainboard) gợi ý các tình huống khác. Dùng mã linh kiện và nguồn hãng ở Data Card cho các ca dựa trên thông số. [Data Card](../data/DATA_CARD.md)
