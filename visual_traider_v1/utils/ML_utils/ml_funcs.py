from scipy import stats
import numpy as np
import cv2
def get_linear_regress(x,y):
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    return slope,intercept

def get_points_linear_reg(x,slope,intercept,offset=0):
    return int(slope * x + intercept+offset)

def draw_trends(x,y,image):
    std_y = np.std(y)
    slope,intercept = get_linear_regress(x,y)
    middle_line = list(map(lambda x:get_points_linear_reg(x,slope,intercept,0), x))
    top_line = list(map(lambda x:get_points_linear_reg(x,slope,intercept,std_y), x))
    bottom_line = list(map(lambda x:get_points_linear_reg(x,slope,intercept,-std_y), x))
    trend = np.column_stack([x, middle_line])
    top_trend = np.column_stack([x, top_line])
    bottom_trend = np.column_stack([x, bottom_line])
    cv2.polylines(image,[trend],False,(255,255,255),2)
    cv2.polylines(image,[top_trend],False,(255,255,255),2)
    cv2.polylines(image,[bottom_trend],False,(255,255,255),2)