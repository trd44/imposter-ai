# Import the app instance
# from app import app

# Import any other required modules or data for your callbacks
# import pandas as pd
import openai
import os
import sys

saved_messages = []

def register_callbacks(app):

    @app.callback(
            Output("chat-window-output", "children", allow_duplicate=True),
            Input('system-input-button', 'n_clicks'),
            State("system-input", "value"),
            prevent_initial_call=True
        )
    def send_sys_message(n_clicks, system_input):
        if n_clicks and n_clicks > 0:
            if system_input:
                save_message({"role": "system", "content": system_input})
                chat_gpt_response = send_message_to_chat_gpt()
                return chat_gpt_response['message']
        else:
            resp = ""
            return resp

    @app.callback(
            Output("chat-window-output", "children"),
            Input('user-input-button', 'n_clicks'),
            State("user-input", "value"),
            prevent_initial_call=True
        )
    def send_user_message(n_clicks, user_input):
        global current_prompt
        if n_clicks and n_clicks > 0:
            if user_input:
                save_message({"role": "user", "content": user_input})
                chat_gpt_response = send_message_to_chat_gpt()
                return chat_gpt_response["message"]
        else:
            resp = current_prompt
            return resp

    def save_message(msg):
        saved_messages.append(msg)

    def send_message_to_chat_gpt():
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=saved_messages
            )
            chat_gpt_response = response.choices[0].message.content
            save_message({"role": "assistant", "content": chat_gpt_response})
            # print(saved_messages)
            return {'status': 'success', 'message': chat_gpt_response}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}
