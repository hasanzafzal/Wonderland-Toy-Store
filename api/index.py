"""Flask application entrypoint for Vercel deployment"""
import sys
import os
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app

try:
    app = create_app()
except Exception as e:
    print(f"Error creating app: {e}")
    # Create a minimal app that can serve a health check
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return jsonify({
            'error': 'Application initialization failed',
            'details': str(e)
        }), 500

