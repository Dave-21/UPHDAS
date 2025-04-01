import get_config as config
from datetime import datetime, timezone

#Used for most internal errors in the UPHDAS project.
class UPHDAS_Error(Exception):
    def __init__(self, code, message, isFatal):
        self.code = code
        self.message = message
        self.isFatal = isFatal
        self.time = datetime.now(timezone.utc)

        #Attempts to load in the config file
        cfg = config.load_config()
        
        #Finds where the log file is
        logPath = cfg.get("pi_config").get("error_log_file")
        
        #Writes the error message to the log file
        outFile = open(logPath, "a")
        
        outFile.write(f"{self} at time {self.time}")
        
        outFile.close()
        
        #Ends program and prints error message if the error is fatal
        if(isFatal == True):
            print(self)
            exit()        
        
        
    def __str__(self):
        return f"Internal Error {self.code}: {self.message}" 
        

#Only used for errors in the config file to prevent infinite looping.
#Always fatal.
class UPHDAS_configError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        print(self)
        exit()
    
    def __str__(self):
        return f"Internal Error {self.code}: {self.message}"
