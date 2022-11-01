ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

APPLICATION_NAME = bank

env:
	echo "DB_CONTAINER_NAME=bank_postgres" > .env
	echo "POSTGRES_DB=postgres" >> .env
	echo "POSTGRES_USER=user" >> .env
	echo "POSTGRES_PASSWORD=hackme" >> .env
	echo "POSTGRES_HOST=localhost" >> .env
	echo "POSTGRES_PORT=5432" >> .env

db:
	docker-compose up -d

init:
	make env && make db

open_db:
	docker exec -it $(DB_CONTAINER_NAME) psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

lint:
	poetry run python -m pylint $(APPLICATION_NAME)

test:
	poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG

run:
	#sanic $(APPLICATION_NAME).server:app
	python $(APPLICATION_NAME)/server.py

revision:
	cd $(APPLICATION_NAME)/db && alembic revision --autogenerate

migrate:
	cd $(APPLICATION_NAME)/db && alembic upgrade head
