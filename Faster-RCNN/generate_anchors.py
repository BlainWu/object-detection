# ------------------------------------------------
# Project: object-detection
# Author:Peilin Wu - Northumbria University
# File name :generate_anchors.py
# Created time :2020/11
# ------------------------------------------------

import numpy as np

def generate_anchors (base_size=16, scales=[8,16,32],ratios=[0.5,1,2]):

    #generate a anchor with [0,0,15,15] in [x1,y1,x2,y2]
    base_anchor = np.array([0,0,base_size-1,base_size-1])

    ratio_anchors = _ratio_anchor(base_anchor,ratios)

def _ratio_anchor(base_anchor,ratios):
    """
    :param base_anchor: basic size anchor
    :param ratios:      ratios of width and height
    :return:
    """
    w,h,x_ctr,y_ctr = _xy_whctrs(base_anchor)

def _xy_whctrs(anchor):
    """
    :param anchor:  an anchor in [x1,y1,x2,y2]
    :return:        an anchor in [w,h,x_center,y_center]
    """
    w = anchor[2] - anchor[0] + 1
    h = anchor[3] - anchor[1] + 1
    x_center = (anchor[0]+anchor[2])/2
    y_center = (anchor[1]+anchor[3])/2
    return w,h,x_center,y_center