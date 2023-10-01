from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = Flask(__name__)

bot = ChatBot('EmotionBot')

trainer = ListTrainer(bot)

emotion_questions = [
    "How are you feeling right now?",
    "Can you tell me more about what's bothering you?",
    "What emotions are you experiencing?",
    "When did you start feeling this way?",
    "Is there something specific that triggered these emotions?",
]

trainer.train(emotion_questions)

current_question_index = 0

@app.route('/')
def index():
    return render_template('index.html', initial_question=emotion_questions[current_question_index])

@app.route('/get')
def get_bot_response():
    global current_question_index
    user_message = request.args.get('msg')
    bot_response = ""

    if user_message.lower() == 'exit'.lower():
        bot_response = "Thank you for chatting with me. Have a great day!"
    else:
        current_question_index += 1
        if current_question_index < len(emotion_questions):
            bot_response = emotion_questions[current_question_index]
        else:
            bot_response = "Thank you for sharing your feelings. If you have more to talk about, feel free to let me know."


    return bot_response

if __name__ == '__main__':
    app.run(debug=True)
