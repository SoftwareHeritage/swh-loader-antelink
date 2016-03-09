# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import click

from swh.loader.antelink import utils, storage


task_name = 'swh.loader.antelink.tasks.AntelinkSesiInjecterTsk'


@click.command()
@click.option('--db-url', default='service=swh-antelink', help='Db access.')
@click.option('--block-size', default=104857600,
              help='Default block size in bytes (100Mib).')
@click.option('--block-max-files', default=1000,
              help='Default max number of files (default: 1000).')
@click.option('--limit', default=None, help='Limit data to fetch.')
@click.option('--dry-run', is_flag=True, help='Dry run.')
@click.option('--final', is_flag=True, help='Limit data to fetch.')
def compute_s3_jobs(db_url, block_size, block_max_files, limit, dry_run,
                    final):
    from swh.scheduler.celery_backend.config import app
    from swh.loader.antelink import tasks  # noqa

    store = storage.Storage(db_url)
    if final:
        gen_data = store.read_content_s3_not_in_sesi_nor_in_swh_final(limit)
    else:
        gen_data = store.read_content_s3_not_in_sesi_nor_in_swh(limit)

    # right inputs
    if isinstance(block_size, str):
        block_size = int(block_size)
    if isinstance(block_max_files, str):
        block_max_files = int(block_max_files)
    if limit and isinstance(limit, str):
        limit = int(limit)
    if dry_run:
        print('** DRY RUN **')

    nb_total_blocks = 0
    for paths, size in utils.split_data_per_size(gen_data, block_size,
                                                 block_max_files):
        nb_total_blocks += 1
        print('%s paths (%s bytes) sent.' % (len(paths), size))
        if dry_run:
            continue
        app.tasks[task_name].delay(paths)

    print('Number of jobs: %s' % nb_total_blocks)


if __name__ == '__main__':
    compute_s3_jobs()
