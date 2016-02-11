# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import itertools

from swh.storage import get_storage
from swh.core import hashutil

from swh.loader.antelink.db import Db


DB_CONN = "service='antelink-swh'"

NB_CONTENT_PER_BLOCK = 100000


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


def read_sha1():
    """Read the sha1 to test again swh...

    """
    db = Db.connect(DB_CONN)
    try:
        keys = ['sha1', 'path']
        with db.transaction() as cur:
            for row in db.read_sha1(cur):
                yield dict(zip(keys, row))
    except Exception as e:
        print('Problem during reading db %s' % e)


if __name__ == '__main__':
    conf = {
        'storage_class': 'remote_storage',
        # 'storage_args': ['http://uffizi.internal.softwareheritage.org:5002/'],  # prod
        'storage_args': ['http://localhost:5000/'],                               # local
    }

    storage = get_storage(conf['storage_class'], conf['storage_args'])

    group_contents = grouper(read_sha1(), NB_CONTENT_PER_BLOCK, fillvalue=None)

    for group_content in group_contents:
        contents_to_retrieve = storage.content_missing_per_sha1(
            (hashutil.hex_to_hash(content['sha1'])
             for content in group_content if content is not None))

        print(contents_to_retrieve)
