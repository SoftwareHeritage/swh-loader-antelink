import functools
import psycopg2

from .db import Db


def db_transaction_generator(meth):
    """decorator to execute Storage methods within DB transactions, while
    returning a generator

    The decorated method must accept a `cur` keyword argument

    """
    @functools.wraps(meth)
    def _meth(self, *args, **kwargs):
        with self.db.transaction() as cur:
            yield from meth(self, *args, cur=cur, **kwargs)
    return _meth


class Storage():
    """SWH storage proxy, encompassing DB and object storage

    """

    def __init__(self, db_conn):
        """
        Args:
            db_conn: libpq connection string

        """
        try:
            self.db = Db.connect(db_conn)
        except psycopg2.OperationalError as e:
            raise e

    @db_transaction_generator
    def read_content_s3_not_in_sesi_nor_in_swh(self, huge=False, final=False,
                                               limit=None, cur=None):
        """Retrieve paths to retrieve from s3.

        """
        db = self.db
        if huge and final:
            gen_data = db.read_content_s3_not_in_sesi_nor_in_swh_huge_final(
                limit, cur)
        elif huge and not final:
            gen_data = db.read_content_s3_not_in_sesi_nor_in_swh_huge(
                limit, cur)
        elif not huge and final:
            gen_data = db.read_content_s3_not_in_sesi_nor_in_swh_final(
                limit, cur)
        else:
            gen_data = db.read_content_s3_not_in_sesi_nor_in_swh(limit, cur)

        for t in gen_data:
            yield t[0], t[1]

    @db_transaction_generator
    def read_content_sesi_not_in_swh(self, huge=False, limit=None, cur=None):
        """Retrieve paths to retrieve from sesi.

        """
        db = self.db
        if huge:
            gen_data = db.read_content_sesi_not_in_swh_huge(limit, cur)
        else:
            gen_data = db.read_content_sesi_not_in_swh(limit, cur)

        for t in gen_data:
            yield t[0], t[1]
