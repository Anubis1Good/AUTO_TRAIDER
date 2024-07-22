import numpy as np
from utils.ML_utils.LR_utils import get_linear_regress,get_points_linear_reg
def get_SMA(points):
    moving_averages = []
    cum_sumx = np.cumsum(points[:,0])
    cum_sumy = np.cumsum(points[:,1])
    i = 1 
    while i <= len(points):
        window_averagex = cum_sumx[i-1] // i *2
        window_averagey = cum_sumy[i-1] // i
        moving_averages.append([window_averagex,window_averagey])
        i += 1
    return np.array(moving_averages)

def SA_point(points):
    return (np.average(points[:,0],axis=0).astype(np.int32),np.average(points[:,1],axis=0).astype(np.int32))

def get_trend_lines(x,y):
    std_y = np.std(y)
    slope,intercept = get_linear_regress(x,y)
    middle_line = list(map(lambda x:get_points_linear_reg(x,slope,intercept,0), x))
    top_line = list(map(lambda x:get_points_linear_reg(x,slope,intercept,std_y), x))
    bottom_line = list(map(lambda x:get_points_linear_reg(x,slope,intercept,-std_y), x))
    trend = np.column_stack([x, middle_line])
    top_trend = np.column_stack([x, top_line])
    bottom_trend = np.column_stack([x, bottom_line])
    return trend,top_trend,bottom_trend

def get_last_point_trend(x,y):
    trend,top_trend,bottom_trend = get_trend_lines(x,y)
    return trend[-1],top_trend[-1],bottom_trend[-1]