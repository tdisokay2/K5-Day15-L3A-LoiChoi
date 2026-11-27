# Data Card · Danh mục linh kiện CP3

| Mục | Nội dung |
|---|---|
| Tệp | [components.json](components.json), schema 1.0 theo spec §4 |
| Phiên bản bàn giao | Catalog từ bản main sau PR #11 (`b19d28f`), rà lại ngày 27/11/2026 cho lượt 1. Git blob `4ccbca2b5b1f184bfdb2a1c35ddab45a3a86e7c6`. Khi chạy lượt 1, đối chiếu bằng `git hash-object data/components.json` và ghi SHA bản chạy cùng run ID. |
| Dùng để làm gì | Tra tên và biến thể, đối chiếu CPU–mainboard, mainboard–RAM và GPU–vỏ. Có thể dùng để viết ca thử cho ba phép kiểm. |
| Nguồn | Trang thông số hoặc hỗ trợ công khai của AMD, ASUS, Kingston, MSI, NZXT và Fractal Design. Mỗi bản ghi liệt kê URL, ngày truy cập và trường có căn cứ. |
| Xử lý | Chọn đúng model, đối chiếu nguồn theo từng trường, chuẩn hóa socket và DDR, ghi chiều dài theo mm, giữ mã BIOS ở dạng chuỗi, và ghi rõ điều kiện lắp đặt của vỏ. Alias chung “B760M” và “Kingston FURY Beast” chủ ý trả nhiều ứng viên. |
| Số dòng | 12 linh kiện gồm 3 CPU, 3 mainboard, 2 RAM, 2 GPU và 2 vỏ. |
| Ngày tra nguồn | 27/11/2026 |
| Nhãn | 12 bản ghi thông số hãng (`synthetic: false`), 0 bản ghi mô phỏng. Danh mục không chứa dữ liệu cá nhân. |
| Giới hạn | Danh mục nhỏ, chỉ có một dòng CPU/BIOS được trích từ danh sách hỗ trợ. Tất cả danh sách CPU của mainboard đều được đánh dấu chưa đầy đủ. Hai mainboard B760M có `cpu_support: null`. Mỗi vỏ lưu một điều kiện bố trí có nguồn. |

## Kết quả rà nguồn CP3

