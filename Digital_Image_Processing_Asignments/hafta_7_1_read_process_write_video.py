# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 03:32:31 2023

@author: ozmen
"""
import numpy as np
import cv2 as cv

VIDEO = "Road_Video_1.webm"
FRAMES_PROC = 50
TYPES = ["momentum", "mean"]
TYPE = TYPES[1]


cap = cv.VideoCapture(VIDEO)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

n = 0    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # break
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    frame = cv.resize(frame, (frame.shape[1]//3, frame.shape[0]//3))
        
    if TYPE == 'mean':
        if n == 0:
            frames = np.zeros((FRAMES_PROC, *frame.shape), dtype = np.uint8)
            fourcc = cv.VideoWriter_fourcc(*'MJPG')
            out = cv.VideoWriter('mean.avi', fourcc, 
                                 cap.get(cv.CAP_PROP_FPS), frame.T.shape[1:])
            mean = np.zeros_like(frame, dtype=np.float32)
            
        
        mean = mean + frame / FRAMES_PROC
        mean = mean - frames[n%FRAMES_PROC] / FRAMES_PROC
        frames[n%FRAMES_PROC] = frame
        frame = mean.astype(np.uint8)
    elif TYPE == 'momentum':
        if n == 0:
            momentum = frame
            fourcc = cv.VideoWriter_fourcc(*'MJPG')
            out = cv.VideoWriter('momentum.avi', fourcc, 
                                 cap.get(cv.CAP_PROP_FPS), frame.T.shape[1:])
        else:
            momentum = momentum*(FRAMES_PROC-1)/FRAMES_PROC + frame/FRAMES_PROC
            frame = momentum.astype(np.uint8)
    
    n += 1
    # if n < FRAMES_PROC:
    #     continue
    # if n == 10000:
    #     break
    
    out.write(frame)
    
    # Display the resulting frame
    # cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
out.release()
cv.destroyAllWindows()












