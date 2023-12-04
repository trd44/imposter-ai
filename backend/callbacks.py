"""
callbacks.py

Author: Tim Duggan
Date: 12/3/2023
Company: ImposterAI
Contact: csw73@cornell.edu

Contains callback functions.
"""

# region General/API imports
import os

# endregion


def load_openai_api_key():
    try:
        with open("API_KEY") as f:
            file_contents = f.read()
        os.environ["OPENAI_API_KEY"] = file_contents
    except Exception as e:
        print(f"error: cannot read api key! {str(e)}")
