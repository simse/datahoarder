from datahoarder import web
from datahoarder import run

web_thread = web.WebThread()
web_thread.start()

run_thread = run.RunThread()
run_thread.start()
