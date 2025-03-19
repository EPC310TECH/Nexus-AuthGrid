import os
import requests
import logging
from flask import Blueprint, jsonify, request
from src.auth.oauth import get_stored_token, refresh_token

zoom_blueprint = Blueprint("zoom", __name__)

# Zoom API Base URL (Ngrok or Zoom Production)
ZOOM_API_BASE = os.getenv("ZOOM_BASE_URL", "https://api.zoom.us/v2")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_zoom_headers():
    """Retrieve OAuth token and construct authorization headers."""
    token = get_stored_token()
    if not token:
        logger.warning("No valid Zoom token found, attempting refresh.")
        token = refresh_token()

    if not token:
        raise Exception("Unable to retrieve Zoom access token.")

    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def zoom_api_request(method, endpoint, data=None, params=None):
    """Generic function for making Zoom API requests."""
    url = f"{ZOOM_API_BASE}/{endpoint}"
    headers = get_zoom_headers()

    try:
        response = requests.request(method, url, headers=headers, json=data, params=params)

        if response.status_code == 401:  # Token expired, try refreshing
            logger.warning("Unauthorized. Attempting token refresh.")
            refresh_token()
            headers = get_zoom_headers()  # Get new token
            response = requests.request(method, url, headers=headers, json=data, params=params)

        response.raise_for_status()  # Raise error for 4xx/5xx status codes
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Zoom API request failed: {e}")
        return {"error": str(e)}


@zoom_blueprint.route("/users", methods=["GET"])
def get_zoom_users():
    """Retrieve a list of Zoom users."""
    users = zoom_api_request("GET", "users")
    return jsonify(users or {"error": "Failed to fetch users"}), 200 if users else 500


@zoom_blueprint.route("/meetings/create", methods=["POST"])
def create_meeting():
    """Create a new Zoom meeting."""
    user_id = request.json.get("user_id")
    topic = request.json.get("topic", "New Meeting")
    start_time = request.json.get("start_time")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    meeting_data = {
        "topic": topic,
        "type": 2,  # Scheduled meeting
        "start_time": start_time,
        "timezone": "UTC",
        "settings": {
            "host_video": True,
            "participant_video": True,
            "mute_upon_entry": True,
            "waiting_room": True
        }
    }

    meeting = zoom_api_request("POST", f"users/{user_id}/meetings", data=meeting_data)
    return jsonify(meeting or {"error": "Failed to create meeting"}), 200 if meeting else 500


@zoom_blueprint.route("/meetings/<meeting_id>", methods=["GET"])
def get_meeting_details(meeting_id):
    """Fetch details of a specific meeting."""
    meeting = zoom_api_request("GET", f"meetings/{meeting_id}")
    return jsonify(meeting or {"error": "Failed to fetch meeting"}), 200 if meeting else 500


@zoom_blueprint.route("/meetings/<meeting_id>/delete", methods=["DELETE"])
def delete_meeting(meeting_id):
    """Delete a Zoom meeting."""
    response = zoom_api_request("DELETE", f"meetings/{meeting_id}")
    return jsonify(response or {"error": "Failed to delete meeting"}), 200 if response else 500


@zoom_blueprint.route("/recordings/<user_id>", methods=["GET"])
def get_user_recordings(user_id):
    """Retrieve a list of cloud recordings for a user."""
    recordings = zoom_api_request("GET", f"users/{user_id}/recordings")
    return jsonify(recordings or {"error": "Failed to fetch recordings"}), 200 if recordings else 500


@zoom_blueprint.route("/recordings/<meeting_id>/delete", methods=["DELETE"])
def delete_recording(meeting_id):
    """Delete a specific cloud recording."""
    response = zoom_api_request("DELETE", f"meetings/{meeting_id}/recordings")
    return jsonify(response or {"error": "Failed to delete recording"}), 200 if response else 500


@zoom_blueprint.route("/webinars/create", methods=["POST"])
def create_webinar():
    """Create a Zoom webinar."""
    user_id = request.json.get("user_id")
    topic = request.json.get("topic", "New Webinar")
    start_time = request.json.get("start_time")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    webinar_data = {
        "topic": topic,
        "type": 5,  # Webinar type
        "start_time": start_time,
        "timezone": "UTC",
        "settings": {
            "panelists_video": True,
            "host_video": True,
            "practice_session": True,
            "hd_video": True
        }
    }

    webinar = zoom_api_request("POST", f"users/{user_id}/webinars", data=webinar_data)
    return jsonify(webinar or {"error": "Failed to create webinar"}), 200 if webinar else 500


@zoom_blueprint.route("/webinars/<webinar_id>", methods=["GET"])
def get_webinar_details(webinar_id):
    """Retrieve details of a specific webinar."""
    webinar = zoom_api_request("GET", f"webinars/{webinar_id}")
    return jsonify(webinar or {"error": "Failed to fetch webinar"}), 200 if webinar else 500


@zoom_blueprint.route("/chat/messages", methods=["POST"])
def send_chat_message():
    """Send a Zoom chat message."""
    to_jid = request.json.get("to_jid")
    message = request.json.get("message")

    if not to_jid or not message:
        return jsonify({"error": "Missing required parameters"}), 400

    chat_data = {
        "to_jid": to_jid,
        "message": message
    }

    response = zoom_api_request("POST", "chat/users/me/messages", data=chat_data)
    return jsonify(response or {"error": "Failed to send message"}), 200 if response else 500

