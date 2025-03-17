import requests
from config import CONFIG
from src.utils.logger import log_info, log_error

def send_slack_alert(message):
    """Send an alert message to Slack webhook."""
    try:
        if not CONFIG["SLACK_WEBHOOK_URL"]:
            log_error("Slack webhook URL not configured")
            return

        payload = {"text": message}
        response = requests.post(CONFIG["SLACK_WEBHOOK_URL"], json=payload)

        if response.status_code == 200:
            log_info(f"Sent Slack alert: {message}")
        else:
            log_error(f"Failed to send Slack alert: {response.text}")
    except Exception as e:
        log_error(f"Error sending Slack alert: {str(e)}")
