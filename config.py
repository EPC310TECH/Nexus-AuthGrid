import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "TOKENVAULT_CLIENT_ID": os.getenv("TokenVault_Client_ID", "default_client_id"),
    "TOKENVAULT_SECRET": os.getenv("TokenVault_Secret_Token", "default_secret"),
    "RATESHIELD_SECRET": os.getenv("RateShield_Client_Secret", "default_ratelimit_secret"),
    "AUTHCORE_ACCOUNT_ID": os.getenv("AuthCore_Account_ID", "default_authcore"),
    "AUTHRELAY_CLIENT_ID": os.getenv("AuthRelay_Client_ID", "default_authrelay"),
    "SLACK_WEBHOOK_URL": os.getenv("SLACK_WEBHOOK_URL", ""),
    "DATABASE_URL": os.getenv("DATABASE_URL", "mongodb://localhost:27017/nexus_authgrid"),
}
