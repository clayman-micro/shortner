import asyncio

import click
import uvloop  # type: ignore
from aiohttp_micro.management.server import server
from config import ConsulConfig, EnvValueProvider, load

from shortner.app import AppConfig, init


structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)


@click.group()
@click.option("--debug", is_flag=True, default=False)
@click.pass_context
def cli(ctx, debug: bool = False) -> None:
    uvloop.install()
    loop = asyncio.get_event_loop()

    consul_config = ConsulConfig()
    load(consul_config, providers=[EnvValueProvider()])

    config = AppConfig(defaults={"consul": consul_config, "debug": debug})
    load(config, providers=[EnvValueProvider()])

    app = loop.run_until_complete(init("shortner", config))

    ctx.obj["app"] = app
    ctx.obj["config"] = config
    ctx.obj["loop"] = loop


cli.add_command(server, name="server")


if __name__ == "__main__":
    cli(obj={})
