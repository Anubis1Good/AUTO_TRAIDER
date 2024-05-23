# import cv2
# import pyautogui as pag
# import easyocr
# import pprint 

# pag.screenshot('our_screen.png')
# print(pag.size())
# region = (4,25,95,50)

# reader = easyocr.Reader(['en'],True)
# img = cv2.imread('our_screen.png')
# result = reader.readtext(img[25:50,4:95])
# for r in result:
#     if 'VTBR' in r:
#         print(r[0][0][0]+4,r[0][0][1]+25)
#         x = r[0][0][0]+4
#         y = r[0][0][1]+25
#         pag.moveTo(500,500)
#         pag.moveTo(220,1063) #разница экранов

# # if 'RENI' in result:
# #     print('yes')
# # else:
# #     print('No')
# pprint.pprint(result)
# print(img[0][0])
# cv2.imshow('img',img)
# cv2.waitKey(0)