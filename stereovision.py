import numpy as np
import cv2


# Camera parameters to undistort and rectify images
cv_file = cv2.FileStorage()
cv_file.open('Map.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

# Open both cameras
cap =  cv2.VideoCapture(0)

while cap.isOpened():

    succes, frame = cap.read()
    # succes_left, frame_left = cap_left.read()

    size = frame.shape

    frame_left = np.zeros((size[0], int(size[1] / 2), size[2]))
    frame_right = np.zeros((size[0], int(size[1] / 2), size[2]))
    frame_left = frame[:,:int(size[1]/2),:]
    frame_right = frame[:,int(size[1]/2) :,:]


    # Undistort and rectify images
    frame_right = cv2.remap(frame_right, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    frame_left = cv2.remap(frame_left, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
                     
    # Show the frames
    cv2.imshow("frame right", frame_right) 
    cv2.imshow("frame left", frame_left)


    # Hit "q" to close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows()
