import random
import json
import torch
import sys
sys.path.append('/data2/kevin7552/personal_assistant/fastapi/core/neuralintents')
from model import NeuralNet
from nltk_modules import bag_of_words, tokenize

class Assisant():
    weight = torch.load('/data2/kevin7552/personal_assistant/fastapi/core/neuralintents/data.pth')
    inputSize = weight['input_size']
    output_size = weight['output_size']
    hiddenSize = weight['hidden_size']
    all_words = weight['all_words']
    tags = weight['tags']
    modelState = weight['model_state']

    def __init__(self, intent_methods={}):
        self.intent_methods = intent_methods
    
    @classmethod
    def load_model(cls):
        cls.device = torch.device('cuda')
        cls.model = NeuralNet(cls.inputSize, cls.hiddenSize, cls.output_size)
        cls.model.load_state_dict(cls.modelState)
        cls.model.to(cls.device)
        cls.model.eval()

    @classmethod
    def load_intents_file(cls):
        with open('/data2/kevin7552/personal_assistant/fastapi/core/neuralintents/intents.json', 'r') as f:
            cls.intents = json.load(f)
    
    @staticmethod
    def cleanup_sentence(sentence):
        return tokenize(sentence)
    
    @classmethod
    def load_input(cls, sentence):
        inputs = bag_of_words(sentence, cls.all_words)
        inputs = inputs.reshape(1, inputs.shape[0])
        inputs = torch.from_numpy(inputs).to(cls.device)
        return inputs
    
    @classmethod
    def predict_response(cls, inputs):
        output = cls.model(inputs)
        _, predicted = torch.max(output, dim=1)
        tag = cls.tags[predicted.item()]
        
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.1:
            for intent in cls.intents['intents']:
                if tag == intent['tag']:
                    print(f'model think {random.choice(intent["responses"])}')
                    return tag

        else:
            print('model does not know')
            return False 
        
    def get_response(self, sentence):
        sentence = self.cleanup_sentence(sentence)
        inputs = self.load_input(sentence)
        response = self.predict_response(inputs)
        if response in self.intent_methods.keys():
            self.intent_methods[response]()
            return f'operation {response} successfully done'
        else:
            return "I dont't know what's your intents"


