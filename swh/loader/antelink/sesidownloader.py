# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information


import logging
import os
import subprocess

from swh.core import config, hashutil
from swh.storage import get_storage

from swh.loader.antelink import utils


DRY_RUN = False


def retrieve_sesi_file(sesi_path, path):
    """Download the sesi_path file to path."""
    cmd = ['scp', sesi_path, path]
    subprocess.check_output(cmd, universal_newlines=True)


class SesiDownloader(config.SWHConfig):
    """A bulk loader for downloading some file from s3.

    """
    DEFAULT_CONFIG = {
        'storage_class': ('str', 'remote_storage'),
        'storage_args': ('list[str]', ['http://localhost:5000/']),
        'db_url': ('string', 'service=antelink-swh'),
        'host': ('string', 'sesi-pv-lc2.inria.fr'),
        'destination_path': ('string',
                             '/srv/storage/space/antelink/inject-checksums/'),
        'max_content_size': ('int', 100 * 1024 * 1024),
    }

    def __init__(self, config):
        self.config = config

        dest_path = self.config['destination_path']
        if not dest_path.endswith('/'):
            self.config['destination_path'] = dest_path + '/'

        self.storage = get_storage(config['storage_class'],
                                   config['storage_args'])

        self.log = logging.getLogger(
            'swh.antelink.loader.SesiDownloader')

    def process_paths(self, paths):
        # Retrieve the list of files
        for path in paths:
            full_dest_path = self.config['destination_path'] + path
            sesi_path = self.config['host'] + ':' + path

            if DRY_RUN:
                self.log.warn('%s -> %s downloaded (dry run)!' %
                              (sesi_path, full_dest_path))
                return

            if os.path.exists(full_dest_path):
                self.log.warn('%s exists!' % full_dest_path)
            else:
                retrieve_sesi_file(sesi_path, full_dest_path)

            parent_path = os.path.dirname(full_dest_path)
            os.makedirs(parent_path, exist_ok=True)

            try:
                data = utils.to_content(
                    full_dest_path,
                    log=self.log,
                    max_content_size=self.config['max_content_size'])

                # Check for corruption on sha1
                origin_sha1 = utils.sha1_from_path(full_dest_path)
                sha1 = hashutil.hash_to_hex(data['sha1'])
                if origin_sha1 != sha1:
                    self.log.warn('(%s, %s) corrupted! %s != %s! Skipped' %
                                  (sesi_path, full_dest_path, origin_sha1,
                                   sha1))
                    return

                yield data
            except Exception as e:
                self.log.error('Problem during retrieval of %s: %s' %
                               (full_dest_path, e))
            finally:
                if os.path.exists(full_dest_path):
                    os.delete(full_dest_path)

    def process(self, paths):
        data = self.process_paths(paths)
        if data:
            self.storage.content_add(list(data))
