import cv2
import time
import numpy as np
import requests

video = cv2.VideoCapture(0)


x_last = 320
y_last= 180

while True:
    '''img_str = requests.get(url , verify=True)
    img_array= np.array(bytearray(img_str.content),dtype=uint8)
    image=cv2.imdecode(img_array , -1 )'''
    check , image = video.read()
    image=cv2.resize(image,(640,360))
    roi = image[10:320,50:600]
    
    
    Blackline = cv2.inRange(roi , (0,0,0) , (60,60,60))
    #minimiser le bruit
    kernel = np.ones((3,3), np.uint8)
    Blackline= cv2.erode(Blackline , kernel , 5)
    Blackline = cv2.dilate(Blackline ,kernel ,9)
    contours_blk , hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours_blk_len = len(contours_blk)
    if len(contours_blk) > 0:
        if contours_blk_len == 1:
            blackbox = cv2.minAreaRect(contours_blk[0])
        else :
            candidates = []
            off_buttom =0
            for con_num in range(contours_blk_len):
                blackbox = cv2.minAreaRect(contours_blk[con_num])
                (x_min,y_min),(w_min,h_min),ang = blackbox
                box=cv2.boxPoints(blackbox)
                #recuperer seulement la 1er point de box
                (x_box,y_box)=box[0]
                if y_box>358:
                    off_buttom+=1
                candidates.append((y_box , con_num , x_min ,y_min))
            candidates = sorted(candidates)
            if off_buttom > 1:
                candidates_off_buttom =[]
                for con_num in range(contours_blk_len - off_buttom ,contours_blk_len):
                    (y_highest , con_highest , x_min ,y_min)=candidates[con_num]
                    total_distance = (abs(x_min -x_last)**2 +abs(y_min - y_last)**2)**0.5
                    candidates_off_buttom.append((total_distance,con_num))
                    #sort that : the one with the shortest distance will be at the top!!
                candidates_off_buttom= sorted(candidates_off_buttom)
                (total_distance,con_highest)= candidates_off_buttom[0]
                blackbox = cv2.minAreaRect(contours_blk[con_highest])
            else :
                
                (y_highest , con_highest ,x_min,y_min)=candidates[contours_blk_len-1]
                blackbox=cv2.minAreaRect(contours_blk[con_highest])
        (x_min ,y_min ),(w_min,h_min),ang = blackbox
        x_last =x_min
        y_laxt= y_min
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
        cv2.line(image , (int(x_min),200),(int(x_min),250),(0,0,255))    #rawCapture.truncate(0)
    key=cv2.waitKey(25) & 0xFF
    
    if key == ord('q'):
        break
    cv2.imshow("orginal",image)
    
video.release()
cv2.destroyAllWindows()


#GPIO.output(40,GPIO.LOW)
