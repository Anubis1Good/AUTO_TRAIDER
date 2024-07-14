import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2
import numpy as np
import keras


model = keras.models.load_model('./Models/PointsReg1.h5')
class ColorsBtnBGR:
    ask = (67, 67, 67)
    bid = (76, 76, 76)
    best_ask = (101, 82, 168)
    best_bid = (100, 117, 66)
    large_value_1 = (198, 140, 48)
    large_value_2 = (178, 201, 45)
    color_x = (9,0,255)
    color_x_shadow = (11,11,175)
    color_x_bb = (0,0,255)

    cur_price_1 = (96,118,50)
    cur_price_2 = (75,75,173)

    candle_color_1 = (111,111,111)
    candle_color_2 = (200,200,200)
def get_chart_point(region):
    color1 = np.array(ColorsBtnBGR.candle_color_1)
    color2 = np.array(ColorsBtnBGR.candle_color_2)
    mask1 = cv2.inRange(region,color1,color1)
    mask2 = cv2.inRange(region,color2,color2)
    mask = cv2.add(mask1,mask2)
    kernel = np.ones((2, 1), np.uint8) 
    # mask = cv2.erode(mask,kernel)
    del kernel,mask1,mask2
    countours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    tops = []
    bottoms = []
    for cnt in countours:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt,True),True)
        area = cv2.contourArea(approx)
        if area > 5:
            bottom = np.max(approx,0)[0]
            top = np.min(approx,0)[0]
            mean = np.mean(approx,0,int)[0]
            bottom_point = (mean[0],bottom[1])
            top_point = (mean[0],top[1])
            tops.append(top_point)
            bottoms.append(bottom_point)
    tops = np.array(tops)
    bottoms = np.array(bottoms)
    tops = tops[tops[:,0].argsort()]
    bottoms = bottoms[bottoms[:,0].argsort()]
    return tops,bottoms


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