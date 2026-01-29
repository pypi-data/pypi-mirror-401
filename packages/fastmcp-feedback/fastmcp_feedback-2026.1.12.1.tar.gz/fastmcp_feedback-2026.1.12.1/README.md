# FastMCP Feedback

Production-ready feedback collection system for [FastMCP](https://gofastmcp.com) servers.

Add structured feedback collection (bug reports, feature requests, general feedback) to any FastMCP server with a single line of code.

## Features

- **One-Line Integration** - Add feedback tools to any FastMCP server instantly
- **Modular Mixins** - Selective tool registration for fine-grained control
- **Multi-Database Support** - SQLite (dev), PostgreSQL, MySQL (production)
- **Privacy-Compliant Analytics** - Optional usage insights without sensitive data
- **Type-Safe** - Full Pydantic validation and type hints
- **Well-Tested** - 97%+ test coverage

## Installation

### From PyPI (Recommended)

```bash
# Using uv (recommended)
uv add fastmcp-feedback

# Using pip
pip install fastmcp-feedback

# With PostgreSQL support
uv add "fastmcp-feedback[postgresql]"
```

### From Git (Latest Development)

```bash
# Latest from main branch
uv add git+https://git.supported.systems/fastmcp-feedback/fastmcp-feedback.git

# Specific release tag
uv add git+https://git.supported.systems/fastmcp-feedback/fastmcp-feedback.git@2026.01.12

# Specific branch (for testing PRs)
uv add git+https://git.supported.systems/fastmcp-feedback/fastmcp-feedback.git@feature-branch
```

### Local Development Install

For contributors or local modifications:

```bash
# Clone the repository
git clone git@git.supported.systems:fastmcp-feedback/fastmcp-feedback.git
cd fastmcp-feedback

# Create virtual environment and install in editable mode
uv venv
uv pip install -e ".[dev]"

# Run tests to verify
uv run pytest
```

## Quick Start

### Basic Integration (One Line)

```python
from fastmcp import FastMCP
from fastmcp_feedback import add_feedback_tools

app = FastMCP("My Server")
add_feedback_tools(app)  # Adds 4 feedback tools instantly!

# That's it! Your server now has:
# - submit_feedback: Collect bug reports, feature requests, general feedback
# - list_feedback: Retrieve and filter feedback items
# - get_feedback_stats: Aggregate statistics
# - update_feedback_status: Workflow management (new → reviewing → resolved)
```

### With Custom Database

```python
# SQLite with custom path
add_feedback_tools(app, database_url="sqlite:///./data/feedback.db")

# PostgreSQL for production
add_feedback_tools(app, database_url="postgresql://user:pass@localhost/mydb")
```

### With Analytics Enabled

```python
add_feedback_tools(app, enable_insights=True)
# Enables privacy-compliant usage tracking
```

## Advanced Usage

### Mixin Architecture

For fine-grained control over which tools are exposed:

```python
from fastmcp_feedback import (
    SubmissionMixin,
    RetrievalMixin,
    ManagementMixin,
    get_database_session,
)

db_session = get_database_session("sqlite:///feedback.db")

# Only expose submission (public-facing)
submission = SubmissionMixin(db_session)
submission.register_tools(app)

# Add retrieval with custom prefix
retrieval = RetrievalMixin(db_session)
retrieval.register_tools(app, prefix="analytics_")

# Admin-only management tools
management = ManagementMixin(db_session)
management.register_tools(admin_app, prefix="admin_")
```

### Available Mixins

| Mixin | Tools | Use Case |
|-------|-------|----------|
| `SubmissionMixin` | `submit_feedback` | Public feedback collection |
| `RetrievalMixin` | `list_feedback`, `get_feedback_stats` | Dashboards, reporting |
| `ManagementMixin` | `update_feedback_status` | Admin workflow |
| `InsightsMixin` | `record_insight`, `get_insights_summary` | Analytics |

### Multi-Tenant Pattern

```python
# Each tenant gets isolated database
def get_tenant_tools(tenant_id: str):
    session = get_database_session(f"sqlite:///data/{tenant_id}.db")
    submission = SubmissionMixin(session)
    submission.register_tools(app, prefix=f"tenant_{tenant_id}_")
```

### Server Composition

```python
from fastmcp_feedback import create_feedback_server

# Create dedicated feedback server
feedback_server = create_feedback_server("Feedback API")

# Compose into main application
main_app.import_server(feedback_server, prefix="feedback_")
```

## API Reference

### `add_feedback_tools(app, database_url=None, enable_insights=False)`

Add all feedback tools to a FastMCP server.

**Parameters:**
- `app`: FastMCP server instance
- `database_url`: Database connection string (default: `sqlite:///feedback.db`)
- `enable_insights`: Enable privacy-compliant analytics (default: `False`)

### Feedback Types

- `bug_report` - Bug reports with severity levels
- `feature_request` - Feature suggestions with priority
- `general` - General feedback and comments

### Status Workflow

`new` → `reviewing` → `planned` → `in_progress` → `resolved` / `wont_fix`

## Documentation

Full documentation: https://fastmcp-feedback.l.supported.systems

- [Quick Start Guide](https://fastmcp-feedback.l.supported.systems/guides/quickstart/)
- [Architecture Overview](https://fastmcp-feedback.l.supported.systems/reference/architecture/)
- [API Reference](https://fastmcp-feedback.l.supported.systems/reference/api/)
- [Examples](https://fastmcp-feedback.l.supported.systems/examples/)

## Examples

See the [fastmcp-feedback-showcase](https://git.supported.systems/fastmcp-feedback/fastmcp-example) repository for comprehensive examples demonstrating all capabilities:

```bash
uvx fastmcp-feedback-showcase  # Run full demo
```

## Contributing

We welcome contributions! FastMCP Feedback is designed to be contributor-friendly.

### Quick Contribution Setup

```bash
# Fork and clone
git clone git@git.supported.systems:YOUR_USERNAME/fastmcp-feedback.git
cd fastmcp-feedback

# Install with dev dependencies
uv venv
uv pip install -e ".[dev]"

# Create feature branch
git checkout -b feature/your-feature

# Make changes, run tests
uv run pytest
uv run ruff check .

# Submit PR
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Versioning

This project uses **calendar versioning** (CalVer): `YYYY.MM.DD`

- `2026.01.12` = Release on January 12, 2026
- Multiple releases on same day: `2026.01.12.1`, `2026.01.12.2`

This makes it clear when each release was made and simplifies dependency management.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- **Documentation**: https://fastmcp-feedback.l.supported.systems
- **Repository**: https://git.supported.systems/fastmcp-feedback/fastmcp-feedback
- **Issues**: https://git.supported.systems/fastmcp-feedback/fastmcp-feedback/issues
- **Showcase**: https://git.supported.systems/fastmcp-feedback/fastmcp-example
- **FastMCP**: https://gofastmcp.com
