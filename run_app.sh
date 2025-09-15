#!/bin/bash

# Exit on error
set -e

# Change to the directory where your manage.py file is
cd "$(dirname "$0")"

# Set environment variables (optional)
export DJANGO_SETTINGS_MODULE=config.settings  # Replace with your settings path
export PYTHONUNBUFFERED=1  # Optional: ensures real-time output

# # Activate virtual environment
# echo "Activating virtual environment..."
# source venv/bin/activate  # Change this path if your venv is located elsewhere

# Apply migrations
echo "Applying database migrations..."
python3 manage.py migrate

# Collect static files (optional, skip in dev)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Start Django development server
echo "Starting Django development server..."
python3 manage.py runserver 0.0.0.0:8000