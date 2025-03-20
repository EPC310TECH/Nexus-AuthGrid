from flask import Flask, jsonify, request
from flask_cors import CORS
from src.webhooks.zoom_handler import zoom_webhook
from src.webhooks.slack_handler import handle_slack_command
from src.auth.oauth_manager import refresh_token
from src.utils.logger import log_info, log_error
from config import configfile
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": config.CORS_ORIGINS}})  # Allow cross-origin requests
AUTHCORE_ACCOUNT_ID = os.getenv("AuthCore_Account_ID")
@app.before_requestD = os.getenv("TokenVault_Client_ID")
def log_request_info():getenv("TokenVault_Secret_Token")
    log_info(f"Incoming request: {request.method} {request.url}")
ION_TOKEN = os.getenv("RateShield_Verification_Token")
# Registering routes
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

app.add_url_rule("/token/refresh", "refresh_token", refresh_token, methods=["POST"])
app.add_url_rule("/webhooks/zoom", "zoom_webhook", zoom_webhook, methods=["POST"])
app.add_url_rule("/webhooks/slack", "slack_webhook", handle_slack_command, methods=["POST"])
# Function to get Zoom OAuth token from TokenVault
@app.errorhandler(500)
def internal_error(error):
    log_error(f"Internal Server Error: {error}")
    return jsonify({"error": "Internal Server Error"}), 500
": f"Basic {TOKENVAULT_CLIENT_ID}:{TOKENVAULT_SECRET}",
@app.errorhandler(404)        "Content-Type": "application/x-www-form-urlencoded",
def not_found(error):    }
    log_error(f"Route not found: {error}")    data = {"grant_type": "client_credentials"}
    return jsonify({"error": "Not Found"}), 404
    response = requests.post(token_url, headers=headers, data=data)
if __name__ == "__main__":    if response.status_code == 200:
    log_info("Starting Nexus AuthGrid API server...")        token_info = response.json()
    app.run(port=config.PORT, debug=config.DEBUG)        access_tokens["zoom"] = token_info["access_token"]
    return received_token == RATESHIELD_VERIFICATION_TOKEN


# Main webhook route
@app.route("/webhook", methods=["POST"])
def zoom_webhook():
    if not verify_webhook_request(request.headers):
        return jsonify({"message": "Unauthorized"}), 403

    event_data = request.json
    event_type = event_data.get("event")

    print(f"🔔 Received Zoom Event: {event_type}")

    # Handle different event types
    event_handlers = {
        "meeting.started": handle_meeting_started,
        "meeting.ended": handle_meeting_ended,
        "recording.completed": handle_recording_completed,
        "user.signed_in": handle_user_signed_in,
        "api.rate_limited": handle_rate_limit_exceeded,
    }

    if event_type in event_handlers:
        event_handlers[event_type](event_data)
    else:
        print("⚠️ Unhandled Event:", event_type)

    return jsonify({"message": "Event received"}), 200


# Event Handlers

def handle_meeting_started(event_data):
    meeting_id = event_data["payload"]["object"]["id"]
    host_email = event_data["payload"]["object"]["host_email"]
    print(f"🚀 Meeting {meeting_id} started by {host_email}")


def handle_meeting_ended(event_data):
    meeting_id = event_data["payload"]["object"]["id"]
    print(f"📅 Meeting {meeting_id} ended")


def handle_recording_completed(event_data):
    recording_url = event_data["payload"]["object"]["recording_files"][0]["play_url"]
    print(f"🎥 New Recording Available: {recording_url}")


def handle_user_signed_in(event_data):
    user_email = event_data["payload"]["object"]["email"]
    print(f"👤 User Signed In: {user_email}")


def handle_rate_limit_exceeded(event_data):
    print("⚠️ API Rate Limit Exceeded! Consider throttling requests.")

# Run Flask Server
if __name__ == "__main__":
    app.run(port=5000, debug=True)
