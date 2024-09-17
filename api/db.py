from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 接続するデータベースのURL。
# DBはMySQL、ORMにaiomysqlを使用。データベース名は'demo'。
ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/demo?charset=utf8"

# DB接続用の非同期エンジン
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)

# 非同期セッション
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    """
    非同期にデータベースセッションを応答する関数。
    """
    async with async_session() as session:
        yield session
