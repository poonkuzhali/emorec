from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from keras.models import load_model

from sentiment_model.prediction import predict_emotions

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
loaded_model = load_model('sentiment_model.h5')
messages = []

my_bot = ChatBot(name='QuestionBot',read_only = True,
                 response_selection_method=get_random_response,
                 logic_adapters=[
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

# trainer.train(
#     "./conversations.yml"
# )
# trainer.train( 'chatterbot.corpus.english.emotion',
#                'chatterbot.corpus.english.conversations')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['GET'])
@cross_origin()
def get_bot_response():
    user_message = request.args.get('userMessage')
    messages.append([user_message])

    if user_message.lower() == 'bye'.lower():
        emotions = get_emotions()
        bot_response = emotions
    else:
        response_statement = my_bot.get_response(user_message)
        bot_response = response_statement.text
    return bot_response

# @app.route('/predict', methods=['GET'])
# @cross_origin()
def get_emotions():
    # user_messages = request.args.get('messages')
    # predict_emotions([['My dog fell sick'], ['Hi dude']], loaded_model)
    emotions = predict_emotions(messages, loaded_model)
    return jsonify({"emotions": emotions})


if __name__ == '__main__':
    app.run(debug=True)
