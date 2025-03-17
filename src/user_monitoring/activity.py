import time
import logging
import json
import requests
from flask import request, jsonify
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Activity Storage (Simulated DB)
user_activity_log = {}

# Webhook URL for external notifications (e.g., Slack, Discord, etc.)
WEBHOOK_URL = "https://your-webhook-url.com"

# Suspicious activity settings
SUSPICIOUS_ACTIVITY_THRESHOLD = 5  # Too many requests in a short time

# Helper Functions
def log_activity(user_id, event, details=None):
    """Log user activity with timestamp and metadata."""
    timestamp = datetime.now(datetime.timezone.utc).isoformat()
    ip_address = request.remote_addr
    user_agent = request.headers.get("User-Agent", "Unknown")

    entry = {
        "timestamp": timestamp,
        "event": event,
        "ip": ip_address,
        "user_agent": user_agent,
        "details": details or {},
    }

    if user_id not in user_activity_log:
        user_activity_log[user_id] = []

    user_activity_log[user_id].append(entry)
    logger.info(f"Activity Logged: {user_id} -> {event}")

    check_suspicious_activity(user_id)

    return entry


def check_suspicious_activity(user_id):
    """Detects rapid consecutive requests from the same user."""
    activities = user_activity_log.get(user_id, [])
    if len(activities) < SUSPICIOUS_ACTIVITY_THRESHOLD:
        return

    recent_activities = activities[-SUSPICIOUS_ACTIVITY_THRESHOLD:]
    time_diffs = [(datetime.fromisoformat(a["timestamp"]) - datetime.fromisoformat(b["timestamp"])).total_seconds()
                  for a, b in zip(recent_activities[1:], recent_activities[:-1])]

    avg_time_diff = sum(time_diffs) / len(time_diffs) if time_diffs else float("inf")

    if avg_time_diff < 2:  # Too many requests too quickly
        logger.warning(f"🚨 Suspicious Activity Detected for {user_id} 🚨")
        send_alert(user_id, recent_activities)


def send_alert(user_id, activity_log):
    """Sends an alert when suspicious activity is detected."""
    alert_message = {
        "text": f"⚠️ **Suspicious Activity Detected** for User: {user_id}",
        "activity_log": activity_log
    }

    try:
        requests.post(WEBHOOK_URL, json=alert_message, timeout=5)
        logger.info("🚀 Suspicious activity alert sent successfully!")
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to send alert: {e}")


# Flask Route Decorator for Activity Monitoring
def monitor_activity(event_name):
    """Decorator to track user activity in API routes."""
    def decorator(f):
        def wrapper(*args, **kwargs):
            user_id = request.headers.get("X-User-ID", "guest")  # Defaults to 'guest' if no user ID provided
            log_activity(user_id, event_name)
            return f(*args, **kwargs)

        wrapper.__name__ = f.__name__
        return wrapper
    return decorator


def activity_blueprint():
    return None