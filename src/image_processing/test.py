import cv2
import numpy as np

# Read input image
img = cv2.imread(
    '/home/patryk/Pulpit/Handwriting-synthesis-with-the-help-of-machine-learning/data/a01-000u.png')

scale_percent = 25

# calculate the 50 percent of original dimensions
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)

# dsize
dsize = (width, height)
blank_image = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)


# convert from BGR to HSV color space
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# apply threshold
thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

# find contours and get one with area about 180*35
# draw all contours in green and accepted ones in red
contours = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
# contours = contours[0] if len(contours) == 2 else contours[1]

contours = sorted(contours, key=lambda c: cv2.boundingRect(c)
                  [2], reverse=False)[:100]
# #area_thresh = 0
# min_area = 0
# max_area = 1000000

#area_thresh = 0
min_area = 0
max_area = 1000000
result = img.copy()

for c in contours:
    area = cv2.contourArea(c)
    cv2.drawContours(result, [c], -1, (0, 255, 0), 1)
    cv2.drawContours(blank_image, [c], -1, (255, 255, 255), 1)
    if area > min_area and area < max_area:
        cv2.drawContours(result, [c], -1, (0, 0, 255), 1)

# save result
cv2.imwrite("box_found.png", result)

# show images
# cv2.imshow("GRAY", gray)
cv2.imshow("THRESH", thresh)
output = cv2.resize(result, dsize)
# cv2.imshow("RESULT", output)
blank_image = cv2.resize(blank_image, dsize)
# cv2.imshow("Black", blank_image)
cv2.waitKey(0)
