import time
import logging
import threading
from flask import request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default Rate Limits (requests per minute)
DEFAULT_LIMITS = {
    "global": (100, 60),  # 100 requests per minute globally
    "per_ip": (50, 60),  # 50 requests per minute per IP
    "per_user": (30, 60)  # 30 requests per minute per user
}

# Rate limit storage (Token Bucket Implementation)
rate_limit_data = {
    "global": {"tokens": DEFAULT_LIMITS["global"][0], "last_refill": time.time()},
    "per_ip": {},
    "per_user": {}
}

lock = threading.Lock()


def refill_tokens(limit_key, limit):
    """Refill tokens based on elapsed time."""
    now = time.time()
    with lock:
        last_refill = rate_limit_data[limit_key].get("last_refill", now)
        elapsed = now - last_refill
        new_tokens = (elapsed / limit[1]) * limit[0]

        rate_limit_data[limit_key]["tokens"] = min(limit[0], rate_limit_data[limit_key]["tokens"] + new_tokens)
        rate_limit_data[limit_key]["last_refill"] = now


def is_rate_limited(limit_key, limit):
    """Check if the request is rate-limited."""
    refill_tokens(limit_key, limit)

    if rate_limit_data[limit_key]["tokens"] >= 1:
        rate_limit_data[limit_key]["tokens"] -= 1
        return False  # Not rate limited
    return True  # Rate limited


def enforce_rate_limit():
    """Main rate limiter function for Flask routes."""
    ip = request.remote_addr
    user_id = request.headers.get("X-User-ID", ip)  # Defaults to IP if no user ID

    # Global Rate Limit
    if is_rate_limited("global", DEFAULT_LIMITS["global"]):
        logger.warning(f"Global rate limit exceeded. IP: {ip}")
        return jsonify({"error": "Global rate limit exceeded. Try again later."}), 429

    # Per-IP Rate Limit
    if ip not in rate_limit_data["per_ip"]:
        rate_limit_data["per_ip"][ip] = {"tokens": DEFAULT_LIMITS["per_ip"][0], "last_refill": time.time()}

    if is_rate_limited(ip, DEFAULT_LIMITS["per_ip"]):
        logger.warning(f"IP rate limit exceeded for {ip}.")
        return jsonify({"error": "IP rate limit exceeded. Try again later."}), 429

    # Per-User Rate Limit
    if user_id not in rate_limit_data["per_user"]:
        rate_limit_data["per_user"][user_id] = {"tokens": DEFAULT_LIMITS["per_user"][0], "last_refill": time.time()}

    if is_rate_limited(user_id, DEFAULT_LIMITS["per_user"]):
        logger.warning(f"User rate limit exceeded for {user_id}.")
        return jsonify({"error": "User rate limit exceeded. Try again later."}), 429

    return None  # No rate limit exceeded


def rate_limiter(f):
    """Flask decorator to enforce rate limits on routes."""
    def wrapper(*args, **kwargs):
        limit_response = enforce_rate_limit()
        if limit_response:
            return limit_response
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


def rate_limiter_blueprint():
    return None