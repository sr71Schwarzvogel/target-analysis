import matplotlib as mlp
import matplotlib.pyplot as plt
import cv2
import time

point_list = []

# Print laser
f = open('data.txt', 'r')
img = cv2.imread('target2.jpeg', cv2.IMREAD_COLOR)
cv2.imshow("1", img)
img2 = cv2.resize(img, (300, 300))
cv2.imshow("2", img2)
k = cv2.waitKey(30) & 0xff
if k == 27:
    cv2.destroyAllWindows()
