import threading
import importlib
import time
from datahoarder.config import *
from datahoarder.archive import *
from datahoarder.download import remove_status_file


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

                # Execute run function
                source_result = getattr(module, 'run')(sources[source])
                files = source_result[0]
                location = source_result[1]

                # Process items
                process_items(location, files)

            except ImportError:

                print('No source named: {}'.format(source))
                pass


