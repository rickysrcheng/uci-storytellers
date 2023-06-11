#!/bin/bash
TRAIN_IMG_DIR="../img/resized/train"
VAL_IMG_DIR="../img/resized/val"
TRAIN_SIS_PATH="../sis/filtered.train.story-in-sequence.json"
VAL_SIS_PATH="../sis/filtered.val.story-in-sequence.json"
MODEL_PATH="./models/"
PRETRAINED_EPOCH=0
CUDA_VISIBLE_DEVICES=0,1,2,3
python train.py --train_image_dir $TRAIN_IMG_DIR --val_image_dir $VAL_IMG_DIR --train_sis_path $TRAIN_SIS_PATH --val_sis_path $VAL_SIS_PATH --model_path $MODEL_PATH --num_epochs 25 --pretrained_epoch $PRETRAINED_EPOCH