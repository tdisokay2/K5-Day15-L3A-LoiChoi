# LoiChoi — Kiểm tra tương thích cấu hình PC trước khi mua

**Thành viên, lớp, track:** xem [TEAMS.md](TEAMS.md). **Điền TEAMS.md đúng format**: khi chấm và đánh giá, BTC quét file này để ghép điểm cho từng người.

*Lát cắt = kiểm tra danh sách linh kiện PC dự định mua theo catalog nhóm chuẩn bị ([data/components.json](data/components.json)) trên đúng 3 quan hệ: **CPU–mainboard** (socket, danh sách CPU hỗ trợ, điều kiện `min_bios`), **mainboard–RAM** (thế hệ DDR4/DDR5) và **GPU–vỏ máy** (chiều dài `mm` theo điều kiện lắp đặt `clearance_condition`).*

> **Giới hạn & lưu ý an toàn:**
> - **Phần chưa kiểm:** Nguồn (PSU) và đầu cấp nguồn, tản nhiệt CPU và khoảng trống lắp đặt, ổ đĩa/kết nối lưu trữ, kích thước form factor mainboard–vỏ máy, QVL/tốc độ/dung lượng/số thanh RAM, độ dày GPU và khoảng trống dây nguồn, giá bán/tồn kho/hiệu năng (FPS).
> - **Điều kiện & thiếu thông tin:** Khi thiếu mã, mơ hồ biến thể/revision, thiếu điều kiện `BIOS` hoặc `bố trí vỏ`, hoặc thiếu nguồn hãng, hệ thống trả trạng thái **Thiếu thông tin (`insufficient_info`)** và hỏi lại, không tự đoán.
> - **Không bảo đảm tương thích toàn bộ máy:** Trạng thái đạt chỉ có nghĩa *"Chưa phát hiện xung đột trong phạm vi đã kiểm"*; người mua cần xác nhận lại với hãng/người bán và tự quyết định.
> - **Dữ liệu mô phỏng (`synthetic`):** Nếu có linh kiện gắn `synthetic: true`, kết quả luôn kèm nhãn **"MÔ PHỎNG — không dùng để quyết định mua"**.

## Nhóm làm gì, khung làm gì

| Nhóm quyết định và viết | Khung làm sẵn (không cần sửa) |
|---|---|
| Người dùng, pain, bằng chứng, impact (`evidence/`, `spec.md` §1–§2) | — |
| Hình dạng giải pháp, công cụ, prompt, luồng (`spec.md` §4, `codebase/agent.py`, `tools.py`, `ai.py`) | Ghi mọi lần gọi model / công cụ vào trace, cộng token (`codebase/tracing.py`) |
| Bộ câu thử, metric, chuẩn "đạt" (`eval/benchmark.csv`, `eval/metric_spec.yaml`, `spec.md` §7) | Kiểm đủ cột, đủ câu `kho` / `tu_choi`, đủ ≥1/3 câu từ người dùng / data thật (`run.py check`) |
| Chấm cột `pass` theo metric spec | Chạy cả bộ một lệnh, có run ID, model, token từng câu (`run.py eval`) · tính % đạt (`run.py score`) |
| Persona, số người dùng thật, giá model (`cost/personas.yaml`) | Sinh ~50 phiên, chạy thật qua bản chạy thử, tính chi phí / phiên, / task thành công, / tháng 3 kịch bản (`run.py simulate`) |

*Ví dụ track A (ví dụ cỡ, không phải lời giải):* nhóm viết công cụ `search_lesson` tra bài pre-class đã đánh mã đoạn, luồng "tra đoạn → model trả lời kèm mã đoạn, không có thì nói không có", metric "mọi khẳng định có mã đoạn đúng", persona "ôn dồn trước kiểm tra". Khung chạy 25 câu thử ra `run-1.csv`, nhóm chấm `pass`, `score` in % đạt; `simulate` chạy 50 phiên ra chi phí / task thành công cho hai model.

