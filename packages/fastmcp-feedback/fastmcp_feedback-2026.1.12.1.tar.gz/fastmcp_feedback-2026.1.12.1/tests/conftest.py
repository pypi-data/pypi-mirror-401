"""Pytest configuration and fixtures for FastMCP Feedback tests."""

import asyncio
import os
import tempfile
from typing import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from fastmcp import FastMCP
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastmcp_feedback.database import FeedbackDatabase
from fastmcp_feedback.insights import FeedbackInsights  
from fastmcp_feedback.models import Base, Feedback, FeedbackType, FeedbackStatus


@pytest_asyncio.fixture
async def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_db_path() -> Generator[str, None, None]:
    """Create a temporary database file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_path = f.name
    
    yield temp_path
    
    # Clean up
    try:
        os.unlink(temp_path)
    except FileNotFoundError:
        pass


@pytest.fixture  
def memory_db_url() -> str:
    """In-memory SQLite database URL for testing."""
    return "sqlite:///:memory:"


@pytest_asyncio.fixture
async def test_database(memory_db_url: str) -> FeedbackDatabase:
    """Create a test database instance with proper async initialization and cleanup."""
    db = FeedbackDatabase(memory_db_url)
    await db.initialize()
    try:
        yield db
    finally:
        # Ensure database is always properly closed
        await db.close()


@pytest.fixture
def test_insights() -> FeedbackInsights:
    """Create a test insights instance with analytics enabled."""
    return FeedbackInsights(enabled=True)


@pytest.fixture
def disabled_insights() -> FeedbackInsights:
    """Create a test insights instance with analytics disabled."""
    return FeedbackInsights(enabled=False)


@pytest.fixture
def sample_feedback_data() -> dict:
    """Sample feedback data for testing."""
    return {
        "type": "bug",
        "title": "Application crashes on startup",
        "description": "The app crashes immediately after launching on iOS 17",
        "submitter": "test_user",
        "contact_info": "test@example.com"
    }


@pytest.fixture
def multiple_feedback_data() -> list:
    """Multiple feedback items for testing."""
    return [
        {
            "type": "bug",
            "title": "Login button broken",
            "description": "Cannot click login button",
            "submitter": "user1",
            "contact_info": "user1@test.com"
        },
        {
            "type": "feature", 
            "title": "Add dark mode",
            "description": "Please add dark mode support",
            "submitter": "user2",
            "contact_info": "user2@test.com"
        },
        {
            "type": "improvement",
            "title": "Faster loading",
            "description": "App loads slowly on older devices",
            "submitter": "user3"
        }
    ]


@pytest.fixture
def mock_fastmcp_server() -> FastMCP:
    """Create a mock FastMCP server for testing."""
    return FastMCP("Test Feedback Server")


@pytest_asyncio.fixture
async def populated_database(test_database: FeedbackDatabase, multiple_feedback_data: list) -> FeedbackDatabase:
    """Database populated with test data."""
    async with test_database.session() as session:
        for data in multiple_feedback_data:
            feedback = Feedback(**data)
            session.add(feedback)
        session.commit()
    
    return test_database


# Test data helpers

@pytest.fixture
def valid_feedback_request():
    """Valid feedback request for testing."""
    from fastmcp_feedback.mixins import SubmitFeedbackRequest
    return SubmitFeedbackRequest(
        type="bug",
        title="Test bug report", 
        description="This is a test bug report for unit testing",
        submitter="test_user"
    )


@pytest.fixture
def invalid_feedback_request():
    """Invalid feedback request for testing validation."""
    return {
        "type": "invalid_type",  # Invalid type
        "title": "",  # Empty title
        "description": "Test description",
        "submitter": ""  # Empty submitter
    }


# Mock objects

@pytest.fixture
def mock_session():
    """Mock database session."""
    session = MagicMock()
    session.add = MagicMock()
    session.commit = MagicMock()
    session.rollback = MagicMock()
    session.flush = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None
    session.query.return_value.count.return_value = 0
    session.query.return_value.all.return_value = []
    return session


@pytest.fixture
def mock_database(mock_session):
    """Mock database with session."""
    db = MagicMock()
    db.get_session.return_value.__enter__.return_value = mock_session
    db.get_session.return_value.__exit__.return_value = None
    return db


# Environment helpers

@pytest.fixture(autouse=True)
def clean_environment():
    """Ensure clean environment for each test."""
    # Store original values
    original_env = {}
    env_vars_to_clean = [
        'FEEDBACK_DATABASE_URL',
        'FEEDBACK_INSIGHTS_ENABLED',
        'FEEDBACK_INSIGHTS_RETENTION_DAYS'
    ]
    
    for var in env_vars_to_clean:
        original_env[var] = os.environ.get(var)
        if var in os.environ:
            del os.environ[var]
    
    yield
    
    # Restore original values
    for var, value in original_env.items():
        if value is not None:
            os.environ[var] = value
        elif var in os.environ:
            del os.environ[var]


# Performance testing helpers

@pytest.fixture
def performance_timer():
    """Simple performance timer for testing."""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        @property
        def duration_ms(self):
            if self.start_time and self.end_time:
                return (self.end_time - self.start_time) * 1000
            return None
    
    return Timer()


# Pytest-html configuration for beautiful test reports

def pytest_html_report_title(report):
    """Customize the HTML report title."""
    report.title = "🗣️ FastMCP Feedback - Test Results"


def pytest_html_results_table_header(cells):
    """Customize the HTML report table headers with enhanced information."""
    cells.insert(2, '<th class="sortable col-category" style="color: #ebdbb2; background: #504945;">Category</th>')
    cells.insert(3, '<th class="sortable col-markers" style="color: #ebdbb2; background: #504945;">Markers</th>')
    cells.insert(4, '<th class="sortable col-duration" style="color: #ebdbb2; background: #504945;">Duration</th>')


def pytest_html_results_table_row(report, cells):
    """Customize the HTML report table rows with comprehensive information."""
    # Determine test category based on file path and markers
    category = "Other"
    category_color = "#928374"
    
    if "unit/" in report.nodeid:
        category = "Unit"
        category_color = "#98971a"  # Green
    elif "integration/" in report.nodeid:
        category = "Integration" 
        category_color = "#458588"  # Blue
    elif hasattr(report, 'keywords'):
        if 'performance' in report.keywords:
            category = "Performance"
            category_color = "#b16286"  # Purple
        elif 'smoke' in report.keywords:
            category = "Smoke"
            category_color = "#d79921"  # Yellow
        elif 'mcp' in report.keywords:
            category = "MCP"
            category_color = "#689d6a"  # Aqua
        elif 'database' in report.keywords:
            category = "Database"
            category_color = "#d65d0e"  # Orange
    
    # Format test category with color
    category_cell = f'<td><span style="color: {category_color}; font-weight: bold;">📁 {category}</span></td>'
    cells.insert(2, category_cell)
    
    # Extract and format markers
    markers = []
    if hasattr(report, 'keywords'):
        test_markers = ['unit', 'integration', 'performance', 'smoke', 'mcp', 'database', 'network', 'benchmark']
        for marker in test_markers:
            if marker in report.keywords:
                markers.append(marker)
    
    if markers:
        markers_str = " • ".join([f'<span style="color: #928374; font-size: 0.8em;">{m}</span>' for m in markers])
    else:
        markers_str = '<span style="color: #504945;">—</span>'
    
    cells.insert(3, f'<td style="font-family: monospace; font-size: 0.85em;">{markers_str}</td>')
    
    # Format duration with performance-based coloring
    duration = getattr(report, 'duration', 0)
    if duration > 2.0:
        duration_str = f'<span style="color: #cc241d; font-weight: bold;">⚠️ {duration:.3f}s</span>'
    elif duration > 1.0:
        duration_str = f'<span style="color: #d79921; font-weight: bold;">⏰ {duration:.3f}s</span>'
    elif duration > 0.5:
        duration_str = f'<span style="color: #928374;">⏱️ {duration:.3f}s</span>'
    else:
        duration_str = f'<span style="color: #689d6a;">⚡ {duration:.3f}s</span>'
    
    cells.insert(4, f'<td style="font-family: monospace; font-size: 0.9em;">{duration_str}</td>')


def pytest_html_results_table_html(report, data):
    """Add custom styling and JavaScript to test results."""
    if report.passed:
        data.append('<tr class="passed">')
    elif report.failed:
        data.append('<tr class="failed">')
    elif report.skipped:
        data.append('<tr class="skipped">')
    else:
        data.append('<tr class="error">')


# Custom markers for test organization

def pytest_configure(config):
    """Register custom markers and configure beautiful reporting."""
    # Register custom markers
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual components"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests for component interaction"
    )
    config.addinivalue_line(
        "markers", "performance: Performance and benchmarking tests"
    )
    config.addinivalue_line(
        "markers", "smoke: Basic functionality smoke tests"
    )
    config.addinivalue_line(
        "markers", "mcp: MCP server integration tests"
    )
    config.addinivalue_line(
        "markers", "database: Tests requiring database setup"
    )
    config.addinivalue_line(
        "markers", "network: Tests requiring network connectivity"
    )
    config.addinivalue_line(
        "markers", "benchmark: Benchmark tests with performance assertions"
    )
    
    # Apply custom CSS styling to pytest-html reports
    from pathlib import Path
    css_file = Path(__file__).parent / "templates" / "style.css"
    if css_file.exists() and hasattr(config.option, 'css'):
        if not config.option.css:
            config.option.css = []
        config.option.css.append(str(css_file))


def pytest_html_results_summary(prefix, summary, postfix):
    """Enhance HTML report with beautiful summary section."""
    prefix.extend([
        '<div style="background: linear-gradient(135deg, #458588, #689d6a); '
        'padding: 20px; border-radius: 8px; margin: 20px 0; color: white; text-align: center;">',
        '<h2 style="margin: 0; font-size: 2.2em; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">'
        '🎯 FastMCP Feedback Test Dashboard</h2>',
        '<p style="margin: 10px 0 0 0; opacity: 0.9; font-family: monospace; font-size: 1.1em;">'
        'Comprehensive Quality Assurance & Reliability Testing</p>',
        '</div>'
    ])
    
    # Add custom test categories summary
    postfix.extend([
        '<div style="background: #3c3836; padding: 15px; border-radius: 6px; '
        'margin: 15px 0; border-left: 4px solid #689d6a;">',
        '<h3 style="color: #ebdbb2; margin: 0 0 10px 0;">📊 Test Categories Overview</h3>',
        '<p style="color: #928374; font-family: monospace; font-size: 0.9em; margin: 0;">'
        'Unit • Integration • Performance • Smoke • MCP • Database</p>',
        '</div>'
    ])