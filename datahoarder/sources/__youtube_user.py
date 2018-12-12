from pytube import YouTube

from datahoarder.source_helpers import *


def run(args):
    channels = args['channels']

    files = {}

    for channel in channels:
        pass

    return [
        files,
        info()['meta']['friendly_name']
    ]


def info():
    return {
        'meta': {
            'id': 'youtube_user',
            'friendly_name': 'YouTube Channel',
            'short_description': 'Download all videos from given YouTube channels.',
            'category': 'media'
        },
        'args': {
            'channels': {
                'type': 'list'
            }
        }
    }
