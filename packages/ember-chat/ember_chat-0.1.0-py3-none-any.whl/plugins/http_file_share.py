# plugins/http_file_share.py
import os
import threading
import time
import base64
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote

FILES_DIR = "files"
os.makedirs(FILES_DIR, exist_ok=True)

class FileRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FILES_DIR, **kwargs)

    def do_GET(self):
        path = unquote(self.path.lstrip('/'))
        if not path or '..' in path or path.startswith(('/', '.')):
            self.send_error(403)
            return
        full = os.path.join(FILES_DIR, path)
        if os.path.isfile(full):
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Disposition", f'attachment; filename="{os.path.basename(full)}"')
            self.end_headers()
            with open(full, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

def start_http_server(port):
    httpd = HTTPServer(('0.0.0.0', port), FileRequestHandler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

def file_message_handler(core, message, source):
    if message.get("type") != "file_upload":
        return
    try:
        sender = message.get("from", "anon")
        filename = "".join(c for c in message.get("filename", "file") if c.isalnum() or c in "._- ")
        if not filename:
            filename = "file"
        data_b64 = message.get("data")
        if not isinstance(data_b64, str):
            return
        file_bytes = base64.b64decode(data_b64)
        unique = f"{int(time.time())}_{filename}"
        with open(os.path.join(FILES_DIR, unique), 'wb') as f:
            f.write(file_bytes)
        url = f"http://localhost:{8000}/{unique}"
        core.broadcast({
            "from": sender,
            "type": "file",
            "filename": message.get("filename", filename),
            "url": url
        }, sender=source)
        print(f"[HTTP] Файл сохранён: {unique}")
    except Exception as e:
        print(f"[HTTP] Ошибка: {e}")

def init_plugin(core, config=None):
    port = config.get("port", 8000) if config else 8000
    start_http_server(port)
    core.add_message_handler(file_message_handler)
    print(f"[HTTP File Plugin] Запущен на порту {port}")