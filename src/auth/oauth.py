import os
import requests
import time
import logging
from flask import Blueprint, request, jsonify
from cryptography.fernet import Fernet

auth_blueprint = Blueprint("auth", __name__)

# Load credentials from environment variables
CLIENT_ID = os.getenv("AuthCore_Client_ID")
CLIENT_SECRET = os.getenv("TokenVault_Secret_Token")
TOKEN_URL = "https://zoom.us/oauth/token"
REDIRECT_URI = os.getenv("AuthCore_Redirect_URI")
TOKEN_STORAGE = {}  # Temporary dictionary for storing tokens (replace with DB in production)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load encryption key from environment variable
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY environment variable is not set")

cipher_suite = Fernet(ENCRYPTION_KEY)


def save_token(token_data):
    """Save token securely (Replace with DB in production)."""
    try:
        encrypted_access_token = cipher_suite.encrypt(token_data["access_token"].encode())
        encrypted_refresh_token = cipher_suite.encrypt(token_data["refresh_token"].encode())
        TOKEN_STORAGE["access_token"] = encrypted_access_token
        TOKEN_STORAGE["refresh_token"] = encrypted_refresh_token
        TOKEN_STORAGE["expires_at"] = time.time() + token_data["expires_in"]
        logger.info("🔐 Tokens saved successfully.")
    except Exception as e:
        logger.error("❌ Error saving tokens: %s", str(e))


def get_stored_token():
    """Retrieve stored OAuth token, refreshing if expired."""
    try:
        if "access_token" in TOKEN_STORAGE and time.time() < TOKEN_STORAGE["expires_at"]:
            decrypted_access_token = cipher_suite.decrypt(TOKEN_STORAGE["access_token"]).decode()
            return decrypted_access_token
        else:
            return refresh_token()
    except Exception as e:
        logger.error("❌ Error retrieving stored token: %s", str(e))
        return None


def refresh_token():
    """Refresh OAuth token using the stored refresh token."""
    try:
        if "refresh_token" not in TOKEN_STORAGE:
            logger.error("❌ No refresh token available.")
            return None

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": cipher_suite.decrypt(TOKEN_STORAGE["refresh_token"]).decode()
        }

        response = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)

        if response.status_code == 200:
            token_data = response.json()
            save_token(token_data)
            return token_data["access_token"]
        else:
            logger.error("❌ Failed to refresh token: %s", response.json())
            return None
    except Exception as e:
        logger.error("❌ Error refreshing token: %s", str(e))
        return None


@auth_blueprint.route("/token", methods=["POST"])
def get_token():
    """Exchange OAuth code for access token."""
    try:
        code = request.json.get("code")
        if not code:
            return jsonify({"error": "Missing authorization code"}), 400

        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        }

        response = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)

        if response.status_code == 200:
            token_data = response.json()
            save_token(token_data)
            return jsonify(token_data), 200
        else:
            logger.error("❌ Failed to get token: %s", response.json())
            return jsonify({"error": "Failed to get token", "details": response.json()}), response.status_code
    except Exception as e:
        logger.error("❌ Error in get_token endpoint: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@auth_blueprint.route("/validate", methods=["GET"])
def validate_token():
    """Validate stored OAuth token."""
    try:
        access_token = get_stored_token()
        if access_token:
            return jsonify({"access_token": access_token, "status": "Valid"}), 200
        else:
            return jsonify({"error": "No valid token available"}), 401
    except Exception as e:
        logger.error("❌ Error in validate_token endpoint: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@auth_blueprint.route("/refresh", methods=["POST"])
def refresh_access_token():
    """Manually trigger token refresh."""
    try:
        new_token = refresh_token()
        if new_token:
            return jsonify({"access_token": new_token, "status": "Refreshed"}), 200
        else:
            return jsonify({"error": "Failed to refresh token"}), 500
    except Exception as e:
        logger.error("❌ Error in refresh_access_token endpoint: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500

