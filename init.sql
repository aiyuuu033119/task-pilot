-- Initialize TaskPilot PostgreSQL database
-- This file is executed when the PostgreSQL container starts for the first time

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Database is already created by the container environment variables
-- Just add any additional setup here if needed

-- Grant permissions (usually not needed since we're using the same user)
GRANT ALL PRIVILEGES ON DATABASE taskpilot TO taskpilot;