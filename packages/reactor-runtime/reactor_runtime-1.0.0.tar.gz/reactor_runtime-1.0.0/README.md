# Reactor Runtime

A Python runtime for building real-time video processing models. This runtime abstracts all the techincal implementations of real-time networking, allowing
researchers and models developers to run their model focusing only on the ML code.

You can think of this similarly to the way you write Telegram/Discord applications or bots using SDKs. You don't have to worry about the networking and the protocols of the medium. Instead, you can put all your effort in writing your application code, which in this case is ML code.

Documentation: https://docs.reactor.inc/runtime/overview

## Installation

```bash
pip install reactor-runtime
```

## Development Setup

Proto dependencies are fetched from the private `reactor-team/reactor-proto` repo. The version is defined in `pyproject.toml` under `[tool.reactor-proto]`.

```bash
# Set your GitHub token (required for private repo access)
export GH_TOKEN=your_github_token

# Install with proto dependencies
make install

# Or fetch protos separately
make proto
```

The proto wheel is downloaded to `generated/` (gitignored). Once installed, proto types are available via:

```python
from api import reactor_pb2
from api.types import api_types_pb2, base_pb2
```

## Publishing

```bash
make publish
```

The publish script performs two key transformations before building:

### 1. Obfuscation

All files and directories prefixed with `_` are stripped from the published package (except `__init__.py` and `__pycache__`). This allows you to keep private/internal code in the repository that won't be shipped to users.

Example: A `_cloud/` directory or `_internal.py` file will exist in the repo for development but won't appear in the PyPI package.

### 2. Proto Vendoring

The script uses AST analysis to scan all remaining (public) source files and identifies which `api.*` modules are actually imported. Only those specific proto files are copied into the published package.

This means:

- Users don't need access to the private `reactor-proto` repo
- The published package is self-contained with proto types bundled
- Only the protos actually used by public code are included, keeping the package minimal

**Prerequisite**: Run `make proto` before publishing to ensure proto types are installed locally for vendoring.

## Reactor CLI

Docs: https://docs.reactor.inc/runtime/cli-reference

## Coding Models

Guide: https://docs.reactor.inc/runtime/coding-models
