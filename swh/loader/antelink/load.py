# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os
import glob

from swh.loader.antelink.db import Db


def load_file(path):
    """Load file and yield sha1, pathname couple."""
    with open(path, 'r') as f:
        for line in f:
            data = line.split(' ')
            pathname = data[len(data) - 1].rstrip('\n')
            sha1 = bytes.fromhex(os.path.basename(pathname).split('.')[0])
            yield sha1, pathname


BUFFER_MAX = 10000


def store_file_to_antelink_db(db, path):
    try:
        with db.transaction() as cur:
            buffer_sha1_path = []
            count = 0
            for sha1, pathname in load_file(path):
                buffer_sha1_path.append({'sha1': sha1, 'path': pathname})
                count += 1
                if count >= BUFFER_MAX:
                    db.copy_to(buffer_sha1_path, 'content_s3', ['sha1', 'path'], cur)
                    count = 0
                    buffer_sha1_path = []
        return True
    except:
        return False


if __name__ == '__main__':
    dirpath = '/home/tony/work/inria/antelink/antelink-object-storage/'

    db = Db.connect("service='antelink-swh'")
    for path in glob.glob(dirpath + '*.ls'):
        res = store_file_to_antelink_db(db, path)
        if res:
            print('%s ok' % path)
        else:
            print('%s ko' % path)
