from aiohttp import web
from aiohttp_metrics import setup as setup_metrics  # type: ignore
from aiohttp_micro import AppConfig, setup as setup_micro


async def init(app_name: str, config: AppConfig) -> web.Application:
    app = web.Application()

    setup_micro(app, app_name=app_name, config=config)
    setup_metrics(app)

    return app
