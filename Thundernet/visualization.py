# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：object-detection -> visualization
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2021/1/11 20:11
@Desc   ：
=================================================='''

import torch
from tqdm import tqdm
import os
import cv2 as cv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-mp','--model_path',default='Test.pth',type = str)
parser.add_argument('-m', '--mode', default='picture', type=str)
parser.add_argument('-vp', '--video_path', default='red_ball.h264', type=str)
args = parser.parse_args()

# 加载模型
pthfile = args.model_path
model = torch.load(pthfile)
print(model)

'''
# 处理图片模式
if args.mode == 'picture':
    # 加在图片列表
    jpg_list = []
    with open('MyDataset/test_list.txt', 'r') as f:
        data = f.read()
        data = data.split('\n')
        for _list in data:
            jpg_list.append(_list.split(' ')[0])
    print("加载完成图片列表")
    # 批量预测和可视化
    for jpg in tqdm(jpg_list):
        jpg_path = os.path.join('./MyDataset', jpg)
        result = model.predict(jpg_path)
        pdx.det.visualize(jpg_path, result, threshold=0.3, save_dir='Test_result')

else:
    video_path = args.video_path
    cap = cv.VideoCapture(video_path)
    save_path = '{0}_result.avi'.format(video_path.split('.')[0])
    out = cv.VideoWriter(save_path,
                         cv.VideoWriter_fourcc(*'XVID'),
                         int(cap.get(5)),
                         (int(cap.get(3)), int(cap.get(4)))
                         )

    # 生成图片序列
    if not os.path.exists('buffer'):
        os.mkdir('buffer')
    frame_index = 0
    ret, frame = cap.read()
    while ret:
        ret, frame = cap.read()
        if not ret:
            print("No frame anymore. Exiting......")
            break
        result = model.predict(frame)
        frame_index += 1
    # 集合成视频
    jpg_list = []
    jpg_list = os.listdir('buffer')
    jpg_list.sort(key=lambda x: int(x.split('.')[0].split('_')[1]))
    # 批量预测和可视化
    for jpg in tqdm(jpg_list):
        jpg_path = os.path.join('buffer', jpg)
        frame_out = cv.imread(jpg_path)
        out.write(frame_out)

'''