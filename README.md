# Termux-Update
Script for updating Termux and its extensions via command line

## How it works

The function of this script is to allow the user to update Termux and its extensions directly from the command line, without the need to have F-Droid installed on the cell phone, thus consuming memory and system resources

The script accesses F-Droid and searches for the link to the latest released version of the apk, then downloads the program and its signature, then compares and asks the user whether or not they want to continue with the update

You can skip the comparison between the installed version and the latest available version by passing the `--skip` or `-s` argument

The comparison of the main Termux application is different from the other extensions and the versions available online

This is because Termux does not state its version code in its API like the other extensions

The program keeps copies of the latest downloaded version of the programs in the `$HOME/.termux-update` folder and the same goes for signing keys

And if used in compatibility mode, you can keep 1 copy of the last updated program in `/storage/emulated/0/Download/termux-update.apk`

In case of error, the program prints a message and exits, giving an error code accordingly, being 1 for user cancellation, 2 for misuse of the program, and 3 onwards for operating or connection error

If no error occurs, the program will return 0

## How to install

The installation process is extremely simple, you only need to have python 3, pip and git installed on the system

1. Clone the repository using `git clone https://github.com/RuanMiguel-DRD/Termux-Update`
2. Enter the repository and run `pip install -r requirements.txt` to install the script dependencies
3. Finally, go to the source folder and run the installer with `python install.py`

After that the script is installed and ready to use

So if you want you can delete the script repository from your Termux

## How to uninstall

The uninstallation process is simple, just run `rm -f $PREFIX/bin/termux-update`

We do not provide ways to uninstall the script's dependencies because there are few of them, and they are also commonly used by other programs, and uninstalling them can lead to bugs and malfunctions in other programs

## Requirements

The program's dependencies are few, namely Python, Pip and some native Termux commands

The other program dependencies are listed in the `requirements.txt` file, and for development, in `requirements-dev.txt`

## Limitation

### Installing programs

The program suffers from operating limitations due to constant changes in Android policies and APIs made by Google, as well as modifications by companies that sell their cell phones and devices with their own modifications to Android

As a result of this huge divergence in Android systems, the program may not work on all devices

If the script does not work traditionally, try using it using the `--compatibility` or `-c` argument to try to install the programs using an alternative method

### Dependence on an external service

In case of changes in the source code of the F-Droid website, addition of a firewall, or change in the naming of Termux files, the entire program is subject to stop working

### Security issues

For the script to work, it needs to modify the `termux.properties` file to release the `allow-external-apps` permission, and the program also requires access to the cell phone's storage if it wants to use compatibility mode, and to ensure proper functioning, it also requires permission to run in the background

All these permissions are used to ensure the program works and may reduce the security of your cell phone, so use at your own risk
