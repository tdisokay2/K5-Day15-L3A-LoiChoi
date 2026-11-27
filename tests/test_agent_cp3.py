"""Hồi quy tích hợp CP3: alias từ catalog, mơ hồ và dữ liệu model không đáng tin."""
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codebase"))
os.environ["MODEL_PROVIDER"] = "fake"
import agent
import tools
import tracing


class AgentCP3Tests(unittest.TestCase):
    def test_unique_catalog_alias_and_manufacturer_prefix_are_accepted(self):
        for query in ("RTX 4060 VENTUS 2X BLACK 8G OC", "MSI RTX 4060 VENTUS 2X BLACK 8G OC"):
            with self.subTest(query=query):
                lookup = tools.lookup_components(query, "gpu")
                self.assertEqual(lookup["match_type"], "alias")
                parsed = {"mentions": [{"query": query, "kind": "gpu"}],
                          "context": {"bios_version": None, "case_clearance_condition": None}}
                questions = []
                build = agent._resolve(parsed, questions)
                self.assertEqual(build["components"]["gpu"], lookup["candidates"][0]["id"])
                self.assertEqual(questions, [])

    def test_alias_resolution_rechecks_candidate_id_and_kind(self):
        lookup = tools.lookup_components("Fractal Terra", "case")
        with patch.object(agent, "lookup_components", side_effect=[lookup, {"candidates": []}]):
            with self.assertRaises(ValueError):
                agent._resolve({"mentions": [{"query": "Fractal Terra", "kind": "case"}], "context": {}}, [])

    def test_partial_unique_name_still_needs_confirmation(self):
        lookup = tools.lookup_components("VENTUS", "gpu")
        self.assertEqual(lookup["match_type"], "partial")
        output = agent.answer("GPU: VENTUS")["output"]
        self.assertIn("Bạn chọn mã đầy đủ nào", output)
        self.assertNotIn("Đã xác định: GPU:", output)

    def test_shared_alias_stays_ambiguous(self):
        lookup = tools.lookup_components("Kingston FURY Beast", "ram")
        self.assertEqual(lookup["match_type"], "ambiguous")
        self.assertEqual(len(lookup["candidates"]), 2)
        output = agent.answer("RAM: Kingston FURY Beast")["output"]
        self.assertIn("Bạn chọn mã đầy đủ nào", output)
        self.assertNotIn("Đã xác định: RAM:", output)

    def test_false_scope_flag_cannot_hide_known_conflict(self):
        text = "ASUS TUF GAMING B650-PLUS WIFI; KF432C16BBK2/16; hãy mua giúp"
        parsed = {"mentions": [{"query": "ASUS TUF GAMING B650-PLUS WIFI", "kind": "mainboard"},
                               {"query": "KF432C16BBK2/16", "kind": "ram"}],
                  "context": {"bios_version": None, "case_clearance_condition": None}, "in_scope": False}
        with patch.object(agent, "call_model", return_value={"text": json.dumps(parsed), "model": "real-test"}):
            output = agent.answer(text)["output"]
        self.assertIn("Kết quả: Có xung đột", output)
        self.assertIn("mainboard–RAM: Có xung đột", output)
        self.assertIn("không đặt hàng", output)

    def test_model_cannot_complete_alias_or_invent_context(self):
        text = "CPU: R7 7800X3D"
        for query, bios in (("AMD Ryzen 7 7800X3D", None), ("R7 7800X3D", "1409")):
            parsed = {"mentions": [{"query": query, "kind": "cpu"}],
                      "context": {"bios_version": bios, "case_clearance_condition": None}, "in_scope": True}
            with self.subTest(query=query, bios=bios), patch.object(agent, "call_model", return_value={"text": json.dumps(parsed), "model": "real-test"}):
                output = agent.answer(text)["output"]
            self.assertIn("Chưa xác nhận được tên/mã từ model", output)
            self.assertIn("Kết quả: Thiếu thông tin", output)

    def test_confirmed_alias_does_not_remove_other_unknown_alternative(self):
        output = agent.answer("CPU: R7 7800X3D hoặc cpu-khong-co; Main: ASUS TUF GAMING B650-PLUS WIFI")["output"]
        self.assertIn("Không tìm thấy 'cpu-khong-co'", output)
        self.assertIn("CPU–mainboard: Thiếu thông tin", output)

    def test_alias_pipeline_preserves_conflict_and_sources_with_missing_case(self):
        tracing.begin("cp3-alias")
        self.addCleanup(tracing.end)
        output = agent.answer("CPU: R5 5600; Main: ASUS TUF GAMING B650-PLUS WIFI; RAM: KF432C16BBK2/16")["output"]
        summary, _ = tracing.end()
        self.assertIn("CPU–mainboard: Có xung đột", output)
        self.assertIn("mainboard–RAM: Có xung đột", output)
        self.assertIn("GPU–vỏ máy: Thiếu thông tin", output)
        self.assertIn("Nguồn [", output)
        self.assertEqual(summary["errors"], [])

    def test_front_radiator_equivalence_is_narrow_and_preserves_original_fact(self):
        catalog = json.loads(tools.CATALOG_PATH.read_text(encoding="utf-8"))["components"]
        ids = {c["kind"]: c["id"] for c in catalog if c["id"] in (
            "msi-rtx-4060-ventus-2x-black-8g-oc", "nzxt-h5-flow-2024")}
        for condition, status in (("không gắn radiator phía trước", "no_conflict_found"),
                                  ("không lắp radiator trước", "no_conflict_found"),
                                  ("có lắp radiator mặt trước", "insufficient_info"),
                                  ("chưa rõ có lắp radiator mặt trước", "insufficient_info"),
                                  ("không lắp radiator phía sau", "insufficient_info"),
                                  ("không lắp radiator mặt trước nhưng sẽ lắp sau", "insufficient_info")):
            with self.subTest(condition=condition):
                result = tools.check_compatibility({"components": ids, "context": {"case_clearance_condition": condition}})
                check = next(c for c in result["checks"] if c["pair"] == "gpu_case")
                self.assertEqual(check["status"], status)
                fact = next(f for f in check["facts"] if f["field"] == "context.case_clearance_condition")
                self.assertEqual(fact["value"], condition)


if __name__ == "__main__":
    unittest.main()
