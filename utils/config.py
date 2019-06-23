import os
import sys

if sys.version_info.major == 2:
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = ConfigParser()
config.read(os.path.join(BASE_DIR, "config.ini"))


def get_config(section, option):
    return os.getenv("_".join([section, option]).upper()) or config.get(section, option)


if __name__ == "__main__":
    print(config.sections())
