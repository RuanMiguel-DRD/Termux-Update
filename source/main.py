#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

"Main program script"

from argparse import ArgumentParser

from os import getenv, remove, system
from os.path import exists

from re import findall

from shutil import copy

from subprocess import PIPE, CompletedProcess, run

from sys import exit

from requests import RequestException, Response, get


argument: ArgumentParser = ArgumentParser(
    prog="termux-update",
    description="Script for updating Termux and its extensions",
    epilog="https://github.com/RuanMiguel-DRD/Termux-Update",
)

argument.add_argument(
    "-s",
    "--skip",
    action="store_true",
    help="if you want to skip the process of comparing versions",
)

argument.add_argument(
    "-c",
    "--compatibility",
    action="store_true",
    help="in case of malfunction, activate to try to install the programs by an alternative method",
)

argument.add_argument(
    "application",
    choices=["app", "api", "boot", "styling", "widget", "window", "tasker"],
    help="choose between Termux and one of its extensions",
)


skip: bool = argument.parse_args().skip
compatibility: bool = argument.parse_args().compatibility
application: str = argument.parse_args().application


def main():
    "Main function of the script"

    try:

        system("termux-wake-lock")

        REGEX_VERSION_REMOTE: str = r"com\.[a-z]+\.?[a-z]+_([0-9]+)\.apk"
        REGEX_VERSION_LOCAL: str = r"com\.termux\." + application + r"\s+versionCode:(\d+)"
        REGEX_DOWNLOAD: str = r"https:\/\/f-droid\.org\/repo\/com\.[a-z]+\.?[a-z]+_[0-9]+"

        endpoint: str

        match application:

            case "api": endpoint = ".api/"
            case "boot": endpoint = ".boot/"
            case "styling": endpoint = ".styling/"
            case "widget": endpoint = ".widget/"
            case "window": endpoint = ".window/"
            case "tasker": endpoint = ".tasker/"
            case _: endpoint = "/"

        url_page: str = f"https://f-droid.org/en/packages/com.termux{endpoint}"

        response: Response = connect(url_page)

        if skip == False and application != "app":

            version_remote: str | None
            version_local: str | None

            command: CompletedProcess = run(
                ["termux-info"], stdout=PIPE, shell=True, text=True
            )

            version_local = findPattern(REGEX_VERSION_LOCAL, command.stdout, False)
            version_remote = findPattern(REGEX_VERSION_REMOTE, response.text)

            if type(version_local) == str:

                if version_local == version_remote:
                    print(f"You already have the latest version of {application} installed")
                    exit(0)

                else:
                    print(f"Your current installed version is {version_local} the latest available version is {version_remote}")

            else:
                print("The program is not installed")

            answers: str

            while True:
                answers = input("Do you want to continue with the installation process? [Y/N] ").lower()

                if answers in ["y", "n"]:
                    if answers == "y":
                        break

                    else:
                        raise KeyboardInterrupt

        url_download: str | None = findPattern(REGEX_DOWNLOAD, response.text)

        download_apk: Response = connect(f"{url_download}.apk")
        download_asc: Response = connect(f"{url_download}.apk.asc")

        home: str | None = getenv("HOME")
        if type(home) != str:
            print("Could not find environment variable")
            exit(2)

        file_name: str = f"{home}/.termux-update/termux-{application}"

        file_apk: str = f"{file_name}.apk"
        file_asc: str = f"{file_name}.apk.asc"

        if exists(file_apk):
            remove(file_apk)

        with open(file_apk, "wb") as file:
            file.write(download_apk.content)
            file.close()

        if exists(file_asc):
            remove(file_asc)

        with open(file_asc, "wb") as file:
            file.write(download_asc.content)
            file.close()

        if compatibility == True:
            file_copy: str = "/storage/emulated/0/Download/termux-update.apk"

            try:
                copy(file_apk, file_copy)
                system(f"am start --user 0 -a android.intent.action.VIEW -d file://{file_copy} -t application/vnd.android.package-archive")

            except (FileNotFoundError, PermissionError):
                print("Error, insufficient permissions or nonexistent destination directory, run `ter` to free up storage access")
                print("And make sure the directory has the proper permissions")
                exit(2)

        else:
            system(f"termux-open {file_apk}")

        exit(0)

    except KeyboardInterrupt:
        print("Script terminated by user")
        exit(1)


def connect(url: str) -> Response:
    """Accesses a URL and returns a instance containing the result of the connection

    Args:
        url (str): text containing the URL that will be accessed

    Returns:
        Response: instance containing the result of the connection
    """

    try:
        response: Response = get(url)
        if response.status_code != 200:
            raise RequestException

        return response

    except RequestException:
        print("An error occurred while connecting to the internet")
        exit(3)


def findPattern(regex: str, text: str, required: bool = True) -> str | None:
    """Function to query regex in texts and return the first compatible result

    Args:
        regex (str): regex code that will be queried
        text (str): text where the regex query will be performed
        required (bool): specifies whether it is mandatory to find a match or not

    Returns:
        str: first result matching the query
        None: if you don't find any results
    """

    try:
        result: list[str] = findall(regex, text)
        return result[0]

    except IndexError:

        if required == True:
            print("No valid results were found during the search")
            exit(2)

        else:
            return None


if __name__ == "__main__":
    main()
