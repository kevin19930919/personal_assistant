import random
import json
import torch
import sys
sys.path.append('/data2/kevin7552/personal_assistant/fastapi/core/neuralintents')
from model import NeuralNet
from nltk_modules import bag_of_words, tokenize

from AIDMS_module import AIDMSHandler
from week_report import WeekReport


#=========responese function==================
def send_mail():
    Filepath = input("what file you want to attach?(abs path plz)")
    WeekReport.send_mail(Filepath)

def stop_apache_server():
    pop = subprocess.Popen('sudo service apache2 stop',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = pop.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    if stderr:
        print(f'stop apache2 fail: {stderr}')
        return False
    else:
        print('stop apache server success')
        return True    

def mount_AIDMS_db():
    AIDMSHandler.mount_AIDMS_db_impl()




class Assisant():

    intent_methods = {
    'send_mail':send_mail,
    'mount_AIDMS_db':mount_AIDMS_db
    }

    weight = torch.load('/data2/kevin7552/personal_assistant/fastapi/core/neuralintents/data.pth')
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
    
    @classmethod
    def get_response(cls, ints, intents_json):
        try:
            tag = ints[0]['intent']
            list_of_intents = intents_json['intents']
            for i in list_of_intents:
                if i['tag']  == tag:
                    result = random.choice(i['responses'])
                    break
        except IndexError:
            result = "I don't understand!"

    
    @classmethod    
    def request(cls, sentence):
        sentence = cls.cleanup_sentence(sentence)
        inputs = cls.load_input(sentence)
        response = cls.predict_response(inputs)
        if response in cls.intent_methods.keys():
            cls.intent_methods[response]()
            return f'operation {response} successfully done'
        else:
            return "I dont't know what's your intents"


