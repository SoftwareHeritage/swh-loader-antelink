# Copyright (C) 2015-2016  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import click

from swh.core.utils import grouper
from swh.loader.antelink import storage, utils


def s3_files_to_download(store, huge, final, limit):
    files_gen = store.read_content_s3_not_in_sesi_nor_in_swh(
        huge=huge, final=final, limit=limit)
    for path, _ in files_gen:
        yield path


@click.command()
@click.option('--db-url', help='Db access.')
@click.option('--block-size', default=1000, help='Default block size to use.')
@click.option('--limit', default=None, help='Limit data to fetch.')
@click.option('--final', is_flag=True, help='Add final s3 files.')
@click.option('--huge', is_flag=True, help='Add huge s3 files.')
def compute_s3_files(db_url, block_size, limit, final, huge):
    from swh.scheduler.celery_backend.config import app
    from swh.loader.antelink import tasks  # noqa

    if db_url:
        store = storage.Storage(db_url)
        gen_data = s3_files_to_download(store, huge, final, limit)
    else:
        gen_data = utils.gen_path_length_from_stdin()

    for paths in grouper(gen_data, block_size):
        app.tasks['swh.loader.antelink.tasks.AntelinkS3DownloaderTsk'].delay(
            list(paths))


if __name__ == '__main__':
    compute_s3_files()
