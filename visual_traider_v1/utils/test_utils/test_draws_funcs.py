import cv2
from utils.chart_utils.general import get_trend_lines,get_four_points_and_slope

def draw_trendlines(image):
    slope,top_trend,bottom_trend = get_trend_lines(image)
    color = (250,250,250)
    cv2.polylines(image,[top_trend],False,color,3)
    cv2.polylines(image,[bottom_trend],False,color,3)
    return image

def draw_four_points(image):
    slope, points = get_four_points_and_slope(image)
    colors = ((200,200,0),(150,150,0),(0,200,200),(0,150,150))
    for i in range(4):
        cv2.circle(image,points[i],1,colors[i],3)
    return image