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
    
def check_bid(region) ->tuple | bool:
    try:
        location = pag.locateOnScreen(ImagesBtns.has_bid, grayscale=True,confidence=0.8, region=region)
        return pag.center(location)
    except:
        try:
            location = pag.locateOnScreen(ImagesBtns.has_close, grayscale=False,confidence=0.8, region=region)
            return pag.center(location)
        except:
            try:
                location = pag.locateOnScreen(ImagesBtns.has_bid_2, grayscale=False,confidence=0.8, region=region)
                return pag.center(location)
            except:
                return False
    
    

    