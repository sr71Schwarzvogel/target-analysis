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
    #kernel = np.ones((3, 3), np.uint8)
    #dilation = cv2.dilate(fgmask, kernel, iterations=1)

    # dilation
    #kernel = np.ones((7, 7), np.uint8)
    #cleaned_mask = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)

    # opening
    kernel = np.ones((7, 7), np.uint8)
    cleaned_mask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    # smoothing
    # kernel = np.ones((15, 15), np.float32) / 225
    # cleaned_mask = cv2.filter2D(fgmask, -1, kernel)



    #cleaned_mask = fgmask

    # invert image
    cleaned_mask = cv2.bitwise_not(cleaned_mask)

    # blob detection
    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create()

    # Detect blobs.
    keypoints = detector.detect(cleaned_mask)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    detected_blobs = cv2.drawKeypoints(cleaned_mask, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow('fgmask', frame)
    cv2.imshow('frame', fgmask)
    cv2.imshow('outcome', detected_blobs)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()