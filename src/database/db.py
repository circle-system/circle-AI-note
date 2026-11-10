from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# -------------------
# データ保存先
# -------------------

APP_DIR = (
    Path.home()
    / "AI_Minutes"
)

APP_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_PATH = (
    APP_DIR
    / "database.db"
)

DATABASE_URL = (
    f"sqlite:///{DATABASE_PATH}"
)

# -------------------
# SQLAlchemy
# -------------------

engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)