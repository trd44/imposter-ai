"""
conversation.py

Author: Christian Welling
Date: 12/3/2023
Company: ImposterAI
Contact: csw73@cornell.edu

Class providing direct access to conversation data between a user and a personality.
Conversation will store the following:
    conversation ID (personality ID),
    personality name,
    messages,
    system prompt,
    personality image path
"""


class Conversation:
    def __init__(
        self,
        id: str = 0,
        name: str = "bot",
        message_log: list = [],
        system_prompt_list: list = [],
        img: str = "",
    ):
        """
        Store and provide access to single conversation between user and personality.

        message_log is a json containing message information in the form of a list of
        dictionaries.

        Each item in the list is formatted with a 'role' key and 'content' key,
        whereby the role specifies the type of message, and the content contains the
        contents of the message it self.

            Example:
                {"role": <string>, "content": <string>}

        3 message role types:
            [1] "user" : Identifies a user generated message.
            [2] "assistant" : Identifies a personality generated message.
            [3] "system" : Identifies a system prompt string used by the AI model.

        message_log only contains messages with 'user' and 'assistant' roles, but
        exporting the conversation will contain all three roles if they exist.

        Args:
            id (int): Conversation id (matching personaity id)
            name (str): Name of personality user converses with
            message_log (list):
                List of dictionaries containing messages (in sequentail order) of the
                'user' and 'assistant'
            system_prompt_list (list): List of strings (str) containing system prompts
            img (str): Path to personality image in backend assets
        """
        self._id: str = id
        self._name: str = name
        self._message_log: list = message_log
        self._system_prompt_list: list = system_prompt_list
        self._img: str = img

    def export_saved_messages(self) -> list:
        """
        Exports conversation into acceptable input format for model API request.

        Will presume that every item in the system prompt array list is a sentence.

        Returns:
            List of dictionaries containing system prompt and messages in sequential
            order.
        """
        message_export = []

        # Create system message from system prompt list if exists
        if self._system_prompt_list:
            sys_prompt = {"role": "system", "content": ""}
            for prompt in self._system_prompt_list:
                if sys_prompt["content"] != "":
                    sys_prompt["content"] = sys_prompt["content"] + " "
                sys_prompt["content"] = sys_prompt["content"] + prompt

            message_export.append(sys_prompt)

        # Add messages from message_log to export if exist and return
        if self._message_log is None:
            return message_export

        else:
            return message_export + self._message_log

    def add_user_message(self, user_message: str) -> None:
        """
        Appends a user message to the message_log list.

        Arguments:
            user_message (str): The message from the user to be appended.
        """
        # Append a dictionary containing 'role' and 'content' into the message log
        self._message_log.append({"role": "user", "content": user_message})

    def add_system_message(self, system_message: str) -> None:
        """
        Appends a system message to the system_prompt_list.

        Arguments:
            system_message (str): The system message to be appended.
        """
        # Append a system message into the system prompt list
        self._system_prompt_list.append(system_message)

    def add_assistant_message(self, assistant_message: str) -> None:
        """
        Appends an assistant message to the message_log list.

        Arguments:
            assistant_message (str): The assistant's message to be appended.
        """
        # Append a dictionary containing 'role' and 'content' into the message log
        self._message_log.append({"role": "assistant", "content": assistant_message})

    def get_messages(self) -> list:
        """
        Fetches all messages from the message_log list.

        Returns:
            list: Returns all messages in the message_log list.
        """
        # Return the entire message log
        return self._message_log

    def get_system_prompt(self) -> list:
        """
        Retrieves all system prompts from the system_prompt_list.

        Returns:
            list: Returns all system prompts in the system_prompt_list.
        """
        # Return the entire system prompt list
        return self._system_prompt_list

    def get_personality_name(self) -> str:
        """
        Fetches the personality name of the assistant.

        Returns:
            str: Returns the name of the assistant.
        """
        # Return the assistant's name
        return self._name

    def get_img(self) -> str:
        """
        Retrieves the image path within the backend assets directory of the assistant.

        Returns:
            str: Returns the image path of the assistant.
        """
        # Return the assistant's image URL
        return self._img
