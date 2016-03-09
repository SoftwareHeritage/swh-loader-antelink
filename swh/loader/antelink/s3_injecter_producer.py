# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import click

from swh.loader.antelink import utils, storage


@click.command()
@click.option('--db-url', default='service=swh-antelink', help='Db access.')
@click.option('--block-size', default=1000, help='Default block size to use.')
@click.option('--limit', default=None, help='Limit data to fetch.')
@click.option('--final', is_flag=True, help='Limit data to fetch.')
def compute_s3_jobs(db_url, block_size, limit, final):
    from swh.scheduler.celery_backend.config import app
    from swh.loader.antelink import tasks  # noqa

    store = storage.Storage(db_url)
    if final:
        files_gen = store.read_content_s3_not_in_sesi_nor_in_swh_final(limit)
    else:
        files_gen = store.read_content_s3_not_in_sesi_nor_in_swh(limit)

    for paths in utils.split_data(files_gen, block_size):
        app.tasks['swh.loader.antelink.tasks.AntelinkS3InjecterTsk'].delay(
            list(paths))


if __name__ == '__main__':
    compute_s3_jobs()
