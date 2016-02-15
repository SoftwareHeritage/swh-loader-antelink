# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information


import binascii
import datetime
import functools
import json
import psycopg2
import tempfile


from contextlib import contextmanager


def stored_procedure(stored_proc):
    """decorator to execute remote stored procedure, specified as argument

    Generally, the body of the decorated function should be empty. If it is
    not, the stored procedure will be executed first; the function body then.

    """
    def wrap(meth):
        @functools.wraps(meth)
        def _meth(self, *args, **kwargs):
            cur = kwargs.get('cur', None)
            self._cursor(cur).execute('SELECT %s()' % stored_proc)
            meth(self, *args, **kwargs)
        return _meth
    return wrap


def jsonize(value):
    """Convert a value to a psycopg2 JSON object if necessary"""
    if isinstance(value, dict):
        return psycopg2.extras.Json(value)

    return value


def entry_to_bytes(entry):
    """Convert an entry coming from the database to bytes"""
    if isinstance(entry, memoryview):
        return entry.tobytes()
    if isinstance(entry, list):
        return [entry_to_bytes(value) for value in entry]
    return entry


def line_to_bytes(line):
    """Convert a line coming from the database to bytes"""
    return line.__class__(entry_to_bytes(entry) for entry in line)


def cursor_to_bytes(cursor):
    """Yield all the data from a cursor as bytes"""
    yield from (line_to_bytes(line) for line in cursor)


class Db:
    """Proxy to the SWH DB, with wrappers around stored procedures

    """

    @classmethod
    def connect(cls, *args, **kwargs):
        """factory method to create a DB proxy

        Accepts all arguments of psycopg2.connect; only some specific
        possibilities are reported below.

        Args:
            connstring: libpq2 connection string

        """
        conn = psycopg2.connect(*args, **kwargs)
        return cls(conn)

    def _cursor(self, cur_arg):
        """get a cursor: from cur_arg if given, or a fresh one otherwise

        meant to avoid boilerplate if/then/else in methods that proxy stored
        procedures

        """
        if cur_arg is not None:
            return cur_arg
        # elif self.cur is not None:
        #     return self.cur
        else:
            return self.conn.cursor()

    def __init__(self, conn):
        """create a DB proxy

        Args:
            conn: psycopg2 connection to the SWH DB

        """
        self.conn = conn

    @contextmanager
    def transaction(self):
        """context manager to execute within a DB transaction

        Yields:
            a psycopg2 cursor

        """
        with self.conn.cursor() as cur:
            try:
                yield cur
                self.conn.commit()
            except:
                if not self.conn.closed:
                    self.conn.rollback()
                raise

    def copy_to(self, items, tblname, columns, cur=None, item_cb=None):
        def escape(data):
            if data is None:
                return ''
            if isinstance(data, bytes):
                return '\\x%s' % binascii.hexlify(data).decode('ascii')
            elif isinstance(data, str):
                return '"%s"' % data.replace('"', '""')
            elif isinstance(data, datetime.datetime):
                # We escape twice to make sure the string generated by
                # isoformat gets escaped
                return escape(data.isoformat())
            elif isinstance(data, dict):
                return escape(json.dumps(data))
            elif isinstance(data, list):
                return escape("{%s}" % ','.join(escape(d) for d in data))
            elif isinstance(data, psycopg2.extras.Range):
                # We escape twice here too, so that we make sure
                # everything gets passed to copy properly
                return escape(
                    '%s%s,%s%s' % (
                        '[' if data.lower_inc else '(',
                        '-infinity' if data.lower_inf else escape(data.lower),
                        'infinity' if data.upper_inf else escape(data.upper),
                        ']' if data.upper_inc else ')',
                    )
                )
            else:
                # We don't escape here to make sure we pass literals properly
                return str(data)
        with tempfile.TemporaryFile('w+') as f:
            for d in items:
                if item_cb is not None:
                    item_cb(d)
                line = [escape(d.get(k)) for k in columns]
                f.write(','.join(line))
                f.write('\n')
            f.seek(0)
            self._cursor(cur).copy_expert('COPY %s (%s) FROM STDIN CSV' % (
                tblname, ', '.join(columns)), f)

    def read_sha1(self, cur=None):
        cur = self._cursor(cur)

        # cur.execute("""select sha1, path from content
        #                union select sha1, path from content_s3""")

        # yield from cursor_to_bytes(cur)

        with open('export-content.csv') as f:
            for line in f:
                l = line.rstrip('\n').split('\t')
                hash = bytes.fromhex(l[0].replace('\\\\x', ''))
                path = l[1]
                yield hash, path

    def read_content_s3_not_in_sesi(self, cur=None):
        cur = self._cursor(cur)

        cur.execute('SELECT path FROM content_s3_not_in_sesi LIMIT 3');

        yield from cursor_to_bytes(cur)
