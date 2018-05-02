import numpy as np
import cv2
from addToAlertLog import addLog
import datetime

cap = cv2.VideoCapture(0)


counter_brightness = 0
counter_freeze = 0
freeze_test_img = []

# Capture loop

while(True):
    # capture frame-by-frame
    ret, frame = cap.read()

    # operate on frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # LOW LIGHTING DETECTION
    if counter_brightness == 0:
        # calculate mean brightness
        brightness = gray.mean() / 255  # make it a percentage
        print('Brightness: ', brightness)
 
        if brightness < 0.250:
            # add alert message to alert log for the day
            now = datetime.datetime.now()
            logMsg = """{0}:{1}:{2} -- Low Lighting Warning""".format(now.hour,now.minute,now.second)

            addLog(logMsg)


    if counter_brightness >= 120:
        counter_brightness = -1
    
    counter_brightness += 1

    # FROZEN VIDEO FEED DETECTION
    if counter_freeze == 0:
        if len(freeze_test_img) > 0:
            same_frame = np.all(gray == freeze_test_img[-1])
            if same_frame:
                logMsg = "{0}:{1}:{2} -- Video May Be Frozen".format(now.hour,now.minute,now.second)
                addLog(logMsg)

        freeze_test_img.append(gray)
   
    if counter_freeze >= 360:
        counter_freeze = -1
    if len(freeze_test_img) > 5:
        freeze_test_img = []
        

    counter_freeze += 1


    # display frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# when done, release capture
cap.release()
cv2.destroyAllWindows()
