#!/bin/bash
set -e
cd ..

CUDA_VISIBLE_DEVICES=0  python trainval_net.py --dataset pascal_voc_0712 --net snet_146 --bs 8 --nw 4 \
     --lr 1e3   --epochs 100 --cuda  --lr_decay_step 25,50,75  --use_tfboard  True \
     --save_dir snet146  --eval_interval 2   --logdir snet146_log --pre ./weights/snet_146.tar \
     #--r True --checkepoch 2
