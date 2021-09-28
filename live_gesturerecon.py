from keras.models import load_model
import cv2
import numpy as np
import time
from datetime import datetime

def getTime():
    time = datetime.now().hour*3600+datetime.now().minute*60 + datetime.now().second + datetime.now().microsecond/1000000
    return time

def getCorrectClass(tmpClass,classMap):
  for key, value in classMap.items():
         if value == tmpClass:
             return key

def getCannyImage(img,lowI,highI):
    return cv2.Canny(img, lowI, highI)

def keyCheck():
    k=cv2.waitKey(10)
    if k == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit()
    if k == ord('p'):
        while True:
            k = cv2.waitKey(1)
            if k == ord('c'):
                return

def predict(frame):
    cannyImage = getCannyImage(frame[ytop:ybottom, xleft:xright],lowIntensity,highIntensity)
    predImage = cv2.resize(cannyImage, (imageSize, imageSize))
    pred = model.predict(predImage.reshape(1, predImage.shape[0], predImage.shape[1], 1))
    pred_cls = np.argmax(pred)
    value = getCorrectClass(pred_cls,classMap)
    return cannyImage,value

model = load_model("FinalModel.h5")

classMap = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, 'EQUALS':6, 'NONE':7, 'SUM':8}
coord = [[50,300],[100,400]]
white = (255, 255, 255)
rectangleThickness = 2
fontThickness = 2
lowIntensity = 50
highIntensity = 150
imageSize = 100
waitTime = 3
displayResultTime = 2
timeRemainingPosition = (10,80)
outcomePosition = (30,80)
font=cv2.FONT_HERSHEY_SIMPLEX
value = 'NONE'

cap = cv2.VideoCapture(0)
while True:
    xleft = coord[0][0]
    xright = coord[0][1]
    ytop = coord[1][0]
    ybottom = coord[1][1]
    ret, frame = cap.read()
    if ret:
        ptime = getTime()
        while(getTime()-ptime<waitTime):
            ret, frame = cap.read()
            if ret:
                timeRemaining = str(round(waitTime - getTime() + ptime,1))
                
                cv2.rectangle(frame, (xleft, ytop), (xright, ybottom), white, rectangleThickness)
                cv2.putText(frame, " Capturing in: " + timeRemaining ,timeRemainingPosition, font, 1.2, white, fontThickness, cv2.LINE_AA)
                cv2.imshow('frame', frame)
                keyCheck()
        ptime = getTime()
        while(getTime()-ptime<displayResultTime):
            ret, frame = cap.read()
            if ret:
                # predict the move made
                cannyImage , value = predict(frame)
                cv2.rectangle(frame, (xleft, ytop), (xright, ybottom), white, rectangleThickness)
                cv2.putText(frame, " Outcome: " + str(value),outcomePosition, font, 1.2, white, fontThickness, cv2.LINE_AA)
                cv2.imshow('frame', frame)
                keyCheck()
    keyCheck()