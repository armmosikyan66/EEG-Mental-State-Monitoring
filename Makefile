.PHONY: venv check-deps update-deps install-deps isort black start

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

VENV=venv
PYTHON=$(VENV)/bin/python3

cmd-exists-%:
	@hash $(*) > /dev/null 2>&1 || \
		(echo "ERROR: '$(*)' must be installed and available on your PATH."; exit 1)

venv: requirements.txt Makefile
	python3 -m pip install --upgrade pip setuptools wheel
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -r requirements.txt

install-deps:
	$(PYTHON) -m pip install -r requirements.txt

update-deps:
	$(PYTHON) -m pip freeze \
 		sed 's/==.*$/''/' > requirements.txt

start:
	uvicorn main:app --reload --log-level debug --host localhost --port ${PORT}

.PHONY: format

format:
	black .
	isort .