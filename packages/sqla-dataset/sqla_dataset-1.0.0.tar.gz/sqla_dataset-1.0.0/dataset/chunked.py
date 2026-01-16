import itertools
from .table import Table
from typing import Callable,Any,Optional,MutableMapping


ChunkerCallback = Callable[[list], Any]

class InvalidCallback(ValueError):
    pass


class _Chunker:
    """
    _Chunker
    Shared batching logic for chunked table operations.

    :param table: Target table instance used by chunk handlers.
    :type table: object
    :param chunksize: Maximum number of queued items before flushing.
    :type chunksize: int
    :param callback: Optional callable invoked with the pending queue before flush.
    :type callback: Callable[[list], object] | None
    :raises InvalidCallback: If `callback` is provided but not callable.
    """
    table: Table
    callback: Optional[ChunkerCallback]
    queue: list[MutableMapping] = []
    chunksize: int = 1000
    def __init__(self, table:Table,  chunksize=1000, callback: Optional[ChunkerCallback] = None):
        """
        __init__
        Initialize the chunker with a target table and queue parameters.

        :param table: Target table instance used by chunk handlers.
        :param chunksize: Maximum number of queued items before flushing.
        :param callback: Optional callable invoked with the pending queue before flush.
        :raises InvalidCallback: If `callback` is provided but not callable.
        """
        self.queue = []
        self.table = table
        self.chunksize = chunksize
        if callback and not callable(callback):
            raise InvalidCallback
        self.callback = callback

    def flush(self):
        """
        flush
        Clear the current queue without persisting items.
        """
        self.queue.clear()

    def _queue_add(self, item):
        """
        _queue_add
        Append an item to the queue and trigger a flush when the chunk size is reached.

        :param item: Item to enqueue prior to persistence.
        """
        self.queue.append(item)
        if len(self.queue) >= self.chunksize:
            self.flush()

    def __enter__(self):
        """
        __enter__
        Support context manager entry.

        :returns: The current chunker instance.
        :rtype: _Chunker
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        __exit__
        Ensure the queue is flushed on context exit.

        :param exc_type: Exception type raised in the context, if any.
        :type exc_type: type[BaseException] | None
        :param exc_val: Exception instance raised in the context, if any.
        :type exc_val: BaseException | None
        :param exc_tb: Traceback associated with the exception, if any.
        :type exc_tb: TracebackType | None
        """
        self.flush()


class ChunkedInsert(_Chunker):
    """Batch up insert operations
    with ChunkedInsert(my_table) as inserter:
        inserter(row)

    Rows will be inserted in groups of `chunksize` (defaulting to 1000). An
    optional callback can be provided that will be called before the insert.
    This callback takes one parameter which is the queue which is about to be
    inserted into the database
    """

    def __init__(self, table, chunksize=1000, callback=None):
        self.fields = set()
        super().__init__(table, chunksize, callback)

    def insert(self, item):
        self.fields.update(item.keys())
        super()._queue_add(item)

    def flush(self):
        for item in self.queue:
            for field in self.fields:
                item[field] = item.get(field)
        if self.callback is not None:
            self.callback(self.queue)
        self.table.insert_many(self.queue)
        super().flush()


class ChunkedUpdate(_Chunker):
    """Batch up update operations
    with ChunkedUpdate(my_table) as updater:
        updater(row)

    Rows will be updated in groups of `chunksize` (defaulting to 1000). An
    optional callback can be provided that will be called before the update.
    This callback takes one parameter which is the queue which is about to be
    updated into the database
    """

    def __init__(self, table, keys, chunksize=1000, callback=None):
        self.keys = keys
        super().__init__(table, chunksize, callback)

    def update(self, item):
        super()._queue_add(item)

    def flush(self):
        if self.callback is not None:
            self.callback(self.queue)
        self.queue.sort(key=lambda row: tuple(sorted(row.keys())))
        for _, items in itertools.groupby(self.queue, key=lambda row: tuple(sorted(row.keys()))):
            self.table.update_many(list(items), self.keys)
        super().flush()
