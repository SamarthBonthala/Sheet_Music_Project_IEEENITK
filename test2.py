import cv2
import numpy as np

img = cv2.imread('ode_to_joy.jpg',0)
height, width = img.shape[:2]

"""Resizing image"""
img_res = cv2.resize(img,(int(0.5*width), int(0.5*height)))#, interpolation = cv.INTER_CUBIC)


#cv2.imshow('img_resize', img_res)
"""Otsu Binarisation"""
ret2,th2 = cv2.threshold(img_res,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
print('ret2', ret2)
#cv2.imshow('thresh', th2)

"""Canny Edge Detection"""
edges = cv2.Canny(th2,50,150,apertureSize = 3)

"""Erosion - to get only the horizontal lines
    Subtract erosion from edges to remove the staff lines"""
kernel = np.ones((1,5), np.uint8)

erosion = cv2.erode(edges, kernel, iterations = 1)
erosion_copy = erosion

cv2.imshow('erosion', erosion)

result = cv2.subtract(edges, erosion)
cv2.imshow('result', result)

"""To find the y-values of staff lines"""
sum_rows = np.sum(erosion, axis=1)
max_sum = np.amax(sum_rows)

ind = np.where(sum_rows > 0.7 * max_sum)
new_ind = ind[0][::2] + 1  ## contains y-values of staff lines

####trying out some stuff

for i in ind[0]:
    erosion[i,:] = 255

cv2.imshow('erosion2', erosion)

result2 = cv2.add(result , erosion_copy)
result2 = cv2.subtract(result2, erosion)


kernel2 = np.ones((2,2), np.uint8)
result2 = cv2.dilate(result2,kernel2,iterations = 1)

# Run length encoding
count = np.zeros(960)

for i in range(55,125):
    for j in range(960):
        if(result2[i][j]==255):
            count[j]=count[j]+1

cv2.imshow('result2', result2)

count2 = np.zeros(225-125) 

for i in range(125,225):
    for j in range(624,659):
        if(result2[i][j]==255):
            count2[i-125] = count2[i-125] + 1


########################################



ref_ind = new_ind[::5] ## Reference value for each set of 5 staff lines
ref_ind2 = new_ind[4::5]

spacing = (ref_ind2 - ref_ind)/4 ## Spacing bw 2 staff lines
""""""

#cv2.imwrite('erosion.jpg', erosion)
#cv2.imwrite('edges.jpg', edges)
#cv2.imwrite('result.jpg', result)

min_line_len = 100
max_line_gap = 20

cv2.waitKey(0)
cv2.destroyAllWindows()