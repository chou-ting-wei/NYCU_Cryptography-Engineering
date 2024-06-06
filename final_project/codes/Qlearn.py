import torch
import numpy as np
from collections import OrderedDict, Counter
from purple.machine import Purple97

class DNN(torch.nn.Module):
    def __init__(self, hidden_dims, state_dim, model = None):
        super(DNN, self).__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model
        self.hidden_dims = hidden_dims
        self.state_dim = state_dim
        if(self.model is None):
            layers = OrderedDict()
            last_dim = state_dim
            for i, hidden_dim in enumerate(hidden_dims):
                layers['layer{}'.format(i)] = torch.nn.Linear(last_dim, hidden_dim)
                layers['relu{}'.format(i)] = torch.nn.ReLU()
                last_dim = hidden_dim
            layers['layer{}'.format(i+1)] = torch.nn.Linear(last_dim, state_dim)
            self.model = torch.nn.Sequential(layers).to(self.device)
        else:
            self.model = model.to(self.device)
        self.loss_fn = torch.nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
    def forward(self, x):
        return self.model(x)
    def train(self, x, y, epochs = 100):
        x = torch.tensor(x, dtype=torch.float32).to(self.device)
        y = torch.tensor(y, dtype=torch.float32).to(self.device)
        for epoch in range(epochs):
            y_pred = self.model(x)
            loss = self.loss_fn(y_pred, y)
            if(epoch % 100 == 0):
                print(epoch, loss.item())
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
    def predict(self, x):
        x = torch.tensor(x, dtype=torch.float32).to(self.device)
        return self.model(x).detach().cpu().numpy()
    def save(self, path):
        torch.save(self.model.state_dict(), path)
    def load(self, path):
        self.model.load_state_dict(torch.load(path))
class Transformer(torch.nn.Module):
    def __init__(self, hidden_dims, state_dim, action_dim, model = None):
        super(Transformer, self).__init__()
        self.hidden_dims = hidden_dims
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.embed = torch.nn.Embedding(state_dim, hidden_dims[0])
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        if(model is None):
            self.model = torch.nn.Transformer(d_model=hidden_dims[-1], nhead=1, num_encoder_layers=1, num_decoder_layers=1, dim_feedforward=32, dropout=0.1, activation='relu').to(self.device)
        else:
            self.model = model.to(self.device)
        def forward(self, x):
            x = self.embed(x)
            return self.model(x)
        def train(self, x, y, epochs = 100):
            x = torch.tensor(x, dtype=torch.float32).to(self.device)
            y = torch.tensor(y, dtype=torch.float32).to(self.device)
            for epoch in range(epochs):
                y_pred = self.model(x)
                loss = self.loss_fn(y_pred, y)
                if(epoch % 100 == 0):
                    print(epoch, loss.item())
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
        
        
class QLearning:
    def __init__(self, state_dim, action_dim, hidden_dims = [32, 32], gamma = 0.99, epsilon = 0.1, alpha = 0.1, model = None):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.hidden_dims = hidden_dims
        self.gamma = gamma
        self.epsilon = epsilon
        self.alpha = alpha
        self.q = Transformer(hidden_dims, state_dim, action_dim, model)
    def get_q(self, state):
        return self.q.predict(state)
    def get_action(self, state):
        if(np.random.rand() < self.epsilon):
            return np.random.randint(self.action_dim)
        else:
            return np.argmax(self.get_q(state))
    def update(self, state, action, reward, next_state):
        q = self.get_q(state)
        next_q = self.get_q(next_state)
        q[action] = q[action] + self.alpha * (reward + self.gamma * np.max(next_q) - q[action])
        self.q.train(state, q)
    def save(self, path):
        self.q.save(path)
    def load(self, path):
        self.q.load(path)
    
