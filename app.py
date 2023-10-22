from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app = Flask(__name__)

my_bot = ChatBot(name='QuestionBot',read_only = True,
                 response_selection_method=get_random_response,
                 logic_adapters=[
        # {
        #     'import_path': 'chatterbot.logic.SpecificResponseAdapter',
        #     'input_text': '',
        #     'output_text': 'Thanks for sharing'
        # },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I do not understand. Sorry.',
            'maximum_similarity_threshold': 0.9
        },
        {
            'import_path': 'chatbot.regex_response_adapter.RegexResponseAdapter'
        }
    ]
    )

trainer = ChatterBotCorpusTrainer(my_bot)

trainer.train(
    "./conversations.yml"
)
trainer.train( 'chatterbot.corpus.english.emotion',
               'chatterbot.corpus.english.conversations')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get')
@cross_origin()
def get_bot_response():
    user_message = request.args.get('userMessage')

    if user_message.lower() == 'bye'.lower():
        bot_response = "Thank you for answering my questions. Have a great day!"
    else:
        response_statement = my_bot.get_response(user_message)
        bot_response = response_statement.text
    return bot_response

if __name__ == '__main__':

    app.run(debug=True)
