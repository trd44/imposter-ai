
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
from backend.DatabaseManager import DatabaseManager
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

#region ChatMessaging

# API endpoint to handle sending user messages
@app.route("/api/send_user_message", methods=['POST'])
@login_required
def send_user_message():
    # Get the user's input
    data = request.json

    # Startup chat manager
    chat_manager = ChatManager(g.user['id'], None, GPTModel())

    # Send message
    # TODO: update for being able to select personality
    response = chat_manager.SendMessage(TEST_PERSONALITY_ID, data['newMessage'])

    # Return ChatGPT's response
    return response

# API endpoint to fetch chat history
@app.route("/api/fetch_chat_history", methods=['GET'])
@login_required
def fetch_chat_history():
    # Startup chat manager
    chat_manager = ChatManager(g.user['id'], None, GPTModel())
    conversation = chat_manager.RetrieveConversation(TEST_PERSONALITY_ID)

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