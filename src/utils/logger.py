import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def log_zoom_api_request(method, endpoint, data=None, params=None):
    """Log a Zoom API request."""
    message = f"{method} {endpoint}"
    if data:
        message += f" with data: {data}"
    if params:
        message += f" and params: {params}"
    logging.info(message)


def log_zoom_api_response(response):
    """Log a Zoom API response."""
    message = f"Received Zoom API response: {response.status_code}"
    if response.text:
        message += f" with content: {response.text}"
    logging.info(message)


def log_info(message):
    logging.info(message)


def log_error(message):
    logging.error(message)
