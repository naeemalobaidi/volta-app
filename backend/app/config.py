"""Config — env-driven. Fail loud if SECRET_KEY is unset (never a silent dev default)."""
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY env var must be set. Refusing to start without it.")

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./volta.db")
TOKEN_TTL_HOURS = 24 * 7  # rolling session
