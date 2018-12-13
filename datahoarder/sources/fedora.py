from datahoarder.helpers.source import *
from datahoarder.cache import *


@cached(cache)
def run(args):
    args = parse_args(args)
    mirror = args['mirror']
    files = {}

    for iso in find_isos(mirror):
        # Works with current Fedora url naming
        version = iso.split('releases/')[-1].split('/')[0]

        if version not in files:
            files[version] = [iso]

        else:
            files[version].append(iso)

    return return_args(files)


def info():
    return {
        'meta': {
            'id': 'fedora',
            'friendly_name': 'Fedora',
            'short_description': 'Downloads the latest Fedora releases.',
            'category': 'linux_distros'
        },
        'args': {
            'mirror': {
                'type': 'str',
                'default': 'http://mirror.math.princeton.edu/pub/fedora-secondary/releases/'
            }
        }
    }
