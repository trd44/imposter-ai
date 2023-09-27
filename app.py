
#region General/API Imports
import os
import datetime
from flask import Flask, request, send_from_directory, g
from flask_restful import Api
from flask_cors import CORS
import openai
#endregion

#region Backend Imports
import backend.callbacks as cb
from backend.HelloApiHandler import HelloApiHandler
from backend.ChatManager import ChatManager
from backend.GPTModel import GPTModel
from backend.auth import login_required
from backend.DatabaseManager import DatabaseManager as dbm
from backend.Utils import SerializeJson
#endregion

#region Data Imports
from Presets.PresetData import TEST_PERSONALITY_ID 
#endregion

#region Application Start

# Initialize Flask app and CORS, set up API and secret key
app = Flask(__name__, static_folder='frontend/build', static_url_path='')
# CORS(app)
api = Api(app)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'imposter.sqlite'),
)


# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Load the API Key
cb.load_openai_api_key()

#endregion

# Serve the static files in the build directory
@app.route('/', defaults={'path': ''})
def serve(path):
    print(path)
    return send_from_directory(app.static_folder,'index.html')

# Handle favicon requests
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'build'), 'favicon.ico')

# Initialize the database and register the auth blueprint
from backend import db
db.init_app(app)
from backend import auth
app.register_blueprint(auth.bp)

#region AssetsHandling
@app.route('/backend_assets/<path:path>')
def backend_assets(path):
    return send_from_directory('backend/static/assets', path)
#endregion

#region
@app.route('/backend/fetch_contacts', methods=['GET'])
@login_required
def fetch_contacts():
    # TODO: unless personality table does not exist, should handle case where db request returns None

    # [1] Retrieve personality list from database
    personality_list = dbm.GetAllPersonalities()

    # [2] Convert list of tuples into list of dictionaries
    personality_list_dict_format = [dict(zip(['id', 'nickname', 'img'], tpl)) for tpl in personality_list]

    # [3] Convert list of dictionaries into JSON format
    personality_list_json_format = SerializeJson(personality_list_dict_format)

    return personality_list_json_format
#endregion


#region ChatMessaging

# API endpoint to handle sending user messages
# TODO: update request.json to contain the personality ID as well [COMPLETED]
@app.route("/api/send_user_message", methods=['POST'])
@login_required
def send_user_message():
    # Get the user's input
    data = request.json

    # Startup chat manager
    chat_manager = ChatManager(g.user['id'], None, GPTModel())

    # Send message to provided personality
    response = chat_manager.SendMessage(data['activeContactId'], data['newMessage'])

    # Return ChatGPT's response
    return response

# API endpoint to fetch chat history
# TODO: request should specify what personality to request history from [COMPLETED]
@app.route("/api/fetch_chat_history", methods=['POST'])
@login_required
def fetch_chat_history():
    # Get user's input
    print("fetch_chat_history, retreiving data from json")
    data = request.json

    # Startup chat manager
    print("fetch_chat_history, setting up chat manager")
    chat_manager = ChatManager(g.user['id'], None, GPTModel())

    # Retreive conversation given ID
    print(f"fetch_chat_history, personality_id: {data['id']}, type: {type(data['id'])}")
    conversation = chat_manager.RetrieveConversation(data['id'])

    # Export conversation history
    message_history = conversation.ExportSavedMessages()

    return message_history

#endregion

# Handle 404 errors by sending the index.html static file
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


# Main entry point
if __name__ == "__main__":
    app.run(debug=True)