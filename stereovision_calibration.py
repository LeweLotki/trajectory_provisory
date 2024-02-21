import numpy as np
import cv2 as cv
import glob
from os import listdir, mkdir
from os.path import join, isdir

def write_single_params():

    ''' Write parameters to .txt files '''
    output_dir = r'Calibration_Files'
    prompt = input('Save parameters to "{}\\"? (y/n): '.format(output_dir))

    if (prompt == 'y'):
        if not isdir(output_dir):
            mkdir(output_dir)
        # np.savetxt(r'Calibration_Files\C1.txt', C1, fmt='%.5e')   # identical to CL
        # np.savetxt(r'Calibration_Files\D1.txt', D1, fmt='%.5e')   # identical to DL
        np.savetxt(join(output_dir, 'Q.txt'), Q, fmt='%.5e')
        # np.savetxt(join(output_dir, 'FundMat.txt'), F, fmt='%.5e')
        np.savetxt(join(output_dir, 'CmL.txt'), newCameraMatrixL, fmt='%.5e')
        np.savetxt(join(output_dir, 'CmR.txt'), newCameraMatrixR, fmt='%.5e')
        np.savetxt(join(output_dir, 'DcL.txt'), distL, fmt='%.5e')
        np.savetxt(join(output_dir, 'DcR.txt'), distR, fmt='%.5e')
        np.savetxt(join(output_dir, 'Rtn.txt'), rot, fmt='%.5e')
        np.savetxt(join(output_dir, 'Trnsl.txt'), trans, fmt='%.5e')
        # np.savetxt(join(output_dir, 'RtnL.txt'), R1, fmt='%.5e')  # Contains 'n' estimate arrays from 'n' images
        # np.savetxt(join(output_dir, 'TrnslL.txt'), T1, fmt='%.5e')
        np.savetxt(join(output_dir, 'RectifL.txt'), rectL, fmt='%.5e')
        np.savetxt(join(output_dir, 'ProjL.txt'), projMatrixL, fmt='%.5e')
        np.savetxt(join(output_dir, 'ProjR.txt'), projMatrixR, fmt='%.5e')
        np.savetxt(join(output_dir, 'umapL.txt'), undistL, fmt='%.5e')
        np.savetxt(join(output_dir, 'rmapL.txt'), rectifL, fmt='%.5e')
        np.savetxt(join(output_dir, 'umapR.txt'), undistR, fmt='%.5e')
        np.savetxt(join(output_dir, 'rmapR.txt'), rectifR, fmt='%.5e')
        np.savetxt(join(output_dir, 'ROIL.txt'), roi_L, fmt='%.5e')
        np.savetxt(join(output_dir, 'ROIR.txt'), roi_R, fmt='%.5e')
        print(f'Parameters saved to folder: [{output_dir}]')

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

chessboardSize = (7,7)
frameSize = (672,376)


# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

size_of_chessboard_squares_mm = 20
objp = objp * size_of_chessboard_squares_mm

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpointsL = [] # 2d points in image plane.
imgpointsR = [] # 2d points in image plane.


imagesLeft = sorted(glob.glob('images/stereoLeft/stereoLeft*.png'))
imagesRight = sorted(glob.glob('images/stereoRight/stereoRight*.png'))

for imgLeft, imgRight in zip(imagesLeft, imagesRight):

    imgL = cv.imread(imgLeft)
    imgR = cv.imread(imgRight)
    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    retL, cornersL = cv.findChessboardCorners(grayL, chessboardSize, None)
    retR, cornersR = cv.findChessboardCorners(grayR, chessboardSize, None)

    # If found, add object points, image points (after refining them)
    if retL and retR:

        objpoints.append(objp)

        cornersL = cv.cornerSubPix(grayL, cornersL, (11,11), (-1,-1), criteria)
        imgpointsL.append(cornersL)

        cornersR = cv.cornerSubPix(grayR, cornersR, (11,11), (-1,-1), criteria)
        imgpointsR.append(cornersR)

        # Draw and display the corners
        cv.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
        cv.imshow('img left', imgL)
        cv.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
        cv.imshow('img right', imgR)
        cv.waitKey(1000)


cv.destroyAllWindows()




############## CALIBRATION #######################################################

retL, cameraMatrixL, distL, rvecsL, tvecsL = cv.calibrateCamera(objpoints, imgpointsL, frameSize, None, None)
heightL, widthL, channelsL = imgL.shape
newCameraMatrixL, roi_L = cv.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

print(f'roi_L value calibration section {roi_L}')

retR, cameraMatrixR, distR, rvecsR, tvecsR = cv.calibrateCamera(objpoints, imgpointsR, frameSize, None, None)
heightR, widthR, channelsR = imgR.shape
newCameraMatrixR, roi_R = cv.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))

print(f'roi_R value calibration section {roi_R}')

########## Stereo Vision Calibration #############################################

flags = 0
flags |= cv.CALIB_FIX_INTRINSIC
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same 

criteria_stereo= (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retStereo, newCameraMatrixL, _, newCameraMatrixR, _, rot, trans, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(objpoints, imgpointsL, imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], criteria_stereo, flags)


########## Stereo Rectification #################################################

rectifyScale= 1
rectL, rectR, projMatrixL, projMatrixR, Q, _, _= cv.stereoRectify(newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], rot, trans, rectifyScale,(0,0))

print(f'roi_L value rectification section {roi_L}')
print(f'roi_R value rectification section {roi_R}')

''' Rectification mapping '''
undistL, rectifL = cv.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv.CV_32FC1)
undistR, rectifR = cv.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv.CV_32FC1)

'''
stereoMapL = cv.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv.CV_16SC2)
stereoMapR = cv.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv.CV_16SC2)


print("Saving parameters!")
cv_file = cv.FileStorage('Map.xml', cv.FILE_STORAGE_WRITE)

cv_file.write('stereoMapL_x',stereoMapL[0])
cv_file.write('stereoMapL_y',stereoMapL[1])
cv_file.write('stereoMapR_x',stereoMapR[0])
cv_file.write('stereoMapR_y',stereoMapR[1])

cv_file.release()
'''

write_single_params()
