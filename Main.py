if __name__ == '__main__':
    import cv2
    from TCPClient import TCPClient
    from cmdline import command
    
    #cap = cv2.VideoCapture('http://192.168.1.157:8090/?action=stream/frame.mjpg')
    cap = cv2.VideoCapture(0) ## to use your webcam instead of stream    
    tcp = TCPClient()
    cmd = command()
    bConnected = False
    
    tcp.sendData(cmd.LED_BLUE.encode())
    tcp.sendData(cmd.LED_RED.encode())
    tcp.sendData(cmd.LED_GREEN.encode())
    
    try:
        tcp.connectToServer(address = ("192.168.1.157", 12345))
        bConnected = True
        #tcp.sendData(">RGB Blue".encode())
    except Exception:
        print("Connect to server Failed!: Check the Server IP is correct and open!")
    
    while bConnected:
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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tcp.disConnect()
            break
    
    cap.release()
    cv2.destroyAllWindows()