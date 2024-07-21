import numpy as np
import json


def get_points(ticker,path_points):
    # ticker = 'ABIO'
    # path_points = './DataForLearning/10.07.24/points/'
    data = ''
    x_tops,y_tops = [],[]
    x_bottoms,y_bottoms = [],[]
    with open(path_points+ticker+'.json') as f:
        data = json.load(f)
        for i in data:
            x_tops.append(list(map(lambda x: x[1],i['tops'][-8:-1])))
            y_tops.append(i['tops'][-1][1])
            x_bottoms.append(list(map(lambda x: x[1],i['bottoms'][-8:-1])))
            y_bottoms.append(i['bottoms'][-1][1])

    # x_bottoms = np.array(x_bottoms)
    # norm_max = np.max(x_bottoms)
    x_bottoms = np.array(x_bottoms)
    y_bottoms = np.array(y_bottoms)
    x_tops = np.array(x_tops)
    y_tops = np.array(y_tops)
    return x_tops,y_tops,x_bottoms,y_bottoms

if __name__ == '__main__':
    print(get_points('ALRS','./DataForLearning/10.07.24/points/'))
