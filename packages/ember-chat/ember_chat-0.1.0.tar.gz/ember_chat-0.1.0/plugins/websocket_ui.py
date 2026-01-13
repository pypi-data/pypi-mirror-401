# plugins/websocket_ui.py
import asyncio
import json
import base64
import threading  # ← ЭТО БЫЛО УДАЛЕНО ПО ОШИБКЕ — ВОЗВРАЩАЕМ!
from core.protocol import encode_message

# Глобальные данные
AUTHORIZED = {}      # websocket → nickname
CLIENT_OBJECTS = {}  # websocket → объект клиента

class WebSocketClient:
    """Обёртка над WebSocket для совместимости с ядром"""
    def __init__(self, ws, core):
        self.ws = ws
        self.core = core
        self.addr = ("websocket", 0)
        self._authenticated = False
        self._nickname = "anonymous"

    def send(self, message: dict):
        """Вызывается ядром для отправки сообщения клиенту"""
        if not self._authenticated:
            return
        try:
            asyncio.create_task(self.ws.send(json.dumps(message)))
        except Exception as e:
            print(f"[WS] Ошибка отправки: {e}")
            self.core.unregister_client(self)

async def handle_websocket(websocket, core):
    client = WebSocketClient(websocket, core)
    CLIENT_OBJECTS[websocket] = client

    try:
        async for raw_message in websocket:
            try:
                msg = json.loads(raw_message)
                msg_type = msg.get("type")

                if not client._authenticated:
                    if msg_type == "auth":
                        password = msg.get("password", "")
                        nickname = (msg.get("nickname") or "anonymous").strip() or "anonymous"
                        auth_ok = True  # временно разрешаем всех

                        if auth_ok:
                            client._authenticated = True
                            client._nickname = nickname
                            client.addr = (
                                websocket.remote_address[0], websocket.remote_address[1]
                            ) if hasattr(websocket, 'remote_address') else ("websocket", 0)

                            core.register_client(client)

                            await websocket.send(json.dumps({
                                "from": "system",
                                "type": "auth_success",
                                "content": "Добро пожаловать!"
                            }))
                            print(f"[WS] Успешный вход: {nickname} ({client.addr[0]})")
                        else:
                            await websocket.send(json.dumps({
                                "from": "system",
                                "type": "auth_fail",
                                "content": "Неверный пароль."
                            }))
                            return
                    else:
                        await websocket.send(json.dumps({
                            "from": "system",
                            "type": "auth_required",
                            "content": "Требуется аутентификация."
                        }))
                        return
                    continue

                if msg_type == "text":
                    msg["from"] = client._nickname
                    core.on_message(msg, source=client)

                elif msg_type == "file_upload":
                    try:
                        filedata = base64.b64decode(msg.get("data", ""))
                        internal_msg = {
                            "from": client._nickname,
                            "type": "file_upload",
                            "filename": msg.get("filename", "file"),
                            "data": base64.b64encode(filedata).decode('ascii')
                        }
                        core.on_message(internal_msg, source=client)
                    except Exception as e:
                        print(f"[WS] Ошибка обработки файла: {e}")

            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "from": "system",
                    "type": "error",
                    "content": "Неверный JSON"
                }))

    except Exception as e:
        print(f"[WS] Ошибка соединения: {e}")
    finally:
        if websocket in CLIENT_OBJECTS:
            core.unregister_client(CLIENT_OBJECTS[websocket])
            del CLIENT_OBJECTS[websocket]
        if websocket in AUTHORIZED:
            del AUTHORIZED[websocket]

async def websocket_server(core, port):
    try:
        from websockets import serve
    except ImportError:
        print("[WS Plugin] ❌ Установи: pip install websockets")
        return

    async with serve(lambda ws: handle_websocket(ws, core), "0.0.0.0", port) as server:
        print(f"[WS Plugin] Слушаю ws://0.0.0.0:{port}")
        await asyncio.Future()

def start_websocket_thread(core, port):
    def run():
        asyncio.run(websocket_server(core, port))
    thread = threading.Thread(target=run, daemon=True)  # ← использует threading
    thread.start()
    return thread

def init_plugin(core, config=None):
    port = config.get("port", 8080) if config else 8080
    start_websocket_thread(core, port)
    print(f"[WebSocket UI Plugin] Активирован на порту {port}")