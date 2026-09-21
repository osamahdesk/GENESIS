# PyPI Release Guide

The distribution name is `genesis-agi`. The Python import remains `genesis`, and the CLI remains `genesis`.

## Build locally

```bash
python3 -m venv .release-venv
source .release-venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
python -m pytest
rm -rf dist build *.egg-info
python -m build
python -m twine check dist/*
```

## TestPyPI

Create a PyPI API token with the smallest appropriate scope. Do not commit it or paste it into source files. Export it only in the publishing shell:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD='pypi-...'
python -m twine upload --repository testpypi dist/*
```

Test installation in a fresh environment:

```bash
python3 -m venv /tmp/genesis-agi-test
source /tmp/genesis-agi-test/bin/activate
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple genesis-agi==0.1.0
genesis --version
genesis run
```

## Production PyPI

After TestPyPI succeeds, upload the exact same artifacts to the production index:

```bash
python -m twine upload dist/*
```

The first production upload is public and the version cannot be overwritten. Confirm the package name, version, README, license, and artifact contents before running this command.

## Optional trusted publishing

A GitHub Actions workflow can publish through PyPI Trusted Publishing without storing a long-lived API token. Configure the PyPI publisher for the `osamahdesk/GENESIS` repository and the `main` branch, then use a release tag workflow.
