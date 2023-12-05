"""
ai_model.py

Author: Christian Welling
Date: 12/4/2023
Company: ImposterAI
Contact: csw73@cornell.edu

Contains abstract class for AI models used in imposter AI.
"""
# region Imports
from abc import abstractmethod

# endregion


class AIModel:
    @abstractmethod
    def make_request(self, conversation_messages):
        """
        Make request to model.

        Args:
            conversation_messages: messages input for api call

        Returns:
            Message response JSON or None if error
        """
        pass
