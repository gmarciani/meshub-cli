.PHONY: setup install

PYTHON_VERSION = 3.14.2
VENV_NAME = meshub-dev

setup:
	pyenv install $(PYTHON_VERSION) --skip-existing
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME) --force
	pyenv local $(VENV_NAME)
	$$HOME/.pyenv/versions/$(VENV_NAME)/bin/python -m pip install --upgrade pip
	pre-commit install

install:
	pip install -e .

install_docs:
	pip install -e ".[docs]"

build_docs: install_docs
	$(MAKE) -C docs html

clean_docs: install_docs
	$(MAKE) -C docs clean

view_docs:
	open docs/_build/html/index.html
