import json
from nltk_modules import *
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from model import NeuralNet


#========================dataset module=======================
class CommunicateDataset(Dataset):

    def __init__(self, trainData, trainLable):
        self.numSamples = len(trainData)
        self.trainData = trainData
        self.trainLable = trainLable

    def __getitem__(self, index):
        return self.trainData[index], self.trainLable[index]

    def __len__(self):
        return self.numSamples


#===================main function===========================
with open('intents.json', 'r') as f:
    intents = json.load(f)

all_words = []
tags = []
dataPair=[]
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)

    for pattern in intent['patterns']:
        words = tokenize(pattern)
        all_words.extend(words)
        dataPair.append((words, tag))

ignore_words = ['?', '!', '.', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words =sorted(set(all_words))
tags = sorted(set(tags))

trainData = []
trainLabel = []
for (patternSentence, tag) in dataPair:
    bag = bag_of_words(patternSentence, all_words)
    trainData.append(bag)
    label = tags.index(tag)
    #crossentropy loss
    trainLabel.append(label)

trainData = np.array(trainData)
trainLabel = np.array(trainLabel)

batchSize = 8
inputSize = len(trainData[0])
hiddenSize = 8
outputSize = len(tags)
learningRate = .001
numEpochs = 100
recordStep = numEpochs/10

dataSet = CommunicateDataset(trainData, trainLabel)
trainLoader = DataLoader(dataset=dataSet, batch_size=batchSize, shuffle=True, num_workers=2)

device = torch.device('cuda:0')
model = NeuralNet(inputSize, hiddenSize, outputSize).to(device)

#loss & optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learningRate)

for epoch in range(numEpochs):
    for (words, labels) in trainLoader:
        words = words.to(device)
        labels = labels.to(device)

        #forward
        outputs = model(words)
        loss = criterion(outputs, labels)

        #backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % recordStep == 0:
        print(f'epoch {epoch+1}/{numEpochs}, loss={loss.item():.4f}')

print(f'Finial loss : {loss.item():.4f}')

data = {
    'model_state': model.state_dict(),
    'input_size': inputSize,
    'output_size': outputSize,
    'hidden_size': hiddenSize,
    'all_words': all_words,
    'tags': tags
}

FILE = 'data.pth'
torch.save(data, FILE)

print(f'training complete. file save to {FILE}')

