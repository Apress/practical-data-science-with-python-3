from collections import OrderedDict

import torch
from torch import nn


class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        self.model = nn.Sequential(OrderedDict([
                ('fc', nn.Linear(input_nodes, hidden_nodes)),
                ('sigmoid', nn.Sigmoid()),
                ('output', nn.Linear(hidden_nodes, output_nodes))]))

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr = learning_rate)
        
    def train(self, features, targets):
        features, targets = features.to(self.device), targets.to(self.device)
        
        self.model.train()
        self.optimizer.zero_grad()        
        output = self.model(features)
        loss = self.criterion(output, targets)
        loss.backward()
        self.optimizer.step()

    def run(self, x):
        self.model.eval()
        with torch.no_grad():
            return self.model(torch.tensor(x.values, dtype = torch.float) \
                       .to(self.device)) \
                       .cpu() \
                       .numpy()
        

#########################################################
# Set your hyperparameters here
##########################################################
iterations = 200
learning_rate = 0.05
hidden_nodes = 20
output_nodes = 1
