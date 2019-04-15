import cv2 as cv
import numpy as np
import time

cap = cv.VideoCapture("/Users/adityakumar/Downloads/Input.mp4")

time.sleep(3)

background = 0

# Extracting background pixels
for i in range(30):
    ret, background = cap.read()

out = cv.VideoWriter("output.avi", cv.VideoWriter_fourcc(*"MJPG"), 10, (1280, 720))
while(cap.isOpened()):

    ret, img = cap.read()
    if not ret:
        break
# Converting image from RGB color space to HSV color space
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
# Extracting Red color cloth
    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    mask1 = cv.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv.inRange(hsv, lower_red, upper_red)

    mask1=mask1+mask2


    mask1 = cv.morphologyEx(mask1, cv.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations = 2)
    mask1 = cv.dilate(mask1, np.ones((3, 3), np.uint8), iterations=2)

# Segmenting the cloth out of the frame
    mask2 = cv.bitwise_not(mask1)

    res1 = cv.bitwise_and(img, img, mask=mask2)

    res2 = cv.bitwise_and(background, background, mask = mask1)

# Generating final output
    final = cv.addWeighted(res1, 1, res2, 1, 0)

    cv.imshow("boom", final)


    k = cv.waitKey(10)
    if k == 27:
        break
