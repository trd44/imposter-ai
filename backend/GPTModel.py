import os
import openai

class GPTModel:

    def __init__(self):
        """
        Initialize model usage
        
        Presumes that the API key is set in the environment already...
        """
        self.model_id = "gpt-3.5-turbo"
        pass

    def SetModel(self, model_id):
        """
        Set what model is used.
        """
        self.model_id = model_id

    def MakeRequest(self, conversation_messages):
        """
        TODO: handle errors if wrong request
        Make request to model

        Args:
            conversation_messages : messages input for api call

        Return:
            "assistant" message response if available
        """
        # TODO: Might need to change how key is set. Should only be set once?
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = openai.ChatCompletion.create(
            model=self.model_id,
            messages=conversation_messages
        )
        
        return completion.choices[0].message


