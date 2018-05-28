import cv2
import numpy as np;

# Read image
# im = cv2.imread("test-pictures/laser-test-picture-4.jpg", cv2.IMREAD_GRAYSCALE)

# Read Video
cap = cv2.VideoCapture('test-pictures/laser-test-video-1.mp4')
while 1:

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

    # cv2.imshow("original", im)
    cv2.imshow("cleaned_mask", cleaned_mask)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
