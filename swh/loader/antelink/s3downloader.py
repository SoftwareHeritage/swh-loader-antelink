# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information


import logging
import os
import subprocess

from swh.core import config
from swh.storage import get_storage


def download_s3_file(s3path, path):
    """Download the s3path file to path."""
    cmd = ['aws', 's3', 'cp', s3path, path]
    subprocess.check_output(cmd, universal_newlines=True)


class AntelinkS3Downloader(config.SWHConfig):
    """A bulk loader for downloading some file from s3.

    """
    DEFAULT_CONFIG = {
        'storage_class': ('str', 'remote_storage'),
        'storage_args': ('list[str]', ['http://localhost:5000/']),
        'bucket': ('string', 's3://antelink-object-storage'),
        'destination_path': ('string', '/home/storage/antelink/s3/'),
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
        localpath = self.config['destination_path'] + dirpath
        s3path = self.config['bucket'] + dirpath

        try:
            if os.path.exists(localpath):
                self.log.warn('%s exists!' % localpath)
            else:
                self.log.info('%s -> %s' % (s3path, localpath))
                download_s3_file(s3path, localpath)
        except Exception as e:
            self.log.error('Problem during retrieval of %s: %s' %
                           (localpath, e))
