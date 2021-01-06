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

'''initilize the img index'''
def get_tmp_index(dir):
    file_list = os.listdir(dir)
    index = []
    if len(file_list)==0:
        tmp_index = 0
    else:
        for i,name in enumerate(file_list):
            index.append(int(name.split('.')[0]))
        index.sort()
        tmp_index = index[-1] + 1
    return tmp_index

import RPi.GPIO as GPIO
import picamera
import time
import os
import argparse

'''setup hardware'''
GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.IN)
GPIO.setup(12, GPIO.OUT)
PWM = GPIO.PWM(12, 3000)

parser = argparse.ArgumentParser()
parser.add_argument('-m','--mode',default='picture',type = str)
parser.add_argument('-t','--time',default=10,type = int)
args = parser.parse_args()

with picamera.PiCamera() as camera:
    camera.rotation = 180
    '''mode select: picture or video'''
    if args.mode == 'picture':
        save_dir = './imgs'
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        print("Selected mode: picture")
        tmp_index = get_tmp_index(save_dir)
        while 1:
            if GPIO.wait_for_edge(10, GPIO.FALLING, bouncetime=300):  # if pressed
                PWM.start(1)  # duty cycle = 1%
                time.sleep(0.2)
                """保存图片"""
                camera.capture('./imgs/{0}.jpg'.format(tmp_index))
                tmp_index += 1
                PWM.stop()

    else:
        save_dir = './videos'
        record_time = args.time
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        print("Selected mode: video")
        tmp_index = get_tmp_index(save_dir)
        while 1:
            if GPIO.wait_for_edge(10, GPIO.FALLING, bouncetime=300) :  # if pressed
                PWM.start(1)  # duty cycle = 1%
                time.sleep(0.2)
                PWM.stop()
                """保存图片"""
                camera.start_recording('./videos/{0}.h264'.format(tmp_index))
                camera.wait_recording(record_time)
                PWM.start(1)  # duty cycle = 1%
                time.sleep(0.5)
                PWM.stop()
                tmp_index += 1
                camera.stop_recording()