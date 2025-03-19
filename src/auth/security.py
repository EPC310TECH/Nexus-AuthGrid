import hmac
import hashlib
import time
from config import CONFIG
from src.utils.logger import log_info, log_error


def verify_signature(payload, received_signature, timestamp):
    """Verifies webhook payload integrity using HMAC-SHA256."""
    try:
        # Prevent replay attacks (reject requests older than 5 minutes)
        if abs(time.time() - int(timestamp)) > 300:
            log_error("Timestamp too old, possible replay attack")
            return False

        computed_signature = hmac.new(
            CONFIG["RATESHIELD_SECRET"].encode(),
            f"{timestamp}{payload}".encode(),
            hashlib.sha256
        ).hexdigest()

        # Log computed and received signatures for debugging
        log_info(f"Computed signature: {computed_signature}")
        log_info(f"Received signature: {received_signature}")

        is_valid = hmac.compare_digest(computed_signature, received_signature)
        if is_valid:
            log_info("Signature verified successfully")
        else:
            log_error("Invalid signature")
        return is_valid
    except Exception as e:
        log_error(f"Error verifying signature: {str(e)}")
        return False
