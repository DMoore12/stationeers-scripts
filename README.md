# DM's Stationeers Scripts

Scripts for hosted game sessions

## Idea

I'd really like to be able to develop within a Visual Studio Code environment. Unforunately, the game's files are held within XML files containing other information. I could go about modifying them directly, but there's too much extra junk on the screen!

This project attempts to create an active mirror. In the future, I'd like to configure it using NSSM to constantly run in the background. It'll allow you to keep plain text files for modification with the editor of your choice while simultaneously updating the XML files in the background so you can use them in game without needing to copy+paste.

Additionally, this system could allow automatic minimization of files prior to upload, allowing much grander files with comments and whitespace. We'll see how far this goes...

> NOTE: This project is in a very primitive state and may break your script files. Please backup all files before starting, and use at your own risk!

## Requirements

- You must have [Python 3.13](https://wiki.python.org/moin/BeginnersGuide/Download) or later installed
- You must have an active Stationeers installation
    - Game scripts must be in `Documents/My Games/Stationeers/scripts`
- You must be willing to accept the risks associated with running this software
    - This project *CAN* and *WILL* overwrite game files if it thinks it needs to

## Usage:

1. Clone the project
2. Install project dependencies using `python -m pip install -r requirements.txt`
3. Start the script using `python mirror.py`

You may view the program help by adding the `-h` or `--help` arguments.

## TODO:

- [X] Automatic mirroring of files to target directory
- [X] File metadata storage and transfer
- [ ] File versioning
- [ ] Program metadata (runtime, stats, etc.)
- [ ] Proper program configuration
- [ ] Minimize code prior to writing XML
- [ ] Copy XML format of game's files
