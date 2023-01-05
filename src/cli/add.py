import os
from hashlib import pbkdf2_hmac
import sys

# Add new combination of handsign for password

# Try to get the original username (not "root") from shell
try:
    user = os.getlogin()
except Exception:
    user = os.environ.get("SUDO_USER")


PATH = os.path.abspath(__file__ + "/..")
SHADOWPATH = "/usr/lib/security/indra/shadow"

if not os.path.exists(SHADOWPATH):
    with open(SHADOWPATH, 'w') as f:
        pass
    os.chmod(SHADOWPATH, 0o744)
else:
    with open(SHADOWPATH) as f:
        lines = f.readlines()
        for line in lines:
            if user in line:
                print(
                    f"hand sign for {user} has been set, please run update command to update your password")
                sys.exit(0)

signs = []

with open(PATH + "/../setting/labels.csv") as fsign:
    for sign in fsign.readlines():
        signs.append(sign.strip())
VALID_SIGN = signs[1:13]
ex = ",".join(VALID_SIGN)

valid = False
while valid is False:
    valid = True
    print(
        f"""Type your jutsu sign, with comma separated between sign(minimum 6 signs).
Valid signs are {ex}""")
    jutsu = input().split(',')
    if len(jutsu) >= 6:
        for i in jutsu:
            if i not in VALID_SIGN:
                print(i + " is not a valid sign")
                valid = False
    else:
        valid = False

passwd = "".join(jutsu)

dk = pbkdf2_hmac('sha256', bytes(passwd, 'utf-8'), bytes(user, 'utf-8'), 50505)

with open(SHADOWPATH, "a") as cred:
    cred.writelines(user+":"+dk.hex()+":"+str(len(jutsu))+"\n")
