import logging
import yaml
import logging.config
from os.path import dirname, join, realpath, exists
import os

BASE_DIR = dirname(realpath(__file__))
if not os.path.exists(join(BASE_DIR, "logs")):
    os.mkdir(join(BASE_DIR, "logs"))
    file = open(join(BASE_DIR, "logs") + "/logs.log", "w")
    file.close()

if not exists(join(BASE_DIR, "logs") + "/logs.log"):
    file = open(join(BASE_DIR, "logs") + "/logs.log", "w")
    file.close()

with open("../../speedsive/logging.yml", "rt") as f:
    config = yaml.safe_load(f.read())
    f.close()

logging.config.dictConfig(config)

logger = logging.getLogger("speedsive")
