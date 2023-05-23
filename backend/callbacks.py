import os

def load_openai_api_key():
    try:
        with open("API_KEY") as f:
            file_contents = f.read()
        os.environ["OPENAI_API_KEY"] = file_contents
    except:
        pass