#!/usr/bin/python3

import logging
import os
import re
import sys

import gzip

from swh.loader.antelink import hashutil

dry_run = False
LOG_LEVEL = logging.WARN  # logging.INFO

SHA1_RE = re.compile(r'^[0-9a-fA-F]{40}$')
TMP_SAS = '/antelink/store0/tmp-compute-checksums/'
MAX_SIZE_TARBALL =  2*1024*1024*1024  # 2G tarball threshold


def is_sha1(s):
    return bool(re.match(SHA1_RE, s))


def compute_hash(path):
    with gzip.open(path, 'rb') as inp:
        return hashutil.hashdata(inp.read())


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

        filesize = os.lstat(path).st_size
        if filesize >= MAX_SIZE_TARBALL:
            logging.warn('Huge compressed file (%s, %s) detected... '
                         'Skipping computation for now.'
                         % (path, filesize))
            # print out the path without computations
            print(','.join(['','','','',path,'']))
            continue
        else:
            logging.info('File gz (%s, %s) detected' % (path, filesize))

        try:
            data = compute_hash(path)
        except Exception as e:
            logging.error('Problem during hash computation for (%s, %s)... %s'
                          % (path, filesize, e))
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
    log_file = TMP_SAS + '/compute-checksums.log'
    logging.basicConfig(level=LOG_LEVEL,
                        handlers=[logging.FileHandler(log_file),
                                  logging.StreamHandler()])
    main()
