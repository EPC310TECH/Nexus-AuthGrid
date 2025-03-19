import os
from dotenv import load_dotenv
from src.utils.logger import log_warning

load_dotenv()

CONFIG = {
    "TOKENVAULT_CLIENT_ID": os.getenv("TOKENVAULT_CLIENT_ID", "default_client_id"),
    "TOKENVAULT_SECRET": os.getenv("TOKENVAULT_SECRET", "default_secret"),
    "RATESHIELD_SECRET": os.getenv("RATESHIELD_SECRET", "default_ratelimit_secret"),
    "AUTHCORE_ACCOUNT_ID": os.getenv("AUTHCORE_ACCOUNT_ID", "default_authcore"),
    "AUTHRELAY_CLIENT_ID": os.getenv("AUTHRELAY_CLIENT_ID", "default_authrelay"),
    "SLACK_WEBHOOK_URL": os.getenv("SLACK_WEBHOOK_URL", ""),
    "DATABASE_URL": os.getenv("DATABASE_URL", "mongodb://localhost:27017/nexus_authgrid"),
}

# Log warnings for missing critical environment variables
for key, value in CONFIG.items():
    if "default" in value:
        log_warning(f"Environment variable for {key} is missing or using default value.")

class Config:
    DEBUG = os.getenv("DEBUG", "True") == "True"
    PORT = int(os.getenv("PORT", 5000))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

config = Config()
