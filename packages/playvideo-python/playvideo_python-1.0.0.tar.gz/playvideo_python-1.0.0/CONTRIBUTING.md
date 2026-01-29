# Contributing to PlayVideo Python SDK

Thank you for your interest in contributing to the PlayVideo Python SDK!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/PlayVideo-dev/playvideo-python.git
   cd playvideo-python
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_client.py

# Run with coverage
pytest --cov=playvideo

# Type check
mypy playvideo

# Lint
ruff check playvideo tests

# Format check
ruff format --check playvideo tests
```

## Project Structure

```
playvideo/
├── __init__.py        # Main exports
├── client.py          # Sync PlayVideo client
├── async_client.py    # Async PlayVideo client
├── resources/         # API resource implementations
│   ├── collections.py
│   ├── videos.py
│   ├── webhooks.py
│   ├── embed.py
│   ├── api_keys.py
│   ├── account.py
│   └── usage.py
├── errors.py          # Exception classes
├── types.py           # Type definitions
└── webhook.py         # Webhook signature verification

tests/
├── test_client.py
├── test_async_client.py
└── test_webhook.py
```

## Making Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest`
6. Ensure type check passes: `mypy playvideo`
7. Ensure lint passes: `ruff check playvideo tests`
8. Format code: `ruff format playvideo tests`
9. Commit your changes: `git commit -m "Add my feature"`
10. Push to your fork: `git push origin feature/my-feature`
11. Open a Pull Request

## Code Style

- We use `ruff` for linting and formatting
- We use `mypy` for type checking with strict mode
- Follow PEP 8 conventions
- Add type hints to all public functions
- Add docstrings to public APIs

## Pull Request Guidelines

- Include a clear description of the changes
- Reference any related issues
- Add tests for new functionality
- Update documentation if needed
- Keep PRs focused on a single change

## Reporting Issues

When reporting issues, please include:

- SDK version
- Python version
- Operating system
- Minimal code to reproduce the issue
- Expected vs actual behavior

## Questions?

If you have questions, feel free to open an issue or reach out at support@playvideo.dev.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
