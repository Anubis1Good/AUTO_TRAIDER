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
