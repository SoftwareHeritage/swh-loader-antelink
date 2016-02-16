# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""Module in charge of loading the 'aws s3 ls' data output in
antelink.content_s3 table."""


import os
import sys

from swh.loader.antelink import utils
from swh.loader.antelink.db import Db


def load_data(path):
    """Load file and yield sha1, pathname couple."""
    with open(path, 'r') as f:
        for line in f:
            data = line.rstrip().split(' ')
            l = len(data)
            pathname = data[l - 1]
            if pathname.endswith('.gz'):
                sha1 = bytes.fromhex(os.path.basename(pathname).split('.')[0])
                length = data[l - 2]
                yield {'sha1': sha1,
                       'path': pathname,
                       'length': length}


def store_file_to_antelink_db(db, path):
    with db.transaction() as cur:
        # group data per 50000-sized data block
        splitdata = utils.grouper(load_data(path), 50000, fillvalue=None)
        for data in splitdata:
            db.copy_to((d for d in data if d), 'content_s3_2',
                       ['sha1', 'path', 'length'], cur)


def store_file_and_print_result(db, path):
    """Try and store the file in the db connection.
    This prints ok or ko depending on the result.

    """
    try:
        store_file_to_antelink_db(db, path)
        print('%s ok' % path)
    except Exception as e:
        print('%s ko %s' % (path, e))


if __name__ == '__main__':
    db_url = "%s" % sys.argv[1]

    db = Db.connect(db_url)
    for line in sys.stdin:
        filepath = line.rstrip()

        if not os.path.exists(filepath):
            print('Path %s does not exist.' % filepath)

        if os.path.isfile(filepath):
            store_file_and_print_result(db, filepath)
