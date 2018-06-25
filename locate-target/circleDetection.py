import cv2

# cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('test-pictures/shot_video_1.mp4')

contour_list = []
contour_rec_counter = 0
x_min = 10000
x_max = 0
y_min = 10000
y_max = 0

while 1:

    _,raw_image = cap.read()
    #raw_image = cv2.imread('test-pictures/shot_target_20.jpg')


    # find edges
    bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
    _, contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #identify circles
    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)

        # if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)):
        if (len(approx) > 10) &  (len(approx) < 30) & (area > 15000) & (area < 90000):
            contour_list.append(contour)

    # find min and max coordinate values of contures
    for contour in contour_list:
        print("x")
        for idx, val in enumerate(contour):
            pt = (contour[idx][0])
            if pt[0] > x_max:
                x_max = pt[0]
            elif pt[0] < x_min:
                x_min = pt[0]
            if pt[1] > y_max:
                y_max = pt[1]
            elif pt[1] < y_min:
                y_min = pt[1]

    # cv2.drawContours(raw_image, contour_list,  Konturenindex (wenn alle gezeichnet werden sollen -1 eingeben), (Farbe der Konturen), Konturdicke)
    # draw relevant findings
    cv2.drawContours(raw_image, contour_list, -1, (255, 0, 255), 3)
    cv2.rectangle(raw_image,(x_min,y_min),(x_max,y_max),(255,0,0),2)

    cv2.imshow('Objects Detected', raw_image)
    k = cv2.waitKey(0) #& 0xff
    if k == 27:
        break

#contours = contour_list
# obtain the first 2 points of contours
#cntx1 = contours[0][0]
#cntx = contours[0][1]
# convert coords to points
#pt1 = (cntx1[0][0], cntx1[0][1])
#pt2 = (cntx[0][0], cntx[0][1])
# print(pt1[0])
# print(pt2)
# print((contour_list[1][1]))


cv2.destroyAllWindows()
