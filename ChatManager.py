

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

        # TODO: retrieve current conversation history for user

        # TODO: update UI with conversation history if it exists...
        # When should this happen? Should the frontend manage its own content?

    def SendMessage(self, conv_id, message):
        """
        Send a message and make an API call
        """

        # [1] Update the conversation via conversation id
        pass
        
    def UpdateSystemPrompt(self, conv_id, prompt_string):
        """
        Presumes there is only a single prompt

        Simply updates system prompt
        """
        pass

    def SendModelRequest(self, conv_id):
        """
        Makes a model request given the current conversation state
        """
        pass