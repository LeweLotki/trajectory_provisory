import cv2
import os
import numpy as np

cap = cv2.VideoCapture(0)

num = 0

while cap.isOpened():

    succes, img = cap.read()

    img_size = img.shape
    
    imgL = np.zeros((img_size[0], int(img_size[1] / 2), img_size[2]))
    imgR = np.zeros((img_size[0], int(img_size[1] / 2), img_size[2]))
    imgL = img[:,:int(img_size[1]/2),:]
    imgR = img[:,int(img_size[1]/2) :,:]

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        
        
        
        cv2.imwrite('images/stereoLeft/stereoLeft' + str(num) + '.png', imgL)
        cv2.imwrite('images/stereoRight/stereoRight' + str(num) + '.png', imgR)
        print("images saved!")
        print(os.getcwd())
        num += 1

    cv2.imshow('Img 1',imgL)
    cv2.imshow('Img 2',imgR)

# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows()
