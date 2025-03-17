from pymongo import MongoClient
from config import CONFIG
from src.utils.logger import log_info, log_error
import time

# Initialize MongoDB connection
client = MongoClient(CONFIG["DATABASE_URL"])
db = client["nexus_authgrid"]

def store_token(service, token, expires_in):
    """Store OAuth tokens in the database with expiration time."""
    try:
        expiry_time = time.time() + expires_in
        db.tokens.update_one(
            {"service": service},
            {"$set": {"token": token, "expiry_time": expiry_time}},
            upsert=True,
        )
        log_info(f"Stored new token for {service}")
    except Exception as e:
        log_error(f"Error storing token: {str(e)}")

def get_token(service):
    """Retrieve token if not expired."""
    try:
        record = db.tokens.find_one({"service": service})
        if record and time.time() < record["expiry_time"]:
            return record["token"]
        return None
    except Exception as e:
        log_error(f"Error retrieving token: {str(e)}")
        return None

def log_webhook_event(event_type, payload):
    """Log webhook events for debugging and audit purposes."""
    try:
        db.webhooks.insert_one({"event": event_type, "payload": payload, "timestamp": time.time()})
        log_info(f"Webhook event logged: {event_type}")
    except Exception as e:
        log_error(f"Error logging webhook event: {str(e)}")

def track_api_usage(service, user):
    """Track API requests for rate limiting."""
    try:
        db.api_usage.insert_one({"service": service, "user": user, "timestamp": time.time()})
    except Exception as e:
        log_error(f"Error tracking API usage: {str(e)}")
