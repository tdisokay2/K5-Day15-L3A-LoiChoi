# Video demo CP4 (~1 phút 31 giây) — LoiChoi

- **Link video (YouTube Không công khai):** https://youtu.be/CnhJdD9oC0c — đã kiểm xem được không cần đăng nhập (28/11/2026).
- **Bản chạy:** `python run.py` trên nhánh `CP4`, code agent `443b6dc` (sau cải tiến #24 và bỏ ví dụ trùng câu thử), catalog `09fac5b`.
- **Model:** `openai/gpt-4.1-mini` qua OpenRouter — cùng model với lượt 1 (`run-1@20261128-005643`) và lượt 2 (`run-2@20261128-123026`).
- **Người quay:** Nguyễn Khắc Khánh, ngày 28/11/2026. Không dựng hay sửa output.
- **Video CP3** (`https://youtu.be/syBKNhpcIIE`, xem [cp3-demo.md](cp3-demo.md)) giữ làm lịch sử / dự phòng thứ hai; kết quả B01 và B07 trong video đó không đổi ở bản CP4.

## Kịch bản quay

Dán lần lượt vào `python run.py`:

| # | Đầu vào | Cho thấy |
|---|---|---|
| 1 | Cấu hình B01 (Ryzen 5 5600 + TUF GAMING B650-PLUS WIFI + KF556C40BBK2-32 + RTX 4060 VENTUS 2X BLACK 8G OC + H5 Flow 2024, không radiator trước) | Ca thường: `Có xung đột` AM4/AM5, căn cứ + URL hãng, mục Chưa kiểm |
| 2 | Cấu hình B15 viết tắt ("r5 5600 + main b650 tuf wifi + …") | Kết quả cải tiến CP4: nhận diện tên viết tắt, báo 2 xung đột (lượt 1 bỏ sót) |
| 3 | B07 ("Main ASUS B760M với RAM Kingston KF432C16BBK2/16 …") | Ca khó: hỏi lại 2 biến thể B760M, không chọn ngầm |
| 4 | B14 ("Chọn giúp mình bộ máy chơi game 20 triệu …") | Giới hạn: từ chối phần ngoài phạm vi (giá, FPS, đặt hàng) |

Đây là kịch bản đã chuẩn bị trước khi quay; người xem đối chiếu nội dung thực tế trên video.

## An toàn

Yêu cầu khi quay: không mở nội dung `.env`, không hiển thị API key hay thông tin cá nhân.
