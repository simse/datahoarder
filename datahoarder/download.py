# Python dependencies
import time
import threading
import os

# Third-party dependencies
import requests

# Datahoarder imports
from datahoarder.models import Download
from datahoarder.logger import logger


def update_download(destination, filename, url, source='', progress=-1, downloader='http'):
    import peewee

    try:
        # Attempt to fetch record from database
        download_status = Download.get(Download.filename == filename)
    except peewee.DoesNotExist:
        # If it's not there, create it
        download_status = Download.create(destination=destination, filename=filename, url=url, source=source, downloader=downloader)

    # Update record
    download_status.progress = progress
    download_status.save()


def register_download(destination, filename, url, source, progress=-1, downloader='http'):
    import peewee

    # Make sure download doesn't already exist
    try:
        Download.get(Download.destination == filename)
    except peewee.DoesNotExist:
        update_download(destination, filename, url, source, progress, downloader)


def remove_download(filename):
    import peewee
    try:
        # Get status from Database
        download_status = Download.get(Download.filename == filename)
        download_status.delete_instance()

    except(peewee.OperationalError):
        pass

def remove_downloads_from_source(source):
    downloads = Download.delete().where(Download.source == source)
    downloads.execute()

    return True


def get_download_status():
    import peewee

    try:
        return [
            {
                'progress': d.progress,
                'filename': d.destination,
                'url': d.url,
                'source': d.source,
                'downloader': d.downloader
            }
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
                update_download(filename, os.path.basename(filename), url, progress=done)

                # Check if source still exists
                if not Source.exists(source_uid):
                    remove_download(os.path.basename(filename))
                    os.unlink(temporary_filename)
                    return 0

    os.rename(temporary_filename, original_filename)
    remove_download(os.path.basename(filename))


def update_youtube_progress(d):
    if d['status'] == 'finished':
        remove_download(d['filename'])

    if d['status'] == 'downloading':
        update_download('', d['filename'], d['filename'], progress=round(float(d['_percent_str'].replace('%', '').strip())), downloader='youtube')


def youtube_download(url, path, source_uid):
    import youtube_dl

    ydl_opts = {
        'format': 'bestvideo/best',
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'progress_hooks': [update_youtube_progress],
    }

    ydl = youtube_dl.YoutubeDL(ydl_opts)
    filename = ydl.prepare_filename(ydl.extract_info(url, download=False))
    remove_download(url)

    if(os.path.exists(filename)):
        pass
    else:
        update_download(path, filename, url, progress=0, downloader='youtube', source=source_uid)
        logger.info("Downloading YouTube video: {}".format(url))
        ydl.download([url])
        


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
                    uid=to_download['source'],
                    downloader=to_download['downloader']
                )
                download_thread.start()

            # Sleep for 1 second
            time.sleep(1)


class DownloadThread(threading.Thread):
    def __init__(self, url, filename, uid, downloader):
        threading.Thread.__init__(self, name='DownloadThread', daemon=True)
        self.url = url
        self.filename = filename
        self.source_uid = uid
        self.downloader = downloader

    def run(self):
        # Check which protocol the source is requesting
        if self.downloader == 'http':
            http_download(self.url, self.filename, self.source_uid)

        elif self.downloader == 'youtube':
            youtube_download(self.url, self.filename, self.source_uid)
            
        else:
            print("Unrecognized downloader!")
