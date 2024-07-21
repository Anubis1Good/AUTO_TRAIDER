import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2
import numpy as np
import keras
from help_about_VT import get_chart_point


model = keras.models.load_model('./Models/PointsReg1.h5')


path_images = './DataForLearning/12.07.24/images/'
files = os.listdir(path_images)
for file in files:
    try:
        img = cv2.imread(path_images + file)
        tops,bottoms = get_chart_point(img)
        tops_p = np.array([tops[-7:,1:].flatten()])
        bottoms_p = np.array([bottoms[-7:,1:].flatten()])

        y_pred_t = model.predict(tops_p)
        y_pred_b = model.predict(bottoms_p)
        point_t = (tops[-1][0]+10,int(y_pred_t[0][0]))
        point_b = (bottoms[-1][0]+10,int(y_pred_b[0][0]))

        cv2.polylines(img,[tops],False,(255,255,255),2)
        cv2.polylines(img,[bottoms],False,(155,155,155),2)
        cv2.circle(img,point_t,1,(255,255,0),2)
        cv2.circle(img,point_b,1,(255,0,255),2)
        img = cv2.resize(img,(600,400))
        cv2.imwrite(f'./test_prediction/{file}',img)
    except Exception as err:
        print(err)
# cv2.imshow(file,img)
# cv2.waitKey(0)