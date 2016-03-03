# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import click

from swh.loader.antelink import storage

task_name = 'swh.loader.antelink.tasks.AntelinkSesiInjecterTsk'


def compute_sesi_jobs(db_url, block_size, block_max_files, limit):
    """Compute the paths to retrieve from sesi and inject in swh.

    It will compute ~block_size (bytes) of files (paths) to retrieve
    and send it to the queue for workers to download and inject in swh.

    """
    accu_size = 0
    paths = []
    nb_files = 0
    store = storage.Storage(db_url)
    for path, length in store.read_content_sesi_not_in_swh(limit):
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
@click.option('--db-url', default='service=swh-antelink', help='Db access')
@click.option('--block-size', default=104857600,
              help='Default block size in bytes (100Mib).')
@click.option('--block-max-files', default=1000,
              help='Default max number of files (default: 1000).')
@click.option('--limit', default=None, help='Limit data to fetch.')
def send_jobs(db_url, block_size, block_max_files, limit):
    """Send paths for worker to retrieve from sesi machine.

    """
    from swh.scheduler.celery_backend.config import app
    from swh.loader.antelink import tasks  # noqa

    nb_total_blocks = 0
    for paths, size in compute_sesi_jobs(db_url, block_size, block_max_files,
                                         limit):
        nb_total_blocks += 1
        print('%s paths (%s bytes) sent.' % (len(paths), size))
        app.tasks[task_name].delay(paths)

    print('Number of jobs: %s' % nb_total_blocks)


if __name__ == '__main__':
    send_jobs()
