# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：object-detection -> video2pic
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2021/1/4 19:45
@Desc   ：
=================================================='''

import cv2 as cv
import os
from tqdm import tqdm

'''Get the largest index in a dir'''
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

'''Turn the videos to pictures'''
def video2pic(videos_dir,frequency = 5):
    videos_list = os.listdir(videos_dir)
    pics_dir = os.path.join(os.path.dirname(videos_dir),'pics')
    if not os.path.exists(pics_dir):
        os.mkdir(pics_dir)
    pic_index = get_tmp_index(pics_dir)
    frame_index = 0

    for video in tqdm(videos_list):
        video_path = os.path.join(videos_dir,video)
        cap = cv.VideoCapture(video_path)
        if cap.isOpened():
            while True :
                ret,frame = cap.read()
                if ret:
                    frame_index += 1
                    if frame_index % frequency == 0:
                        cv.imwrite(os.path.join(pics_dir,"{0}.jpg".format(pic_index)),frame)
                        pic_index += 1
                else:
                    break
        else:
            print("Failed to load video: ", video_path)
    print("Processed {0} videos, reached {1} pictures.".format(len(videos_list),pic_index))

'''Rename the index in a dir'''
def re_index(dir,start_index = 0):
    pics_list = os.listdir(dir)
    pics_list.sort(key = lambda x : int(x.split('.')[0]))
    new_index = start_index
    for pic in tqdm(pics_list):
        pic_path = os.path.join(dir,pic)
        os.rename(pic_path,os.path.join(dir,'{0}.jpg'.format(new_index)))
        new_index += 1

if __name__ == '__main__':
    #video2pic(videos_dir= './simple_background/videos')
    re_index(dir = './simple_background/pics')
