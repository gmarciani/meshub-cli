# Development

## Setup

Setup development environment
```bash
pyenv virtualenv 3.12 meshub-dev
pyenv activate meshub-dev
pip install -e .
```

Install development dependencies
```bash
pip install -r requirements-dev.txt
pre-commit install
```

## Validate
Run tests and linters
```bash
# Run all tests and linting with tox
tox

# Run specific environments
tox -e py312        # Tests on Python 3.12
tox -e lint         # Linting only
tox -e type         # Type checking only
tox -e format       # Format code
tox -e coverage     # Code coverage report
```

## Release

Update version in `constants.py`
```
VERSION="1.0.0"
```

Draft the release
```
gh release create v${VERSION} \
   --title "meshub v$VERSION" \
   --target main \
   --notes-file CHANGELOG.md \
   --latest \
   --draft
```

Make changes to the release notes, and publish
```
gh release edit v${VERSION} --draft false
```

This will automatically trigger Test PyPI publishing

### Manual Test PyPI Publishing

To manually publish to Test PyPI

```bash
python -m build
python -m twine upload --repository testpypi dist/*
```
