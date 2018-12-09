from datahoarder.source_helpers import *


def run(args):
    mirror = args['mirror']
    isos = find_isos(mirror)
    files = {}

    for iso in isos:
        # Works with current Ubuntu naming scheme e.g. ubuntu-18.04.iso
        version = iso.split('/ubuntu-')[-1].split('-')[0]

        if version not in files:
            files[version] = [iso]

        else:
            files[version].append(iso)

    return [
        files,
        'Ubuntu'
    ]


def info():
    return {
        'meta': {
            'id': 'fedora',
            'friendly_name': 'Ubuntu',
            'short_description': 'It\'s Ubuntu man!',
            'image': 'https://assets.ubuntu.com/v1/048f7fde-ubuntu_black-orange_hex.jpg'
        },
        'args': {
            'mirror': {
                'type': 'str',
                'default': 'http://mirror.math.princeton.edu/pub/ubuntu-iso/'
            }
        }
    }
