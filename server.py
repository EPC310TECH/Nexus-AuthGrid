import os
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from src.auth.oauth import auth_blueprint
from src.ratelimit.limiter import rate_limiter_blueprint
from src.recordings.manager import recording_blueprint
from src.user_monitoring.activity import activity_blueprint
from src.webhooks.slack_handler import slack_blueprint
from src.webhooks.zoom_webhook_handler import zoom_webhook as zoom_webhook_blueprint

# Load environment variables
load_dotenv()

class Config:
    DEBUG = os.getenv("DEBUG", "True") == "True"
    LOG_FILE = os.getenv("LOG_FILE", "app.log")
    PORT = int(os.getenv("PORT", 5000))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}})  # Allow cross-origin requests

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
    app.run(host="0.0.0.0", port=Config.PORT)
