import hashlib
import secrets
import string


def generate_secure_ticket(length: int = 8) -> str:
    """Генерация криптографически безопасного тикета"""
    # Исключаем неоднозначные символы (l/I/1, 0/O)
    alphabet = string.ascii_letters + string.digits
    ambiguous = {"l", "I", "1", "0", "O"}
    alphabet = "".join(c for c in alphabet if c not in ambiguous)

    # Генерация с использованием secrets (криптографически безопасно)
    return "".join(secrets.choice(alphabet) for _ in range(length))


def hash_ticket(ticket: str) -> str:
    """Хэширование тикета"""
    return hashlib.sha256(("pepper" + ticket).encode()).hexdigest()
