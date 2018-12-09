from datahoarder.source_helpers import *


def run(args):
    psid = args['psid']
    osID = args['osID']
    languageCode = args['languageCode']

    geforce = requests.get(
        'https://gfwsl.geforce.com/services_toolkit/services/com/nvidia/services/AjaxDriverService.php',
        params={
            'func': 'DriverManualLookup',
            'psid': psid,
            'osID': osID,
            'languageCode': languageCode,
            'numberOfResults': 100
        }
    )

    geforce_drivers = json.loads(geforce.text)['IDS']

    return [
        [d['downloadInfo']['DownloadURL'] for d in geforce_drivers],
        info()['meta']['friendly_name']
    ]


def info():
    return {
        'meta': {
            'id': 'geforce_drivers',
            'friendly_name': 'GeForce Drivers',
            'short_description': 'Downloads all available GeForce drivers with the specified parameters.',
            'category': 'driver'
        },
        'args': {
            'psid': {
                'type': 'int',
                'default': 107
            },
            'osID': {
                'type': 'int',
                'default': 57
            },
            'languageCode': {
                'type': 'int',
                'default': 1033
            }
        }
    }
