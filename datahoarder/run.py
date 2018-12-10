import threading
import importlib
import time

from datahoarder.config import *
from datahoarder.archive import *
from datahoarder.download import remove_status_file
from datahoarder.source import set_source_status


class RunThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name='RunThread')

    def run(self):
        remove_status_file()

        while True:
            self._run()

            time.sleep(60)

    @staticmethod
    def _run():
        sources = config['sources']

        for source in sources:
            # Import module to handle the source
            try:
                module = importlib.import_module('datahoarder.sources.{}'.format(source))

                # Set source status to searching
                set_source_status(source, 'searching')

                # Execute run function
                source_result = getattr(module, 'run')(sources[source])
                files = source_result[0]
                location = source_result[1]

                # Set source status to downloading
                set_source_status(source, 'downloading')

                # Process items
                process_items(location, files)

                # Set source status to synced
                set_source_status(source, 'synced')

            except ImportError:

                print('No source named: {}'.format(source))
                pass


