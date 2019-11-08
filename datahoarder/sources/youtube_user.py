from datahoarder.helpers.source import *
from datahoarder.cache import *


@cached(cache)
def run(args):
    dh = DatahoarderSource(args)
    channel = dh.get('channel')

    files = {
        'simon':[
            {'type': 'youtube', 'url': "https://www.youtube.com/watch?v=-nTlH-9zPEk"},
            {'type': 'youtube', 'url': "https://www.youtube.com/watch?v=mntweGmTvS4"},
            {'type': 'youtube', 'url': "https://www.youtube.com/watch?v=1J3SsBngDUo"},
            {'type': 'youtube', 'url': "https://www.youtube.com/watch?v=Gjl-RU2VegY"}
        ]
    }

    return return_args(files)


def info():
    return {
        'meta': {
            'id': 'youtube',
            'friendly_name': 'YouTube Channel',
            'short_description': 'Download all videos from a given YouTube channel.',
            'category': 'media'
        },
        'args': [
            {
                'type': 'str',
                'name': 'channel',
                'friendly_name': 'Youtube Channel URL'
            },
            {
                'type': 'str',
                'name': 'api_key',
                'friendly_name': 'Youtube API key'
            }
        ]
    }


def name(args):
    dh = DatahoarderSource(args)
    channel = dh.get('channel')

    return "Simon"