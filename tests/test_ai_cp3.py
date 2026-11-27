"""Kiểm hợp đồng HTTP/usage và trace CP3 bằng phản hồi giả lập, không gọi API thật."""
import copy
import io
import json
import os
from pathlib import Path
import sys
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codebase"))
os.environ["MODEL_PROVIDER"] = "fake"
import ai
import agent
import tracing


class OpenRouterTests(unittest.TestCase):
    def setUp(self):
        self.settings = patch.multiple(ai, MODEL_PROVIDER="openrouter", MODEL_NAME="vendor/requested", API_KEY="test-secret")
        self.settings.start()
        self.addCleanup(self.settings.stop)
        self.response = {
            "model": "vendor/actual",
            "choices": [{"finish_reason": "stop", "message": {"content": json.dumps({
                "mentions": [{"query": "KF432C16BBK2/16", "kind": "ram"}],
                "context": {"bios_version": None, "case_clearance_condition": None}, "in_scope": True})}}],
            "usage": {"prompt_tokens": 81, "completion_tokens": 47,
                      "completion_tokens_details": {"reasoning_tokens": 19}},
        }

    def http_response(self, data):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(data).encode("utf-8")
        return response

    def test_request_and_usage_reach_trace_and_checker(self):
        tracing.begin("mock-http-cp3")
        self.addCleanup(tracing.end)
        with patch.object(ai.urllib.request, "urlopen", return_value=self.http_response(self.response)) as send:
            output = agent.answer("RAM: KF432C16BBK2/16")["output"]
        summary, _ = tracing.end()
        request = send.call_args.args[0]
        body = json.loads(request.data)
        self.assertEqual(request.full_url, ai.URL_OPENROUTER)
        self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")
        self.assertEqual(send.call_args.kwargs["timeout"], 60)
        self.assertEqual(body["model"], "vendor/requested")
        self.assertEqual(body["response_format"], {"type": "json_object"})
        self.assertEqual(body["messages"][0]["content"], agent.SYSTEM)
        self.assertEqual(summary["models"], ["vendor/actual"])
        self.assertEqual((summary["model_calls"], summary["tokens_in"], summary["tokens_out"]), (1, 81, 47))
        self.assertEqual(summary["errors"], [])
        self.assertIn("RAM: kingston-kf432c16bbk2-16", output)
        self.assertNotIn("MODEL GIẢ", output)

    def test_usage_missing_or_invalid_is_never_estimated(self):
        for value in (None, {}, {"prompt_tokens": True, "completion_tokens": 10},
                      {"prompt_tokens": 10, "completion_tokens": -1},
                      {"prompt_tokens": 10, "completion_tokens": "12"}):
            with self.subTest(usage=value):
                data = dict(self.response, usage=value)
                with patch.object(ai, "_post_json", return_value=data):
                    with self.assertRaisesRegex(RuntimeError, "usage"):
                        ai.call_model("JSON", "input")

    def test_truncated_refused_or_empty_response_is_rejected(self):
        for reason, content in (("length", "{}"), ("content_filter", None), ("stop", "")):
            data = copy.deepcopy(self.response)
            data["choices"][0].update(finish_reason=reason, message={"content": content})
            with self.subTest(reason=reason, content=content), patch.object(ai, "_post_json", return_value=data):
                with self.assertRaises(RuntimeError):
                    ai.call_model("JSON", "input")

    def test_invalid_model_json_keeps_usage_and_requests_clarification(self):
        data = copy.deepcopy(self.response)
        data["choices"][0]["message"]["content"] = "not-json"
        tracing.begin("invalid-json")
        self.addCleanup(tracing.end)
        with patch.object(ai, "_post_json", return_value=data):
            output = agent.answer("RAM: KF432C16BBK2/16")["output"]
        summary, _ = tracing.end()
        self.assertEqual(summary["tokens_out"], 47)
        self.assertIn("Chưa xác nhận được tên/mã từ model", output)
        self.assertNotIn("Kết quả: Chưa phát hiện xung đột", output)

    def test_http_errors_are_recorded_without_secret_or_raw_body(self):
        for status in (401, 402, 429, 500):
            error = urllib.error.HTTPError(ai.URL_OPENROUTER, status, "test-secret", {}, io.BytesIO(b"test-secret"))
            tracing.begin("http-error")
            with self.subTest(status=status), patch.object(ai.urllib.request, "urlopen", side_effect=error):
                output = agent.answer("RAM: KF432C16BBK2/16")["output"]
            summary, events = tracing.end()
            self.assertIn("HTTP " + str(status), summary["errors"][0])
            self.assertNotIn("test-secret", json.dumps(events) + output)
            self.assertEqual(summary["models"], [])
            self.assertIn("Kết quả: Thiếu thông tin", output)

    def test_timeout_and_non_json_http_response(self):
        for error in (TimeoutError("test-secret"), urllib.error.URLError("test-secret")):
            with patch.object(ai.urllib.request, "urlopen", side_effect=error):
                with self.assertRaises(RuntimeError) as caught:
                    ai.call_model("JSON", "input")
                self.assertNotIn("test-secret", str(caught.exception))
        response = self.http_response(None)
        response.__enter__.return_value.read.return_value = b"not JSON test-secret"
        with patch.object(ai.urllib.request, "urlopen", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "JSON"):
                ai.call_model("JSON", "input")

    def test_api_error_body_is_not_logged(self):
        with patch.object(ai.urllib.request, "urlopen", return_value=self.http_response({"error": {"message": "test-secret"}})):
            with self.assertRaises(RuntimeError) as caught:
                ai.call_model("JSON", "input")
        self.assertNotIn("test-secret", str(caught.exception))

    def test_configuration_fails_before_network(self):
        for settings in ({"API_KEY": ""}, {"MODEL_NAME": ""}, {"MODEL_PROVIDER": "unsupported"}):
            with self.subTest(settings=settings), patch.multiple(ai, **settings), patch.object(ai.urllib.request, "urlopen") as send:
                with self.assertRaises((RuntimeError, ValueError)):
                    ai.call_model("JSON", "input")
                send.assert_not_called()

    def test_explicit_fake_does_not_use_network(self):
        with patch.object(ai, "MODEL_PROVIDER", "fake"), patch.object(ai.urllib.request, "urlopen") as send:
            result = ai.call_model("JSON", json.dumps({"input": "RAM: KF432C16BBK2/16"}))
        send.assert_not_called()
        self.assertEqual((result["model"], result["tokens_in"], result["tokens_out"]), ("fake", 0, 0))


if __name__ == "__main__":
    unittest.main()
