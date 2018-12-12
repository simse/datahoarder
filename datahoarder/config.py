import os
import json

# Check if config exists
CONFIG_PATH = os.environ.get('DH_CONFIG_PATH', '/config') + os.path.sep + 'datahoarder.json'
config = None


# Functions for managing config
def save_config(config):
    config_file = open(CONFIG_PATH, 'w')
    config_file.write(json.dumps(config))
    config_file.close()


def load_config():
    global config
    config = json.loads(open(CONFIG_PATH, 'r').read())


# Make sure config exists
if os.path.exists(CONFIG_PATH):

    load_config()

else:
    config = {
        'sources': {}
    }

    save_config(config)
