'''
1. Проверка наличия позиции -> Need_close
2. Проверка наличия заявки на закрытие позиции -> Has_close
3. Проверка наличия заявки на открытие позиции -> Has_bid
4. Иначе -> Send_bid
'''
from utils.config import ColorsBtnBGR
from utils.utils import color_search

def check_pos(img,region)->tuple | bool:
    
    x,y = color_search(img,ColorsBtnBGR.best_bid,region) 
    return x >= 0



def check_req(img,region) ->tuple | bool:
    x,y = color_search(img,ColorsBtnBGR.color_x_shadow,region)
    if x>0:
        return x,y
    else:
        x,y = color_search(img,ColorsBtnBGR.color_x,region)
        if x > 0:
            return x,y
        else:
            x,y = color_search(img,ColorsBtnBGR.color_x_bb,region)
            return x,y

    
def help_graphic_level(img,region,color,buy_level,sell_level):
    x,y = color_search(img,color,region)
    if y>0:
        if region[3] > y > buy_level:
            return 'buy'
        if region[1] < y < sell_level:
            return 'sell'
        return 'wait'
    return 'Not found'

def check_graphic_level(img,region):
    graphic_part = (region[3] - region[1])
    long_zone = graphic_part//5
    short_zone = graphic_part//3
    buy_level = region[3] - long_zone
    sell_level = region[1] + short_zone
    result = help_graphic_level(img,region,ColorsBtnBGR.cur_price_1,buy_level,sell_level)
    if result == 'Not found':
        result = help_graphic_level(img,region,ColorsBtnBGR.cur_price_2,buy_level,sell_level)
        return result
    return result
