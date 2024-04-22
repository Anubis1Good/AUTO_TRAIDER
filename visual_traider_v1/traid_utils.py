import pyautogui as pag
from config import ImagesBtns
from conditions import check_bid

# ask
# help functions
def check_ask_btn(image,region):
        btn = pag.locateOnScreen(image,grayscale=False,region=region)
        return btn

def reset_and_click_ask(btn):
    with pag.hold('altleft'):
        pag.moveTo(btn)
        pag.press('f')
        pag.click(btn.left, btn.top-10)

# work functions
def click_ask(region):
    try:
        btn = check_ask_btn(ImagesBtns.plate_ask,region)
        reset_and_click_ask(btn)
    except:
        try:
            btn = check_ask_btn(ImagesBtns.plate_ask_full,region)
            reset_and_click_ask(btn)
        except:
            pag.PAUSE
            print('не найден аск')

def reset_ask(region):
    try:
        new_btn = check_ask_btn(ImagesBtns.plate_ask,region)
        old_btn = check_bid(region)
        if old_btn[1] > new_btn[1]:
            reset_and_click_ask(new_btn)
    except:
        try:
            new_btn = check_ask_btn(ImagesBtns.plate_ask_full,region)
            old_btn = check_bid(region)
            if old_btn[1] > new_btn[1]:
                reset_and_click_ask(new_btn)
        except:
            pag.PAUSE
# bid          
# help functions
def check_bid_btn(image,region):
    bid = pag.locateAllOnScreen(image,grayscale=False,region=region)
    return list(bid)[-1]

def reset_and_click_bid(btn):
    with pag.hold('altleft'):
        pag.moveTo(btn)
        pag.press('f')
        pag.click(btn.left, btn.top+10,button='right')

# work functions
def click_bid(region):
    try:
        btn = check_bid_btn(ImagesBtns.plate_bid, region)
        reset_and_click_bid(btn)
    except:
        try:
            btn = check_bid_btn(ImagesBtns.plate_bid_full, region)
            reset_and_click_bid(btn)
        except:
            pag.PAUSE
            print('sd')

def reset_bid(region):
    try:
        new_btn = check_bid_btn(ImagesBtns.plate_bid, region)
        old_btn = check_bid(region)
        if new_btn[1] > old_btn[1]:
            reset_and_click_bid(new_btn)
    except:
        try:
            new_btn = check_bid_btn(ImagesBtns.plate_bid_full, region)
            old_btn = check_bid(region)
            if new_btn[1] > old_btn[1]:
                reset_and_click_bid(new_btn)
        except:
            pag.PAUSE

