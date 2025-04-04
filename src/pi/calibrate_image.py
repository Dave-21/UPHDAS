import numpy as np
import cv2 as cv
import yaml
import get_config as gc
import error_Handler as ERR
import os

def undistort_Image(filepath):
    #Disclaimer: some code used from opencv website

    cfg = gc.load_config().get("image_calibration")

    #File to load calibration data from
    paramFile = cfg.get("parameter_file", 'calibrationParams.npz')
    outputdir = cfg.get("outputdir", '')
    outputprefix = cfg.get("output_prefix", 'calibrated_')
    filetype = cfg.get("filetype", '.png')

    


    #File to save calibrated image to.
    #Index 0 is the filepath, index 1 is the extension
    outputPath = [f'{outputdir}{outputprefix}', filetype]


    # Load calibration parameters from .npz file

    if not os.path.isfile(paramFile):
        ERR.raiseError("03001", "Couldn't load undistortion parameters", False)
        return None
    elif paramFile[-4:] != '.npz':
        ERR.raiseError("03004", "Undistortion parameter file is of incorrect type.", False)
        return None


    data = np.load(paramFile)
    mtx = data['mtx']
    dist = data['dist']
    calib_size = tuple(data['calib_size'])  # (width, height)

    filepath = filepath.strip()

    img = cv.imread(filepath)
    
    if img is None:
        ERR.raiseError("03002", "Couldn't load input image to undistort", False)
        return None

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

    os.makedirs(outputdir, exist_ok=True)


    # Full undistotred image
    filename = filepath.split("/")[-1]
    print(f"filename is {filename}")
    output_file = f'{outputPath[0]}{filename.rsplit(".", 1)[0]}{outputPath[1]}'
    print(f"outputfile is {output_file}")
    try:
        cv.imwrite(output_file, dst)
    except Exception as e:
        ERR.raiseError("03003", f"Couldn't save image: {e}", False)
        return None

    return output_file

