import numpy as np
import cv2
from addToAlertLog import addLog
import datetime
import emailAlert


def matrix_similarity(a,b):
	c = a == b
	c = c.flatten()
	truths = 0
	for booly in c:
		if booly:
			truths += 1
	return truths / len(c)


# BEGIN VIDEO CAPTURE
try:
	cap = cv2.VideoCapture('videoplayback.mp4')  # CHOOSE VIDEO SOURCE

	counter_brightness = 0
	
	counter_freeze = 0
	freeze_test_img = []
	
	counter_pov = 0
	corners = {'top_left': [], 'bottom_left': [],
		'top_right': [], 'bottom_right': []}

	# Capture loop
	while(True):
	    # capture frame-by-frame
	    ret, frame = cap.read()

	    # operate on frame
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    h = gray.shape[1]
	    v = gray.shape[0]

	    cv2.rectangle(gray, (0,0), (40,40), 255, 3)
	    cv2.rectangle(gray, (h,0), (h - 40,40), 255, 3)
	    cv2.rectangle(gray, (0,v - 40), (40,v), 255, 3)
	    cv2.rectangle(gray, (h,v - 40), (h - 40, v), 255, 3)

	    counter_brightness += 1

	    # LOW LIGHTING DETECTION
	    if counter_brightness == 0:
	        # calculate mean brightness
	        brightness = gray.mean() / 255  # make it a percentage
	        #print('Brightness: ', brightness)
	 
	        if brightness < 0.250:
	            # add alert message to alert log for the day
	            now = datetime.datetime.now()
	            # alert the user
	            logMsg = """{0:02d}:{1:02d}:{2:02d} -- Low Lighting Warning""".format(now.hour,now.minute,now.second)
	            addLog(logMsg)


	    if counter_brightness >= 120:
	        counter_brightness = -1
	    
	    

	    # FROZEN VIDEO FEED DETECTION
	    if counter_freeze == 0:
	        if len(freeze_test_img) > 0:
	            same_frame = np.all(gray == freeze_test_img[-1])
	            similarity = matrix_similarity(gray, freeze_test_img[-1])
	            
	            # test for 85% similarity between images 4 seconds apart
	            if similarity > 0.85:
	                now = datetime.datetime.now()
	                # alert the user
	                logMsg = "{0:02d}:{1:02d}:{2:02d} -- Video May Be Frozen".format(now.hour,now.minute,now.second)
	                addLog(logMsg)

	        freeze_test_img.append(gray)
	   
	    if counter_freeze >= 120:
	        counter_freeze = -1
	    if len(freeze_test_img) > 5:
	        freeze_test_img = []
	        
	    counter_freeze += 1



	    # DETECT LARGE DIFFERENCES IN CORNER VALUES
	    counter_pov += 1

	    if counter_pov == 0:
	    	top_left = frame[0:40][0:40]
	    	bottom_left = frame[0:40][-40:]
	    	top_right = frame[-40:][0:40]
	    	bottom_right = frame[-40:][-40:]
	    	if len(corners['top_left']) > 0:
	    		tl_diff = matrix_similarity(top_left, corners['top_left'][-1])
	    		tr_diff = matrix_similarity(top_right, corners['top_right'][-1])
	    		bl_diff = matrix_similarity(bottom_left, corners['bottom_left'][-1])
	    		br_diff = matrix_similarity(bottom_right, corners['bottom_right'][-1])
	    		
	    		closest = max([tl_diff, tr_diff, bl_diff, br_diff])
	    		if closest < 0.025:
	    			now = datetime.datetime.now()
	    			logMsg = "{0:02d}:{1:02d}:{2:02d} -- Camera May Have Been Moved".format(now.hour,now.minute,now.second)
	    			addLog(logMsg)

	    	corners['top_left'].append(top_left)
	    	corners['top_right'].append(top_right)
	    	corners['bottom_left'].append(bottom_left)
	    	corners['bottom_right'].append(bottom_right)

	    if counter_pov >= 120:
	    	counter_pov = -1
	    if len(corners['top_left']) > 5:
	    	corners['top_left'] = []
	    	corners['top_right'] = []
	    	corners['bottom_left'] = []
	    	corners['bottom_right'] = []




	    # display frame
	    cv2.imshow('Video Surveillance System', gray)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	    elif cv2.waitKey(1) & 0xFF == ord('s'):
		    subject = "Alert Log for {0}/{1}/{2}".format(now.month, now.day, now.year)
		    f = open("AlertLog_{2}_{1}_{0}.txt".format(now.day, now.month, now.year), 'r')
		    msg = f.read()
		    emailAlert.SendAlert('kevinwalsh322@gmail.com', subject, msg)

	# when done, release capture
	cap.release()
	cv2.destroyAllWindows()

except(cv2.error):
	print("OpenCV Error Encountered - System Shutdown")
	
	# Alert the user here
	now = datetime.datetime.now()
	logMsg = "{0:02d}:{1:02d}:{2:02d} -- Camera Connection Shutdown".format(now.hour, now.minute, now.second)
	addLog(logMsg)

	subject = "Alert Log for {0}/{1}/{2}".format(now.month, now.day, now.year)

	f = open("AlertLog_{2}_{1}_{0}.txt".format(now.day, now.month, now.year))
	msg = f.read()
	emailAlert.SendAlert('kevinwalsh322@gmail.com', subject, msg)

	exit(1)