##Great gentle introduction
#https://pythonprogramming.net/drawing-writing-python-opencv-tutorial/?completed=/loading-video-python-opencv-tutorial/

##Serious mathematics and image loading/facial recognition theory and application:
## Definitely study the below. Huge read though.
#https://docs.opencv.org/2.4/modules/contrib/doc/facerec/facerec_tutorial.html#introduction

## Nice Explanation of OpenCV
## START HERE. The "Haar Cascade" part is particularly pertinent
# https://www.datacamp.com/community/tutorials/face-detection-python-opencv#images-as-arrays

import cv2
cap = cv2.VideoCapture('http://192.168.1.157:8090/?action=stream/frame.mjpg')
#cap = cv2.VideoCapture(0) ## to use your webcam instead of stream

while True:
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('Anything',gray)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()