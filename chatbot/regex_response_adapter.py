import random
import re

from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

responses = ("How was your day?\n", "Why do you say that?\n",
        "Interesting. Can you tell me more?\n", "I see. What is your outlook on life?\n", "Do you like music?\n",
             "What did you do today?", "How do you feel now?", "Are you doing good?", "Are you okay?")

class RegexResponseAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super(RegexResponseAdapter, self).__init__(chatbot, **kwargs)

    def process(self, statement, additional_response_selection_parameters=None):
        input_text = statement.text

        if re.match(r'It (was|is).*', input_text, re.IGNORECASE) or re.match(r'I am.*', input_text, re.IGNORECASE):
            response = random.choice(responses)
            response_statement = Statement(response)
            response_statement.confidence = 1.0
        elif  re.match(r'You .*', input_text, re.IGNORECASE):
            response = "You are amazing!"
            response_statement = Statement(response)
            response_statement.confidence = 1.0
        else:
            response = 'I do not understand.'
            response_statement = Statement(response)
            response_statement.confidence = 0.5

        return response_statement
