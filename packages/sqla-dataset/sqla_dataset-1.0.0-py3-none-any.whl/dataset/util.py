from hashlib import sha1
from urllib.parse import urlparse, urlencode
from collections import OrderedDict
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy import ResultProxy,RowMapping, Row,CursorResult

from typing import Iterator

QUERY_STEP = 1000
row_type = OrderedDict


def convert_row(rt, row:Row):
    if row is None:
        return None
    return rt(zip(row._fields, row))


class DatasetException(Exception):
    pass


def iter_result_proxy(rp: ResultProxy, size: int | None = None)-> Iterator[Row]:
    """Iterate over the ResultProxy."""
    while True:
        if size is None:
            chunk = rp.fetchall()
        else:
            chunk = rp.fetchmany(size=size)
        if not chunk:
            break
        for row in chunk:
            yield row


def make_sqlite_url(
    path,
    cache=None,
    timeout=None,
    mode=None,
    check_same_thread=True,
    immutable=False,
    nolock=False,
):
    # NOTE: this PR
    # https://gerrit.sqlalchemy.org/c/sqlalchemy/sqlalchemy/+/1474/
    # added support for URIs in SQLite
    # The full list of supported URIs is a combination of:
    # https://docs.python.org/3/library/sqlite3.html#sqlite3.connect
    # and
    # https://www.sqlite.org/uri.html
    params = {}
    if cache:
        assert cache in ("shared", "private")
        params["cache"] = cache
    if timeout:
        # Note: if timeout is None, it uses the default timeout
        params["timeout"] = timeout
    if mode:
        assert mode in ("ro", "rw", "rwc")
        params["mode"] = mode
    if nolock:
        params["nolock"] = 1
    if immutable:
        params["immutable"] = 1
    if not check_same_thread:
        params["check_same_thread"] = "false"
    if not params:
        return "sqlite:///" + path
    params["uri"] = "true"
    return "sqlite:///file:" + path + "?" + urlencode(params)


class ResultIter:
    """SQLAlchemy ResultProxies are not iterable to get a
    list of dictionaries. This is to wrap them."""

    def __init__(self, cursor, row_type=row_type, size:int|None=None):
        self.row_type = row_type
        self.cursor = cursor
        try:
            self.keys = list(cursor.keys())
            self._iter = iter_result_proxy(cursor, size=size)
        except ResourceClosedError:
            self.keys = []
            self._iter = iter([])

    def __next__(self):
        try:
            return convert_row(self.row_type, next(self._iter))
        except StopIteration:
            self.close()
            raise

    next = __next__

    def __iter__(self):
        return self

    def close(self):
        self.cursor.close()


def normalize_column_name(name, encoding="utf-8"):
    """Check if a string is a reasonable thing to use as a column name."""
    if not isinstance(name, str):
        raise ValueError("%r is not a valid column name." % name)

    # limit to 63 characters
    name = name.strip()[:63]
    # column names can be 63 *bytes* max in postgresql
    if isinstance(name, str):
        while len(name.encode(encoding=encoding)) >= 64:
            name = name[: len(name) - 1]

    if not len(name) or "." in name or "-" in name:
        raise ValueError("%r is not a valid column name." % name)
    return name


def normalize_column_key(name):
    """Return a comparable column name."""
    if name is None or not isinstance(name, str):
        return None
    return name.upper().strip().replace(" ", "")


def normalize_table_name(name:str):
    """Check if the table name is obviously invalid."""
    if not isinstance(name, str):
        raise ValueError("Invalid table name: %r" % name)
    name = name.strip()[:63]
    if not len(name):
        raise ValueError("Invalid table name: %r" % name)
    return name


def safe_url(url:str):
    """Remove password from printed connection URLs."""
    parsed = urlparse(url)
    if parsed.password is not None:
        pwd = ":%s@" % parsed.password
        url = url.replace(pwd, ":*****@")
    return url


def index_name(table, columns, encoding="utf-8"):
    """Generate an artificial index name."""
    sig = "||".join(columns)
    key = sha1(sig.encode(encoding=encoding)).hexdigest()[:16]
    return "ix_%s_%s" % (table, key)


def pad_chunk_columns(chunk, columns):
    """Given a set of items to be inserted, make sure they all have the
    same columns by padding columns with None if they are missing."""
    for record in chunk:
        for column in columns:
            record.setdefault(column, None)
    return chunk
