# Người dùng thử · CP4

**Các phiên thử:** ngày **28/11/2026**, ba sinh viên ngoài nhóm LoiChoi trực tiếp thao tác. Mỗi buổi kéo dài **20 phút**, dài hơn thời lượng khoảng 10 phút/người trong hướng dẫn của issue #28. Ngày và thời lượng do Dũng xác nhận.

**Bản đã thử:** Dũng xác nhận cả ba dùng bản dòng lệnh `python run.py`. Thắng xác nhận code bản chính thức ở `7ab87c5`, mốc bàn giao CP4 `36c1d07`. Bản này kiểm CPU–mainboard, mainboard–RAM và GPU–vỏ. PSU nằm ngoài phạm vi. [Phạm vi trong spec](../spec.md#4-thiết-kế-guide-22-32)

**Đính chính ghi chép:** Dũng xác nhận các chi tiết về nút bấm, bảng cuộn ngang và kết luận công suất PSU là ghi nhầm. Các chi tiết đó cùng nhận định dựa trên màu sắc hoặc bố cục đã được bỏ khỏi kết quả bên dưới. Dũng xác nhận U1 và U2 đồng ý lưu câu nói nguyên văn.

## Đối chiếu nhánh CP2 và CP3

- **CP2 (`5ee93db`):** chạy dòng lệnh với model giả. Tài liệu có ghi một buổi thử tay prompt trên ChatGPT web do Khánh thực hiện để kiểm cách chấm metric. Log người dùng thử của nhánh vẫn là mẫu trống. [Bản chạy CP2](https://github.com/tdisokay2/K5-Day15-L3A-LoiChoi/blob/5ee93db/codebase/app.py) · [Buổi thử tay CP2](https://github.com/tdisokay2/K5-Day15-L3A-LoiChoi/blob/5ee93db/eval/thu-tay/log.md)
- **CP3 (`11260ef`):** demo dùng `python run.py` trong terminal với model thật. Log người dùng thử vẫn là mẫu trống. Ba hồ sơ P1–P3 ghi phỏng vấn về quá trình chọn linh kiện. [Kịch bản demo CP3](https://github.com/tdisokay2/K5-Day15-L3A-LoiChoi/blob/11260ef/docs/cp3-demo.md) · [Log trên CP3](https://github.com/tdisokay2/K5-Day15-L3A-LoiChoi/blob/11260ef/validation/log.md)

Lịch sử hai nhánh chưa có log các buổi của U1–U3. Nguồn xác nhận họ đã dùng bản CLI là thông tin Dũng cung cấp ngày 28/11/2026.

## Ghi chép sau đính chính

Đầu vào dưới đây là phần mô tả cấu hình từ ghi chép, chưa có lệnh nhập hay output nguyên văn. Mức nghiêm trọng là đánh giá của người tổng hợp.

| Người thử | Việc giao | Hành vi và phản hồi ghi được | Mức nghiêm trọng |
|---|---|---|---|
| U1 · Sinh viên năm nhất, chọn linh kiện PC đầu tiên | Rà trước khi mua và nói sẽ làm gì tiếp. Cấu hình mô tả CPU AMD AM5, mainboard AM4, RAM DDR4, nguồn 450 W và GPU tầm trung. | Bắt đầu từ CPU. Hiểu từ socket là ổ cắm điện và hỏi lại một lần. Biết cấu hình có vấn đề nhưng chưa rõ nên kiểm lại CPU hay mainboard trước, định hỏi người quen. Tự đánh giá tin khoảng 70% và muốn thấy nguồn. Hơi tiếc nếu mất công cụ. | **Vừa**, do cần trợ giúp để hiểu thuật ngữ và bước tiếp theo. |
| U2 · Sinh viên năm ba, nâng cấp PC cũ | Giữ mainboard, thay GPU và cân nhắc nguồn 550 W. | Bắt đầu với GPU và tự tra công suất bên ngoài, không cần trợ giúp. Muốn có thông số và căn cứ để chọn nguồn. Hơi tiếc nếu mất công cụ. | **Thấp** trong phiên thử. Người dùng tự tìm thông tin nằm ngoài phạm vi kiểm của công cụ. |
| U3 · Sinh viên năm hai, chọn linh kiện theo ngân sách | Rà một cấu hình được mô tả là tương thích, có nguồn 500 W không rõ hãng. | Nhập linh kiện theo thứ tự giá từ thấp đến cao. Khi hỏi lại, U3 chưa phân biệt rõ kết quả kiểm tương thích với quyết định có nên mua. Không sao nếu mất công cụ. Chưa đối chiếu được cách U3 diễn giải dòng kết quả CLI cụ thể. | **Vừa** theo phản hồi sau buổi thử. Cần làm rõ giới hạn của kết luận trước khi mua. |

### Trích dẫn được phép lưu

- U1: “Nó báo lỗi rồi nhưng mình vẫn không biết nên đổi cái nào.”
- U2: “Cho mình xem nó tính ra bao nhiêu W thì mình mới yên tâm.”

## Tổng hợp để bàn giao

- **Chủ đề lặp:** U1 và U2 muốn biết căn cứ. U1 và U3 gặp khó khi hiểu thuật ngữ hoặc dùng kết luận để quyết định bước tiếp theo.
- **Trước demo:** nói rõ phạm vi ba cặp ngay khi đọc kết quả, giải thích socket là chuẩn chân cắm giữa CPU và mainboard và chỉ ra cặp cần kiểm lại. Khi được hỏi về nguồn, nêu PSU nằm ngoài phạm vi.
- **Giữ:** kết luận theo từng cặp đi kèm căn cứ, để người dùng biết điểm nào cần đối chiếu.
- **Để sau:** đánh giá riêng nhu cầu tính công suất nguồn. Nếu đổi code sau lượt 2, chuyển góp ý cho Dương và Khánh để ghi changelog và kiểm lại bản sửa.

**Nội dung bàn giao:** Khánh có thể dẫn log ở mục 4 của báo cáo đánh giá để ghi hai điểm còn lại là cách giải thích thuật ngữ và phạm vi kết luận. Thắng có thể dùng hai điểm này khi thuyết minh demo và slide. Các quan sát áp dụng cho bản đã thử.
