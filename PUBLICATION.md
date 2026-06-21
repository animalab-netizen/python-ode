# Publication Guide

## Current State

`python-ode` is structured as a standalone Python package.

Current coordinates:

- package: `python-ode`
- version: `0.1.1`
- repository: [github.com/animalab-netizen/python-ode](https://github.com/animalab-netizen/python-ode)

## Trusted Publishing

`python-ode` is prepared for PyPI Trusted Publishing from GitHub Actions.

Repository-side workflow:

- workflow file: `.github/workflows/release.yml`
- provider model: GitHub Actions OIDC
- publish trigger: push tag `v*`
- GitHub Actions environment: `pypi`
- required workflow permission: `id-token: write`
- publication action: `pypa/gh-action-pypi-publish@release/v1`

PyPI still needs the matching Trusted Publisher entry created in the package owner account. No API token should be stored in GitHub Secrets for this flow.

## Distribution Model

The package is intended for:

- direct PyPI distribution as the public Python ODE runtime
- consumption by community showcases such as `python-ode-consumer`
- installation without any private company-specific domain once public publication is enabled

## Installation

```bash
pip install python-ode
```

## Release Checklist

### GitHub Release Gate

1. Run `python3 -m unittest discover /Users/caiosanchezchristino/Desktop/ode-projects/python-ode/tests`
2. Run `python3 setup.py sdist --dist-dir /tmp/python-ode-dist`
3. Confirm CI is green in `.github/workflows/ci.yml`
4. Update `CHANGELOG.md`
5. Confirm version in `pyproject.toml`
6. Commit release metadata
7. Create and push tag `v0.1.1`

### Public Package Gate

1. Confirm the package name remains `python-ode`
2. In PyPI, create or verify the Trusted Publisher entry for the intended repository workflow
3. Confirm the GitHub workflow file is `.github/workflows/release.yml`
4. Confirm the workflow job has `id-token: write`
5. Push tag `v0.1.1`
6. Verify the package page on PyPI
7. Validate installation from a clean consumer with `pip install python-ode==0.1.1`
8. Publish release notes with install and usage examples

## Packaging Notes

- the package ships from `src/python_ode`
- the runtime has no third-party production dependencies
- package metadata is embedded in `pyproject.toml`
- `setup.cfg` and `setup.py` remain present as compatibility fallbacks for conservative Python environments
