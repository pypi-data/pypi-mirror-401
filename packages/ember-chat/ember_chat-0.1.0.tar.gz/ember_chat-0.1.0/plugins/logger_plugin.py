# plugins/logger_plugin.py
import json
import os
from datetime import datetime

# Глобальная переменная с путём к лог-файлу
LOG_FILE_PATH = "chat.log"

def log_message_handler(core, message, source):
    """Записывает каждое сообщение в файл в формате NDJSON"""
    try:
        log_entry = dict(message)
        log_entry["_logged_at"] = datetime.utcnow().isoformat() + "Z"
        if hasattr(source, 'addr'):
            log_entry["_ip"] = source.addr[0]
        else:
            log_entry["_ip"] = "unknown"

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            f.flush()

    except Exception as e:
        print(f"[Logger] Ошибка записи: {e}")

def init_plugin(core, config=None):
    global LOG_FILE_PATH  # ← теперь правильно: сначала global, потом присваивание
    
    log_file = config.get("file", "chat.log") if config else "chat.log"
    LOG_FILE_PATH = log_file

    # Создаём директорию, если нужно
    log_dir = os.path.dirname(LOG_FILE_PATH)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    core.add_message_handler(log_message_handler)
    print(f"[Logger Plugin] Логирование включено → {LOG_FILE_PATH}")