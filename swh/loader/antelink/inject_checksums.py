# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""Module in charge of loading the data retrieved from sesi's backup.
The module swh.loader.antelink.compute_checksums will output the data
needed in csv.  This one will parse and load the data in db
antelink.content_sesi_all.

"""

import os
import sys

from swh.loader.antelink.db import Db
from swh.core import hashutil

DB_CONN = "service='antelink-swh'"


def load_file(path):
    """Load file and yield sha1, pathname couple."""
    with open(path, 'r') as f:
        for line in f:
            data = line.rstrip('\n').split(',')
            yield {'sha1': hashutil.hex_to_hash(data[1]),
                   'sha1_git': hashutil.hex_to_hash(data[1]),
                   'sha256': hashutil.hex_to_hash(data[2]),
                   'length': data[3],
                   'path': data[4],
                   'corrupted': data[5]}


def store_file_content(path):
    """The first round finished, there were errors. Adapting the code and
    running this command will finish appropriately the first round.

    """
    db = Db.connect(DB_CONN)
    with db.transaction() as cur:
        db.copy_to(list(load_file(path)), 'content_sesi_all',
                   ['sha1', 'sha1_git', 'sha256', 'length',
                    'path', 'corrupted'], cur)

if __name__ == '__main__':
    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print('Path %s does not exist.' % filepath)

    # expects output of previous conditional run with 1 absolute
    # filepath separated by 1 space then 'ok|ko' referencing the
    # success|failure of such file injection
    if os.path.isfile(filepath):
        store_file_content(filepath)
