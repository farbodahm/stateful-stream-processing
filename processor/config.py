import argparse

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine


class ClientGenerator:
    """Class for generating required objects based on given CLI configs."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.db_async_engine = self._get_db_async_engine(
            ip=args.database_ip,
            port=args.database_port,
            username=args.database_username,
            password=args.database_password,
            db_name=args.database_name,
        )

    def _get_db_async_engine(
        self, ip: str, port: str, username: str, password: str, db_name: str
    ) -> AsyncEngine:
        """Create and return Async SQLAlchemy Engine object."""
        db_url = f"postgresql+asyncpg://{username}:{password}@{ip}:{port}/{db_name}"
        engine = create_async_engine(db_url, echo=True)

        return engine


class CliArgsParser:
    """Class for generating required ArgParse arguments"""

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description=(
                "Service for generating expected queries and send them to consumers."
                "For Dev env, processor engine is PostgreSQL and consumer is a WebSocket."
            )
        )

        self._add_arguments()

    def _add_arguments(self) -> None:
        """Add arguments that parser needs to parse."""
        self.parser.add_argument(
            "--db-ip",
            dest="database_ip",
            default="localhost",
            help="Databse IP",
        )
        self.parser.add_argument(
            "--db-port",
            dest="database_port",
            default="5432",
            help="Databse Port",
        )
        self.parser.add_argument(
            "--db-user",
            dest="database_username",
            default="postgres",
            help="Databse Username",
        )
        self.parser.add_argument(
            "--db-password",
            dest="database_password",
            default="postgres",
            help="Databse Password",
        )
        self.parser.add_argument(
            "--db-name",
            dest="database_name",
            default="twitter",
            help="Databse Name",
        )
        self.parser.add_argument(
            "--ws-host",
            dest="ws_host",
            default="localhost",
            help="WebSocket host to listen on",
        )
        self.parser.add_argument(
            "--ws-port",
            dest="ws_port",
            default="8765",
            help="WebSocket port to listen on",
        )
        self.parser.add_argument(
            "--ws-write-pool-size",
            dest="ws_write_pool_size",
            default=10,
            type=int,
            help=(
                "Pool buffer for writing queries on WebSocket. If pool size reached that limit,"
                "no new queries will run until buffer gets written."
            ),
        )
