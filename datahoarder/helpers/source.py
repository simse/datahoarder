# Python dependencies
import os
import json
from urllib.parse import urljoin

# Third-party dependencies
from bs4 import BeautifulSoup
import requests


# The master helper class that contains all the goodies for sources
class DatahoarderSource:

    args = None

    def __init__(self, args):
        self.args = json.loads(args)

    def get(self, key):
        return self.args[key]


def find_closest_mirror(mirrors):

    #TODO: Add logic
    return mirrors[0]


def load_static_stream(stream):
    stream = 'static_streams/' + stream + '.json'
    # Make sure static stream exists
    if not os.path.isfile(stream):
        return False

    # Load and parse JSON
    stream = json.loads(open(stream, 'r').read())
    return stream


def parse_args(args):
    return json.loads(args)


def return_args(args):
    return json.dumps(args)


def load_static_streams(streams):
    files = []

    # Get all streams individually
    for stream in streams:
        stream_name = stream
        stream = load_static_stream(stream)

        # TODO: Throw exception
        if not stream:
            print('[DH] Stream {} does not exist'.format(stream_name))
            return False

        files += stream

    return files


def find_isos(url, ignore_keywords=[]):
    parsed_page = BeautifulSoup(requests.get(url).text, 'lxml')
    links = parsed_page.find_all('a')
    checked_links = []
    isos = []

    while len(links) > 0:

        # Process link
        try:
            href = links[0].get('href')  # If link is straight from BS4
            href = urljoin(url, href)
        except AttributeError:
            href = links[0]

        # Check url against constraints
        if verify_url_on_linux_mirror(href, url, checked_links, isos, ignore_keywords):
            # If link ends with iso it's a match!
            if href.endswith('.iso'):
                isos.append(href)

            else:
                # Get links from that page and add them to pool
                current_url = urljoin(url, href)
                additional_links = BeautifulSoup(requests.get(current_url).text, 'lxml').find_all('a')
                for l in additional_links:
                    # Convert relative URL to absolute
                    links.append(urljoin(current_url, l.get('href')))

                checked_links.append(href)
            del links[0]

        else:
            # Prevent link from being checked again
            checked_links.append(href)
            del links[0]

    # Before returning, loop and remove duplicates
    known_isos = []
    filtered_isos = []
    for iso in isos:
        # Check ISO name from URL
        iso_name = iso.split('/')[-1]

        # Check if the ISO has been seen before
        if iso_name not in known_isos:
            known_isos.append(iso_name)
            filtered_isos.append(iso)

    return filtered_isos


def verify_url_on_linux_mirror(url, base_url, ignore, isos, ignore_keywords):

    if url.endswith('.iso'):
        return True

    if url in ignore:
        return False

    if any(keyword in url for keyword in ignore_keywords):
        return False

    # Check if first character is a dot
    if url[0] is '.':
        return False

    # Check if first character is a question mark
    if url[0] is '?':
        return False

    # Check if the href is just a slash
    if url is '/':
        return False

    # Check if href is not a folder
    if not url.endswith('/'):
        return False

    # Check if href points to different domain
    if base_url not in url:
        return False

    # Check if connection is ftp or rsync
    if url.startswith('ftp://') or url.startswith('rsync://'):
        return False

    # Check if ISO has already been found
    if any(url.split('/')[-1] in s for s in isos):
        return False

    # Mirror specific rules
    # Fedora mirror
    if 'armhfp' in url or 'source' in url or 'debug' in url:
        return False

    # Ubuntu mirror
    if 'ubuntu-cd/releases' in url or 'ubuntu-cd/precise' in url:
        return False

    return True
