from datahoarder import web
from datahoarder import run
from datahoarder import download

web_thread = web.WebThread()
web_thread.start()

run_thread = run.RunThread()
run_thread.start()

download_thread = download.DownloadWatcherThread()
download_thread.start()
