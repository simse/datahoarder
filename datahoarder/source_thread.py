# Python dependencies
import threading

# Third-party dependencies

# Datahoarder dependencies
from datahoarder.source import Source
from datahoarder.archive import process_items


# Run source-thread
class SourceThread(threading.Thread):

    def __init__(self, source_id):
        threading.Thread.__init__(self, name=source_id)
        self.source_id = source_id

    def run(self):
        source = Source(self.source_id)

        # Set source status to searching
        source.set_status('searching')

        # Execute run function
        files = source.run()
        location = source.path()

        # Process items
        process_items(location, files, source.id)

        source.set_status('synced')
