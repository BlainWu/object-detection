#!/bin/bash
set -e
cd ..

CUDA_VISIBLE_DEVICES=0  python trainval_net.py --dataset pascal_voc_0712 --net snet_49 --bs 8 --nw 4 \
    --lr 1e2   --epochs 75 --cuda  --lr_decay_step 100,200,300  --use_tfboard  True\
     --save_dir snet_49  --eval_interval 2   \
     --r True  --checkepoch 63
