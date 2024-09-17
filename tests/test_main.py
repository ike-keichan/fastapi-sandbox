import pytest
import pytest_asyncio
import starlette.status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.db import Base, get_db
from api.main import app

# 接続するデータベースのURL。
# DBはSQLite、ORMにaiomysqlを使用。
ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"

# TODO: 仮で記入、ふぁいる分割したい。

@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # DB接続用の非同期エンジン
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)

    # 非同期セッション
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # テスト用にDBをリセット
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # テスト用に非同期にデータベースセッションを応答
    async def get_test_db():
        async with async_session() as session:
            yield session

    # テスト用にDBの向き先を変更
    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを応答
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_and_read(async_client):
    response = await async_client.post("/tasks", json={"title": "テストタスク"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク"

    response = await async_client.get("/tasks")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "テストタスク"
    assert response_obj[0]["is_done"] is False


@pytest.mark.asyncio
async def test_done_flag(async_client):
    response = await async_client.post("/tasks", json={"title": "テストタスク2"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク2"

    # 完了フラグを立てる
    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク2"
    assert response_obj["is_done"] is True

    # 完了フラグを外す
    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク2"
    assert response_obj["is_done"] is False


@pytest.mark.asyncio
async def test_due_date(async_client):
    response = await async_client.post(
        "/tasks", json={"title": "テストタスク", "due_date": "2024-09-01"}
    )
    assert response.status_code == starlette.status.HTTP_200_OK
