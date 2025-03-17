import time

from src.notifications.slack_notifier import send_slack_alert
from src.utils.logger import log_error

RATE_LIMIT = 100  # Max requests per hour per user

def rate_limit_check(service, user):
    """Check if user exceeded rate limit."""
    try:
        now = time.time()
        one_hour_ago = now - 3600

        # Get count of API calls in the last hour
        api_calls = db.api_usage.count_documents({"service": service, "user": user, "timestamp": {"$gt": one_hour_ago}})

        if api_calls >= RATE_LIMIT:
            log_error(f"Rate limit exceeded for {user} on {service}")
            send_slack_alert(f"🚨 Rate Limit Exceeded: {user} exceeded {RATE_LIMIT} requests on {service}")
            return False
        return True
    except Exception as e:
        log_error(f"Rate limit check failed: {str(e)}")
        return False
