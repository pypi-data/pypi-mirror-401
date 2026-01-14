# tuto-python-setup-package

<p align="center">
  <a href="https://github.com/JarryGabriel/tuto-python-setup-package/actions/workflows/ci.yml"><img src="https://github.com/JarryGabriel/tuto-python-setup-package/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://coveralls.io/github/JarryGabriel/tuto-python-setup-package?branch=main"><img src="https://coveralls.io/repos/github/JarryGabriel/tuto-python-setup-package/badge.svg?branch=main" alt="Coverage"></a>
  <a href="https://pypi.org/project/tuto-python-setup-package/"><img src="https://img.shields.io/pypi/v/tuto-python-setup-package" alt="PyPI"></a>
  <img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/typed-strict-blue" alt="Typed">
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv"></a>
  <a href="https://JarryGabriel.github.io/tuto-python-setup-package/"><img src="https://img.shields.io/badge/docs-live-brightgreen" alt="Docs"></a>
</p>

> Tutorial package for Python setup workflow

## Installation

```bash
uv add tuto-python-setup-package
```

## Quick Start

```python
from tuto_python_setup_package import hello

print(hello())
```

## Development

```bash
git clone https://github.com/JarryGabriel/tuto-python-setup-package.git
cd tuto-python-setup-package
make install
make check
```

## License

MIT - See [LICENSE](LICENSE) for details.
