import cv2
import numpy as np

# cap = cv2.VideoCapture(0)

while (1):
    # _, frame = cap.read()
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    frame = cv2.imread('test-pictures/shot_target_20.jpg')
    # hsv = cv2.rgb2hsv(rgb)
    # frame = frame[1000:1000, 1500:2500]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # hsv hue sat value
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([255, 255, 150])

    # find black
    mask = cv2.inRange(hsv, lower_black, upper_black)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # invert colors
    mask2 = cv2.inRange(mask, 0, 100)

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create()

    # Detect blobs.
    keypoints = detector.detect(mask2)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


    cv2.imshow('frame', im_with_keypoints)
    cv2.imshow('mask', mask2)
    #cv2.imshow('res', res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()