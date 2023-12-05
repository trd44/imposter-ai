"""
database_manager.py

Author: Christian Welling
Date: 12/3/2023
Company: ImposterAI
Contact: csw73@cornell.edu

Class for managing database usage.
"""

# region Imports
from backend.db import get_db
from backend.utils import serialize_json, deserialize_json
from sqlite3 import Connection

# endregion


class DatabaseManager:
    @staticmethod
    def get_all_personalities() -> list:
        """
        Fetches all personalities from the database as a list of tuples.

        Returns:
            list: A list of tuples where each tuple contains the following information
            for each personality, (ID, name, image file name, introduction message).
            Will return None if no personalities are found in the database.
        """

        # Connect to the database
        db: Connection = get_db()

        # Execute SQL command to fetch all personalities from personalities table
        personality_list = db.execute(
            """
            SELECT ID, NAME, IMAGE_PATH, INTRO_MESSAGE
            FROM personalities
            """
        ).fetchall()

        # Return the fetched list
        return personality_list

    @staticmethod
    def get_chat_list(user_id: int) -> list:
        """
        Fetches a list of personalities user has started a conversation
        with.

        Args:
            user_id (int): The ID of the user for whom to fetch chat details.

        Returns:
            list: A list of tuples, where each tuple contains
            (Personality ID, Personality Name).
            Will return None if no chat records found for the given user_id.
        """

        # Connect to the database
        db: Connection = get_db()

        # Execute SQL command to fetch chat details corresponding to the user_id.
        # Joining chats and personalities table to get the personality name.
        personality_list = db.execute(
            """
            SELECT chats.PERSONALITY_ID, personalities.NAME
            FROM chats
            JOIN personalities ON chats.PERSONALITY_ID = personalities.ID
            WHERE chats.USER_ID = ?
            """,
            (user_id,),
        ).fetchall()

        # Return the fetched list
        return personality_list

    @staticmethod
    def get_chat_from_id(user_id: int, personality_id: int):
        """
        Fetches and deserializes the messages associated with the given user ID
        and personality ID.

        Args:
            user_id (int): The ID of the user for whom to fetch message details.
            personality_id (int):
                The ID of the personality related to the chat messages.

        Returns:
            Deserialized JSON object (message list) if found, else None.
        """

        # Connect to the database
        db: Connection = get_db()

        # Execute SQL command to fetch messages corresponding to the user_id
        # and personality_id from the chats table
        messages = db.execute(
            """
            SELECT MESSAGES
            FROM chats
            WHERE USER_ID = ? AND PERSONALITY_ID = ?
            """,
            (user_id, personality_id),
        ).fetchone()

        # Return deserialized messages if found, else return None
        return deserialize_json(messages[0]) if messages is not None else None

    @staticmethod
    def get_personality_from_id(personality_id: int):
        """
        Fetches and deserializes the personality details associated with the given
        personality ID.

        Args:
            personality_id (int): The ID of the personality for whom to fetch details.

        Returns:
            Tuple containing personality name, deserialized system prompt JSON,
            intro message, and image file path if found; else None.
        """

        # Connect to the database
        db: Connection = get_db()

        # Execute SQL command to fetch details corresponding to the personality_id
        # from the personalities table
        personality_row = db.execute(
            """
            SELECT NAME, SYSTEM_PROMPT, INTRO_MESSAGE, IMAGE_PATH
            FROM personalities
            WHERE ID = ?
            """,
            (personality_id,),
        ).fetchone()

        if personality_row is not None:
            # If a personality row is found, return a tuple of deserialized data
            ret = (
                personality_row[0],
                deserialize_json(personality_row[1]),
                personality_row[2],
                personality_row[3],
            )
        else:
            ret = None

        # Return the tuple or None if personality was not found
        return ret

    @staticmethod
    def save_chat(user_id: int, personality_id: int, messages_json) -> None:
        """
        Saves a conversation with a personality in the chat table for
        a specific user. The function will overwrite any existing conversation data
        for an existing conversation.

        Args:
            user_id (int): The ID of the user involved in the chat.
            personality_id (int): The ID of the personality involved in the chat.
            messages_json: The JSON object representing the messages in the chat.
        """

        # Check that messages_json is not None
        # TODO: Remove assert statement and add checks on inputs instead
        assert messages_json is not None

        # Connect to database
        db: Connection = get_db()

        try:
            # Insert or replace entire row in chats table
            db.execute(
                """
                INSERT OR REPLACE INTO chats (USER_ID, PERSONALITY_ID, MESSAGES) 
                VALUES (?, ?, ?)
                """,
                (user_id, personality_id, serialize_json(messages_json)),
            )
            db.commit()
        except Exception as e:
            # Log errors
            # TODO: Replace print statement with logging
            print(e)

    @staticmethod
    def save_personality(
        personality_id: int, nickname: str, system_prompt: str, img_file: str = None
    ) -> None:
        """
        Saves or updates a personality in the personality table.
        The function will overwrite existing data for the specified personality id with
        the exception of the image file path. Will use existing path if not provided
        in update.

        Args:
            personality_id (int): The ID of the personality to be saved.
            nickname (str): The nickname for the personality.
            system_prompt (str): The system_prompt related to the personality.
            img_file (str): The image file path for the personality.
        """

        # Check that system_prompt is not None
        # TODO: Remove assert statement and add checks on inputs instead
        assert system_prompt is not None

        # Connect to database
        db: Connection = get_db()

        try:
            # If img_file is not provided, update only non-image columns
            if img_file is None:
                db.execute(
                    """
                    UPDATE personalities
                    SET NAME = ?, SYSTEM_PROMPT = ?
                    WHERE ID = ?
                    """,
                    (nickname, serialize_json(system_prompt), personality_id),
                )
            # If img_file is provided, replace entire row including image
            else:
                db.execute(
                    """
                    INSERT OR REPLACE INTO personalities (ID, NAME, SYSTEM_PROMPT, IMAGE_PATH) 
                    VALUES (?, ?, ?, ?)
                    """,
                    (personality_id, nickname, serialize_json(system_prompt), img_file),
                )

            db.commit()
        except Exception as e:
            # Log errors
            # TODO: Replace print statement with logging
            print(e)
