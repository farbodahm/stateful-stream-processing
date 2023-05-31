import asyncio
from time import sleep

from sqlalchemy.ext.asyncio import async_sessionmaker

from async_processor import AsyncProcessor
from config import CliArgsParser, ClientGenerator


def main() -> None:
    """Starting point of processor application"""
    # TODO: Find a good way to wait for the consumer to be ready
    sleep(5)

    cli_args_parser = CliArgsParser()
    cli_args = cli_args_parser.parser.parse_args()

    clients = ClientGenerator(cli_args)
    async_session = async_sessionmaker(clients.db_async_engine, expire_on_commit=False)

    processor = AsyncProcessor(
        async_session=async_session,
        ws_host=cli_args.ws_host,
        ws_port=cli_args.ws_port,
        query_pool_size=cli_args.ws_write_pool_size,
    )
    asyncio.run(processor.run())


if __name__ == "__main__":
    main()
