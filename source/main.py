#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main program script"""

from argparse import ArgumentParser, Namespace

from os import getenv, remove, system
from os.path import exists

from re import findall

from shutil import copy

from subprocess import PIPE, CompletedProcess, run

from requests import RequestException, Response, get


argument = ArgumentParser(
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


skip: Namespace = argument.parse_args().skip
compatibility: Namespace = argument.parse_args().compatibility
application: Namespace = argument.parse_args().application


REGEX_VERSION_REMOTE: str = r"com\.[a-z]+\.?[a-z]+_([0-9]+)\.apk"
REGEX_VERSION_LOCAL: str = r"com\.termux\." + str(application) + r"\s+versionCode:(\d+)"
REGEX_DOWNLOAD: str = r"https:\/\/f-droid\.org\/repo\/com\.[a-z]+\.?[a-z]+_[0-9]+"


def main():
    """Main function of the script"""

    try:

        system("termux-wake-lock")

        endpoint: str

        match application:

            case "api":
                endpoint = ".api/"

            case "boot":
                endpoint = ".boot/"

            case "styling":
                endpoint = ".styling/"

            case "widget":
                endpoint = ".widget/"

            case "window":
                endpoint = ".window/"

            case "tasker":
                endpoint = ".tasker/"

            case _:
                endpoint = "/"

        url_page: str = f"https://f-droid.org/en/packages/com.termux{endpoint}"

        response: Response = connect(url_page)

        if skip == False:

            version_remote: str | None
            version_local: str | None

            if application != "app":
                command: CompletedProcess = run(
                    ["termux-info"], stdout=PIPE, shell=True, text=True
                )

                version_local = findPattern(REGEX_VERSION_LOCAL, command.stdout, False)

            else:
                version_local = getEnv("TERMUX_VERSION")

            version_remote = findPattern(REGEX_VERSION_REMOTE, response.text)

            if application == "app":
                print(
                    "Termux does not provide a version code in its API in the same way as its extensions"
                )

            print(f"Current version available on servers is: {version_remote}")
            print(f"Current installed version is: {version_local}")

            input("\nPress ENTER to continue or CTRL + C, then ENTER to cancel")

        url_download: str | None = findPattern(REGEX_DOWNLOAD, response.text)

        download_apk: Response = connect(f"{url_download}.apk")
        download_asc: Response = connect(f"{url_download}.apk.asc")

        home: str = getEnv("HOME")

        file_name: str = f"{home}/.termux-update/termux-{application}"

        file_apk: str = f"{file_name}.apk"
        file_asc: str = f"{file_name}.apk.asc"

        if exists(file_apk):
            remove(file_apk)

        if exists(file_asc):
            remove(file_asc)

        with open(file_apk, "wb") as file:
            file.write(download_apk.content)
            file.close()

        with open(file_asc, "wb") as file:
            file.write(download_asc.content)
            file.close()

        if compatibility == True:
            file_comp: str = "/storage/emulated/0/Download/termux-update.apk"

            copy(file_apk, file_comp)
            system(
                f"am start --user 0 -a android.intent.action.VIEW -d file://{file_comp} -t application/vnd.android.package-archive"
            )

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

        if required != False:
            print("No valid results were found during the search")
            exit(2)

        else:
            return None


def getEnv(env: str) -> str:
    """Function to receive the value of an environment variable

    Args:
        env (str): environment variable

    Returns:
        str: environment variable value
    """

    environment: str | None = getenv(env)

    if type(environment) != str:
        print("Could not find environment variable")
        exit(2)

    return environment


if __name__ == "__main__":
    main()