import numpy as np
import cv2 as cv

#Disclaimer: some code used from opencv website

inFile = open("calibrationParams.txt", "r")

rawText = inFile.read()

paramsList = rawText.split(";")

inFile.close()

filepath = input("Enter an image to open: ")
imgText = filepath[:-4]
img = cv.imread(filepath)

ret = float(paramsList[0])
print(ret)
tempmtx = paramsList[1][1:-1].split()
mtx = [[float(tempmtx[0][1:]), float(tempmtx[1]), float(tempmtx[2][:-1])],
[float(tempmtx[3][1:]), float(tempmtx[4]), float(tempmtx[5][:-1])],
[float(tempmtx[6][1:]), float(tempmtx[7]), float(tempmtx[8][:-1])]]
mtx[0] = np.array(mtx[0])
mtx[1] = np.array(mtx[1])
mtx[2] = np.array(mtx[2])
mtx = np.array(mtx)
print(mtx)
tempdist = paramsList[2][2:-2]
dist = [0]
tempdist = tempdist.split()

for i in range(5):
	tempdist[i] = float(tempdist[0])
	
dist[0] = np.array(tempdist)

dist = np.array(dist)
	
print(dist)
rvecs = paramsList[3]
tvecs = paramsList[4]

print(f"processing image {imgText}")
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
dst = cv.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]


cv.imwrite(f'calibrateResult{imgText}.png', dst)

print(f"Wrote image out to calibrateResult{imgText}.png")
