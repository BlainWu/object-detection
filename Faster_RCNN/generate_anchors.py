# ------------------------------------------------
# Project: object-detection
# Author:Peilin Wu - Northumbria University
# File name :generate_anchors.py
# Created time :2020/11
# ------------------------------------------------

import numpy as np

"""
Generate 9 anchors ,by default
[[ -84.  -40.   99.   55.]
 [-176.  -88.  191.  103.]
 [-360. -184.  375.  199.]
 [ -56.  -56.   71.   71.]
 [-120. -120.  135.  135.]
 [-248. -248.  263.  263.]
 [ -36.  -80.   51.   95.]
 [ -80. -168.   95.  183.]
 [-168. -344.  183.  359.]]
"""

def generate_anchors (base_size=16, scales=2**np.arange(3, 6),ratios=[0.5,1,2]):
    """
    :param base_size:   the smallest square length
    :param scales:      multiples of width and height
    :param ratios:      multiples of area
    :return:            9 anchors with a same center in [x1,y1,x2,y2]
    """
    #generate a anchor with [0,0,15,15] in [x1,y1,x2,y2]
    base_anchor = np.array([0,0,base_size-1,base_size-1])
    #generate 3 anchors of a pair from base-anchor
    ratio_anchors = _ratio_anchor(base_anchor,ratios)
    #generate 9 anchors of a same center from ratio_anchors
    anchors = np.vstack([_scale_anchors(ratio_anchors[i, :], scales)
                         for i in range(ratio_anchors.shape[0])])
    return anchors

def _ratio_anchor(base_anchor,ratios):
    """
    :param base_anchor: basic size anchor ,square box
    :param ratios:      ratios of width and height
    :return:            3 anchors of a same pair in [x1,y1,x2,y2]
    """
    w,h,x_ctr,y_ctr = _xy_whctrs(base_anchor)
    size = w * h
    ratios_size = size / ratios         #[512,256,128]
    ws = np.round(np.sqrt(ratios_size)) #[23,16,11]
    hs = np.round(ws * ratios)          #[12,16,22]

    anchors = _mkanchors(ws,hs,x_ctr,y_ctr)
    return anchors

def _scale_anchors(anchor, scales):
    """
    :param anchor:  1 anchor
    :param scales:  width-height ratio (!!!array type,not list)
    :return:        9 anchors
    """
    w, h, x_ctr, y_ctr = _xy_whctrs(anchor)
    ws = int(w) * scales
    hs = int(h) * scales
    anchors = _mkanchors(ws, hs,x_ctr,y_ctr)
    return anchors

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

def _mkanchors(ws,hs,x_ctr,y_ctr):
    """
    :param ws:      [23,16,11]
    :param hs:      [12,16,22]
    :param x_ctr:`  [7.5]
    :param y_ctr:   [7.5]
    :return:        3 anchors of a same group in [x1,y1,x2,y2]
    """
    ws = ws[:, np.newaxis]
    hs = hs[:, np.newaxis]
    anchors = np.hstack((x_ctr - 0.5 * (ws - 1),  #x1
                         y_ctr - 0.5 * (hs - 1),  #y1
                         x_ctr + 0.5 * (ws - 1),  #x2
                         y_ctr + 0.5 * (hs - 1)   #y2
                         ))
    return anchors

