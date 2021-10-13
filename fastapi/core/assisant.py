import random
import json
import torch
import sys
sys.path.append('/data2/kevin7552/personal_assistant/personal_assisant/neuralintents')
from model import NeuralNet
from nltk_modules import bag_of_words, tokenize

class AssisantModel():
    weight = torch.load('/data2/kevin7552/personal_assistant/personal_assisant/neuralintents/data.pth')
    inputSize = weight['input_size']
    output_size = weight['output_size']
    hiddenSize = weight['hidden_size']
    all_words = weight['all_words']
    tags = weight['tags']
    modelState = weight['model_state']

    @classmethod
    def load_model(cls):
        cls.device = torch.device('cuda')
        cls.model = NeuralNet(cls.inputSize, cls.hiddenSize, cls.output_size)
        cls.model.load_state_dict(cls.modelState)
        cls.model.to(cls.device)
        cls.model.eval()

    @classmethod
    def load_intents_file(cls):
        with open('/data2/kevin7552/personal_assistant/personal_assisant/neuralintents/intents.json', 'r') as f:
            cls.intents = json.load(f)
    
    @classmethod
    def get_response(cls, sentence):
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, cls.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(cls.device)

        output = cls.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = cls.tags[predicted.item()]
        
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.5:
            for intent in cls.intents['intents']:
                if tag == intent['tag']:
                    print(f'model think {random.choice(intent["responses"])}')

        else:
            print('model does not know')   





# File = '/data2/kevin7552/personal_assistant/personal_assisant/neuralintents/data.pth'
# data = torch.load(File)

# inputSize = data['input_size']
# output_size = data['output_size']
# hiddenSize = data['hidden_size']
# all_words = data['all_words']
# tags = data['tags']
# modelState = data['model_state']


# device = torch.device('cuda')
# model = NeuralNet(inputSize, hiddenSize, output_size)
# model.load_state_dict(modelState)
# model.to(device)
# model.eval()


# with open('/data2/kevin7552/personal_assistant/personal_assisant/neuralintents/intents.json', 'r') as f:
#     intents = json.load(f)

# while True:
#     sentence = input('command:')
#     if sentence == 'quit':
#         break

#     sentence = tokenize(sentence)
#     X = bag_of_words(sentence, all_words)
#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)

#     output =model(X)
#     _, predicted = torch.max(output, dim=1)
#     tag = tags[predicted.item()]
    
#     probs = torch.softmax(output, dim=1)
#     prob = probs[0][predicted.item()]
#     if prob.item() > 0.5:
#         for intent in intents['intents']:
#             if tag == intent['tag']:
#                 print(f'model think {random.choice(intent["responses"])}')

#     else:
#         print('model does not know')            