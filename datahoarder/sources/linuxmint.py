from datahoarder.helpers.source import *
from datahoarder.cache import *


@cached(cache)
def run(args):
    args = parse_args(args)
    mirror = args['mirror']
    files = {}

    for iso in find_isos(mirror):
        # Works with current Ubuntu naming scheme e.g. ubuntu-18.04.iso
        version = iso.lower().split('linuxmint-')[-1].split('-')[0]

        if version not in files:
            files[version] = [iso]

        else:
            files[version].append(iso)

    return return_args(files)


def info():
    return {
        'meta': {
            'id': 'linuxmint',
            'friendly_name': 'Linux Mint',
            'short_description': 'Downloads all available Limux Mint images.',
            'category': 'linux_distros'
        },
        'args': {
            'mirror': {
                'type': 'str',
                'default': 'http://mirrors.dotsrc.org/linuxmint-cd/stable/'
            }
        }
    }