## Chạy trong 3 phút

Bộ khung cần **Python 3.10 trở lên** (Python 3.9 có sẵn trên macOS vẫn chạy được, chỉ in một dòng nhắc). **Không cần `pip install`.**

**Bước 1 — Mở cửa sổ lệnh ngay trong thư mục repo**

| Windows (PowerShell) | macOS |
|---|---|
| Mở thư mục repo bằng File Explorer → bấm vào thanh địa chỉ → gõ `powershell` → Enter | Mở **Terminal** (Cmd + Space, gõ "Terminal") → gõ `cd ` (có dấu cách) → kéo thả thư mục repo vào → Enter |

Gõ `dir` (Windows) hoặc `ls` (macOS / Linux): thấy `run.py` và `README.md` là đang đứng đúng chỗ.

**Bước 2 — Kiểm Python và chạy thử**

| Việc | Windows (PowerShell) | macOS / Linux |
|---|---|---|
| Kiểm Python | `python --version` (không được thì `py --version`) | `python3 --version` |
| Chạy bản chạy thử (chế độ giả, chưa gọi model) | `python run.py` | `python3 run.py` |
| Kiểm bộ câu thử | `python run.py check` | `python3 run.py check` |
| Tạo file `.env` để nối model | `copy .env.example .env` | `cp .env.example .env` |

- Windows: gõ `python` mà mở Microsoft Store hoặc báo không có lệnh → dùng `py`. Chưa có Python: cài từ python.org, **tick "Add python.exe to PATH"**, mở lại PowerShell.
- macOS: báo `command not found: python` là bình thường → dùng `python3`.
- `python run.py` chạy từ thư mục gốc repo ở chế độ giả (`MODEL_PROVIDER=fake`, **không cần API key**, token vào/ra = `0`). Nối model thật (chặng CP3): [docs/connect-model.md](docs/connect-model.md).
- **Đầu vào mẫu chạy thử với `python run.py`** (dán nguyên dòng sau rồi nhấn Enter):
  - Ca đủ thông tin (chưa phát hiện xung đột trong phạm vi đã kiểm):
    `CPU: AMD Ryzen 7 7800X3D; Main: ASUS TUF GAMING B650-PLUS WIFI; RAM: Kingston KF556C40BBK2-32; GPU: MSI GeForce RTX 4060 VENTUS 2X BLACK 8G OC; Case: NZXT H5 Flow (2024); BIOS: 1409; bố trí vỏ: Không lắp radiator mặt trước`
  - Ca thiếu/mơ hồ (trả `Thiếu thông tin` và hỏi lại):
    `CPU: Ryzen 5 5600; Main: B760M; RAM: Kingston FURY Beast`

Trong README này lệnh viết là `python …`; máy nhóm cần `python3` hay `py` thì gõ thay.

## Lệnh

