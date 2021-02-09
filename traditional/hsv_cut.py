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

def extract_color(img):
    #https://www.cnblogs.com/wangyblzu/p/5710715.html
    lower_hsv = np.array([100, 43, 46])
    upper_hsv = np.array([124, 255, 255])
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lowerb=lower_hsv,upperb=upper_hsv)
    return mask

if __name__ == '__main__':
    img = cv2.imread('../dataset/new_ball/pics/1.jpg')
    hsv = extract_color(img)
    contours, hierarchy = cv2.findContours(hsv, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[5]
    x, y, w, h = cv2.boundingRect(cnt)
    print(x,y,w,h)

    cv2.rectangle(img, (x, y), (x + w, y + h), BLUE, 5)

    cv2.imshow('origin',img)
    cv2.waitKey(0)
