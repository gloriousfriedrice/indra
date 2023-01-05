import configparser
import os
import fileinput
# Get the absolute filepath
config_path = os.path.dirname(os.path.abspath(__file__)) + "/../config.ini"

# Read config from disk
config = configparser.ConfigParser()
config.read(config_path)

cur_stat = config.get("core", "disabled")

if cur_stat == "true":
    # Loop though the config file and only replace the line containing the disable config
    for line in fileinput.input([config_path], inplace=1):
        print(line.replace("disabled = " + config.get("core",
              "disabled"), "disabled = " + "false"), end="")
    print("Indra has been enabled")

else:
    print("Indra is enabled")
