import cv2
import numpy as np
import math

# cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('shot_video_1.mp4')
# 25px ~ 1cm shot_video_1.mp4

target_cascade = cv2.CascadeClassifier('cascade 5.xml')

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
bullet_holes = []
nonzero = [1]
laserTrack = []
laser_correction_x = 0
laser_correction_y = 0
last_shot_x = 0
last_shot_y = 0
new_shot = False
first_shot = False
targets =[]
relevant_targets = []
file = open("data.txt", "w")
file.write("300" + "\n")
file.write("300" + "\n")

while 1:
    new_shot = False
    first_shot = False
    _,raw_image = cap.read()
    # raw_image = cv2.imread('test-pictures/shot_target_20.jpg')

    # on the first frame the camera is 2 focused on the relevant area
    if frame_number == 1:
        # find edges
        bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
        edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
        _, contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # identify circles
        contour_list = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            area = cv2.contourArea(contour)

            if (len(approx) > 10) & (len(approx) < 30) & (area > 15000) & (area < 90000):
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

        # run haar detection
        gray = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
        targets = target_cascade.detectMultiScale(gray, 1.3, 5)

    frame_number = frame_number + 1

    for (x, y, w, h) in targets:
        x_temp = x + w/2
        y_temp = y + h/2
        if (x_temp > x_middle - 100) & (x_temp < x_middle + 100) & (y_temp > y_middle - 100) & (y_temp < y_middle + 100):
            relevant_targets.append((x, y, w, h))

    # set relevant area
    if y_middle != 0:
        relevant_image = raw_image[y_middle - 150: y_middle + 150, x_middle - 150: x_middle + 150].copy()
    else:
        relevant_image = raw_image.copy()

    # find bullet holes
    # convert relevant area to hsv
    hsv = cv2.cvtColor(relevant_image, cv2.COLOR_BGR2HSV)

    # hsv hue sat value
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([255, 255, 150])

    # find black
    mask = cv2.inRange(hsv, lower_black, upper_black)
    res = cv2.bitwise_and(relevant_image, relevant_image, mask=mask)

    # invert colors
    mask_bulletholes = cv2.inRange(mask, 0, 100)

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create()

    # Detect blobs.
    keypoints = detector.detect(mask_bulletholes)

    # check if hole is already detected
    for keypoint in keypoints:
        exists = False
        if bullet_holes == []:
            x_diff = math.sqrt((150 - keypoint.pt[0]) ** 2)
            y_diff = math.sqrt((150 - y_min - keypoint.pt[1]) ** 2)
            diff = math.sqrt((x_diff ** 2) + (y_diff ** 2))
            bullet_holes.append((keypoint.pt[0], keypoint.pt[1], diff))
            last_shot_x = keypoint.pt[0]
            last_shot_y = keypoint.pt[1]
            new_shot = True
            first_shot = True
            file.write(str(keypoint.pt[1]) + "," + str(keypoint.pt[0]) + "," + str(diff) + "\n")

        else:
            for points in bullet_holes:
                if ((points[0] - keypoint.pt[0]) ** 2 < 1000) & ((points[1] - keypoint.pt[1]) ** 2 < 1000):
                    exists = True
            if exists is False:
                x_diff = math.sqrt((150 - keypoint.pt[0])**2)
                y_diff = math.sqrt((150 - keypoint.pt[1]) ** 2)
                diff = math.sqrt((x_diff ** 2)+(y_diff ** 2))
                bullet_holes.append((keypoint.pt[0], keypoint.pt[1], diff))
                last_shot_x = keypoint.pt[0]
                last_shot_y = keypoint.pt[1]
                new_shot = True
                file.write(str(keypoint.pt[1]) + "," + str(keypoint.pt[0]) + "," + str(diff) + "\n")

    #detect laser
    im = cv2.cvtColor(relevant_image, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(im, 250, 255)

    # cleaning the mask
    # closing
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations=1)
    # dilation
    kernel = np.ones((7, 7), np.uint8)
    cleaned_mask = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)

    # get middle coordinates of laser
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
        x = (x_sum / z_counter) + laser_correction_x
        y = (y_sum / z_counter) + laser_correction_y

        # round up coordinates
        x = math.ceil(x)
        y = math.ceil(y)

        if new_shot is False:
            file.write(str(x) + "," + str(y) + "\n")

        laserTrack.append([x, y])
        if first_shot is True:
            laser_correction_x = (x - last_shot_x)/2
            laser_correction_y = (y - last_shot_y)/2

            for points in laserTrack:
                points[0] = points[0] + laser_correction_x
                points[1] = points[1] + laser_correction_y

    # draw line on image
    s = len(laserTrack)
    if s > 2:
        for i in range(1, s):
            p1 = laserTrack[i - 1]
            p2 = laserTrack[i]
            cv2.line(relevant_image, (int(p1[1]), int(p1[0])), (int(p2[1]), int(p2[0])), (255, 0, 0), 2)  # draw laser track

    # draw bullet holes
    for holes in bullet_holes:
        cv2.circle(raw_image, (int(holes[0]+x_middle-150), int(holes[1]+y_middle-150)), 7, (0, 255, 0), 2)  # bullet holes
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(relevant_image, str(int(holes[2]/2.5)), (int(holes[0]), int(holes[1])), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    # draw relevant findings
    cv2.drawContours(raw_image, contour_list, -1, (255, 0, 255), 3)  # Lilac circles - biggest circle
    cv2.rectangle(raw_image,(x_min,y_min),(x_max,y_max),(255,0,0),2)  # blue rectangle - rectangle around inner circle
    cv2.circle(raw_image, (x_middle, y_middle), 2, (0, 0, 255), 1)  # red circle - middle of target
    cv2.circle(relevant_image, (x_middle, y_middle), 2, (0, 0, 255), 1)  # red circle

    for (x, y, w, h) in relevant_targets:
        if x < x_max:
            print("x")
            cv2.rectangle(raw_image, (x, y), (x + w, y + h), (255, 255, 0), 2)  # turquois rectangle relevant haar matches

    cv2.imshow('relevant range', relevant_image)
    cv2.imshow('raw image', raw_image)
    cv2.imshow('mask bullet holes', mask_bulletholes)
    # cv2.imshow('image with holes', im_with_keypoints)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

file.close()
cv2.destroyAllWindows()
