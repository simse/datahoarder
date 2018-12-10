# Python dependencies
import threading
import importlib.util
import importlib
from pathlib import Path

# Third-party dependencies


# Datahoarder dependencies
from datahoarder.config import *
from datahoarder.archive import process_items, ARCHIVE_PATH
from datahoarder.models import SourceStatus
from datahoarder.download import remove_downloads_from_source


# Functions to query sources and so on
def set_source_status(source, status):
    SourceStatus.delete().where(SourceStatus.source == source).execute()

    source_status = SourceStatus.create(source=source, status=status)

    return source_status.save()


def get_source_status(source):
    # Get the last inserted status for source
    try:
        return SourceStatus.select().where(SourceStatus.source == source).order_by(SourceStatus.added.desc())[0].status
    except:
        return 'Unknown'


def get_info_from_source(source_name):
    module = importlib.import_module('datahoarder.sources.{}'.format(source_name))
    source_info = getattr(module, 'info')()

    source_info['meta']['active'] = source_name in config['sources']

    return source_info


def get_available_sources():
    available_sources = []
    package_name = 'datahoarder.sources'

    # Find package location of sources
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return set()

    # Scan the directory for source modules
    pathname = Path(spec.origin).parent
    ret = set()
    with os.scandir(pathname) as entries:
        for entry in entries:
            # Prevent __init__.py file
            if entry.name.startswith('__'):
                continue
            current = '.'.join((package_name, entry.name.partition('.')[0]))
            if entry.is_file():
                # Make sure it's actually a Python module
                if entry.name.endswith('.py'):
                    ret.add(current)

    # Execute info function in module
    for source in ret:
        available_sources.append(get_info_from_source(source.split('.')[-1]))

    return available_sources


def get_active_sources():
    active_sources = config['sources']
    detailed_active_sources = {}

    for source_name in active_sources:
        # Attempt to get folder size
        try:
            source_size = folder_size(ARCHIVE_PATH + get_info_from_source(source_name)['meta']['friendly_name'])
        # If the folder doesn't exist, the source is likely brand new
        except FileNotFoundError:
            source_size = 0

        detailed_active_sources[source_name] = {
            'config': config['sources'][source_name],
            'source': get_info_from_source(source_name),
            'size': source_size,
            'status': get_source_status(source_name)
        }

    return detailed_active_sources


def folder_size(path='.'):
    total = 0
    # Get all items in directory
    for entry in os.scandir(path):
        # Check if it's a file
        if entry.is_file():
            # If it is, add size to total
            total += entry.stat().st_size
        elif entry.is_dir():
            # If it is a folder run function again, recursively
            total += folder_size(entry.path)
    return total


def remove_source(source):
    try:
        del config['sources'][source]
        save_config(config)

        # Remove any pending downloads
        remove_downloads_from_source(source)

        # Stop any threads related to the source
        for t in threading.enumerate():
            if t.getName() is source:
                t._stop()


    except KeyError:
        return False

    return True


# Run source-thread
class SourceThread(threading.Thread):

    def __init__(self, source_id):
        threading.Thread.__init__(self, name=source_id)
        self.source_id = source_id

    def run(self):
        source = self.source_id

        module = importlib.import_module('datahoarder.sources.{}'.format(source))

        # Set source status to searching
        set_source_status(source, 'searching')

        # Execute run function
        source_result = getattr(module, 'run')(config['sources'][source])
        files = source_result[0]
        location = source_result[1]

        # Set source status to downloading
        set_source_status(source, 'downloading')

        # Process items
        process_items(location, files, source)

        # Set source status to synced
        set_source_status(source, 'synced')

