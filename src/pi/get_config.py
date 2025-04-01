import yaml
import error_Handler as ERR
import os

def load_config(config_path="config.yaml"):
    
    if(os.path.isfile(config_path) == False):
        raise ERR.UPHDAS_configError("00001", f"Couldn't find config file {config_path}") 

    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    return cfg


