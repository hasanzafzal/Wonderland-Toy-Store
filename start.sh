#!/bin/bash
set -e

mkdir -p /app/instance
chmod 777 /app/instance

echo "🌱 Seeding database..."
python seed_data.py

echo "🚀 Starting Flask application..."
python run.py
