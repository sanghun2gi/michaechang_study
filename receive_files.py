#!/usr/bin/env python3
"""
파일 수신 서버 — Windows에서 .LOG 파일을 업로드 받음
실행: python receive_files.py
"""
import http.server, os, json

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'gps_log')
os.makedirs(SAVE_DIR, exist_ok=True)
PORT = 8765

class UploadHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            length   = int(self.headers['Content-Length'])
            filename = self.headers.get('X-Filename', 'unknown.LOG')
            data     = self.rfile.read(length)
            save_path = os.path.join(SAVE_DIR, os.path.basename(filename))
            with open(save_path, 'wb') as f:
                f.write(data)
            print(f'  받음: {filename} ({length:,} bytes)')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404); self.end_headers()

    def do_GET(self):
        if self.path == '/ping':
            self.send_response(200); self.end_headers()
            self.wfile.write(b'pong')
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, *args): pass   # 불필요한 로그 숨김

print(f'수신 서버 시작 — 포트 {PORT}')
print(f'저장 경로: {SAVE_DIR}')
print(f'Windows에서 upload_to_server.py 를 실행하세요...\n')
http.server.HTTPServer(('0.0.0.0', PORT), UploadHandler).serve_forever()
