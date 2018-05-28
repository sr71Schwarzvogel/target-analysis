import cv2
import numpy as np
import math


x_old = -1
y_old = -1

# Read image
draw_pic = cv2.imread("test-pictures/laser-test-picture-4.jpg", cv2.IMREAD_GRAYSCALE)

# Read Video
cap = cv2.VideoCapture('test-pictures/laser-test-video-1.mp4')
nonzero = [1]
videoRunning = True
while (videoRunning):
    try:
        _, im = cap.read()
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)



        mask = cv2.inRange(im, 220, 255)

        # cleaning the mask
        #closing
        kernel = np.ones((3, 3), np.uint8)
        dilation = cv2.dilate(mask, kernel, iterations=1)

        # opening
        kernel = np.ones((7, 7), np.uint8)
        cleaned_mask = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)

        # opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # erosion = cv2.erode(mask,kernel,iterations = 1)
        # dilation = cv2.dilate(mask,kernel,iterations = 1)

        # TODO draw the locations of the laser (connections between blobs? or white points)

        # get middle coordinates of white
        nonzero = np.argwhere(cleaned_mask == 255)
        x_sum = 0
        y_sum = 0
        x = 0
        y = 0
        z_counter = 1
        print(nonzero)
        for z in nonzero:
            x_sum = x_sum + z[0]
            y_sum = y_sum + z[1]
            z_counter = z_counter + 1


        x = x_sum / z_counter
        y = y_sum / z_counter

        # round up coordinates
        x = math.ceil(x)
        y = math.ceil(y)

        # draw line on image
        if x_old != -1:
            cv2.line(cleaned_mask, (x, y), (x_old, y_old), (0, 255, 0), 2)

        
        x_old = x
        y_old = y


        cv2.imshow("original", im)
        cv2.imshow("cleaned_mask", cleaned_mask)
        #cv2.imshow("movement", draw_pic)


        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break


    except cv2.error:
        videoRunning = False

