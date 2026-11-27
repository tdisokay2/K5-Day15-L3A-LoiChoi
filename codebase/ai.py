"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    mô phỏng trích tên/mã bằng quy tắc, model "fake", token 0; không kiểm tương thích.
    Hỗ trợ danh sách phân cách bằng dấu ;/dấu phẩy, nhãn CPU:/RAM:..., hoặc JSON components.
    Không phải khả năng hiểu ngôn ngữ của model thật; không đọc benchmark hay tự sinh thông số.
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import os
import json
import re
import unicodedata

try:
    from tracing import model_call
except ImportError:
    from .tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


# Khi chủ động chọn fake, không cần mở .env hoặc đọc khóa của nhà cung cấp.
if (os.environ.get("MODEL_PROVIDER") or "").strip().lower() != "fake":
    load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


def _plain(text):
    text = text.lower().replace("đ", "d")
    return "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c))


def _kind(label):
    label = _plain(label).strip()
    aliases = {"cpu": "cpu", "processor": "cpu", "vi xu ly": "cpu",
               "main": "mainboard", "mainboard": "mainboard", "motherboard": "mainboard", "bo mach chu": "mainboard",
               "ram": "ram", "bo nho": "ram", "gpu": "gpu", "vga": "gpu", "card": "gpu",
               "card do hoa": "gpu", "vo": "case", "vo may": "case", "case": "case"}
    return aliases.get(label)


def _fake_extract(text):
    context = {"bios_version": None, "case_clearance_condition": None}
    mentions = []
    try:
        structured = json.loads(text)
    except ValueError:
        structured = None
    if isinstance(structured, dict) and isinstance(structured.get("components"), dict):
        supplied_context = structured.get("context", {})
        if isinstance(supplied_context, dict):
            for key in context:
                value = supplied_context.get(key)
                if value is not None and not isinstance(value, str):
                    raise ValueError("Context phải là chuỗi hoặc null")
                context[key] = value
        for label, values in structured["components"].items():
            kind = _kind(label)
            if kind is None:
                raise ValueError("Loại linh kiện JSON không được hỗ trợ")
            if values is None:
                continue
            for value in (values if isinstance(values, list) else [values]):
                if not isinstance(value, str) or not value.strip():
                    raise ValueError("Mã linh kiện phải là chuỗi")
                mentions.append({"query": value.strip(), "kind": kind})
        return {"mentions": mentions, "context": context, "in_scope": True}

    # Chỉ lấy context được gắn nhãn, không suy BIOS/clearance từ thông số hãng.
    def take_context(match):
        label, value = match.group(1), match.group(2).strip()
        key = "bios_version" if "bios" in _plain(label) else "case_clearance_condition"
        if _plain(value) not in ("unknown", "null", "chua ro", "khong biet", "chua biet"):
            if context[key] is not None and context[key] != value:
                raise ValueError("Có nhiều giá trị context khác nhau")
            context[key] = value
        return ";"

    remaining = re.sub(r"\b(bios(?:_version)?|case_clearance_condition|bố trí vỏ|điều kiện vỏ|clearance)\s*[:=]\s*([^;\n]+)", take_context, text, flags=re.IGNORECASE)
    labels = r"cpu|processor|vi xử lý|mainboard|motherboard|main|bo mạch chủ|ram|bộ nhớ|gpu|vga|card đồ họa|case|vỏ máy|vỏ"
    remaining = re.sub(r"(?<!\w)(" + labels + r")\s*[:=]", r";\1:", remaining, flags=re.IGNORECASE)
    chunks = re.split(r"([;,\n+|]|\s+(?:và|and|hoặc|or)\s+)", remaining, flags=re.IGNORECASE)
    inherited_kind = None
    for chunk in chunks:
        if re.fullmatch(r"[;,\n+|]|\s+(?:và|and|hoặc|or)\s+", chunk, flags=re.IGNORECASE):
            if _plain(chunk).strip() not in ("hoac", "or"):
                inherited_kind = None
            continue
        chunk = chunk.strip(" .?!\t")
        if not chunk:
            continue
        labelled = re.match(r"^(" + labels + r")\s*:\s*(.*)$", chunk, flags=re.IGNORECASE)
        kind = _kind(labelled.group(1)) if labelled else None
        query = labelled.group(2).strip() if labelled else chunk
        query = re.sub(r"^(?:kiểm tra cấu hình|kiểm tra|kiểm giúp tôi|kiểm giúp|cấu hình(?: của tôi)?|tôi có|mình có)\s*[:\-]?\s*", "", query, flags=re.IGNORECASE).strip()
        if not labelled:
            prefix = re.match(r"^(" + labels + r")\s+(.+)$", query, flags=re.IGNORECASE)
            if prefix:
                kind, query = _kind(prefix.group(1)), prefix.group(2).strip()
        if not query:
            continue
        plain = _plain(query)
        if kind is None:
            if re.search(r"\b(?:ryzen|core|celeron|pentium|threadripper|i[3579]-\d)", plain):
                kind = "cpu"
            elif re.search(r"\b(?:rtx|gtx|radeon|rx\s*\d)", plain):
                kind = "gpu"
            elif re.search(r"\b(?:ddr[345]|dimm|kf\d)", plain):
                kind = "ram"
            elif re.search(r"\b(?:[abhzqx]\d{3}[a-z]*|motherboard|mainboard)\b", plain):
                kind = "mainboard"
        # Không thực thi phần chỉ dẫn xen vào danh sách; vẫn kiểm các mã đã nêu.
        if re.search(r"(?:\.env|api.?key|\[system\]|bo qua|dat hang|thanh toan|fps|gia re|ngan sach)", plain) and kind is None:
            continue
        if plain in ("xin chao", "chao", "hello", "kiem giup toi", "kiem giup", "co tuong thich khong"):
            continue
        if labelled:
            inherited_kind = kind
        elif kind is None and inherited_kind is not None:
            kind = inherited_kind
        mentions.append({"query": query, "kind": kind})
    return {"mentions": mentions, "context": context, "in_scope": bool(mentions)}


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        payload = json.loads(user)
        result = _fake_extract(payload["input"])
        return {"text": json.dumps(result, ensure_ascii=False), "model": "fake", "tokens_in": 0, "tokens_out": 0}

    # NHÓM VIẾT: gọi model thật ở đây (theo MODEL_PROVIDER, MODEL_NAME, API_KEY) rồi trả đúng 4 khoá.
    # Ví dụ chép được cho từng nhà cung cấp: docs/connect-model.md mục 2.
    raise NotImplementedError(
        "chưa viết phần gọi model thật cho MODEL_PROVIDER=%s trong codebase/ai.py — xem docs/connect-model.md"
        % MODEL_PROVIDER)
