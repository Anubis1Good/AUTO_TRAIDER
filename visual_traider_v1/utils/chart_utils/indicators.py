import numpy as np
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