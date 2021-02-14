import nltk
from nltk.stem.lancaster import LancasterStemmer
from tensorflow.python.framework import ops
stemmer = LancasterStemmer()

import numpy
# -*- coding: utf-8 -*-
import tflearn
import tensorflow
import random
import json
import pickle
import ipdb
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('volume', 3.0)

with open("data/intents.json", 'r', encoding='utf8') as file:
    data = json.load(file)

try:
    with open("data/training/data.pickle", "rb") as f:
        words, labels, training, output = pickle.load()
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open("data/training/data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

ops.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model_file = open("data/training/model.tflearn.index")
    model_file.close()
    model.load("data/training/model.tflearn")
except FileNotFoundError:
    model.fit(training, output, n_epoch=2000, batch_size=8, show_metric=True)
    model.save("data/training/model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w== se:
                bag[i] = 1
    
    return numpy.array(bag)

def conversation(text):
    results = model.predict([bag_of_words(text, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    if results[results_index] > 0.5:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        response = random.choice(responses)
        return {"response": response,
        "tag": tag}
    else: 
        responses = ['não entendi o que você disse', 'isso não me diz nada', 'sinceramente?. Não entendi']
        return {"response": random.choice(responses),
        "tag": "não entendeu"}
