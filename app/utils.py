from cryptography.fernet import Fernet, InvalidToken
from app.config import settings

def get_fernet():
    key = settings.ENCRYPTION_KEY
    if not key:
        raise RuntimeError("ENCRYPTION_KEY not set")
    return Fernet(key.encode() if isinstance(key, str) else key)

def encrypt(value: str) -> str:
    f = get_fernet()
    return f.encrypt(value.encode()).decode()

def decrypt(token: str) -> str:
    f = get_fernet()
    return f.decrypt(token.encode()).decode()
