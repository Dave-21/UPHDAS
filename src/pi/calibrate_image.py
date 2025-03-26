import numpy as np
import cv2 as cv

#Disclaimer: some code used from opencv website

# Load calibration parameters from .npz file
data = np.load("calibrationParams.npz")
mtx = data['mtx']
dist = data['dist']
calib_size = tuple(data['calib_size'])  # (width, height)

filepath = input("Enter an image to open: ").strip()
img = cv.imread(filepath)
if img is None:
	print("Couldn't load image")
	exit()

h,  w = img.shape[:2]

# If test image resolution is different from calibration resolution, scale camera matrix
if (w, h) != calib_size:
    scale_x = w / float(calib_size[0])
    scale_y = h / float(calib_size[1])
    print("Scaling calibration parameters from", calib_size, "to", (w, h))
    mtx[0, 0] *= scale_x
    mtx[0, 2] *= scale_x
    mtx[1, 1] *= scale_y
    mtx[1, 2] *= scale_y

# Get new camera matrix and undistort image
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
dst = cv.undistort(img, mtx, dist, None, newcameramtx)

# Full undistotred image
output_file = f'calibrateResult{filepath.rsplit(".", 1)[0]}.png'
cv.imwrite(output_file, dst)
print(f"Wrote image out to calibrateResult{output_file}.png")
