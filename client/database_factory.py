"""Database factory to choose between SQLite and PostgreSQL based on configuration"""
from typing import Union
from config import config
from database import ChatDatabase
from database_postgres import PostgreSQLDatabase


def get_database() -> Union[ChatDatabase, PostgreSQLDatabase]:
    """Get database instance based on DATABASE_URL configuration"""
    if config.DATABASE_URL.startswith("postgresql") or config.DATABASE_URL.startswith("postgres"):
        return PostgreSQLDatabase(config.DATABASE_URL)
    else:
        return ChatDatabase(config.DATABASE_URL.replace("sqlite:///", ""))


# Create database instance
db = get_database()