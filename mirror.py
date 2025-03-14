# Global imports
import os
import time
from bs4 import BeautifulSoup

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
    friendly_modified = time.ctime(0)
    meta_file = DEFAULT_PATH
    meta_generated = False
    meta_modified = time.ctime(0)
    xml_file = DEFAULT_PATH
    xml_generated = False
    xml_modified = time.ctime(0)

    # __init__()
    #
    # Creates a new project instance
    #
    # Arguments:
    #   - name    - name of the project
    def __init__(self, name):
        self.name = name
        self.root = Path(MIRROR_DIRECTORY).joinpath(name)
        self.mirror = Path(resolved_root_dir()).joinpath(name)
        self.friendly_file = self.root.joinpath(FRIENDLY_FILE_NAME)
        self.meta_file = self.root.joinpath(META_FILE_NAME)
        self.meta_generated = self.meta_file.exists()
        self.xml_file = self.mirror.joinpath(XML_FILE_NAME)
        self.refresh_files_status()

    # saveIC10()
    #
    # Overwrites the local friendly file with this project instance's data
    # def saveIC10(self):

    # loadXML()
    #
    # Loads the local friendly file and stores the resulting information
    # within the project's instance
    # def loadIC10(self):

    # saveXML()
    #
    # Overwrites the game's XML file with this project instance's data
    # def saveXML(self):
    #     with open(self.xml_file)

    # loadXML()
    #
    # Loads the game's XML file and stores the resulting information within
    # the project instance
    def loadXML(self):
        mirror_logger.debug(f"Loading XML file for project '{self.name}' from '{self.xml_file}'")

        # Perform file status refresh
        self.refresh_files_status()

        # Don't generate if file doesn't exist
        if not self.xml_generated:
            mirror_logger.error(f"Cannot load XML for project '{self.name}' as it hasn't been marked as created yet")

        with open(self.xml_file, 'r') as fh:
            data = fh.read()

        xml_data = BeautifulSoup(data, "xml")
        self.date_time = int(xml_data.find("DateTime").text)
        self.game_version = xml_data.find("GameVersion").text
        self.description = xml_data.find("Description").text
        self.author = xml_data.find("Author").text
        self.workshop_file_handle = int(xml_data.find("WorkshopFileHandle").text)
        self.instructions = xml_data.find("Instructions").text.split("\n")

    # refresh_files_status()
    #
    # Refreshes the generation status and modification timestamps for all
    # important files within a project
    def refresh_files_status(self):
        self.friendly_generated = self.friendly_file.exists()
        if self.friendly_generated:
            self.friendly_modified = time.ctime(os.path.getctime(self.friendly_file))
        self.meta_generated = self.meta_file.exists()
        if self.meta_generated:
            self.meta_modified = time.ctime(os.path.getctime(self.meta_file))
        self.xml_generated = self.xml_file.exists()
        if self.xml_generated:
            self.xml_modified = time.ctime(os.path.getctime(self.xml_file))

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

def check_mirror(projects):
    have_work = False
    
    # for project in projects:


    return (projects, have_work)

def perform_mirror(projects):


    return projects

# mirror()
#
# Starts the mirroring process. Should probably only be invoked by main()
# within the mirror.py file, but shoot ya shot playa
#
# Arguments:
#   - mirror_dir - directory to mirror from
#   - root_dir   - directory that scripts are actually held (Stationers game data)
def mirror(mirror_dir, root_dir):
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

    # Mirror forever
    while True:
        # Search for changes and queue them
        (projects, have_work) = check_mirror(projects)
        
        # Perform changes only if necessary
        if have_work:
            perform_mirror(projects)

        # Wait a bit...
        time.sleep(MIRROR_PERIOD)

# main()
#
# Unofficial "official" entry point
def main():
    mirror(MIRROR_DIRECTORY, resolved_root_dir())

# Entry point
#
# Run main when invoking this as a standalone script
if __name__ == "__main__":
    main()