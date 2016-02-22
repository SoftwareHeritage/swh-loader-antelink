#!/usr/bin/python3

"""Module in charge of computing metadata from sesi's antelink backup.
This outputs the results as csv content with:
sha1,sha1_git,sha256,length,path,corrupted

Note:
- The path is the one from sesi.
- sesi machine has no access to swh's network that's why we output as
  files first

"""

import logging
import os
import re
import sys

from swh.core import hashutil
from swh.loader.antelink import utils

dry_run = False
LOG_LEVEL = logging.WARN  # logging.INFO

SHA1_RE = re.compile(r'^[0-9a-fA-F]{40}$')
MAX_SIZE_TARBALL = None  # 2*1024*1024*1024  # 2G tarball threshold


def is_sha1(s):
    return bool(re.match(SHA1_RE, s))


def main():
    """Expects filepaths to be piped in.
    The filepath is then:
    - check for being named <sha1>.gz (if not skipped)
    - check for existence (if not skipped)
    - check for filesize threshold (if too much, logged and
      computations are skipped for now)
    - hash computation on the uncompressed file and length

    The output is as follows:
    sha1,sha1_git,sha256,length,path,corrupted

    for huge file or hash computation pb file, the output is as follows:
    ,,,,path,

    (The computation will have to be replayed later)

    """
    for line in sys.stdin:
        path = line.rstrip()
        logging.debug('Treating file %s' % path)

        filename = os.path.basename(path)
        sha1_filename = filename.rstrip('.gz')

        if not is_sha1(sha1_filename):
            logging.debug('Skipping non-SHA1 file %s' % sha1_filename)
            continue

        if not os.path.isfile(path):
            logging.warn('file %s is not a regular file, skipping it' % path)
            continue

        if dry_run:
            logging.warn('dry run, do nothing...')
            continue

        filesize = os.lstat(path).st_size
        if MAX_SIZE_TARBALL and filesize >= MAX_SIZE_TARBALL:
            logging.warn('Huge compressed file (%s, %s) detected... '
                         'Skipping computation for now.'
                         % (path, filesize))
            # print out the path without computations
            print(','.join(['', '', '', '', path, '']))
            continue
        else:
            logging.info('File gz (%s, %s) detected' % (path, filesize))

        try:
            data = utils.compute_hash(path)
        except Exception as e:
            logging.error('Problem during hash computation for (%s, %s)... %s'
                          % (path, filesize, e))
            print(','.join(['', '', '', '', path, '']))
            continue

        content_sha1 = hashutil.hash_to_hex(data['sha1'])

        corrupted = False
        if sha1_filename != content_sha1:
            logging.error('File gz (%s, %s) corrupted (content sha1: %s)'
                          % (path, filesize, content_sha1))
            corrupted = True

        data.update({
            'path': path,
            'length': str(data['length']),
            'corrupted': str(corrupted),
        })

        print(','.join([hashutil.hash_to_hex(data['sha1']),
                        hashutil.hash_to_hex(data['sha1_git']),
                        hashutil.hash_to_hex(data['sha256']),
                        data['length'],
                        data['path'],
                        data['corrupted']]))

if __name__ == '__main__':
    process_log_file = sys.argv[1]

    logging.basicConfig(level=LOG_LEVEL,
                        handlers=[logging.FileHandler(process_log_file),
                                  logging.StreamHandler()])
    main()
