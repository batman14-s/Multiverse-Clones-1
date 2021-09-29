from keras.models import load_model
import cv2
import numpy as np
from datetime import datetime
from scipy import stats
import pyttsx3


def speak(a):
    textspeech = pyttsx3.init()
    speak = a
    textspeech.say(speak)
    textspeech.runAndWait()


def getTime():
    time = datetime.now().hour * 3600 + datetime.now().minute * 60 + \
        datetime.now().second + datetime.now().microsecond / 1000000
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


def predict(frame):
    cannyImage = getCannyImage(
        frame[ytop:ybottom, xleft:xright], lowIntensity, highIntensity)
    predImage = cv2.resize(cannyImage, (imageSize, imageSize))
    pred = model.predict(predImage.reshape(
        1, predImage.shape[0], predImage.shape[1], 1))
    pred_cls = np.argmax(pred)
    value = getCorrectClass(pred_cls, classMap)
    return cannyImage, value


def addDisplayImage(frame, displayImage):
    img = cv2.imread('./MenuImages/' + displayImage + '.png')
    img = cv2.resize(img, (xright-xleft, ybottom-ytop),
                     interpolation=cv2.INTER_AREA)
    frame[ytop:ybottom, xleft+300:xright+300] = img
    return frame


def waiting(displayImage):
    ptime = getTime()
    while (getTime() - ptime < waitTime):
        ret, frame = cap.read()
        if ret:
            timeRemaining = round(waitTime - getTime() + ptime, 1)
            if (timeRemaining <= 0):
                timeRemaining = 0
            cv2.rectangle(frame, (xleft, ytop), (xright, ybottom),
                          white, rectangleThickness)
            cv2.rectangle(frame, (xleft + 40, ytop + 30),
                          (xright - 40, ybottom - 30), red, rectangleThickness)
            cv2.putText(frame, " Capturing in: " + str(timeRemaining), timeRemainingPosition, font, 1.2, white,
                        fontThickness, cv2.LINE_AA)
            frame = addDisplayImage(frame, displayImage)
            cv2.imshow('frame', frame)
        keyCheck()


def getSelection(displayImage):
    ptime = getTime()
    order = []
    while (getTime() - ptime < resultCalculationTime):
        ret, frame = cap.read()
        if ret:
            # predict the move made
            cannyImage, value = predict(frame)
            order.append(value)
            cv2.rectangle(frame, (xleft, ytop), (xright, ybottom),
                          white, rectangleThickness)
            cv2.rectangle(frame, (xleft + 40, ytop + 30),
                          (xright - 40, ybottom - 30), red, rectangleThickness)
            cv2.putText(frame, "Finding Outcome", outcomePosition,
                        font, 1.2, white, fontThickness, cv2.LINE_AA)
            frame = addDisplayImage(frame, displayImage)
            cv2.imshow('frame', frame)
        keyCheck()
    return stats.mode(np.array(order))[0][0]


def display(order, orders, displayImage, showImage, showOrder):
    ptime = getTime()
    printedOrder = False
    while (getTime() - ptime < displayResultTime):
        ret, frame = cap.read()
        if ret:
            # predict the move made
            cv2.rectangle(frame, (xleft, ytop), (xright, ybottom),
                          white, rectangleThickness)
            cv2.putText(frame, " Outcome: " + str(order), outcomePosition,
                        font, 1.2, white, fontThickness, cv2.LINE_AA)
            if showImage == True:
                frame = addDisplayImage(frame, displayImage)
                # pass
            elif showOrder == True:
                if printedOrder == False:
                    print(orders)
                    printedOrder = True
                # cv2.putText(frame, "Final items Purchased: ", str(orders),
                            # (100, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            keyCheck()


def placeOrder(order, displayImage):
    Salad = {'1': 'Veggie Salad', '2': 'Avocado salad',
             '3': 'Corn salad', '4': 'Pasta salad', '5': 'Fruit salad'}
    Starters = {'1': 'French fries', '2': 'Soup',
                '3': 'Donuts', '4': 'Pasta', '5': 'Onion rings'}
    MainCourse = {'1': 'Dal makhani', '2': 'Rajma chawal', '3': 'Shahi paneer', '4': 'Stuffed mushrooms',
                  '5': 'Aaloo gobhi'}
    Desserts = {'1': 'Chocalate moose cake', '2': 'Ice cream', '3': 'Blueberry cheesecake', '4': 'Nutella waffle',
                '5': 'Strawberry cupcake'}
    ShakesAndDrinks = {'1': 'Chocalate milkshake', '2': 'Banana milkshake', '3': 'Strawberry milkshake',
                       '4': 'Strawberry milkshake', '5': 'Vanilla shake'}
    if displayImage == 'Salad':
        return Salad[order]
    elif displayImage == 'Starters':
        return Starters[order]
    elif displayImage == 'Main Course':
        return MainCourse[order]
    elif displayImage == 'Desserts':
        return Desserts[order]
    return ShakesAndDrinks[order]


def logicToDisplay(order, orders, displayImage):
    if order == 'NONE':
        display(order, orders, displayImage, True, False)
    elif order == 'EQUALS' or order == 'SUM' or order == '0':
        if order == '0' and len(orders) != 0:
            orders = orders[:len(orders) - 1]
        display(order, orders, displayImage, False, True)
        displayImage = "Menu"
        if order == 'EQUALS':
            cap.release()
            cv2.destroyAllWindows()
            exit()
    elif displayImage == 'Menu':
        display(order, orders, displayImage, False, False)
        displayImage = Menu[order]
    else:
        display(order, orders, displayImage, False, True)
        orders.append(placeOrder(order, displayImage))
        displayImage = 'Menu'
    return orders, displayImage


model = load_model("UltimateUltimateHeaven.h5")

classMap = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
            '5': 5, 'EQUALS': 6, 'NONE': 7, 'SUM': 8}
imageSize = 100
coord = [[50, 300], [100, 400]]
white = (255, 255, 255)
red = (0, 0, 255)
rectangleThickness = fontThickness = 2
timeRemainingPosition = (10, 80)
outcomePosition = (30, 80)
font = cv2.FONT_HERSHEY_SIMPLEX
value = 'NONE'
displayImage = 'Menu'

orders = []
Menu = {'1': 'Salad', '2': 'Starters', '3': 'Main Course',
        '4': 'Desserts', '5': 'Shakes and Drinks'}

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
        waiting(displayImage)
        order = getSelection(displayImage)
        speak(str(order))
        orders, displayImage = logicToDisplay(order, orders, displayImage)
    keyCheck()
