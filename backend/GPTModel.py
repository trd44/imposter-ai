import os
import openai

class GPTModel:

    def __init__(self):
        """
        Initialize model usage
        
        Presumes that the API key is set in the environment already...
        """
        #self.model_id = "gpt-3.5-turbo"
        self.model_id = "gpt-4"
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
            None if error
        """
        # TODO: Might need to change how key is set. Should only be set once?
        openai.api_key = os.getenv("OPENAI_API_KEY")

        ret = None
        try:
            completion = openai.ChatCompletion.create(
                model=self.model_id,
                messages=conversation_messages,
                temperature=1.2,
            )
            print("Model Completion:")
            print(completion)
            ret = completion.choices[0].message
        ### API ERROR HANDLING
        ## [SERVICE ERRORS]
        except openai.error.APIConnectionError as e:
            #Handle connection error here
            print(f"Failed to connect to OpenAI API: {e}")
        except openai.error.ServiceUnavailableError as e:
            #Handle service unavailabe error
            print(f"OpenAI API service is currently unavailable: {e}")
        except openai.error.RateLimitError as e:
            #Handle rate limit error (we recommend using exponential backoff)
            print(f"OpenAI API request exceeded rate limit: {e}")
        except (openai.error.Timeout, openai.error.TryAgain) as e:
            #Handle timeout error (retry after a few seconds)
            print(f"OpenAI API request timeout: {e}")
        
        ## [AUTHENTIFICATION ERRORS]
        except openai.error.AuthenticationError as e:
            #Handle authetication error
            print(f"OpenAI API key cannot be authenticated: {e}")
        except openai.error.PermissionError as e:
            #Handle permission error
            print(f"OpenAI API request does not have permission: {e}")    
        except openai.error.SignatureVerificationError as e:
            #Handle signature verification error
            print(f"OpenAI API signature cannot be verified: {e}")

        ## [REQUEST ERRORS]
        except openai.error.InvalidAPIType as e:
            #Handle invalid API Type error
            print(f"OpenAI API request contained invalid API Type: {e}")
        except openai.error.InvalidRequestError as e:
            #Handle invalid request error
            print(f"OpenAI API request is invalid: {e}")   

        ## [GENERAL API ERROR]
        except openai.error.APIError as e:
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")

        ## [UNKNOWN ERROR]
        except Exception as e:
            print(f"An unknown error occured: {e}")
        
        return ret