| Lệnh | Làm gì |
|---|---|
| `python run.py` | Chạy bản chạy thử (gõ đầu vào, nhận kết quả, kèm số lần gọi model / token) |
| `python run.py check` | Kiểm `eval/benchmark.csv` (6 cột, số câu, `kho` / `tu_choi`, mã `source`, ô trống, dòng mẫu) `eval/metric_spec.yaml` (≥3 metric điền đủ) và `TEAMS.md` (đúng format để BTC quét). Chỉ cảnh báo, không sửa file |
| `python run.py eval --try` | **Thử nối model:** chạy 3 câu đầu (`--try 5` = 5 câu) → `eval/run-try.csv`. Thấy "Nối model được" là xong. Không tính là một lượt |
| `python run.py eval` | Chạy cả bộ qua `codebase/agent.py` → `eval/run-1.csv` (lần sau `run-2.csv`…) + `traces/run-1.jsonl`. Mỗi dòng có run ID, model, số lần gọi model / công cụ, token. Model còn giả → chỉ ghi `run-mock.csv`; mọi câu lỗi → `run-error.csv`; Ctrl+C → `run-stopped.csv` — đều **không** được đánh số |
| `python run.py eval --fake` | Thử riêng bộ chạy, không gọi agent → `eval/run-fake.csv` |
| `python run.py score eval/run-1.csv` | Sau khi điền cột `pass` (1 / 0): in % đạt tổng và theo `type`. Còn ô trống → "CHƯA CHẤM XONG", không in % |
| `python run.py simulate --try` | Thử mô phỏng chi phí 10 phiên (làm trước CP3) → `cost/simulate-try.csv` |
| `python run.py simulate` | Mô phỏng chi phí khi dùng thật theo `cost/personas.yaml` (≥50 phiên) → `cost/simulate-N.csv` + `cost/simulate-N-summary.md` |
| `python run.py simulate --rate-from eval/run-2.csv` | Như trên, lấy tỉ lệ đạt từ đúng lượt chỉ định. Không ghi thì khung lấy lượt `run-N` mới nhất đã chấm, cùng model, và ghi rõ đã lấy lượt nào trong bản tóm tắt |

Gói miễn phí báo hết lượt: thêm `--wait 4` sau `eval` hoặc `simulate` (nghỉ 4 giây giữa hai lượt gọi). Sửa CSV bằng Excel: *File → Save As → CSV UTF-8*; Google Sheets: *Tệp → Tải xuống → CSV*.

**Lượt có lỗi kỹ thuật** (cột `error` có chữ): không sửa tay file đó, chạy lại thành lượt mới và ghi vào bảng các lượt ở `eval/README.md`. Không xoá file lượt nào.

Nhóm dùng stack khác (Node, Streamlit, notebook…): sửa hàm `run_app()` trong `run.py` để `python run.py` vẫn chạy được bản chạy thử, và giữ `answer()` trong `codebase/agent.py` để `eval`, `simulate` chạy được.

## Bản chạy thử — viết ở đâu

| File | Viết gì | Bước guide |
|---|---|---|
| `codebase/agent.py` | `answer(text)` — luồng chính, đúng hình dạng ở `spec.md` §4. Khung có sẵn một workflow 2 bước *ví dụ* | 3.2 |
| `codebase/tools.py` | Công cụ của bài toán, mỗi công cụ một hàm có `@tool` | 2.2, 3.2 |
| `codebase/ai.py` | `call_model(system, user)` — chỗ duy nhất gọi model. Chưa điền `.env` thì chạy **chế độ giả** | 3.3 |

