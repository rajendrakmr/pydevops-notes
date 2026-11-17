#!/usr/bin/python3
import os 

config_path = os.path.abspath("config/app.yaml")
if not os.path.exists(config_path):
    raise FileNotFoundError(f"Configuration not found: {config_path}")

if not os.path.isfile(config_path):
    raise ValueError(f"Expected a file: {config_path}")

print("Configuration file exists:", os.path.getsize(config_path), "bytes")
      
#file 
dir_path=os.path.abspath("deploy")
for folder in ("logs","backup","config","script"):
    path = os.path.join(dir_path,folder)
    os.makedirs(path,exist_ok=True)
    print("Ready:", path)
print(os.getcwd())
print("Directory entries:", os.listdir("."))

