"""
plate_solve.py
    - Handles plate solving ASTAP, loading resulting FITS file, and converting pixel
        coordinates to RA/Dec using a WCS solution.
    - This is designed to be used in conjunction with the rolling_capture.py (main).

Configuration parameters (to be added in config.yaml under a relevant section):
  astap_speed:        (default "slow")
  astap_search_radius: (default 180)
  astap_fov:          (default 0)
  astap_demosaic:     (default true)
  astap_color_correction: (default true)
"""

import os
import subprocess
from astropy.wcs import WCS
import error_Handler as ERR

# Runs ASTAP plate solving on the given image and outputs .ini/.wcs solution
def run_plate_solve(image_path, config, output_dir="plate_solve_results"):
    
    #Checks if the input image exists/is a file
    if(os.path.isfile(image_path) == False):
        ERR.raiseError("01001", "Image to plate solve wasn't found.", False)
        return None
    
    os.makedirs(output_dir, exist_ok=True)
    # Use the input image's basename for the output name
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_basename = os.path.join(output_dir, base_name)
    
    # Build le ASTAP command
    
    # Sample command: astap -f shot19.png -fov 0 -r 180 -m 3 -speed slow -dcm -cc -o <output_basename>
    command = [
        "astap",
        "-f", image_path,
        "-fov", str(config.get("astap_fov", 0)),
        "-r", str(config.get("astap_search_radius", 180)),
        "-m", "3",
        "-speed", config.get("astap_speed", "slow"),
    ]
    if config.get("astap_demosaic", True):
        command.append("-dcm")
    if config.get("astap_color_correction", True):
        command.append("-cc")
    command += ["-o", output_basename]
    
    print("Running ASTAP plate solving with command:")
    print(" ".join(command))
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        ERR.raiseError("01002", f"ASTAP plate solving failed: {e}", False)
        return None

    # ASTAP will produce an .ini file

    ini_file = output_basename + ".ini"
    if os.path.exists(ini_file):
        return ini_file
    else:
        ERR.raiseError("01003", f"Expected ASTAP .ini file not found after plate solving. Verify {ini_file} is a valid filepath.", False)
        return None

# Read WCS solution from ASTAP .ini file
# Returns an astropy.wcs.WCS object
def load_wcs_from_ini(ini_file):

    if((not os.path.isfile(ini_file)) or ini_file[-4:] != ".ini"):
       ERR.raiseError("01005", f"{ini_file} is not a valid .ini file.", False)
       return

    params = {}
    try:
        with open(ini_file, "r") as f:
            for line in f:
                if '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    try:
                        params[key] = float(val.split()[0])
                    except Exception as e:
                        continue
    except Exception as e:
        ERR.raiseError("01004", f"Error reading {ini_file}: {e}", False)
        return None

    try:
        wcs_sol = WCS(naxis=2)
        wcs_sol.wcs.crpix = [params['CRPIX1'], params['CRPIX2']]
        wcs_sol.wcs.crval = [params['CRVAL1'], params['CRVAL2']]
        # Use the CD matrix if available (astropy docs)
        if all(k in params for k in ("CD1_1", "CD1_2", "CD2_1", "CD2_2")):
            wcs_sol.wcs.cd = [[params['CD1_1'], params['CD1_2']],
                              [params['CD2_1'], params['CD2_2']]]
        else:
            # Fallback to using CDELT values (astropy docs)
            wcs_sol.wcs.cdelt = [params.get("CDELT1", 1), params.get("CDELT2", 1)]
        wcs_sol.wcs.ctype = ['RA---TAN', 'DEC--TAN']
        return wcs_sol
    except Exception as e:
        ERR.raiseError("01005", f"Couldn't construct WCS file from {ini_file}: {e}", False)
        return None

# Converts pixel coordinates to RA/Dec using the WCS solution
# Takes pixel coordinates (1-indexed) and WCS object
# Returns tuple: (RA, Dec) in degrees
def pixel_to_radec(x, y, wcs_sol):
    if(str(type(wcs_sol)) != "<class 'astropy.wcs.wcs.WCS'>"):
        ERR.raiseError("01006", "3rd parameter for function plate_solve.pixel_to_radec is not of type <class 'astropy.wcs.wcs.WCS'>.", False)
        return None
    if(str(type(x)) != "<class 'int'>" or str(type(y)) != "<class 'int'>"):
        ERR.raiseError("01007", "1st and/or 2nd parameters for function plate_solve.pixel_to_radec must be ints.", False)
        return None
    ra, dec = wcs_sol.all_pix2world(x, y, 1)
    return ra, dec
