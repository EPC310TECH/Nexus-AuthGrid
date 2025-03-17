import os
import requests
import time
from flask import Blueprint, request, jsonify

auth_blueprint = Blueprint("auth", __name__)

# Load credentials from environment variables
CLIENT_ID = os.getenv("AuthCore_Client_ID")
CLIENT_SECRET = os.getenv("TokenVault_Secret_Token")
TOKEN_URL = "https://zoom.us/oauth/token"
REDIRECT_URI = os.getenv("AuthCore_Redirect_URI")
TOKEN_STORAGE = {}  # Temporary dictionary for storing tokens (replace with DB in production)


def save_token(token_data):
    """Save token securely (Replace with DB in production)."""
    TOKEN_STORAGE["access_token"] = token_data["access_token"]
    TOKEN_STORAGE["refresh_token"] = token_data["refresh_token"]
    TOKEN_STORAGE["expires_at"] = time.time() + token_data["expires_in"]
    print("🔐 Tokens saved successfully.")


def get_stored_token():
    """Retrieve stored OAuth token, refreshing if expired."""
    if "access_token" in TOKEN_STORAGE and time.time() < TOKEN_STORAGE["expires_at"]:
        return TOKEN_STORAGE["access_token"]
    else:
        return refresh_token()


def refresh_token():
    """Refresh OAuth token using the stored refresh token."""
    if "refresh_token" not in TOKEN_STORAGE:
        return None

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": TOKEN_STORAGE["refresh_token"]
    }

    response = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)

    if response.status_code == 200:
        token_data = response.json()
        save_token(token_data)
        return token_data["access_token"]
    else:
        print("❌ Failed to refresh token:", response.json())
        return None


@auth_blueprint.route("/token", methods=["POST"])
def get_token():
    """Exchange OAuth code for access token."""
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
        return jsonify({"error": "Failed to get token", "details": response.json()}), response.status_code


@auth_blueprint.route("/validate", methods=["GET"])
def validate_token():
    """Validate stored OAuth token."""
    access_token = get_stored_token()
    if access_token:
        return jsonify({"access_token": access_token, "status": "Valid"}), 200
    else:
        return jsonify({"error": "No valid token available"}), 401


@auth_blueprint.route("/refresh", methods=["POST"])
def refresh_access_token():
    """Manually trigger token refresh."""
    new_token = refresh_token()
    if new_token:
        return jsonify({"access_token": new_token, "status": "Refreshed"}), 200
    else:
        return jsonify({"error": "Failed to refresh token"}), 500
