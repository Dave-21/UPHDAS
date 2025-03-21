import numpy as np
import cv2 as cv
import glob
 
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((14*14,3), np.float32)
objp[:,:2] = np.mgrid[0:14,0:14].T.reshape(-1,2)
 
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
 
images = glob.glob('shot*.png')
 
print("Starting") 
 
for fname in images:
    print(f"Processing Image {fname}")
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    #cv.imshow('img', gray)
    #cv.waitKey(500)
    #cv.destroyAllWindows()
 
    # Find the chess board corners
    print("Finding corners...")
    ret, corners = cv.findChessboardCorners(gray, (14,14), None)
    
 
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
 
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
 
        # Draw and display the corners
        cv.drawChessboardCorners(img, (14,14), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(50)
 
cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print(f'ret is {ret}, mtx is {mtx}, dist is {dist}, rvecs is {rvecs}, tvecs is {tvecs}')
#input()
file = open("calibrationParams.txt", "w")
file.write(str(ret))
file.write(";")
print(f"Wrote ret {ret}")
file.write(str(mtx))
file.write(";")
print(f"Wrote mtx {mtx}")
file.write(str(dist))
file.write(";")
print(f"Wrote dist {dist}")
file.write(str(rvecs))
file.write(";")
print(f"Wrote rvecs {rvecs}")
file.write(str(tvecs))

print(f"Wrote tvecs {tvecs}")
file.close()

images = glob.glob('shot*.png')


for imageText in images:
    print(f"processing image {imageText}")
    img = cv.imread(imageText)
    h,  w = img.shape[:2]
    #print(f'h is {h}, w is {w}')
    #input()
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    #print(f'newcameramtx is {newcameramtx}, roi is {roi}')
    #input()
    # undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    #print(f'dst is {dst}')
    #input()

    # crop the image
    x, y, w, h = roi
    #print(f' x is {x}, y is {y}, w is {w}, h is {h}')
    #input()
    dst = dst[y:y+h, x:x+w]
    #print(f'dst is {dst}')
    #input()

    cv.imwrite(f'calibresult{imageText}.png', dst)
    
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error

print( "total error: {}".format(mean_error/len(objpoints)) )
