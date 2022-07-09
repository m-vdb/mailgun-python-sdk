.PHONY: install test-install


install:
	poetry install --no-dev

test-install: install
	poetry install

analysis:
	poetry run flake8 --ignore=E123,E126,E128,E501,W391,W291,W293,F401 tests
	poetry run flake8 --ignore=E402,F401,W391,W291,W293 mailgun --max-line-length=300

test: analysis
	poetry run pytest
