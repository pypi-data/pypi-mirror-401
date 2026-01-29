# url2rss (Developer Guide)

`url2rss` is a Python library that converts public web pages (HTML pages, search results, and JavaScript-rendered pages) into RSS XML feeds.

This document is intended for **developers and maintainers** of the project and focuses on:
- Project structure
- Development workflow
- Version management
- Environment consistency (dev & prod)

---

## Project Overview

The core goal of `url2rss` is to provide a **single, stable API** for generating RSS feeds from arbitrary URLs, regardless of whether the source page is:
- Static HTML
- A search or listing page
- JavaScript-rendered content

The public API is intentionally small to keep usage simple and maintenance predictable.

---

## Development Setup

### Requirements
- Python 3.10+
- pip
- Playwright (optional, for JS-rendered pages)

```sh
pip install -r requirements.txt
playwright install
```

## Core API
```py
from url2rss import url_to_rss

rss_xml = url_to_rss("<any-public-url>")
```
The function returns a valid RSS XML string.

---

## Version Management (IMPORTANT)

### Manual Versioning Strategy
This project uses manual versioning, defined explicitly in ```pyproject.toml```.

```py
[project]
version = "0.0.1"
```

There is <b>no automatic version bumping</b> in CI/CD.

### When to update the version

You <b>must increment the version manuall</b>y in ```pyproject.toml``` when:

- Publishing a new release to TestPyPI (dev)
- Publishing a new release to PyPI (prod)

Failing to do so will result in <b>upload failures</b>, as PyPI does not allow reusing the same version number.

### Recommended version increments

Use simple incremental versions:

> 0.0.1 → 0.0.2 → 0.0.3

The same version number is used for both environments.

---

## Environment Discipline (Dev vs Prod)

This project maintains <b>two deployment environments</b>:

| Branch      | Environment | Registry                                           |
| --------    | --------    | --------                                           |
| ```dev```   | Development | [TestPyPI](https://test.pypi.org/project/url2rss/) |
| ```main```  | Production  | [PyPI](https://pypi.org/project/url2rss/)          |

### Rules to follow

1. <b>Always update the version before pushing</b>
2. <b>Push the same version to ```dev``` first</b>
3. Validate behavior from TestPyPI
4. Merge ```dev``` → ```main```
5. Publish the same version to PyPI

This ensures:
- No version drift
- No environment mismatch
- Predictable releases

---

## CI/CD Behavior

- Pushing to ```main``` publishes the package to TestPyPI
- Pushing to main publishes the package to PyPI
- CI does not modify the repository
- CI reads the version directly from ```pyproject.toml```

Version correctness is the responsibility of the developer.

---

## Repository Structure (Simplified)
```bash
.
├── src/url2rss/        # Library source code
├── pyproject.toml      # Project metadata & version
├── README.md           # Developer documentation (this file)
├── PYPI.md             # Usage documentation for PyPI
└── .github/workflows/  # CI/CD workflows
```

---

