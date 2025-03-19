from flask import Flask, jsonify, request
from flask_cors import CORS
from src.webhooks.zoom_handler import zoom_webhook
from src.webhooks.slack_handler import handle_slack_command
from src.auth.oauth_manager import refresh_token
from src.utils.logger import log_info, log_error
from config import config

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": config.CORS_ORIGINS}})  # Allow cross-origin requests

@app.before_request
def log_request_info():
    log_info(f"Incoming request: {request.method} {request.url}")

# Registering routes
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

app.add_url_rule("/token/refresh", "refresh_token", refresh_token, methods=["POST"])
app.add_url_rule("/webhooks/zoom", "zoom_webhook", zoom_webhook, methods=["POST"])
app.add_url_rule("/webhooks/slack", "slack_webhook", handle_slack_command, methods=["POST"])

@app.errorhandler(500)
def internal_error(error):
    log_error(f"Internal Server Error: {error}")
    return jsonify({"error": "Internal Server Error"}), 500

@app.errorhandler(404)
def not_found(error):
    log_error(f"Route not found: {error}")
    return jsonify({"error": "Not Found"}), 404

if __name__ == "__main__":
    log_info("Starting Nexus AuthGrid API server...")
    app.run(port=config.PORT, debug=config.DEBUG)

import pytest
from server import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Nexus AuthGrid is running!"}

def test_auth_blueprint(client):
    """Test the auth blueprint route."""
    response = client.get('/auth')
    assert response.status_code == 200  # Adjust based on your actual endpoint response

def test_zoom_webhook_blueprint(client):
    """Test the Zoom webhook blueprint route."""
    response = client.get('/webhook/zoom')
    assert response.status_code == 200  # Adjust based on your actual endpoint response

def test_rate_limiter_blueprint(client):
    """Test the rate limiter blueprint route."""
    response = client.get('/ratelimit')
    assert response.status_code == 200  # Adjust based on your actual endpoint response

def test_activity_blueprint(client):
    """Test the activity blueprint route."""
    response = client.get('/user')
    assert response.status_code == 200  # Adjust based on your actual endpoint response

def test_recording_blueprint(client):
    """Test the recording blueprint route."""
    response = client.get('/recording')
    assert response.status_code == 200  # Adjust based on your actual endpoint response

def test_slack_blueprint(client):
    """Test the Slack blueprint route."""
    response = client.get('/slack')
    assert response.status_code == 200  # Adjust based on your actual endpoint response
    
def main.py import os
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
from src.auth.oauth import auth_blueprint
from src.ratelimit.limiter import rate_limiter_blueprint
from src.recordings.manager import recording_blueprint
from src.user_monitoring.activity import activity_blueprint
from src.webhooks.slack_handler import slack_blueprint
from src.webhooks.zoom_webhook_handler import zoom_webhook as zoom_webhook_blueprint    # Load environment variables
load_dotenv()
class Config:
    DEBUG = os.getenv("DEBUG", "True") == "True"
    LOG_FILE = os.getenv("LOG_FILE", "app.log")
    PORT = int(os.getenv("PORT", 5000))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Register blueprints (API modules)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(zoom_webhook_blueprint, url_prefix="/webhook/zoom")
    app.register_blueprint(rate_limiter_blueprint, url_prefix="/ratelimit")
    app.register_blueprint(activity_blueprint, url_prefix="/user")
    app.register_blueprint(recording_blueprint, url_prefix="/recording")
    app.register_blueprint(slack_blueprint, url_prefix="/slack")
    # Home route (for status checks)
    @app.route("/", methods=["GET"])
    def home():
        app.logger.info("Received request to home route")
        return jsonify({"message": "Nexus AuthGrid is running!"}), 200
    return app
# Initialize Flask app
app = create_app()
# Configure logging
logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler(Config.LOG_FILE)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
# Run the server
if __name__ == "__main__":
    app.run(host="

