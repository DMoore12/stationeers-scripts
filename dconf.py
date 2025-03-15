import toml
from pathlib import Path
from version import Version

# Declare the global default configuration file. This will be loaded if no alternative is given
DEFAULT_CONFIG = "config.toml"

class Config:
    runs = 0
    version = Version.from_string("0.0.1.b")

    def __init__(self, config=DEFAULT_CONFIG):
        # Create a valid configuration if one doesn't exist
        if not Path(self).exists():
            self.write()
            return
        
        # Load config
        self.load_config(config)

    def write(self):
        # Create empty dicts for data
        data = {}
        inner_data = {}

        # Pack data
        data["version"] = self.version
        inner_data["runs"] = self.runs
        data["meta"] = inner_data

        # Open and write file
        with open(self.meta_file, "w+") as fh:
            toml.dump(data, fh)

    def load_config(self, config):
        # Load config
        with open(config, "r") as fh:
            data = toml.load(fh)

        # Unpack data
        self.runs = data["meta"]["runs"]
