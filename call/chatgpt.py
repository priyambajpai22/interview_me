import os
import openai
from .constant import first_gpt_chat
import logging
logger = logging.getLogger(__name__)



class ChatSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ChatSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ChatGptInitailize(metaclass=ChatSingleton):
    def __init__(self):
        self.key=''
        openai.api_key ='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'
        self.messages=[{"role": "system", "content":first_gpt_chat}]
        self.Model='gpt-3.5-turbo'


    def initailize_chat(self):
        response = openai.ChatCompletion.create(
        model=self.Model,
        messages=self.messages,temperature=0,stream=False)
        self.messages.append(response['choices'][0]['message'])
        logger.info(response)
        print(response)



    def talk_to_gpt(self,text):
        data={"role":"user",'content':text}
        self.messages.append(data)
        response = openai.ChatCompletion.create(
        model=self.Model,
        messages=self.messages[-4:],temperature=0,stream=True)
        logger.info(response)
        print(response)

        for x in response:
            yield x


    def fine_tune_model(self):
        pass





    