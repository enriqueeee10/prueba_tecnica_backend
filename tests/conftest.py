import asyncio
import pytest_asyncio
from httpx import AsyncClient
from app.main import app


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Cliente HTTP asíncrono para pruebas
@pytest_asyncio.fixture
async def test_client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
