# core/server.py
import time
from typing import List, Callable, Any

class ChatCore:
    def __init__(self):
        self.clients: List[Any] = []
        self.message_handlers: List[Callable] = []

    def register_client(self, client):
        self.clients.append(client)

    def unregister_client(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def broadcast(self, message: dict, sender=None):
        if "timestamp" not in message:
            message["timestamp"] = int(time.time())
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message)
                except Exception as e:
                    print(f"[Core] Ошибка отправки клиенту: {e}")

    def on_message(self, message: dict, source=None):
        print(f"[Core] Сообщение: {message.get('from', '?')}: {message.get('content', message)}")
        self.broadcast(message, sender=source)
        for handler in self.message_handlers:
            try:
                handler(self, message, source)
            except Exception as e:
                print(f"[Core] Ошибка в обработчике: {e}")

    def add_message_handler(self, handler: Callable):
        self.message_handlers.append(handler)