# Tổng hợp bằng chứng nhu cầu · CP2

Giả thuyết được ghi trước khi phỏng vấn ở [hypothesis.md](hypothesis.md). Người dùng mục tiêu là sinh viên ngoài nhóm đã tự chọn linh kiện cho máy tính để bàn lần đầu, ưu tiên lần chọn trong 30 ngày gần nhất.

## Tiến độ thu thập

| Nguồn | Tiến độ ghi nhận trong repo | Ngưỡng theo guide |
|---|---|---|
| Phỏng vấn | 0 bản ghi. Tình trạng đã liên hệ, đã hẹn hoặc đang chờ phản hồi chưa có ghi nhận. | Ít nhất 3 người đúng vai |
| Khảo sát | 8 phản hồi Google Forms ngày 27/11/2026. 4 chọn “Có” ở câu sàng lọc và trả lời đủ 9 câu trong bản xuất. | 4/20 người đúng vai, còn thiếu 16 |
| Đào dữ liệu hành vi | Chưa có tập dữ liệu hành vi đã phân tích | Có mẫu số, cách đếm chạy lại được và ví dụ có nguồn |

Bản phân tích dùng [CSV ẩn danh](survey/results.csv) và [bộ câu hỏi](survey/questions.md). CSV giữ nguyên các đáp án trắc nghiệm, bỏ dấu thời gian và gắn mã S01–S08 theo thứ tự dòng trong bản xuất. Câu 1 có 4 “Có”, 3 “Không” và 1 “Không chắc chắn”. Chỉ tính 4 người chọn “Có” cho kết quả dưới đây. Bản xuất có 9 câu, thiếu câu 10 về thời gian phát sinh. [Guide của BTC, bước 1.2](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/02-guide.md)

## Kết quả ban đầu

| Câu | Kết quả trong 4 phản hồi qua sàng lọc |
|---|---|
| Câu 2 · Lần chọn gần nhất | 1 trong 7 ngày qua, 1 cách đây 31–90 ngày, 2 hơn 90 ngày. |
| Câu 3 · Số nguồn | 1 tự đối chiếu, 1 dùng một nguồn, 2 dùng hai nguồn. |
| Câu 4 · Cách dựa vào chủ yếu | 3 chọn hỏi trợ lý AI, 1 chọn hỏi bạn bè, người có kinh nghiệm hoặc cộng đồng. |
| Câu 5 · Trạng thái danh sách | 2 đã chốt, 2 chốt một phần. |
| Câu 6 · Việc tốn thời gian nhất | Giá/ngân sách, hiệu năng, rà đúng mã và kiểm tương thích mỗi mục có 1 người chọn. |
| Câu 7 · Bước phát sinh | 2/4 chọn một bước phát sinh, gồm 1 tra thêm và 1 nhờ xác nhận. 2 chọn không kiểm. Cả 4 có đáp án, nên mẫu số theo quy tắc khảo sát là 4. |
| Câu 8 · Phần phân vân | CPU–mainboard, mainboard–RAM và GPU–vỏ mỗi mục 1 người chọn. 1 chọn có kiểm tra và không phân vân. |
| Câu 9 · Số lần trong 30 ngày | 1 chọn 0 lần, 3 chọn 2 lần. Hai trong ba dòng chọn 2 lần lại chọn lần rà gần nhất đã quá 30 ngày, nên chưa dùng số này để ước tính tần suất. |

Câu 7 của S01 và S07 ghi không kiểm tra, trong khi câu 3 và 8 có thông tin về việc kiểm tra. Giữ nguyên các dòng và báo x/N theo câu 7 như đã định. Hai điểm chưa nhất quán này, mẫu nhỏ và nhiều lần chọn đã lâu giới hạn cách diễn giải.

### Ví dụ đáp án đã ẩn danh

| Mã | Đáp án trong bản xuất | Câu |
|---|---|---|
| S01 | Tìm giá hoặc cân đối ngân sách | 6 |
| S02 | Tra thêm thông số, tài liệu hoặc nguồn khác | 7 |
| S05 | Nhờ người khác xác nhận | 7 |
| S07 | Kiểm tra xem các linh kiện có dùng được với nhau không | 6 |

Bốn ví dụ đến từ bốn phản hồi đủ điều kiện. Cần thêm nguồn hợp lệ để đạt ít nhất năm ví dụ. S02 và S05 cho thấy có người phải tra thêm hoặc nhờ xác nhận, phù hợp một phần với giả thuyết. Chưa đủ dữ liệu để kết luận độ phổ biến hoặc tính impact theo phút. Ngưỡng phỏng vấn của giả thuyết vẫn chờ ghi chép thật.

## Dẫn chứng kỹ thuật đã kiểm

- ASUS có hai phiên bản B760M-PLUS WIFI dùng DDR4 và DDR5 khác nhau. Tên “B760M” còn thiếu chi tiết để chốt một mã. [Bảng so sánh của ASUS](https://www.asus.com/us/product-compare?LevelId=Motherboards-Components-Motherboards&ProductID=22497%2C22366)
- ASUS ghi Ryzen 7 7800X3D được xác nhận từ BIOS 1409 trên TUF GAMING B650-PLUS WIFI. Socket khớp vẫn cần xem điều kiện BIOS. [Danh sách CPU hỗ trợ của ASUS](https://www.asus.com/us/supportonly/tuf%20gaming%20b650-plus%20wifi/helpdesk_cpu/)
- NZXT công bố H5 Flow (2024) hỗ trợ GPU dài tối đa 410 mm và ghi rõ radiator mặt trước có thể giảm khoảng trống. [Hướng dẫn của NZXT](https://support.nzxt.com/hc/en-us/articles/47061130443291-What-is-the-maximum-GPU-length-for-the-H5-Flow-2024)

Các nguồn hãng kiểm chứng quy tắc kỹ thuật và có thể dùng dựng ca thử cho Khánh. Tần suất người mới vướng từng tình huống vẫn là câu hỏi phỏng vấn.

## Cách thu thập và bàn giao

- Mỗi thành viên tìm người phù hợp ngoài nhóm. Dũng ghi vai, giờ hẹn và trạng thái thực tế, rồi tổng hợp theo mẫu [ghi chép phỏng vấn](interviews/TEMPLATE.md).
- Hỏi về lần chọn cấu hình gần nhất trước khi nhắc tới công cụ hay tương thích. Nếu được đồng ý, xin danh sách linh kiện đã bỏ tên, số điện thoại, mã đơn và thông tin riêng tư.
- Lưu trích dẫn nguyên văn khi được phép. Với mỗi người, ghi số lần gặp trong 30 ngày và thời gian lần gần nhất, hoặc ghi “không nhớ”. Đếm mỗi người đủ tiêu chí một lần và báo x/N theo số bản ghi thực tế.
- Số liệu khảo sát ban đầu đã cập nhật vào Canvas. Sau khi có ghi chép phỏng vấn thật, bổ sung mẫu số, số người gặp, trích dẫn đã ẩn danh và điều còn thiếu.
