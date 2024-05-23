import pyautogui as pag
import pydirectinput as pdi
from utils.config import ColorsBtnBGR
from utils.conditions import check_req
from utils.utils import color_search


# long_request
# help functions
def check_lr(image,region):
    xbb,ybb = color_search(image,ColorsBtnBGR.best_bid,region)
    if xbb > 0:
        new_region = (xbb,ybb,region[2],region[3])
        x,y = color_search(image,ColorsBtnBGR.large_value_2,new_region)
        delta = y - ybb
        if delta < 300:
            return x,y
    return -1,-1

def reset_and_click_lr(x,y):
    pag.moveTo(x,y)
    pdi.press('f')
    pag.click(x, y-10)

# work functions
def click_lr(image,region):
    x,y = check_lr(image,region)
    if x > 0:
        reset_and_click_lr(x,y)

def click_bl(image,region):
    pag.moveTo(region[0]+10,region[1]+10)
    pdi.press('f')
    pdi.press('a')

    # x,y = color_search(image, ColorsBtnBGR.best_bid,region)
    # if x > 0:
    #     reset_and_click_lr(x,y)


def reset_lr(image,region):
    xr,yr = check_req(image, region)
    if xr > 0:
        xnr,ynr = check_lr(image,region)
        if xnr > 0:
            delta = yr-ynr
            if delta > 20:
                reset_and_click_lr(xnr,ynr)
# bid          
# help functions


def check_sr(image,region):
    xbb,ybb = color_search(image,ColorsBtnBGR.best_bid,region)
    if xbb > 0:
        new_region = (region[0],region[1]-11,xbb,ybb)
        x1,y1 = color_search(image,ColorsBtnBGR.large_value_1,new_region,reverse=True)
        x2,y2 = color_search(image,ColorsBtnBGR.large_value_2,new_region,reverse=True)
        if y1 > y2:
            return x1,y1
        else:
            return x2,y2
    else:
        return -1,-1


def reset_and_click_sr(x,y):
    pag.moveTo(x,y)
    pdi.press('f')
    pdi.keyDown('altleft')
    pag.click(x, y,button='right')
    pdi.keyUp('altleft')

    

# work functions
def click_sr(image,region):
    x,y = check_sr(image,region)
    if x > 0:
        reset_and_click_sr(x,y+10)

def click_bs(image,region):
    x,y = color_search(image, ColorsBtnBGR.best_ask,region,reverse=True)
    if x > 0:
        reset_and_click_sr(x-50,y-5)

def reset_sr(image,region):
    xr,yr = check_req(image, region)
    if xr > 0:  
        xbb,ybb = color_search(image,ColorsBtnBGR.best_ask,region,reverse=True)
        xnr,ynr = check_sr(image,region)
        if xnr > 0:
            delta = ynr - yr
            if delta > 20 or ybb < yr:
                reset_and_click_sr(xnr,ynr) 
                    

# wait function
def not_idea(image,region):
    xr,yr = check_req(image, region)
    if xr > 0: 
        pag.moveTo(xr,yr)
        pdi.press('f')

def idle(image,region):
    pass