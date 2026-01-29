"""EvidentSource Python Client.

This package provides a Python client for the EvidentSource event sourcing database.

Example:
    ```python
    import asyncio
    from evidentsource_client import EvidentSource
    from evidentsource_core import DatabaseName, Selector, ProspectiveEvent, StringEventData

    async def main():
        # Connect to the server
        async with await EvidentSource.connect("localhost:50051") as es:
            # Create a database
            db_name = DatabaseName("my-app")
            await es.create_database(db_name)

            # Connect to the database
            conn = await es.connect_database(db_name)

            # Transact events
            events = [
                ProspectiveEvent(
                    id="evt-1",
                    stream="orders",
                    event_type="OrderCreated",
                    data=StringEventData('{"orderId": "123"}'),
                )
            ]
            db = await conn.transact(events)
            print(f"Committed at revision: {db.revision}")

            # Query events
            db = await conn.latest_database()
            async for event in db.query_events(Selector.stream("orders")):
                print(f"Event: {event.id} - {event.event_type}")

    asyncio.run(main())
    ```
"""

from evidentsource_client.connection import Connection
from evidentsource_client.database import (
    DatabaseAtRevisionAndEffectiveTimestampImpl,
    DatabaseAtRevisionImpl,
    SpeculativeDatabaseImpl,
)
from evidentsource_client.evident_source import (
    DatabaseIdentityImpl,
    EvidentSource,
)

__version__ = "0.8.0"

__all__ = [
    # Main entrypoint
    "EvidentSource",
    # Connection
    "Connection",
    # Database views
    "DatabaseAtRevisionImpl",
    "DatabaseAtRevisionAndEffectiveTimestampImpl",
    "SpeculativeDatabaseImpl",
    # Identity
    "DatabaseIdentityImpl",
]
