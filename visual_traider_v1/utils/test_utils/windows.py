import cv2
from traider_bots.VisualTraider import  VisualTraider
def draw_borders(img,traiders: list[VisualTraider]):
    for t in traiders:
        cv2.polylines(img,[[(t.region_glass[0],t.region_glass[1]),(t.region_glass[2],t.region_glass[3])]],True,(255,0,0),5)
    cv2.imwrite('windows.png',img)