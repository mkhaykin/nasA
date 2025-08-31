import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key-here"

    ADMIN_PORT = 3000
    USER_PORT = 46032

    SHARED_FOLDER = Path(os.environ.get("SHARED_FOLDER", "./uploads"))
    MAX_CONTENT_LENGTH = int(
        os.environ.get(
            "MAX_CONTENT_LENGTH",
            100 * 1024 * 1024,
        ),
    )  # 100MB default

    DB_FOLDER = Path(os.environ.get("DB_FOLDER", "./db"))
    DB_PATH = Path(DB_FOLDER) / "nas.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    DATABASE_TRACK_MODIFICATIONS = False

    TICKET_LENGTH = 7
    RANDOM_SUFFIX_LENGTH = 7
