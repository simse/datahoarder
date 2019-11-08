# Python dependencies
import os

# Datahoarder dependencies
from datahoarder.download import register_download
from datahoarder.helpers.utils import create_path

ARCHIVE_PATH = os.environ.get('DH_ARCHIVE_PATH', '/archive') + os.path.sep

# Make sure archive path exists
create_path(ARCHIVE_PATH)


def process_items(location, files, source, do_download=False):
    # Make sure location exists
    create_path(location)

    for dest in files:
        final_dest = location + os.path.sep + dest
        create_path(final_dest)

        _files(files[dest], final_dest, source, do_download)


def _files(files, location, source, do_download):
    for file in files:
        if file['type'] == 'http':
            file = file['url']
            file_name = os.path.basename(file).replace('%20', ' ')
            file_destination = location + os.sep + file_name

            if os.path.isfile(file_destination):
                print("{} already in archive!".format(file_name))
                pass

            else:
                print("{} NOT in archive, downloading...".format(file_name))

                if do_download:

                    register_download(file_destination, file_name, file, source, downloader='http')

        elif file['type'] == 'youtube':
            register_download(location, file['url'], file['url'], source, downloader='youtube')
