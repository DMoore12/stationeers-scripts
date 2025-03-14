# Global imports
import os
import re
import logging
from pathlib import Path

# Logging directory
LOGGING_DIRECTORY = "./logs"

# config_logging()
#
# Configures logging support for the application and returns
# a newly created logging object
#
# Arguments:
#   - module - name of module under which to log
def config_logging(module):
    user = os.getlogin()
    dir = Path(LOGGING_DIRECTORY)

    # Create logging directory if it doesn't exist
    if not dir.exists():
        os.mkdir(str(dir))

    # Create user sub-directory if it doesn't exist
    dir = dir.joinpath(user)
    if not dir.exists():
        os.mkdir(str(dir))

    # Logfile is {LOGGING_DIRECTORY}/{user}/{module_name}.log
    dir = dir.joinpath(f"{module}.log")

    # Capture friendly module name for logging
    name = module.upper()
    if len(module) > 3:
        name = name[:3]

    # Get and configure logger
    logger = logging.getLogger(module)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(f"%(asctime)s - {name} -  %(message)s")
    file_handler = logging.FileHandler(str(dir))
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    # Print initialization message
    logger.info("Logging started")

    return logger

# Logging object
utils_logger = config_logging(Path(__file__).name.replace(".py", ""))

# Global constants
ROOT_DIRECTORY = "C:/Users/{user}/Documents/My Games/Stationeers/scripts"
MIRROR_DIRECTORY = "./projects"
MIRROR_PERIOD = 1
FRIENDLY_FILE_NAME = "instruction.ic10"
META_FILE_NAME = "instruction.toml"
XML_FILE_NAME = "instruction.xml"

# Class representing a version comparison
class VersionResult:
    EQUAL        = 0
    LESS_THAN    = 1
    GREATER_THAN = 2

    # compare()
    #
    # Compares two values, returning a version comparison result
    #
    # Arguments:
    #   - v1 - value on left side of comparison
    #   - v2 - value on right side of comparison
    #
    # Returns:
    #   - Version comparison result indicating relative difference
    def compare(v1, v2):
        if v1 < v2:
            return VersionResult.LESS_THAN
        elif v1 > v2:
            return VersionResult.GREATER_THAN
        
        return VersionResult.EQUAL

# Class representing the version of something
class Version:
    major = 0
    minor = 0
    build = 0
    proto = True

    # ___init__()
    #
    # Creates a new version instance with the given targeted version
    #
    # Arguments:
    #   - version_major - major version:
    #   - version_minor - minor version:
    #   - version_build - build version:
    #   - version_proto - boolean indicating if this is a prototype version
    def __init__(self, version_major, version_minor, version_build, version_proto):
        self.major = version_major
        self.minor = version_minor
        self.build = version_build
        self.proto = version_proto

    # islt()
    #
    # Runs the comparison self < input and returns the result
    #
    # Arguments:
    #   - v - version to compare against
    #
    # Returns:
    #   - True when version is less than the input
    def islt(self, v):
        return Version._compare(self, v) == VersionResult.LESS_THAN
    
    # isgt()
    #
    # Runs the comparison self > input and returns the result
    #
    # Arguments:
    #   - v - version to compare against
    #
    # Returns:
    #   - True when version is greater than the input
    def isgt(self, v):
        return Version._compare(self, v) == VersionResult.GREATER_THAN
    
    # iseq()
    #
    # Runs the comparison self == input and returns the result
    #
    # Arguments:
    #   - v - version to compare against
    #
    # Returns:
    #   - True when version is equal to the input
    def iseq(self, v):
        return Version._compare(self, v) == VersionResult.EQUAL

    # islteq()
    #
    # Runs the comparison self <= input and returns the result
    #
    # Arguments:
    #   - v - version to compare against
    #
    # Returns:
    #   - True when version is less than or equal to the input
    def islteq(self, v):
        comp = Version._compare(self, v)

        return comp == VersionResult.LESS_THAN or comp == VersionResult.LESS_THAN
    
    # isgteq()
    #
    # Runs the comparison self >= input and returns the result
    #
    # Arguments:
    #   - v - version to compare against
    #
    # Returns:
    #   - True when version is greater than or equal to the input
    def isgteq(self, v):
        comp = Version._compare(self, v)

        return comp == VersionResult.LESS_THAN or comp == VersionResult.GREATER_THAN

    # compare()
    #
    # Non-static multipurpose comparison function
    #
    # Arguments:
    #   - v - input version for comparison
    #
    # Returns:
    #   - Version comparison result (less than, greater than, or equal)
    def compare(self, v):
        Version._compare(self, v)

    # _compare()
    #
    # Static multipurpose version comparison function
    #
    # Arguments:
    #   - v1 - first version for comparison
    #   - v2 - second version for comparison
    #
    # Returns:
    #   - Version comparison result (less than, greater than, or equal)
    def _compare(v1, v2):
        # Compare major version
        ret = VersionResult.compare(v1.major, v2.major)
        if ret != VersionResult.EQUAL:
            return ret

        # Compare minor version
        ret = VersionResult.compare(v1.minor, v2.minor)
        if ret != VersionResult.EQUAL:
            return ret
        
        # Compare build version
        ret = VersionResult.compare(v1.build, v2.build)
        if ret != VersionResult.EQUAL:
            return ret
        
        # Compare prototype version
        return VersionResult.compare(v1.proto, v2.proto)

# resolved_root_dir
#
# Gets the resolved root directory applying replacements where valid
# and necessary
def resolved_root_dir():
    install_dir = ROOT_DIRECTORY
    sequences = re.findall("{.*}", install_dir)

    for sequence in sequences:
        replacement = ""
        text = sequence[1:len(sequence)-1]

        match text:
            case "user":
                replacement = os.getlogin()

            case _:
                utils_logger.error(f"Unknown match value '{text}'")
                return "."
            
        install_dir = install_dir.replace(sequence, replacement)

    return install_dir
        
