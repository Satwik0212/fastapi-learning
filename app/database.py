from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

URL_DATABASE = "postgresql+psycopg://postgres:Akki_2026.@localhost:5432/fastapi"

engine = create_engine(URL_DATABASE)
# Establishes the database connection engine that manages a pool of connections.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# A database session factory class used to instantiate sessions for database transactions.

Base = declarative_base()
# The declarative base class that all ORM model classes will inherit from to map Python classes to database tables.
async def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
