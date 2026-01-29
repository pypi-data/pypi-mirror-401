"""EvidentSource - the main entrypoint for connecting to an EvidentSource server."""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

import grpc
from evidentsource_core import (
    DatabaseAlreadyExists,
    DatabaseError,
    DatabaseName,
    DatabaseNotFound,
    DatabaseServerError,
)

if TYPE_CHECKING:
    from evidentsource_client.connection import Connection

from evidentsource_client.conversions import timestamp_to_datetime
from evidentsource_client.proto import service_pb2 as proto
from evidentsource_client.proto import service_pb2_grpc as service_grpc


@dataclass
class DatabaseIdentityImpl:
    """Simple database identity returned from create_database."""

    _name: DatabaseName
    _created_at: datetime

    @property
    def name(self) -> DatabaseName:
        """Get the database name."""
        return self._name

    @property
    def created_at(self) -> datetime:
        """Get the timestamp when this database was created."""
        return self._created_at


class EvidentSource:
    """The main entrypoint for connecting to an EvidentSource server.

    EvidentSource manages the gRPC connection and provides methods for:
    - Listing available databases (DatabaseCatalog trait)
    - Creating and deleting databases
    - Connecting to a specific database for operations

    Example:
        ```python
        from evidentsource_client import EvidentSource
        from evidentsource_core import DatabaseName

        # Connect to the server
        es = await EvidentSource.connect("http://localhost:50051")

        # List all databases
        async for name in es.list_databases():
            print(f"Database: {name}")

        # Connect to a specific database
        db_name = DatabaseName("my-db")
        conn = await es.connect_database(db_name)

        # Use the connection for operations
        latest = await conn.latest_database()
        print(f"Latest revision: {latest.revision}")
        ```
    """

    def __init__(self, channel: grpc.aio.Channel) -> None:
        """Create an EvidentSource instance from an existing channel."""
        self._channel = channel
        self._stub = service_grpc.EvidentSourceStub(channel)  # type: ignore[no-untyped-call]

    @classmethod
    async def connect(cls, addr: str) -> EvidentSource:
        """Connect to an EvidentSource server.

        Args:
            addr: The server address (e.g., "localhost:50051" or "api.example.com:443")

        Returns:
            A connected EvidentSource instance

        Example:
            ```python
            es = await EvidentSource.connect("localhost:50051")
            ```
        """
        # Determine if we should use secure channel
        if addr.startswith("https://"):
            addr = addr[8:]  # Remove https://
            channel = grpc.aio.secure_channel(addr, grpc.ssl_channel_credentials())
        elif addr.startswith("http://"):
            addr = addr[7:]  # Remove http://
            channel = grpc.aio.insecure_channel(addr)
        else:
            # Assume insecure for bare addresses
            channel = grpc.aio.insecure_channel(addr)

        return cls(channel)

    @classmethod
    def from_channel(cls, channel: grpc.aio.Channel) -> EvidentSource:
        """Create an EvidentSource instance from an existing gRPC channel."""
        return cls(channel)

    async def list_databases(self) -> AsyncIterator[DatabaseName]:
        """List all databases in the catalog.

        Yields:
            DatabaseName objects for each database

        Example:
            ```python
            async for name in es.list_databases():
                print(f"Found database: {name}")
            ```
        """
        request = proto.CatalogRequest()
        try:
            async for reply in self._stub.FetchCatalog(request):
                try:
                    yield DatabaseName(reply.database_name)
                except Exception:
                    # Skip invalid database names
                    pass
        except grpc.aio.AioRpcError:
            # Return empty on error
            return

    async def create_database(self, name: DatabaseName) -> DatabaseIdentityImpl:
        """Create a new database with the given name.

        Args:
            name: The name of the database to create

        Returns:
            The identity of the created database

        Raises:
            DatabaseAlreadyExists: If a database with this name already exists
            DatabaseServerError: If the server returns an error

        Example:
            ```python
            db_name = DatabaseName("my-new-db")
            identity = await es.create_database(db_name)
            print(f"Created at: {identity.created_at}")
            ```
        """
        request = proto.CreateDatabaseRequest(database_name=str(name))

        try:
            reply = await self._stub.CreateDatabase(request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(name)) from e

        db = reply.database
        db_name = DatabaseName(db.name)
        created_at = timestamp_to_datetime(db.created_at)

        return DatabaseIdentityImpl(_name=db_name, _created_at=created_at)

    async def delete_database(self, name: DatabaseName) -> None:
        """Delete a database by name.

        Args:
            name: The name of the database to delete

        Raises:
            DatabaseNotFound: If no database with this name exists
            DatabaseServerError: If the server returns an error

        Example:
            ```python
            db_name = DatabaseName("old-db")
            await es.delete_database(db_name)
            ```
        """
        request = proto.DeleteDatabaseRequest(database_name=str(name))

        try:
            await self._stub.DeleteDatabase(request)
        except grpc.aio.AioRpcError as e:
            raise _to_database_error(e, str(name)) from e

    async def connect_database(self, name: DatabaseName) -> Connection:
        """Connect to a specific database.

        This returns a Connection that maintains a live subscription to
        database updates and implements DatabaseProvider and DatabaseConnection.

        Args:
            name: The name of the database to connect to

        Returns:
            A Connection instance for the database

        Example:
            ```python
            db_name = DatabaseName("my-db")
            conn = await es.connect_database(db_name)
            ```
        """
        from evidentsource_client.connection import Connection

        return await Connection.connect(self._stub, name)

    async def close(self) -> None:
        """Close the connection to the server."""
        await self._channel.close()

    async def __aenter__(self) -> EvidentSource:
        """Enter async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Exit async context manager."""
        await self.close()


def _to_database_error(e: grpc.aio.AioRpcError, db_name: str) -> DatabaseError:
    """Convert a gRPC error to a DatabaseError."""
    code = e.code()

    if code == grpc.StatusCode.NOT_FOUND:
        return DatabaseNotFound(db_name)
    elif code == grpc.StatusCode.ALREADY_EXISTS:
        return DatabaseAlreadyExists(db_name)
    else:
        return DatabaseServerError(str(e.details()))
