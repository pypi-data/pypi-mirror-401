import hashlib


def hash_text(text: str) -> str:
    if not text:
        return ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def safe_value(value: str, max_len: int = 500) -> str:
    if not value:
        return ""
    value = str(value)
    return value[:max_len]
