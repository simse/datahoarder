import os
import wget

ARCHIVE_PATH = 'Z:\\Archive\\'

# Make sure archive path exists
if not os.path.exists(ARCHIVE_PATH):
    os.mkdir(ARCHIVE_PATH)


def process_items(location, files, do_download=True):

    # Make sure location exists
    if not os.path.exists(ARCHIVE_PATH + location):
        os.mkdir(ARCHIVE_PATH + location)

    if isinstance(files, list):
        _files(files, location, do_download)

    if isinstance(files, dict):
        for dest in files:
            final_dest = location + os.path.sep + dest

            if not os.path.exists(ARCHIVE_PATH + final_dest):
                os.mkdir(ARCHIVE_PATH + final_dest)

            _files(files[dest], final_dest, do_download)


def _files(files, location, do_download):
    for file in files:
        file_name = os.path.basename(file)
        file_destination = ARCHIVE_PATH + location + os.sep + file_name

        if os.path.isfile(file_destination):
            print("{} already in archive!".format(file_name))

        else:
            print("{} NOT in archive, downloading...".format(file_name))

            if do_download:
                download(location, file)


def download(location, file):
    file_name = os.path.basename(file)
    file_destination = ARCHIVE_PATH + location + os.sep + file_name

    print(file_destination)

    wget.download(file, file_destination)
