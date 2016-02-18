# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import gzip
import itertools

from swh.loader.antelink import hashutil


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


def compute_hash(path):
    """Compute the gzip file's hashes and length.

    Args:
        path: path to the gzip file to hash

    Returns:
        dictionary of sha1, sha1_git, sha256 and length.

    """
    with gzip.open(path, 'rb') as f:
        l = compute_len(f)
        f.seek(0)
        data = hashutil.hashfile(f, length=l)
        data['length'] = l
        return data
