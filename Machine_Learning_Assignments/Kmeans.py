# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:29:46 2023

@author: ozmen
"""
import numpy as np
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay
from matplotlib import pyplot as plt

np.random.seed(0)

def k_means(inputs, k = 10, dist_func = lambda x, y: np.sum((x-y)**2, axis = 1),
            iterations = 100):
    def allocate(input_, centroids):
        return np.argmin(dist_func(input_, centroids))
    
    centroids = np.random.random_sample((k, inputs.shape[1]))
    allocation = np.empty(inputs.shape[0])
    changed = True
    while(changed and iterations > 0):
        changed = False
        
        for i, input_ in enumerate(inputs):
            allocation[i] = allocate(input_, centroids)
        for i in range(k):
            centroid = np.average(inputs[allocation == i])
            if np.any(centroids[i] != centroid):
                centroids[i] = centroid
                changed = True
        iterations -= 1

    return allocation.astype('int32')

def confusion_matrix(y_true, y_pred):
    shape = max(y_true) + 1
    
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

min_ = data_x.min()
max_ = data_x.max()
data_x = (data_x - min_)/(max_ - min_)

data_x = data_x.to_numpy()
data_y = data_y.to_numpy()
allocations = k_means(data_x, k = 3)

data_y_dense = np.argmax(data_y, axis = 1)
cm = confusion_matrix(data_y_dense, allocations)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(colorbar = True)
plt.xticks(ticks = [0,1,2], labels = ['Küme 1', 'Küme 2', 'Küme 3'])
plt.yticks(ticks = [0,1,2], labels = ['Adelie', 'Chinstrap', 'Gentoo'])
plt.tick_params(axis = 'both', bottom = False, left = False, labeltop = True,
                labelbottom = False)
plt.show()






    

