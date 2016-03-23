# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.loader.antelink.s3downloader import AntelinkS3Downloader
from swh.loader.antelink.s3injecter import AntelinkS3Injecter
from swh.loader.antelink.sesiinjecter import AntelinkSesiInjecter

from swh.scheduler.task import Task


class AntelinkS3DownloaderTsk(Task):
    """Download an s3 antelink file.

    """
    task_queue = 'swh_antelink_s3_downloader'

    CONFIG_BASE_FILENAME = 'antelink/s3-downloader.ini'
    ADDITIONAL_CONFIG = {}

    def __init__(self):
        self.config = AntelinkS3Downloader.parse_config_file(
            base_filename=self.CONFIG_BASE_FILENAME,
            additional_configs=[self.ADDITIONAL_CONFIG])

    def run(self, s3dirpath):
        """Import a s3 directory path.

        Args:
            cf. swh.loader.antelink.s3downloader.process docstring

        """
        s3downloader = AntelinkS3Downloader(self.config)
        s3downloader.log = self.log
        s3downloader.process(s3dirpath)


class AntelinkS3InjecterTsk(Task):
    """Inject an s3 antelink file.

    """
    task_queue = 'swh_antelink_s3_injecter'

    CONFIG_BASE_FILENAME = 'antelink/s3-injecter.ini'
    ADDITIONAL_CONFIG = {}

    def __init__(self):
        self.config = AntelinkS3Injecter.parse_config_file(
            base_filename=self.CONFIG_BASE_FILENAME,
            additional_configs=[self.ADDITIONAL_CONFIG])

    def run(self, s3dirpath):
        """Import a s3 directory path.

        Args:
            cf. swh.loader.antelink.s3injecter.process docstring

        """
        s3inj = AntelinkS3Injecter(self.config)
        s3inj.log = self.log
        s3inj.process(s3dirpath)


class AntelinkSesiInjecterTsk(Task):
    """Download antelink file from sesi machine.

    """
    task_queue = 'swh_antelink_sesi_downloader'

    CONFIG_BASE_FILENAME = 'antelink/sesi.ini'
    ADDITIONAL_CONFIG = {}

    def __init__(self):
        self.config = AntelinkSesiInjecter.parse_config_file(
            base_filename=self.CONFIG_BASE_FILENAME,
            additional_configs=[self.ADDITIONAL_CONFIG])

    def run(self, paths):
        """Import a bunch of paths from sesi machines.

        Args:
            cf. swh.loader.antelink.sesiinjecter.process docstring

        """
        sesiinjecter = AntelinkSesiInjecter(self.config)
        sesiinjecter.log = self.log
        sesiinjecter.process(paths)
