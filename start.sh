set -e

echo "🌱 Seeding database..."
python seed_data.py

echo "🚀 Starting Flask application..."
python run.py
