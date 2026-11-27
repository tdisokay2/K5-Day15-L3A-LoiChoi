"""Công cụ tra cứu danh mục và kiểm tra tương thích cấu hình PC.

Mỗi công cụ gắn @tool và có docstring gồm: tên · input · output · có tác động ra ngoài không.
Chỉ dùng thư viện chuẩn Python và chỉ đọc catalog cục bộ tại data/components.json.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

try:
    from tracing import tool, TOOLS  # noqa: F401
except ImportError:
    from .tracing import tool, TOOLS  # noqa: F401

CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "components.json"

VALID_KINDS = ("cpu", "mainboard", "ram", "gpu", "case")
CHECK_PAIRS = ("cpu_mainboard", "mainboard_ram", "gpu_case")
SYNTHETIC_NOTICE = "MÔ PHỎNG — không dùng để quyết định mua"

UNCHECKED_ITEMS = [
    "Nguồn (PSU) và đầu cấp nguồn",
    "Tản nhiệt CPU và khoảng trống lắp đặt",
    "Ổ đĩa và kết nối lưu trữ",
    "Kích thước mainboard–vỏ máy (form factor)",
    "QVL RAM, tốc độ, dung lượng và số thanh RAM",
    "Độ dày GPU và khoảng trống dây nguồn",
    "Giá bán, tồn kho và hiệu năng (FPS)",
]


def _norm(text: str) -> str:
    """Chuẩn hóa chuỗi để so khớp không phân biệt hoa thường và khoảng trắng thừa."""
    return re.sub(r"\s+", " ", text.strip().lower())


def _load_catalog(catalog_path: Path | None = None) -> tuple[dict[str, dict[str, Any]] | None, str | None]:
    """Đọc và kiểm tra schema cơ bản của catalog cục bộ.

    Trả về (by_id, error_message). Không làm rò rỉ stack trace hoặc bí mật.
    """
    path = catalog_path or CATALOG_PATH
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except FileNotFoundError:
        return None, "Không tìm thấy tệp catalog cục bộ."
    except (OSError, json.JSONDecodeError):
        return None, "Catalog cục bộ sai định dạng JSON hoặc không đọc được."

    if not isinstance(data, dict) or data.get("schema_version") != "1.0":
        return None, "Catalog sai schema_version (yêu cầu '1.0')."

    items = data.get("components")
    if not isinstance(items, list):
        return None, "Catalog thiếu danh sách 'components' hợp lệ."

    by_id: dict[str, dict[str, Any]] = {}
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            return None, f"Phần tử catalog #{idx} không phải object."
        cid = item.get("id")
        kind = item.get("kind")
        if not isinstance(cid, str) or not cid.strip():
            return None, f"Phần tử catalog #{idx} thiếu 'id' hợp lệ."
        if cid in by_id:
            return None, f"Trùng id trong catalog: '{cid}'."
        if kind not in VALID_KINDS:
            return None, f"Linh kiện '{cid}' có kind không hợp lệ."
        for req_str in ("name", "manufacturer", "model"):
            val = item.get(req_str)
            if not isinstance(val, str) or not val.strip():
                return None, f"Linh kiện '{cid}' thiếu trường '{req_str}'."
        if not isinstance(item.get("synthetic"), bool):
            return None, f"Linh kiện '{cid}' thiếu cờ boolean 'synthetic'."
        if not isinstance(item.get("specs"), dict):
            return None, f"Linh kiện '{cid}' thiếu object 'specs'."
        if not isinstance(item.get("sources"), list):
            return None, f"Linh kiện '{cid}' thiếu danh sách 'sources'."
        if not isinstance(item.get("aliases"), list):
            return None, f"Linh kiện '{cid}' thiếu danh sách 'aliases'."
        if not isinstance(item.get("missing_fields"), list):
            return None, f"Linh kiện '{cid}' thiếu danh sách 'missing_fields'."
        by_id[cid] = item

    return by_id, None


def _candidate_summary(comp: dict[str, Any]) -> dict[str, Any]:
    """Rút gọn thông tin ứng viên đúng hợp đồng lookup_components."""
    return {
        "id": comp["id"],
        "kind": comp["kind"],
        "name": comp["name"],
        "model": comp["model"],
        "revision": comp.get("revision"),
    }


def _match_components(query: str, components: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """So khớp theo 3 tầng: khớp chính xác id/name/model -> khớp alias -> khớp từ khóa."""
    q_norm = _norm(query)
    if not q_norm:
        return []

    exact = [
        c for c in components
        if q_norm in (_norm(c["id"]), _norm(c["name"]), _norm(c["model"]))
    ]
    if exact:
        return exact

    alias_exact = [
        c for c in components
        if any(isinstance(a, str) and _norm(a) == q_norm for a in c.get("aliases", []))
    ]
    if alias_exact:
        return alias_exact

    tokens = [t for t in re.split(r"[\s\-_/]+", q_norm) if t]
    partial: list[dict[str, Any]] = []
    for c in components:
        haystacks = [c["id"], c["name"], c["model"]] + [
            a for a in c.get("aliases", []) if isinstance(a, str)
        ]
        norm_haystacks = [_norm(h) for h in haystacks]
        if any(q_norm in h for h in norm_haystacks):
            partial.append(c)
            continue
        joined = " ".join(norm_haystacks)
        if tokens and all(tok in joined for tok in tokens):
            partial.append(c)
    return partial


@tool
def lookup_components(query: str, kind: str | None = None) -> dict[str, Any]:
    """lookup_components — Tra mã và biến thể linh kiện trong catalog cục bộ.

    Input: query (str: tên hoặc mã linh kiện), kind (str | None: cpu, mainboard, ram, gpu, case).
    Output: dict {"candidates": [{id, kind, name, model, revision}], "reason": str}.
    Tác động ra ngoài: Không; chỉ đọc catalog cục bộ.
    """
    if kind is not None:
        if not isinstance(kind, str) or _norm(kind) not in VALID_KINDS:
            return {
                "candidates": [],
                "reason": f"Loại linh kiện '{kind}' không nằm trong phạm vi hỗ trợ ({', '.join(VALID_KINDS)}).",
            }
        kind_norm = _norm(kind)
    else:
        kind_norm = None

    if not isinstance(query, str) or not query.strip():
        return {
            "candidates": [],
            "reason": "Từ khóa tra cứu trống; cần hỏi người dùng tên hoặc mã linh kiện cụ thể.",
        }

    by_id, err = _load_catalog()
    if err or by_id is None:
        return {
            "candidates": [],
            "reason": f"Lỗi dữ liệu catalog: {err}",
        }

    pool = [c for c in by_id.values() if kind_norm is None or c["kind"] == kind_norm]
    matches = _match_components(query, pool)
    candidates = [_candidate_summary(c) for c in matches]

    if len(candidates) == 0:
        reason = f"Không tìm thấy linh kiện khớp '{query.strip()}' trong catalog; cần hỏi lại đúng mã hãng hoặc nguồn."
    elif len(candidates) == 1:
        c = candidates[0]
        reason = f"Xác định duy nhất {c['name']} (id: {c['id']})."
    else:
        reason = (
            f"Tìm thấy {len(candidates)} ứng viên khớp '{query.strip()}'; "
            "cần hỏi lại để xác định đúng model/revision/biến thể."
        )

    return {"candidates": candidates, "reason": reason}


def _extract_sources(
    comp: dict[str, Any],
    field_paths: tuple[str, ...],
    source_ids_filter: list[str] | None = None,
) -> tuple[list[dict[str, str]], str | None]:
    """Lấy và xác thực nguồn hãng cho các trường thông số được sử dụng."""
    cid = comp["id"]
    if comp.get("synthetic") is True:
        return [], None

    missing_fields = set(comp.get("missing_fields") or [])
    for fp in field_paths:
        if fp in missing_fields:
            return [], f"Trường '{fp}' của '{cid}' đang được đánh dấu thiếu dữ liệu."

    raw_sources = comp.get("sources") or []
    seen_ids: set[str] = set()
    by_sid: dict[str, dict[str, Any]] = {}
    for src in raw_sources:
        if not isinstance(src, dict):
            return [], f"Nguồn của '{cid}' sai cấu trúc."
        sid = src.get("id")
        url = src.get("url")
        fields = src.get("fields")
        if not isinstance(sid, str) or not sid or sid in seen_ids:
            return [], f"ID nguồn của '{cid}' không hợp lệ hoặc bị trùng."
        seen_ids.add(sid)
        if not isinstance(url, str) or not url.startswith("https://"):
            return [], f"URL nguồn '{sid}' của '{cid}' phải là HTTPS hợp lệ."
        if not isinstance(fields, list):
            return [], f"Danh sách fields của nguồn '{sid}' ({cid}) không hợp lệ."
        by_sid[sid] = src

    matched: list[dict[str, str]] = []
    covered: set[str] = set()
    for sid, src in by_sid.items():
        if source_ids_filter is not None and sid not in source_ids_filter:
            continue
        src_fields = set(src["fields"])
        if any(fp in src_fields for fp in field_paths):
            covered.update(fp for fp in field_paths if fp in src_fields)
            matched.append({"component_id": cid, "source_id": sid, "url": src["url"]})

    if source_ids_filter is not None and not matched:
        return [], f"Thiếu nguồn hãng tham chiếu ({', '.join(source_ids_filter)}) cho '{cid}'."
    if not all(fp in covered for fp in field_paths):
        uncovered = [fp for fp in field_paths if fp not in covered]
        return [], f"Thiếu nguồn hãng cho trường {', '.join(uncovered)} của '{cid}'."

    return matched, None


def _make_fact(cid: str, field: str, value: Any, unit: str | None = None) -> dict[str, Any]:
    return {"component_id": cid, "field": field, "value": value, "unit": unit}


def _dedup_sources(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, str]] = []
    for s in sources:
        key = (s["component_id"], s["source_id"])
        if key not in seen:
            seen.add(key)
            out.append(s)
    return out


def _append_synthetic_notice(reason: str, is_synthetic: bool) -> str:
    if is_synthetic and SYNTHETIC_NOTICE not in reason:
        return f"{reason} ({SYNTHETIC_NOTICE})"
    return reason


def _resolve_slot(
    slot: str,
    raw_id: Any,
    by_id: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any] | None, str | None]:
    """Xác thực một ô linh kiện trong build['components']."""
    if raw_id is None:
        return None, f"Thiếu mã {slot}"
    if not isinstance(raw_id, str) or not raw_id.strip():
        return None, f"Giá trị {slot} không hợp lệ (cần id dạng chuỗi hoặc null)"
    comp = by_id.get(raw_id)
    if comp is None:
        return None, f"Mã {slot} '{raw_id}' không có trong catalog"
    if comp["kind"] != slot:
        return None, f"Mã '{raw_id}' thuộc loại '{comp['kind']}', không khớp ô '{slot}'"
    return comp, None


def _check_cpu_mainboard(
    cpu: dict[str, Any] | None,
    cpu_err: str | None,
    mb: dict[str, Any] | None,
    mb_err: str | None,
    bios_version: str | None,
) -> dict[str, Any]:
    missing: list[str] = []
    facts: list[dict[str, Any]] = []
    sources: list[dict[str, str]] = []

    if cpu_err:
        missing.append(cpu_err)
    if mb_err:
        missing.append(mb_err)
    if cpu is None or mb is None:
        return {
            "pair": "cpu_mainboard",
            "status": "insufficient_info",
            "reason": "Chưa đủ mã CPU và mainboard hợp lệ để kiểm tra socket, danh sách CPU hỗ trợ và BIOS.",
            "facts": facts,
            "sources": sources,
            "missing": missing,
        }

    is_synth = bool(cpu["synthetic"] or mb["synthetic"])
    cpu_socket = cpu["specs"].get("socket")
    mb_socket = mb["specs"].get("socket")

    if not isinstance(cpu_socket, str) or not cpu_socket.strip():
        missing.append(f"Thiếu thông số socket của CPU '{cpu['id']}'")
    else:
        cpu_srcs, err = _extract_sources(cpu, ("specs.socket",))
        if err:
            missing.append(err)
        else:
            facts.append(_make_fact(cpu["id"], "specs.socket", cpu_socket, None))
            sources.extend(cpu_srcs)

    if not isinstance(mb_socket, str) or not mb_socket.strip():
        missing.append(f"Thiếu thông số socket của mainboard '{mb['id']}'")
    else:
        mb_srcs, err = _extract_sources(mb, ("specs.socket",))
        if err:
            missing.append(err)
        else:
            facts.append(_make_fact(mb["id"], "specs.socket", mb_socket, None))
            sources.extend(mb_srcs)

    if missing:
        return {
            "pair": "cpu_mainboard",
            "status": "insufficient_info",
            "reason": _append_synthetic_notice(
                "Thiếu thông số hoặc nguồn socket của CPU/mainboard nên chưa thể đối chiếu.",
                is_synth,
            ),
            "facts": facts,
            "sources": _dedup_sources(sources),
            "missing": missing,
        }

    if _norm(cpu_socket) != _norm(mb_socket):
        return {
            "pair": "cpu_mainboard",
            "status": "conflict",
            "reason": _append_synthetic_notice(
                f"Xung đột socket: CPU dùng socket {cpu_socket}, trong khi mainboard dùng socket {mb_socket}.",
                is_synth,
            ),
            "facts": facts,
            "sources": _dedup_sources(sources),
            "missing": [],
        }

    # Socket giống nhau chưa đủ: phải kiểm tra cpu_support và BIOS
    cpu_support = mb["specs"].get("cpu_support")
    cpu_support_complete = mb["specs"].get("cpu_support_complete")

    if not isinstance(cpu_support, list):
        missing.append(f"Thiếu danh sách cpu_support của mainboard '{mb['id']}'")
        return {
            "pair": "cpu_mainboard",
            "status": "insufficient_info",
            "reason": _append_synthetic_notice(
                f"Cùng socket {cpu_socket}, nhưng mainboard chưa có danh sách CPU hỗ trợ có nguồn để xác nhận.",
                is_synth,
            ),
            "facts": facts,
            "sources": _dedup_sources(sources),
            "missing": missing,
        }

    support_srcs, err = _extract_sources(mb, ("specs.cpu_support",))
    if err:
        missing.append(err)
        return {
            "pair": "cpu_mainboard",
            "status": "insufficient_info",
            "reason": _append_synthetic_notice(
                f"Cùng socket {cpu_socket}, nhưng thiếu nguồn hãng cho danh sách CPU hỗ trợ của mainboard.",
                is_synth,
            ),
            "facts": facts,
            "sources": _dedup_sources(sources),
            "missing": missing,
        }
    sources.extend(support_srcs)

    entry = next((e for e in cpu_support if isinstance(e, dict) and e.get("cpu_id") == cpu["id"]), None)
    if entry is None:
        if cpu_support_complete is True:
            facts.append(_make_fact(mb["id"], "specs.cpu_support_complete", True, None))
            return {
                "pair": "cpu_mainboard",
                "status": "conflict",
                "reason": _append_synthetic_notice(
                    f"Cùng socket {cpu_socket}, nhưng CPU '{cpu['name']}' không có trong danh sách CPU hỗ trợ đầy đủ của mainboard.",
                    is_synth,
                ),
                "facts": facts,
                "sources": _dedup_sources(sources),
                "missing": [],
            }
        missing.append(f"Danh sách cpu_support của '{mb['id']}' chưa đầy đủ (cpu_support_complete=false)")
        facts.append(_make_fact(mb["id"], "specs.cpu_support_complete", bool(cpu_support_complete), None))
        return {
            "pair": "cpu_mainboard",
            "status": "insufficient_info",
            "reason": _append_synthetic_notice(
                f"Cùng socket {cpu_socket}, nhưng danh sách CPU hỗ trợ trong catalog chưa đầy đủ nên chưa thể kết luận cho '{cpu['name']}'.",
                is_synth,
            ),
            "facts": facts,
            "sources": _dedup_sources(sources),
            "missing": missing,
        }

    entry_src_ids = entry.get("source_ids")
    if not mb["synthetic"]:
        if not isinstance(entry_src_ids, list) or not entry_src_ids:
            missing.append(f"Dòng cpu_support cho '{cpu['id']}' thiếu source_ids")
            return {
                "pair": "cpu_mainboard",
                "status": "insufficient_info",
                "reason": _append_synthetic_notice(
                    "Thiếu tham chiếu nguồn cho dòng CPU hỗ trợ trong catalog.",
                    is_synth,
                ),
                "facts": facts,
                "sources": _dedup_sources(sources),
                "missing": missing,
            }
        entry_srcs, err = _extract_sources(mb, ("specs.cpu_support",), source_ids_filter=entry_src_ids)
        if err:
            missing.append(err)
            return {
                "pair": "cpu_mainboard",
                "status": "insufficient_info",
                "reason": _append_synthetic_notice(
                    "Nguồn tham chiếu cho dòng CPU hỗ trợ không hợp lệ.",
                    is_synth,
                ),
                "facts": facts,
                "sources": _dedup_sources(sources),
                "missing": missing,
            }
        sources.extend(entry_srcs)

    min_bios = entry.get("min_bios")
    if min_bios is not None:
        if not isinstance(min_bios, str) or not min_bios.strip():
            missing.append(f"Giá trị min_bios của '{mb['id']}' cho '{cpu['id']}' không hợp lệ")
            return {
                "pair": "cpu_mainboard",
                "status": "insufficient_info",
                "reason": _append_synthetic_notice(
                    "Điều kiện min_bios trong catalog không hợp lệ nên chưa thể kết luận.",
                    is_synth,
                ),
                "facts": facts,
                "sources": _dedup_sources(sources),
                "missing": missing,
            }

        bios_srcs, err = _extract_sources(mb, ("specs.cpu_support.min_bios",), source_ids_filter=entry_src_ids if not mb["synthetic"] else None)
        if err:
            missing.append(err)
            return {
                "pair": "cpu_mainboard",
                "status": "insufficient_info",
                "reason": _append_synthetic_notice(
                    "Thiếu nguồn hãng cho điều kiện min_bios của mainboard.",
                    is_synth,
                ),
                "facts": facts,
                "sources": _dedup_sources(sources),
                "missing": missing,
            }
        sources.extend(bios_srcs)
        facts.append(_make_fact(mb["id"], "specs.cpu_support.min_bios", min_bios, None))

        if not isinstance(bios_version, str) or not bios_version.strip():
            missing.append(f"Phiên bản BIOS hiện tại trên mainboard (cần tối thiểu {min_bios})")
            return {
                "pair": "cpu_mainboard",
                "status": "insufficient_info",
                "reason": _append_synthetic_notice(
                    f"Cùng socket {cpu_socket} và CPU có trong danh sách hỗ trợ với điều kiện BIOS {min_bios}, nhưng chưa rõ phiên bản BIOS hiện tại trên mainboard.",
                    is_synth,
                ),
                "facts": facts,
                "sources": _dedup_sources(sources),
                "missing": missing,
            }

        facts.append(_make_fact(mb["id"], "context.bios_version", bios_version.strip(), None))
        if _norm(bios_version) != _norm(min_bios):
            missing.append(f"Chưa chứng minh được quan hệ phiên bản BIOS '{bios_version.strip()}' so với mốc hãng '{min_bios}'")
            return {
                "pair": "cpu_mainboard",
                "status": "insufficient_info",
                "reason": _append_synthetic_notice(
                    f"Cùng socket {cpu_socket} và CPU có trong danh sách hỗ trợ (mốc BIOS {min_bios}), nhưng chưa chứng minh được thứ tự phiên bản từ hãng giữa '{bios_version.strip()}' và '{min_bios}'.",
                    is_synth,
                ),
                "facts": facts,
                "sources": _dedup_sources(sources),
                "missing": missing,
            }

    return {
        "pair": "cpu_mainboard",
        "status": "no_conflict_found",
        "reason": _append_synthetic_notice(
            f"Chưa phát hiện xung đột CPU–mainboard: cùng socket {cpu_socket}, CPU nằm trong danh sách hỗ trợ và điều kiện BIOS đã được xác nhận.",
            is_synth,
        ),
        "facts": facts,
        "sources": _dedup_sources(sources),
        "missing": [],
    }


def _check_mainboard_ram(
    mb: dict[str, Any] | None,
    mb_err: str | None,
    ram: dict[str, Any] | None,
    ram_err: str | None,
) -> dict[str, Any]:
    missing: list[str] = []
    facts: list[dict[str, Any]] = []
    sources: list[dict[str, str]] = []

    if mb_err:
        missing.append(mb_err)
    if ram_err:
        missing.append(ram_err)
    if mb is None or ram is None:
        return {
            "pair": "mainboard_ram",
            "status": "insufficient_info",
            "reason": "Chưa đủ mã mainboard và RAM hợp lệ để đối chiếu thế hệ DDR.",
            "facts": facts,
            "sources": sources,
            "missing": missing,
        }

    is_synth = bool(mb["synthetic"] or ram["synthetic"])
    mb_ddr = mb["specs"].get("memory_type")
    ram_ddr = ram["specs"].get("memory_type")

    if not isinstance(mb_ddr, str) or not mb_ddr.strip():
        missing.append(f"Thiếu thông số thế hệ DDR của mainboard '{mb['id']}'")
    else:
        mb_srcs, err = _extract_sources(mb, ("specs.memory_type",))
        if err:
            missing.append(err)
        else:
            facts.append(_make_fact(mb["id"], "specs.memory_type", mb_ddr, None))
            sources.extend(mb_srcs)

    if not isinstance(ram_ddr, str) or not ram_ddr.strip():
        missing.append(f"Thiếu thông số thế hệ DDR của RAM '{ram['id']}'")
    else:
        ram_srcs, err = _extract_sources(ram, ("specs.memory_type",))
        if err:
            missing.append(err)
        else:
            facts.append(_make_fact(ram["id"], "specs.memory_type", ram_ddr, None))
            sources.extend(ram_srcs)

    if missing:
        return {
            "pair": "mainboard_ram",
            "status": "insufficient_info",
            "reason": _append_synthetic_notice(
                "Thiếu thông số hoặc nguồn thế hệ DDR của mainboard/RAM nên chưa thể kết luận.",
                is_synth,
            ),
            "facts": facts,
            "sources": _dedup_sources(sources),
            "missing": missing,
        }

    if _norm(mb_ddr) != _norm(ram_ddr):
        return {
            "pair": "mainboard_ram",
            "status": "conflict",
            "reason": _append_synthetic_notice(
                f"Xung đột thế hệ RAM: mainboard hỗ trợ {mb_ddr}, trong khi RAM là {ram_ddr}.",
                is_synth,
            ),
            "facts": facts,
            "sources": _dedup_sources(sources),
            "missing": [],
        }

    return {
        "pair": "mainboard_ram",
        "status": "no_conflict_found",
        "reason": _append_synthetic_notice(
            f"Chưa phát hiện xung đột về thế hệ DDR (cùng {mb_ddr}); QVL, tốc độ, dung lượng và số thanh RAM chưa được kiểm.",
            is_synth,
        ),
        "facts": facts,
        "sources": _dedup_sources(sources),
        "missing": [],
    }


def _check_gpu_case(
    gpu: dict[str, Any] | None,
    gpu_err: str | None,
    case: dict[str, Any] | None,
    case_err: str | None,
    case_clearance_condition: str | None,
) -> dict[str, Any]:
    missing: list[str] = []
    facts: list[dict[str, Any]] = []
    sources: list[dict[str, str]] = []

    if gpu_err:
        missing.append(gpu_err)
    if case_err:
        missing.append(case_err)
    if gpu is None or case is None:
        return {
            "pair": "gpu_case",
            "status": "insufficient_info",
            "reason": "Chưa đủ mã GPU và vỏ máy hợp lệ để đối chiếu chiều dài GPU và điều kiện lắp đặt.",
            "facts": facts,
            "sources": sources,
            "missing": missing,
        }

    is_synth = bool(gpu["synthetic"] or case["synthetic"])
    gpu_len = gpu["specs"].get("length_mm")
    case_max = case["specs"].get("max_gpu_length_mm")
    case_cond = case["specs"].get("clearance_condition")

    if isinstance(gpu_len, bool) or not isinstance(gpu_len, (int, float)) or gpu_len <= 0:
        missing.append(f"Thiếu chiều dài GPU hợp lệ (mm > 0) của '{gpu['id']}'")
    else:
        gpu_srcs, err = _extract_sources(gpu, ("specs.length_mm",))
        if err:
            missing.append(err)
        else:
            facts.append(_make_fact(gpu["id"], "specs.length_mm", gpu_len, "mm"))
            sources.extend(gpu_srcs)

    if isinstance(case_max, bool) or not isinstance(case_max, (int, float)) or case_max <= 0:
        missing.append(f"Thiếu giới hạn chiều dài GPU hợp lệ (mm > 0) của '{case['id']}'")
    else:
        case_len_srcs, err = _extract_sources(case, ("specs.max_gpu_length_mm",))
        if err:
            missing.append(err)
        else:
            facts.append(_make_fact(case["id"], "specs.max_gpu_length_mm", case_max, "mm"))
            sources.extend(case_len_srcs)

    if not isinstance(case_cond, str) or not case_cond.strip():
        missing.append(f"Thiếu điều kiện lắp đặt clearance_condition của vỏ '{case['id']}'")
    else:
        case_cond_srcs, err = _extract_sources(case, ("specs.clearance_condition",))
        if err:
            missing.append(err)
        else:
            facts.append(_make_fact(case["id"], "specs.clearance_condition", case_cond, None))
            sources.extend(case_cond_srcs)

    if missing:
        return {
            "pair": "gpu_case",
            "status": "insufficient_info",
            "reason": _append_synthetic_notice(
                "Thiếu thông số chiều dài, điều kiện lắp đặt hoặc nguồn hãng của GPU/vỏ máy nên chưa thể kết luận.",
                is_synth,
            ),
            "facts": facts,
            "sources": _dedup_sources(sources),
            "missing": missing,
        }

    if not isinstance(case_clearance_condition, str) or not case_clearance_condition.strip():
        missing.append(f"Chưa xác nhận điều kiện lắp đặt vỏ máy (mốc hãng: '{case_cond}')")
        return {
            "pair": "gpu_case",
            "status": "insufficient_info",
            "reason": _append_synthetic_notice(
                f"Đã có chiều dài GPU ({gpu_len} mm) và giới hạn vỏ ({case_max} mm theo điều kiện '{case_cond}'), nhưng người dùng chưa xác nhận bố trí vỏ máy.",
                is_synth,
            ),
            "facts": facts,
            "sources": _dedup_sources(sources),
            "missing": missing,
        }

    facts.append(_make_fact(case["id"], "context.case_clearance_condition", case_clearance_condition.strip(), None))
    if _norm(case_clearance_condition) != _norm(case_cond):
        missing.append(
            f"Điều kiện lắp đặt người dùng ('{case_clearance_condition.strip()}') không khớp điều kiện của thông số hãng ('{case_cond}')"
        )
        return {
            "pair": "gpu_case",
            "status": "insufficient_info",
            "reason": _append_synthetic_notice(
                f"Bố trí vỏ máy ('{case_clearance_condition.strip()}') chưa khớp điều kiện '{case_cond}' của giới hạn {case_max} mm nên chưa thể đối chiếu.",
                is_synth,
            ),
            "facts": facts,
            "sources": _dedup_sources(sources),
            "missing": missing,
        }

    if gpu_len > case_max:
        return {
            "pair": "gpu_case",
            "status": "conflict",
            "reason": _append_synthetic_notice(
                f"Xung đột kích thước GPU–vỏ: GPU dài {gpu_len} mm vượt giới hạn {case_max} mm của vỏ ở điều kiện '{case_cond}'.",
                is_synth,
            ),
            "facts": facts,
            "sources": _dedup_sources(sources),
            "missing": [],
        }

    return {
        "pair": "gpu_case",
        "status": "no_conflict_found",
        "reason": _append_synthetic_notice(
            f"Chưa phát hiện xung đột về chiều dài GPU ({gpu_len} mm ≤ {case_max} mm ở điều kiện '{case_cond}'); độ dày card và khoảng trống dây nguồn chưa được kiểm.",
            is_synth,
        ),
        "facts": facts,
        "sources": _dedup_sources(sources),
        "missing": [],
    }


@tool
def check_compatibility(build: dict[str, Any]) -> dict[str, Any]:
    """check_compatibility — Kiểm tra 3 quan hệ tương thích bằng code từ catalog cục bộ.

    Input: build (dict gồm components, context, unresolved theo spec.md §4).
    Output: dict {"status", "checks", "missing", "unchecked", "synthetic"}.
    Tác động ra ngoài: Không; chỉ đọc catalog cục bộ và so sánh bằng code.
    """
    if not isinstance(build, dict):
        return {
            "status": "insufficient_info",
            "checks": [
                {"pair": p, "status": "insufficient_info", "reason": "Đầu vào build không phải object hợp lệ.", "facts": [], "sources": [], "missing": ["build phải là dict"]}
                for p in CHECK_PAIRS
            ],
            "missing": ["build phải là dict"],
            "unchecked": list(UNCHECKED_ITEMS),
            "synthetic": False,
        }

    by_id, err = _load_catalog()
    if err or by_id is None:
        return {
            "status": "insufficient_info",
            "checks": [
                {"pair": p, "status": "insufficient_info", "reason": f"Lỗi dữ liệu catalog: {err}", "facts": [], "sources": [], "missing": [f"Lỗi dữ liệu catalog: {err}"]}
                for p in CHECK_PAIRS
            ],
            "missing": [f"Lỗi dữ liệu catalog: {err}"],
            "unchecked": list(UNCHECKED_ITEMS),
            "synthetic": False,
        }

    comp_map = build.get("components")
    if not isinstance(comp_map, dict):
        comp_map = {}
    context = build.get("context")
    if not isinstance(context, dict):
        context = {}
    unresolved = build.get("unresolved")
    if not isinstance(unresolved, list):
        unresolved = []

    resolved: dict[str, dict[str, Any] | None] = {}
    slot_errors: dict[str, str | None] = {}
    for slot in VALID_KINDS:
        resolved[slot], slot_errors[slot] = _resolve_slot(slot, comp_map.get(slot), by_id)

    checks = [
        _check_cpu_mainboard(
            resolved["cpu"], slot_errors["cpu"],
            resolved["mainboard"], slot_errors["mainboard"],
            context.get("bios_version"),
        ),
        _check_mainboard_ram(
            resolved["mainboard"], slot_errors["mainboard"],
            resolved["ram"], slot_errors["ram"],
        ),
        _check_gpu_case(
            resolved["gpu"], slot_errors["gpu"],
            resolved["case"], slot_errors["case"],
            context.get("case_clearance_condition"),
        ),
    ]

    aggregated_missing: list[str] = []
    for chk in checks:
        for item in chk["missing"]:
            if item not in aggregated_missing:
                aggregated_missing.append(item)

    for u in unresolved:
        if isinstance(u, dict):
            mention = u.get("mention") or u.get("kind") or "linh kiện"
            msg = f"Mã chưa xác định/mơ hồ: {mention}"
        else:
            msg = "Còn mã chưa xác định trong unresolved"
        if msg not in aggregated_missing:
            aggregated_missing.append(msg)

    statuses = [chk["status"] for chk in checks]
    if "conflict" in statuses:
        overall_status = "conflict"
    elif "insufficient_info" in statuses or len(unresolved) > 0:
        overall_status = "insufficient_info"
    else:
        overall_status = "no_conflict_found"

    is_synthetic = any(c is not None and c.get("synthetic") is True for c in resolved.values())

    return {
        "status": overall_status,
        "checks": checks,
        "missing": aggregated_missing,
        "unchecked": list(UNCHECKED_ITEMS),
        "synthetic": is_synthetic,
    }
