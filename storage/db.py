# storage/db.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use Postgres connection string from environment variable or default fallback
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db:5432/calls"  # Use this for dev; replace with Postgres URL for prod

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to use in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
