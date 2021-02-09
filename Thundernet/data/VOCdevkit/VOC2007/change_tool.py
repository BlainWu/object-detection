# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：object-detection -> change_tool
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2021/1/11 14:51
@Desc   ：
=================================================='''
import os
from tqdm import tqdm
import xml.etree.ElementTree as ET


def lime_list():
    with open('ImageSets/Main/train.txt') as train_f:
        new_data = []
        for line in train_f:
            print(line)
            index = line.split('.jpg')[0]
            index_ = index.split('/')[1]
            new_data.append(index_)
        with open('trian.txt', 'w') as new_file:
            for i in new_data:
                print(i)
                new_file.write(i+'\n')

    with open('ImageSets/Main/val.txt') as train_f:
        new_data = []
        for line in train_f:
            print(line)
            index = line.split('.jpg')[0]
            index_ = index.split('/')[1]
            new_data.append(index_)
        with open('ImageSets/Main/val.txt', 'w') as new_file:
            for i in new_data:
                print(i)
                new_file.write(i+'\n')

def xml_single(xml_dir = './Annotations'):
    xml_list = os.listdir(xml_dir)
    print("把所有标签都改成ball")
    for xml in tqdm(xml_list):
        xml_path = os.path.join(xml_dir,xml)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for object in root.findall('object'):
            object.find('name').text = 'ball'
        tree.write(xml_path)

if __name__ == '__main__':
    xml_single()