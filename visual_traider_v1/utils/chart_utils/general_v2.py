import cv2
import numpy as np
import numpy.typing as npt
import pytesseract as tsrct
from utils.config import ColorsBtnBGR

def get_candle_mask(image:npt.ArrayLike) -> npt.ArrayLike:
    mask1 = cv2.inRange(image,ColorsBtnBGR.candle_color_1,ColorsBtnBGR.candle_color_1)
    mask2 = cv2.inRange(image,ColorsBtnBGR.candle_color_2,ColorsBtnBGR.candle_color_2)
    mask = cv2.add(mask1,mask2)
    kernel = np.ones((2, 1), np.uint8) 
    mask = cv2.erode(mask,kernel)
    return mask

def get_volume_mask(image:npt.ArrayLike) -> npt.ArrayLike:
    mask1 = cv2.inRange(image,ColorsBtnBGR.volume_color_1,ColorsBtnBGR.volume_color_1)
    mask2 = cv2.inRange(image,ColorsBtnBGR.volume_color_2,ColorsBtnBGR.volume_color_2)
    mask = cv2.add(mask1,mask2)
    return mask

def get_cords_on_mask(mask:npt.ArrayLike) -> npt.NDArray:
    cords = np.argwhere(mask == 255)
    return cords

def get_statistic_volume(cords:npt.NDArray):
    max_val = (10,np.min(cords[:,:1]))
    mean_val = (10,int(np.mean(cords,axis=0)[0]))
    return mean_val,max_val

def get_corners(mask:npt.ArrayLike) -> npt.NDArray:
    corners = cv2.goodFeaturesToTrack(mask,3000,0.01,1)
    corners = np.intp(corners) 
    shape = corners.shape
    corners = corners.reshape((shape[0],shape[2]))
    corners = corners[corners[:, 0].argsort()]
    return corners

def get_divide_chart(corners:npt.NDArray,divider:int=3) -> tuple:
    last_i = 0
    len_corners = len(corners)
    step = len_corners//divider
    corners = corners[corners[:, 1].argsort()]
    regions = []
    for i in range(step-1,len_corners,step):
        if len_corners - i < step:
            distict = corners[last_i:len_corners-1]
        else:
            distict = corners[last_i:i]
        last_i = i

        y_max = np.max(distict[:,1:])
        x_max = np.max(distict[:,:1])
        y_min = np.min(distict[:,1:])
        x_min = np.min(distict[:,:1])
        regions.append((x_min,y_min,x_max,y_max))
    return tuple(regions)

def get_xy(corners:npt.NDArray) -> npt.NDArray:
    x = corners[:,0]
    y = corners[:,1]
    return x,y

def get_cur_price(self,chart):
    mask1 = self._get_mask(chart,ColorsBtnBGR.cur_price_1)
    mask1 = self._get_cords_on_mask(mask1)
    mask2 = self._get_mask(chart,ColorsBtnBGR.cur_price_2)
    mask2 = self._get_cords_on_mask(mask2)
    if mask1.shape[0] > 0:
        mask = mask1
    if mask2.shape[0] > 0:
        mask = mask2
    region_price = (mask[0][1],mask[0][0],mask[-1][1],mask[-1][0])
    price_chart = self._get_chart(chart,region_price)
    pc_copy = price_chart.copy()
    pc_copy = cv2.resize(pc_copy,None,fx=9,fy=9)
    tsrct.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    res = tsrct.image_to_string(pc_copy, config='outputbase digits')
    return res
