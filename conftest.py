# conftest.py

import pytest
from app import app as flask_app, db

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    # Configure the app for testing
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use an in-memory DB
    })

    with flask_app.app_context():
        db.create_all()  # Create all database tables

    yield flask_app

    with flask_app.app_context():
        db.drop_all()  # Clean up the database

@pytest.fixture()
def client(app):
    """A test client for the app."""
    return app.test_client()