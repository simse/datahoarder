import threading
import time

from datahoarder.config import *
from datahoarder.source import SourceThread
from datahoarder.models import clean_db


class RunThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name='RunThread')

    def run(self):
        clean_db()
        sync()

        while True:
            sync()

            time.sleep(600)


def sync():
    sources = config['sources']

    try:
        for source in sources:
            SourceThread(source).start()
    except RuntimeError:
        pass
