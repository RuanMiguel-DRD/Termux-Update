# Termux-Update
Script for updating Termux and its extensions via command line

## Warning

**This project has been discontinued and is unstable**

The constant changes in Android, variations in the operating system on each different cell phone, and other factors, make this project very difficult to become stable

It may or may not work on your device, but there is no guarantee and this may change over time

The malfunction that prevents this script from working is Termux's inability to open the application installer in a stable way

## How it works

The function of this script is to allow the user to update Termux and its extensions directly from the command line, without the need to have F-Droid installed on the cell phone, thus consuming memory and system resources

The script accesses F-Droid and searches for the latest released version of the apk, then makes a comparison between the versions. If you do not have the program installed or the latest version of it, it asks if you want to continue with the installation, and if you confirm, the latest version of the program will be downloaded and installed on your device

You can skip the comparison between the installed version and the latest available version by passing the `--skip` or `-s` argument

If you do not skip the version check, Termux will copy a text containing the version specifications to the clipboard

No comparison occurs if you try to update Termux, as it does not have a proper way to make its version code available

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

### Security considerations

For the script to work, it needs to modify the `termux.properties` file to release the `allow-external-apps` permission, and the program also requires access to the cell phone's storage if it wants to use compatibility mode, and to ensure proper functioning, it also requires permission to run in the background

All these permissions are used to ensure the program works and may reduce the security of your cell phone, so use at your own risk

### Version control

The script will always download the latest released version of the programs, regardless of whether they are unstable, incompatible with your Android version or incompatible with your architecture

### Execution speed

The speed of the program is directly linked to your internet speed, and if you run it without using the `-s` argument to skip the version comparison, it may take a little longer, because to check the current version of your programs, the script needs to run the `termux-info` command, and it takes a little while
