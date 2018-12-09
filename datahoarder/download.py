# Python dependencies
import json
import os

# Third-party dependencies
import requests


DOWNLOAD_STATUS = '.downloading'


def register_download(filename, progress=0):
    if os.path.isfile(DOWNLOAD_STATUS):
        status_file = open(DOWNLOAD_STATUS, 'r')
        status = json.loads(status_file.read())
        status[filename] = progress
        status_file.close()

    else:
        status = dict()
        status[filename] = progress

    status_file = open(DOWNLOAD_STATUS, 'w')
    status_file.write(json.dumps(status))
    status_file.close()


def remove_download(filename):
    if os.path.isfile(DOWNLOAD_STATUS):
        status_file = open(DOWNLOAD_STATUS, 'r')
        status = json.loads(status_file.read())
        del status[filename]
        status_file.close()

        status_file = open(DOWNLOAD_STATUS, 'w')
        status_file.write(json.dumps(status))
        status_file.close()


def get_download_status():
    if os.path.isfile(DOWNLOAD_STATUS):
        status_file = open(DOWNLOAD_STATUS, 'r').read()

        return json.loads(status_file)


def remove_status_file():
    if os.path.isfile(DOWNLOAD_STATUS):
        os.remove(DOWNLOAD_STATUS)


def download(url, filename):
    with open(filename, 'wb') as f:
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
                register_download(filename, done)

    remove_download(filename)
