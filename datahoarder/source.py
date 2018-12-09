# Python dependencies
import os
import importlib.util
import importlib
from pathlib import Path

# Third-party dependencies


# Datahoarder dependencies
from datahoarder.config import *
from datahoarder.archive import ARCHIVE_PATH


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
        detailed_active_sources[source_name] = {
            'config': config['sources'][source_name],
            'source': get_info_from_source(source_name),
            'size': folder_size(ARCHIVE_PATH + get_info_from_source(source_name)['meta']['friendly_name'])
        }

    return detailed_active_sources


def folder_size(path='.'):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)
    return total