# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information


import logging
import os
import subprocess

from swh.core import config
from swh.storage import get_storage

from swh.loader.antelink import utils, hashutil


DRY_RUN = False


def download_s3_file(s3path, path):
    """Download the s3path file to path."""
    cmd = ['aws', 's3', 'cp', s3path, path]
    subprocess.check_output(cmd, universal_newlines=True)


def to_content(path, log=None, max_content_size=None, origin_id=None):
    """Load path into a content for swh.

    """
    data = utils.compute_hash(path, with_data=True)
    log.info('to content: %s' % data)
    size = data['length']
    ret = {
        'sha1': data['sha1'],
        'sha1_git': data['sha1_git'],
        'sha256': data['sha256'],
        'length': size,
    }

    if max_content_size and size > max_content_size:
        if log:
            log.info('Skipping content %s, too large (%s > %s)' %
                     (hashutil.hash_to_hex(data['sha1']), size,
                      max_content_size))
        ret.update({
            'status': 'absent',
            'reason': 'Content too large',
            'origin': origin_id,
        })
        return ret

    ret.update({
        'status': 'visible',
        'data': data['data']
    })

    return ret


class AntelinkS3Downloader(config.SWHConfig):
    """A bulk loader for downloading some file from s3.

    """
    DEFAULT_CONFIG = {
        'storage_class': ('str', 'remote_storage'),
        'storage_args': ('list[str]', ['http://localhost:5000/']),
        'db_url': ('string', 'service=antelink-swh'),
        'bucket': ('string', 's3://antelink-object-storage'),
        'destination_path': ('string', '/home/storage/antelink/s3/'),
        'max_content_size': ('int', 100 * 1024 * 1024),
    }

    def __init__(self, config):
        self.config = config

        dest_path = self.config['destination_path']
        if not dest_path.endswith('/'):
            self.config['destination_path'] = dest_path + '/'

        s3path = self.config['bucket']
        if not s3path.endswith('/'):
            self.config['bucket'] = s3path + '/'

        self.storage = get_storage(config['storage_class'],
                                   config['storage_args'])

        self.log = logging.getLogger(
            'swh.antelink.loader.AntelinkS3Downloader')

    def process(self, dirpath):
        full_dest_path = self.config['destination_path'] + dirpath
        s3path = self.config['bucket'] + dirpath

        if DRY_RUN:
            self.log.warn('%s -> %s downloaded (dry run)!' % (s3path, full_dest_path))
            return

        if os.path.exists(full_dest_path):
            self.log.warn('%s exists!' % full_dest_path)
        else:
            download_s3_file(s3path, full_dest_path)

        parent_path = os.path.dirname(full_dest_path)
        os.makedirs(parent_path, exist_ok=True)

        try:
            data = to_content(full_dest_path,
                              log=self.log,
                              max_content_size=self.config['max_content_size'])
            self.log.info('content to send: %s' % data)
            self.storage.content_add([data])
        except Exception as e:
            self.log.error('Problem during retrieval of %s: %s' %
                           (full_dest_path, e))
        # finally:
        #     if os.path.exists(full_dest_path):
        #         os.delete(full_dest_path)
