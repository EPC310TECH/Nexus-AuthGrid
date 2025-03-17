import os

from dotenv import load_dotenv
from flask import Flask, jsonify

from src.auth.oauth import auth_blueprint
from src.ratelimit.limiter import rate_limiter_blueprint
from src.recordings.manager import recording_blueprint
from src.user_monitoring.activity import activity_blueprint
from src.webhooks.slack_handler import slack_blueprint
from src.webhooks.zoom_webhook_handler import zoom_webhook as zoom_webhook_blueprint

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

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
    print("Received request to home route")
    return jsonify({"message": "Nexus AuthGrid is running!"}), 200


# Run the server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default port: 5000
    app.run(host="0.0.0.0", port=port, debug=True)
