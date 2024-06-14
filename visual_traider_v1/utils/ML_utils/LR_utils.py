from scipy import stats

def learn_LR(x,y): 
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    return slope,intercept

def predict_LR(x,offset,slope,intercept):
    return int(slope * x + intercept+offset)