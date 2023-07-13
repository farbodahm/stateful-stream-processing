import json
from typing import Dict, Any, List

import asyncio
from websockets.legacy.server import WebSocketServerProtocol
import websockets
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from sqlalchemy import TextClause
from sqlalchemy.engine.row import Row


from utility.logger import logger


class AsyncProcessor:
    """AsyncProcessor class is an async class with ProducerConsumer pattern which:
    1. Producers run the given queries on DB and add the results to the queue [async].
    2. Consumers consume the results from the queue and send them to the websocket [async].
    TODO: Refactor this class to 2 classes: AsyncProducer and AsyncConsumer.
    """

    def __init__(
        self,
        async_session: async_sessionmaker[AsyncSession],
        query_pool_size: int = 10,
        ws_host: str = "localhost",
        ws_port: int = 8765,
    ) -> None:
        self.ws_host = ws_host
        self.ws_port = int(ws_port)
        self._async_session = async_session

        logger.info(f"Query pool size: {query_pool_size}")
        # Queue which holds the results of the queries
        self._queue = asyncio.Queue(query_pool_size)

    async def start_websocket_server(self) -> None:
        """Start the WebSocket and wait for connection"""
        async with websockets.serve(self.ws_handler, self.ws_host, self.ws_port):
            logger.info(f"WebSocket server started at {self.ws_host}:{self.ws_port}")
            await asyncio.Future()  # run forever

    async def ws_handler(self, ws: WebSocketServerProtocol) -> None:
        """Handler function gets called after WS connected.
        It reads from query results queue and write in on started WS."""
        logger.info("WebSocket connected")
        while True:
            await ws.send(await self._queue.get())
            await asyncio.sleep(1)

    async def add_to_ws_queue(self, item: Dict[str, Any]) -> None:
        """Add the given itam to queue of items that will be write on WS."""
        await self._queue.put(json.dumps(item, default=str))

    async def process_query(
        self, query: TextClause, async_session: async_sessionmaker[AsyncSession]
    ) -> None:
        """Run the given query and add the results to the processing queue."""
        async with async_session() as session:
            while True:
                try:
                    rows: List[Row] = await session.execute(query)
                except Exception as e:
                    logger.error(f"Error running query {query.text}: {e}")
                    result = {
                        "status": "ERROR",
                        "message": f"Error running query {query.text}: {e}",
                    }
                    await self.add_to_ws_queue(result)
                    await asyncio.sleep(1)
                else:
                    logger.info(f"Query {query.text} executed successfully.")
                    for row in rows:
                        result = row._asdict()
                        result["status"] = "OK"
                        result["query"] = query.text
                        await self.add_to_ws_queue(result)
                        await asyncio.sleep(1)
                await asyncio.sleep(5)

    def get_queries(self) -> List[str]:
        """Return queries which should be run on DB and write back result to WS.
        TODO: Think about logic of this function on how to retrieve queries.
        """
        return [
            """SELECT u.first_name, u.last_name, u.id, u.gender, COUNT(t.id) as tweet_count
FROM "user" u
INNER JOIN tweet t ON u.id = t.user_id
GROUP BY u.id, u.first_name, u.last_name, u.gender
ORDER BY tweet_count DESC
LIMIT 10;""",
            """SELECT t.id, t.text, COUNT(l.tweet_id) as like_count
FROM tweet t
INNER JOIN tweet_like l ON t.id = l.tweet_id
GROUP BY t.id, t.text
ORDER BY like_count DESC
LIMIT 10;""",
        ]

    async def run(self) -> None:
        """Entry point for processor class. This will run the given queries periodically
        on database and write results to WebSocket"""
        logger.info("Started processor application")
        queries = self.get_queries()
        logger.info(f"Queries to run: {queries}")
        queries = [text(query) for query in queries]

        ws_writer_task = asyncio.create_task(self.start_websocket_server())
        query_tasks = [
            asyncio.create_task(self.process_query(query, self._async_session))
            for query in queries
        ]

        await asyncio.gather(ws_writer_task, *query_tasks)
