import os


config_path = os.path.abspath("deploy/config.yml")

# Check whether path exists
if not os.path.exists(config_path):
    raise FileNotFoundError("Config file missing!")

# Check whether it is a file
if not os.path.isfile(config_path):
    raise ValueError("Config path is not a file!")

print("Configuration validated!")
print("Starting deployment...")