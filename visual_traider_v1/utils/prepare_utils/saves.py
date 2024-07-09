import cv2
import json
from time import time

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



def save_points(image):
    pass

def save_trends(image):
    pass

# def get_save_test():
#     saves = []
#     with open('test.json') as f:
#         saves = json.load(f)
#     return saves
# def send_save_test(saves):
#     with open('test.json','w') as f:
#         json.dump(saves,f)