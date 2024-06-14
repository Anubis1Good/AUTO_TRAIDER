# test function
import json
from datetime import datetime
def get_save_test():
    saves = []
    with open('test.json') as f:
        saves = json.load(f)
    return saves
def send_save_test(saves):
    with open('test.json','w') as f:
        json.dump(saves,f)
def test_open(image,name):
    saves = get_save_test()
    saves_length = len(saves)
    for i in range(saves_length-1,-1,-1):
        if saves[i]['name'] == name and not saves[i]['close']:
            return None
    saves.append({
        "name":name,
        "open":str(datetime.now()),
        "close":""
    })
    send_save_test(saves)

def test_close(image,name):
    saves = get_save_test()
    saves_length = len(saves)
    for i in range(saves_length-1,-1,-1):
        if saves[i]['name'] == name and not saves[i]['close']:
            saves[i]['close'] = str(datetime.now())
            send_save_test(saves)
            break

# print('name' in get_save_test()[0])
# test_open(1,'moex')
# test_close(1,'moex')