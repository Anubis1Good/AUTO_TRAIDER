import os
import cv2
import json
import numpy as np
from time import time
from utils.chart_utils.general import get_chart_point,get_last_points_trend

def save_img(image,name):
    image = image.copy()
    # image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    img_name = './learn_data/images/'+ name + str(time()) +'.png'
    cv2.imwrite(img_name,image)
    saves = {}
    with open('./learn_data/images.json','r') as f:
        saves = json.load(f)
        if name in saves:
            saves[name].append(img_name)
        else:
            saves[name] = [img_name]
    with open('./learn_data/images.json','w') as f:
        json.dump(saves,f)

def save_arraylike(image,name):
    image = image.copy()
    filename = f'./learn_data/arrayLikes/{name}.json'
    if os.path.exists(filename):
        with open(filename,'r') as f:
            data = json.load(f)
            data.append([image.tolist(),time()])
        with open(filename,'w') as f:
            json.dump(data,f)
    else:
        data = []
        with open(filename,'w') as f:
            json.dump(data,f)

def save_points(image,name,cur_price):
    tops,bottoms = get_chart_point(image)
    slope,top_trend,bottom_trend = get_last_points_trend(image)
    filename = f'./learn_data/points/{name}.json'
    if os.path.exists(filename):
        with open(filename,'r') as f:
            data = json.load(f)
            data.append({
                "cur_price":int(cur_price),
                "tops":tops.tolist(),
                "bottoms":bottoms.tolist(),
                "slope":slope,
                "top_trend":top_trend[1],
                "bottom_trend":bottom_trend[1],
                "time":time()
            })
        with open(filename,'w') as f:
            json.dump(data,f)
    else:
        data = []
        with open(filename,'w') as f:
            json.dump(data,f)

def save_trends(image):
    pass

def read_arraylike(filename):
    with open(filename) as f:
        data = json.load(f)
        return data
        
if __name__ == '__main__':
    data = read_arraylike('./learn_data/arrayLikes/APTK.json')
    img = np.array(data[0][0],np.uint8)
    # print(type(img))
    # img = Image.fromarray(img.astype(np.uint8))
    # img.show()
    # cv2.imshow('test',img.astype(np.uint8))
    cv2.imshow('test',img)
    cv2.waitKey(0)



# def get_save_test():
#     saves = []
#     with open('test.json') as f:
#         saves = json.load(f)
#     return saves
# def send_save_test(saves):
#     with open('test.json','w') as f:
#         json.dump(saves,f)