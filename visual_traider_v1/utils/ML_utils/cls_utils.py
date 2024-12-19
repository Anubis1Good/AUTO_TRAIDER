import numpy as np
import numpy.typing as npt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import cosine_similarity
from utils.chart_utils.dtype import HalfBar

def most_similar_point_cs(points:npt.NDArray,size_cluster:int=10):
    data = points[:-size_cluster]
    test_slice = points[-size_cluster:]
    max_cs = -1
    max_i = 0
    for i,point in enumerate(data):
        slice = points[i:i+size_cluster]
        cs= cosine_similarity([slice],[test_slice])
        if cs[0][0] > max_cs:
            max_cs = cs[0][0]
            max_i = i
    return max_i

def most_similar_point_cs_mult(hbs:list[HalfBar],size_cluster:int=10):
    
    yhs = np.array(list(map(lambda x: x.yh,hbs)))
    yms = np.array(list(map(lambda x: x.ym,hbs)))
    yls = np.array(list(map(lambda x: x.yl,hbs)))
    # yvs = np.array(list(map(lambda x: x.yv,hbs)))
    # groups = [yhs,yms,yls,yvs]
    groups = [yhs,yms,yls]
    tss = []
    for gp in groups:
        test_slice = gp[-size_cluster:]
        tss.append(test_slice)
    max_cs = -1
    max_i = 0
    for i in range(len(hbs)-size_cluster*2):
        for j in range(len(groups)):
            css = []
            slice = groups[j][i:i+size_cluster]
            test_slice = tss[j]
            cs= cosine_similarity([slice],[test_slice])
            css.append(cs[0][0])
        css = np.array(css)
        cs = css.mean()
        if cs > max_cs:
            max_cs = cs
            max_i = i

    return max_i

def most_similar_relative_point_cs(points:npt.NDArray,size_cluster:int=10):
    data = points[:-size_cluster]
    test_slice = points[-size_cluster:]
    test_slice = np.array(list(map(lambda i: test_slice[0] - i,test_slice)))
    max_cs = -1
    max_i = 0
    # for i,point in enumerate(data):
    for i in range(len(points)-size_cluster*2):
        slice = points[i:i+size_cluster]
        slice = np.array(list(map(lambda i: slice[0] - i,slice)))
        cs= cosine_similarity([slice],[test_slice])
        if cs[0][0] > max_cs:
            max_cs = cs[0][0]
            max_i = i
    return max_i

def most_similar_relative_point_cs_mult(hbs:list[HalfBar],size_cluster:int=10,use_volume:bool=False):
    yhs = np.array(list(map(lambda x: x.yh,hbs)))
    yms = np.array(list(map(lambda x: x.ym,hbs)))
    yls = np.array(list(map(lambda x: x.yl,hbs)))
    groups = [yhs,yms,yls]
    if use_volume:
        yvs = np.array(list(map(lambda x: x.yv,hbs)))
        groups.append(yvs)
    tss = []
    for gp in groups:
        test_slice = gp[-size_cluster:]
        test_slice = np.array(list(map(lambda i: test_slice[0] - i,test_slice)))
        tss.append(test_slice)
    max_cs = -1
    max_i = 0
    for i in range(len(hbs)-size_cluster*2):
        for j in range(len(groups)):
            css = []
            slice = groups[j][i:i+size_cluster]
            slice = np.array(list(map(lambda i: slice[0] - i,slice)))
            test_slice = tss[j]
            cs= cosine_similarity([slice],[test_slice])
            css.append(cs[0][0])
        css = np.array(css)
        cs = css.mean()
        if cs > max_cs:
            max_cs = cs
            max_i = i

    return max_i