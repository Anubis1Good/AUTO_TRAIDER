from scipy import stats

# for VisualTraider before v2
def learn_LR(x,y): 
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    return round(slope,4),intercept

def predict_LR(x,offset,slope,intercept):
    return int(slope * x + intercept+offset)

# for VisualTraider after v2
def get_linear_regress(x,y):
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    return round(slope,4),intercept

def get_points_linear_reg(x,slope,intercept,offset=0):
    return int(slope * x + intercept+offset)