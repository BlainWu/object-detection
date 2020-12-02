# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：object-detection -> camera
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/12/2 17:17
=================================================='''
'''
When button is pressed, the buzzer goes off and Pi saves a picture
Modules Pinout:
1) button:GPIO-10 (19)->INPUT:  pressed high; release low;
2) buzeer:GPIO-12 (32)->OUTPUT: PWM 2~5Khz
'''
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(10,GPIO.IN )
GPIO.setup(12,GPIO.OUT)
PWM = GPIO.PWM(12,3000)

while 1:
    if GPIO.wait_for_edge(10,GPIO.FALLING,bouncetime=300):  #if pressed
        PWM.start(1)    #duty cycle = 1%
        time.sleep(0.2)
        print("Taken")
        PWM.stop()

