
#region Imports
import sqlite3
from backend.db import get_db
from backend.Utils import SerializeJson, DeserializeJson
#endregion

# Query the DB for stuff

class DatabaseManager:

    def __init__(self):
        pass

    # all access functions should go here
    # class should be static?
    #TODO: Move functionality from db.py to DatabaseManager

    def GetChatList(user_id: int):
        """
        Returns a list of tuples where each tuple contains,
        (personality_id, nickname)
        Will return None if empty
        """
        db = get_db()
        personality_list = db.execute('''
            SELECT chat.personality_id, personality.nickname
            FROM chat
            JOIN personality ON chat.personality_id = personality.id
            WHERE chat.user_id = ?
            ''', (user_id,)).fetchall()
        return personality_list

    def GetChatFromID(user_id: int, personality_id: int):
        """
        Returns deserialized message json
        Will return None if cannot find
        """
        db = get_db()
        messages = db.execute('''
            SELECT messages 
            FROM chat 
            WHERE user_id = ? AND personality_id = ?
            ''', (user_id, personality_id)).fetchone()
        return DeserializeJson(messages[0]) if messages is not None else None

    def GetSystemPromptFromID(personality_id: int):
        """
        Returns (nickname, deserialized system prompt json, img file path)
        Will return None if cannot find
        """
        db = get_db()
        system_prompt = db.execute('''
            SELECT nickname, system_prompt, img
            FROM personality
            WHERE id = ?
            ''', (personality_id,)).fetchone()
        
        if system_prompt is not None:
            ret = (system_prompt[0], DeserializeJson(system_prompt[1]), system_prompt[2])
        else:
            ret = None
        return ret

    def SaveChat(user_id: int, personality_id: int, messages_json):
        """
        Will save a conversation in the chat table. Will overwrite whatever exists in the table
        at the user_id, personality_id rows
        """
        #TODO: remove assert and have check on inputs instead
        assert messages_json is not None
        db = get_db()

        # Insert chat if not exist, replace if does. Entire row will be replaced, so be sure to include all column data.
        try:
            db.execute('''
                INSERT OR REPLACE INTO chat (user_id, personality_id, messages) 
                VALUES (?, ?, ?)
                ''', (user_id, personality_id, SerializeJson(messages_json)))
            db.commit()
        except Exception as e:
            #TODO: Log errors. Print right now for testing...
            print(e)

    def SavePersonality(personality_id: int, nickname: str, system_prompt, img_file: str = None):
        """
        Will save a personality in the personality table. Will overwrite whatever exists in the table
        at the personality_id row
        """
        #TODO: remove assert and have check on inputs instead
        assert system_prompt is not None
        db = get_db()
    
        # Insert personality if not exist, replace if does. Entire row will be replaced, so be sure to include all column data.
        try:
            if img_file is None:
                '''When img_file is not provided, update only the non-image columns.'''
                db.execute('''
                    UPDATE personality
                    SET nickname = ?, system_prompt = ?
                    WHERE id = ?
                    ''', (nickname, SerializeJson(system_prompt), personality_id))
    
            else:
                '''If img_file is provided, replace the entire row including image '''
                db.execute('''
                    INSERT OR REPLACE INTO personality (id, nickname, system_prompt, img) 
                    VALUES (?, ?, ?, ?)
                    ''', (personality_id, nickname, SerializeJson(system_prompt), img_file))
                
            db.commit()
        except Exception as e:
            #TODO: Log errors. Print right now for testing...
            print(e)