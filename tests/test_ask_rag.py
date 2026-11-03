import json
import os
from types import SimpleNamespace
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import unittest
from unittest.mock import patch

from scripts import ask_rag


class AnswerTests(unittest.TestCase):
    def args(self, **overrides):
        values = dict(provider=None, key_file=None, api_key_env=None, base_url=None, model=None)
        values.update(overrides)
        return SimpleNamespace(**values)

    def test_interactive_api_setup_has_no_desktop_dependency(self):
        with patch.dict(os.environ, {}, clear=True), patch('builtins.input', side_effect=['1', '1', '']), \
             patch.object(ask_rag, 'hidden_key', return_value='test-secret'), patch.object(ask_rag, 'read_key') as read:
            connection = ask_rag.configure(self.args())
        read.assert_not_called()
        self.assertEqual(connection.provider, 'openrouter')
        self.assertEqual(connection.model, ask_rag.MODEL)
        self.assertNotIn('test-secret', repr(connection))

    def test_local_setup_discovers_model_without_key(self):
        with patch('builtins.input', side_effect=['2', 'http://localhost:11434', '1']), \
             patch.object(ask_rag, 'hidden_key', return_value=''), \
             patch.object(ask_rag, 'discover_models', return_value=['local-model']):
            connection = ask_rag.configure(self.args())
        self.assertEqual(connection.base_url, 'http://localhost:11434/v1')
        self.assertEqual(connection.model, 'local-model')
        self.assertEqual(connection.api_key, '')

    def test_explicit_local_options_need_no_prompts(self):
        with patch('builtins.input', side_effect=AssertionError('Unexpected prompt')):
            connection = ask_rag.configure(self.args(provider='local', base_url='http://localhost:1234/v1', model='test-model'))
        self.assertEqual(connection.model, 'test-model')

    def test_urls_are_normalized_and_embedded_credentials_rejected(self):
        self.assertEqual(ask_rag.normalize_url('http://localhost:1234/v1/chat/completions/'), 'http://localhost:1234/v1')
        with self.assertRaises(ValueError):
            ask_rag.normalize_url('https://user:secret@example.com/v1')

    def test_openai_payload_uses_completion_token_parameter(self):
        answer = {'answer': 'Supported [S1]', 'citations': ['S1'], 'grounded': True}
        response = unittest.mock.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({'choices': [{'message': {'content': json.dumps(answer)}, 'finish_reason': 'stop'}]}).encode()
        connection = ask_rag.Connection('openai', 'https://api.openai.com/v1', 'chosen-model', 'test-secret')
        with patch.object(ask_rag.urllib.request, 'urlopen', return_value=response) as send:
            ask_rag.generate('Question', [{'id': 'S1'}], connection)
        request = send.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(payload['model'], 'chosen-model')
        self.assertIn('max_completion_tokens', payload)
        self.assertNotIn('max_tokens', payload)
        self.assertNotIn('reasoning', payload)

    def test_local_server_http_round_trip_and_citations(self):
        captured = {}
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                captured['models_path'] = self.path
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"data":[{"id":"local-test"}]}')

            def do_POST(self):
                captured['path'] = self.path
                captured['authorization'] = self.headers.get('Authorization')
                captured['payload'] = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                answer = {'answer': 'Supported [S1]', 'citations': ['S1'], 'grounded': True}
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({'choices': [{'message': {'content': json.dumps(answer)}, 'finish_reason': 'stop'}]}).encode())

            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f'http://127.0.0.1:{server.server_port}/v1'
            self.assertEqual(ask_rag.discover_models(base, ''), ['local-test'])
            result = ask_rag.generate('Question', [{'id': 'S1'}], ask_rag.Connection('local', base, 'local-test'))
            self.assertTrue(result['grounded'])
            self.assertEqual(captured['models_path'], '/v1/models')
            self.assertEqual(captured['path'], '/v1/chat/completions')
            self.assertIsNone(captured['authorization'])
            self.assertNotIn('reasoning', captured['payload'])
            self.assertNotIn('response_format', captured['payload'])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def test_unknown_citations_are_rejected(self):
        with self.assertRaises(ValueError):
            ask_rag.validate_answer(json.dumps({"answer": "Claim [S9]", "citations": ["S9"], "grounded": True}), [{"id": "S1"}])

    def test_grounded_answer_requires_inline_support(self):
        with self.assertRaises(ValueError):
            ask_rag.validate_answer(json.dumps({"answer": "Claim", "citations": [], "grounded": True}), [{"id": "S1"}])

    def test_supported_answer_and_abstention(self):
        for result in [{"answer": "Claim [S1]", "citations": ["S1"], "grounded": True},
                       {"answer": "The sources do not cover that.", "citations": [], "grounded": False}]:
            self.assertEqual(ask_rag.validate_answer(json.dumps(result), [{"id": "S1"}]), result)

    def test_empty_retrieval_does_not_call_provider(self):
        with patch.object(ask_rag, "select_sources", return_value=[]), patch.object(ask_rag, "generate") as generate:
            result, sources = ask_rag.answer_question(None, [], None, {}, "Question", "unused")
            generate.assert_not_called()
            self.assertFalse(result["grounded"])


if __name__ == "__main__":
    unittest.main()
