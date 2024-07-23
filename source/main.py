#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main program script"""

from argparse import ArgumentParser

from requests import RequestException, Response, get

from re import findall

from os import getenv, remove, system
from os.path import exists

argument = ArgumentParser(
    prog='termux-update',
    description='Script for updating Termux and its extensions',
    epilog='https://github.com/RuanMiguel-DRD/Termux-Update'
)

argument.add_argument(
    'application',
    choices=['app', 'api', 'boot', 'styling', 'widget', 'float', 'tasker']
)

arg: str = argument.parse_args().application

match arg:

    case 'api':
        url: str = r'https://f-droid.org/en/packages/com.termux.api/'

    case 'boot':
        url: str = r'https://f-droid.org/en/packages/com.termux.boot/'

    case 'styling':
        url: str = r'https://f-droid.org/en/packages/com.termux.styling/'

    case 'widget':
        url: str = r'https://f-droid.org/en/packages/com.termux.widget/'

    case 'float':
        url: str = r'https://f-droid.org/en/packages/com.termux.window/'

    case 'tasker':
        url: str = r'https://f-droid.org/en/packages/com.termux.tasker/'

    case _:
        url: str = r'https://f-droid.org/en/packages/com.termux/'

regex: str = r'https:\/\/f-droid\.org\/repo\/com\.[a-z]+\.?[a-z]+_[0-9]+\.apk'

class CodeStatusError(BaseException):
    """Exception for unexpected HTTP response errors"""

try:

    response: Response = get(url)

    if response.status_code != 200:
        raise CodeStatusError

    result: list[str] = findall(regex, response.text)
    if len(result) < 1:
        raise IndexError

    download: Response = get(result[0])

    if download.status_code != 200:
        raise CodeStatusError

    home: (str | None) = getenv('HOME')
    if type(home) != str: home = '/data/data/com.termux/files/home'

    filepath: str = home + '/.termux-update.apk'

    if exists(filepath):
        remove(filepath)

    with open(filepath, 'wb') as file:
        file.write(download.content)
        file.close()

    system(f'termux-open {filepath}')
    exit(0)

except (RequestException):
    print('An error occurred while connecting to the internet')
    exit(1)

except (CodeStatusError):
    print('Error, unexpected HTTP response')
    exit(1)

except (IndexError):
    print('Error, no link to download the program was found')
    exit(1)
