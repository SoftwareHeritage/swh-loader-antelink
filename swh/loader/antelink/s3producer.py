#!/usr/bin/env python3


import sys

from swh.loader.antelink.db import Db


def list_s3_file(db_url):
    db = Db.connect(db_url)
    with db.transaction() as cur:
        for path in db.read_content_s3_not_in_sesi(cur):
            yield path[0]


if __name__ == '__main__':
    db_url = "%s" % sys.argv[1]

    # instantiate celery app with its configuration
    from swh.scheduler.worker import app
    from swh.loader.antelink import tasks  # noqa

    for path in list_s3_file(db_url):
        app.tasks['swh.loader.antelink.tasks.DownloadS3AntelinkFile'].delay(
            path)
