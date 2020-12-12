import time
import cv2
import numpy as np



video = cv2.VideoCapture(0)

while True:   
    check , image = video.read()
    image=cv2.resize(image,(640,360))
    roi = image[10:320,50:600]
    
    
    Blackline = cv2.inRange(image , (0,0,0) , (50,50,50))
    kernel = np.ones((3,3), np.uint8)
    Blackline= cv2.erode(Blackline , kernel , 5)
    Blackline = cv2.dilate(Blackline ,kernel ,9)
    contours_blk , hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours_blk) > 0:

        # trouver l'angle à partir de ROTATED RECTANGLE !!!!
        #bound minimum area conseder rotation
        blackbox = cv2.minAreaRect(contours_blk[0])
        (x_min , y_min) , (w_min,h_min), ang = blackbox #les dimension minimum se sont les output de cv2.boundingRect()
        if ang < -45 :
            ang = 90 + ang 
        if w_min < h_min and ang >0:
            ang = (90 - ang) * -1
        if w_min > h_min and ang < 0 :
            ang = 90 + ang
        setpoint = 320
        erreur = int(x_min - setpoint)
        ang = int(ang)
        #to draw this rotated rect we need 4 corners so
        box = cv2.boxPoints(blackbox)
        box = np.int0(box)
        #draw the rotated rect
        cv2.drawContours(image , [box],0,(0,0,255),3)
        cv2.putText(image , str(ang),(10,40),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)
        cv2.putText(image , str(erreur) , (10,320) , cv2.FONT_HERSHEY_SIMPLEX ,1,(255,0,0),2)
        cv2.line(image , (int(x_min),200),(int(x_min),250),(0,0,255))


        
    
    #rawCapture.truncate(0)
    key=cv2.waitKey(25) & 0xFF
    
    if key == ord('q'):
        break
    cv2.imshow("orginal",image)



GPIO.output(40,GPIO.LOW)
