from flask import Flask, jsonify, request, request
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
@app.route("/health", methods=["GET"])en/refresh", "refresh_token", refresh_token, methods=["POST"])
def health_check():s/zoom", "zoom_webhook", zoom_webhook, methods=["POST"])
    return jsonify({"status": "healthy"}), 200ck_webhook", handle_slack_command, methods=["POST"])

# Registering routes@app.route("/health", methods=["GET"])
app.add_url_rule("/token/refresh", "refresh_token", refresh_token, methods=["POST"])
app.add_url_rule("/webhooks/zoom", "zoom_webhook", zoom_webhook, methods=["POST"])status": "healthy"}), 200
app.add_url_rule("/webhooks/slack_handler", "slack_webhook", handle_slack_command, methods=["POST"])

@app.errorhandler(500)def internal_error(error):
def internal_error(error):erver Error: {error}")
    log_error(f"Internal Server Error: {error}")), 500
    return jsonify({"error": "Internal Server Error"}), 500
@app.errorhandler(404)









    app.run(port=config.PORT, debug=config.DEBUG)    log_info("Starting Nexus AuthGrid API server...")if __name__ == "__main__":    return jsonify({"error": "Not Found"}), 404    log_error(f"Route not found: {error}")def not_found(error):@app.errorhandler(404)def not_found(error):
    log_error(f"Route not found: {error}")
    return jsonify({"error": "Not Found"}), 404

if __name__ == "__main__":
    log_info("Starting Nexus AuthGrid API server...")
    app.run(port=5000, debug=True)
