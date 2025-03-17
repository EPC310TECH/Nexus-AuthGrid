import requests

from config import CONFIG
from src.database.db import store_token, get_token
from src.utils.logger import log_info, log_error


def get_access_token():
    """Fetch a new access token from Zoom OAuth."""
    try:
        url = "https://zoom.us/oauth/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": CONFIG["TOKENVAULT_CLIENT_ID"],
            "client_secret": CONFIG["TOKENVAULT_SECRET"],
        }
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            token = response.json().get("access_token")
            expires_in = response.json().get("expires_in", 3600)
            store_token("zoom", token, expires_in)
            log_info("New access token acquired")
            return token
        else:
            log_error(f"Failed to retrieve token: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        log_error(f"Error retrieving token: {str(e)}")
        return None


def refresh_token():
    """Refresh the token if expired."""
    token = get_token("zoom")
    if not token:
        return {"access_token": get_access_token(), "expires_in": 3600}
    return {"access_token": token}
