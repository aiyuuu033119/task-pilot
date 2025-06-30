# Database Setup Guide

This guide covers setting up both SQLite and PostgreSQL databases for TaskPilot.

## Quick Start

### 1. Automatic Setup (Recommended)

Run the setup script to automatically configure your database:

```bash
python setup_database.py
```

This will:
- Detect your database configuration
- Initialize the database schema
- Create test data
- Provide next steps

### 2. Manual Setup

If you prefer manual setup, follow the steps below for your chosen database.

## SQLite Setup (Default)

SQLite is the default database and requires no additional setup.

### Configuration

Create or update `client/.env`:

```env
# Database (SQLite - default)
DATABASE_URL=sqlite:///./task_pilot.db

# AI Provider API Keys
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### Initialization

```bash
cd client
source venv/bin/activate
python -c "
import asyncio
from database import ChatDatabase
async def init(): 
    db = ChatDatabase()
    await db.init_db()
    print('SQLite database initialized!')
asyncio.run(init())
"
```

## PostgreSQL Setup

PostgreSQL provides better performance and features for production use.

### Prerequisites

1. **Install PostgreSQL**
   - Ubuntu/Debian: `sudo apt install postgresql postgresql-contrib`
   - macOS: `brew install postgresql`
   - Windows: Download from [postgresql.org](https://www.postgresql.org/download/)

2. **Or use Docker**
   ```bash
   docker run -d \
     --name taskpilot-postgres \
     -e POSTGRES_USER=taskpilot \
     -e POSTGRES_PASSWORD=secure_password_123 \
     -e POSTGRES_DB=taskpilot \
     -p 5432:5432 \
     postgres:16
   ```

### Database Creation

Connect to PostgreSQL and create the database:

```sql
-- Connect as postgres user
sudo -u postgres psql

-- Create user and database
CREATE USER taskpilot WITH PASSWORD 'secure_password_123';
CREATE DATABASE taskpilot OWNER taskpilot;
GRANT ALL PRIVILEGES ON DATABASE taskpilot TO taskpilot;

-- Exit
\q
```

### Configuration

Create or update `client/.env`:

```env
# Database (PostgreSQL)
POSTGRES_USER=taskpilot
POSTGRES_PASSWORD=secure_password_123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=taskpilot
DATABASE_URL=postgresql+asyncpg://taskpilot:secure_password_123@localhost:5432/taskpilot

# AI Provider API Keys
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### Schema Creation

```bash
cd client
source venv/bin/activate

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### Alternative: Direct Schema Creation

```bash
cd client
source venv/bin/activate
python -c "
import asyncio
from database_postgres import PostgreSQLDatabase
from config import config
async def init(): 
    db = PostgreSQLDatabase(config.DATABASE_URL)
    await db.init_db()
    print('PostgreSQL schema created!')
    await db.close()
asyncio.run(init())
"
```

## Testing Database Connection

Use the test script to verify your database setup:

```bash
cd client
source venv/bin/activate
python test_database.py
```

This will test:
- Database connection
- User creation and authentication
- Session management
- Message storage and retrieval
- Token management

## Docker Compose Setup

For easy PostgreSQL setup with Docker Compose:

```bash
# Start PostgreSQL
docker compose -f docker-compose.postgres.yml up -d

# Check status
docker compose -f docker-compose.postgres.yml ps

# View logs
docker compose -f docker-compose.postgres.yml logs postgres

# Stop
docker compose -f docker-compose.postgres.yml down
```

## Migration Management

### Creating Migrations

When you modify the database models:

```bash
cd client
source venv/bin/activate
alembic revision --autogenerate -m "Description of changes"
```

### Applying Migrations

```bash
cd client
source venv/bin/activate
alembic upgrade head
```

### Migration History

```bash
# View current version
alembic current

# View migration history
alembic history

# Downgrade (if needed)
alembic downgrade -1
```

## Database Administration

### PostgreSQL Admin Commands

```sql
-- Connect to database
psql -U taskpilot -d taskpilot -h localhost

-- List tables
\dt

-- Describe table structure
\d users

-- View table data
SELECT * FROM users LIMIT 5;

-- Exit
\q
```

### SQLite Admin Commands

```bash
# Open database
sqlite3 task_pilot.db

# List tables
.tables

# Describe table structure
.schema users

# View table data
SELECT * FROM users LIMIT 5;

# Exit
.quit
```

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   ```bash
   cd client
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **PostgreSQL connection refused**
   - Check if PostgreSQL is running: `sudo systemctl status postgresql`
   - Verify connection settings in `.env`
   - Check firewall settings

3. **Permission errors**
   - Ensure database user has proper permissions
   - Check file permissions for SQLite database

4. **Migration errors**
   - Check database connection
   - Ensure models are properly imported in `alembic/env.py`
   - Review migration files before applying

### Getting Help

1. Check the logs: `tail -f client/app.log`
2. Run the test script: `python test_database.py`
3. Verify configuration: `python -c "from config import config; print(config.DATABASE_URL)"`

## Performance Considerations

### SQLite
- Good for development and small applications
- Single file storage
- No network overhead
- Limited concurrent writes

### PostgreSQL
- Better for production environments
- Excellent concurrent performance
- Advanced features (JSON, full-text search, etc.)
- Requires separate server process

## Security Best Practices

1. **Use strong passwords** for database users
2. **Limit database access** to necessary hosts only
3. **Use SSL/TLS** for remote connections
4. **Regular backups** of your database
5. **Keep software updated** (PostgreSQL, Python packages)

## Backup and Recovery

### SQLite Backup
```bash
# Create backup
cp task_pilot.db task_pilot.db.backup

# Restore backup
cp task_pilot.db.backup task_pilot.db
```

### PostgreSQL Backup
```bash
# Create backup
pg_dump -U taskpilot -h localhost taskpilot > backup.sql

# Restore backup
psql -U taskpilot -h localhost taskpilot < backup.sql
```