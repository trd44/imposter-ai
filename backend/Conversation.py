

''' Stores the messages in a conversation as well as the system prompt message '''
class Conversation:

    def __init__(self, id = 0, name = "bot", message_log = [], system_prompt_list = [], img = ''):
        """ 
        Initializes a conversation


        message_log is a json containing message information {"role": <string>, "content": <string>}
        3 Roles: "user", "assistant", "system" (last reserved for system prompt)

        system prompt is a list of strings. [<string>]

        """
        self.id = id
        self.name = name
        self.message_log = message_log
        self.system_prompt_list = system_prompt_list
        self.img = img

    def ExportSavedMessages(self):
        """
        Exports conversation into acceptable input format for OpenAI API request

        Will presume that every item in the system prompt array list is a sentence.
        """
        # create system message
        message_export = []
        if self.system_prompt_list:
            sys_prompt = {"role" : "system", "content": ""}
            for prompt in self.system_prompt_list:
                if sys_prompt["content"] != "":
                    sys_prompt["content"] = sys_prompt["content"] + " "
                sys_prompt["content"] = sys_prompt["content"] + prompt
        
            message_export.append(sys_prompt)

        # print("Exported Message")
        # print(message_export)

        if self.message_log is None:
            return message_export
        
        else:
            # print("self.message_log")
            # print(self.message_log)
            return message_export + self.message_log

    def AddUserMessage(self, user_message):
        self.message_log.append({"role": "user", "content": user_message})
        
    def AddSystemMessage(self, system_message):
        self.system_prompt_list.append(system_message)

    def AddAssistantMessage(self, assistant_message):
        self.message_log.append({"role": "assistant", "content": assistant_message})

    def GetMessages(self):
        return self.message_log
    
    def GetSystemPrompt(self):
        return self.system_prompt_list
    
    def GetPersonalityName(self):
        return self.name

    def GetImg(self):
        return self.img