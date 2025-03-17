from flask import request, jsonify
from src.auth.security import verify_signature
from src.notifications.slack_notifier import send_slack_alert
from src.utils.logger import log_info, log_error

def zoom_webhook():
    """Handles incoming Zoom webhook events."""
    data = request.get_json()
    signature = request.headers.get("X-Zoom-Signature")
    timestamp = request.headers.get("X-Zoom-Request-Timestamp")

    if not verify_signature(str(data), signature, timestamp):
        log_error("Unauthorized webhook request")
        return "Unauthorized", 401

    event_type = data.get("event")

    if event_type == "meeting.started":
        log_info("Zoom Meeting Started")
        send_slack_alert(f"📢 Zoom Meeting Started: {data['payload']['object']['topic']}")
    elif event_type == "meeting.ended":
        log_info("Zoom Meeting Ended")
        send_slack_alert(f"🛑 Zoom Meeting Ended: {data['payload']['object']['topic']}")
    elif event_type == "recording.completed":
        log_info("Zoom Recording Completed")
        send_slack_alert(f"🎥 Recording completed for {data['payload']['object']['topic']}")

    return jsonify({"status": "received"}), 200
