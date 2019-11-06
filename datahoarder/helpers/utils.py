# Python dependencies
import os
import random
import string
from pathlib import Path

# Third-party dependencies


def folder_size(folder):
    total = 0

    for entry in os.scandir(folder):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)

    return total


def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def create_path(path):
    Path(path).mkdir(parents=True, exist_ok=True)