- **Trước CP2:** để chế độ giả, công cụ trả dữ liệu giả — `python run.py` đi hết luồng là đủ.
- **CP3 · bước 01 ([issue #12](https://github.com/tdisokay2/K5-Day15-L3A-LoiChoi/issues/12)):** `codebase/ai.py` đã có kết nối OpenRouter bằng thư viện chuẩn. Cấu hình `.env`: `MODEL_PROVIDER=openrouter`, `MODEL_NAME=openai/gpt-4.1-mini`, `API_KEY=<key riêng>`. Biến môi trường được ưu tiên hơn `.env`; bỏ giá trị `MODEL_PROVIDER=fake` đã đặt ở terminal khi thử API thật. Các ví dụ hãng khác trong [docs/connect-model.md](docs/connect-model.md) chưa được triển khai. 35/35 kiểm thử cục bộ đạt với HTTP giả lập; đã xác nhận API/token thật, xem trạng thái thử kỹ thuật bên dưới. Chưa có lượt đánh giá chính thức.
- Bộ chạy gửi **nguyên ô `input`** của câu thử vào `answer(text)`. Dữ liệu nền (bài học, thông báo, lịch…) để trong `data/`, đọc qua công cụ.

## Phần nào thật, phần nào giả

| Thành phần | Thật / Giả | Ghi chú |
|---|---|---|
| Lời gọi AI nhận diện ở CP2 (`codebase/ai.py`) | **Giả** (`MODEL_PROVIDER=fake`, token = `0`) | Mô phỏng trích tên/mã bằng quy tắc, chưa gọi model AI thật; bắt buộc nối model thật qua `.env` từ CP3 |
| Kết nối OpenRouter CP3 (`codebase/ai.py`) | **Đã xác nhận CLI và 3 câu thử API thật** | Chọn `openai/gpt-4.1-mini`; CLI thật dùng 279/165 token. Dương chạy `eval --try` B01–B03: tổng 831 token vào/484 token ra, CSV và trace khớp, không có lỗi kỹ thuật. `eval/run-try.csv` và `traces/run-try.jsonl` hiện là lượt Mini, khung đã ghi đè lượt Nano khi người dùng chạy lại. Đây là thử kết nối, chưa chấm benchmark chính thức. Tên viết tắt và điều kiện vỏ khác cách diễn đạt vẫn cần rà ở bước tích hợp |
| Catalog linh kiện (`data/components.json`) | **Thật** | Thông số kỹ thuật và link nguồn hãng do nhóm thu thập, kiểm chéo thủ công |
| Công cụ tra cứu & kiểm tra (`codebase/tools.py`) | **Thật** | `lookup_components` và `check_compatibility` chạy bằng code Python thuần trên catalog cục bộ |
| Luồng chính (`codebase/agent.py`) | **Thật** | Workflow cố định: nhận diện → tra cứu → xác thực id → checker → hiển thị có căn cứ |
| Tích hợp CP3 · bước 06 ([#17](https://github.com/tdisokay2/K5-Day15-L3A-LoiChoi/issues/17)) | **Đã smoke test model thật** | Alias duy nhất được lookup xác thực; tên gần đúng/mơ hồ vẫn hỏi lại. Code nhận cách nói tương đương hẹp về không lắp radiator trước, giữ context gốc trong fact. Model không đổi kết luận hoặc thêm URL |
| Đánh giá model thật (`eval/run-1.csv`) | **Thật** (`openai/gpt-4.1-mini`) | Lượt 1 `run-1@20261128-005643`: `16/25` (64%), 0 lỗi; chưa đạt chuẩn §7 (`≥80%` và 0 sót xung đột) |
| Thử mô phỏng chi phí 10 phiên (`simulate --try`) | **Thật** (`simulate-try@20261128-033519`) | 10 phiên trên `openai/gpt-4.1-mini` (`--rate-from eval/run-1.csv`): 24 lượt gọi, 9.520 token vào / 2.680 token ra, 0/10 lỗi. Đây là chạy thử CP3, chưa phải bản `≥50` phiên / CP4 |
| Mô phỏng chi phí ≥50 phiên & slide | **Chưa triển khai** | Hoàn thiện ở chặng CP4 |

### Video demo CP3 (~30 giây)

- **Model:** `openai/gpt-4.1-mini` (cùng model lượt 1) · **Kịch bản:** [docs/cp3-demo.md](docs/cp3-demo.md)
- **Link video (YouTube Không công khai):** https://youtu.be/syBKNhpcIIE

**Bàn giao bước 06:** 44/44 unittest đạt; `python run.py check` không cảnh báo (25 câu, 5 metric, 4 thành viên). Smoke mới nhất: [`smoke-cp3-17-20261127T174226Z`](traces/smoke-cp3-17-20261127T174226Z.jsonl), 7 ca Mini thật, tổng 2764 token vào/748 token ra, không lỗi kỹ thuật; CLI thật 433/193 token tại [biên bản CLI](traces/cli-cp3-17-20261127T174307Z.jsonl). Giữ [lượt smoke trước sửa](traces/smoke-cp3-17-20261127T174105Z.jsonl) để truy lỗi điều kiện radiator. Lỗi API/tools/JSON được kiểm bằng giả lập trong unittest, không mô tả là lỗi API thật. Đây chưa phải lượt đánh giá chính thức hoặc tỷ lệ đạt. **B15 còn thiếu kết luận xung đột do tên viết tắt quá ngắn chưa xác thực được**; giữ nguyên expected để đánh giá. Catalog `09fac5b`, benchmark đã chốt `15183c9`; bàn giao SHA code tại commit hoàn thành issue #17.

## Dùng AI vào việc gì

Nhóm sử dụng coding agent (Claude Code / Antigravity / Codex) để hỗ trợ viết và kiểm tra mã nguồn `codebase/` theo thiết kế ở `spec.md`, rà soát câu chữ tài liệu và cấu trúc câu thử; không dùng AI để bịa phỏng vấn, khảo sát hay sửa kết quả chạy. Mọi thay đổi mã nguồn, nguồn hãng trong `data/components.json` và bộ câu thử đều do các thành viên (Dương, Dũng, Khánh, Thắng) tự đọc, chạy thử và kiểm duyệt trước khi commit. Chi tiết: [docs/ai-usage.md](docs/ai-usage.md). Coding agent đọc [AGENTS.md](AGENTS.md).

## File mẫu — điền ở bước nào

| File | Điền ở bước guide | Mốc |
|---|---|---|
| `TEAMS.md` | 1.0 | CP1 · **đúng format**, BTC quét khi chấm |
| `canvas.md` | 1.4 | CP1, cập nhật CP2 |
| `evidence/hypothesis.md` | 1.1 | trước khi tìm bằng chứng |
| `evidence/data-mining.md` · `evidence/interviews/TEMPLATE.md` → `P1.md`… · `evidence/survey/TEMPLATE.md` | 1.2 | bắt đầu sau Zoom, xong CP3 |
| `evidence/summary.md` | 1.2 | CP3 |
| `spec.md` | §0–§2: 1.1–1.3 · §3–§5: 2.1–2.3 · §7: 2.4 · §8: 4.2 · §10: suốt | §7 chốt CP2 · §0–§7 CP3 · đủ CP4 |
| `data/DATA_CARD.md` | 2.4 | bản đầu CP2 |
| `eval/benchmark.csv` · `eval/metric_spec.yaml` | 2.4 | ≥10 câu + metric chốt CP2 · 20–30 câu CP3 |
| `codebase/` | 3.2, 3.3 | khung CP2 · AI thật CP3 |
| `eval/report.md` · `eval/README.md` | 4.1 (README mục 1–4 từ 2.4) | CP4 |
| `cost/personas.yaml` · `cost/cost-estimate.md` | 4.2 | thử 10 phiên CP3 · đủ CP4 |
| `validation/log.md` *(bonus)* | 4.3 | CP4 |
| `slides/outline.md` → `demo-slides.pdf` | 5.1 | CP4 |
| `reflection/TEMPLATE.md` → `reflection/<ten>.md` | 5.3 | 23:59 Thứ Bảy 28/11 |
| `AGENTS.md` · `docs/ai-usage.md` | khi dùng coding agent / AI | suốt |

## Bảy hạng mục bắt buộc — nằm ở file nào

| # | Hạng mục | File |
|---|---|---|
| 1 | Bằng chứng pain | `evidence/` (tổng hợp ở `evidence/summary.md`) |
| 2 | Impact có số | `spec.md` §2 |
| 3 | Thiết kế giải pháp | `spec.md` §4 |
| 4 | Bản chạy thử làm trọn lát cắt | `codebase/` · lệnh ở mục "Lệnh" |
| 5 | Định nghĩa "tốt" + bộ câu thử | `data/DATA_CARD.md` · `eval/` |
| 6 | Mô phỏng chi phí khi dùng thật | `cost/` |
| 7 | Slide + demo + video dự phòng | slide trong repo (PDF, PPTX, HTML…) hoặc link slide ở form CP4 · link video: https://youtu.be/syBKNhpcIIE |
| + | *Bonus:* người dùng thử | `validation/log.md` |
