# Contributing to dbbasic-content

Thanks for considering contributing to dbbasic-content!

## Philosophy

This project is built on Unix foundations. Before contributing, please read:
- [Unix Foundation for Web Development](https://quellhorst.com/unix-foundation-web-dev/)

Core principles:
- **Simple over complex** - Reject unnecessary complexity
- **Files over databases** - Use filesystem primitives
- **Unix tools** - Compose with existing tools
- **No magic** - Code should be obvious

## Development Setup

```bash
# Clone the repository
git clone https://github.com/askrobots/dbbasic-content.git
cd dbbasic-content

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=dbbasic_content --cov-report=html
```

## Making Changes

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/my-feature`
3. **Make your changes**
4. **Write tests** - All new code needs tests
5. **Run tests**: `pytest`
6. **Commit**: Use clear commit messages
7. **Push** and create a Pull Request

## Code Style

- Follow PEP 8
- Use type hints where helpful
- Write docstrings for public APIs
- Keep functions small and focused
- Prefer clarity over cleverness

## Testing

- Write unit tests for all new features
- Ensure all tests pass: `pytest`
- Maintain or improve coverage
- Test edge cases

## Documentation

- Update README.md if needed
- Add examples for new features
- Document breaking changes
- Keep QUICKSTART.md up to date

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG if significant
5. Reference any related issues

## Questions?

Open an issue! We're here to help.

## License

By contributing, you agree your contributions will be licensed under the MIT License.
