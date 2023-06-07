
#region Imports
from backend.Conversation import Conversation
from backend.DatabaseManager import DatabaseManager as dbm
#endregion

#region Test Data Imports
from Presets.PresetData import TEST_PERSONALITY_NICKNAME, TEST_PERSONALITY_ID, TEST_SYSTEM_PROMPT
#endregion

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

        # TODO: retrieve current conversation history for user
        self.UpdateConversationHistoryFromRemote()

        # TODO: update UI with conversation history if it exists...
        # When should this happen? Should the frontend manage its own content?

    def SendMessage(self, conv_id, message):
        """
        Send a message and make an API call
        """

        # [1] Update the conversation via conversation id
        self.current_conversation = self.conversation_history[conv_id]
        self.current_conversation.AddUserMessage(message)

        # [2] Send message
        resp = self.SendModelRequest(conv_id)

        # TODO: error handling on response
        # [3] Update conversation with response
        self.current_conversation.AddAssistantMessage(resp.choices[0].message.content)
        
        return resp.choices[0].message

    def UpdateSystemPrompt(self, conv_id, prompt_string):
        """
        Presumes there is only a single prompt

        Simply updates system prompt
        """
        self.current_conversation = self.current_conversation[conv_id]
        self.current_conversation.AddSystemMessage(prompt_string)

    def SendModelRequest(self, conv_id):
        """
        Makes a model request given the current conversation state
        """
        self.model.MakeRequest(self.conversation_history[conv_id].ExportSavedMessages())

    def StoreConversation(self, conv_id):
        """
        Stores the current state of the conversation in the database
        """
        # retreive messages from conversation
        messages = self.conversation_history[conv_id].GetMessages()
        dbm.SaveChat(self.user_id, conv_id, messages)

        # TODO: handle when to save personality...for now always do
        name = self.conversation_history[conv_id].GetPersonalityName()
        system_prompt = self.conversation_history[conv_id].GetSystemPrompt()
        dbm.SavePersonality(conv_id, name, system_prompt)

    def QuerySavedConversations(self):
        """
        Retrieves all of the available chats. If there are none, returns none
        Returns a list of tubles containing conversation ids and the corresponding personality name
        (conv_id, personality_name)
        """
        return dbm.GetChatList(self.user_id)

    def UpdateConversationHistoryFromRemote(self):
        """
        Updates conversation list with remove conversations
        """
        conversation_list = self.QuerySavedConversations()
        if conversation_list is None:
            self.conversation_history[TEST_PERSONALITY_ID] = Conversation(TEST_PERSONALITY_ID, TEST_PERSONALITY_NICKNAME, TEST_SYSTEM_PROMPT)
        else:
            for conv_id, _ in conversation_list:
                # get conversation
                self.RetrieveConversation(conv_id)
        
    def RetrieveConversation(self, conv_id):
        """
        Updates conversation with the stored conversation from the database
        """
        # TODO: error checking
        messages = dbm.GetChatFromID(self.user_id, conv_id)
        name, system_prompt = dbm.GetSystemPromptFromID(conv_id)
        self.conversation_history[conv_id] = Conversation(conv_id, name, messages, system_prompt)
        return self.conversation_history[conv_id]