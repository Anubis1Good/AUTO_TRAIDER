import os
import cv2
import numpy as np
from utils.config import ColorsBtnBGR
config = (686,400,1362,700)

test_data = 'test_data'
days = os.listdir(test_data)

train_data = 'train_data'

if not os.path.exists(train_data):
    os.mkdir(train_data)

for day in days:
    imgs = os.listdir(os.path.join(test_data,day))
    for i,img in enumerate(imgs):
        if i%200 == 0:
            img_mat = cv2.imread(os.path.join(test_data,day,img))
            img_mat = img_mat[config[1]:config[3],config[0]:config[2]]
            mask1 = cv2.inRange(img_mat,ColorsBtnBGR.candle_color_1,ColorsBtnBGR.candle_color_1)
            mask2 = cv2.inRange(img_mat,ColorsBtnBGR.candle_color_2,ColorsBtnBGR.candle_color_2)
            mask = cv2.add(mask1,mask2)
            kernel = np.ones((2, 1), np.uint8) 
            mask = cv2.erode(mask,kernel)

            # cv2.imshow('0',mask)
            # cv2.waitKey(0)
            img_path = os.path.join(train_data,'train_'+img)
            cv2.imwrite(img_path,mask)