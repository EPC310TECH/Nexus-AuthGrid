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
from test_server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health check route."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_auth_blueprint(client):
    """Test the auth blueprint route."""
    response = client.get('/auth')
    assert response.status_code == 200  # Adjust based on your actual endpoint response

def test_zoom_webhook_blueprint(client):
    """Test the Zoom webhook blueprint route."""
    response = client.post('/webhooks/zoom')
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
    response = client.post('/webhooks/slack')
    assert response.status_code == 200  # Adjust based on your actual endpoint response

