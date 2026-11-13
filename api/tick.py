import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(_file_))))
from http.server import BaseHTTPRequestHandler
from core.runtime import make_env, authorized
from core.bot import tick

class handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        b = json.dumps(obj, default=float).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b)

    def _run_tick(self):
        if not authorized(self.headers):
            return self._send(401, {"error": "unauthorized"})
        try:
            self._send(200, tick(make_env()))
        except Exception as e:
            self._send(500, {"error": repr(e)[:300]})

    def do_GET(self):
        self._run_tick()

    def do_POST(self):
        self._run_tick()
