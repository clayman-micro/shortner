import click
import structlog  # type: ignore
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

    consul_config = ConsulConfig()
    load(consul_config, providers=[EnvValueProvider()])

    config = AppConfig(defaults={"consul": consul_config, "debug": debug})
    load(config, providers=[EnvValueProvider()])

    app = init("shortner", config)

    ctx.obj["app"] = app
    ctx.obj["config"] = config


cli.add_command(server, name="server")


if __name__ == "__main__":
    cli(obj={})
