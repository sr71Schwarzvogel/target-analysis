import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

# https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
target_cascade = cv2.CascadeClassifier('cascade 5.xml')


# cap = cv2.VideoCapture(0)

while 1:
    # ret, img = cap.read()
    img = cv2.imread('test-pictures/shot_target_20.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    targets = target_cascade.detectMultiScale(gray, 1.3, 5)
    print(targets)
    for (x, y, w, h) in targets:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# cap.release()
cv2.destroyAllWindows()