"""
chat_manager.py

Author: Christian Welling
Date: 12/3/2023
Company: ImposterAI
Contact: csw73@cornell.edu

Class for managing conversations of a user. Pulls conversation and personality
information from DatabaseManager.
"""

# region Backend Imports
from backend.conversation import Conversation
from backend.database_manager import DatabaseManager as dbm
from backend.gpt_model import AIModel
from backend.logger import LOGGER

# endregion


class ChatManager:
    def __init__(self, user_id: int, model: AIModel) -> None:
        """
        Manages conversations and API model usage for a user.

        Args:
            user_id (int): user identification used in querying database
            model: Some type of model object which isn't specified here.
        """
        self._user_id: int = user_id
        self._model: AIModel = model
        self._conversation_history: dict = {}

        # Retrieve current conversation history for user
        self.update_conversation_history_from_remote()

    def send_message(self, conv_id: int, message) -> dict[str, str]:
        """
        Send a message by making API request for given model and returns response.

        This method sends a message to a given conversation ID. If the conversation
        doesn't exist yet, a new one will be created. The method also handles the
        response from the API, updates the conversation history with the assistant's
        message and stores it.

        Args:
            conv_id (int):
                The ID of the conversation to which the message should be sent.

            message (str):
                The content of the message to be sent.

        Returns:
            dict[str, str]:
                A dictionary including the response content and the id of the
                conversation. The dictionary keys are "content" for the message
                returned by the API (with a fallback error message if no response is
                received) and "id" for the conversation ID.
        """

        # [1] Retrieve the conversation in question
        LOGGER.debug(f"Sending message for conversation ID: {conv_id}.")

        # If conversation ID does not exist, create new conversation
        if conv_id not in self._conversation_history.keys():
            LOGGER.debug("Creating new conversation.")
            self.create_conversation(conv_id)

        self.current_conversation: Conversation = self._conversation_history[conv_id]

        # [2] Update the conversation via conversation id
        self.current_conversation.add_user_message(message)

        # [3] Send message
        # TODO: error handling on response
        resp = self._send_model_request(conv_id)
        if resp:
            LOGGER.debug("Response received.")

            # [4] Update conversation with response
            self.current_conversation.add_assistant_message(resp.content)

            # Store History
            self.store_conversation(conv_id)
        else:
            error_msg = (
                "... Imposter does not feel like responding at the current moment "
                + "... please try again later!"
            )
            resp = {"content": error_msg}

        # [5] Include id in response payload
        resp["id"] = conv_id

        return resp

    def update_system_prompt(self, conv_id: int, prompt_string: str) -> None:
        """
        Updates the system pompt for a specified conversation/personality ID.
        Presumes there is only a single prompt.

        Args:
            conv_id (int): Conversation/personality id
            prompt_string (str): System prompt
        """
        # TODO: error handling (1) if conversation does not exist
        # Fetch relevant conversation if exist
        if conv_id in self._conversation_history:
            self.current_conversation: Conversation = self.current_conversation[conv_id]
            # Update system prompt for conversation
            self.current_conversation.add_system_message(prompt_string)
        else:
            LOGGER.error(
                f"Conversation does not exist, cannot update prompt for ID: {conv_id}!"
            )

    def _send_model_request(self, conv_id: int):
        """
        Makes a model request given the current conversation state.

        Args:
            conv_id (int): Conversation id

        Return:
            Model restful API response json.
        """
        return self._model.make_request(
            self._conversation_history[conv_id].export_saved_messages()
        )

    def store_conversation(self, conv_id) -> None:
        """
        Stores the current state of the conversation in the database.

        Args:
            conv_id (int): Conversation id
        """
        # retreive messages from conversation
        messages = self._conversation_history[conv_id].get_messages()
        dbm.save_chat(self._user_id, conv_id, messages)

    def query_saved_conversations(self) -> list:
        """
        Retrieves all available chat conversations for a user from the database.

        Returns:
            list: A list of tuples where each tuple contains a conversation id
            ('conv_id') and a corresponding personality name ('personality_name').
            If there are no saved conversations, it returns an empty list.

            Example:
                [('conv_id_1', 'personality_name_1'),...]
        """
        return dbm.get_chat_list(self._user_id)

    def update_conversation_history_from_remote(self) -> None:
        """
        Updates conversation list with any existing conversations from remote.
        """
        LOGGER.info("Updating conversation history.")
        conversation_list = self.query_saved_conversations()
        if conversation_list is None or conversation_list == []:
            LOGGER.info(f"No recorded conversations for User ID: {self._user_id}")
        else:
            for conv_id, _ in conversation_list:
                # Create conversation object for all retrieved convesations from remote
                self.retrieve_conversation(conv_id)

    def retrieve_conversation(self, conv_id: int) -> Conversation:
        """
        Updates conversation history with the stored conversation from the database
        given conversation id.

        Args:
            conv_id (int): Conversation id

        Returns:
            conversation object for current conversation id.
        """
        # Retrieve conversation messages from database if conversation exists
        LOGGER.info(f"Retreiving conversation with ID: {conv_id}.")
        messages = dbm.get_chat_from_id(self._user_id, conv_id)
        if messages is None:
            messages = []
            LOGGER.debug(f"No record of conversation with ID: {conv_id} exists!")
            LOGGER.debug("Creating new conversation!")

        return self.create_conversation(conv_id, messages)

    def create_conversation(
        self, personality_id: int, messages: list = []
    ) -> Conversation:
        """
        Creates a new conversation object and assigns it to the conv_id key in
        conversation_history dict. Conversation id (conv_id) will match the
        personality id (personality_id) when a conversation is created.

        Args:
            personality_id (int): Personality id (same as conversation id)
            messages (list):
                Array of messages related to conversation. If new conversation,
                leave as empty list.

        Returns:
            Newly created conversation object.
        """
        # TODO: error checking personality_id does not match any know personalities in
        # database
        # [1] Get personality information from database
        name, system_prompt, intro_message, img = dbm.get_personality_from_id(
            personality_id
        )
        LOGGER.debug(
            f"Retrieved personality information for {name} ({personality_id})."
        )

        if messages == []:
            # If no messages are provided, create a new conversation
            messages.append({"role": "assistant", "content": intro_message})

        # [2] Create new conversation in history with personality and message
        # information
        self._conversation_history[personality_id] = Conversation(
            personality_id, name, messages, system_prompt, img
        )
        return self._conversation_history[personality_id]
