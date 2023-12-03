# region Imports
from backend.conversation import Conversation
from backend.DatabaseManager import DatabaseManager as dbm

# endregion


class ChatManager:
    def __init__(self, user_id, database, model):
        """
        Manages conversations and API model usage for a user

        TODO: database as service injection
        TODO: model as service injection

        Args:
            user_id : user identification used in querying database
        """
        self.database = database
        self.user_id = user_id
        self.model = model
        self.conversation_history = {}

        # Retrieve current conversation history for user
        self.UpdateConversationHistoryFromRemote()

    def SendMessage(self, conv_id, message):
        """
        Send a message and make an API call
        """

        # [1] Retrieve the conversation in question
        print(self.conversation_history)
        print("Sending message for conversation ID: ", conv_id)

        # If conversation ID does not exist, create new conversation
        if conv_id not in self.conversation_history.keys():
            print("New conversation")
            # TODO: New conversations might need to have a specific "first message" that is curated or stored somewhere...
            #      Currently, there is no "first message" for a new conversation.
            self.CreateConversation(conv_id)

        self.current_conversation = self.conversation_history[conv_id]

        # [2] Update the conversation via conversation id
        print("Appending message")
        self.current_conversation.AddUserMessage(message)

        # [3] Send message
        # TODO: error handling on response
        resp = self.SendModelRequest(conv_id)
        if resp:
            print("Response received")
            print(resp)

            # [4] Update conversation with response
            self.current_conversation.AddAssistantMessage(resp.content)

            # Store History
            self.StoreConversation(conv_id)
        else:
            error_msg = "... Imposter does not feel like responding at the current moment ... please try again later!"
            resp = {"content": error_msg}

        # [5] Include id in response payload
        resp["id"] = conv_id

        return resp

    def UpdateSystemPrompt(self, conv_id, prompt_string):
        """
        Updates the system pompt for a specified conversation/personality ID.
        Presumes there is only a single prompt.

        Args:
            conv_id : Conversation/personality id
            prompt_string : System prompt
        """
        # TODO: error handling (1) if conversation does not exist
        if conv_id in self.conversation_history:
            self.current_conversation = self.current_conversation[conv_id]
            try:
                self.current_conversation.AddSystemMessage(prompt_string)
            except Exception as e:
                print(
                    f"Object stored at current_conversation[{conv_id}] is not a valid Conversation object!\n Error: ",
                    e,
                )
        else:
            print(
                f"Conversation does not exist, cannot update prompt for ID: {conv_id}!"
            )

    def SendModelRequest(self, conv_id):
        """
        Makes a model request given the current conversation state.

        Args:
            conv_id : Conversation id

        Return:
            Model restful API response json.
        """
        return self.model.MakeRequest(
            self.conversation_history[conv_id].ExportSavedMessages()
        )

    def StoreConversation(self, conv_id):
        """
        Stores the current state of the conversation in the database. Will not update the personality table in any way.

        Args:
            conv_id : Conversation id
        """
        # retreive messages from conversation
        messages = self.conversation_history[conv_id].GetMessages()
        dbm.SaveChat(self.user_id, conv_id, messages)

    def QuerySavedConversations(self):
        """
        Retrieves all of the available chats. If there are none, returns none
        Returns a list of tubles containing conversation ids and the corresponding personality name
        (conv_id, personality_name)
        """
        return dbm.GetChatList(self.user_id)

    def UpdateConversationHistoryFromRemote(self):
        """
        Updates conversation list with any existing conversations from remote.
        """
        print("Updating Conversation History")
        conversation_list = self.QuerySavedConversations()
        print("Conversation List:")
        print(conversation_list)
        if conversation_list is None or conversation_list == []:
            print("No recorded conversations!")
        else:
            for conv_id, _ in conversation_list:
                # Create conversation object for all retrieved convesations from remote
                self.RetrieveConversation(conv_id)

    def RetrieveConversation(self, conv_id):
        """
        Updates conversation history with the stored conversation from the database given conversation id.

        Args:
            conv_id : Conversation id

        Returns:
            conversation object for current id
        """
        print(f"RETRIEVING CONVERSATION for ID: {conv_id}")
        messages = dbm.GetChatFromID(self.user_id, conv_id)
        if messages:
            print("Retreived messages:")
            print(messages)
        else:
            messages = []
            print(f"No record of conversation with ID: {conv_id} exists!")
            print(f"Creating new conversation!")

        return self.CreateConversation(conv_id, messages)

    def CreateConversation(self, personality_id, messages=[]):
        """
        Creates a new conversation object and assigns it to the conv_id key in conversation_history dict

        Args:
            personality_id : Personality id
            messages: Array of messages related to conversation. If new conversation leave empty.
        """
        # TODO: error checking (1) if conv_id does not exist
        # [1] Get personality information from database
        name, system_prompt, intro_message, img = dbm.GetPersonalityFromID(
            personality_id
        )
        print(f"Retrieved personality {name}")

        if messages == []:
            # If no messages are provided, create a new conversation
            messages.append({"role": "assistant", "content": intro_message})

        # [2] create new conversation in history with personality and message information
        self.conversation_history[personality_id] = Conversation(
            personality_id, name, messages, system_prompt, img
        )
        return self.conversation_history[personality_id]
