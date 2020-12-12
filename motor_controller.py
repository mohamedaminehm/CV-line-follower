import time
import State
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
pwm1 = GPIO.PWM(7,50)
pwm2 = GPIO.PWM(15,50)
pwm1.start(0)
pwm2.start(0)
time.sleep(2)
def stop_motors():

    GPIO.output(5,GPIO.LOW)
    GPIO.output(3,GPIO.LOW)

    GPIO.output(13,GPIO.LOW)
    GPIO.output(11,GPIO.LOW)
def Motor_steer(speed,steering):
    #print("steering before =", steering)
    global pwm1,pwm2
    GPIO.setmode(GPIO.BOARD)


    
    if steering == 0:
        GPIO.output(5,GPIO.LOW)
        GPIO.output(3,GPIO.HIGH)

        GPIO.output(13,GPIO.LOW)
        GPIO.output(11,GPIO.HIGH)
        pwm1.ChangeDutyCycle(speed*0.8)
        #pwm == right
        pwm2.ChangeDutyCycle(speed*0.8)

        
        
        
        
        return
    if steering > 0 :
        steering = 100  - steering
        #print("steering right > 0 =", steering)
        if steering < 0:

            GPIO.output(5,GPIO.LOW)
            GPIO.output(3,GPIO.HIGH)

            GPIO.output(13,GPIO.HIGH)
            GPIO.output(11,GPIO.LOW)

            pwm1.ChangeDutyCycle(speed*1.2)
            pwm2.ChangeDutyCycle(speed*0.6)
            return 
        
        elif steering < 55:

            GPIO.output(5,GPIO.LOW)
            GPIO.output(3,GPIO.HIGH)

            GPIO.output(13,GPIO.LOW)
            GPIO.output(11,GPIO.LOW)

            pwm1.ChangeDutyCycle(speed*1.2)
            pwm2.ChangeDutyCycle(0)
            return 
        
        else :
        #ser.write(chr(abs(int(speed*steering/100))).encode())
            GPIO.output(5,GPIO.LOW)
            GPIO.output(3,GPIO.HIGH)

            GPIO.output(13,GPIO.LOW)
            GPIO.output(11,GPIO.HIGH)
            #print(" speed = " + str(speed*steering/100))

            pwm1.ChangeDutyCycle(speed*0.9)
            pwm2.ChangeDutyCycle(abs(speed*steering*0.8/100))

            return
    if steering < 0 :
        #turn left
        steering = steering * -1
        steering = 100  - steering
        #print("steering left > 0 =", steering)
        #print("steering =",  steering)
        if steering < 55:

            GPIO.output(5,GPIO.LOW)
            GPIO.output(3,GPIO.HIGH)

            GPIO.output(13,GPIO.LOW)
            GPIO.output(11,GPIO.HIGH)

            pwm1.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(speed*1.2)
            return 
        
        else :    

            GPIO.output(5,GPIO.LOW)
            GPIO.output(3,GPIO.HIGH)

            GPIO.output(13,GPIO.LOW)
            GPIO.output(11,GPIO.HIGH)

            pwm2.ChangeDutyCycle(speed*0.8)
            pwm1.ChangeDutyCycle(abs(speed*steering*0.8/100))
            #ser.write(chr(abs(int(speed*steering/100))).encode())
            #print(" speed = " + str(speed*steering/100))
            return

