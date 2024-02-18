import cv2
import os
import numpy as np

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

num = 0

while cap.isOpened():

    succes1, img = cap.read()
    succes2, img2 = cap2.read()

    img2_size = img2.shape
    
    imgL = np.zeros((img2_size[0], int(img2_size[1] / 2), img2_size[2]))
    imgR = np.zeros((img2_size[0], int(img2_size[1] / 2), img2_size[2]))
    imgL = img2[:,:int(img2_size[1]/2),:]
    imgR = img2[:,int(img2_size[1]/2) :,:]

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        
        
        
        cv2.imwrite('images/stereoLeft/stereoLeft' + str(num) + '.png', imgL)
        cv2.imwrite('images/stereoRight/stereoRight' + str(num) + '.png', imgR)
        print("images saved!")
        print(os.getcwd())
        num += 1

    print(img2_size)
    
    cv2.imshow('Img 1',imgL)
    cv2.imshow('Img 2',imgR)

# Release and destroy all windows before termination
cap.release()
cap2.release()

cv2.destroyAllWindows()
