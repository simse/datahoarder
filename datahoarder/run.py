import threading
import time

from datahoarder.source_thread import SourceThread
from datahoarder.models import clean_db, SourceModel
from datahoarder.helpers.source import find_isos


class RunThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name='RunThread', daemon=True)

    def run(self):
        clean_db()
        sync()

        while True:
            sync()

            time.sleep(600)


def sync():
    try:
        for source in SourceModel.select():
            SourceThread(source.uid).start()
    except RuntimeError:
        pass
