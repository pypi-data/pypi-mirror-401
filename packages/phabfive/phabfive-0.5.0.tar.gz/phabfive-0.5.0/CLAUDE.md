# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Commands

### Testing
- **Run all tests**: `uv run tox --skip-missing-interpreters`
- **Run tests for specific Python version**: `uv run tox -e py310`
- **Run linting only**: `uv run tox -e flake8`
- **Run coverage**: `uv run tox -e coverage`
- **Build documentation**: `uv run tox -e mkdocs`

### Development Environment
- **Create virtual environment**: `uv venv`
- **Install dependencies**: `uv pip install -e .[test]`
- **Clean build artifacts**: `make cleanall`
- **Clean tox environments**: `make cleantox`

### Building and Installation
- **Install locally**: `python setup.py install`
- **Build source distribution**: `make sdist`
- **Build wheel**: `make bdist`

## Architecture Overview

phabfive is a CLI tool for interacting with Phabricator. The codebase follows a modular inheritance pattern:

### Core Infrastructure
- **phabfive/core.py**: Base `Phabfive` class providing configuration management, API client setup, and common utilities
- **phabfive/constants.py**: Application constants, monogram patterns, validation rules
- **phabfive/exceptions.py**: Custom exception hierarchy (`PhabfiveException`, `PhabfiveDataException`, etc.)
- **phabfive/cli.py**: CLI entry point with docopt-based argument parsing and monogram shortcut support

### Application Modules
All inherit from `core.Phabfive` and implement specific Phabricator functionality:
- **passphrase.py**: Secret retrieval
- **diffusion.py**: Repository management
- **paste.py**: Text paste operations
- **user.py**: User information
- **maniphest.py**: Task management (most complex - search, create, comment, column operations)
- **repl.py**: Interactive REPL interface

### Configuration System
Hierarchical configuration loading with precedence:
1. Hard-coded defaults
2. `/etc/phabfive.yaml`
3. `/etc/phabfive.d/*.yaml`
4. `~/.config/phabfive.yaml`
5. `~/.config/phabfive.d/*.yaml`
6. Environment variables (highest precedence)

Required: `PHAB_TOKEN` (32-char API token) and `PHAB_URL` (API endpoint ending in `/api/`)

### CLI Design Patterns
- Two-stage parsing: base arguments first, then subcommand-specific arguments
- Monogram shortcut support (e.g., `phabfive T123` → `phabfive maniphest show T123`)
- Consistent help and error handling across all commands
- Uses docopt for declarative argument parsing

### Development Patterns
- All API modules inherit from `core.Phabfive` for consistent configuration and API access
- Transaction-based API updates using `to_transactions()` helper
- Custom exception hierarchy for structured error handling
- Input validation for configuration and API parameters
- Uses the `phabricator` Python library for API communication

### Testing Structure
- Minimal test coverage currently (basic constant and module import tests)
- pytest as test runner with tox orchestration
- Supports Python 3.9, 3.10, 3.11
- Flake8 linting with multiple plugins
- Coverage reporting with 1% minimum threshold

### Recent Development Focus
Based on git history, recent work includes:
- Enhanced Maniphest search functionality (search by column, project columns)
- Improved error handling and user experience
- REPL enhancements
- Monogram shortcut system

## Local Development Setup

For testing with a local Phabricator instance:
1. Add `127.0.0.1 phabricator.domain.tld` to `/etc/hosts`
2. Start MySQL: `docker compose -f docker-compose-phabricator.yml up mysql`
3. Start Phabricator: `docker compose -f docker-compose-phabricator.yml up phabricator`
4. Access at `http://phabricator.domain.tld/` and create API token

## Version Management
- Follows SemVer with PEP 440 extensions
- Version defined in `phabfive/__init__.py` as `__version__`
- Release instructions follow Python packaging documentation
- PyPI uploads require owner/maintainer permissions