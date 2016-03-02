# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import click

from swh.loader.antelink.db import Db


task_name = 'swh.loader.antelink.tasks.AntelinkSesiInjecterTsk'


def list_files(db_url, limit=None):
    db = Db.connect(db_url)
    with db.transaction() as cur:
        for path in db.read_content_sesi_not_in_swh(limit=limit, cur=cur):
            yield path[0], path[1]


@click.command()
@click.option('--db-url', default='service=swh-antelink', help='Db access')
@click.option('--block-size', default=104857600,
              help='Default block size in bytes (100Mib).')
@click.option('--limit', default=None, help='Limit data to fetch.')
def compute_sesi_jobs(db_url, block_size, limit):
    """Compute the paths to retrieve from sesi and inject in swh.

    It will compute ~block_size (bytes) of files (paths) to retrieve
    and send it to the queue for workers to download and inject in swh.

    """
    from swh.scheduler.celery_backend.config import app
    from swh.loader.antelink import tasks  # noqa

    accu_size = 0
    paths = []
    nb_blocks = 0
    for path, length in list_files(db_url, limit):
        accu_size += length
        paths.append(path)

        if accu_size >= block_size:
            nb_blocks += 1
            app.tasks[task_name].delay(paths)
            print('%s paths (%s bytes) sent.' % (len(paths), accu_size))
            paths = []
            accu_size = 0

    # if remaining paths
    if accu_size > 0 or paths:
        app.tasks[task_name].delay(paths)
        nb_blocks += 1
        print('%s remaining paths (%s bytes) sent.' % (len(paths), accu_size))

    print('Number of jobs: %s' % nb_blocks)

if __name__ == '__main__':
    compute_sesi_jobs()
