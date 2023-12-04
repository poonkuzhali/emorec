import pickle
import re

from flask import jsonify
from keras.src.utils import pad_sequences
import numpy as np


def get_emotions(loaded_model, userMessages):
    with open(r"./sentiment_model/labelEncoder.pickle", "rb") as input_file:
        le = pickle.load(input_file)
    with open(r"./sentiment_model/tokenizer.pickle", "rb") as input_file:
        tokenizer = pickle.load(input_file)

    sentence = ' '.join(userMessages)
    print(sentence)
    sentence = clean(sentence)
    sentence = tokenizer.texts_to_sequences([sentence])
    sentence = pad_sequences(sentence, maxlen=256, truncating='pre')
    result = le.inverse_transform(np.argmax(loaded_model.predict(sentence), axis=-1))[0]
    proba = np.max(loaded_model.predict(sentence))
    print(f"{result} : {proba}\n\n")
    return jsonify({"emotions": result})

def clean(text):
    text = re.sub(r'[^a-zA-Z ]', '', text)
    text = text.lower()
    return text