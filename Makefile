.PHONY: install run test lint docker
install:
	pip install -e ".[dev]"
run:
	uvicorn app.main:app --reload
test:
	pytest
lint:
	ruff check .
docker:
	docker compose up --build
