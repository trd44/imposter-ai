# Generic Utils Functions until a new home can be found

# region Imports
import json

# endregion


def SerializeJson(json_data):
    return json.dumps(json_data)


def DeserializeJson(serialized_json):
    return json.loads(serialized_json)
