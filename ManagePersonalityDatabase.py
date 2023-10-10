
import argparse
import json
import sqlite3

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
        INSERT INTO personality (nickname, system_prompt, img)
        VALUES (?, ?, ?)
    """, (data['nickname'], data['system_prompt'], data['img']))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Data inserted successfully!")

def delete_personality(personality_id):
    # Connect to the SQLite database
    conn = sqlite3.connect("instance/imposter.sqlite")
    cursor = conn.cursor()

    # Delete record based on ID
    cursor.execute("DELETE FROM personality WHERE id = ?", (personality_id,))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Record with ID {personality_id} deleted successfully!")


def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Manage data in a SQLite database.')

    # Subparsers for different operations
    subparsers = parser.add_subparsers(dest='operation', required=True)

    # Parser for inserting data
    insert_parser = subparsers.add_parser('insert', help='Insert data from a JSON file into the database.')
    insert_parser.add_argument('json_file', help='Path to the JSON file.')

    # Parser for deleting a record
    delete_parser = subparsers.add_parser('delete', help='Delete a record from the database using its ID.')
    delete_parser.add_argument('personality_id', type=int, help='ID of the record to delete.')

    # Parse the arguments
    args = parser.parse_args()

    # Call the function
    

    # Call the appropriate function based on the operation
    if args.operation == 'insert':
        CreateNewPersonalityFromJSON(args.json_file)
    elif args.operation == 'delete':
        delete_personality(args.personality_id)


if __name__ == '__main__':
    main()