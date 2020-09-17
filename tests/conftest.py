from unittest import mock

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


@pytest.fixture(scope="function")
def logger():
    logger = mock.Mock()
    logger.info = mock.Mock()
    return logger


@pytest.yield_fixture(scope="function")
async def app(config, logger):
    app = init("shortner", config, logger)
    runner = web.AppRunner(app)

    await runner.setup()

    yield app

    await runner.cleanup()
