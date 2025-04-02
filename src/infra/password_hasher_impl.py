import logging
from passlib.context import CryptContext

from src.core.interface.password_hasher import IPasswordHasher
from src.application.settings import settings

logger = logging.getLogger(__name__)


class PasswordHasher(IPasswordHasher):
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["argon2"],
            argon2__time_cost=3,  # Число итераций (3-5 для production)
            argon2__memory_cost=65536,  # 64MB (можно увеличить до 102400 — 100MB)
            argon2__parallelism=4,  # Число потоков
            argon2__hash_len=32,  # Длина хеша (32 байта)
            argon2__salt_size=16,  # Размер соли (16 байт)
        )

        self.pepper = self._load_pepper()
        self._settings = settings
        logging.info("PasswordHasher initialized")

    def _load_pepper(self) -> str:
        if settings.PROJ_ENV != "local":
            pass  # TODO СДЕЛАТЬ SecretsManager AWS Secrets Manager
        else:
            pepper = "Lol" * 32
        if not pepper:
            raise RuntimeError("PASSWORD_PEPPER environment variable is not set!")

        if len(pepper) < 32:
            raise ValueError("PASSWORD_PEPPER must be at least 32 characters long")

        return pepper

    def hash_password(self, password: str) -> str:
        if not password:
            raise ValueError("Password cannot be empty")
        return self.pwd_context.hash(password + self.pepper)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        if not all([plain_password, hashed_password]):
            return False
        return self.pwd_context.verify(plain_password + self.pepper, hashed_password)
