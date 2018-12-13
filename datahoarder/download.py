# Python dependencies
import time
import threading
import os

# Third-party dependencies
import requests

# Datahoarder imports
from datahoarder.models import Download
from datahoarder.config import config


def update_download(filename, url, source='', progress=0):
    import peewee

    try:
        # Attempt to fetch record from database
        download_status = Download.get(Download.destination == filename)
    except peewee.DoesNotExist:
        # If it's not there, create it
        download_status = Download.create(destination=filename, url=url, source=source)

    # Update record
    download_status.progress = progress
    download_status.save()


def register_download(filename, url, source, progress=0):
    # Check if source still exists before registering download
    if source not in config['sources']:
        return False

    import peewee

    # Make sure download doesn't already exist
    try:
        Download.get(Download.destination == filename)
    except peewee.DoesNotExist:
        update_download(filename, url, source, progress)


def remove_download(filename):
    # Get status from Database
    download_status = Download.get(Download.destination == filename)

    # Only attempt to remove if it exists
    if download_status is not None:
        download_status.delete_instance()


def remove_downloads_from_source(source):
    downloads = Download.delete().where(Download.source == source)
    downloads.execute()

    return True


def get_download_status():
    import peewee

    try:
        return [
            {'progress': d.progress, 'filename': d.destination, 'url': d.url}
            for d in Download.select()
        ]
    except peewee.OperationalError:
        return {}


def download(url, filename):
    original_filename = filename
    temporary_filename = filename + '.tmp'

    with open(temporary_filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                downloaded += len(data)
                f.write(data)
                done = int(100 * downloaded / total)
                update_download(filename, url, progress=done)

    os.rename(temporary_filename, original_filename)
    remove_download(filename)


class DownloadWatcherThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name='DownloadWatcherThread')

    def run(self):
        # Run loop
        while True:
            # Check if there are any files downloading
            skip = False

            for t in threading.enumerate():
                if t.getName() == 'DownloadThread':
                    skip = True

            if skip:
                # Sleep for 1 second and move on
                time.sleep(1)
                continue

            # Check if there are any downloads queued
            try:
                download_status = get_download_status()
                if download_status is not {}:
                    to_download = download_status[0]

                    # Start download thread
                    download_thread = DownloadThread(
                        url=to_download['url'],
                        filename=to_download['filename']
                    )
                    download_thread.start()
            except IndexError:
                pass

            # Sleep for 1 second
            time.sleep(1)


class DownloadThread(threading.Thread):

    def __init__(self, url, filename):
        threading.Thread.__init__(self, name='DownloadThread')
        self.url = url
        self.filename = filename

    def run(self):
        download(self.url, self.filename)
