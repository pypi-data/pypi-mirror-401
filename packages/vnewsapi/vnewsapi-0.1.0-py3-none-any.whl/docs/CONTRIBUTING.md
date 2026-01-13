# Contributing to vnewsapi

Thank you for your interest in contributing to vnewsapi! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/vnewsapi.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt -r requirements-dev.txt`
6. Install the package in development mode: `pip install -e .`

## Development Workflow

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write or update tests
4. Run tests: `pytest`
5. Check code style: `black .` and `flake8 .`
6. Commit your changes: `git commit -m "Add feature: your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Code Style

- Follow PEP 8 style guide
- Use `black` for code formatting: `black .`
- Use type hints where possible
- Write docstrings for all public functions and classes
- Keep line length under 100 characters

## Testing

- Write tests for all new features
- Run tests: `pytest`
- Run with coverage: `pytest --cov=vnewsapi`
- Aim for at least 70% test coverage

## Adding New News Sources

To add a new news source:

1. Add configuration to `vnewsapi/config/sites.py`
2. Update `SUPPORTED_SITES` list
3. Add tests in `tests/unit/test_crawler.py`
4. Update documentation

## Documentation

- Update README.md if adding new features
- Add examples to `docs/examples/`
- Update CHANGELOG.md for user-facing changes

## Pull Request Guidelines

- Provide a clear description of changes
- Reference any related issues
- Ensure all tests pass
- Update documentation as needed
- Keep PRs focused on a single feature or fix

## Questions?

Open an issue on GitHub for any questions or discussions.

Thank you for contributing!

