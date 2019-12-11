import socket

import pkg_resources
import sentry_sdk
from aiohttp import web
from aiohttp_metrics import setup as setup_metrics  # type: ignore
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from shortner import config
from shortner.handlers import meta
from shortner.middlewares import catch_exceptions_middleware


class AppConfig(config.Config):
    consul = config.NestedField(config.ConsulConfig, key="consul")
    db = config.NestedField(config.PostgresConfig, key="db")
    debug = config.BoolField(default=False)
    sentry_dsn = config.StrField()


async def init(app_name: str, config: AppConfig) -> web.Application:
    app = web.Application()

    app["config"] = config
    app["distribution"] = pkg_resources.get_distribution(app_name)
    app["hostname"] = socket.gethostname()

    if "config" in app and app["config"].sentry_dsn:
        sentry_sdk.init(
            dsn=app["config"].sentry_dsn, integrations=[AioHttpIntegration()]
        )

    setup_metrics(app, app_name=app_name)

    app.middlewares.append(catch_exceptions_middleware)  # type: ignore

    app.router.add_routes(
        [
            web.get("/-/health", meta.health, name="health"),
            web.get("/-/meta", meta.index, name="index"),
        ]
    )

    return app
