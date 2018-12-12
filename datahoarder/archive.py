import os


from datahoarder.download import register_download

ARCHIVE_PATH = os.environ.get('DH_ARCHIVE_PATH', '/archive') + os.path.sep

# Make sure archive path exists
if not os.path.exists(ARCHIVE_PATH):
    os.mkdir(ARCHIVE_PATH)


def process_items(location, files, source, do_download=True):

    # Make sure location exists
    if not os.path.exists(ARCHIVE_PATH + location):
        os.mkdir(ARCHIVE_PATH + location)

    if isinstance(files, list):
        _files(files, location, source, do_download)

    if isinstance(files, dict):
        for dest in files:
            final_dest = location + os.path.sep + dest

            if not os.path.exists(ARCHIVE_PATH + final_dest):
                os.mkdir(ARCHIVE_PATH + final_dest)

            _files(files[dest], final_dest, source, do_download)


def _files(files, location, source, do_download):
    for file in files:
        file_name = os.path.basename(file).replace('%20', ' ')
        file_destination = ARCHIVE_PATH + location + os.sep + file_name

        if os.path.isfile(file_destination):
            # print("{} already in archive!".format(file_name))
            pass

        else:
            # print("{} NOT in archive, downloading...".format(file_name))

            if do_download:
                file_name = os.path.basename(file)
                file_destination = ARCHIVE_PATH + location + os.sep + file_name

                register_download(file_destination, file, source)
