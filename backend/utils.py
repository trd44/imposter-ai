"""
utils.py

Author: Christian Welling
Date: 12/3/2023
Company: ImposterAI
Contact: csw73@cornell.edu

Utility functions.
"""

# region Imports
import json
from typing import Any

# endregion


def serialize_json(json_data: Any) -> str:
    """
    Serializes Python data structure into a JSON formatted string.

    Arguments:
        json_data (Any):
            The data to be serialized.
            Typically, it would be a dictionary or a list.

    Returns:
        str: Returns JSON formatted string.
    """
    # Convert Python object to JSON string
    return json.dumps(json_data)


def deserialize_json(serialized_json) -> Any:
    """
    Deserializes a JSON formatted string into a Python data structure.

    Arguments:
        serialized_json (str): The JSON string to be deserialized.

    Returns:
        Any: Returns a deserialized data, typically as a dictionary or a list.
    """
    # Convert JSON string to Python object
    return json.loads(serialized_json)
