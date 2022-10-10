.ONESHELL:
.DELETE_ON_ERROR:

SHELL := /bin/bash

.PHONY: activate requirements local integration test poetry run build test

poetry:
	curl -sSL https://install.python-poetry.org | python3 - && \
	export PATH="/Users/$$(USER)/.local/bin:$$(PATH)" && \
	poetry self update

activate:
	@echo "Connecting pyenv & poetry..."
	poetry config virtualenvs.in-project true && \
	poetry env use $$(pyenv which python) && \
	poetry config virtualenvs.prefer-active-python true
	@echo "Done!"

requirements:
	poetry export -f requirements.txt --without-hashes | cut -f1 -d\; > requirements.txt

local:
	export ENV=LOCAL && \
	poetry run uvicorn app.main:app --host localhost --port 8000 --reload

integration:
	export ENV=INTEGRATION && \
	poetry run uvicorn app.main:app --host localhost --reload

test:
	poetry run pytest -rx

build:
	cd ../.. && \
	docker build -f ./goodies/Dockerfile -t goodies .

run: build
	cd ../.. && \
	docker run --env-file ./app/.integration.env --rm -it --name goodies -p 8000:8000 goodies

test:
	poetry run black ./ && \
	poetry run flake8 ./ && \
	poetry run isort ./
