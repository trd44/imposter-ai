import os
import openai
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from api.HelloApiHandler import HelloApiHandler

import datetime

x = datetime.datetime.now()

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)
api = Api(app)

def load_openai_api_key():
    try:
        with open("API_KEY") as f:
            file_contents = f.read()
        os.environ["OPENAI_API_KEY"] = file_contents
    except:
        pass

# Load the API Key
load_openai_api_key()

saved_messages = [{"role": "system", "content": "respond to me as if you were a helpful travel agent helping me plan a trip."}]

@app.route('/', defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(HelloApiHandler, '/flask/hello')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'build'), 'favicon.ico')

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def serve(path):
#     if path != "" and os.path.exists(app.static_folder + '/' + path):
#         return send_from_directory(app.static_folder, path)
#     else:
#         return send_from_directory(app.static_folder, 'index.html')

@app.route("/api/send_user_message", methods=['POST'])
def send_user_message():
    # Get the user's input
    data = request.json
    saved_messages.append({"role": "user", "content": data['newQuestion']})

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

@app.route("/data")
def get_time():
    return{
        'Name':"Tim",
        'Age':"29",
        'Date':x,
        "Programming":"Python"
    }

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)
    app.run(debug=True)
