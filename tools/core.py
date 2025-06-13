import json
import os
import numpy as np

for file in os.listdir('tools'):
    
    if "LogisticRegression" in file:
        with open(os.path.join('tools', file), 'r') as params:
            logreg_params = json.load(params)

    if "MinMaxScaler" in file:
        with open(os.path.join('tools', file), 'r') as params:
            minmax_params = json.load(params)

        break

class MinMaxScalerInference:
    
    def __init__(self):
        
        self.min = np.array(minmax_params['min'])
        self.max = np.array(minmax_params['max'])
        self.feature_range = minmax_params['feature_range']

    def transform(self, X):
        
        X = np.array(X)
        scale = self.feature_range[1] - self.feature_range[0]
        X_std = (X - self.min) / (self.max - self.min)
        
        return self.feature_range[0] + X_std * scale

    def inverse_transform(self, X_scaled):
        
        X_scaled = np.array(X_scaled)
        scale = self.feature_range[1] - self.feature_range[0]
        X_std = (X_scaled - self.feature_range[0]) / scale
        
        return X_std * (self.max - self.min) + self.min

class LogisticRegressionInference:
    
    def __init__(self):
        
        self.learning_rate = logreg_params['learning_rate']
        self.weights = np.array(logreg_params['weights'])
        self.bias = np.array(logreg_params['bias'])

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def predict(self, X):
        
        model = np.dot(X, self.weights) + self.bias
        predictions = self.sigmoid(model)
        return (predictions >= 0.5).astype(int), predictions