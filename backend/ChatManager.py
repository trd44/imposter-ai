
#region Imports
from backend.Conversation import Conversation
from backend.DatabaseManager import DatabaseManager as dbm
#endregion

#region Test Data Imports
from Presets.PresetData import TEST_PERSONALITY_NICKNAME, TEST_PERSONALITY_ID, TEST_SYSTEM_PROMPT, TEST_PERSONALITY_IMG
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
        print(self.conversation_history)
        print("Sending Message For Conversation ID: ", conv_id)
        self.current_conversation = self.conversation_history[conv_id]
        print("Appending Message")
        self.current_conversation.AddUserMessage(message)

        # [2] Send message
        # TODO: error handling on response
        resp = self.SendModelRequest(conv_id)
        if resp:
            print("Response Received")
            print(resp)

            # [3] Update conversation with response
            self.current_conversation.AddAssistantMessage(resp.content)

            # Store History
            self.StoreConversation(conv_id)
        else:
            error_msg = "... Imposter does not feel like responding at the current moment ... please try again later!"
            resp = {"content": error_msg}

        # [5] Include id in response payload
        resp['id'] = conv_id

        return resp

    def UpdateSystemPrompt(self, conv_id, prompt_string):
        """
        Updates the system pompt for a specified conversation/personality ID.
        Presumes there is only a single prompt.

        Args:
            conv_id : Conversation/personality id
            prompt_string : System prompt
        """
        #TODO: error handling (1) if conversation does not exist
        if conv_id in self.conversation_history:
            self.current_conversation = self.current_conversation[conv_id]
            try:
                self.current_conversation.AddSystemMessage(prompt_string)
            except Exception as e:
                print(f"Object stored at current_conversation[{conv_id}] is not a valid Conversation object!\n Error: ", e)
        else:
            print(f"Conversation does not exist, cannot update prompt for ID: {conv_id}!")

    def SendModelRequest(self, conv_id):
        """
        Makes a model request given the current conversation state.

        Args:
            conv_id : Conversation id

        Return:
            Model restful API response json.
        """
        return self.model.MakeRequest(self.conversation_history[conv_id].ExportSavedMessages())

    def StoreConversation(self, conv_id):
        """
        Stores the current state of the conversation in the database.

        Args:
            conv_id : Conversation id
        """
        # retreive messages from conversation
        messages = self.conversation_history[conv_id].GetMessages()
        dbm.SaveChat(self.user_id, conv_id, messages)

        # TODO: handle when to save personality...for now always do
        name = self.conversation_history[conv_id].GetPersonalityName()
        system_prompt = self.conversation_history[conv_id].GetSystemPrompt()
        img = self.conversation_history[conv_id].GetImg()
        ## TODO: Do not save personality each time???
        ## TODO: Address not overwriting the test contact image each time...where to update personality...
        dbm.SavePersonality(conv_id, name, system_prompt, img)

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
        print("Updating Conversation History")
        conversation_list = self.QuerySavedConversations()
        print("Conversation List:")
        print(conversation_list)
        #TODO: currently, we save all personality info in the conversation object, maybe we dont want to do that...
        #TODO: should create this default conversation for every personality
        if conversation_list is None or conversation_list == []:
            self.conversation_history[TEST_PERSONALITY_ID] = Conversation(TEST_PERSONALITY_ID, TEST_PERSONALITY_NICKNAME, [], TEST_SYSTEM_PROMPT, TEST_PERSONALITY_IMG)
            print("No recorded conversations. Creating first one!", "First Conversation ID: ", TEST_PERSONALITY_ID)
        else:
            for conv_id, _ in conversation_list:
                # get conversation
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
    
    def CreateConversation(self, conv_id, messages = []):
        """
        Creates a new conversation object and assigns it to the conv_id key in conversation_history dict

        Args:
            conv_id : Conversation id/personality id
            messages: Array of messages related to conversation. If new conversation leave empty.
        """
        # TODO: error checking (1) if conv_id does not exist
        # [1] Get personality information from database
        name, system_prompt, img = dbm.GetSystemPromptFromID(conv_id)
        print("Retreived system prompt for, ", name)
        print(system_prompt)

        # [2] create new conversation in history with personality and message information
        self.conversation_history[conv_id] = Conversation(conv_id, name, messages, system_prompt, img)
        return self.conversation_history[conv_id]