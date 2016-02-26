# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import sys

from swh.loader.antelink import utils
from swh.loader.antelink.db import Db


def list_files(db_url, limit=None):
    db = Db.connect(db_url)
    with db.transaction() as cur:
        for path in db.read_content_sesi_not_in_swh(limit=limit, cur=cur):
            yield path[0]


if __name__ == '__main__':
    largv = len(sys.argv)
    db_url = "%s" % sys.argv[1]
    if largv > 2:
        block_size = int(sys.argv[2])
    else:
        block_size = 1000

    if largv > 3:
        limit = int(sys.argv[3])
    else:
        limit = None

    from swh.scheduler.celery_backend.config import app
    from swh.loader.antelink import tasks  # noqa

    genpaths = utils.grouper(list_files(db_url, limit),
                             block_size, fillvalue=None)
    for paths in genpaths:
        app.tasks['swh.loader.antelink.tasks.AntelinkSesiInjecterTsk'].delay(
            list(p for p in paths if p))
