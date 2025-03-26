import numpy as np
import cv2 as cv
import glob
 
#Note that this program does not uncalibrate images
 
 
#Number of internal squares on the calibration checkerboard.
#Assumes the checkerboard is of n x n dimensions
squares = 13
 
#Change to the directory to where the raw, uncalibrated images are.
rawImages = 'Images/shot*.png'
 
#Change to where the program should store calibration parameters
paramFile = 'calibrationParams.npz'
 
 
 
 
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((squares*squares,3), np.float32)
objp[:,:2] = np.mgrid[0:squares,0:squares].T.reshape(-1,2)
 
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
 
images = glob.glob(rawImages)
 
print("Starting") 
 
for fname in images:
    print(f"Processing Image {fname}")
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
 
    # Find the chess board corners
    print("Finding corners...")
    ret, corners = cv.findChessboardCorners(gray, (squares,squares), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
 
        # Draw and display the corners
        cv.drawChessboardCorners(img, (squares,squares), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(50)
cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print(f'ret is {ret}, mtx is {mtx}, dist is {dist}, rvecs is {rvecs}, tvecs is {tvecs}')
calib_size = gray.shape[::-1]  # (width, height)

print("Finished on calibration")
print("Reprojection Error: ", ret)
print("Camera Matrix:\n", mtx)
print("Distortion Coefficients:\n", dist)


# Save calibration parameters with image size
np.savez(paramFile, mtx=mtx, dist=dist, calib_size=calib_size, allow_pickle=False)
print(f"Calibration parameters have been saved to {paramFile} gracefully")
