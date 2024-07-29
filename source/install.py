#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

"""Program installation script"""

from os import getenv, mkdir, system
from os.path import dirname, exists

from re import Match, Pattern, compile

from shutil import copy

prefix: str | None = getenv("PREFIX")

program_path: str
if type(prefix) == str:
    program_path = prefix + "/bin/termux-update"
else:
    program_path = "/data/data/com.termux/files/usr/bin/termux-update"

copy(f"{dirname(__file__)}/main.py", program_path)
system(f"chmod +x {program_path}")

home: str | None = getenv("HOME")

file_path: str
if type(home) == str:
    file_path = home + "/.termux/termux.properties"
else:
    file_path = "/data/data/com.termux/files/home/.termux/termux.properties"

mkdir(f"{home}/.termux-update")

if not exists(f"{file_path}.bak"):
    copy(file_path, f"{file_path}.bak")

with open(file_path, "r") as file:
    file_copy: list[str] = file.readlines()
    file.close()

with open(file_path, "w") as file:

    permission: bool = False
    pattern: Pattern = compile(r"(^#?\s*allow-external-apps\s*=\s*)(\S+)(.*)")

    for line in file_copy:

        correspond: Match | None = pattern.match(line)

        if correspond:
            comment: str | None = correspond.group(3)
            file.write(f"allow-external-apps = true {comment}\n")
            permission = True

        else:
            file.write(line)

    if permission == False:
        file.write("# Parameter modified by Termux Update:\n")
        file.write("allow-external-apps = true\n")

    file.close()

system("termux-reload-settings")

print("Termux Update installed successfully!")
print("Run the 'termux-update' command to start the script")
exit(0)
