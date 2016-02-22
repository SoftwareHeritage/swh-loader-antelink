# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.loader.antelink.s3downloader import AntelinkS3Downloader
from swh.loader.antelink.sesidownloader import AntelinkSesiDownloader

from swh.scheduler.task import Task


class DownloadS3AntelinkFile(Task):
    """Download an s3 antelink file.

    """
    task_queue = 'swh_s3_antelink_downloader'

    CONFIG_BASE_FILENAME = 'downloader/antelink.ini'
    ADDITIONAL_CONFIG = {}

    def __init__(self):
        self.config = AntelinkS3Downloader.parse_config_file(
            base_filename=self.CONFIG_BASE_FILENAME,
            additional_configs=[self.ADDITIONAL_CONFIG],
        )

    def run(self, s3dirpath):
        """Import a s3 directory path.

        Args:
            cf. swh.loader.antelink.s3downloader.process docstring

        """
        s3downloader = AntelinkS3Downloader(self.config)
        s3downloader.log = self.log
        s3downloader.process(s3dirpath)


class DownloadSesiAntelinkFiles(Task):
    """Download antelink file from sesi machine.

    """
    task_queue = 'swh_sesi_antelink_downloader'

    CONFIG_BASE_FILENAME = 'downloader/antelink-sesi.ini'
    ADDITIONAL_CONFIG = {}

    def __init__(self):
        self.config = AntelinkS3Downloader.parse_config_file(
            base_filename=self.CONFIG_BASE_FILENAME,
            additional_configs=[self.ADDITIONAL_CONFIG],
        )

    def run(self, paths):
        """Import a bunch of paths from sesi machines.

        Args:
            cf. swh.loader.antelink.sesidownloader.process docstring

        """
        sesidownloader = AntelinkSesiDownloader(self.config)
        sesidownloader.log = self.log
        sesidownloader.process(paths)
