import numpy as np
import cv2
from addToAlertLog import addLog
import datetime

cap = cv2.VideoCapture(1)


counter = 0
while(True):
    # capture frame-by-frame
    ret, frame = cap.read()

    # operate on frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if counter == 0:
        brightness = gray.mean()
        print('Brightness: ', brightness / 255)
        
        if brightness < 0.30:
            now = datetime.datetime.now()
            logMsg = "{0}:{1}:{2} -- Low Lighting Warning".format(now.hour,now.minute,now.second)

            addLog(logMsg)


    if counter >= 120:
        counter = -1
    
    counter = counter + 1

    # display frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# when done, release capture
cap.release()
cv2.destroyAllWindows()
