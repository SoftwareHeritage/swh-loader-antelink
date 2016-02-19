# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""Module in charge of loading the data retrieved from sesi's backup.
This expects to receive filepaths from sys.stdin.
Those filepath must point to existing file which are of the form:
sha1,sha1_git,sha256,length,path,corrupted

This is the output format of module swh.loader.antelink.compute_checksums.

The data are stored in table content_sesi_all.

"""

import os
import sys

from swh.core import hashutil

from swh.loader.antelink import utils
from swh.loader.antelink.db import Db


BLOCK_SIZE = 100000


def load_file(path):
    """Load file and yield sha1, pathname couple."""
    with open(path, 'r') as f:
        for line in f:
            data = line.rstrip().split(',')
            path = data[4]
            # some line can be empty on sha1, sha1_git, sha256 (when
            # huge file or pb during hash computation)
            if data[0]:
                yield {'sha1': hashutil.hex_to_hash(data[0]),
                       'sha1_git': hashutil.hex_to_hash(data[1]),
                       'sha256': hashutil.hex_to_hash(data[2]),
                       'length': data[3],
                       'path': path,
                       'corrupted': data[5]}
            else:
                print('Path %s skipped.' % path)


def store_file_content(db_url, path):
    """The first round finished, there were errors. Adapting the code and
    running this command will finish appropriately the first round.

    """
    db = Db.connect(db_url)
    with db.transaction() as cur:
        for data in utils.split_data(load_file(path), BLOCK_SIZE):
            db.copy_to(data, 'content_sesi_all',
                       ['sha1', 'sha1_git', 'sha256', 'length',
                        'path', 'corrupted'], cur)


if __name__ == '__main__':
    db_url = "%s" % sys.argv[1]

    for filepath in sys.stdin:
        filepath = filepath.rstrip()

        if not os.path.exists(filepath):
            print('Path %s does not exist.' % filepath)
            continue

        if not os.path.isfile(filepath):
            print('Path %s does not reference a file.' % filepath)
            continue

        try:
            store_file_content(db_url, filepath)
            print('%s ok' % filepath)
        except Exception as e:
            print('%s ko %s' % (filepath, e))
