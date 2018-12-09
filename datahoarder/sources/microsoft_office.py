
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
            'image': 'http://4.bp.blogspot.com/-HED88Q-SAEg/UAbb_w1DVxI/AAAAAAAAItU/miEPtzBgw80/s1600/Microsoft+Office+logo+2012.png'
        },
        'args': {
            'streams': {
                'type': 'list',
                'default': ['office_2016', 'office_365']
            }
        }
    }