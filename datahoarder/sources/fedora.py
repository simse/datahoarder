from datahoarder.source_helpers import *


def run(args):
    mirror = args['mirror']
    isos = find_isos(mirror)
    files = {}

    for iso in isos:
        # Works with current Fedora url naming
        version = iso.split('releases/')[-1].split('/')[0]

        if version not in files:
            files[version] = [iso]

        else:
            files[version].append(iso)

    return [
        files,
        'Fedora'
    ]


def info():
    return {
        'meta': {
            'id': 'fedora',
            'friendly_name': 'Fedora',
            'short_description': 'Downloads the latest Fedora releases.',
            'image': 'https://fedoraproject.org/w/uploads/2/2d/Logo_fedoralogo.png'
        },
        'args': {
            'mirror': {
                'type': 'str',
                'default': 'http://mirror.math.princeton.edu/pub/fedora-secondary/releases/'
            }
        }
    }
