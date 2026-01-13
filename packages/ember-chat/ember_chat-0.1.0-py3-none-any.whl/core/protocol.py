# core/protocol.py
import json

def encode_message(message: dict) -> bytes:
    json_bytes = json.dumps(message, ensure_ascii=False).encode('utf-8')
    return len(json_bytes).to_bytes(4, 'big') + json_bytes

def decode_message(data: bytes) -> dict:
    return json.loads(data.decode('utf-8'))