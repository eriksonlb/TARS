import json
import math
import random
import ipdb


def get_response(text):
    with open("data/intents.json", 'r', encoding='utf8') as file:
        data = json.load(file)
        intents = data['intents']
        bag_words = []
        max_acc = 0
        for intent in intents:
            inputs = intent['patterns']
            tag = intent['tag']
            for input in inputs:
                input_bag = []
                phrase = input.split(" ")
                try:
                    phrase.remove('')
                except:
                    pass
                for word in phrase:
                    input_bag.append(1) if word in text else 0
                value = sum(input_bag)
                n_words = len(text.split(" "))
                accuracy = (value * 100) / n_words
                label = f"{tag} - {input} - {accuracy}%"
                print(label)
                if accuracy > max_acc:
                    max_acc = accuracy
                    response_tag = tag
                    response = intent['responses']
        print(text)
        if max_acc > 41:
            return {"response": random.choice(response),
                    "tag": response_tag}
        else:
            responses = ['não entendi o que você disse', 'isso não me diz nada', 'sinceramente?. Não entendi']
            return {"response": random.choice(responses),
                    "tag": "não entendeu"}
