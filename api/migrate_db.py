from sqlalchemy import create_engine

from api.models.task.index import Base

# 接続するデータベースのURL。
# DBはMySQL、ORMにpymysqlを使用。DB名は'demo'。
DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"

# DB接続用のエンジン
engine = create_engine(DB_URL, echo=True)


def reset_database():
    """
    DBをリセットする関数。
    現在のDBの全テーブルを削除し、再度作成する。
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
