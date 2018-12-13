# Python dependencies
import threading
import importlib.util
import importlib
from pathlib import Path

# Third-party dependencies


# Datahoarder dependencies
from datahoarder.config import *
from datahoarder.archive import ARCHIVE_PATH
from datahoarder.models import SourceStatus
from datahoarder.download import remove_downloads_from_source
from datahoarder.helpers.utils import folder_size, create_path


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
        available_sources.append(Source(source_id).get_meta())

    return available_sources


def get_active_sources():
    active_sources = config['sources']
    detailed_active_sources = {}

    for source_id in active_sources:
        source = Source(source_id)

        detailed_active_sources[source_id] = {
            'config': source.config,
            'source': source.get_meta(),
            'size': source.size_on_disk(),
            'status': source.get_status()
        }

    return detailed_active_sources


# Class representing a source GOTTA REPRESENT
class Source:
    # Source module
    module = None

    # Source values
    id = None
    friendly_name = None
    description = None
    category = None
    arguments = None
    active = False
    config = None

    def __init__(self, source_id):
        self.id = source_id

        # Make sure source exists
        if not self.exists(self.id):
            raise ValueError('This source does not exists: {}'.format(self.id))

        # Load metadata from source and config
        self.load()

    @staticmethod
    def exists(source_id):
        try:
            importlib.import_module('datahoarder.sources.{}'.format(source_id))
        except ImportError:
            return False

        return True

    def load(self):
        # Import module
        source_module = importlib.import_module('datahoarder.sources.{}'.format(self.id))
        self.module = source_module  # Save module to class to avoid further imports
        source_info = getattr(source_module, 'info')()

        self.friendly_name = source_info['meta']['friendly_name']
        self.description = source_info['meta']['short_description']
        self.category = source_info['meta']['category']
        self.arguments = source_info['args']

        self.active = self.id in config['sources']
        if self.active:
            self.config = config['sources'][self.id]

    def remove(self):
        # Remove all source configuration
        try:
            del config['sources'][self.id]
            save_config(config)
        except KeyError:
            pass

        # Remove any pending downloads
        remove_downloads_from_source(self.id)

        # Stop any threads related to the source
        for t in threading.enumerate():
            if t.getName() is self.id:
                t._stop()  # TODO: Find alternative to accessing private thread function

        return True

    def path(self):
        category = self.category.replace('_', ' ').title()
        path = ARCHIVE_PATH + category + os.path.sep + self.friendly_name

        return path

    def create_path(self):
        create_path(self.path())

    def run(self):
        args = json.dumps(self.config)
        run = getattr(self.module, 'run')(args)

        return json.loads(run)

    def get_meta(self):
        return {
            'args': self.arguments,
            'meta': {
                'id': self.id,
                'friendly_name': self.friendly_name,
                'short_description': self.description,
                'category': self.category,
                'active': self.active
            }
        }

    def get_status(self):
        try:
            return SourceStatus \
                    .select() \
                    .where(SourceStatus.source == self.id) \
                    .order_by(
                        SourceStatus.added.desc()
                    )[0].status

        # TODO: Change exception
        except Exception:
            return 'unknown'

    def set_status(self, status='unknown'):
        # First remove any registered statuses for the source
        SourceStatus \
            .delete() \
            .where(SourceStatus.source == self.id) \
            .execute()

        # Then insert new status
        SourceStatus.create(source=self.id, status=status).save()

    def size_on_disk(self):
        return folder_size(self.path())
