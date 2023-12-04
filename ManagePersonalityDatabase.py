"""
ManagePersonalityDatabas.py

Author: Tim Duggan
Date: 12/3/2023
Company: ImposterAI
Contact: csw73@cornell.edu

This is a Python scripting tool for updating and modifying the personality table
in the ImposerAI database.
"""
# region General/API Imports
import argparse
import json
import sqlite3

# endregion

# region Backend Imports
from backend.utils import SerializeJson

# endregion


# region Table Manipulation Functions
def create_new_personality_from_json(json_filename: str):
    """
    Will create a new personality in the personality table from a JSON file.

    Args:
        json_filename (str): JSON filename (absolute path)
    """
    # [1] Extract personality data from JSON file
    with open(json_filename, "r") as file:
        data = json.load(file)

    # [2] Connect to the SQLite database
    conn = sqlite3.connect("instance/imposter.sqlite")
    cursor = conn.cursor()

    # [3] Insert data from the JSON file into the database
    cursor.execute(
        """
        INSERT INTO personalities (NAME, SYSTEM_PROMPT, INTRO_MESSAGE, IMAGE_PATH)
        VALUES (?, ?, ?, ?)
    """,
        (
            data["name"],
            SerializeJson(data["system_prompt"]),
            data["intro_message"],
            data["image_path"],
        ),
    )

    # [4] Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Data inserted successfully!")


def delete_personality(personality_id: int):
    """
    Will delete personality from personality table.

    Args:
        personality_id (int): ID of personality to remove from table
    """
    # [1] Connect to the SQLite database
    conn = sqlite3.connect("instance/imposter.sqlite")
    cursor = conn.cursor()

    # [2] Delete record based on ID
    cursor.execute("DELETE FROM personalities WHERE ID = ?", (personality_id,))

    # [3] Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Record with ID {personality_id} deleted successfully!")


def update_personality(personality_id: int, json_filename: str):
    """
    Update the personality by its ID from JSON file.

    Args:
        personality_id (int): ID of personality to update
        json_filename (str): JSON filename (absolute path)
    """
    # [1] Extract personality data from JSON file
    with open(json_filename, "r") as file:
        data = json.load(file)

    # [2] Connect to the SQLite database
    conn = sqlite3.connect("instance/imposter.sqlite")
    cursor = conn.cursor()

    # [3] Update the nickname for the specified personality ID
    cursor.execute(
        """
        UPDATE personalities
        SET 
            NAME = ?,
            SYSTEM_PROMPT = ?,
            INTRO_MESSAGE = ?,
            IMAGE_PATH = ?
        WHERE ID = ?
    """,
        (
            data["name"],
            SerializeJson(data["system_prompt"]),
            data["intro_message"],
            data["image_path"],
            personality_id,
        ),
    )
    # [4] Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Personality {personality_id} updated successfully!")


# endregion


def main():
    """
    Take appropriate actions to update databse given the aruments provided by the user.
    """
    # [1] Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Manage data in the personalities SQLite database."
    )

    # [2] Subparsers for different operations
    subparsers = parser.add_subparsers(dest="operation", required=True)

    # [3] Parser for inserting data
    insert_parser = subparsers.add_parser(
        "insert",
        help="Insert data from a JSON file into the database. Args [json_file_path]]",
    )
    insert_parser.add_argument("json_file", help="Path to the JSON file.")

    # [4] Parser for deleting a record
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a record from the database using its ID. Args [personality_id]",
    )
    delete_parser.add_argument(
        "personality_id", type=int, help="ID of the record to delete."
    )

    # [5] Parser for updating a record
    update_parser = subparsers.add_parser(
        "update",
        help="Update a record from the database using its ID. "
        + "Args [personality_id, json_file_path]",
    )
    update_parser.add_argument(
        "personality_id", type=int, help="ID of the record to update."
    )
    update_parser.add_argument("json_file", help="Path to the JSON file.")

    # [6] Parse the arguments
    args = parser.parse_args()

    # [7] Call the appropriate function based on the operation
    if args.operation == "insert":
        create_new_personality_from_json(args.json_file)
    elif args.operation == "delete":
        delete_personality(args.personality_id)
    elif args.operation == "update":
        update_personality(args.personality_id, args.json_file)


if __name__ == "__main__":
    main()
