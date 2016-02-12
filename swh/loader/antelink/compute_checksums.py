#!/usr/bin/python3

import logging
import os
import re
import sys

import gzip

from swh.loader.antelink import hashutil

dry_run = False
LOG_LEVEL = logging.DEBUG  # logging.INFO

SHA1_RE = re.compile(r'^[0-9a-fA-F]{40}$')
TMP_SAS = '/antelink/store0/tmp-compute-checksums/'


def is_sha1(s):
    return bool(re.match(SHA1_RE, s))


def gunzip(path):
    """Uncompress a path leading to a compressed file.
       Expects a path ending in .gz.

    Returns:
        The path stripped of the .gz if all went well.

    Raises:
        Exception if problem during uncompressing time.

    """
    newpath = os.path.join(TMP_SAS, os.path.basename(path).rstrip('.gz'))
    with gzip.open(path, 'rb') as inp:
        with open(newpath, 'wb') as out:
            out.write(inp.read())
    return newpath


def main():
    """Expects filepath to be piped in."""
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

        logging.info('gzipped %s detected.' % path)

        # decompress the file
        try:
            uncompress_path = gunzip(path)
        except Exception as e:
            logging.error('Problem during uncompression... %s' % e)
            continue
        data = hashutil.hashfile(uncompress_path)
        content_sha1 = hashutil.hash_to_hex(data['sha1'])

        corrupted = False
        if sha1_filename != content_sha1:
            logging.error('file %s is corrupted (content sha1: %s), skipping it'
                          % (path, content_sha1))
            corrupted = True

        data.update({
            'length': os.lstat(uncompress_path).st_size,
            'path': path,
            'corrupted': corrupted,
        })

        # clean up
        if os.path.isfile(uncompress_path):
            os.remove(uncompress_path)

        print(data['sha1'],
              data['sha1_git'],
              data['sha256'],
              data['length'],
              data['path'],
              data['corrupted'])

if __name__ == '__main__':
    log_file = './compute-checksums.log'
    logging.basicConfig(level=LOG_LEVEL,
                        handlers=[logging.FileHandler(log_file),
                                  logging.StreamHandler()])
    main()
