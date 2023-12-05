# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 00:31:31 2022

@author: ozmen
"""


def convolution(image, conv):
    """
    full padding with 0's, stride 1, normalizes processed image to 0-255 range
    image is list of lists of integers with rectangular shape, 
    conv is list of lists of integers with odd x odd rectangular shape
    returns processed image which has the same shape as (original) image
    """
    rows = len(image)
    columns = len(image[0])
    conv_size = len(conv)
    n = conv_size // 2
    processed = [[] for _ in image]
    for row in range(rows):
        for column in range(columns):
            conv_sum = 0.0
            for i in range(-n, n + 1):
                for j in range(-n, n + 1):
                    conv_sum += conv[i+n][j+n] * (image[row+i][column+j] if
                                                  (row+i>=0 and row+i<rows
                                                   and column+j>=0 and 
                                                   column+j<columns) else 0)
            if(row == 0 and column == 0):
                min_intensity = max_intensity = conv_sum
            else:
                min_intensity = conv_sum if conv_sum<min_intensity\
                                         else min_intensity
                max_intensity = conv_sum if conv_sum>max_intensity\
                                         else max_intensity                     
                
            processed[row].append(conv_sum)        
    intensity_range = max_intensity - min_intensity
    for row in range(len(processed)):
        for column in range(len(processed[0])):
            processed[row][column] = (processed[row][column] - min_intensity)\
                                     / (intensity_range if intensity_range!=0 
                                        else 1) * 255 // 1
    return processed

# image1 = [[1,3,4,5,6,1],[22,33,11,55,44,22],[234,123,111,235,11,22],
#           [12,31,155,125,2,33]]
# conv1 = [[1,1,1],[1,1,1],[1,1,1]]
# print(convolution(image1, conv1))                                 
                                     
