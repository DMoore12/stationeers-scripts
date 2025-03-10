# Global imports
import os
import time
import logging

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

    # Class variables
    name = ""
    root = Path(".")
    mirror = Path(".")
    friendly_file = Path(".")
    friendly_generated = False
    xml_file = Path(".")
    xml_generated = False
    project_version = Version(0, 0, 0, True)

    # __init__()
    #
    # Creates a new project instance. This method assumes that we do not
    # already have the link to the mirrored files created. It will create
    # a default mirror link based on is_root
    #
    # Arguments:
    #   - name    - name of the project
    #   - path    - path to the project (either root or the mirror)
    #   - is_root - true when the given path is root rather than mirror
    def __init__(self, name, path, is_root):
        self.name = name
        
        if is_root:
            self.root = Path(path)
            self.mirror = resolved_root_dir().joinpath(name)
            self.friendly_generated = True
        else:
            self.root = Path(".").joinpath(name)
            self.mirror = Path(path)
            self.friendly_generated = False
        
        self.friendly_file = self.root.joinpath(FRIENDLY_FILE_NAME)
        self.xml_file = self.mirror.joinpath(XML_FILE_NAME)
        self.xml_generated = not self.friendly_generated

    # find_projects()
    #
    # Finds all projects within a given directory and initializes empty
    # projects. Collects all such projects in a list and returns it
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
    #   - List of projects
    def find_projects(path, is_root):
        projects = []
        
        for (_, dirs, _) in os.walk(path):
            for dir in dirs:
                mirror_logger.info(f"Found project {dir}")

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
    mirror_logger.info(f"Starting mirror between '{mirror_dir}' and {root_dir}")

    root_projects = Project.find_projects(root_dir, True)
    mirror_projects = Project.find_projects(mirror_dir, False)

    # Let user know if project counts differ
    if len(root_projects) != len(mirror_projects):
        mirror_logger.info("Project counts differ")

    # Let user know if we did not find any projects
    if len(root_projects) == 0 and len(mirror_projects) == 0:
        mirror_logger.fatal("Could not find any projects")
        return

    # Find projects that aren't mirrored
    names = [x.name for x in root_projects].append([x.name for x in mirror_projects])
    known = set()
    diff = [x for x in names if x not in known and not known.add(x)]

    # Print projects that aren't mirrored
    for name in diff:
        mirror_logger.info(f"Found unmirrored project '{name}'")

    # Mirror forever
    while True:
        mirror_logger.warning("Not configured to do anything")
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