
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：object-detection -> hsv_cut
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2021/2/9 20:34
=================================================='''
"""
Milestones: 
1.Blue + simple background (0.h264)
2.Blue + complex background
"""
import os
import cv2
import numpy as np
import time
#import picamera
#import picamera.array

MIN_POINTS = 50
MIN_AREA = 1000
'''----------------------------'''
color_map = {'GREEN':(0,255,0),
             'BLUE' :(255,0,0),
             'RED'  :(0,0,255)}

def timer():
    pass

def extract_color(img,color):
    #https://www.cnblogs.com/wangyblzu/p/5710715.html
    assert color in ['GREEN','BLUE','RED','None']
    if color == 'RED':
        lower_hsv = np.array([156 ,100, 46])
        upper_hsv = np.array([180, 255, 255])
    elif color == 'BLUE':
        lower_hsv = np.array([100, 200, 46])
        upper_hsv = np.array([144, 255, 255])
    elif color == 'GREEN':
        lower_hsv = np.array([35, 180, 46])
        upper_hsv = np.array([77, 255, 255])
    elif color == 'None':
        lower_hsv = np.array([0, 0, 0])
        upper_hsv = np.array([0, 0, 0])
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lowerb=lower_hsv,upperb=upper_hsv)
    return mask

def rect_balls(img, mask,color):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #area filter
    for i in range(len(contours)):
        if(len(contours[i])>MIN_POINTS) and (cv2.contourArea(contours[i])>MIN_AREA):
            x,y,w,h = cv2.boundingRect(contours[i])
            cv2.rectangle(img, (x, y), (x + w, y + h), color_map[color], 5)
        else:
            continue
    return img

"""后续把color改成*args"""
def image_detector(path,color):
    img = cv2.imread(path)
    mask = extract_color(img,color)
    img = rect_balls(img,mask,color)
    cv2.imshow('HSV',mask)
    cv2.imshow('Origin',img)
    cv2.waitKey(0)

def video_detector(video_path,color,save_path=None):
    cap = cv2.VideoCapture(video_path)
    ret,frame = cap.read()
    save_flag = False
    if save_path is not None:
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(f'{save_path}/{color}_output.avi',
                              fourcc, fps, size)
        save_flag = True
    while(ret):
        #start_time = time.clock()

        for i in range(len(color)):
            mask = extract_color(frame,color[i])
            frame = rect_balls(frame,mask,color[i])
        if save_flag is True:
            out.write(frame)
        cv2.imshow(f'Track {color} balls',frame)
        cv2.waitKey(1)
        ret, frame = cap.read()

        #proc_time = time.clock()-start_time
        #print(f' {format(proc_time,".3f")}s - {format(1/proc_time,".2f")}FPS')
    cap.release()
    out.release()
    cv2.destroyAllWindows()


"""后面输出结果还可以concat一下，把HSV图片和彩色图片同时输出"""
def camera_detector(img_size = (640,480),color = ['BLUE'],save_path = None):

    camera_fps = 30
    save_flag = False if not save_path else True
    if save_flag:
        cap = cv2.VideoCapture(save_path)
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(f'{save_path}/{color}_output.avi',
                              fourcc, camera_fps, img_size)

    with picamera.PiCamera() as camera:
        camera.rotation = 180
        camera.resolution = img_size
        camera.framerate = camera_fps
        assert len(color)>0,print("Detect Nothing, please define the color.")

        with picamera.array.PiRGBArray(camera,size=img_size) as stream:
            while(1):
                #start_time = time.time()
                camera.capture(stream,format='bgr',use_video_port=True)
                frame = stream.array

                for i in range(len(color)):
                    mask = extract_color(frame,color[i])
                    frame = rect_balls(frame,mask,color[i])

                cv2.imshow('frame',frame)
                #cv2.imshow('mask', mask)

                if save_flag:
                    out.write(frame)

                cv2.waitKey(1)
                #print(1/ (time.time() - start_time))
                stream.seek(0)
                stream.truncate()

def show_process(image,save_dir,color):

    from matplotlib import pyplot as plt
    import matplotlib.gridspec as gridspec

    assert os.path.exists(image),f'{image} is not exist.'
    assert color is not None,f'Please enter the color you want to track.'

    for _color in color:
        assert _color in ['RED','GREEN','BLUE'],f'{_color} is not a valid color name, it should be RED GREEN BLUE'

    save_dir = (os.path.dirname(image) if save_dir is None else save_dir)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)


    #====================================================#
    gs = gridspec.GridSpec(2,2)
    plt.figure(dpi= 100 ,figsize=(10,10))
    font_size =26

    '''----------------Original_image-----------------'''
    img = cv2.imread(image)
    out_put = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.subplot(gs[0,0])
    plt.imshow(out_put)
    plt.title('Input Image',fontsize=font_size)
    plt.xticks([])
    plt.yticks([])
    '''-----------------------------------------------'''

    '''---------------------Mask----------------------'''
    mask = extract_color(img,'None')
    for _color in color:
        mask = extract_color(img,_color) + mask

    plt.subplot(gs[0,1])
    plt.imshow(mask,cmap='gray')
    plt.title('Extract Colors',fontsize=font_size)
    plt.xticks([])
    plt.yticks([])
    '''-----------------------------------------------'''
    #contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    '''---------------------Final result----------------------'''

    for i in range(len(color)):
        mask = extract_color(img, color[i])
        img = rect_balls(img, mask, color[i])

    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.subplot(2,1,2)
    plt.imshow(img)
    plt.title('Output Image',fontsize=font_size)
    plt.xticks([])
    plt.yticks([])

    '''-----------------------------------------------'''
    plt.savefig(os.path.join(save_dir, 'Result.jpg'))
    plt.show()



if __name__ == '__main__':

    #image_detector('./pics/1.jpg','BLUE')
    #video_detector('./videos/5.h264',['RED','BLUE','GREEN'],'./results')
    #camera_detector(color = ['BLUE'],save_path='./saved_video')
    show_process(image='./data/origin.jpg',save_dir=None,color = ['RED','BLUE','GREEN'])
    pass
