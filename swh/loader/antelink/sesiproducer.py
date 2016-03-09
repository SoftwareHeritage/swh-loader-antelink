# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import click
import sys

from swh.loader.antelink import storage

task_name = 'swh.loader.antelink.tasks.AntelinkSesiInjecterTsk'


def gen_path_length_from_db(db_url, limit):
    """Retrieve path, length from sesi from the storage.

    It will compute ~block_size (bytes) of files (paths) to retrieve
    and send it to the queue for workers to download and inject in swh.

    """
    store = storage.Storage(db_url)
    yield from store.read_content_sesi_not_in_swh(limit)


def gen_path_length_from_stdin():
    """Compute the paths to retrieve from sesi and inject in swh.

    It will compute ~block_size (bytes) of files (paths) to retrieve
    and send it to the queue for workers to download and inject in swh.

    """
    for line in sys.stdin:
        line = line.rstrip()
        data = line.split(' ')
        yield data[0], int(data[1])


def split_data_per_jobs(gen_data, block_size, block_max_files):
    """Compute the paths to retrieve from sesi and inject in swh.

    It will compute ~block_size (bytes) of files (paths) to retrieve
    and send it to the queue for workers to download and inject in swh.

    """
    accu_size = 0
    paths = []
    nb_files = 0

    for path, length in gen_data:
        accu_size += length
        paths.append(path)
        nb_files += 1

        if accu_size >= block_size or nb_files >= block_max_files:
            yield paths, accu_size
            paths = []
            accu_size = 0
            nb_files = 0

    # if remaining paths
    if accu_size > 0 or paths:
        yield paths, accu_size


@click.command()
@click.option('--db-url', help="""Optional db access.
                                  If not specified, wait for stdin entries.
                               """)
@click.option('--block-size', default=104857600,
              help='Default block size in bytes (100Mib).')
@click.option('--block-max-files', default=1000,
              help='Default max number of files (default: 1000).')
@click.option('--limit', default=None, help='Limit data to fetch.')
@click.option('--dry-run', is_flag=True, help='Dry run.')
def send_jobs(db_url, block_size, block_max_files, limit, dry_run):
    """Send paths for worker to retrieve from sesi machine.

    """
    from swh.scheduler.celery_backend.config import app
    from swh.loader.antelink import tasks  # noqa

    # right inputs
    if isinstance(block_size, str):
        block_size = int(block_size)
    if isinstance(block_max_files, str):
        block_max_files = int(block_max_files)
    if limit and isinstance(limit, str):
        limit = int(limit)
    if dry_run:
        print('** DRY RUN **')

    if db_url:
        gen_data = gen_path_length_from_db(db_url, limit)
    else:
        gen_data = gen_path_length_from_stdin()

    nb_total_blocks = 0
    for paths, size in split_data_per_jobs(gen_data, block_size,
                                           block_max_files):
        nb_total_blocks += 1
        print('%s paths (%s bytes) sent.' % (len(paths), size))
        if dry_run:
            continue
        app.tasks[task_name].delay(paths)

    print('Number of jobs: %s' % nb_total_blocks)


if __name__ == '__main__':
    send_jobs()
