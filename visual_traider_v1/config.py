import os
# class ImagesBtn():
work_dir = os.getcwd()
path = os.path.join(work_dir,'buttons\\')

class ImagesBtns:
    get_long = os.path.join(path,'Long_1.png')
    get_short = os.path.join(path, 'Short_1.png')
    header = os.path.join(path,'Header.png')
    has_bid = os.path.join(path,'Has_bid.png')
    has_bid_bb = os.path.join(path,'hBB.png')
    has_bid_ba = os.path.join(path,'hBA.png')
    has_long = os.path.join(path,'Has_long1.png')

    best_bid = os.path.join(path,'BB.png')
    best_bid = os.path.join(path,'BB_full.png')
    best_ask = os.path.join(path,'BA.png')
    plate_bid = os.path.join(path,'Plate_bid.png')
    plate_ask = os.path.join(path,'Plate_ask.png')
    plate_bid_full = os.path.join(path,'Plate_bid_full.png')
    plate_ask_full = os.path.join(path,'Plate_ask_full.png')

class ColorsBtnBGR:
    ask = (67, 67, 67)
    bid = (76, 76, 76)
    best_ask = (101, 82, 168)
    best_bid = (100, 117, 66)
    large_value_1 = (198, 140, 48)
    large_value_2 = (178, 201, 45)
    color_x = (0,0,255)
    color_x_shadow = (11,11,177)
