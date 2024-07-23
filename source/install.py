#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

"""Program installation script"""

from os import getenv, system
from os.path import dirname, exists

from shutil import copy

from re import match

prefix: (str | None) = getenv('PREFIX')

if type(prefix) == str: filepath: str = prefix + '/bin/termux-update'
else: filepath: str = '/data/data/com.termux/files/usr/bin/termux-update'

copy(f'{dirname(__file__)}/main.py', filepath)
system(f'chmod +x {filepath}')

home: (str | None) = getenv('HOME')

if type(home) == str: filepath: str = home + '/.termux/termux.properties'
else: filepath: str = '/data/data/com.termux/files/home/.termux/termux.properties'

if not exists(f'{filepath}.bak'):
    copy(filepath, f'{filepath}.bak')

with open(filepath, 'r') as file:
    lines = file.readlines()

allow_external_apps: bool = False

with open(filepath, 'w') as file:
    for line in lines:

        if match(r'^#?\s*allow-external-apps\s*=', line):
            file.write('allow-external-apps = true\n')
            allow_external_apps = True

        else:
            file.write(line)

    if allow_external_apps == False:
        file.write('allow-external-apps = true\n')

system('termux-reload-settings')

print('Termux Update installed successfully!')
print('Run the \'termux-update\' command to start the script')
exit(0)
