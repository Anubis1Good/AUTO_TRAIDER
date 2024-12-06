import numpy as np
class ColorsBtnBGR:
    ask = (67, 67, 67)
    bid = (76, 76, 76)
    best_ask = (101, 82, 168)
    best_bid = (100, 117, 66)
    large_value_1 = (198, 140, 48)
    large_value_2 = (178, 201, 45)
    color_x = (9,0,255)
    color_x_shadow = (11,11,175)
    color_x_bb = (0,0,255)

    cur_price_1 = (96,118,50)
    cur_price_2 = (75,75,173)

    candle_color_1 = (111,111,111)
    candle_color_2 = (200,200,200)

    volume_color_1 = (92,107,61)
    volume_color_2 = (89,89,128)

class TemplateCandle:
    candle_top = np.array([
        [0,0,0],
        [0,255,0]
    ],dtype=np.uint8)

    candle_bottom = np.array([
        [0,255,0],
        [0,0,0]
    ],dtype=np.uint8)

    volume_top = np.array([
        [0,0,0,0],
        [0,255,255,0]
    ],dtype=np.uint8)

class ColorsBtnGray:
    ask = 67
    bid = 76
    best_ask = 109
    best_bid = 99
    large_value_1 = 119
    large_value_2 = 151
    color_x = 80
    color_x_shadow = 70
    color_x_bb = 75
    cur_price_1 = 95
    cur_price_2 = 104
    candle_color_1 = 111
    candle_color_2 = 200
    volume_color_1 = 92
    volume_color_2 = 101
