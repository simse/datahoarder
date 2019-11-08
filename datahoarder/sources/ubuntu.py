from datahoarder.helpers.source import *
from datahoarder.cache import *


@cached(cache)
def run(args):
    dh = DatahoarderSource(args)
    mirror = dh.get('mirror')

    versioned_files = {}

    # Sort the files into versions
    for iso in find_isos(mirror):
        # Works with current Ubuntu naming scheme e.g. ubuntu-18.04.iso
        version = iso.split('/ubuntu-')[-1].split('-')[0]

        if version not in versioned_files:
            versioned_files[version] = [{'type': 'http', 'url': iso}]

        else:
            versioned_files[version].append({'type': 'http', 'url': iso})

    return return_args(versioned_files)


def info():
    return {
        'meta': {
            'id': 'ubuntu',
            'friendly_name': 'Ubuntu',
            'short_description': 'Downloads all available Ubuntu images.',
            'category': 'linux_distros'
        },
        'args': [
            {
                'name': 'mirror',
                'friendly_name': 'Mirror',
                'type': 'str',
                'default': 'http://mirror.math.princeton.edu/pub/ubuntu-iso/'
            },
            {
                'name': 'Be a poopyhead?',
                'type': 'boolean'
            },
            {
                'name': 'version',
                'type': 'select',
                'default': None,
                'multiple': True,
                'options': [
                    {
                        'text': 'Yes',
                        'value': 'y'
                    },
                    {
                        'text': 'Maybe',
                        'value': 'm'
                    },
                    {
                        'text': 'No',
                        'value': 'n'
                    }
                ]
            },
        ]
    }
