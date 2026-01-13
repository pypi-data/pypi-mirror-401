# Copyright (c) 2025 Manos Stoumpos
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
This module contains the `AsyncConnection` class, which constitutes
the wrapper class that manages `AsyncPyDbAPIv2Connection` instances.
"""

from contextlib import asynccontextmanager

# fmt: off
# isort: off
from asyncio import Lock, current_task # <replace>
# isort: on
# fmt: on
from types import EllipsisType
from typing import Any, AsyncIterator, Self, TypeVar

from onlymaps._drivers import BaseDriver, Driver, UnknownDriver
from onlymaps.asyncio._query import AsyncQuery
from onlymaps.asyncio._spec import AsyncPyDbAPIv2Connection, AsyncPyDbAPIv2Cursor
from onlymaps._utils import (  co_exec, # <include>
    Error,
    AsyncPyDbAPIv2ConnectionFactory,
    assert_is_open,
    get_async_pydbapiv2_conn_factory_and_driver,
    require,
    require_open,
)

__all__ = ["AsyncConnection"]


T = TypeVar("T")


class AsyncConnection:
    """
    This class represents a single connection.
    """

    def __init__(
        self,
        conn_factory: AsyncPyDbAPIv2ConnectionFactory,
        driver: BaseDriver | None = None,
        handle_broken_conn: bool = False,
    ) -> None:
        """
        This class represents a single connection.

        :param `AsyncPyDbAPIv2Connection` conn: A connection instance that
            implements the `AsyncPyDbAPIv2Connection` protocol.
        :param `BaseDriver` | None driver: The connection's underlying driver.
            Defaults to `None` if unknown or not supported.
        :param bool handle_broken_conn: If set to `True`, a broken connection
            is automatically handled by pinging the database before each query.
            If the connection is indeed deemed as broken, a new underlying connection
            is established in its place. Defaults to `False`.
        """
        self.__conn_factory = conn_factory
        self.__driver = driver if driver else UnknownDriver.create()
        self.__handle_broken_conn = handle_broken_conn
        self.__cursor_lock = Lock()
        self.__open_lock = Lock()
        self.__iter_lock = Lock()
        self.__is_open = False
        self.__iteration_id: int | None = None
        self.__transaction_id: int | None = None
        self.__query = AsyncQuery(driver=self.__driver, safe_cursor=self._safe_cursor)
        self.__conn: AsyncPyDbAPIv2Connection

    @property
    def driver(self) -> Driver:
        """
        The connection's underlying driver.
        """
        return self.__driver.tag

    @property
    def is_open(self) -> bool:
        """
        Indicates whether a connection to the database
        has been established or not.
        """
        return self.__is_open

    @property
    def __in_transaction(self) -> bool:
        """
        Returns `True` if there currently exists an
        active transaction, else returns `False`.
        """
        return self.__transaction_id is not None

    @property
    def __context_id(self) -> int:
        """
        Returns an integer uniquely identifying the
        current execution context.
        """
        return id(current_task()) # <replace>

    @classmethod
    def from_conn_str(
        cls, conn_str: str, /, *, connect_timeout: int, **kwargs: Any
    ) -> Self:
        """
        Creates and returns a connection based on the provided
        connection string.

        :param str conn_str: The connection string. A connection
            string must be formatted as such:

            `<DRIVER>://<USER>[:<PASSWORD>]@<HOST>:<PORT>/<DATABASE>`
        :param int connect_timeout: The maximum number of seconds
            to block while waiting for a connection to be established,
            before raising a `TimeoutError`.
        :param Any **kwargs: Any other keyword arguments that are to
            be provided to the underlying connection function. These
            keyword arguments are specific to the driver that is being
            used so as to establish a connection to the database.
        """
        conn_factory, driver = get_async_pydbapiv2_conn_factory_and_driver(
            conn_str,
            False,
            connect_timeout,
            **kwargs,
        )
        return cls(conn_factory, driver)

    async def __aenter__(self) -> Self:  # <async>
        """
        Opens a connection to the database and returns
        the instance itself.
        """
        await self.open()  # <await>
        return self

    async def __aexit__(self, *_: tuple[Any, ...]) -> None:  # <async>
        """
        Closes the connection to the database.
        """
        if self.is_open:
            await self.close()  # <await>

    def __assert_not_iter_same_ctx(self) -> None:
        """
        A function which asserts that there does not exist
        an active iterator in the current execution context.

        :raises RuntimeError: There exists an active iterator
            in this execution context.
        """
        if self.__iteration_id == self.__context_id:
            raise Error.ConnActiveIteratorSameCtx

    def __assert_not_trans_same_ctx(self) -> None:
        """
        A function which asserts that there does not exist
        an active transaction in the current execution context.

        :raises RuntimeError: There exists an active iterator
            in this execution context.
        """
        if self.__transaction_id == self.__context_id:
            raise Error.ConnActiveTransactionSameCtx

    # Assertion functions as decorators.
    __require_not_iter_same_ctx = require(__assert_not_iter_same_ctx)
    __require_not_trans_same_ctx = require(__assert_not_trans_same_ctx)

    @asynccontextmanager
    async def _safe_cursor(self) -> AsyncIterator[AsyncPyDbAPIv2Cursor]:  # <async>
        """
        This context manager can be used so as to provide an `AsyncPyDbAPIv2Cursor`
        instance used to interact with the database. Furthermore, the context
        handles the following:

        1. The cursor is closed after the database interaction is over.

        2. Any changes are committed if appropriate.

        3. In case a cursor cannot be obtained, for example due to the
           database having closed the connection from its side, a new
           connection is established and there is an attempt to obtain
           a second cursor via this new connection. If this fails too,
           no further handling occurs, though the same procedure will
           be followed again during the next query. This is especially
           useful when connection pooling in order to ensure that no
           dead connections remain within the pool.

        NOTE: Case #3 only applies if `self.__handle_broken_conn` has been
              set to `True` and the underlying connection is not in the middle
              of a transaction.
        """

        # If there does not exist an active transaction in the
        # current execution context, then acquire the lock.
        acquire_lock = self.__transaction_id != self.__context_id

        if acquire_lock:
            await self.__cursor_lock.acquire()  # <await>

        try:

            cursor = await self.__cursor(  # <await>
                test_connection=self.__handle_broken_conn and not self.__in_transaction
            )

            try:
                if not self.__in_transaction:
                    self.__driver.init_transaction(self.__conn)
                yield cursor
                is_query_successful = True
            except:
                is_query_successful = False
                if not self.__in_transaction:
                    await self.__conn.rollback()  # <await>
                raise
            finally:
                await co_exec(cursor.close) # <replace>
                # Commit only if query execution was successful
                # and not in the middle of a transaction.
                if is_query_successful and not self.__in_transaction:
                    await self.__conn.commit()  # <await>
        finally:
            if acquire_lock:
                self.__cursor_lock.release()

    @require_open
    @__require_not_iter_same_ctx
    async def exec(self, sql: str, /, *args: Any, **kwargs: Any) -> None:  # <async>
        """
        Executes the given SQL query.

        :param str sql: The SQL query to be executed.
        :param Any *args: A sequence of positional arguments to be used
            as query parameters.
        :param Any **kwargs: A sequence of keyword arguments to be used
            as query parameters.

        :raises RuntimeError: AsyncConnection is not open.
        """
        await self.__query.exec(sql, args, kwargs)  # <await>

    @require_open
    @__require_not_iter_same_ctx
    async def fetch_one_or_none(  # <async>
        self, t: type[T] | EllipsisType, sql: str, /, *args: Any, **kwargs: Any
    ) -> T | Any | None:
        """
        Executes the query and returns a single row object of type `T`,
        if the query resulted in such object, else returns `None`.

        :param `T` | ellipsis t: The type to which the query result is mapped.
            If an `ellipsis` is provided, then no type check/cast occurs.
        :param str sql: The SQL query to be executed.
        :param Any *args: A sequence of positional arguments to be used
            as query parameters.
        :param Any **kwargs: A sequence of keyword arguments to be used
            as query parameters.

        :raises RuntimeError: AsyncConnection is not open.
        """
        return await self.__query.one_or_none(t, sql, args, kwargs)  # <await>

    @require_open
    @__require_not_iter_same_ctx
    async def fetch_one(  # <async>
        self, t: type[T] | EllipsisType, sql: str, /, *args: Any, **kwargs: Any
    ) -> T | Any:
        """
        Executes the query and returns a single row object of type `T`.

        :param `T` | ellipsis t: The type to which the query result is mapped.
            If an `ellipsis` is provided, then no type check/cast occurs.
        :param str sql: The SQL query to be executed.
        :param Any *args: A sequence of positional arguments to be used
            as query parameters.
        :param Any **kwargs: A sequence of keyword arguments to be used
            as query parameters.

        :raises ValueError: No row object was found to return.
        :raises RuntimeError: AsyncConnection is not open.
        """
        return await self.__query.one(t, sql, args, kwargs)  # <await>

    @require_open
    @__require_not_iter_same_ctx
    async def fetch_many(  # <async>
        self, t: type[T] | EllipsisType, sql: str, /, *args: Any, **kwargs: Any
    ) -> list[T] | list[Any]:
        """
        Executes the query and returns a a list of row objects of type `T`.

        :param `T` | ellipsis t: The type to which the query result is mapped.
            If an `ellipsis` is provided, then no type check/cast occurs.
        :param str sql: The SQL query to be executed.
        :param Any *args: A sequence of positional arguments to be used
            as query parameters.
        :param Any **kwargs: A sequence of keyword arguments to be used
            as query parameters.

        :raises RuntimeError: AsyncConnection is not open.
        """
        return await self.__query.many(t, sql, args, kwargs)  # <await>

    @asynccontextmanager
    async def iter(  # <async>
        self,
        t: type[T] | EllipsisType,
        size: int,
        sql: str,
        /,
        *args: Any,
        **kwargs: Any,
    ) -> AsyncIterator[AsyncIterator[list[T]] | AsyncIterator[list[Any]]]:
        """
        Executes the query and returns an iterator on batches of row objects
        of type `T`. Each batch of rows is loaded into memory during the
        iteration.

        :param `T` | ellipsis t: The type to which the query result is mapped.
            If an `ellipsis` is provided, then no type check/cast occurs.
        :param int size: The number of rows each batch contains.
        :param str sql: The SQL query to be executed.
        :param Any *args: A sequence of positional arguments to be used
            as query parameters.
        :param Any **kwargs: A sequence of keyword arguments to be used
            as query parameters.

        :raises RuntimeError: AsyncConnection is not open.
        """
        # pylint: disable=contextmanager-generator-missing-cleanup
        # Can't start a transaction while the connection is closed.
        assert_is_open(self)
        # Can' start an iteration while there is an another active one.
        self.__assert_not_iter_same_ctx()

        async with self.__iter_lock:  # <async>
            if self.__iteration_id is None:
                self.__iteration_id = self.__context_id
            try:
                self.__iteration_id = self.__context_id
                async with self.__query.iter(t, size, sql, args, kwargs) as it:  # <async>
                    yield it
            finally:
                self.__iteration_id = None

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:  # <async>
        """
        Opens a trasnaction so that any changes caused by any
        queries executed under said transaction are either all
        committed together after the transaction successfully exits,
        or none of them are if an exception is raised during the
        transaction.

        :raises RuntimeError: AsyncConnection is not open.
        """
        # Can't start a transaction while the connection is closed.
        assert_is_open(self)
        # Can't start a transaction while an iterator is active.
        self.__assert_not_iter_same_ctx()
        # Can't start a transaction while another transaction is active.
        self.__assert_not_trans_same_ctx()

        # Acquire the cursor lock for the entire lifetime
        # of the transaction.
        async with self.__cursor_lock:  # <async>
            try:
                self.__transaction_id = self.__context_id
                self.__driver.init_transaction(self.__conn)
                yield
                await self.__conn.commit()  # <await>
            except:
                await self.__conn.rollback()  # <await>
                raise
            finally:
                self.__transaction_id = None

    async def open(self) -> None:  # <async>
        """
        Establishes a connection to the database.

        :raises RuntimeError: AsyncConnection is already open.
        """

        # Check for open to avoid any deadlocks
        # in the case when for some reason `open`
        # is called from within an active iterator
        # or transaction.
        if self.__is_open:
            raise Error.DbOpenConnection

        # Re-check if open to avoid the case where two
        # or more threads call `open` at the same time
        # waiting for the lock.
        async with self.__open_lock:  # <async>
            if self.__is_open:
                raise Error.DbOpenConnection

            try:
                self.__conn = self.__driver.init_connection(
                    await self.__conn_factory()  # <await>
                )
                self.__is_open = True
            except:
                self.__is_open = False
                raise

    @__require_not_iter_same_ctx
    @__require_not_trans_same_ctx
    async def close(self) -> None:  # <async>
        """
        Closes the underlying connection to the database.

        :raises RuntimeError: AsyncConnection is not open.
        """
        # Wait for cursor lock to be released so that all currently
        # executing queries finish execution before closing.
        async with self.__cursor_lock:  # <async>

            if not self.__is_open:
                raise Error.DbClosedConnection

            await self.__close()  # <await>

    async def __close(self) -> None:  # <async>
        """
        Closes the underlying connection to the database.

        :NOTE: This function does not aquire a lock and must be
            called while `self.__cursor_lock` has been acquired.
        """
        self.__is_open = False
        await co_exec(self.__conn.close) # <replace>

    async def __cursor(self, test_connection: bool) -> AsyncPyDbAPIv2Cursor:  # <async>
        """
        Obtains a cursor from the underlying connection and returns it.

        :param bool test_connection: If set to `True`, then the connection is tested
            before returning a cursor in order to ensure it's not broken or closed
            by the database, in which case a new connection is established which is
            used to obtain the returned cursor.
        """
        if test_connection:
            try:
                # Obtain a cursor and test the connection.
                cursor = (
                    await co_exec(self.__conn.cursor) # <replace>
                )
                await cursor.execute("SELECT 1 WHERE FALSE")  # <await>
            except:  # pylint: disable=bare-except
                try:
                    # NOTE: The connection is likely to be already closed
                    # at this point, though an attempt to close it
                    # doesn't hurt!
                    await self.__close()  # <await>
                except:  # pylint: disable=bare-except
                    pass
                finally:
                    await self.open()  # <await>
                    test_connection = False

        # Only acquire a cursor if no testing has occurred or
        # if the testing actually failed.
        if not test_connection:
            # fmt: off
            cursor = (
                await co_exec(self.__conn.cursor) # <replace>
            )
            # fmt: on

        return cursor
