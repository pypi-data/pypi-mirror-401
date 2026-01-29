# Contributing to FastMCP Feedback

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Git

### Getting Started

```bash
# 1. Fork the repository on git.supported.systems
# 2. Clone your fork
git clone git@git.supported.systems:YOUR_USERNAME/fastmcp-feedback.git
cd fastmcp-feedback

# 3. Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"

# 4. Verify setup
uv run pytest
```

### Development Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes...

# Run tests
uv run pytest

# Run linting
uv run ruff check .
uv run ruff format .

# Run type checking (optional but appreciated)
uv run mypy src/fastmcp_feedback

# Commit with clear message
git commit -m "feat: Add support for custom validators"

# Push and create PR
git push origin feature/your-feature-name
```

## Code Style

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Style Guidelines

- **Line length**: 88 characters (Black default)
- **Imports**: Sorted with isort (via Ruff)
- **Type hints**: Required for public APIs
- **Docstrings**: Google style for public functions

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/unit/test_tools.py

# Run specific test
uv run pytest -k "test_submit_feedback"

# Run only unit tests
uv run pytest -m unit

# Run only integration tests
uv run pytest -m integration
```

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use descriptive test names: `test_submit_feedback_with_invalid_type_raises_error`
- Use fixtures from `tests/conftest.py`

Example test:

```python
import pytest
from fastmcp_feedback import add_feedback_tools

@pytest.mark.unit
async def test_submit_feedback_creates_record(app_with_feedback, db_session):
    """Submitting feedback should create a database record."""
    result = await app_with_feedback.call_tool(
        "submit_feedback",
        type="bug_report",
        title="Test Bug",
        description="Description"
    )

    assert result["status"] == "success"
    assert result["id"] is not None
```

## Pull Request Guidelines

### Before Submitting

1. **Tests pass**: `uv run pytest`
2. **Linting passes**: `uv run ruff check .`
3. **New features have tests**
4. **Documentation updated** (if applicable)

### PR Title Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: Add custom validation support`
- `fix: Handle empty feedback list correctly`
- `docs: Update installation instructions`
- `test: Add edge case tests for insights`
- `refactor: Simplify database connection logic`

### PR Description Template

```markdown
## Summary
Brief description of changes.

## Changes
- Added X
- Fixed Y
- Updated Z

## Testing
How were these changes tested?

## Breaking Changes
None / List any breaking changes
```

## Project Structure

```
fastmcp-feedback/
├── src/fastmcp_feedback/
│   ├── __init__.py       # Public API exports
│   ├── tools.py          # Main add_feedback_tools function
│   ├── models.py         # Pydantic models and SQLAlchemy ORM
│   ├── database.py       # Database connection management
│   ├── feedback.py       # Standalone server factory
│   ├── insights.py       # Privacy-compliant analytics
│   └── mixins/           # Modular tool mixins
│       ├── base.py
│       ├── submission.py
│       ├── retrieval.py
│       └── management.py
├── tests/
│   ├── conftest.py       # Shared fixtures
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── pyproject.toml        # Package configuration
├── README.md
├── CONTRIBUTING.md       # This file
├── CHANGELOG.md
└── LICENSE
```

## Adding New Features

### Adding a New Mixin

1. Create `src/fastmcp_feedback/mixins/your_mixin.py`
2. Inherit from `BaseMixin`
3. Implement `register_tools(app, prefix="")`
4. Export from `src/fastmcp_feedback/mixins/__init__.py`
5. Add to main `__init__.py` exports
6. Write tests in `tests/unit/test_your_mixin.py`
7. Update documentation

### Adding a New Tool

1. Add to appropriate mixin or create new one
2. Use `@app.tool()` decorator with clear description
3. Add Pydantic models for request/response if complex
4. Write unit tests
5. Add integration test
6. Document in README

## Versioning

We use **calendar versioning** (CalVer): `YYYY.MM.DD`

Version bumps happen automatically on release. Contributors don't need to update version numbers.

## Getting Help

- **Questions**: Open a discussion on the repository
- **Bugs**: Open an issue with reproduction steps
- **Features**: Open an issue describing the use case

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
