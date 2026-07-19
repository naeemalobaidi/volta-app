"""DB engine + helpers."""
from sqlalchemy import create_engine
from .models import metadata
from ..config import DATABASE_URL

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

def init_db():
    metadata.create_all(engine)
