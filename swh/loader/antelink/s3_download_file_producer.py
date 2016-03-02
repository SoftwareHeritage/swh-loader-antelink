# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import click

from swh.loader.antelink import utils
from swh.loader.antelink.db import Db


def list_files(db_url, limit=None):
    db = Db.connect(db_url)
    with db.transaction() as cur:
        for path in db.read_content_s3_not_in_sesi_nor_in_swh(limit=limit,
                                                              cur=cur):
            yield path[0]


@click.command()
@click.option('--db-url', default='service=swh-antelink', help='Db access.')
@click.option('--block-size', default=1000, help='Default block size to use.')
@click.option('--limit', default=None, help='Limit data to fetch.')
def compute_s3_files(db_url, block_size, limit):
    from swh.scheduler.celery_backend.config import app
    from swh.loader.antelink import tasks  # noqa

    genpaths = utils.grouper(list_files(db_url, limit),
                             block_size, fillvalue=None)
    for paths in genpaths:
        app.tasks['swh.loader.antelink.tasks.AntelinkS3DownloaderTsk'].delay(
            list(p for p in paths if p))


if __name__ == '__main__':
    compute_s3_files()
