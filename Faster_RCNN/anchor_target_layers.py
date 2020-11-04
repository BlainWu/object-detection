# ------------------------------------------------
# Project: object-detection
# Author:Peilin Wu - Northumbria University
# File name :anchor_target_layers.py
# Created time :2020/11
# ------------------------------------------------
from generate_anchors import generate_anchors
import numpy as np
import torch
import torch.nn as nn

class _AnchorTargetLayer(nn.Module):

    def init__(self,feat_stride,scales,ratios):
        super(_AnchorTargetLayer,self).__init__()

        self._feat_stride = feat_stride
        self._scales = scales
        self._anchors = torch.from_numpy(generate_anchors(scales = np.array(scales),
                                                          ratios = np.array(ratios))).float()
        self._num_anchors = self._anchors.size(0)

        #allow anchors are locatted over the edge by a small value
        #default is 0
        self._allowed_boarder = 0



test = _AnchorTargetLayer()
print(test._num_anchors)