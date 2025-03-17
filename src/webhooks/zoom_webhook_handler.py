import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()

# Retrieve stored credentials
AUTHCORE_ACCOUNT_ID = os.getenv("AuthCore_Account_ID")
TOKENVAULT_CLIENT_ID = os.getenv("TokenVault_Client_ID")
TOKENVAULT_SECRET = os.getenv("TokenVault_Secret_Token")
RATESHIELD_SECRET = os.getenv("RateShield_Client_Secret")
RATESHIELD_VERIFICATION_TOKEN = os.getenv("RateShield_Verification_Token")
AUTHRELAY_CLIENT_ID = os.getenv("AuthRelay_Client_ID")

app = Flask(__name__)

# Temporary storage for OAuth tokens
access_tokens = {}


# Function to get Zoom OAuth token from TokenVault
def get_zoom_access_token():
    global access_tokens
    token_url = "https://zoom.us/oauth/token"
    headers = {
        "Authorization": f"Basic {TOKENVAULT_CLIENT_ID}:{TOKENVAULT_SECRET}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        token_info = response.json()
        access_tokens["zoom"] = token_info["access_token"]
        return token_info["access_token"]
    else:
        print("❌ Failed to obtain OAuth token:", response.text)
        return None


# Verify webhook request authenticity
def verify_webhook_request(headers):
    received_token = headers.get("Authorization")
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
