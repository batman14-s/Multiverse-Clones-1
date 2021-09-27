from keras.models import load_model
import cv2
import numpy as np

def getCorrectClass(tmpClass,classMap):
  for key, value in classMap.items():
         if value == tmpClass:
             return key

model = load_model("WrongDataModel.h5")
classMap = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, 'EQUALS':6, 'NONE':7, 'PLUS':8}
cap = cv2.VideoCapture(0)
prev_move = None
while True:
    ret, frame = cap.read()
    if not ret:
        continue
    # rectangle for user to play
    cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)
    # extract the region of image within the user rectangle
    roi = frame[100:500, 100:500]
    # img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img2 = cv2.Canny(roi, 50, 80)
    imageSize = 100
    img = cv2.resize(img2, (imageSize, imageSize))
    # predict the move made
  
    pred = model.predict(img.reshape(1, img.shape[0], img.shape[1], 1))
    pred_cls = np.argmax(pred)
    symbol= getCorrectClass(pred_cls,classMap)
    print(symbol)

    # display the information
    font=cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img2, " outcome: " + str(symbol),
                (imageSize, imageSize), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
   
    cv2.imshow('frame', img2)

    k=cv2.waitKey(10)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()