from sentiment_model.emotion_detection import preprocess, encoding, Glove, enc
import numpy as np


def predict_emotions(user_messages, loaded_model):
    emotion = []
    for msg in user_messages:
        text = preprocess(msg)
        text = encoding(text, Glove)
        text = np.array(text)
        sentiment = loaded_model.predict(text)[0]
        label = np.argmax(sentiment)
        emotion.append(enc.categories_[0][label])
    return emotion