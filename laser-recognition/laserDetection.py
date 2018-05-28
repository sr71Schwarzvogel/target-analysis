import cv2
import numpy as np
import math

nonzero = [1]
laserTrack = []

# Read Video
cap = cv2.VideoCapture('test-pictures/laser-test-video-1.mp4')

videoRunning = True
while (videoRunning):
    try:
        _, im = cap.read()
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        mask = cv2.inRange(im, 220, 255)

        # cleaning the mask
        # closing
        kernel = np.ones((3, 3), np.uint8)
        dilation = cv2.dilate(mask, kernel, iterations=1)

        # opening
        kernel = np.ones((7, 7), np.uint8)
        cleaned_mask = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)

        # get middle coordinates of white
        nonzero = np.argwhere(cleaned_mask == 255)
        x_sum = 0
        y_sum = 0
        x = 0
        y = 0
        z_counter = 1

        for z in nonzero:
            x_sum = x_sum + z[0]
            y_sum = y_sum + z[1]
            z_counter = z_counter + 1

        if x_sum != 0:
            z_counter = z_counter - 1
            x = x_sum / z_counter
            y = y_sum / z_counter

            # round up coordinates
            x = math.ceil(x)
            y = math.ceil(y)

            laserTrack.append([x, y])

        # draw line on image
        s = len(laserTrack)
        if s > 2:
            for i in range(1, s):
                p1 = laserTrack[i-1]
                p2 = laserTrack[i]
                cv2.line(im, (p1[1], p1[0]), (p2[1], p2[0]), (255, 0, 0), 2)

        cv2.imshow("original", im)
        # cv2.imshow("cleaned_mask", cleaned_mask)
        # cv2.imshow("movement", draw_pic)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    except cv2.error:
        videoRunning = False


