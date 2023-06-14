
#region General/API Imports
import os
import datetime
import openai
from flask import Flask, request, jsonify, send_from_directory, render_template, g
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
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

#region Global Variables
x = datetime.datetime.now()
#endregion

#region Application Start
app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)
api = Api(app)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'imposter.sqlite'),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Load the API Key
# TODO: How to handle API Key?
cb.load_openai_api_key()
#endregion


# TODO: Clean this up...
@app.route('/', defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(HelloApiHandler, '/flask/hello')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'build'), 'favicon.ico')

from backend import db
db.init_app(app)

from backend import auth
app.register_blueprint(auth.bp)

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def serve(path):
#     if path != "" and os.path.exists(app.static_folder + '/' + path):
#         return send_from_directory(app.static_folder, path)
#     else:
#         return send_from_directory(app.static_folder, 'index.html')

saved_messages = [{"role": "system", "content": "respond to me as if you were a helpful travel agent helping me plan a trip."}]

#region ChatMessaging
#TODO: Add login as required...
@app.route("/api/send_user_message", methods=['POST'])
@login_required
def send_user_message():
    # Get the user's input
    data = request.json

    '''
    saved_messages.append({"role": "user", "content": data['newMessage']})
    # Send the user's input to the ChatGPT API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=saved_messages
    )
    print(completion.choices[0].message)
    saved_messages.append({"role": "assistant", "content": completion.choices[0].message.content})
    # Return the ChatGPT's response
    return completion.choices[0].message
    '''
    # Startup chat manager
    chat_manager = ChatManager(g.user['id'], None, GPTModel())

    # Send message
    # TODO: update for being able to select personality
    response = chat_manager.SendMessage(TEST_PERSONALITY_ID, data['newMessage'])
    print("Sent Message")

    print(response.content)

    # Return the ChatGPT's response
    return response

#TODO: Add login as required...
@app.route("/api/old/send_user_message", methods=['POST'])
def old_send_user_message():
    # Get the user's input
    data = request.json

    saved_messages.append({"role": "user", "content": data['newMessage']})
    # Send the user's input to the ChatGPT API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=saved_messages
    )
    print(completion.choices[0].message)
    saved_messages.append({"role": "assistant", "content": completion.choices[0].message.content})
    # Return the ChatGPT's response
    return completion.choices[0].message

@app.route('/api/some_function', methods=['POST'])
def some_function():
    data = request.json
    # Process the data and perform the desired function
    result = {'result': 'Hello, ' + data['name']}
    return jsonify(result)

#endregion

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)
    app.run(debug=True)
