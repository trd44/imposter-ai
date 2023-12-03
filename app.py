"""
app.py

Author: Christian Welling, Tim Duggan
Date: 12/3/2023
Company: ImposterAI
Contact: csw73@cornell.edu

This is a Python program using Flask framework to launch the backend server
for ImposterAI application.
"""

# region General/API Imports
import os
from flask import Flask, request, send_from_directory, g
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from typing import List, Dict

# endregion

# region Backend Imports
from backend import db
from backend import auth
from backend.config import Config
import backend.callbacks as cb
from backend.chat_manager import ChatManager
from backend.GPTModel import GPTModel
from backend.auth import login_required
from backend.database_manager import DatabaseManager as dbm
from backend.utils import SerializeJson

# endregion

# region Application Start
app = Flask(__name__, static_folder="frontend/build", static_url_path="")
api = Api(app)
app.config.from_object(Config)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Load the API Key
cb.load_openai_api_key()
# endregion


@app.route("/", defaults={"path": ""})
def serve(path: str):
    """
    Serve the static files in the build directory.

    Args:
        path (str): path to static file

    Returns:
        flask.wrappers.Response: A Flask Response object with the contents of
        the 'index.html'.
    """
    print(path)
    return send_from_directory(app.static_folder, "index.html")


@app.route("/favicon.ico")
def favicon():
    """
    Handle favicon requests.

    Returns:
        The requested 'favicon.ico' file.
    """
    return send_from_directory(os.path.join(app.root_path, "build"), "favicon.ico")


# Initialize the database and register the auth blueprint
db.init_app(app)
app.register_blueprint(auth.bp)


# region AssetsHandling
@app.route("/backend_assets/<path:path>")
def backend_assets(path: str):
    """
    Provide link to backend hosted asset given path.

    Args:
        path (str): path to asset

    Returns:
        str: Full URL to the asset on the backend.
    """
    return send_from_directory("backend/static/assets", path)


# endregion


# region ContactRetrieval
@app.route("/backend/fetch_contacts", methods=["GET"])
@login_required
def fetch_contacts() -> str:
    """
    Retrieve contact information from personality table.

    Returns:
        str: A JSON formatted string representing list of contacts,
        each with their id, nickname, img, and last_message.
    """
    print("fetch_contacts, fetching contacts")
    # [1] Retrieve personality list from database
    # TODO: handle case where fetching all personalities returns none
    personality_list = dbm.GetAllPersonalities()

    # [2] Convert list of tuples into dictionaries identified by personality_id
    # {
    #   id:
    #   {
    #       id:,
    #       nickname:,
    #       img:,
    #       last_message:
    #   },
    #   ...
    # }
    personality_dict = {
        tpl[0]: dict(zip(["id", "nickname", "img", "last_message"], tpl))
        for tpl in personality_list
    }

    # [3] Retrieve chat list
    user_id = g.user["id"]
    chat_list = dbm.GetChatList(user_id)

    # [4] Update any last message given personalities with existing
    # conversations
    for personality_id, _ in chat_list:
        last_message = get_last_message(user_id, personality_id)
        if last_message is None:
            print(f"Database Error. Conversation for [{personality_id}] not found!")
        else:
            personality_dict[personality_id]["last_message"] = last_message

    # [5] Convert to list of dictionaries in JSON format
    personality_list_dict_format = list(personality_dict.values())
    personality_list_json_format = SerializeJson(personality_list_dict_format)
    return personality_list_json_format


def get_last_message(user_id: int, personality_id: int) -> str:
    """
    Retrieves the last message given user_id and personality_id. If
    conversation does not exist, will return None.

    Args:
        user_id (int): User identifier.
        personality_id (int): Personality identifier.

    Returns:
        str: The content of the last message, or None if no message exists.
    """
    try:
        last_message = None
        message_log = dbm.GetChatFromID(user_id, personality_id)

        # Return the last message (content key in dict) from log
        if (
            message_log
            and isinstance(message_log, list)
            and "content" in message_log[-1]
        ):
            last_message = message_log[-1]["content"]
        return last_message
    except Exception as e:
        print(
            "An error occurred while retrieving the last message for user_id"
            + f"{user_id} and personality_id {personality_id}: {str(e)}"
        )
        return None


# endregion


# region ChatMessaging
@app.route("/api/send_user_message", methods=["POST"])
@login_required
def send_user_message() -> Dict:
    """
    API endpoint to handle sending user messages.

    Returns:
        JSON response containing response to user message or error message.
    """
    # TODO: Error handling of payload content
    # [1] Get the user's input
    data = request.json

    # [2] Startup chat manager
    chat_manager = ChatManager(g.user["id"], None, GPTModel())

    # [3] Send message to provided personality
    response = chat_manager.SendMessage(data["activeContactId"], data["newMessage"])

    # [4] Return ChatGPT's response
    return response


@app.route("/api/fetch_chat_history", methods=["POST"])
@login_required
def fetch_chat_history() -> List:
    """
    API endpoint to fetch chat history.

    Returns:
        list: A list of dictionaries representing each message in the conversation.
              Each dictionary has the following structure:
                {
                    'role': <Role of the sender, can be one of 'user', 'assistant',
                            or 'system'>,
                    'content': <Content of the message>
                }

              The messages are ordered as they appeared in the conversation.
              First, any system prompts appear, followed by user and assistant
              messages in their chronological order.
    """
    # [1] Get user's input
    print("fetch_chat_history, retreiving data from json")
    data = request.json

    # [2] Startup chat manager
    print("fetch_chat_history, setting up chat manager")
    chat_manager = ChatManager(g.user["id"], None, GPTModel())

    # [3] Retreive conversation given ID
    print(f"fetch_chat_history, personality_id: {data['id']}, type: {type(data['id'])}")
    conversation = chat_manager.RetrieveConversation(data["id"])

    # [4] Export conversation history
    message_history = conversation.ExportSavedMessages()
    return message_history


# endregion


@app.errorhandler(404)
def not_found(e: HTTPException) -> Flask.response_class:
    """
    Handle 404 errors by sending the index.html static file.

    Args:
        e (HTTPException): The exception instance with status code 404.

    Returns:
        response_class: A Flask response object that sends the static "index.html"
        file back to the client.
    """
    return app.send_static_file("index.html")


# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
