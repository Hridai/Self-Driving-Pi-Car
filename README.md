# Self-Driving-Pi-Car
## This is a project to create a self-driving car using a Raspberry Pi 3B and using the libraries **OpenCV** and **face_recognition**. 
### Below we have the instructions on how to set up all the required applications and libraries to ensure that you can compile OpenCV on your RPi.

OpenCV (Open Source Computer Vision Library) is an open source computer vision library and has bindings for C++, Python, and Java. It is has a multitude of applications including medical image analysis, stitching street view images, surveillance video, detecting and recognizing faces, tracking moving objects, extracting 3D models and much more.

In this guide we will be training the car to drive in circles until it detects a labrador. In which case it will drive directly towards it.

### Important note: The Raspberry Pi will not be doing any of the image processing
We will not be limiting ourselves by the processing power of the Raspberry Pi. The raspberry pi will simply feed the image seen by it's camera over wi-fi to a computer by using socket programming. The **TCPClient** class is invaluable for this. Once connected over the LAN, the computer will run the image processor over the video feed and will send back, to the car, the commands to move forward/ or backwards or left or right. This way we are not bound by the RPi's processor.

## Prerequisites
You must have the [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) operating system installed on your Raspberry Pi 3.
Install the openCV libraries in your python environment on your computer. You will **not** need to install this on the Raspberry Pi which is good news as this requires approximately 10 hours of work and some trial and error to get it to work.

## Main Script
Look at Main.py, you can see that we point the script to the video feed we have access to over the WiFi.

```python
cap = cv2.VideoCapture('http://192.168.1.157:8090/?action=stream/frame.mjpg')
```

Make the connection with the raspberry pi over the wifi and flash the lights of the car to give a visual indicator that the script is working and the connection has been successful.
```python
from TCPClient import TCPClient
from cmdline import command
tcp = TCPClient()
cmd = command()
tcp.sendData(cmd.LED_BLUE.encode())
tcp.sendData(cmd.LED_RED.encode())
tcp.sendData(cmd.LED_GREEN.encode())
```

Note: You will need to change the ip address to your IP address that you are connected to over the LAN.
Now you run your classifier over the video feed. It first turns the feed into a greyscale image (however the output you see will still be in colour). If running the haarcascade_eye.xml and the haarcascade_frontalface_default.xml then you will see the squares drawn over your face and your eyes. This is where a neural network trained on images of labradors will be placed.

The below code will send the car forward whenever the camera detects a face. It will cease to move forward if the face is no longer detected. This is the basic theory on how we are going to get the car to move directly towards the dog.

```python
ret, frame = cap.read()
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(gray, 1.3,5)
for (x, y, w, h) in faces:
    cv2.rectangle(frame, (x, ys), (x+w, y+h), (255, 255, 0), 2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = frame[y:y+h, x:x+w]
    eyes = cv2.CascadeClassifier('haarcascade_eye.xml').detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    tcp.sendData(cmd.MOVE_FWD.encode())
cv2.imshow('Anything',frame)
if type(faces) is tuple: # This means no face is detected in this loop
    tcp.sendData(cmd.MOVE_STOP.encode())
```

Note to stop the program running you can just press the q button on the keyboard.

## Further Steps
Complete neural network implementation update to come shortly - Updated by Hridai 12th February 2020
