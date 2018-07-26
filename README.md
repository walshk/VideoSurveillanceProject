# VideoSurveillanceProject
Predictive Analytics Mini-Project 3

By:
+ Min A
+ Ben Dantowitz
+ Kevin Walsh

## Requirements
Anaconda (Python 3.6 version)

## Errors you may run into
The module will not function properly if:
+ You don't have a webcam attached to your computer
+ The module attempts to send an email without having a new client_secret.json file saved

## Workarounds
You can get around the webcam requirement by changing the parameter passed into VideoCapture() on line 37 of video_module.py from 0 to 'testvideo_long.mp4' or 'testvideo_short.mp4'.
