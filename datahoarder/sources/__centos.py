from datahoarder.helpers.source import *
from datahoarder.cache import *


@cached(cache)
def run(args):
    args = parse_args(args)
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

    return return_args(files)


def info():
    return {
        'meta': {
            'id': 'centos',
            'friendly_name': 'CentOS',
            'short_description': 'Downloads all available CentOS images, earliest version is current 3.1.',
            'category': 'linux_distros'
        },
        'args': {
            'mirror': {
                'type': 'str',
                'default': 'http://mirror.math.princeton.edu/pub/centos/'
            }
        }
    }
