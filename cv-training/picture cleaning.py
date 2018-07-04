import urllib.request
import cv2
import numpy as np
import os

# find and delete pictures in neg that are also in uglies - for 404 pictures
def find_uglies():
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly, question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))

# method to resize and recolor (gray) a single image
def resize_positive():

    img = cv2.imread("pos/target positive 3.jpg", cv2.IMREAD_GRAYSCALE)
    resized_image = cv2.resize(img, (50, 50))
    cv2.imwrite("pos/target positive 3 50x50G.jpg", resized_image)

resize_positive()