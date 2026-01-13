# plugins/auth_plugin.py
import hashlib
from core.protocol import encode_message

# Настройки по умолчанию
DEFAULT_PASSWORD = "123"
HASHED_PASSWORD = None  # будет вычислен при старте

# Хранилище авторизованных клиентов
AUTHORIZED_CLIENTS = {}  # socket -> nickname

def check_password(password: str) -> bool:
    """Проверяет пароль (поддерживает plain и sha256)"""
    if password == DEFAULT_PASSWORD:
        return True
    # Поддержка хэшированного пароля (безопаснее)
    if HASHED_PASSWORD and hashlib.sha256(password.encode()).hexdigest() == HASHED_PASSWORD:
        return True
    return False

def auth_message_handler(core, message, source):
    """Перехватывает первое сообщение для аутентификации"""
    # Если клиент уже авторизован — пропускаем
    if getattr(source, '_authenticated', False):
        return

    msg_type = message.get("type")
    if msg_type == "auth":
        password = message.get("password", "")
        nickname = message.get("nickname", "anonymous").strip() or "anonymous"

        if check_password(password):
            # Успешная авторизация
            source._authenticated = True
            source._nickname = nickname
            AUTHORIZED_CLIENTS[source] = nickname

            # Обновляем "from" в текущем сообщении (если есть content)
            if "content" in message:
                message["from"] = nickname
                core.on_message(message, source=source)  # повторно отправляем как обычное

            # Отправляем подтверждение
            source.send({
                "from": "system",
                "type": "auth_success",
                "content": "Добро пожаловать!"
            })
            print(f"[Auth] Успешный вход: {nickname} ({getattr(source, 'addr', ('unknown',))[0]})")
        else:
            # Неверный пароль
            source.send({
                "from": "system",
                "type": "auth_fail",
                "content": "Неверный пароль. Соединение закрыто."
            })
            core.unregister_client(source)
            print(f"[Auth] Отклонён: {getattr(source, 'addr', ('unknown',))[0]}")
    else:
        # Первое сообщение не auth — отклоняем
        source.send({
            "from": "system",
            "type": "auth_required",
            "content": "Требуется аутентификация: отправьте {\"type\":\"auth\", \"password\":\"...\", \"nickname\":\"...\"}"
        })
        core.unregister_client(source)

def init_plugin(core, config=None):
    global DEFAULT_PASSWORD, HASHED_PASSWORD

    if config:
        if "password" in config:
            DEFAULT_PASSWORD = config["password"]
        if "password_sha256" in config:
            HASHED_PASSWORD = config["password_sha256"].lower()

    # Предупреждение, если используется пароль по умолчанию
    if DEFAULT_PASSWORD == "changeme" and not HASHED_PASSWORD:
        print("[Auth Plugin] ⚠️ Используется пароль по умолчанию! Измените его в config.yaml.")

    core.add_message_handler(auth_message_handler)
    print("[Auth Plugin] Активирован. Требуется аутентификация.")