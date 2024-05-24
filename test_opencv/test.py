import cv2
import numpy as np

image = cv2.imread('Screenshot_6.png')
# image = cv2.resize(image,(480,540))
image = image[0:540,0:480]
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
mask = cv2.erode(mask,kernel)
# mask1 = cv2.erode(mask1,kernel)
# mask = cv2.medianBlur(mask,5)

# image = cv2.bitwise_and(image,image,mask=mask)
countours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
tops = []
bottoms = []
for cnt in countours:
    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt,True),True)
    # approx = cnt
    area = cv2.contourArea(approx)
    if area > 5:
        bottom = np.max(approx,0)[0]
        top = np.min(approx,0)[0]
        mean = np.mean(approx,0,int)[0]
        bottom_point = (mean[0],bottom[1])
        top_point = (mean[0],top[1])
        # print(mean)
        # print(top,bottom)
        cv2.drawContours(image, [approx], 0, (0, 0, 255), 2)  
        # image[top[1],top[0]] = [255,0,0]
        cv2.circle(image, top_point,2, (255,0,0),-1)
        cv2.circle(image, bottom_point,2, (0,255,0),-1)
        tops.append(top_point)
        bottoms.append(bottom_point)
        # cv2.circle(image, top,2, (255,0,0),-1)
        # cv2.circle(image, bottom,2, (0,255,0),-1)
        # cv2.circle(image, mean,1, (255,255,0),-1)
tops = np.array(tops)
bottoms = np.array(bottoms)
tops = tops[tops[:,0].argsort()]
bottoms = bottoms[bottoms[:,0].argsort()]
cv2.polylines(image,[tops],False,(255,0,0),1)
cv2.polylines(image,[bottoms],False,(0,255,0),1)
# cv2.imwrite('output.png',image)
cv2.imshow('Chart',image)
cv2.imshow('mask',mask)
# cv2.imshow('mask1',mask1)
cv2.waitKey(0)
cv2.destroyAllWindows()