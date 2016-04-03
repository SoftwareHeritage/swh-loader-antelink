# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import click
import sys

from swh.core import hashutil
from swh.core.utils import grouper
from swh.storage import get_storage
from swh.loader.antelink import storage, utils


def gen_path_length_from_stdin():
    """Compute the paths to retrieve from sesi and inject in swh.

    It will compute ~block_size (bytes) of files (paths) to retrieve
    and send it to the queue for workers to download and inject in swh.

    """
    for line in sys.stdin:
        line = line.rstrip()
        data = line.split(' ')
        yield data[0], int(data[1])


def process_paths(paths):
    """Compute map from sha1 to localpath.
    """
    m = {}
    for localpath, size in paths:
        sha1 = hashutil.hex_to_hash(utils.sha1_from_path(localpath))
        m[sha1] = [localpath, size]
    return m


def retrieve_unknown_sha1s(swhstorage, gendata):
    # Compute blocks of 1000 sha1s
    for paths in grouper(gendata, n=1000):
        data = process_paths(paths)
        sha1s_tocheck = list(data.keys())
        if len(sha1s_tocheck) > 0:
            # let those inexistent sha1s flow
            for sha1 in swhstorage.content_missing_per_sha1(sha1s_tocheck):
                yield data[sha1][0], data[sha1][1]


@click.command()
@click.option('--db-url',
              help="""Optional db access.
                      If not specified, wait for stdin entries.""")
@click.option('--block-size',
              default=104857600,
              help='Default block size in bytes (100Mib).')
@click.option('--block-max-files',
              default=1000,
              help='Default max number of files (default: 1000).')
@click.option('--limit', default=None, help='Limit data to fetch.')
@click.option('--dry-run', is_flag=True, help='Dry run.')
@click.option('--huge', is_flag=True, help='Deal with huge files.')
@click.option('--storage-class', default='remote_storage')
@click.option('--storage-args',
              default='http://uffizi.internal.softwareheritage.org:5002/')
def send_jobs(db_url, block_size, block_max_files, limit, dry_run, huge,
              storage_class, storage_args):
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
        store = storage.Storage(db_url)
        gen_data = store.read_content_sesi_not_in_swh(huge, limit)
    else:
        gen_data = gen_path_length_from_stdin()

    if huge:
        task_name = 'swh.loader.antelink.tasks.AntelinkSesiInjecterHugeTsk'
    else:
        task_name = 'swh.loader.antelink.tasks.AntelinkSesiInjecterTsk'

    swhstorage = get_storage(storage_class, storage_args.split(','))
    gen_data = retrieve_unknown_sha1s(swhstorage, gen_data)

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
    send_jobs()
