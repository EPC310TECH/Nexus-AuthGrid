from flask import Flask, jsonify
from flask_cors import CORS
from src.webhooks.zoom_handler import zoom_webhook
from src.webhooks.slack_handler import handle_slack_command
from src.auth.oauth_manager import refresh_token
from src.utils.logger import log_info, log_error

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Registering routes
app.add_url_rule("/token/refresh", "refresh_token", refresh_token, methods=["POST"])
app.add_url_rule("/webhooks/zoom", "zoom_webhook", zoom_webhook, methods=["POST"])
app.add_url_rule("/webhooks/slack_handler", "slack_webhook", handle_slack_command(), methods=["POST"])

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
    app.run(port=5000, debug=True)
