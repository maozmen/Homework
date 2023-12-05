# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 09:06:38 2023

@author: ozmen
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay
from matplotlib import pyplot as plt

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def logistic_regression(inputs, targets, lr = 0.1, max_epoch = 10000,
                        precision = 0.001):
    targets = targets.swapaxes(0, 1)
    inputs = np.append(inputs, np.ones((inputs.shape[0],1)), axis = 1)
    weights = np.random.random_sample((targets.shape[0], inputs.shape[-1]))
    outputs = np.ones((targets.shape[0], inputs.shape[0]))
    deltas = np.zeros((targets.shape[0], inputs.shape[-1]))
    for i in range(max_epoch):
        
        for i in range(targets.shape[0]):
            outputs[i] = sigmoid(np.dot(inputs, weights[i]))
        
        for i in range(3):
            deltas[i] = -(np.dot((1 - outputs[i]) * targets[i],  inputs) +\
                np.dot(-outputs[i] * (1 - targets[i]), inputs)) / inputs.shape[-1]
        weights -= deltas * lr
    return np.argmax(outputs.swapaxes(0, 1), axis = 1), weights

def lr_predict(inputs, weights):
    inputs = np.append(inputs, np.ones((inputs.shape[0],1)), axis = 1)
    outputs = np.empty((weights.shape[0], inputs.shape[0]))
    for i in range(weights.shape[0]):
        outputs[i] = sigmoid(np.dot(inputs, weights[i]))
    return np.argmax(outputs.swapaxes(0, 1), axis = 1)

def confusion_matrix(y_true, y_pred):
    shape = max(max(y_true), max(y_pred)) + 1
    
    cm = np.zeros((shape, shape))
    
    for i in range(y_true.shape[0]):
        cm[y_true[i], y_pred[i]] += 1
    
    return cm

data = pd.read_csv("penguins_size.csv")
data = data.dropna()

data_x = data.iloc[:, 1:]
data_y = data.iloc[:, :1]
data_y = pd.get_dummies(data_y)
dummies = pd.get_dummies(data_x.iloc[:, [0,5]])

data_x = data_x.iloc[:, 1:5]
data_x = pd.concat([data_x, dummies], axis = 1)

x_train, x_test, y_train, y_test = train_test_split(data_x, data_y,\
                                                    train_size = 0.7,
                                                    random_state = 0)

min_ = x_train.min()
max_ = x_train.max()

x_train = (x_train - min_)/(max_ - min_)
x_test = (x_test - min_)/(max_ - min_)

x_train = x_train.to_numpy()
x_test = x_test.to_numpy()
y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

outputs, weights = logistic_regression(x_train, y_train, max_epoch = 15000)

outputs_test = lr_predict(x_test, weights)

y_test_dense = np.argmax(y_test, axis = 1)
cm = confusion_matrix(y_test_dense, outputs_test)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(colorbar = True)
plt.xticks(ticks = [0,1,2], labels = ['Adelie', 'Chinstrap', 'Gentoo'])
plt.yticks(ticks = [0,1,2], labels = ['Adelie', 'Chinstrap', 'Gentoo'])
plt.tick_params(axis = 'both', bottom = False, left = False, labeltop = True,
                labelbottom = False)
plt.show()






