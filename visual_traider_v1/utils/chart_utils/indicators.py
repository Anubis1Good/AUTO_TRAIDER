import numpy as np
import numpy.typing as npt
from utils.ML_utils.LR_utils import get_linear_regress,get_points_linear_reg

def get_SMA(points:npt.NDArray,step) -> npt.NDArray:
    moving_averages = []
    # cum_sumx = np.cumsum(points[:,0])
    i = step 
    while i <= len(points):
        slice = points[i-step:i,1]
        cum_sumy = np.sum(slice)
        window_averagex = points[i-1][0]
        window_averagey = cum_sumy // step
        moving_averages.append([window_averagex,window_averagey])
        i += 1
    return np.array(moving_averages)

def get_bollinger_bands(points:npt.NDArray) -> tuple[npt.NDArray]:
    sma20 = []
    bbu = []
    bbd = []
    step = 20
    i = step 
    while i <= len(points):
        slice = points[i-step:i,1]
        cum_sumy = np.sum(slice)
        window_averagex = points[i-1][0]
        window_averagey = cum_sumy // step
        sma20.append([window_averagex,window_averagey])
        std = int(np.std(slice))*2
        bbu_y = window_averagey - std
        bbd_y = window_averagey + std
        bbu.append([window_averagex,bbu_y])
        bbd.append([window_averagex,bbd_y])
        i += 1
    sma20 = np.array(sma20)
    bbu = np.array(bbu)
    bbd = np.array(bbd)
    return sma20,bbu,bbd

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