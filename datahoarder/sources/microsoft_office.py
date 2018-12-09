
from datahoarder.source_helpers import *


def run(args):
    # Short generic function
    return [
        load_static_streams(args['streams']),
        'Microsoft Office'
    ]


def info():
    return {
        'meta': {
            'id': 'microsoft_office',
            'friendly_name': 'Microsoft Office',
            'short_description': 'Downloads Office 2016 and Office 365 ISO images.',
            'category': 'software_iso'
        },
        'args': {
            'streams': {
                'type': 'list',
                'default': ['office_2016', 'office_365']
            }
        }
    }