from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

db_path = os.path.join("/tmp", "journal.db")
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)