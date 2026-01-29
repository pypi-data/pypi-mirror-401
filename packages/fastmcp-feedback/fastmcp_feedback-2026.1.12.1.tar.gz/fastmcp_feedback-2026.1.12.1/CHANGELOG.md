# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) (YYYY.MM.DD).

## [2026.01.12] - 2026-01-12

### Added
- Initial public release
- Core feedback tools: `submit_feedback`, `list_feedback`, `get_feedback_stats`, `update_feedback_status`
- `add_feedback_tools()` one-line integration function
- Modular mixin architecture:
  - `SubmissionMixin` - feedback collection
  - `RetrievalMixin` - listing and statistics
  - `ManagementMixin` - status workflow management
  - `InsightsMixin` - privacy-compliant analytics
- Multi-database support: SQLite, PostgreSQL, MySQL
- `create_feedback_server()` for server composition
- Comprehensive test suite (97%+ coverage)
- Full type hints and Pydantic validation
- Documentation site at https://fastmcp-feedback.l.supported.systems

### Technical Details
- Built on FastMCP 2.12.2+
- SQLAlchemy 2.0+ ORM
- Pydantic 2.11+ validation
- Python 3.11+ required
