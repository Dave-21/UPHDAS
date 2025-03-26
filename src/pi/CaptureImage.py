#Rest in peace harambe
#You will be missed 

import picamera2
from picamera2 import Preview
from libcamera import controls
import os
import os.path
import json
import datetime


os.makedirs("Shot_Metadata", exist_ok=True)

#picamera2.set_controls({"AeMeteringMode": controls.AeMeteringModeEnum.Spot})
#picam2.set_controls("AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0 )
 

with picamera2.Picamera2() as camera:
   
        camera.resolution = (4056,3040)
        #camera.framerate = Fraction(1, 2)
        camera.iso = 0
        camera.exposure_mode = 'off'
        camera.awb_mode = 'off'
        camera.awb_gains = (1.8,1.8)
        if(input('Capture images at a lower resolution? (y/n) ').lower() == 'y'):
            config = camera.create_still_configuration({"size": (1014,760)})
        else:
            config = camera.create_still_configuration()
        previewConfig = camera.create_preview_configuration()
        
        # The reason the resolution was being set low is because the camera config is set twice
        # Commenting out the "#camera.configure(previewConfig)" fixes this, so that means the
        #   camera configuration should only be set the previewConfig if preview mode is selected
        camera.configure(config)
        #camera.configure(previewConfig)
 
 
        #camera.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0})
     
		
        camera.set_controls({"ExposureTime": 150000,
                             "AnalogueGain": .5,
                             "Brightness": 0.0,
                             "Contrast": 1.0, 
                             "AwbEnable": False,
                             "AeEnable": False, })
                             #"AfMode": 0, 
                             #"LensPosition": 0.0 })
        settings = [150000, .5, 0.0, 1.0]
        multiPrompt = 'False'
        
        
        # Main program loop
        while(1):
                keyInput = -1
                numPictures = 1
                
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
                             7 - Load Camera Controls\n
                             8 - Start camera preview\n
                             9 - Enable multiple image capture\n
                            10 - Set focus lens position (does not work)\n""")
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
                            elif keyInput == 8:
                                # If we ddo this, where we set the preview configuration here, then if we try taking
                                #   a shot after previewing, it keeps the preview config (the resolution will be low)
                                camera.configure(previewConfig)
                                print("Starting camera preview...")
                                camera.start()
                                camera.stop_preview()
                                camera.start_preview(Preview.QTGL)
                                print("Preview started. Press enter to end preview.")
                                input()
                                camera.stop_preview()
                                camera.stop()
                                
                                # Temporary solution to low resolution, set config to normal still after previewing
                                # Itta works as intended, babieee
                                camera.configure(config)
                            elif keyInput == 9:
                                while(1==1):
                                    print("Enter the number of pictures to be taken: ")
                                    numPictures = input()
                                    if not str(keyInput).isnumeric():
                                        print("Enter only positive numbers.")
                                    elif int(numPictures) <= 0:
                                        print("Enter only positive numbers.")
                                    else:
                                        break
                                multiPromptInput = input("Prompt before each image? (y/n) ")
                                if(multiPromptInput.lower() == 'y'):
                                    multiPrompt = True
                                else:
                                    multiPrompt = False
                                numPictures = int(numPictures)        
                                print(f"Next time 1 is selected in the menu, the program will capture {numPictures} images.")
                                print("Press enter to continue.")
                                input()
                                    
                                    
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
                                    #elif keyInput == 10:
                                        #camera.set_controls({"LensPosition" : float(valueInput)})

                                        
                                  
                for x in range(numPictures):
                        
                        camera.resolution = (4056,3040)
                        # This outputs the correct time of when picture is taken: 2025-02-06T16:51:54.422853
                        print(datetime.datetime.utcnow().isoformat())
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
                        
                        # Getting time here results in this: "UTC_time": "2025-02-06T16:52:09.940170"
                        
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
                        metadata_path = os.path.join("new_metadata", metadata_filename)
                        with open(metadata_path, "w") as metadata_file:
                                json.dump(metadata, metadata_file, indent=2)
                        print(f"Saved metadata as {metadata_filename}\n\n")
                        
                        if multiPrompt == True:
                            input("Press enter to take the next image. ")
