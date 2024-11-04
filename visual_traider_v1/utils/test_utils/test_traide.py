# test function
import os
import json
from time import time
import cv2


def get_save_test():
    saves = []
    with open('test.json') as f:
        saves = json.load(f)
    return saves

def send_save_test(saves):
    with open('test.json','w') as f:
        json.dump(saves,f)

def save_img(image,name,now,draw):
    image = image.copy()
    image = draw(image)
    save_dir= './test_images/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    img_name = save_dir + name + now +'.png'
    cv2.imwrite(img_name,image)
    return img_name

def test_open(image,name,pos,traider,draw,price):
    saves = get_save_test()
    saves_length = len(saves)
    for i in range(saves_length-1,-1,-1):
        if saves[i]['name'] == name and not saves[i]['close'] and saves[i]['traider'] == traider:
            return 0
    now = str(time())
    image_name = save_img(image,name,now,draw)
    saves.append({
        "name":name,
        "open":now,
        "close":"",
        "open_image":image_name,
        "close_img":"",
        "pos":pos,
        "traider":traider,
        "open_price":price,
        "close_price":price
    })
    send_save_test(saves)
    return 1

def test_close(image,name,pos,traider,draw,price):
    saves = get_save_test()
    saves_length = len(saves)
    now = str(time())
    for i in range(saves_length-1,-1,-1):
        if saves[i]['name'] == name and not saves[i]['close'] and saves[i]['pos'] == pos and saves[i]['traider'] == traider:
            img_name = save_img(image,name,now,draw)
            saves[i]['close'] = now
            saves[i]['close_img'] = img_name
            saves[i]['close_price'] = price
            send_save_test(saves)
            return 1
    else:
        return 0

# print('name' in get_save_test()[0])
# test_open(1,'moex')
# test_close(1,'moex')