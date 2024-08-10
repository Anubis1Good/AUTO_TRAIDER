import cv2
from utils.chart_utils.archive.general import get_trend_lines,get_four_points_and_slope
from utils.chart_utils.indicators import get_trend_lines

# for VT before v2
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
    cv2.putText(image, str(round(slope,2)), (30, 30) , cv2.FONT_HERSHEY_SIMPLEX,  
                   1, (255, 255, 255), 3, cv2.LINE_AA)
    return image

# for VT after v2
def draw_trendlines_v2(x,y,image):
    trend,top_trend,bottom_trend = get_trend_lines(x,y)
    cv2.polylines(image,[trend],False,(255,255,255),2)
    cv2.polylines(image,[top_trend],False,(255,255,255),2)
    cv2.polylines(image,[bottom_trend],False,(255,255,255),2)

def draw_bollinger(chart,ma,ups,downs,color=(200,0,0),thickness=1):
    cv2.polylines(chart,[ma],False,color,thickness)
    cv2.polylines(chart,[ups],False,color,thickness)
    cv2.polylines(chart,[downs],False,color,thickness)