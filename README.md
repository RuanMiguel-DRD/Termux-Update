# Termux-Update
Script for updating Termux and its extensions via command line

## How it works

The function of this script is to allow the user to update Termux and its extensions directly from the command line, without the need to have F-Droid installed on the cell phone, thus consuming memory and system resources

The script accesses F-Droid and looks for the link to the latest released version of the apk, then downloads it and opens the apk installer to try to install it

For the script to work, it needs to modify the Termux ``termux.properties`` file to grant permission to install apks directly through Termux, and this can lead to security breaches, use at your own risk

## How to install

The installation process is extremely simple, you only need to have python 3, pip and git installed on the system

1. Clone the repository using `git clone https://github.com/RuanMiguel-DRD/Termux-Update`
2. Enter the repository and run `pip install -r requirements.txt` to install the script dependencies
3. Lastly, run our installer with `python install.py`

After that, the script will be installed and running on your Termux

Then, if desired, you can delete the script repository from your Termux

## How to uninstall

The uninstallation process is simple, just run `rm -f /data/data/com.termux/files/usr/bin/termux-update`

We do not provide ways to uninstall the script's dependencies because there are few of them, and they are also commonly used by other programs, and uninstalling them can lead to bugs and malfunctions in other programs
