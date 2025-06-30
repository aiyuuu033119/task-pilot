#!/usr/bin/env python3
"""
Database setup script for TaskPilot
Supports both SQLite and PostgreSQL
"""
import asyncio
import sys
import os
from pathlib import Path

# Add client directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "client"))

from config import config


async def setup_database():
    """Setup and initialize the database"""
    print("=== TaskPilot Database Setup ===")
    print(f"Database URL: {config.DATABASE_URL}")
    
    if config.DATABASE_URL.startswith("postgresql"):
        print("Setting up PostgreSQL database...")
        await setup_postgresql()
    else:
        print("Setting up SQLite database...")
        await setup_sqlite()


async def setup_sqlite():
    """Setup SQLite database"""
    from database import ChatDatabase
    
    db = ChatDatabase(config.DATABASE_URL.replace("sqlite:///", ""))
    
    try:
        print("1. Initializing SQLite database...")
        await db.init_db()
        print("✓ SQLite database initialized successfully")
        
        print("2. Testing basic operations...")
        # Test basic operations
        test_user_id = await db.create_user(
            email="admin@taskpilot.local",
            password="admin123",
            full_name="Admin User",
            display_name="Admin"
        )
        
        if test_user_id:
            print(f"✓ Test user created with ID: {test_user_id}")
        
        print("✅ SQLite database setup completed successfully!")
        
    except Exception as e:
        print(f"❌ SQLite setup failed: {e}")
        raise


async def setup_postgresql():
    """Setup PostgreSQL database"""
    from database_postgres import PostgreSQLDatabase
    
    db = PostgreSQLDatabase(config.DATABASE_URL)
    
    try:
        print("1. Connecting to PostgreSQL...")
        print("2. Creating database schema...")
        await db.init_db()
        print("✓ PostgreSQL database schema created successfully")
        
        print("3. Testing basic operations...")
        # Test basic operations
        test_user_id = await db.create_user(
            email="admin@taskpilot.local",
            password="admin123",
            full_name="Admin User",
            display_name="Admin"
        )
        
        if test_user_id:
            print(f"✓ Test user created with ID: {test_user_id}")
            
        print("4. Running migrations...")
        await run_alembic_migrations()
        
        print("✅ PostgreSQL database setup completed successfully!")
        
    except Exception as e:
        print(f"❌ PostgreSQL setup failed: {e}")
        print("Make sure PostgreSQL is running and accessible at:")
        print(f"  Host: {config.POSTGRES_HOST}")
        print(f"  Port: {config.POSTGRES_PORT}")
        print(f"  Database: {config.POSTGRES_DB}")
        print(f"  User: {config.POSTGRES_USER}")
        raise
    
    finally:
        await db.close()


async def run_alembic_migrations():
    """Run Alembic migrations for PostgreSQL"""
    try:
        import subprocess
        
        # Change to client directory
        client_dir = Path(__file__).parent / "client"
        
        # Run alembic revision
        result = subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", "Initial migration"],
            cwd=client_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Migration files created")
        else:
            print(f"⚠ Migration creation warning: {result.stderr}")
        
        # Run alembic upgrade
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=client_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Database migrations applied")
        else:
            print(f"❌ Migration failed: {result.stderr}")
            
    except Exception as e:
        print(f"⚠ Migration error (this is usually fine): {e}")


def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "="*50)
    print("DATABASE SETUP COMPLETED")
    print("="*50)
    
    if config.DATABASE_URL.startswith("postgresql"):
        print("""
PostgreSQL Database Setup Complete!

To start using PostgreSQL:
1. Make sure your PostgreSQL server is running
2. Use the following environment variables in your .env file:

POSTGRES_USER=taskpilot
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=taskpilot
DATABASE_URL=postgresql+asyncpg://taskpilot:your-secure-password@localhost:5432/taskpilot

To start PostgreSQL with Docker:
docker run -d \\
  --name taskpilot-postgres \\
  -e POSTGRES_USER=taskpilot \\
  -e POSTGRES_PASSWORD=secure_password_123 \\
  -e POSTGRES_DB=taskpilot \\
  -p 5432:5432 \\
  postgres:16
        """)
    else:
        print("""
SQLite Database Setup Complete!

Your database file is located at: """ + config.DATABASE_URL.replace("sqlite:///", "") + """

To switch to PostgreSQL later:
1. Set up PostgreSQL server
2. Update your .env file with PostgreSQL settings
3. Run this setup script again
        """)
    
    print("""
Next steps:
1. Start the MCP server: cd server && ./run.sh
2. Start the client: cd client && ./run.sh
3. Access the application at http://localhost:8000
    """)


async def main():
    """Main setup function"""
    try:
        await setup_database()
        print_usage_instructions()
        return 0
    except Exception as e:
        print(f"\n❌ Database setup failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)