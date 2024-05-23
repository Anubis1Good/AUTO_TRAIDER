import numpy as np
import numpy.typing as npt
# region - (x1,y1,x2,y2)

def color_search(img:npt.ArrayLike,color:tuple[int],region:tuple[int],reverse:bool=False):
    try:
        result = np.argwhere(
            (img[region[1]:region[3],region[0]:region[2],0] == color[0])& 
            (img[region[1]:region[3],region[0]:region[2],1] == color[1])& 
            (img[region[1]:region[3],region[0]:region[2],2] == color[2])
        )
        y = -1 if reverse else 0
        

        return result[y,1]+region[0], result[y,0]+region[1]
    except:
        return -1,-1

# pag.moveTo(x[-1,1],x[-1,0])
# pag.moveTo(x[0,1],x[0,0])
    
def convertHEXtoRGB(color: str) -> tuple:
    colors_hex = [color[3:5],color[5:7],color[7:]]
    colors_rgb = []
    for c in colors_hex:
        colors_rgb.append(int(c,16))
    return tuple(colors_rgb)

# print(convertHEXtoRGB('#FF434343'))
# print(convertHEXtoRGB('#FF4C4C4C'))
# print(convertHEXtoRGB('#FFA85265'))
# print(convertHEXtoRGB('#FF427564'))
# print(convertHEXtoRGB('#FF308CC6'))
# print(convertHEXtoRGB('#FF2DC9B2'))
