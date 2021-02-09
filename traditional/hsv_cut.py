# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：object-detection -> hsv_cut
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2021/2/9 20:34
@Desc   ：
=================================================='''
import cv2
import numpy as np
GREEN = (0,255,0)
BLUE = (255,0,0)
RED = (0,255,255)

def extract_color(img,color):
    #https://www.cnblogs.com/wangyblzu/p/5710715.html
    if color == 'R':
        lower_hsv = np.array([100, 43, 46])
        upper_hsv = np.array([124, 255, 255])
    elif color == 'B':
        lower_hsv = np.array([100, 43, 46])
        upper_hsv = np.array([124, 255, 255])
    elif color == 'G':
        lower_hsv = np.array([35, 43, 46])
        upper_hsv = np.array([77, 255, 255])
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lowerb=lower_hsv,upperb=upper_hsv)
    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    #opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    #sure_bg = cv2.dilate(mask, kernel, iterations=6)
    sure_bg = cv2.erode(mask,kernel,iterations=5)
    return sure_bg

def rect_balls(img,hsv):
    contours, hierarchy = cv2.findContours(hsv, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]
    print(cnt)
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(img, (x, y), (x + w, y + h), BLUE, 5)
    return img


if __name__ == '__main__':

    video_path = '../dataset/new_ball/videos/GreenTest.h264'
    cap = cv2.VideoCapture(video_path)
    ret,frame = cap.read()
    while(ret):
        #img = cv2.imread('../dataset/new_ball/pics/1.jpg')

        hsv = extract_color(frame,'G')
        img = rect_balls(frame,hsv)

        cv2.imshow('origin',hsv)
        cv2.waitKey(100)
        ret, frame = cap.read()


    cap.release()
