'''
1. Проверка наличия позиции -> Need_close
2. Проверка наличия заявки на закрытие позиции -> Has_close
3. Проверка наличия заявки на открытие позиции -> Has_bid
4. Иначе -> Send_bid
'''
from config import ImagesBtns
import pyautogui as pag

def check_pos(region)->tuple | bool:
    try:
        pag.locateOnScreen(ImagesBtns.has_long,grayscale=False, region=region)
        return True
    except:
        return False

def search_bid(btn,region,grayscale):
    location = pag.locateOnScreen(btn, grayscale=grayscale,confidence=0.8, region=region)
    return pag.center(location)

def check_bid(region) ->tuple | bool:
    try:
        return search_bid(ImagesBtns.has_bid,region,True)
    except:
        try:
            return search_bid(ImagesBtns.has_bid_ba,region, False)
        except:
            try:
                return search_bid(ImagesBtns.has_bid_bb,region, False)
            except:
                return False
        
    