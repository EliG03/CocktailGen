'''
This file contains the fixtures for the tests.
'''

import os
from contextlib import contextmanager
from unittest.mock import patch, MagicMock
import pytest
from dotenv import load_dotenv
from website import create_app, db

load_dotenv(dotenv_path = ".env.test")

@pytest.fixture()
def test_client():
    '''
    Flask test client for testing the application.
    '''

    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    flask_app = create_app()
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as test_client:
        yield test_client


@pytest.fixture()
def mock_openai_client():
    '''
    Mock the OpenAI client for testing the application.
    '''
    @contextmanager
    def _mock_openai_client(response=None):
        mock_client = MagicMock()
        mock_completion = MagicMock()

        # Simulate success or failure based on `response`
        if response is None:
            mock_completion.choices = []  # Simulate failure
        else:
            mock_choice = MagicMock()
            mock_choice.message = MagicMock()
            mock_choice.message.content = response
            mock_completion.choices = [mock_choice]

        mock_client.chat.completions.create.return_value = mock_completion

        with patch('website.views.OpenAI', return_value=mock_client):
            yield mock_client

    return _mock_openai_client

@pytest.fixture
def mock_db():
    '''
    Mock the database for testing the application.
    '''
    with patch.object(db, "init_app") as mock_init, patch.object(db, "create_all") as mock_create:
        yield mock_init, mock_create
