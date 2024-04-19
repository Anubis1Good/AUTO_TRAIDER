import pyautogui as pag
from config import ImagesBtns
from conditions import check_bid

def click_bid(region):
    try:
        bid = pag.locateOnScreen(ImagesBtns.get_long,grayscale=False,region=region)
        pag.moveTo(bid)
        pag.press('f')
        pag.click(bid.left, bid.top+1)
    except:
        pag.PAUSE

def reset_bid(region):
    try:
        new_bid = pag.locateOnScreen(ImagesBtns.get_long,grayscale=False,region=region)
        old_bid = check_bid(region)
        if new_bid[1] < old_bid[1]:
            pag.moveTo(new_bid)
            pag.press('f')
            pag.click(new_bid.left, new_bid.top+1)

    except:
        pag.PAUSE

def click_close(region):
    try:
        bid = pag.locateAllOnScreen(ImagesBtns.get_short,grayscale=False,region=region)
        bid = list(bid)[-1]
        pag.moveTo(bid)
        pag.press('f')
        pag.click(bid.left, bid.top+10,button='right')
    except:
        pag.PAUSE

def reset_close(region):
    try:
        new_bid = pag.locateAllOnScreen(ImagesBtns.get_short,grayscale=False,region=region)
        new_bid = list(new_bid)[-1]
        old_bid = check_bid(region)
        if new_bid[1] > old_bid[1]:
            pag.moveTo(new_bid)
            pag.press('f')
            pag.click(new_bid.left, new_bid.top+10,button='right')

    except:
        pag.PAUSE
