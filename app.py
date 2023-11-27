#region General/API Imports
import os
from flask import Flask, request, send_from_directory, g
from flask_restful import Api
#endregion

#region Backend Imports
from backend import db
from backend import auth
from backend.config import Config
import backend.callbacks as cb
from backend.ChatManager import ChatManager
from backend.GPTModel import GPTModel
from backend.auth import login_required
from backend.DatabaseManager import DatabaseManager as dbm
from backend.Utils import SerializeJson
#endregion

#region Application Start
app = Flask(__name__, static_folder='frontend/build', static_url_path='')
api = Api(app)
app.config.from_object(Config)

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
db.init_app(app)
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
    print("fetch_contacts, fetching contacts")
    # TODO: unless personality table does not exist, should handle case where db request returns None

    # [1] Retrieve personality list from database
    personality_list = dbm.GetAllPersonalities()

    # [2] Convert list of tuples into dictionaries identified by personality_id
    # {id: {id:,nickname:,img:,last_message:,},...}
    #personality_list_dict_format = [dict(zip(['id', 'nickname', 'img', 'last_message'], tpl)) for tpl in personality_list]
    personality_dict = {tpl[0]: dict(zip(['id', 'nickname', 'img', 'last_message'], tpl)) for tpl in personality_list}

    # [3] Retrieve Chat List
    user_id = g.user['id']
    chat_list = dbm.GetChatList(user_id)
    
    # [4] Update any last message given personalities with existing conversations
    for personality_id, _ in chat_list:
        last_message = get_last_message(user_id, personality_id)
        if last_message is None:
            print(f"Database Error. Conversation for [{personality_id}] not found!")
        else:
            personality_dict[personality_id]['last_message'] = last_message

    # [X] Convert to list of dictionaries in JSON format
    personality_list_dict_format = list(personality_dict.values())
    personality_list_json_format = SerializeJson(personality_list_dict_format)

    return personality_list_json_format

def get_last_message(user_id: int, personality_id: int) -> str:
    """
    Retrieves the last message given user_id and personality_id. If
    conversation does not exist, will return None
    """
    last_message = None
    message_log = dbm.GetChatFromID(user_id, personality_id)

    # return the last message (content key in dict) from log
    if message_log:
        last_message = message_log[-1]["content"]
    return last_message

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