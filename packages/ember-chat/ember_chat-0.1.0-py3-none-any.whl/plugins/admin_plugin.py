# plugins/admin_plugin.py
import threading
import sys
import json
import os
from typing import Set, Dict, Any

# Глобальные данные модуля
MODERATORS: Set[str] = set()
BANNED_IPS: Set[str] = set()
BANNED_NAMES: Set[str] = set()
CLIENT_INFO: Dict[str, Dict[str, Any]] = {}  # nickname -> {ip, connected_at, ...}

def save_bans():
    """Сохраняет баны в файл при завершении"""
    data = {
        "banned_ips": list(BANNED_IPS),
        "banned_names": list(BANNED_NAMES)
    }
    with open("bans.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_bans():
    """Загружает баны при старте"""
    global BANNED_IPS, BANNED_NAMES
    if os.path.exists("bans.json"):
        try:
            with open("bans.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                BANNED_IPS = set(data.get("banned_ips", []))
                BANNED_NAMES = set(data.get("banned_names", []))
            print(f"[Admin] Загружено {len(BANNED_IPS)} забаненных IP и {len(BANNED_NAMES)} имён.")
        except Exception as e:
            print(f"[Admin] Ошибка загрузки банов: {e}")

def console_input_loop(core):
    """Обрабатывает команды из серверной консоли"""
    print("\n" + "="*50)
    print("🛠️  Админская консоль активна!")
    print("Команды:")
    print("  /mod <ник>          — назначить модератора")
    print("  /unmod <ник>        — снять модератора")
    print("  /ban <ник/IP>       — забанить по нику или IP")
    print("  /unban <ник/IP>     — разбанить")
    print("  /kick <ник>         — выгнать из чата")
    print("  /list               — список пользователей")
    print("  /mods               — список модераторов")
    print("  /bans               — список банов")
    print("="*50 + "\n")

    while True:
        try:
            cmd = input().strip()
            if not cmd:
                continue

            parts = cmd.split()
            if parts[0] == "/mod" and len(parts) == 2:
                MODERATORS.add(parts[1])
                print(f"✅ {parts[1]} теперь модератор.")

            elif parts[0] == "/unmod" and len(parts) == 2:
                MODERATORS.discard(parts[1])
                print(f"❌ {parts[1]} больше не модератор.")

            elif parts[0] == "/ban" and len(parts) == 2:
                target = parts[1]
                if '.' in target and any(c.isdigit() for c in target):  # похоже на IP
                    BANNED_IPS.add(target)
                    print(f"🚫 IP {target} забанен.")
                else:
                    BANNED_NAMES.add(target)
                    print(f"🚫 Пользователь {target} забанен.")
                save_bans()

            elif parts[0] == "/unban" and len(parts) == 2:
                target = parts[1]
                if target in BANNED_IPS:
                    BANNED_IPS.remove(target)
                    print(f"✅ IP {target} разбанен.")
                elif target in BANNED_NAMES:
                    BANNED_NAMES.remove(target)
                    print(f"✅ Пользователь {target} разбанен.")
                else:
                    print("⚠️ Не найден в банах.")
                save_bans()

            elif parts[0] == "/kick" and len(parts) == 2:
                nick = parts[1]
                if nick in CLIENT_INFO:
                    client_obj = CLIENT_INFO[nick].get("client")
                    if client_obj:
                        try:
                            client_obj.send({
                                "from": "system",
                                "type": "system",
                                "content": "Вы были выгнаны администратором."
                            })
                            core.unregister_client(client_obj)
                            del CLIENT_INFO[nick]
                            print(f"👢 {nick} выгнан.")
                        except:
                            pass
                else:
                    print("⚠️ Пользователь не найден.")

            elif parts[0] == "/list":
                if CLIENT_INFO:
                    print("\n👥 Пользователи:")
                    for nick, info in CLIENT_INFO.items():
                        mod = " (мод)" if nick in MODERATORS else ""
                        print(f"  {nick}{mod} — {info.get('ip', '???')}")
                else:
                    print("📭 Никого нет в чате.")

            elif parts[0] == "/mods":
                if MODERATORS:
                    print("\n🛡️ Модераторы:", ", ".join(MODERATORS))
                else:
                    print("🛡️ Модераторов нет.")

            elif parts[0] == "/bans":
                print("\n🚫 Забаненные IP:", ", ".join(BANNED_IPS) if BANNED_IPS else "нет")
                print("📛 Забаненные ники:", ", ".join(BANNED_NAMES) if BANNED_NAMES else "нет")

            else:
                print("❓ Неизвестная команда. Введите /help для справки.")

        except (EOFError, KeyboardInterrupt):
            break
        except Exception as e:
            print(f"❗ Ошибка: {e}")

def message_handler(core, message, source):
    """Перехватывает сообщения для проверки прав и обновления данных"""
    sender = message.get("from", "anonymous")
    
    # Сохраняем информацию о пользователе (если есть source с IP)
    if hasattr(source, 'addr') and source.addr:
        ip = source.addr[0]
        CLIENT_INFO[sender] = {
            "ip": ip,
            "client": source,
            "connected_at": CLIENT_INFO.get(sender, {}).get("connected_at", None) or __import__('time').time()
        }

    # Проверка: не забанен ли отправитель?
    if sender in BANNED_NAMES:
        if hasattr(source, 'send'):
            source.send({
                "from": "system",
                "type": "system",
                "content": "Вы забанены и не можете отправлять сообщения."
            })
        return

    # Проверка IP (если доступен)
    if hasattr(source, 'addr') and source.addr[0] in BANNED_IPS:
        if hasattr(source, 'send'):
            source.send({
                "from": "system",
                "type": "system",
                "content": "Ваш IP забанен."
            })
        core.unregister_client(source)
        if sender in CLIENT_INFO:
            del CLIENT_INFO[sender]
        return

def init_plugin(core, config=None):
    """Инициализация админского плагина"""
    load_bans()
    core.add_message_handler(message_handler)
    
    # Запуск консоли в отдельном потоке
    thread = threading.Thread(target=console_input_loop, args=(core,), daemon=True)
    thread.start()
    
    print("[Admin Plugin] Активирован. Введите команды в эту консоль.")