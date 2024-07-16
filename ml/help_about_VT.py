import cv2
import numpy as np
import numpy.typing as npt
from scipy import stats

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

def get_xy_for_LR(tops,bottoms):
    x = np.concatenate((tops[:,0],bottoms[:,0]))
    y = np.concatenate((tops[:,1],bottoms[:,1]))
    return x,y

def get_last_points_trend(tops,bottoms):
    x,y = get_xy_for_LR(tops,bottoms)
    slope,intercept = learn_LR(x,y)
    std_y = np.std(y)
    # middle_point = predict_LR(x[-1],0,slope,intercept)
    top_point = predict_LR(x[-1],-std_y,slope,intercept)
    bottom_point = predict_LR(x[-1],std_y,slope,intercept)
    # trend = (x[-1],middle_point)
    top_trend = (x[-1],top_point)
    bottom_trend = (x[-1],bottom_point)
    return slope,top_trend,bottom_trend


def learn_LR(x,y): 
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    return round(slope,4),intercept

def predict_LR(x,offset,slope,intercept):
    return int(slope * x + intercept+offset)

def color_search(img:npt.ArrayLike,color:tuple[int],reverse:bool=False):
    try:
        result = np.argwhere(
            (img[:,:,0] == color[0])& 
            (img[:,:,1] == color[1])& 
            (img[:,:,2] == color[2])
        )
        y = -1 if reverse else 0
        

        return result[y,1], result[y,0]
    except:
        return -1,-1
    
def get_level_variant(img,color):
    x,y = color_search(img,color,True)
    return y

def get_current_level(img) -> int:
    y = get_level_variant(img,ColorsBtnBGR.cur_price_1)
    if y > 0:
        return y
    y = get_level_variant(img,ColorsBtnBGR.cur_price_2)
    if y > 0:
        return y
    return None