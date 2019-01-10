import yaml
import os
import logging


class ConfigReader (object):
    script_dir = os.path.dirname(__file__)
    config_file = os.path.join(script_dir, "config.yaml")

    def __init__(self, filename=None):
        if filename is not None:
            self.filename = filename

    def get_config_section(self, section):
        logging.debug("Opening %s for reading configuration.", self.config_file)
        with open(self.config_file, 'r') as ymlconfig:
            config = yaml.load(ymlconfig)
            try:
                sec = config[section]
                return sec
            except KeyError:
                logging.error("Section %s not found in config file.", section)
                return None

