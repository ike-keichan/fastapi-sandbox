## コンテナ操作系
# コンテナの起動
up:
	docker compose up --force-recreate
# コンテナの起動（バックグランド）
upd:
	docker compose up -d --force-recreate
# コンテナの停止
stop:
	docker compose stop
# コンテナの再起動（停止+起動）
restart:
	docker compose restart
# コンテナのビルド
build:
	docker compose build
# コンテナの削除
down:
	docker compose down --remove-orphans
# コンテナの削除（ボリューム含む）
downv:
	docker compose down -v --remove-orphans
# コンテナの状態確認
ps:
	docker compose ps -a


# TODO:DB関連のコマンドを整理する。シードの追加処理の追加。
## DB操作系
# DBのマイグレーション
db/migrate:
	docker compose exec fastapi-sandbox poetry run python -m api.migrate_db
# DBのリセット
db/reset:
	echo "TODO"


## Poetry操作系
# パッケージインストール
py/install:
	docker compose run --rm --entrypoint "poetry install --no-root" fastapi-sandbox
# パッケージ追加
py/add:
	docker compose exec fastapi-sandbox poetry add $(TARGET)
	docker compose build --no-cache
# パッケージ追加（devDependency）
py/add-d:
	docker compose exec fastapi-sandbox poetry add -G dev $(TARGET)
	docker compose build --no-cache
# コード修正
py/fix: py/fix-lint py/fix-format
# コード修正（リンター）
py/fix-lint:
	docker compose run --rm --entrypoint "poetry run ruff check --fix" fastapi-sandbox
# コード修正（フォーマッタ）
py/fix-format:
	docker compose run --rm --entrypoint "poetry run ruff format" fastapi-sandbox
# コードチェック
py/check: py/check-lint
# コードチェック（リンター）
py/check-lint:
	docker compose run --rm --entrypoint "poetry run ruff check" fastapi-sandbox
# テスト
py/test:
	docker compose run --rm --entrypoint "poetry run pytest" fastapi-sandbox


## コンソール系
# pythonコンテナ
c:
	docker compose exec fastapi-sandbox bash
# pythonコンテナのpython
pyc:
	docker compose exec fastapi-sandbox python
# DBコンテナのmysql
dbc:
	docker compose exec db mysql demo


## その他
# セットアップ
setup:
	docker compose build
	docker compose up -d --force-recreate
	@sleep 7
	docker compose exec fastapi-sandbox poetry run python -m api.migrate_db
	docker compose stop
