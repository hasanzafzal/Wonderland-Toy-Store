"""Flask application entrypoint for Vercel deployment"""
import sys
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app

app = create_app()
