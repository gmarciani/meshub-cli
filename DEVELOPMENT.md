# Development

## Setup

Setup development environment
```shell
pyenv virtualenv 3.12 meshub-dev
pyenv activate meshub-dev
pip install -e .
```

Install development dependencies
```shell
pip install -e ".[dev]"
pre-commit install
```

## Validate
Run tests and linters
```shell
# Run all tests and linting with tox
tox

# Run specific environments
tox -e test        # Tests on Python 3.12
tox -e coverage    # Code coverage report
tox -e lint        # Linting only
tox -e type        # Type checking only
tox -e format      # Format code
```

## Documentation

Generate the CLI reference documentation using Sphinx:

```shell
# Install documentation dependencies
pip install -e ".[docs]"

# Build HTML documentation
cd docs
make html
```

The generated documentation will be in `docs/_build/html/`. Open `docs/_build/html/index.html` in a browser to view.

To clean and rebuild:
```shell
cd docs
make clean html
```

## Release

Update version in `constants.py`
```
VERSION="0.0.2"
```

Draft the release
```
gh release create v${VERSION} \
   --title "v$VERSION" \
   --target main \
   --notes-file CHANGELOG.md \
   --latest \
   --draft
```

Make changes to the release notes, and publish
```
gh release edit v${VERSION} --draft=false
```

This will automatically trigger Test PyPI publishing

### Manual Test PyPI Publishing

To manually publish to Test PyPI

```bash
python -m build
python -m twine upload --repository testpypi dist/*
```
