import hashlib


def sha1(value: str, length: int) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:length]
