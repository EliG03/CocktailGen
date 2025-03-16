'''
This file contains the tests for the __init__.py file.
'''
import os
from unittest.mock import patch, MagicMock
from website import create_app

def mock_db():
    '''
    Mock SQLAlchemy for testing
    '''
    with patch("website.db") as mock_db_instance:
        mock_db_instance.init_app = MagicMock()
        mock_db_instance.create_all = MagicMock()
        yield mock_db_instance

def test_database_setup():
    """
    Test that the database setup correctly initializes without connecting.
    """
    with patch.dict(os.environ, {"CONFIG_TYPE": "", "DATABASE_URL": "sqlite:///:memory:"}):
        with patch("website.db.create_all") as mock_create_all:
            app = create_app()
            mock_create_all.assert_called_once()

def test_database_setup_no_postgres():
    '''
    Test that the database setup correctly initializes without connecting.
    '''
    with patch.dict(os.environ, {"CONFIG_TYPE": "", "DATABASE_URL": ""}):
        app = create_app()
        assert app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite")
