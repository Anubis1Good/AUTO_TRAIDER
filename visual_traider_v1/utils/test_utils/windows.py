import cv2
import numpy as np
from traider_bots.VisualTraider import  VisualTraider
def draw_borders(img,traiders: list[VisualTraider]):
    for t in traiders:
        points = np.array([[t.region_glass[0],t.region_glass[1]],[t.region_glass[2],t.region_glass[3]]], np.int32)
        cv2.polylines(img,[points],True,(255,0,0),5)
        points = np.array([[t.region_chart[0],t.region_chart[1]],[t.region_chart[2],t.region_chart[3]]], np.int32)
        cv2.polylines(img,[points],True,(255,0,0),5)

    cv2.imwrite('windows.png',img)


