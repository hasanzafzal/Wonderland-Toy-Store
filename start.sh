#!/bin/bash
set -e

mkdir -p /app/instance
chmod 777 /app/instance

# Ensure products images directory has correct permissions
mkdir -p /app/app/static/images/products
chmod 777 /app/app/static/images
chmod 777 /app/app/static/images/products

echo "🌱 Seeding database..."
python seed_data.py

echo "🚀 Starting Flask application..."
python run.py
