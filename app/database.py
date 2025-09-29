# database.py
from __future__ import annotations

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise RuntimeError(
        "DB_URL não configurado. Crie .env na raiz, por exemplo:\n"
        "DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/ipca"
    )

engine = create_engine(DB_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
