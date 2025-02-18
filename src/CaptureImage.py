#Rest in peace harambe
#You will be missed 

import picamera2
from libcamera import controls
import os
import os.path
import json
import datetime

os.makedirs("Shot_Metadata", exist_ok=True)

#picamera2.set_controls({"AeMeteringMode": controls.AeMeteringModeEnum.Spot})
#picam2.set_controls("AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0 )}
 

with picamera2.Picamera2() as camera:
   
        camera.resolution = (4056,3040)
        #camera.framerate = Fraction(1, 2)
        camera.iso = 0
        camera.exposure_mode = 'off'
        camera.awb_mode = 'off'
        camera.awb_gains = (1.8,1.8)
        
        config = camera.create_still_configuration()
        camera.configure(config)
 
     
		
        camera.set_controls({"ExposureTime": 150000,
                             "AnalogueGain": .5,
                             "Brightness": 0.0,
                             "Contrast": 1.0, 
                             "AwbEnable": False,
                             "AeEnable": False, 
                             "AfMode": 0, 
                             "LensPosition": 0.0 })
        settings = [150000, .5, 0.0, 1.0]
        
        # Main program loop
        while(1):
                keyInput = -1
                
                #Loop for each image capture
                while keyInput != 1:
                    #Prints out an options menu
                    print("""
                             0 - Exit\n
                             1 - Take image \n 
                             2 - Set Exposure \n 
                             3 - Set Analogue Gain \n 
                             4 - Set Brightness \n
                             5 - Set Contrast \n 
                             6 - Save Camera Controls\n
                             7 - Load Camera Controls\n""")
                    print("==========================================================================")
                    keyInput = input()
                    
                    #Sanity checking input
                    if not str(keyInput).isnumeric():
                        print("Enter only a number.")
                    else:
                            #Selects option based off of input
                            keyInput = int(keyInput)
                            if keyInput == 0:
                                #Quits program
                                quit()
                            elif keyInput == 1:
                                #Breaks options loop and takes image    
                                break
                            elif keyInput == 6:
                                #Saves camera parameters in a file
                                filenumber = input("Enter parameter slot to save: ")
                                with open(f"Parameters/cameraParams{filenumber}.txt","w") as file:
                                        file.write(f'Exposure Time: {settings[0]}\n')
                                        file.write(f'Analogue Gain: {settings[1]}\n')
                                        file.write(f'Brightness: {settings[2]}\n')
                                        file.write(f'Contrast: {settings[3]}\n')
                                        file.close()
                                
                            elif keyInput == 7:
                                #Loads camera parameters from a file    
                                try:
                                    filenumber = input("Enter parameter slot to load: ")
                                    with open(f"Parameters/cameraParams{filenumber}.txt","r") as file:
                                        settings = []
                                        settings.append(int(file.readline()[15:-1]))
                                        settings.append(float(file.readline()[15:-1]))
                                        settings.append(float(file.readline()[12:-1]))
                                        settings.append(float(file.readline()[10:-1]))
                                        print(settings)
                                        camera.set_controls({"ExposureTime": int(settings[0]),
                                                             "AnalogueGain": float(settings[1]),
                                                             "Brightness": float(settings[2]),
                                                             "Contrast": float(settings[3])})
                                        file.close()
                                except Exception as e:
                                        print(f"Error: {e}")
                            else:
                                    #Handles the setting of camera settings
                                    valueInput = input("Enter value: ")
                                     
                                    if keyInput == 2:
                                        #Sets exposure time    
                                        settings[0] = int(valueInput)
                                        camera.set_controls({"ExposureTime" : int(valueInput)})
                                    elif keyInput == 3:
                                        #Sets analogue gain    
                                        settings[1] = float(valueInput)
                                        camera.set_controls({"AnalogueGain" : float(valueInput)})
                                    elif keyInput == 4:
                                        #Sets Brightness, sanity checks for acceptable value
                                        if(float(valueInput) <= 1.0 and float(valueInput) >= -1.0):
                                                settings[2] = float(valueInput)
                                                camera.set_controls({"Brightness" : float(valueInput)})
                                        else:
                                                print("Outside of acceptable range. \n Acceptable range is -1.0 to 1.0")
                                    elif keyInput == 5:
                                        #Sets contrast, sanity checks for acceptable value    
                                        if(float(valueInput) <= 32.0 and float(valueInput) >= 0.0):
                                                settings[3] = float(valueInput)
                                                camera.set_controls({"Contrast" : float(valueInput)})
                                        else:
                                                print("Outside of acceptable range. \n Acceptable range is 0.0 to 32.0")
                                    elif keyInput == 8:
                                        #Sets contrast, sanity checks for acceptable value    
                                                camera.set_controls({"LensPosition" : float(valueInput)})

                                        
                                  
                
                #Takes an image
                camera.start()
                
                #Searches for a file name that has not already been taken
                filenum = 0
                while(os.path.isfile(f"Captured_Pictures/shot{filenum}.png") == True):
                        filenum += 1
                        
                #Saves the image        
                camera.capture_file(f'Captured_Pictures/shot{filenum}.png')
                #Prints out the metadata and confirmation
                print(camera.capture_metadata())
                print(f"Saved image as shot{filenum}.png")
                        
                camera.stop()
                
                # Make le metadata
                utc_now = datetime.datetime.utcnow().isoformat()
                metadata = {
                "UTC_time": utc_now,
                "exposure_time": settings[0],
                "analogue_gain": settings[1],
                "latitude": "",
                "longitude": "",
                "altitude": "143.5",
                "azimuth": "265",
                "elevation": "-60",
                "notes": ""
                }
                
                #saves metadata (i think)
                metadata_filename = f"shot{filenum}.txt"
                metadata_path = os.path.join("Shot_Metadata", metadata_filename)
                with open(metadata_path, "w") as metadata_file:
                        json.dump(metadata, metadata_file, indent=2)
                print(f"Saved metadata as {metadata_filename}\n\n")
