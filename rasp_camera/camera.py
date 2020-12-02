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
import picamera
import time
import os

'''setup hardware'''
GPIO.setmode(GPIO.BCM)
GPIO.setup(10,GPIO.IN )
GPIO.setup(12,GPIO.OUT)
PWM = GPIO.PWM(12,3000)
camera = picamera.PiCamera()
camera.rotation = 180

'''initilize the img index'''
imgs_list = os.listdir("./imgs")
index = []

if len(imgs_list)==0:
    tmp_index = 0
else:
    for i,name in enumerate(imgs_list):
        index.append(int(name.split('.')[0]))
    index.sort()
    tmp_index = index[-1] + 1

while 1:
    if GPIO.wait_for_edge(10,GPIO.FALLING,bouncetime=300):  #if pressed
        PWM.start(1)    #duty cycle = 1%
        time.sleep(0.2)
        """保存图片"""
        camera.capture('./imgs/{0}.jpg'.format(tmp_index))
        tmp_index += 1
        PWM.stop()
