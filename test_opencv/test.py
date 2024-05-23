import cv2
import numpy as np

image = cv2.imread('Screenshot_7.png')
# image = cv2.resize(image,(480,540))
# image = image[0:540,0:480]
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
color1 = np.array([111,111,111])
color2 = np.array([200,200,200])
# mask = image.copy()
# mask[(mask[:,:,0] != 111) & (mask[:,:,1] != 111) & (mask[:,:,2] != 111)] = np.array([0,0,0])
# mask2 = image.copy()
# mask2[(mask2[:,:,0] != 200) & (mask2[:,:,1] != 200) & (mask2[:,:,2] != 200)] = np.array([0,0,0])
# mask = mask + mask2
# _,mask = cv2.threshold(mask,100,255, cv2.THRESH_BINARY)
# print(mask)
mask1 = cv2.inRange(image,color1,color1)
mask2 = cv2.inRange(image,color2,color2)
mask = cv2.add(mask1,mask2)
kernel = np.ones((2, 1), np.uint8) 
# mask1 = cv2.erode(mask1,kernel)
mask = cv2.erode(mask,kernel)
# mask = cv2.medianBlur(mask,5)

# # image = cv2.bitwise_and(image,image,mask=mask)
# countours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# for cnt in countours:
#     approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt,True),True)
#     cv2.drawContours(image, [approx], 0, (0, 0, 255), 1)  
# cv2.imwrite('output.png',image)
# cv2.imshow('Chart',image)
cv2.imshow('mask',mask)
# cv2.imshow('mask1',mask1)
cv2.waitKey(0)
cv2.destroyAllWindows()