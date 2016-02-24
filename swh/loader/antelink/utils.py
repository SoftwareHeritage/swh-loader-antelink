# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import gzip
import itertools
import os

from swh.core import hashutil


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks.

    Args:
        iterable: an iterable
        n: size of block
        fillvalue: value to use for the last block

    Returns:
        fixed-length chunks of blocks as iterables

    """
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


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


def compute_data(f):
    """Compute file-like f object's size.

    Returns:
        Length of the file-like f object.

    """
    data = b''
    while True:
        chunk = f.read(hashutil.HASH_BLOCK_SIZE)
        if not chunk:
            break
        data += chunk
    return data


def compute_hash(path, with_data=False):
    """Compute the gzip file's hashes and length.

    Args:
        path: path to the gzip file to hash

    Returns:
        dictionary of sha1, sha1_git, sha256 and length.

    """
    data = {}
    with gzip.open(path, 'rb') as f:
        if with_data:
            raw = compute_data(f)
            data['data'] = raw
            l = len(raw)
        else:
            l = compute_len(f)

        f.seek(0)
        hashes = hashutil.hashfile(f, length=l)
        hashes.update({
            'length': l,
            'data': data.get('data')
        })
        return hashes


def split_data(data, block_size):
    """Split the data of the generator of block with a given size.
    The last block may be inferior of block_size.

    Args:
        data: generator of data to slice in blocks of size block-size
        block_size: size block to use
    """
    splitdata = grouper(data, block_size, fillvalue=None)
    for _data in splitdata:
        yield (d for d in _data if d)


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
    size = data['length']
    return {
        'sha1': data['sha1'],
        'sha1_git': data['sha1_git'],
        'sha256': data['sha256'],
        'length': size,
        'status': 'visible',
        'data': data['data']
    }
