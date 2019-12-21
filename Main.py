##Great gentle introduction
#https://pythonprogramming.net/drawing-writing-python-opencv-tutorial/?completed=/loading-video-python-opencv-tutorial/

##Serious mathematics and image loading/facial recognition theory and application:
## Definitely study the below. Huge read though.
#https://docs.opencv.org/2.4/modules/contrib/doc/facerec/facerec_tutorial.html#introduction

## Nice Explanation of OpenCV
## START HERE. The "Haar Cascade" part is particularly pertinent
# https://www.datacamp.com/community/tutorials/face-detection-python-opencv#images-as-arrays

# Fire up the raspberry pi, Load up the video feed on it
# Run this script to start the facial recognition

import cv2
from TCPClient import TCPClient

#cap = cv2.VideoCapture('http://192.168.1.157:8090/?action=stream/frame.mjpg')
cap = cv2.VideoCapture(0) ## to use your webcam instead of stream
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
tcp = TCPClient()
bConnected = False
stop_cmd = '>Move Stop'
fwd_cmd = '>Move Forward' + str(50)

try:
    tcp.connectToServer(address = ("192.168.1.157", 12345))
    bConnected = True
    tcp.sendData(">RGB Blue".encode())
    tcp.sendData(">RGB Red".encode())
    tcp.sendData(">RGB Green".encode())
except Exception:
    print("Connect to server Faild!: Check the Server IP is correct and open!")

while bConnected:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3,5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            tcp.sendData(fwd_cmd.encode())
    cv2.imshow('Anything',frame)
    tcp.sendData(stop_cmd.encode())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        tcp.disConnect()
        break

cap.release()
cv2.destroyAllWindows()