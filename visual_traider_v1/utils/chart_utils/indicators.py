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

def get_bollinger_bands(points:npt.NDArray,k:int=2,step=20) -> tuple[npt.NDArray]:
    sma20 = []
    bbu = []
    bbd = []
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

def get_trend_lines(x,y) -> tuple[npt.NDArray]:
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

def get_linear_reg_clear(x,y):
    slope,intercept = get_linear_regress(x,y)
    x1 = np.array([x[-1] + (x[-1] - x[-2])])
    middle_line = list(map(lambda x:get_points_linear_reg(x,slope,intercept,0), x1))
    trend = np.column_stack([x1, middle_line])
    return trend[-1]

def get_fractals(hpts,lpts,n=5) -> tuple[npt.NDArray]:
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

def get_williams_fractals(hpts:npt.NDArray,lpts:npt.NDArray,n=2,is_qual=False) -> tuple[npt.NDArray]:
    maxs = []
    mins = []
    hpts = list(hpts.tolist())
    lpts = list(lpts.tolist())
    for i in range(n,len(hpts)-n):
        slice_h = hpts[i-n:i]
        slice_h += hpts[i+1:i+n+1]
        slice_l = lpts[i-n:i]
        slice_l += lpts[i+1:i+n]
        if is_qual:
            if all([j[1] >= hpts[i][1] for j in slice_h]):
                maxs.append(np.array(hpts[i]))
            if all([j[1] <= lpts[i][1] for j in slice_l]):
                mins.append(np.array(lpts[i]))
        else:
            if all([j[1] > hpts[i][1] for j in slice_h]):
                maxs.append(np.array(hpts[i]))
            if all([j[1] < lpts[i][1] for j in slice_l]):
                mins.append(np.array(lpts[i]))
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

def check_zona(zona,half_bars,cur_price=None,method=None):
    is_zona = False
    if not cur_price:
        cur_price =  half_bars[-1].ym
    cz = None
    for z in zona:
        if z[0][1] < half_bars[-1].yh < z[1][1]:
            is_zona = True
            cz = z
            break
        if z[0][1] < half_bars[-1].yl < z[1][1]:
            is_zona = True
            cz = z
            break
        if z[0][1] < half_bars[-1].ym < z[1][1]:
            is_zona = True
            cz = z
            break
    if method == 'long' and cz:
        if cur_price > cz[1][1]:
            is_zona = False
    if method == 'short' and cz:
        if cur_price < cz[0][1]:
            is_zona = False
    return is_zona

# strange_result
def get_rsi(half_bars:list[HalfBar],period=14):
    ups,downs = [],[]
    for i in range(len(half_bars)-period,len(half_bars)):
        if half_bars[i].yh > half_bars[i-1].yh:
            ups.append(half_bars[i].spred)
        else:
            downs.append(half_bars[i].spred)
    ups = np.array(ups)
    downs = np.array(downs)
    # print(np.exp(ups))
    rs =  np.average(ups) / np.average(downs) 
    rsi = 100 - 100 / (1 + rs)
    return rsi
    # RSI = 100 – 100 / (1 + RS),
    # RS = EMAn(Up) / EMAn(Down)

def get_spred_channel(half_bars:list[HalfBar],period=14) -> tuple[npt.NDArray]:
    ma = []
    ups,downs = [],[]
    ups2,downs2 = [],[]
    # cum_sumx = np.cumsum(points[:,0])
    i = period 
    while i <= len(half_bars):
        slice = half_bars[i-period:i]
        slice_ym = []
        slice_spreds = []
        for hb in slice:
            slice_ym.append(hb.ym)
            slice_spreds.append(hb.spred)
        cum_sumy_ma = np.sum(np.array(slice_ym))
        cum_sumy_spred = np.sum(np.array(slice_spreds))
        xs = half_bars[i-1].x
        ma_y = cum_sumy_ma // period
        spreds = cum_sumy_spred // period
    
        ma.append([xs,ma_y])
        ups.append([xs,ma_y - spreds])
        downs.append([xs,ma_y + spreds])
        ups2.append([xs,ma_y - spreds*2])
        downs2.append([xs,ma_y + spreds*2])
        i += 1
    return np.array(ma),np.array(ups),np.array(downs),np.array(ups2),np.array(downs2)



def get_bb_points(ups,downs,step=10) -> tuple[npt.NDArray]:
    creeks = []
    ices = []
    for i in range(step,len(ups)-(step+1)):
        ups_prev = ups[i-step:i]
        ups_next = ups[i+1:i+step]
        downs_prev = downs[i-step:i]
        downs_next = downs[i+1:i+step]
        if all([ups[i][1] <= y[1] for y in ups_prev]) and all([ups[i][1] <= y[1] for y in ups_next]):
            creeks.append(ups[i])
        if all([downs[i][1] >= y[1] for y in downs_prev]) and all([downs[i][1]>= y[1] for y in downs_next]):
            ices.append(downs[i])
    creeks = np.array(creeks)
    ices = np.array(ices)
    return creeks,ices


def get_borders(region,divider=4)  -> tuple[npt.NDArray]:
    heigth = region[3]-region[1]
    width = region[2] - region[0]
    buff = heigth // divider
    top_line =np.array(((10,0+buff),(width-10,0+buff)))
    bottom_line =np.array(((10,heigth-buff),(width-10,heigth-buff)))
    return top_line,bottom_line

def get_donchan_channel(half_bars:list[HalfBar],period=20,delay=0)  -> tuple[npt.NDArray]:
    ups,downs = [],[]
    avarage = []
    for i in range(period,len(half_bars)-delay):
        slice = half_bars[i-period:i]
        max_hb = half_bars[i].hpt
        min_hb = half_bars[i].lpt
        for j in slice:
            if j.yh < max_hb[1]:
                max_hb = max_hb[0],j.yh
            if j.yl > min_hb[1]:
                min_hb = max_hb[0],j.yl
        ups.append(max_hb)
        downs.append(min_hb)
        avarage_y = (min_hb[1] + max_hb[1])//2
        avarage.append((max_hb[0],avarage_y))
    return np.array(ups),np.array(downs),np.array(avarage)

def get_level_DC():
    pass