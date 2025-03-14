# Global imports
import os
import time
import argparse
from bs4 import BeautifulSoup
from datetime import datetime

# Local imports
from utils import *

# Logging object
mirror_logger = config_logging(Path(__file__).name.replace(".py", ""))

# Class representing an individual IC10 project
class Project:
    # NOTES:
    #   - A project's 'root' is the directory on your drive where Stationeers
    #     saves individual IC10 projects. The 'mirror' directory is where this
    #     script saves 'friendly' files that are stored on Github
    #   - The game stores IC10 scripts in XML files. They're primarly just the
    #     code you write with the ingame editor, but there is a bit of additional
    #     fluff that can get annooying. 'Friendly' files are the same as the XML
    #     copies, just without the fluff
    #   - 'Friendly' files are automatically converted to XML files for use in
    #      game. XML files are automatically converted to 'friendly' files for
    #      storage on Github

    # Constants
    DEFAULT_PATH = Path(".")

    # Metadata
    name = ""
    project_version = Version(0, 0, 0, True)
    date_time = 0
    game_version = ""
    description = ""
    author = ""
    workshop_file_handle = 0

    # Instructions
    instructions = []

    # FS info
    root = DEFAULT_PATH
    mirror = DEFAULT_PATH
    friendly_file = DEFAULT_PATH
    friendly_generated = False
    friendly_modified = 0.0
    meta_file = DEFAULT_PATH
    meta_generated = False
    meta_modified = 0.0
    xml_file = DEFAULT_PATH
    xml_generated = False
    xml_modified = 0.0

    # __init__()
    #
    # Creates a new project instance
    #
    # Arguments:
    #   - name    - name of the project
    def __init__(self, name):
        self.name = name
        self.root = Path(MIRROR_DIRECTORY).joinpath(name)
        self.root.mkdir(parents=True, exist_ok=True)
        self.mirror = Path(resolved_root_dir()).joinpath(name)
        self.mirror.mkdir(parents=True, exist_ok=True)
        self.friendly_file = self.root.joinpath(FRIENDLY_FILE_NAME)
        self.meta_file = self.root.joinpath(META_FILE_NAME)
        self.meta_generated = self.meta_file.exists()
        self.xml_file = self.mirror.joinpath(XML_FILE_NAME)
        self.refresh_files_status()

    # saveIC10()
    #
    # Overwrites the local friendly file with this project instance's data
    def saveIC10(self):
        mirror_logger.debug(f"Saving '{str(self.friendly_file)}'")

        with open(self.friendly_file, "w+") as fh:
            for line in self.instructions:
                fh.write(line + "\n")

        self.friendly_generated = True

    # loadXML()
    #
    # Loads the local friendly file and stores the resulting information
    # within the project's instance
    def loadIC10(self):
        mirror_logger.debug(f"Loading '{str(self.friendly_file)}'")

        # Don't load if file doesn't exist
        if not self.friendly_generated:
            mirror_logger.error(f"Cannot load IC10 for project '{self.name}' as it hasn't been marked as created yet...")
            return

        # Open and load file
        with open(self.friendly_file, "r") as fh:
            self.instructions = fh.read()

    # modifyXML()
    #
    # Overwrites the game's XMl file with this project's instruction data.
    # Does not output any metadata
    def modifyXML(self):
        mirror_logger.debug(f"Loading '{str(self.xml_file)}'")

        # Don't load if file doesn't exist
        if not self.xml_generated:
            mirror_logger.error(f"Cannot load XML for project '{self.name}' as it hasn't been marked as created yet...")
            return
        
        # Open and load file
        with open(self.xml_file, 'r') as fh:
            data = fh.read()

        # Parse the XML
        xml_data = BeautifulSoup(data, "xml")

        # Build instructions into a single string
        instructions = ""
        for line in self.instructions:
            instructions += line

        # Attempt to update the tag
        try:
            xml_data.find("Instructions").string = instructions

            with open(self.xml_file, 'w+') as fh:
                mirror_logger.debug(f"Saving '{str(self.xml_file)}")
                fh.write(xml_data.prettify())
        except Exception as e:
            mirror_logger.error(f"Failed to update XML tag for project '{self.name}'")
        finally:
            self.refresh_files_status()

    # saveXML()
    #
    # Overwrites the game's XML file with this project instance's data
    def saveXML(self):
        mirror_logger.debug(f"Saving '{str(self.xml_file)}'")

        with open(self.xml_file, 'w+') as fh:
            mirror_logger.error(f"XML 'saving' not implemented. You must use XML modification for now...")
            mirror_logger.error(f"XML saving cannot be implemented until meta files are being saved")
            mirror_logger.error(f"We cannot overwrite the meta within the XML if the IC10 is newer on startup...")
            mirror_logger.error(f"And we certainly don't want to overwrite any new changes on startup. Modification it is (for now)")
            return

        self.xml_generated = True

    # loadXML()
    #
    # Loads the game's XML file and stores the resulting information within
    # the project instance
    def loadXML(self):
        mirror_logger.debug(f"Loading '{str(self.xml_file)}'")

        # Don't load if file doesn't exist
        if not self.xml_generated:
            mirror_logger.error(f"Cannot load XML for project '{self.name}' as it hasn't been marked as created yet...")
            return

        # Open and load file
        with open(self.xml_file, 'r') as fh:
            data = fh.read()

        # Parse, strip, and unpack everything
        xml_data = BeautifulSoup(data, "xml")
        self.date_time = int(xml_data.find("DateTime").text.strip())
        self.game_version = xml_data.find("GameVersion").text.strip()
        self.description = xml_data.find("Description").text.strip()
        self.author = xml_data.find("Author").text.strip()
        self.workshop_file_handle = int(xml_data.find("WorkshopFileHandle").text.strip())
        self.instructions = xml_data.find("Instructions").text.strip().split("\n")

    # refresh_files_status()
    #
    # Refreshes the generation status and modification timestamps for all
    # important files within a project
    #
    # Returns:
    #   - True when files are new, false when they aren't
    def refresh_files_status(self):
        changed = False

        # Perform refresh on IC10 file
        self.friendly_generated = self.friendly_file.exists()
        if self.friendly_generated:
            timestamp = os.path.getmtime(self.friendly_file)
            if self.friendly_modified != timestamp:
                changed = True
            self.friendly_modified = timestamp

        # Perform refresh on meta file
        self.meta_generated = self.meta_file.exists()
        if self.meta_generated:
            timestamp = os.path.getmtime(self.meta_file)
            if self.meta_modified != timestamp:
                changed = True
            self.meta_modified = timestamp
        
        # Perform refresh on XML file
        self.xml_generated = self.xml_file.exists()
        if self.xml_generated:
            timestamp = os.path.getmtime(self.xml_file)
            if self.xml_modified != timestamp:
                changed = True
            self.xml_modified = timestamp

        return changed

    # perform_mirror()
    #
    # Where the magic happens, baby! This function is only to be called when
    # it is already known there is work to do. This function will blindly
    # overwrite in one direction depending on which file is newest
    def perform_mirror(self):
        friendly_time = datetime.fromtimestamp(self.friendly_modified)
        xml_time = datetime.fromtimestamp(self.xml_modified)

        # If local is newer than the game's copy, write to the game's copy
        if friendly_time > xml_time:
            self.loadIC10()
            self.modifyXML()
        # Else, 
        else:
            self.loadXML()
            self.saveIC10()

    # find_projects()
    #
    # Finds the names of all projects within a certain directory
    #
    # NOTE: This function is a bit dumb. It will assume all directories
    #       within the given directory are projects without checking for
    #       the instruction file. Likewise, it won't check that the given
    #       directory even exists! Make sure to give a valid path (or
    #       update this function to protect)!
    #
    # Arguments:
    #   - path - path to search for projects
    #
    # Returns:
    #   - List of project names
    def find_projects(path):
        projects = []
        
        for (_, dirs, _) in os.walk(path):
            for dir in dirs:
                projects.append(Path(dir).name)

        return projects
    
    # debug()
    #
    # Displays a debug view of this project
    def debug(self):
        mirror_logger.debug(f"Project '{self.name}'")
        mirror_logger.debug(f"  - Root:                 '{self.root}'")
        mirror_logger.debug(f"  - Name:                 '{self.name}'")
        mirror_logger.debug(f"  - Game version:         '{self.game_version}'")
        mirror_logger.debug(f"  - Description:          '{self.description}'")
        mirror_logger.debug(f"  - Author:               '{self.author}'")
        mirror_logger.debug(f"  - Workshop file handle:  {self.workshop_file_handle}")

