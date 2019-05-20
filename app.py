import time

from datahoarder import web
from datahoarder import run
from datahoarder import download

web_thread = web.WebThread()
web_thread.start()

run_thread = run.RunThread()
run_thread.start()

download_thread = download.DownloadWatcherThread()
download_thread.start()


while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nAlright, I'm off to bed then.")
        exit()
