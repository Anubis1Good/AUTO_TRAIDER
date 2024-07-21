import cv2
import numpy as np
image = cv2.imread('Screenshot_6.png')
image = cv2.imread('./09.07.24/images/SBER1720516220.255987.png')
# image = image[0:540,0:480]
print(image.shape)
image = image[None:None,None:None]
print(image.shape)
# constantes colors
color1 = np.array([111,111,111])
color2 = np.array([200,200,200])
color_val1 = np.array([92,107,61])
color_val2 = np.array([89,89,128])

# get masks
mask_val1 = cv2.inRange(image,color_val1,color_val1)
mask_val2 = cv2.inRange(image,color_val2,color_val2)
mask_val = cv2.add(mask_val1,mask_val2)
mask1 = cv2.inRange(image,color1,color1)
mask2 = cv2.inRange(image,color2,color2)
mask = cv2.add(mask1,mask2)
del mask2,mask1,mask_val1,mask_val2
kernel = np.ones((2, 1), np.uint8) 
mask = cv2.erode(mask,kernel)

# get_volume statistic points
cords_val = np.argwhere(mask_val == 255)
max_val = np.min(cords_val[:,:1])
mean_val = int(np.mean(cords_val,axis=0)[0])
corners = cv2.goodFeaturesToTrack(mask_val,1000,0.01,1)
corners = np.int32(corners) 

for i in corners: 
    x, y = i.ravel() 
    cv2.circle(mask_val, (x, y), 1, (120,0,0), -1) 

# get chart points
cords_charts = np.argwhere(mask == 255)
mean_charts = np.mean(cords_charts,axis=1)
corners = cv2.goodFeaturesToTrack(mask,1000,0.01,1)
corners = np.int0(corners) 
shape = corners.shape
corners = corners.reshape((shape[0],shape[2]))
corners = corners[corners[:, 0].argsort()]
# print(corners)
for i in range(1,len(corners)-1): 
    x1, y1 = corners[i].ravel()
    x0, y0 = corners[i-1].ravel()
    x2, y2 = corners[i+1].ravel()
    if  y0 >= y1 <= y2 or y0 <= y1 >= y2:
    # if  x0 >= x1 <= x2 or x0 <= x1 >= x2:
        cv2.circle(image, (x1, y1), 2, (20,200,0), -1) 
    cv2.circle(mask, (x1, y1), 1, (120,0,0), -1) 
last_i = 0
len_corners = len(corners)
step = len_corners//5
# print(len_corners)
for i in range(step-1,len_corners,step):
    print(i)
    if len_corners - i < step:
        distict = corners[last_i:len_corners-1]
    else:
        distict = corners[last_i:i]
    last_i = i

    y_max = np.max(distict[:,1:])
    x_max = np.max(distict[:,:1])
    y_min = np.min(distict[:,1:])
    x_min = np.min(distict[:,:1])
    
    cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,0,200),2)
    # cv2.circle(image,(y_max,x_max),3,(0,100,200),-1)
# print(cords_charts)
# print(mean_charts)

# draw in image
cv2.line(image,(0,mean_val),(400,mean_val),(250,200,10),2)
# cv2.line(image,(0,max_val),(400,max_val),(200,200,9),2)

# experiment
# mask = cv2.blur(mask,(100,100))
# show images
cv2.imshow('chart',image)
cv2.imshow('mask',mask)
cv2.imshow('mask_val',mask_val)
cv2.imwrite('mask_val.png',mask_val)
cv2.waitKey(0)
