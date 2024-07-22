import cv2
import numpy as np
from traider_bots.VisualTraider_v2 import VisualTraider_v2
def draw_borders(img,traider:VisualTraider_v2):
    attrs = vars(traider)
    for item in attrs.items():
        i = item[1]
        if type(i) == tuple:
            if len(i) == 4:
                points = np.array([[i[0],i[1]],[i[2],i[1]],[i[2],i[3]],[i[0],i[3]]], np.int32)
                cv2.polylines(img,[points],True,(255,0,0),1)
    cv2.imwrite('windows.png',img)


