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
def config_logging(module, level=logging.INFO):
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
    formatter = logging.Formatter(f"%(asctime)s - {name}.%(levelname)-5s - %(message)s")
    file_handler = logging.FileHandler(str(dir))
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    # Print initialization message
    logger.info("Logging started")

    return logger

# Logging object
utils_logger = config_logging(Path(__file__).name.replace(".py", ""))

# Global constants
PROJECT_CONFIG = "projects/.meta.toml"
# TODO (DWM): revert from test
ROOT_DIRECTORY = "C:/Users/{user}/Documents/My Games/Stationeers/test"
MIRROR_DIRECTORY = "./projects"
MIRROR_PERIOD = 1
FRIENDLY_FILE_NAME = "instruction.ic10"
META_FILE_NAME = "instruction.toml"
XML_FILE_NAME = "instruction.xml"

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
        
