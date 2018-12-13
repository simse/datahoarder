from datahoarder.helpers.source import *


def run(args):
    args = parse_args(args)

    # Short generic function
    return return_args({
        '': load_static_streams(args['streams'])
    })


def info():
    return {
        'meta': {
            'id': 'microsoft_office',
            'friendly_name': 'Microsoft Office',
            'short_description': 'Downloads Office 2016 and Office 365 ISO images.',
            'category': 'software_isos'
        },
        'args': {
            'streams': {
                'type': 'list',
                'default': ['office_2016', 'office_365']
            }
        }
    }