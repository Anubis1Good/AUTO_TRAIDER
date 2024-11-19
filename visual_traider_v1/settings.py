import json
import os
import shutil
# for VisualTraider before v2
def configurtion_traiders(Traider,filename):
    traiders = []
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split('-')
            glass = tuple(map(int,line[0].split(',')))
            chart = tuple(map(int,line[1].split(',')))
            traiders.append(Traider(glass,chart))
    return traiders

def configuration_traiders_v2(filename:str):
    fields = []
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            field = tuple(map(int,line.split(',')))
            fields.append(field)
    return fields

def reset_test_json():
    saves = [
        {
        "name": "moex",
        "open": "2024-06-14 16:05:29.360793",
        "close": "2024-06-14 16:08:51.910451",
        "open_image": "./test_images/none.png",
        "close_img": "./test_images/none.png",
        "pos": "long",
        "traider": "VisualTraider"
        }
    ]
    with open('test.json','w') as f:
        json.dump(saves,f)

def reset_fast_test_json():
    saves = [
        {
        "name": "pupse",
        "open": True,
        "close": True,
        "pos": "long",
        "trader": "VT"
        }
    ]
    with open('test_files/fast_test.json','w') as f:
        json.dump(saves,f)

def clear_test_images():
    shutil.rmtree('./test_images') 
    os.mkdir('./test_images')
def clear_logs():
    shutil.rmtree('./logs') 
    os.mkdir('./logs')
    
if __name__ == '__main__':
    print(configuration_traiders_v2('./config_dev.txt'))
