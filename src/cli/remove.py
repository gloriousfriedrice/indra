import os

# Add new combination of handsign for password

# Try to get the original username (not "root") from shell
try:
    user = os.getlogin()
except Exception:
    user = os.environ.get("SUDO_USER")

PATH = os.path.abspath(__file__ + "/..")
signs = []

os.remove(PATH+"/"+user)
