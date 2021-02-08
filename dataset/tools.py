# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：object-detection -> video2pic
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2021/1/4 19:45
=================================================='''
import random
import cv2 as cv
import os
import shutil
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


"""Remove unlabeled images"""
def dataset_check(img_dir,antation_dir):
    img_list = os.listdir(img_dir)
    antation_list=os.listdir(antation_dir)
    print(f'图片数量{len(img_list)},标签数量{len(antation_list)}')
    if(len(img_list) ==len(antation_list) ):
        return
    else:
        for index,list in enumerate(antation_list):
            antation_list[index] = list.split('.')[0]

        del_list = []
        for index,list in enumerate(img_list):
            img_list[index] = list.split('.')[0]
            if img_list[index] not in antation_list:
                del_list.append(img_list[index])

        print(f'以下图片序号没有找到标注{del_list}')
        for i in del_list:
            del_path = i+'.jpg'
            os.remove(os.path.join(img_dir,del_path))
            print(f'已删除{del_path}')

'''Divided the dataset into train and val in Tensorflow format'''
def divide_dataset(img_dir,antation_dir,ratio=0.9):
    dataset_check(img_dir,antation_dir)#check the dataset
    img_list = os.listdir(img_dir)
    for index, list in enumerate(img_list):
        img_list[index] = list.split('.')[0]
    '''shuffle and divide the dataset'''
    random.shuffle(img_list)
    cut_point = int(ratio * len(img_list))
    train_list = img_list[:cut_point]
    test_list = img_list[cut_point:]

    parent_dir = os.path.dirname(img_dir)
    target_dir = os.path.join(parent_dir,'images')
    train_dir = os.path.join(target_dir,'train')
    test_dir = os.path.join(target_dir, 'test')

    if os.path.exists(target_dir):
        flag = input("已经存在images文件夹，是否覆盖(y/n):")
        if flag == 'n':
            print("没有区分数据集，程序结束。")
            return
        elif flag =='y':
            shutil.rmtree(target_dir)
            os.mkdir(target_dir)
            os.mkdir(train_dir)
            os.mkdir(test_dir)
    else:
        os.mkdir(target_dir)
        os.mkdir(train_dir)
        os.mkdir(test_dir)

    for train in tqdm(train_list):
        ims_file = os.path.join(img_dir,train + '.jpg')
        nota_file = os.path.join(antation_dir,train+ '.xml')
        shutil.copy(ims_file,train_dir)
        shutil.copy(nota_file, train_dir)

    for test in tqdm(test_list):
        ims_file = os.path.join(img_dir,test + '.jpg')
        nota_file = os.path.join(antation_dir,test+ '.xml')
        shutil.copy(ims_file,test_dir)
        shutil.copy(nota_file, test_dir)
    print("区分数据集成功。")

if __name__ == '__main__':
    #video2pic(videos_dir= './simple_background/videos')
    #re_index(dir = './simple_background/pics')
    #dataset_check(img_dir='./new_ball/pics', antation_dir='./new_ball/annotations')
    #divide_dataset(img_dir='./new_ball/pics', antation_dir='./new_ball/annotations')