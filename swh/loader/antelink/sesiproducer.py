#!/usr/bin/env python3


import sys

from swh.loader.antelink import utils
from swh.loader.antelink.db import Db


def list_files(db_url):
    db = Db.connect(db_url)
    with db.transaction() as cur:
        for path in db.read_content_sesi_not_in_swh(cur):
            yield path[0]


if __name__ == '__main__':
    db_url = "%s" % sys.argv[1]
    if len(sys.argv) > 2:
        block_size = int(sys.argv[2])
    else:
        block_size = 1000

    # instantiate celery app with its configuration
    from swh.scheduler.celery_backend.config import app
    from swh.loader.antelink import tasks  # noqa

    genpaths = utils.grouper(list_files(db_url),
                             block_size, fillvalue=None)
    for paths in genpaths:
        app.tasks['swh.loader.antelink.tasks.DownloadSesiAntelinkFiles'].delay(
            list(p for p in paths if p))
