from datahoarder.source_helpers import *


def run(args):
    mirror = args['mirror']
    isos = find_isos(mirror,
                     ['cloud', 'contrib', 'cr', 'extras',
                      'fasttrack', 'sclo', 'storage', 'updates', 'virt',
                      'headers', 'source', 'addons', 'scripts', 'testing', 'apt',
                      'docs']
                     )
    files = {}

    for iso in isos:
        # Works with current Ubuntu naming scheme e.g. 	CentOS-4.0-i386-bin1of4.iso
        version = iso.lower().split('centos-')[-1].split('-')[0]

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
            'id': 'centos',
            'friendly_name': 'CentOS',
            'short_description': 'Downloads all available CentOS images, earliest version is current 3.1.',
            'category': 'linux_distro'
        },
        'args': {
            'mirror': {
                'type': 'str',
                'default': 'http://mirror.math.princeton.edu/pub/centos/'
            }
        }
    }
