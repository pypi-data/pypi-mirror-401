#!/bin/bash
set -e

echo "Starting deployment script..."
echo "DB_HOST: $DB_HOST"
echo "DB_USER: $DB_USER"
echo "DB_NAME: $DB_NAME"

# Note: Cloud SQL Proxy mounts the socket asynchronously after container starts.
# We start the app immediately and let it handle DB connections with retry logic.
echo "Starting application (Cloud SQL socket will mount in background)..."

# Run database migrations - block app startup to ensure schema is ready
echo "Running database migrations (blocking startup)..."

# Try migrations with retries
for i in {1..5}; do
    echo "Migration attempt $i/5..."
    if timeout 60s alembic upgrade head 2>&1; then
        echo "Migrations completed successfully."
        break
    else
        if [ $i -lt 5 ]; then
            echo "Migration failed, retrying in 5s..."
            sleep 5
        else
            echo "WARNING: Migrations failed after 5 attempts. App will start anyway, but may encounter schema errors."
        fi
    fi
done

# Start the application immediately - don't wait for migrations
echo "Starting uvicorn..."
exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers
