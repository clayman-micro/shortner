import config  # type: ignore
from aiohttp import web
from aiohttp_metrics import setup as setup_metrics  # type: ignore
from aiohttp_micro import setup as setup_micro  # type: ignore


class AppConfig(config.Config):
    consul = config.NestedField(config.ConsulConfig, key="consul")
    db = config.NestedField(config.PostgresConfig, key="db")
    debug = config.BoolField(default=False)
    sentry_dsn = config.StrField()


async def init(app_name: str, config: AppConfig, logger) -> web.Application:
    app = web.Application()

    setup_micro(app, app_name, config)
    setup_metrics(app, app_name=app_name)

    app["logger"].info("Initialize application")

    return app