# mirror_all()
#
# Performs a synchronization of all projects.
def mirror_all(projects):
    # This should only be done once at startup... Let the user know this
    mirror_logger.info(f"Performing one time synchronization of all projects...")

    # Loop through and mirror all projects
    for project in projects:
        project.perform_mirror()
        project.refresh_files_status()

# mirror_process()
#
# Starts the mirroring process. Should probably only be invoked by main()
# within the mirror.py file, but shoot ya shot playa
#
# Arguments:
#   - mirror_dir - directory to mirror from
#   - root_dir   - directory that scripts are actually held (Stationers game data)
#   - one_shot   - if true, this function will not mirror forever
def mirror_process(mirror_dir, root_dir, one_shot=False):
    mirror_logger.info(f"Starting mirror between '{mirror_dir}' and '{root_dir}'")

    # Find projects
    root_projects = Project.find_projects(root_dir)
    mirror_projects = Project.find_projects(mirror_dir)

    # Let user know if we did not find any projects
    if len(root_projects) == 0 and len(mirror_projects) == 0:
        mirror_logger.fatal("Could not find any projects")
        return

    # Find only unique projects
    project_names = list(set(root_projects + mirror_projects))
    projects = []
    for name in project_names:
        projects.append(Project(name))
        
    for project in projects:
        project.loadXML()
        project.debug()

    # Let user know how many projects we found
    mirror_logger.info(f"Found {len(projects)} projects")

    # Update all projects once
    # NOTE: All projects were refreshed upon creation, so there isn't a huge need
    #       to perform another one (or one within mirror_all() for that matter),
    #       but if there are some odd choices being made at startup, this should be
    #       the first place to look
    mirror_all(projects)

    # Don't run forever if in one-shot mode
    if one_shot:
        return

    # Mirror forever
    while True:
        # Detect changes in file status and perform mirror when required
        for project in projects:
            if project.refresh_files_status():
                mirror_logger.info(f"Changes to project '{project.name}' detected. Starting mirror process...")
                project.perform_mirror()

        # Wait a bit...
        time.sleep(MIRROR_PERIOD)

# main()
#
# Unofficial "official" entry point
def main(args):
    global mirror_logger

    # Enter verbose mode if required
    if args.verbose:
        mirror_logger.info("Reinitializing mirror logger to enable debug logging...")

        # Close handlers
        handlers = mirror_logger.handlers[:]
        for handler in handlers:
            mirror_logger.removeHandler(handler)
            handler.close()

        # Reinitialize
        mirror_logger = config_logging(Path(__file__).name.replace(".py", ""), logging.DEBUG)

    mirror_process(MIRROR_DIRECTORY, resolved_root_dir(), args.one_shot)

# Entry point
#
# Run main when invoking this as a standalone script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stationeers script mirroring service")

    parser.add_argument('--one_shot', action='store_true', help="Performs a single synchronization, then exits")
    parser.add_argument('--verbose', action='store_true', help="Enables verbose (debug) output")

    main(parser.parse_args())