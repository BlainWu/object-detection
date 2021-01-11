#!/bin/bash
set -e
cd ..

CUDA_VISIBLE_DEVICES=0  python demo.py --dataset pascal_voc_0712 --net snet_49 --load_dir snet_49 \
       --checkepoch 35  --cuda \
        --image_dir voc_images/input
