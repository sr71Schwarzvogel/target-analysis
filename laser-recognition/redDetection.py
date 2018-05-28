import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while (1):
    #_, frame = cap.read()
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    frame = cv2.imread('test-pictures/laser-test-bild-4.jpg')
    # hsv = cv2.rgb2hsv(rgb)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    #hsv hue sat value
    lower_red = np.array([135, 5, 200])
    upper_red = np.array([160,100, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    #cv2.imshow('res', res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()