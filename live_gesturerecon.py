from keras.models import load_model
import cv2
import numpy as np
from datetime import datetime
from scipy import stats
import pyttsx3


def getTime():
    time = datetime.now().hour * 3600 + datetime.now().minute * 60 + datetime.now().second + datetime.now().microsecond / 1000000
    return time


def getCorrectClass(tmpClass, classMap):
    for key, value in classMap.items():
        if value == tmpClass:
            return key


def getCannyImage(img, lowI, highI):
    return cv2.Canny(img, lowI, highI)


def keyCheck():
    k = cv2.waitKey(10)
    if k == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit()
    if k == ord('p'):
        while True:
            k = cv2.waitKey(1)
            if k == ord('c'):
                return


def speak(a):
    textspeech = pyttsx3.init()
    speak = a
    textspeech.say(speak)
    textspeech.runAndWait()


def predict(frame):
    cannyImage = getCannyImage(frame[ytop:ybottom, xleft:xright], lowIntensity, highIntensity)
    predImage = cv2.resize(cannyImage, (imageSize, imageSize))
    pred = model.predict(predImage.reshape(1, predImage.shape[0], predImage.shape[1], 1))
    pred_cls = np.argmax(pred)
    value = getCorrectClass(pred_cls, classMap)
    return cannyImage, value


model = load_model("UltimateUltimateHeaven.h5")

classMap = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, 'EQUALS': 6, 'NONE': 7, 'SUM': 8}
imageSize = 100
coord = [[50, 300], [100, 400]]
white = (255, 255, 255)
red = (0,0,255)
rectangleThickness = fontThickness = 2
timeRemainingPosition = (10, 80)
outcomePosition = (30, 80)
font = cv2.FONT_HERSHEY_SIMPLEX
value = 'NONE'

orders = []
orderMenu = {'1': 'karela', '2': 'khichdi', '3': 'tinde', '4': 'tori', '5': 'ghiya'}

lowIntensity = 50
highIntensity = 100

waitTime = 2
resultCalculationTime = 2
displayResultTime = 2

cap = cv2.VideoCapture(0)
while True:
    xleft = coord[0][0]
    xright = coord[0][1]
    ytop = coord[1][0]
    ybottom = coord[1][1]
    ret, frame = cap.read()
    if ret:
        # waiting for selection to begin
        ptime = getTime()
        while (getTime() - ptime < waitTime):
            ret, frame = cap.read()
            if ret:
                timeRemaining = round(waitTime - getTime() + ptime, 1)
                if (timeRemaining <= 0):
                    timeRemaining = 0
                cv2.rectangle(frame, (xleft, ytop), (xright, ybottom), white, rectangleThickness)
                cv2.rectangle(frame, (xleft+40, ytop+30), (xright-40, ybottom-30), red, rectangleThickness)
                cv2.putText(frame, " Capturing in: " + str(timeRemaining), timeRemainingPosition, font, 1.2, white,
                            fontThickness, cv2.LINE_AA)
                cv2.imshow('frame', frame)
                keyCheck()

        # getting selection
        ptime = getTime()
        order = []
        while (getTime() - ptime < resultCalculationTime):
            ret, frame = cap.read()
            if ret:
                # predict the move made
                cannyImage, value = predict(frame)
                order.append(value)
                cv2.rectangle(frame, (xleft, ytop), (xright, ybottom), white, rectangleThickness)
                cv2.rectangle(frame, (xleft+40, ytop+30), (xright-40, ybottom-30), red, rectangleThickness)
                cv2.putText(frame, "Finding Outcome", outcomePosition, font, 1.2, white, fontThickness, cv2.LINE_AA)
                cv2.imshow('frame', frame)
                keyCheck()
        order = stats.mode(np.array(order))[0][0]
        speak(order)

        # displaying selectiong
        ptime = getTime()
        while (getTime() - ptime < displayResultTime):
            ret, frame = cap.read()
            if ret:
                # predict the move made
                cv2.rectangle(frame, (xleft, ytop), (xright, ybottom), white, rectangleThickness)
                cv2.putText(frame, " Outcome: " + str(order), outcomePosition, font, 1.2, white, fontThickness,
                            cv2.LINE_AA)
                cv2.imshow('frame', frame)
                keyCheck()

    if (order == 'SUM'):
        print('Total no of orders are:', len(orders))
        print("Orders are:", orders)
    elif(order == 'EQUALS'):
        print("Orders are:", orders)
        print('Order placed')
        cap.release()
        cv2.destroyAllWindows()
        exit()
    elif order == '0':
        orders = orders[:len(orders) - 1]
    elif order != 'NONE':
        orders.append(orderMenu[order])

    keyCheck()
    speak(orders)