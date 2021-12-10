.PHONY: venv install test-install

venv:
	@python --version || (echo "Python is not installed, Python 3.6+"; exit 1);
	virtualenv --python=python venv

install: venv
	. venv/bin/activate; pip install .

test-install: install
	. venv/bin/activate; pip install -r tests/requirements.txt