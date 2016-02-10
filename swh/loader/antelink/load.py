# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os
import glob
import sys

from swh.loader.antelink.db import Db


DB_CONN = "service='antelink-swh'"


def load_file(path):
    """Load file and yield sha1, pathname couple."""
    with open(path, 'r') as f:
        for line in f:
            data = line.rstrip('\n').split(' ')
            pathname = data[len(data) - 1]
            if pathname.endswith('.gz'):
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


def store_file_and_print_result(db, path):
    """Try and store the file in the db connection.
    This prints ok or ko depending on the result.

    """
    res = store_file_to_antelink_db(db, path)
    if res:
        print('%s ok' % path)
    else:
        print('%s ko' % path)


def store_initial_round(dirpath):
    """Starting from scratch, this will fetch all *.ls files and injects
    them in db.

    """
    db = Db.connect(DB_CONN)
    for path in glob.glob(dirpath + '*.ls'):
        store_file_and_print_result(db, path)


def store_second_round(path):
    """The first round finished, there were errors. Adapting the code and
    running this command will finish appropriately the first round.

    """
    db = Db.connect(DB_CONN)
    with open(path, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.endswith('ko'):
                failed_filepath = line.split(' ')[0]
                store_file_and_print_result(db, failed_filepath)


if __name__ == '__main__':
    dir_or_file_path = sys.argv[1]

    if not os.path.exists(dir_or_file_path):
        print('Path %s does not exist.' % dir_or_file_path)

    # expects path to antelink-object-storage containing 4096 file
    # with .ls extensions
    if os.path.isdir(dir_or_file_path):
        # dirpath = '/home/tony/work/inria/antelink/antelink-object-storage/'
        dirpath = dir_or_file_path
        store_initial_round(dirpath)  # piping that result in some
                                      # file is a good idea to keep
                                      # the result per file

    # expects output of previous conditional run with 1 absolute
    # filepath separated by 1 space then 'ok|ko' referencing the
    # success|failure of such file injection
    elif os.path.isfile(dir_or_file_path):
        # filepath = '/home/tony/work/inria/repo/swh-environment/swh-loader-antelink/stats/round-1'
        filepath = dir_or_file_path
        store_second_round(filepath)
