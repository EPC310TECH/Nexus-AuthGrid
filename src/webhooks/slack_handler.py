import json

from flask import Blueprint

slack_blueprint = Blueprint("slack", __name__)

# Load the slack_texts.json file
with open("src/webhooks/slack_texts.json", "r") as f:
    slack_texts = json.load(f)


# Define a function to handle the Slack command
def handle_slack_command(command, text):
    return handle_command(command, text)


# Define a function to generate the options for each command
def get_options(command):
    return slack_texts.get(command, [])


# Define a function to handle the Slack command
def handle_command(command: object, text: object) -> object:
    # Get the options for the command
    options = get_options(command)

    # If there are options, display them as a dropdown menu
    if options:
        # Create a dropdown menu with the options
        dropdown_menu = {
            "type": "select",
            "name": "option",
            "options": [{"text": option, "value": option} for option in options]
        }

        # Send the dropdown menu to the user
        return {"type": "interactive", "data": dropdown_menu}

    # If there are no options, handle the command as usual
    else:
        # Handle the command as usual
        return handle_command_without_options(command, text)


# Define a function to handle the command without options
def handle_command_without_options(command, text):
    # Handle the command as usual
    if command == "/zoom_alert":
        # Send a Zoom alert with the custom text
        return {"type": "message", "text": f"Zoom alert: {text}"}
    elif command == "/auth_issue":
        # Send an authentication issue alert with the custom text
        return {"type": "message", "text": f"Auth issue: {text}"}
    elif command == "/rate_limit_exceeded":
        # Send a rate limit exceeded alert with the custom text
        return {"type": "message", "text": f"Rate limit exceeded: {text}"}
    elif command == "/general_notification":
        # Send a general notification with the custom text
        return {"type": "message", "text": f"Notification: {text}"}
    elif command == "/custom_notification":
        # Send a custom notification with the custom text
        return {"type": "message", "text": f"Custom notification: {text}"}
    elif command == "/custom_alert":
        # Send a custom alert with the custom text
        return {"type": "message", "text": f"Alert: {text}"}
    else:
        # Send a general alert with the custom text
        return {"type": "message", "text": f"Alert: {text}"}
