# plugins/tcp_transport.py
import socket
import threading
from core.protocol import decode_message, encode_message

class TCPClient:
    def __init__(self, sock, addr, core):
        self.sock = sock
        self.addr = addr
        self.core = core

    def send(self, message: dict):
        try:
            self.sock.sendall(encode_message(message))
        except:
            self.core.unregister_client(self)

    def run(self):
        try:
            while True:
                header = self.sock.recv(4)
                if len(header) < 4:
                    break
                msg_len = int.from_bytes(header, 'big')
                raw = b''
                while len(raw) < msg_len:
                    chunk = self.sock.recv(msg_len - len(raw))
                    if not chunk:
                        break
                    raw += chunk
                if raw:
                    msg = decode_message(raw)
                    msg.setdefault("from", "anonymous")
                    self.core.on_message(msg, source=self)
        except Exception as e:
            pass
        finally:
            self.core.unregister_client(self)
            self.sock.close()

def init_plugin(core, config=None):
    host = config.get("host", "0.0.0.0") if config else "0.0.0.0"
    port = config.get("port", 12345) if config else 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"[TCP Plugin] Слушаю {host}:{port}")

    def accept_loop():
        while True:
            try:
                sock, addr = server.accept()
                client = TCPClient(sock, addr, core)
                core.register_client(client)
                threading.Thread(target=client.run, daemon=True).start()
            except:
                break

    threading.Thread(target=accept_loop, daemon=True).start()