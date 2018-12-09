from datahoarder.source_helpers import *


def run(args):
    mirror = args['mirror']
    isos = find_isos(mirror)
    files = {}

    for iso in isos:
        # Works with current Ubuntu naming scheme e.g. ubuntu-18.04.iso
        version = iso.lower().split('linuxmint-')[-1].split('-')[0]

        if version not in files:
            files[version] = [iso]

        else:
            files[version].append(iso)

    return [
        files,
        info()['meta']['friendly_name']
    ]


def info():
    return {
        'meta': {
            'id': 'linuxmint',
            'friendly_name': 'Linux Mint',
            'short_description': 'Downloads all available Limux Mint images.',
            'category': 'linux_distro'
        },
        'args': {
            'mirror': {
                'type': 'str',
                'default': 'http://mirrors.dotsrc.org/linuxmint-cd/stable/'
            }
        }
    }
