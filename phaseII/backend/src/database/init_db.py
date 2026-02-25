from .session import create_db_and_tables
from ..core.config import settings
from sqlmodel import SQLModel, create_engine

def init_db():
    # Create tables
    create_db_and_tables()
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()