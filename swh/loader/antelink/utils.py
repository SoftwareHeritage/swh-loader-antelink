# Copyright (C) 2015-2017  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import gzip
import os
import sys

from swh.model import hashutil


def compute_len(f):
    """Compute file-like f object's size.

    Returns:
        Length of the file-like f object.

    """
    total = 0
    while True:
        chunk = f.read(hashutil.HASH_BLOCK_SIZE)
        if not chunk:
            break
        total += len(chunk)
    return total


def hashfile(f, with_data=False):
    """hash the content of a file-like object.

    """
    length = compute_len(f)
    f.seek(0)

    if with_data:
        localdata = []

        def add_chunk(chunk, localdata=localdata):
            localdata.append(chunk)

        data = hashutil.hash_file(f, length, chunk_cb=add_chunk)
        data['data'] = b''.join(localdata)
    else:
        data = hashutil.hash_file(f, length)

    data['length'] = length
    return data


def compute_hash(path, with_data=False):
    """Compute the gzip file's hashes and length.

    Args:
        path: path to the gzip file to hash

    Returns:
        dictionary of sha1, sha1_git, sha256 and length.

    """
    with gzip.open(path, 'rb') as f:
        return hashfile(f, with_data=with_data)


def sha1_from_path(path):
    """Path expected to ends with .gz.

    Ex: /some/path/to/<sha1>.gz

    Returns:
        sha1 extracted from the pathname.

    """
    return os.path.basename(path).split('.')[0]


def to_content(path, log=None):
    """Load path into a content for swh.

    """
    data = compute_hash(path, with_data=True)
    data['update'] = 'visible'
    return data


def split_data_per_size(gen_data, block_size, block_max_files):
    """Compute the paths to retrieve from sesi and inject in swh.

    It will compute ~block_size (bytes) of files (paths) to retrieve
    and send it to the queue for workers to download and inject in swh.

    """
    accu_size = 0
    paths = []
    nb_files = 0

    for path, length in gen_data:
        accu_size += length
        paths.append(path)
        nb_files += 1

        if accu_size >= block_size or nb_files >= block_max_files:
            yield paths, accu_size
            paths = []
            accu_size = 0
            nb_files = 0

    # if remaining paths
    if accu_size > 0 or paths:
        yield paths, accu_size


def gen_path_length_from_stdin():
    """Compute the paths to retrieve from sesi and inject in swh.

    It will compute ~block_size (bytes) of files (paths) to retrieve
    and send it to the queue for workers to download and inject in swh.

    """
    for line in sys.stdin:
        line = line.rstrip()
        data = line.split(' ')
        if len(data) > 1:
            yield data[0], int(data[1])
        else:
            yield data[0]
