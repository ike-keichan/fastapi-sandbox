up:
	docker compose up --force-recreate
upd:
	docker compose up -d --force-recreate
stop:
	docker compose stop
ps:
	docker compose ps
build:
	docker compose build
buildn:
	docker compose build --no-cache
down:
	docker compose down --remove-orphans
downv:
	docker compose down -v --remove-orphans
restart:
	docker compose restart
db/console:
	docker compose exec db mysql demo
db/migrate:
	docker compose exec fastapi-sandbox poetry run python -m api.migrate_db
py/install:
	docker compose run --entrypoint "poetry install --no-root" fastapi-sandbox
py/add:
	docker compose exec fastapi-sandbox poetry add $(TARGET)
py/adddev:
	docker compose exec fastapi-sandbox poetry add -G dev $(TARGET)
py/test:
	docker compose run --entrypoint "poetry run pytest" fastapi-sandbox