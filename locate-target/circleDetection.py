import cv2

# raw_image = cv2.imread('shapes.png')

#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('test-pictures/shot_video_1.mp4')
# cv2.imshow('Original Image', raw_image)
# cv2.waitKey(0)

while 1:

    _,raw_image = cap.read()
    #raw_image = cv2.imread('test-pictures/shot_target_19.jpg')

    bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
    # cv2.imshow('Bilateral', bilateral_filtered_image)
    # cv2.waitKey(0)

    edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
    # cv2.imshow('Edge', edge_detected_image)
    # cv2.waitKey(0)

    _, contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)

       # if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)):
        if ((len(approx) > 10) &  (len(approx) < 30) & (area > 9000) & (area < 90000)):
            contour_list.append(contour)
            print("x")
            print(contour)



    # cv2.drawContours(raw_image, contour_list,  Konturenindex (wenn alle gezeichnet werden sollen -1 eingeben), (Farbe der Konturen), Konturdicke)
    cv2.drawContours(raw_image, contour_list, -1, (255, 0, 255), 3)
    cv2.imshow('Objects Detected', raw_image)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break



raw_image.release()
cv2.destroyAllWindows()
