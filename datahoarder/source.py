# Python dependencies
import os
import json
import threading
import importlib.util
import importlib
from pathlib import Path

# Third-party dependencies


# Datahoarder dependencies
from datahoarder.archive import ARCHIVE_PATH
from datahoarder.models import SourceModel
from datahoarder.download import remove_downloads_from_source
from datahoarder.helpers.utils import folder_size, create_path, random_string


def get_source_metadata(source_name):
    source_module = importlib.import_module('datahoarder.sources.{}'.format(source_name))
    module = source_module  # Save module to class to avoid further imports
    source_info = getattr(source_module, 'info')()

    return {
        'id': source_name,
        'friendly_name': source_info['meta']['friendly_name'],
        'short_description': source_info['meta']['short_description'],
        'category': source_info['meta']['category'],
        'args': source_info['args']
    }

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
        source_id = source.split('.')[-1]
        available_sources.append(get_source_metadata(source_id))

    return available_sources


def get_active_sources():
    active_sources = SourceModel.select()
    detailed_active_sources = {}

    for source in active_sources:
        source = Source(source.uid)

        detailed_active_sources[source.uid] = {
            'args': source.arguments,
            'source': source.get_meta(),
            'size': source.size_on_disk(),
            'status': source.get_status(),
            'uid': source.uid
        }

    return detailed_active_sources


def new_source(source_id, args):
    source_model = SourceModel()
    source_model.uid = random_string()
    source_model.source_id = source_id
    source_model.arguments = json.dumps(args)
    source_model.save()

    return source_model.uid


# Class representing a source; GOTTA REPRESENT
class Source:
    # Source module
    module = None

    # Source DB model
    model = None

    def __init__(self, source_uid):
        self.uid = source_uid

        self.load()

    @staticmethod
    def exists(source_uid):
        try:
            SourceModel.get(SourceModel.uid == source_uid)
        except(Exception):
            return False

        return True

    def load(self):
        # Load metadata from database
        self.model = SourceModel.get(SourceModel.uid == self.uid)
        self.status = self.model.status
        self.id = self.model.source_id
        self.config = self.model.arguments

        # Import module
        source_module = importlib.import_module('datahoarder.sources.{}'.format(self.id))
        self.module = source_module  # Save module to class to avoid further imports
        source_info = getattr(source_module, 'info')()

        self.friendly_name = source_info['meta']['friendly_name']
        self.description = source_info['meta']['short_description']
        self.category = source_info['meta']['category']
        self.downloader = source_info['meta']['downloader']
        self.arguments = source_info['args']

    def remove(self):
        # Remove all source configuration
        SourceModel.get(SourceModel.uid==self.uid).delete_instance()

        # Remove any pending downloads
        remove_downloads_from_source(self.uid)

        return True

    def path(self):
        category = self.category.replace('_', ' ').title()
        path = ARCHIVE_PATH + category + os.path.sep + self.friendly_name

        return path

    def create_path(self):
        create_path(self.path())

    def run(self):
        run = getattr(self.module, 'run')(self.config)

        return json.loads(run)

    def get_meta(self):
        return {
            'args': self.arguments,
            'meta': {
                'uid': self.uid,
                'friendly_name': self.friendly_name,
                'short_description': self.description,
                'category': self.category,
                'status': self.status
            }
        }

    def get_status(self):
        return self.status

    def set_status(self, status='unknown'):
        # Set status here
        self.status = status

        # Update database
        self.model.status = status
        self.model.save()

    def size_on_disk(self):
        try:
            return folder_size(self.path())
        except(FileNotFoundError):
            return 0
