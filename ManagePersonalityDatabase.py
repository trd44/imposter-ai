
import argparse
import json
import sqlite3
from backend.Utils import SerializeJson

def CreateNewPersonalityFromJSON(json_filename):
    """
    Will create a new personality in the personality table from a JSON file.
    """
    with open(json_filename, 'r') as file:
        data = json.load(file)

    # Connect to the SQLite database
    conn = sqlite3.connect("instance/imposter.sqlite")
    cursor = conn.cursor()

    # Insert data from the JSON file into the database
    cursor.execute("""
        INSERT INTO personalities (NAME, SYSTEM_PROMPT, INTRO_MESSAGE, IMAGE_PATH)
        VALUES (?, ?, ?, ?)
    """, (data['name'], SerializeJson(data['system_prompt']), data['intro_message'], data['image_path']))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Data inserted successfully!")

def delete_personality(personality_id):
    # Connect to the SQLite database
    conn = sqlite3.connect("instance/imposter.sqlite")
    cursor = conn.cursor()

    # Delete record based on ID
    cursor.execute("DELETE FROM personalities WHERE ID = ?", (personality_id,))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Record with ID {personality_id} deleted successfully!")

def update_personality(personality_id, json_filename):
    """Update the personality by its ID."""

    with open(json_filename, 'r') as file:
        data = json.load(file)
    
    # Connect to the SQLite database
    conn = sqlite3.connect("instance/imposter.sqlite")
    cursor = conn.cursor()

    # Update the nickname for the specified personality ID
    cursor.execute("""
        UPDATE personalities
        SET 
            NAME = ?,
            SYSTEM_PROMPT = ?,
            INTRO_MESSAGE = ?,
            IMAGE_PATH = ?
        WHERE ID = ?
    """, (data['name'], SerializeJson(data['system_prompt']), data['intro_message'], data['image_path'], personality_id))
    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Personality {personality_id} updated successfully!")
    pass

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Manage data in the personalities SQLite database.')

    # Subparsers for different operations
    subparsers = parser.add_subparsers(dest='operation', required=True)

    # Parser for inserting data
    insert_parser = subparsers.add_parser('insert', help='Insert data from a JSON file into the database. Args [json_file_path]]')
    insert_parser.add_argument('json_file', help='Path to the JSON file.')

    # Parser for deleting a record
    delete_parser = subparsers.add_parser('delete', help='Delete a record from the database using its ID. Args [personality_id]')
    delete_parser.add_argument('personality_id', type=int, help='ID of the record to delete.')

    # Parser for updating a record
    update_parser = subparsers.add_parser('update', help='Update a record from the database using its ID. Args [personality_id, json_file_path]')
    update_parser.add_argument('personality_id', type=int, help='ID of the record to update.')
    update_parser.add_argument('json_file', help='Path to the JSON file.')

    # Parse the arguments
    args = parser.parse_args()

    # Call the function
    

    # Call the appropriate function based on the operation
    if args.operation == 'insert':
        CreateNewPersonalityFromJSON(args.json_file)
    elif args.operation == 'delete':
        delete_personality(args.personality_id)
    elif args.operation == 'update':
        update_personality(args.personality_id, args.json_file)


if __name__ == '__main__':
    main()