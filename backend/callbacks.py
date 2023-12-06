"""
callbacks.py

Author: Tim Duggan
Date: 12/3/2023
Company: ImposterAI
Contact: csw73@cornell.edu

Contains callback functions.
"""

# region General/API Imports
import os

# endregion

# region Backend Imports
from backend.logger import LOGGER

# endregion


def load_openai_api_key() -> None:
    """
    Load OpenAI API key from a file and set it to the environment variable.

    This function reads the 'API_KEY' file in the current directory and
    puts its contents (expected to be the API Key) into an environment variable named
    'OPENAI_API_KEY'.
    """

    try:
        # Open the file named "API_KEY" and read its contents
        with open("API_KEY") as f:
            file_contents = f.read()

        # Set the content of the file as the value of the environment variable "OPENAI_API_KEY"
        os.environ["OPENAI_API_KEY"] = file_contents

    # Handle exceptions if something goes wrong while opening the file or reading from it
    except Exception as e:
        # Print error message with the details of the exception
        LOGGER.error(f"error: cannot read api key! {str(e)}")
