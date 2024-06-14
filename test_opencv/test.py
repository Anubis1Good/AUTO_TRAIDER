import math
import cv2
import numpy as np
import pyautogui as pag
from scipy import stats
from scipy.spatial.distance import euclidean
pag.screenshot('Screen.png')

# image = cv2.imread('Screenshot_7.png')
image = cv2.imread('Screen.png')
# image = cv2.resize(image,(480,540))
# image = image[0:540,0:480]
image = image[550:1040,0:450]
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
# del mask1,mask2
# kernel = np.ones((2, 1), np.uint8) 
# mask = cv2.erode(mask,kernel)
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
        # cv2.drawContours(image, [approx], 0, (0, 0, 255), 2)  
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
# print(tops,bottoms)
tops = tops[tops[:,0].argsort()]
bottoms = bottoms[bottoms[:,0].argsort()]
x = np.concatenate((tops[:,0],bottoms[:,0]))
y = np.concatenate((tops[:,1],bottoms[:,1]))
# print(y)
# print(x)
cv2.polylines(image,[tops],False,(255,0,0),1)
cv2.polylines(image,[bottoms],False,(0,255,0),1)


slope, intercept, r, p, std_err = stats.linregress(x, y)

def get_points_linear_reg(x,offset):
  return int(slope * x + intercept+offset)

# print(slope)
std_y = np.std(y)
middle_line = list(map(lambda x:get_points_linear_reg(x,0), x))
top_line = list(map(lambda x:get_points_linear_reg(x,std_y), x))
bottom_line = list(map(lambda x:get_points_linear_reg(x,-std_y), x))
trend = np.column_stack([x, middle_line])
top_trend = np.column_stack([x, top_line])
bottom_trend = np.column_stack([x, bottom_line])
# print(trend)
# print(mymodel)
cv2.polylines(image,[trend],False,(255,255,255),2)
cv2.polylines(image,[top_trend],False,(255,255,255),2)
cv2.polylines(image,[bottom_trend],False,(255,255,255),2)
print(slope)
# top_border = list(map(lambda x:myfunc(x,y.std()), x))
# bottom_border = list(map(lambda x:myfunc(x,-y.std()), x))
# print(cum_sumx)
# Loop through the array elements
# def get_SMA(points):
#     moving_averages = []
#     cum_sumx = np.cumsum(points[:,0])
#     cum_sumy = np.cumsum(points[:,1])
#     i = 1 
#     while i <= len(points):
    
#         # Calculate the cumulative average by dividing
#         # cumulative sum by number of elements till 
#         # that position
#         window_averagex = cum_sumx[i-1] // i *2
#         window_averagey = cum_sumy[i-1] // i
        
#         # Store the cumulative average of
#         # current window in moving average list
#         moving_averages.append([window_averagex,window_averagey])
        
#         # Shift window to right by one position
#         i += 1
#     return np.array(moving_averages)
# print(bottoms)
# print(moving_averages)
# cv2.polylines(image,[get_SMA(tops)],False,(255,255,0),2)
# cv2.polylines(image,[get_SMA(bottoms)],False,(0,255,255),2)
# def levels(points,dir):
#     max_x = np.max(points[:,0])
#     min_x = np.min(points[:,0])
#     x = points[:,0]
#     levels = points[:,1]
#     diff = np.diff(levels)
#     p = []
#     i = 0
#     current=diff[0]
#     while i<len(levels)-1:
#         if dir:
#             if diff[i]>0 and current<0:
#                 p.append((x[i],levels[i]))
#         else:
#             if diff[i]<0 and current>0:
#                 p.append((x[i],levels[i]))

#         current = diff[i]

#         i += 1
#     p.append(points[0])
#     p.append(points[-1])
#     p = np.array(p)
#     levels = p[:,1]
#     #diff = np.diff(levels)
#     #mean = np.mean(np.abs(diff))
#     #match = abs(diff)> mean//10
#     #match =np.append(match,True)
#     #p = p[match]
#     return p
# # print(levels(tops))
# def get_extremum_points(points):
#     points_sort = points[points[:,1].argsort()]
#     return points_sort
# def get_half(points,is_left):
#     max_x = np.max(points[:,0])
#     min_x = np.min(points[:,0])
#     mean = (max_x+min_x)//2
#     left = points[points[:,0]<mean]
#     right = points[points[:,0]>mean]
#     if is_left:
#         return left
#     return right

# def angle_between(p1, p2):
#     x1, y1 = p1
#     x2, y2 = p2
#     dx = x2 - x1
#     dy = y1 - y2
#     r = math.degrees(math.pi/2 - math.atan(dx/dy))
#     if dy > 0:
#         return 90-r
#     else:
#         return 180-(r-90)


# top_rotate_point = levels(tops,True)
# bottom_rotate_point = levels(bottoms,False)
# top_rotate_point = top_rotate_point[top_rotate_point[:,0].argsort()]
# bottom_rotate_point = bottom_rotate_point[bottom_rotate_point[:,0].argsort()]

# lpt = get_extremum_points(get_half(top_rotate_point, True))[0]
# rpt = get_extremum_points(get_half(top_rotate_point, False))[0]

# lpb = get_extremum_points(get_half(bottom_rotate_point, True))[-1]
# rpb = get_extremum_points(get_half(bottom_rotate_point, False))[-1]

# angle_top = angle_between(lpt,rpt)
# angle_bottom = angle_between(lpb, rpb)

# def get_trande(angle):
#     if 0 < angle < 80:
#         return 1 
#     if 80 < angle < 100:
#         return 0
#     return -1
# def get_formation():
#     trend_top = get_trande(angle_top)
#     trend_bottom = get_trande(angle_bottom)

#     total = trend_top + trend_bottom
#     if total > 1:
#         return 'long'
#     if total < -1:
#         return 'short'
#     return 'range'

# print(get_formation())
    
# for i in top_rotate_point:
#     cv2.circle(image, i, 3, (255,200,100),-1)
# for i in bottom_rotate_point:
#     cv2.circle(image, i, 3, (155,200,200),-1)


#cv2.polylines(image,[top_rotate_point],False,(200,200,0),3)

#cv2.polylines(image,[bottom_rotate_point],False,(0,200,200),3)

# cv2.line(image,lpt,rpt,(0,200,100),2)
# cv2.line(image,lpb,rpb,(200,200,0),2)
# cv2.circle(image, lpt,5, (0,200,100),-1)
# cv2.circle(image, rpt,5, (0,200,100),-1)
# cv2.circle(image, lpb,5, (200,200,100),-1)
# cv2.circle(image, rpb,5, (200,200,100),-1)
# cv2.imwrite('output.png',image)
cv2.imshow('Chart',image)
# cv2.imshow('mask',mask)
# cv2.imshow('mask1',mask1)
cv2.waitKey(0)
cv2.destroyAllWindows()