# Python dependencies
import time
import threading
import os

# Third-party dependencies
import requests

# Datahoarder imports
from datahoarder.models import Download


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
            {'progress': d.progress, 'filename': d.destination, 'url': d.url, 'source': d.source}
            for d in Download.select()
        ]
    except peewee.OperationalError:
        return {}


def http_download(url, filename, source_uid):
    from datahoarder.source import Source

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

                # Check if source still exists
                if not Source.exists(source_uid):
                    remove_download(filename)
                    os.unlink(temporary_filename)
                    return 0

    os.rename(temporary_filename, original_filename)
    remove_download(filename)


def youtube_download(url, filename, source_uid):
    
    pass


class DownloadWatcherThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name='DownloadWatcherThread', daemon=True)

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
            download_status = get_download_status()

            if len(download_status) > 0:
                to_download = download_status[0]

                # Start download thread
                download_thread = DownloadThread(
                    url=to_download['url'],
                    filename=to_download['filename'],
                    uid=to_download['source']
                )
                download_thread.start()

            # Sleep for 1 second
            time.sleep(1)


class DownloadThread(threading.Thread):
    def __init__(self, url, filename, uid):
        threading.Thread.__init__(self, name='DownloadThread', daemon=True)
        self.url = url
        self.filename = filename
        self.source_uid = uid

    def run(self):
        from datahoarder.source import Source
        source = Source(self.source_uid)

        # Check which protocol the source is requesting
        if source.downloader == 'http':
            http_download(self.url, self.filename, self.source_uid)

        elif source.downloader == 'youtube':
            youtube_download(self.url, self.filename, self.source_uid)
            
        else:
            print("Unrecognized downloader!")
