# Open the config file in an editor

# Import required modules
import os
import subprocess

# Let the user know what we're doing
print("Opening config.ini in the default editor")

# Default to the nano editor
editor = os.getenv('EDITOR')


# Use the user preferred editor if available
if "EDITOR" in os.environ:
    editor = os.environ["EDITOR"]
elif os.path.isfile("/etc/alternatives/editor"):
    editor = "/etc/alternatives/editor"

# Open the editor as a subprocess and fork it
subprocess.call([editor, os.path.dirname(
    os.path.realpath(__file__)) + "/../config.ini"])
