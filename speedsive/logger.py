import logging
import yaml
import logging.config
from os.path import dirname, join, realpath, exists
import os
from utils.Path import reducePath

BASE_DIR = dirname(realpath(__file__))

DIR = reducePath(BASE_DIR, 1)
if not os.path.exists(join(DIR, "logs")):
    os.mkdir(join(DIR, "logs"))
    file = open(join(DIR, "logs") + "/logs.log", "w")
    file.close()

if not exists(join(DIR, "logs") + "/logs.log"):
    file = open(join(DIR, "logs") + "/logs.log", "w")
    file.close()

with open("speedsive/logging.yml", "rt") as f:
    config = yaml.safe_load(f.read())
    f.close()

logging.config.dictConfig(config)

logger = logging.getLogger("speedsive")
