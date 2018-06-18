import numpy as np
import cv2

cap = cv2.VideoCapture('test-pictures/shot-test-video-1.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2()

while (1):
    ret, frame = cap.read()

    # TODO "intelligent" focus on the target
    frame = frame[130:450, 550:914]

    fgmask = fgbg.apply(frame)

    # TODO clean the image

    # cleaning the mask
    # closing
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(fgmask, kernel, iterations=1)

    # dilation
    kernel = np.ones((7, 7), np.uint8)
    cleaned_mask = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)


    cv2.imshow('fgmask', frame)
    cv2.imshow('frame', fgmask)
    cv2.imshow('cleaned mask', cleaned_mask)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()