import asyncio

import click
import structlog  # type: ignore
import uvloop  # type: ignore

from shortner.app import AppConfig, init
from shortner.management.server import server


structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)


@click.group()
@click.option("--debug", default=False)
@click.pass_context
def cli(ctx, debug):
    uvloop.install()
    loop = asyncio.get_event_loop()

    logger = structlog.get_logger()

    config = AppConfig()
    config.load_from_env()

    config.debug = debug

    app = loop.run_until_complete(init("shortner", config, logger))

    ctx.obj["app"] = app
    ctx.obj["config"] = config
    ctx.obj["loop"] = loop


cli.add_command(server, name="server")


if __name__ == "__main__":
    cli(obj={})