| Model trong catalog | Thông số đối chiếu | Nguồn hãng |
|---|---|---|
| Ryzen 5 5600 | AM4 | [AMD](https://www.amd.com/en/support/downloads/drivers.html/processors/ryzen/ryzen-5000-series/amd-ryzen-5-5600.html) |
| Ryzen 5 7600 | AM5 | [AMD](https://www.amd.com/en/products/processors/desktops/ryzen/7000-series/amd-ryzen-5-7600.html) |
| Ryzen 7 7800X3D | AM5 | [AMD](https://www.amd.com/en/products/processors/desktops/ryzen/7000-series/amd-ryzen-7-7800x3d.html) |
| TUF GAMING B650-PLUS WIFI | AM5, DDR5, 7800X3D xác nhận từ BIOS 1409 trên mọi PCB trong bảng hỗ trợ | [Thông số ASUS](https://www.asus.com/us/motherboards-components/motherboards/tuf-gaming/tuf-gaming-b650-plus-wifi/techspec/) · [CPU Support ASUS](https://www.asus.com/us/supportonly/tuf%20gaming%20b650-plus%20wifi/helpdesk_cpu/) |
| TUF GAMING B760M-PLUS WIFI D4 | LGA1700, DDR4 | [ASUS](https://www.asus.com/us/motherboards-components/motherboards/tuf-gaming/tuf-gaming-b760m-plus-wifi-d4/techspec/) |
| TUF GAMING B760M-PLUS WIFI | LGA1700, DDR5 | [ASUS](https://www.asus.com/us/motherboards-components/motherboards/tuf-gaming/tuf-gaming-b760m-plus-wifi/techspec/) |
| KF432C16BBK2/16 | DDR4 | [Kingston](https://www.kingston.com/unitedkingdom/en/memory/search/?partid=KF432C16BBK2%2F16) |
| KF556C40BBK2-32 | DDR5 | [Kingston](https://www.kingston.com/en/memory/search?partId=KF556C40BBK2-32) |
| GeForce RTX 4060 VENTUS 2X BLACK 8G OC | 199 mm | [MSI](https://www.msi.com/Graphics-Card/GeForce-RTX-4060-VENTUS-2X-BLACK-8G-OC/Specification) |
| PROART-RTX4080S-O16G | 300 mm | [ASUS](https://www.asus.com/my/motherboards-components/graphics-cards/proart/proart-rtx4080s-o16g/techspec/) |
| H5 Flow (2024) | 410 mm khi không lắp radiator mặt trước | [NZXT](https://support.nzxt.com/hc/en-us/articles/47061130443291-What-is-the-maximum-GPU-length-for-the-H5-Flow-2024) |
| Terra | 200 mm khi lắp radiator 120 mm | [Fractal Design](https://support.fractal-design.com/support/solutions/articles/4000194849) |

H5 Flow ghi `revision: "2024"` theo phiên bản hãng. Các model còn lại được xác định bằng mã sản phẩm và để `revision: null` khi chưa ghi nhận một revision riêng. Hậu tố `D4`, `OC` và các dấu phân tách trong mã RAM được giữ nguyên. NZXT xác nhận 425 mm trong hướng dẫn H5 Flow cũ là lỗi in, nên giữ 410 mm với điều kiện trên. Mức 322 mm của Terra dùng cho bố trí khác mức 200 mm trong catalog. [Đính chính NZXT](https://support.nzxt.com/hc/en-us/articles/47061130443291-What-is-the-maximum-GPU-length-for-the-H5-Flow-2024) · [Các mức của Terra](https://support.fractal-design.com/support/solutions/articles/4000194849)

## Lưu ý khi tích hợp

- CPU–mainboard: dùng BIOS `1409` cho ca khớp chính xác. Với BIOS khác, checker cần căn cứ của hãng để xác định thứ tự phiên bản. Ryzen 5 7600 chưa được trích vào catalog vì hợp đồng hiện tại chưa biểu diễn điều kiện “all BIOS”. [Danh sách CPU hỗ trợ của ASUS](https://www.asus.com/us/supportonly/tuf%20gaming%20b650-plus%20wifi/helpdesk_cpu/)
- GPU–vỏ: checker đối chiếu chuỗi điều kiện bố trí sau chuẩn hóa. Catalog lưu một bố trí mỗi vỏ. Khi chưa xác nhận đúng điều kiện, trả thiếu thông tin theo §4. [Hợp đồng và quy tắc](../spec.md#4-thiết-kế-guide-22-32)

## Cặp dữ liệu cho ca thử

| Cặp / đầu vào | Kịch bản có thể kiểm bằng dữ liệu |
|---|---|
| Ryzen 5 5600 + TUF GAMING B650-PLUS WIFI | Xung đột AM4 và AM5 |
| Ryzen 7 7800X3D + TUF GAMING B650-PLUS WIFI | Có căn cứ ở BIOS 1409, thiếu thông tin khi BIOS chưa được xác nhận |
| B760M + KF432C16BBK2/16 | Hỏi đúng biến thể main. Bản D4 khớp thế hệ DDR, bản DDR5 xung đột. |
| MSI RTX 4060 VENTUS 2X BLACK 8G OC + H5 Flow (2024) | 199 mm trong giới hạn 410 mm, với điều kiện bố trí đã nêu |
| ASUS PROART-RTX4080S-O16G + Terra | 300 mm vượt giới hạn 200 mm khi vỏ có radiator 120 mm |
| MSI RTX 4060 VENTUS 2X BLACK 8G OC + Terra | 199 mm dưới giới hạn 200 mm đúng 1 mm khi có radiator 120 mm. Cặp này chỉ kiểm chiều dài. |
| ASUS PROART-RTX4080S-O16G + Terra, người dùng ghi bố trí không lắp radiator | Catalog chưa lưu giới hạn cho bố trí người dùng đưa. Nguồn Fractal giải thích 322 mm và 200 mm áp dụng ở hai bố trí. Checker cần trả thiếu thông tin ở cặp này theo catalog hiện tại. |

Bàn giao Khánh: dùng bảng nguồn để đối chiếu các ca dựng từ thông số hãng (`data_that`). Nếu dựng riêng ca đúng bằng ngưỡng bằng số tự tạo, ghi nguồn theo cách dựng thực tế. Bảng này kiểm căn cứ kỹ thuật. Dữ liệu về nhu cầu, tần suất và thời gian nằm trong hồ sơ bằng chứng. [Bằng chứng nhu cầu](../evidence/summary.md)
