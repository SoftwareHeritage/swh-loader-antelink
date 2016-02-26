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


def retrieve_sesi_files(host, sesi_paths, destination_path):
    """Download the sesi_paths files to destination path.

    """
    spaths = (host + ':' + p for p in sesi_paths)
    cmd = ['scp'] + list(spaths) + [destination_path]
    subprocess.check_call(cmd)
    for path in sesi_paths:
        yield os.path.sep.join([destination_path.rstrip('/'),
                                os.path.basename(path)])


class AntelinkSesiDownloader(config.SWHConfig):
    """A bulk loader for downloading some file from s3.

    """
    DEFAULT_CONFIG = {
        'storage_class': ('str', 'remote_storage'),
        'storage_args': ('list[str]', ['http://localhost:5000/']),
        'host': ('string', 'sesi-pv-lc2.inria.fr'),
        'destination_path': ('string',
                             '/srv/storage/space/antelink/inject-checksums/'),
    }

    def __init__(self, config):
        self.config = config

        dest_path = self.config['destination_path']
        if not dest_path.endswith('/'):
            self.config['destination_path'] = dest_path + '/'

        self.storage = get_storage(config['storage_class'],
                                   config['storage_args'])

        self.log = logging.getLogger(
            'swh.antelink.loader.AntelinkSesiDownloader')

    def process_paths(self, paths):
        for localpath in paths:
            if not os.path.exists(localpath):
                self.log.warn('%s does not exist!' % localpath)
                continue

            try:
                data = utils.to_content(localpath, log=self.log)

                # Check for corruption on sha1
                origin_sha1 = utils.sha1_from_path(localpath)
                sha1 = hashutil.hash_to_hex(data['sha1'])
                if origin_sha1 != sha1:
                    self.log.warn('%s corrupted - %s != %s. Skipping!' %
                                  (localpath, origin_sha1, sha1))
                    continue

                self.log.info('%s -> swh' % sha1)
                yield data
            except Exception as e:
                self.log.error('Problem during computation of %s: %s' %
                               (localpath, e))
            finally:
                if os.path.exists(localpath):
                    os.remove(localpath)

    def process(self, paths):
        # Retrieve the data from sesi first
        localpaths = retrieve_sesi_files(self.config['host'],
                                         paths,
                                         self.config['destination_path'])

        # Then process them and store in swh
        data = self.process_paths(localpaths)
        if data:
            self.storage.content_add(data)
