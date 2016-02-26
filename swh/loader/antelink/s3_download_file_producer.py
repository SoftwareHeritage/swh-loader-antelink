#!/usr/bin/env python3


import sys

from swh.loader.antelink.db import Db


def list_s3_file(db_url, limit=None):
    db = Db.connect(db_url)
    with db.transaction() as cur:
        for path in db.read_content_s3_not_in_sesi_nor_in_swh(limit=limit,
                                                              cur=cur):
            yield path[0]


if __name__ == '__main__':
    db_url = "%s" % sys.argv[1]
    if len(sys.argv) > 2:
        limit = int(sys.argv[2])
    else:
        limit = None

    from swh.scheduler.celery_backend.config import app
    from swh.loader.antelink import tasks  # noqa

    for path in list_s3_file(db_url, limit):
        app.tasks['swh.loader.antelink.tasks.DownloadS3AntelinkFile'].delay(
            path)
