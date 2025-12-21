"""Flask application entrypoint for Vercel deployment"""
import sys
import os
import traceback
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set environment variable for Vercel
os.environ['VERCEL'] = 'true'

try:
    print("Importing app module...")
    from app import create_app
    print("Creating Flask app...")
    app = create_app()
    print("App created successfully")
except Exception as e:
    print(f"Error creating app: {e}")
    print(traceback.format_exc())
    
    # Create a minimal app that can serve a health check
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    error_message = f"{type(e).__name__}: {str(e)}"
    error_traceback = traceback.format_exc()
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return jsonify({
            'error': 'Application initialization failed',
            'message': error_message,
            'traceback': error_traceback
        }), 500


