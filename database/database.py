import os
import sys

from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(
    str(os.environ.get("POSTGRES_URI")),
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    """Create all database tables based on SQLAlchemy models."""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except SQLAlchemyError as e:
        print(f"Error creating database tables: {e}")
        sys.exit(1)

def check_postgres_connection():
    """Check if we can connect to PostgreSQL."""
    print(f"Trying to connect to PostgreSQL")

    try:
        # Try to execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Successfully connected to PostgreSQL!")
    except SQLAlchemyError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        print("\nPlease check your database settings:")
        sys.exit(1)

def get_db():
    """Dependency for getting DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
