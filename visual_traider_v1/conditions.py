'''
1. Проверка наличия позиции -> Need_close
2. Проверка наличия заявки на закрытие позиции -> Has_close
3. Проверка наличия заявки на открытие позиции -> Has_bid
4. Иначе -> Send_bid
'''
from config import ColorsBtnBGR
from utils import color_search

def check_pos(img,region)->tuple | bool:
    
    x,y = color_search(img,ColorsBtnBGR.best_bid,region) 
    return x >= 0



def check_req(img,region) ->tuple | bool:
    x,y = color_search(img,ColorsBtnBGR.color_x_shadow,region)
    if x>0:
        return x,y
    else:
        x,y = color_search(img,ColorsBtnBGR.color_x,region)
        return x,y

    