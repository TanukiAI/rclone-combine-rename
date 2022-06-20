import pyperclip
import re
import json
import sys
import os
import argparse

# Argparser
parser = argparse.ArgumentParser(description="Combine Renamer")
parser.add_argument("--clipboard", action="store_true")
parser.add_argument("--file", default="input.txt")
parser.add_argument("--cryptfile")
args = parser.parse_args()

# Read the rename config
RENAME_CONFIG: dict = json.load(open("rename.json", "r", encoding="utf-8-sig"))

# Read the combine config and output the name
CONFIG: str = open(args.file, "r", encoding="utf-8-sig").read() if not args.clipboard else pyperclip.paste()
GD_NAME = re.findall(r'remote = (.*?),team_drive', CONFIG)[0]
print("Account Name:", GD_NAME)

# Get all alias remotes
REMOTES = re.findall(r"\[(.*?)]", CONFIG)
REMOTES.remove("AllDrives")

# Start renaming all configs
for i in REMOTES:
    # Add the Google Drive remote name to the aliases
    new_name = f"[{i}_{GD_NAME}]"
    CONFIG = CONFIG.replace(f"[{i}]", new_name)

    # Look at the rename config and if the alias name is present, take the new name
    repr_name = i
    if i in RENAME_CONFIG:
        repr_name = RENAME_CONFIG[i]
    CONFIG = CONFIG.replace(f'"{i}={i}:"', f'"{repr_name}={new_name[1:-1]}:"')

# Rename the AllDrives
CONFIG = CONFIG.replace("[AllDrives]", f"[{GD_NAME}_all]")

# Add a root alias at the top
CONFIG = fr"""
[root_{GD_NAME}]
type = alias
remote = {GD_NAME},team_drive=,root_folder_id=root:

""" + CONFIG
CONFIG = CONFIG.replace("upstreams = ", f'upstreams = "[_Root] Root=root_{GD_NAME}:" ')

# if args.cryptfile is given
passwords = None
if args.cryptfile and os.path.exists(args.cryptfile):
    with open(args.cryptfile, "r", encoding="utf-8-sig") as f:
        _passwords = f.read().strip().splitlines()
        if len(_passwords) > 2:
            print("Warning! There are more than 2 passwords in the file:", _passwords)
        else:
            passwords = _passwords

if passwords:
    CONFIG += rf"""
[{GD_NAME}_all_crypt]
type = crypt
remote = {GD_NAME}_all:
password = {passwords[0]}
{"password2 = " + passwords[1] if len(passwords) == 2 else ""}

"""

# Write new config
if not args.clipboard:
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(CONFIG)
else:
    pyperclip.copy(CONFIG)
