import logging
import yaml
import logging.config

with open('speedsive/logs/logging.yml', 'rt') as f:
    config = yaml.safe_load(f.read())
    f.close()

logging.config.dictConfig(config)

logger = logging.getLogger("speedsive")
