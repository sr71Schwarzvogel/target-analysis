import cv2

# cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('shot_video_1.mp4')

# target_cascade = cv2.CascadeClassifier('cascade 1.xml')

contour_list = []
contour_rec_counter = 0
x_min = 10000
x_max = 0
y_min = 10000
y_max = 0
x_middle = 0
y_middle = 0
frame_number = 1
relevant_image = []

while 1:

    _,raw_image = cap.read()
    # raw_image = cv2.imread('test-pictures/shot_target_20.jpg')

    # on the first frame the camera is 2 focused on the relevant area
    if frame_number == 30:  # TODO check in the end if it works to set the middle for every frame
        # find edges
        bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
        edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
        _, contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # identify circles
        contour_list = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            area = cv2.contourArea(contour)

            if (len(approx) > 10) &  (len(approx) < 30) & (area > 15000) & (area < 90000):
                contour_list.append(contour)

        # find min and max coordinate values of contures
        for contour in contour_list:  # go through all contures in contour_list
            for idx, val in enumerate(contour):  # get all points of a contour
                pt = (contour[idx][0])  # get point out of coordinate
                if pt[0] > x_max:
                    x_max = pt[0]
                elif pt[0] < x_min:
                    x_min = pt[0]
                if pt[1] > y_max:
                    y_max = pt[1]
                elif pt[1] < y_min:
                    y_min = pt[1]

        # calculate center of target
        x_middle = int((x_max - x_min) / 2 + x_min)
        y_middle = int((y_max - y_min) / 2 + y_min)

        # TODO redo cascade with new target
        # TODO run cascade an combine to relevant area
        # gray = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
        # argets = target_cascade.detectMultiScale(gray, 1.3, 5)

        # for (x, y, w, h) in targets:
        #     if x < x_max

        #    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    frame_number = frame_number + 1

    # set relevant area
    if y_middle != 0:
        relevant_image = raw_image[y_middle - 150: y_middle + 150, x_middle - 150: x_middle + 150]
    else:
        relevant_image = raw_image

    



    # draw relevant findings
    cv2.drawContours(raw_image, contour_list, -1, (255, 0, 255), 3)
    cv2.rectangle(raw_image,(x_min,y_min),(x_max,y_max),(255,0,0),2)
    cv2.circle(raw_image,(x_middle,y_middle), 2, (0,0,255), 1)

    cv2.imshow('relevant range', relevant_image)
    cv2.imshow('raw image', raw_image)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()
