import faker  # type: ignore
import pytest  # type: ignore
from aiohttp import web

from shortner.app import AppConfig, init


@pytest.fixture(scope="session")
def fake():
    return faker.Faker()


@pytest.fixture(scope="session")
def config():
    return AppConfig()


@pytest.yield_fixture(scope="function")
def app(loop, config):
    app = loop.run_until_complete(init("shortner", config))
    runner = web.AppRunner(app)

    loop.run_until_complete(runner.setup())

    yield app

    loop.run_until_complete(runner.cleanup())
