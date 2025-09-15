#!/bin/bash

# Exit on any error
set -e

# Change to the directory containing manage.py
cd "$(dirname "$0")"

# Set environment variable (adjust this to your project)
export DJANGO_SETTINGS_MODULE=config.settings  # Change as needed

# Activate virtual environment
# source venv/bin/activate  # Change this if your venv is elsewhere

# Forward all arguments to manage.py
python manage.py "$@"
