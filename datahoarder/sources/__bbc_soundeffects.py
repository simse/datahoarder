# Thank you to: FThompson
from datahoarder.source_helpers import *


def run(args):
    do_cat = args['categories']
    sound_effects = load_static_stream('bbc_soundeffects')
    files = {}

    for sound in sound_effects:
        cat = 'Uncategorized' if sound['category'] == '' else sound['category'].replace(':', '')
        location = 'http://bbcsfx.acropolis.org.uk/assets/' + sound['location']

        if cat not in files:
            files[cat] = [location]

        else:
            files[cat].append(location)

    return [
        files,
        info()['meta']['friendly_name']
    ]


def info():
    return {
        'meta': {
            'id': 'bbc_soundeffects',
            'friendly_name': 'BBC Sound Effect Library',
            'short_description': 'Downloads all 16K sound effects from the public domain library provided by BBC.',
            'category': 'sound',
        },
        'args': {
            'categories': {
                'type': 'bool',
                'default': True
            }
        }
    }
