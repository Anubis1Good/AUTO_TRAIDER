import math
import cv2
import numpy as np
from utils.config import ColorsBtnBGR
from utils.ML_utils.LR_utils import learn_LR,predict_LR

# function for search point of chart
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

# function for getting training data of linear regression
def get_xy_for_LR(tops,bottoms):
    x = np.concatenate((tops[:,0],bottoms[:,0]))
    y = np.concatenate((tops[:,1],bottoms[:,1]))
    return x,y

def get_trend_lines(region):
    tops,bottoms = get_chart_point(region)
    x,y = get_xy_for_LR(tops,bottoms)
    slope,intercept = learn_LR(x,y)
    std_y = np.std(y)
    # middle_line = list(map(lambda x:predict_LR(x,0,slope,intercept), x))
    top_line = list(map(lambda x:predict_LR(x,std_y,slope,intercept), x))
    bottom_line = list(map(lambda x:predict_LR(x,-std_y,slope,intercept), x))
    # trend = np.column_stack([x, middle_line])
    top_trend = np.column_stack([x, top_line])
    bottom_trend = np.column_stack([x, bottom_line])
    return slope,top_trend,bottom_trend

def get_last_points_trend(region):
    tops,bottoms = get_chart_point(region)
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

def get_four_points_and_slope(region):
    tops,bottoms = get_chart_point(region)
    x,y = get_xy_for_LR(tops,bottoms)
    slope,intercept = learn_LR(x,y)
    top_median = (np.average(tops[:,0],axis=0).astype(np.int32),np.average(tops[:,1],axis=0).astype(np.int32))
    top_quantile = (np.quantile(tops[:,0],0.2,axis=0).astype(np.int32),np.quantile(tops[:,1],0.2,axis=0).astype(np.int32))
    bottom_median = (np.average(bottoms[:,0],axis=0).astype(np.int32),np.average(bottoms[:,1],axis=0).astype(np.int32))
    bottom_quantile = (np.quantile(bottoms[:,0],0.8,axis=0).astype(np.int32),np.quantile(bottoms[:,1],0.8,axis=0).astype(np.int32))
    points = [top_median,top_quantile,bottom_median,bottom_quantile]
    return slope, points

# function for search rotate points
def levels(points,dir=True):
    x = points[:,0]
    levels = points[:,1]
    diff = np.diff(levels)
    p = []
    i = 0
    current=diff[0]
    while i<len(levels)-1:
        if dir:
            if diff[i]>0 and current<0:
                p.append((x[i],levels[i]))
        else:
            if diff[i]<0 and current>0:
                p.append((x[i],levels[i]))
        current = diff[i]
        i += 1
    p.append(points[0])
    p.append(points[-1])
    p = np.array(p)
    levels = p[:,1]
    return p

# function sort points for y
def get_extremum_points(points):
    points_sort = points[points[:,1].argsort()]
    return points_sort

# function for getting some half of points
def get_half(points,is_left):
    max_x = np.max(points[:,0])
    min_x = np.min(points[:,0])
    mean = (max_x+min_x)//2
    left = points[points[:,0]<mean]
    right = points[points[:,0]>mean]
    if is_left:
        return left
    return right

# function for getitng direction angle
def angle_between(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y1 - y2
    try:
        d = dx/dy
    except:
        d = 0
    r = math.degrees(math.pi/2 - math.atan(d))
    if dy > 0:
        return 90-r
    else:
        return 180-(r-90)
    
# function for getting four main points 
def get_main_points(region):
    tops,bottoms = get_chart_point(region) 
    top_rotate_point = levels(tops,True)
    bottom_rotate_point = levels(bottoms,False)
    top_rotate_point = top_rotate_point[top_rotate_point[:,0].argsort()]
    bottom_rotate_point = bottom_rotate_point[bottom_rotate_point[:,0].argsort()]
    lpt = get_extremum_points(get_half(top_rotate_point, True))[0]
    rpt = get_extremum_points(get_half(top_rotate_point, False))[0]
    lpb = get_extremum_points(get_half(bottom_rotate_point, True))[-1]
    rpb = get_extremum_points(get_half(bottom_rotate_point, False))[-1]
    return lpt,rpt,lpb,rpb

# function for getting mean level
def get_mean_y(lp,rp):
    return (lp[1] + rp[1])//2

# function for getting direction angle of trande lines
def get_angels_on_chart(mp):
    lpt,rpt,lpb,rpb = mp
    angle_top = angle_between(lpt,rpt)
    angle_bottom = angle_between(lpb, rpb)
    return angle_top,angle_bottom

# function classification trande line
# 1 - long, 0 - range, -1 - short
def get_trande(angle):
    if 0 < angle < 80:
        return 1 
    if 80 < angle < 100:
        return 0
    return -1

# function for getting current state of chart
def get_formation(mp):
    angle_top,angle_bottom = get_angels_on_chart(mp)
    trend_top = get_trande(angle_top)
    trend_bottom = get_trande(angle_bottom)

    total = trend_top + trend_bottom
    if total > 1:
        return 'long'
    if total < -1 or trend_bottom == -1:
        return 'short'
    return 'range'