import numpy as np
import cv2 as cv

#Disclaimer: some code used from opencv website

#File to load calibration data from
paramFile = 'calibrationParams.npz'

#File to save calibrated image to.
#Index 0 is the filepath, index 1 is the extension
outputPath = ['Calibrated/calibrated_', '.png']


# Load calibration parameters from .npz file
data = np.load(paramFile)
if data is None:
    print("Couldn't open file")
mtx = data['mtx']
print(mtx)
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
filename = filepath.split("/")[-1]
output_file = f'{outputPath[0]}{filename.rsplit(".", 1)[0]}{outputPath[1]}'
cv.imwrite(output_file, dst)
print(f"Wrote image out to {output_file}")
