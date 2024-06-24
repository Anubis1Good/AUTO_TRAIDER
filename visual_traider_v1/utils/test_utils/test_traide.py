# test function
import json
from datetime import datetime
import cv2
from utils.chart_utils.general import get_trend_lines

def get_save_test():
    saves = []
    with open('test.json') as f:
        saves = json.load(f)
    return saves
def send_save_test(saves):
    with open('test.json','w') as f:
        json.dump(saves,f)

def save_img(image,name,now):
    slope,top_trend,bottom_trend = get_trend_lines(image)
    cv2.polylines(image,[top_trend],False,(255,255,255),2)
    cv2.polylines(image,[bottom_trend],False,(255,255,255),2)
    img_name = './test_images/'+ name + now[-6:] +'.png'
    cv2.imwrite(img_name,image)
    return img_name

def test_open(image,name):
    saves = get_save_test()
    saves_length = len(saves)
    for i in range(saves_length-1,-1,-1):
        if saves[i]['name'] == name and not saves[i]['close']:
            return None
    now = str(datetime.now())
    image_name = save_img(image,name,now)
    saves.append({
        "name":name,
        "open":now,
        "close":"",
        "open_image":image_name,
        "close_img":""
    })
    send_save_test(saves)

def test_close(image,name):
    saves = get_save_test()
    saves_length = len(saves)
    now = str(datetime.now())
    for i in range(saves_length-1,-1,-1):
        if saves[i]['name'] == name and not saves[i]['close']:
            img_name = save_img(image,name,now)
            saves[i]['close'] = now
            saves[i]['close_img'] = img_name
            send_save_test(saves)
            break
    else:
        return None

# print('name' in get_save_test()[0])
# test_open(1,'moex')
# test_close(1,'moex')