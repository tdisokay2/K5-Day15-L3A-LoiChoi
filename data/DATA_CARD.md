# Data Card · Danh mục linh kiện CP2

| Mục | Nội dung |
|---|---|
| Tệp | [components.json](components.json), schema 1.0 theo spec §4 |
| Dùng để làm gì | Tra tên và biến thể, đối chiếu CPU–mainboard, mainboard–RAM và GPU–vỏ. Có thể dùng để viết ca thử cho ba phép kiểm. |
| Nguồn | Trang thông số hoặc hỗ trợ công khai của AMD, ASUS, Kingston, MSI, NZXT và Fractal Design. Mỗi bản ghi liệt kê URL, ngày truy cập và trường có căn cứ. |
| Xử lý | Chọn đúng model, đối chiếu nguồn theo từng trường, chuẩn hóa socket và DDR, ghi chiều dài theo mm, giữ mã BIOS ở dạng chuỗi, và ghi rõ điều kiện lắp đặt của vỏ. Alias chung “B760M” và “Kingston FURY Beast” chủ ý trả nhiều ứng viên. |
| Số dòng | 12 linh kiện gồm 3 CPU, 3 mainboard, 2 RAM, 2 GPU và 2 vỏ. |
| Ngày tra nguồn | 27/11/2026 |
| Nhãn | 12 bản ghi thông số hãng, đều có `synthetic: false`. Danh mục không chứa dữ liệu cá nhân. |
| Giới hạn | Danh mục nhỏ, chỉ có một dòng CPU/BIOS được trích từ danh sách hỗ trợ. Tất cả danh sách CPU của mainboard đều được đánh dấu chưa đầy đủ. Hai mainboard B760M có `cpu_support: null`. Mỗi vỏ lưu một điều kiện bố trí có nguồn. |

## Lưu ý khi tích hợp

- `TUF GAMING B650-PLUS WIFI` có dòng hỗ trợ Ryzen 7 7800X3D từ BIOS `1409` trên mọi PCB theo ASUS. Dùng `1409` cho ca khớp chính xác. Với BIOS khác, cần căn cứ của hãng để xác định thứ tự phiên bản. Catalog CP2 chưa biểu diễn điều kiện hãng ghi “all BIOS”; vì vậy dòng Ryzen 5 7600 chưa được đưa vào phần trích CPU hỗ trợ. [Danh sách CPU hỗ trợ của ASUS](https://www.asus.com/us/supportonly/tuf%20gaming%20b650-plus%20wifi/helpdesk_cpu/)
- `KF432C16BBK2/16` là DDR4, `KF556C40BBK2-32` là DDR5. Giữ nguyên dấu gạch chéo và dấu gạch nối trong mã hãng. [Kingston DDR4](https://www.kingston.com/unitedkingdom/en/memory/search/?partid=KF432C16BBK2%2F16) · [Kingston DDR5](https://www.kingston.com/en/memory/search?partId=KF556C40BBK2-32)
- H5 Flow (2024) lưu 410 mm khi không lắp radiator mặt trước. Terra lưu 200 mm khi có radiator 120 mm. Khi chưa xác nhận đúng điều kiện, kết quả GPU–vỏ là thiếu thông tin. [Điều kiện của NZXT](https://support.nzxt.com/hc/en-us/articles/47061130443291-What-is-the-maximum-GPU-length-for-the-H5-Flow-2024) · [Điều kiện của Fractal Design](https://support.fractal-design.com/support/solutions/articles/4000194849)

## Cặp dữ liệu cho ca thử

| Cặp / đầu vào | Kịch bản có thể kiểm bằng dữ liệu |
|---|---|
| Ryzen 5 5600 + TUF GAMING B650-PLUS WIFI | Xung đột AM4 và AM5 |
| Ryzen 7 7800X3D + TUF GAMING B650-PLUS WIFI | Có căn cứ ở BIOS 1409, thiếu thông tin khi BIOS chưa được xác nhận |
| B760M + KF432C16BBK2/16 | Hỏi đúng biến thể main. Bản D4 khớp thế hệ DDR, bản DDR5 xung đột. |
| MSI RTX 4060 VENTUS 2X BLACK 8G OC + H5 Flow (2024) | 199 mm trong giới hạn 410 mm, với điều kiện bố trí đã nêu |
| ASUS PROART-RTX4080S-O16G + Terra | 300 mm vượt giới hạn 200 mm khi vỏ có radiator 120 mm |

Các cặp trên dùng để đối chiếu từng quy tắc trong §4. Dữ liệu này chưa dùng để đo nhu cầu, tỷ lệ gặp khó hoặc thời gian người dùng bỏ ra.
