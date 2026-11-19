import json
import threading
import unittest
from contextlib import ExitStack
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from uptime_monitor import UptimeMonitor


class RetryIntegrationTest(unittest.TestCase):
    def test_webhook_failure_is_retried_before_recovery(self):
        service_status = 200
        deliveries = []

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(service_status)
                self.end_headers()

            def do_POST(self):
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                deliveries.append(payload["text"])
                self.send_response(503 if len(deliveries) == 1 else 204)
                self.end_headers()

            def log_message(self, format, *args):
                pass

        with ExitStack() as stack:
            server = stack.enter_context(ThreadingHTTPServer(("127.0.0.1", 0), Handler))
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            stack.callback(worker.join, 5)
            stack.callback(server.shutdown)

            endpoint = f"http://127.0.0.1:{server.server_port}"
            monitor = UptimeMonitor(f"{endpoint}/health", f"{endpoint}/webhook", timeout=2)
            monitor.poll()
            self.assertEqual(deliveries, [])

            service_status = 503
            monitor.poll()
            self.assertEqual(len(deliveries), 1)
            self.assertIn("ALERT: DOWN", deliveries[0])

            service_status = 200
            monitor.poll()
            self.assertEqual(deliveries, [deliveries[0], deliveries[0]])

            monitor.poll()
            self.assertEqual(len(deliveries), 3)
            self.assertIn("RECOVERY: UP", deliveries[2])
            self.assertFalse(monitor.pending)

            monitor.poll()
            self.assertEqual(len(deliveries), 3)


if __name__ == "__main__":
    unittest.main()
