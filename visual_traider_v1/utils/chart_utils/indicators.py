import numpy as np
import numpy.typing as npt
from utils.ML_utils.LR_utils import get_linear_regress,get_points_linear_reg
from utils.chart_utils.dtype import HalfBar

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

def get_bollinger_bands(points:npt.NDArray,k:int=2) -> tuple[npt.NDArray]:
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
        std = int(np.std(slice)*k)
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

def get_fractals(hpts,lpts,n=5):
    maxs = []
    mins = []
    for i in range(n,len(hpts),n):
        max_p = hpts[i][1]
        min_p = lpts[i][1]
        ph = hpts[i]
        pl = lpts[i]
        for j in range(i-n,i):

            if max_p > hpts[j][1]:
                max_p = hpts[j][1]
                ph = hpts[j]
            if min_p < lpts[j][1]:
                min_p = lpts[j][1]
                pl = lpts[j]
        maxs.append(np.array(ph))
        mins.append(np.array(pl))

    return np.array(maxs),np.array(mins)

def get_context(half_bars):
    max_hb_i,min_hb_i = 0,0
    max_hb,min_hb = half_bars[0],half_bars[0]
    local_hb,direction = None,None
    for i in range(len(half_bars)):
        if half_bars[i].yh < max_hb.yh:
            max_hb = half_bars[i]
            max_hb_i = i
        if half_bars[i].yl > min_hb.yl:
            min_hb = half_bars[i]
            min_hb_i = i
    if max_hb_i > min_hb_i:
        direction = 'long'
        local_hb = max_hb
        if max_hb_i < len(half_bars)-1:
            for i in range(max_hb_i,len(half_bars)):
                if half_bars[i].yl > local_hb.yl:
                    local_hb = half_bars[i]       
    else:
        direction = 'short'
        local_hb = min_hb
        if min_hb_i < len(half_bars)-1:
            for i in range(min_hb_i,len(half_bars)):
                if half_bars[i].yh < local_hb.yh:
                    local_hb = half_bars[i]
    return max_hb,min_hb,local_hb,direction,max_hb_i,min_hb_i

def get_zona(half_bars,cur_price,vpts,v_sma):
    cur_history_hb_i = 0
    z = False
    m_pt_zona = None
    for i in range(len(half_bars)-2,0,-1):
        if half_bars[i].yh < cur_price[1] < half_bars[i].yl:
            cur_history_hb_i = i
            v_history = vpts[cur_history_hb_i]
            v_sma_history = v_sma[cur_history_hb_i-19]
            z = v_history[1] < v_sma_history[1]
            m_pt_zona = half_bars[cur_history_hb_i].ym
            break
    return z,m_pt_zona

def get_last_pick(half_bars,top_trend,bottom_trend):
    last_pick = 0
    for i in half_bars:
        pts_t = top_trend[np.argwhere(top_trend[:,0] == i.x)].flatten()
        pts_b = bottom_trend[np.argwhere(bottom_trend[:,0] == i.x)].flatten()
        if len(pts_t) > 0:
            if i.yh < pts_t[-1]:
                last_pick = 1
        if len(pts_b) > 0:
            if i.yl > pts_b[-1]:
                last_pick = -1  
    return last_pick
        
def get_dynamics(points,n=10):
    deltas = 0
    for i in range(len(points)-2,len(points)-n,-1):
        delta = points[i+1][1] - points[i][1]
        deltas += delta
    return deltas
    # return deltas//n

def check_zona(zona,half_bars):
    is_zona = False
    for z in zona:
        if z[0][1] < half_bars[-1].yh < z[1][1]:
            is_zona = True
            break
        if z[0][1] < half_bars[-1].yl < z[1][1]:
            is_zona = True
            break
        if z[0][1] < half_bars[-1].ym < z[1][1]:
            is_zona = True
            break
        if z[0][1] < half_bars[-2].yh < z[1][1]:
            is_zona = True
            break
        if z[0][1] < half_bars[-2].yl < z[1][1]:
            is_zona = True
            break
        if z[0][1] < half_bars[-2].ym < z[1][1]:
            is_zona = True
            break
    return is_zona
