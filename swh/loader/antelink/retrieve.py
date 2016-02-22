# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""Tryout module to filter data already present in swh storage."""


from swh.storage import get_storage

from swh.loader.antelink import sesi, utils
from swh.loader.antelink.db import Db

DB_CONN = "service='antelink-swh'"

NB_CONTENT_PER_BLOCK = 100000


def read_sha1():
    """Read the sha1 to test again swh...

    """
    db = Db.connect(DB_CONN)
    try:
        keys = ['sha1', 'path']
        with db.transaction() as cur:
            for row in db.read_sha1(cur):
                yield dict(zip(keys, row))
    except Exception as e:
        print('Problem during reading db %s' % e)


if __name__ == '__main__':
    conf = {
        'storage_class': 'remote_storage',
        # 'storage_args': [
        #  'http://uffizi.internal.softwareheritage.org:5002/'],  # prod
        'storage_args': ['http://localhost:5000/'],               # local
    }

    storage = get_storage(conf['storage_class'], conf['storage_args'])

    group_contents = utils.grouper(read_sha1(), NB_CONTENT_PER_BLOCK,
                                   fillvalue=None)

    contents = {}
    contents_from_s3 = {}
    contents_from_sesi = {}

    for group_content in group_contents:
        # keep information about content
        for content in group_content:
            if content:
                # hack: change the db's values
                content['path'] = content['path'] + '.gz'
                contents[content['sha1']] = content

        # check the missing sha1s
        sha1s_missing = storage.content_missing_per_sha1(
            (content['sha1'] for content in group_content if content))

        # check for those missing sha1s if they still exist on sesi
        for sha1 in sha1s_missing:
            c = contents[sha1]
            r = sesi.check_file_exists(c['path'])
            if r:
                print('File %s exists.' % c['path'])
                contents_from_sesi[c['sha1']] = c
            else:
                print('File %s does not exist.' % c['path'])
                contents_from_s3[c['sha1']] = c

    print('sesi: ', len(contents_from_sesi.keys()))
    print('s3: ', len(contents_from_s3.keys()))
